from collections import defaultdict

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.ingestion_run import IngestionRun
from app.models.supplier import Supplier

router = APIRouter()


@router.get("/reports/unmapped-columns")
async def get_unmapped_columns(
    supplier_name: str | None = Query(default=None),
    min_confidence: int = Query(default=0),
    session: AsyncSession = Depends(get_db),
):
    query = (
        select(
            IngestionRun,
            Supplier,
        )
        .join(
            Supplier,
            Supplier.id == IngestionRun.supplier_id,
        )
        .order_by(IngestionRun.created_at.desc())
    )

    if supplier_name:
        query = query.where(
            Supplier.name == supplier_name.strip().lower()
        )

    result = await session.execute(query)
    rows = result.all()

    grouped = defaultdict(
        lambda: {
            "count": 0,
            "suppliers": set(),
            "examples": [],
        }
    )

    for ingestion_run, supplier in rows:
        report = ingestion_run.normalization_report or []

        for item in report:
            if item.get("mapped_to"):
                continue

            confidence = item.get("confidence") or 0

            if confidence < min_confidence:
                continue

            column = item.get("column")
            key = column

            grouped[key]["count"] += 1
            grouped[key]["suppliers"].add(supplier.name)

            if len(grouped[key]["examples"]) < 3:
                grouped[key]["examples"].append(
                    {
                        "supplier": supplier.name,
                        "ingestion_run_id": ingestion_run.id,
                        "filename": ingestion_run.filename,
                        "cleaned_column": item.get("cleaned_column"),
                        "tokens": item.get("tokens"),
                        "confidence": confidence,
                        "matched_synonym": item.get("matched_synonym"),
                        "alternatives": item.get("alternatives"),
                    }
                )

    items = []

    for column, data in grouped.items():
        items.append(
            {
                "column": column,
                "count": data["count"],
                "suppliers": sorted(data["suppliers"]),
                "examples": data["examples"],
            }
        )

    items = sorted(
        items,
        key=lambda item: item["count"],
        reverse=True,
    )

    return {
        "total_unmapped_columns": len(items),
        "items": items,
    }