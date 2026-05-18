from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.supplier import Supplier
from app.models.ingestion_run import IngestionRun
from app.models.supplier_column_mapping import SupplierColumnMapping


async def get_or_create_supplier(
    session: AsyncSession,
    supplier_name: str,
) -> Supplier:
    normalized_name = supplier_name.strip().lower()

    result = await session.execute(
        select(Supplier).where(Supplier.name == normalized_name)
    )
    supplier = result.scalar_one_or_none()

    if supplier:
        return supplier

    supplier = Supplier(name=normalized_name)

    session.add(supplier)

    await session.flush()

    return supplier


async def save_ingestion_run(
    session: AsyncSession,
    supplier_id: int,
    filename: str,
    rows_total: int,
    rows_valid: int,
    rows_failed: int,
    normalization_report: list[dict],
) -> IngestionRun:
    run = IngestionRun(
        supplier_id=supplier_id,
        filename=filename,
        status="completed",
        rows_total=rows_total,
        rows_valid=rows_valid,
        rows_failed=rows_failed,
        normalization_report=normalization_report,
    )

    session.add(run)

    await session.flush()

    return run


async def save_column_mappings(
    session: AsyncSession,
    supplier_id: int,
    normalization_report: list[dict],
) -> int:
    # Replace mappings for this supplier instead of endlessly duplicating them
    await session.execute(
        delete(SupplierColumnMapping).where(
            SupplierColumnMapping.supplier_id == supplier_id
        )
    )

    count = 0

    for item in normalization_report:
        mapped_to = item.get("mapped_to")

        if not mapped_to:
            continue

        mapping = SupplierColumnMapping(
            supplier_id=supplier_id,
            source_column=item["column"],
            target_column=mapped_to,
            confidence=item["confidence"],
        )

        session.add(mapping)

        count += 1

    await session.flush()

    return count