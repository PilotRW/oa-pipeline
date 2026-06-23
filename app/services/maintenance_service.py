from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.import_draft_service import (
    clear_import_drafts,
    get_import_draft_stats,
)


DATABASE_DATA_TABLES = [
    "deal_candidates",
    "amazon_presence_checks",
    "keepa_product_metrics",
    "amazon_product_matches",
    "offer_research_queue",
    "supplier_offers",
    "supplier_column_mappings",
    "ingestion_runs",
]


class MaintenanceService:
    def __init__(self, db: AsyncSession):
        self.db = db

    def clear_workspace(self) -> dict:
        return {
            "status": "ok",
            **clear_import_drafts(),
        }

    async def get_status(self) -> dict:
        database = await self._database_stats()

        return {
            "status": "ok",
            "workspace": get_import_draft_stats(),
            "database": database,
        }

    async def _database_stats(self) -> dict:
        counts = {}
        sizes = {}

        for table_name in DATABASE_DATA_TABLES:
            count_result = await self.db.execute(
                text(f"SELECT count(*) FROM {table_name}")
            )
            size_result = await self.db.execute(
                text(
                    "SELECT pg_total_relation_size("
                    "to_regclass(:table_name)"
                    ")"
                ),
                {"table_name": table_name},
            )
            counts[table_name] = int(count_result.scalar_one())
            sizes[table_name] = int(size_result.scalar_one() or 0)

        return {
            "rows": sum(counts.values()),
            "estimated_bytes": sum(sizes.values()),
            "tables": {
                table_name: {
                    "rows": counts[table_name],
                    "estimated_bytes": sizes[table_name],
                }
                for table_name in DATABASE_DATA_TABLES
            },
        }

    async def clear_database_data(self) -> dict:
        before = await self._database_stats()

        table_list = ", ".join(DATABASE_DATA_TABLES)
        await self.db.execute(
            text(
                f"TRUNCATE TABLE {table_list} "
                "RESTART IDENTITY"
            )
        )
        await self.db.commit()
        after = await self._database_stats()

        return {
            "status": "ok",
            "tables_cleared": {
                table_name: table["rows"]
                for table_name, table in before["tables"].items()
            },
            "rows_cleared": before["rows"],
            "estimated_bytes_released": max(
                before["estimated_bytes"] - after["estimated_bytes"],
                0,
            ),
            "database_after": after,
            "preserved": [
                "suppliers",
                "pipeline_settings",
                "research_rules",
            ],
        }
