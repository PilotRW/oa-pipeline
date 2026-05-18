# OA Pipeline

Backend pipeline for ecommerce Online Arbitrage automation.

## Current status

✅ FastAPI backend  
✅ PostgreSQL database  
✅ SQLAlchemy models  
✅ Alembic migrations  
✅ Supplier CSV / Excel ingestion  
✅ Header auto-detection  
✅ Multilingual column normalization  
✅ Fuzzy column matching  
✅ Supplier offer persistence  
✅ Feed refresh / duplicate handling  
✅ Unmapped-column analytics  
🚧 Comparison Engine MVP — current stage

---

## Project structure

```text
oa-pipeline/
├── alembic/
│   ├── versions/
│   ├── env.py
│   ├── README
│   └── script.py.mako
│
├── app/
│   ├── api/
│   │   ├── ingestion.py
│   │   └── comparison.py
│   │
│   ├── config/
│   │   └── settings.py
│   │
│   ├── db/
│   │   └── database.py
│   │
│   ├── ingestion/
│   │   ├── column_normalizer.py
│   │   ├── excel_reader.py
│   │   ├── csv_reader.py
│   │   ├── cleaners.py
│   │   └── mappings.py
│   │
│   ├── models/
│   │   ├── supplier.py
│   │   ├── supplier_offer.py
│   │   ├── ingestion_run.py
│   │   ├── supplier_column_mapping.py
│   │   ├── product_cluster.py
│   │   ├── cluster_offer.py
│   │   └── cluster_price_stats.py
│   │
│   ├── services/
│   │   ├── ingestion_service.py
│   │   └── comparison_service.py
│   │
│   └── main.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── docker/
│
├── .env
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md