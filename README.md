# oa-pipeline

Data pipeline for online arbitrage:
supplier offers → ASIN mapping → market data → ROI analysis.

---

## Project Structure

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
│   ├── config/
│   │   └── settings.py
│   │
│   ├── db/
│   │   └── database.py
│   │
│   ├── ingestion/
│   │
│   ├── models/
│   │   └── supplier_offer.py
│   │
│   ├── services/
│   │
│   └── main.py
│
├── data/
│
├── docker/
│
├── .env
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md