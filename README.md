# OA Pipeline

Backend pipeline for ecommerce Online Arbitrage automation.

The project ingests supplier feeds, normalizes and stores supplier offers,
queues offers for Amazon research, enriches matched products with marketplace
metrics, evaluates profitability, and produces deal candidates.

## Current Status

Implemented:

- FastAPI backend
- PostgreSQL database
- SQLAlchemy async models
- Alembic migrations
- CSV and Excel supplier feed ingestion
- Header auto-detection
- Multilingual column normalization
- Fuzzy column matching
- Supplier offer persistence and feed refresh
- Unmapped-column reporting
- Research queue population and priority scoring
- Configurable research rules and scoring weights
- Mock Amazon EAN to ASIN matching
- Mock Keepa metric enrichment
- Deal candidate generation
- Pipeline batch orchestration
- Config API with Pydantic validation for future UI use
- Static FastAPI-hosted control panel at `/ui/`
- UI language switcher for English, German, and Ukrainian

Current stage:

- Removing hardcoded business and operational rules
- Making pipeline behavior configurable through API-backed settings
- Preparing backend contracts for a future UI

Not implemented yet:

- Real FBA/VAT/shipping fee engine
- Frontend UI
- Supplier-specific rules

## Pipeline Flow

```text
Supplier feeds
    -> supplier_offers
    -> offer_research_queue
    -> amazon_product_matches
    -> keepa_product_metrics
    -> deal_candidates
```

Main queue status flow:

```text
needs_amazon_match
    -> matched
    -> keepa_pending
    -> keepa_completed
    -> deal_candidate
```

Alternative states:

```text
amazon_match_not_found
rejected_low_roi
rejected_unprofitable
```

## Configuration Model

The project intentionally separates technical settings from business rules.

Technical settings live in `pipeline_settings`:

- `use_real_keepa`
- `default_batch_size`
- `default_marketplace`

Business rules live in `research_rules`:

- priority score threshold
- stock thresholds
- cost ranges
- scoring weights
- ROI and profit thresholds
- fee assumptions
- sales rank and monthly sales filters
- Amazon-in-stock exclusion

Stock is intentionally not a hard blocker for research queue population. Some
suppliers may allow ordering even when stock appears unavailable, so stock only
affects priority score.

## API Endpoints

Upload:

```text
POST /upload/preview
POST /upload/commit
POST /upload
```

The UI uses the two-step import flow: upload a supplier file for preview first,
then commit the import after column normalization and sample rows look correct.
The legacy `POST /upload` endpoint still performs a direct save for scripts or
manual API use.

Reports:

```text
GET /reports/unmapped-columns
```

Research queue:

```text
POST /research-queue/populate
POST /research-queue/recalculate-priority
GET  /research-queue/
```

Amazon matching:

```text
POST /amazon-matches/create-pending
POST /amazon-matches/process-pending
GET  /amazon-matches/
```

Keepa:

```text
POST /keepa/create-pending
POST /keepa/process-pending
GET  /keepa/
```

Deals:

```text
POST /deals/create-candidates
GET  /deals/
```

Pipeline:

```text
POST /pipeline/run-batch
GET  /pipeline/summary
```

Config:

```text
GET   /config/pipeline-settings
PATCH /config/pipeline-settings

GET   /config/research-rules
PATCH /config/research-rules
```

`PATCH /config/*` uses Pydantic schemas with partial updates, forbidden
unknown fields, and validation designed for UI clients.

## Run Locally

Start the stack:

```bash
docker compose up --build
```

Apply migrations:

```bash
docker compose exec app alembic upgrade head
```

Check API health:

```bash
curl http://localhost:8000/
```

Check pipeline summary:

```bash
curl http://localhost:8000/pipeline/summary
```

Open the control panel:

```text
http://localhost:8000/ui/
```

Run one pipeline batch:

```bash
curl -X POST http://localhost:8000/pipeline/run-batch
```

## Environment

Required:

```text
DATABASE_URL
ALEMBIC_DATABASE_URL
```

Optional:

```text
KEEPA_API_KEY
USE_KEEPA_REAL_API
```

Current provider behavior:

- `pipeline_settings.use_real_keepa=false` uses mock Amazon matching and mock
  Keepa metrics.
- `pipeline_settings.use_real_keepa=true` uses Keepa for Amazon EAN to ASIN
  matching and Keepa metric enrichment.
- If real Keepa mode is enabled without a valid `KEEPA_API_KEY`, processing
  returns a controlled `not_configured` result instead of falling back to mock
  data or raising a server error.

## Project Structure

```text
oa-pipeline/
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── app/
│   ├── api/
│   │   ├── amazon_matches.py
│   │   ├── config.py
│   │   ├── config_schemas.py
│   │   ├── deals.py
│   │   ├── keepa.py
│   │   ├── pipeline.py
│   │   ├── reports.py
│   │   ├── research_queue.py
│   │   └── upload.py
│   ├── config/
│   │   └── settings.py
│   ├── db/
│   │   ├── database.py
│   │   └── session.py
│   ├── ingestion/
│   │   ├── cleaners.py
│   │   ├── normalizer.py
│   │   ├── parser.py
│   │   ├── schemas.py
│   │   └── synonyms.py
│   ├── models/
│   │   ├── amazon_product_match.py
│   │   ├── deal_candidate.py
│   │   ├── ingestion_run.py
│   │   ├── keepa_product_metric.py
│   │   ├── offer_research_queue.py
│   │   ├── pipeline_setting.py
│   │   ├── research_rule.py
│   │   ├── supplier.py
│   │   ├── supplier_column_mapping.py
│   │   └── supplier_offer.py
│   ├── services/
│   │   ├── amazon_match_service.py
│   │   ├── config_service.py
│   │   ├── deal_service.py
│   │   ├── ingestion_service.py
│   │   ├── keepa_service.py
│   │   ├── marketplace.py
│   │   ├── pipeline_service.py
│   │   ├── research_queue_service.py
│   │   └── supplier_offer_service.py
│   ├── static/
│   │   ├── app.js
│   │   ├── index.html
│   │   └── styles.css
│   └── main.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## Development Notes

- Do not add new hardcoded business thresholds in service code.
- Put business rules in `research_rules`.
- Put operational/provider settings in `pipeline_settings`.
- Keep temporary mock provider values inside mock/provider code rather than
  exposing them as user-facing settings.
- Comparison engine work is postponed until multiple overlapping supplier
  catalogs exist.
