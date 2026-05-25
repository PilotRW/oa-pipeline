# Mirenelle Automation / OA Pipeline

Backend and local control panel for ecommerce Online Arbitrage automation.

The project ingests supplier catalog files, normalizes supplier offers, queues
offers for Amazon research, enriches matched products with marketplace metrics,
evaluates profitability, and produces ranked deal candidates.

## Current Status

Implemented:

- FastAPI backend with PostgreSQL, async SQLAlchemy models, and Alembic
  migrations.
- Static FastAPI-hosted UI at `/ui/`, branded as Mirenelle Automation.
- UI localization for English, German, and Ukrainian.
- CSV and Excel supplier feed ingestion.
- Two-step import flow: preview first, then save.
- Human-readable import preview table, column mapping preview, and quality
  checks.
- Multilingual semantic column normalization and fuzzy matching.
- Supplier offer persistence, feed refresh, and duplicate prevention.
- Supplier management with visible/hidden toggle.
- Supplier detail page with offer stats, pipeline status, import history, recent
  offers, supplier scope actions, and supplier-scoped research.
- Supplier-scoped Overview, Research, Pipeline, Deals, and issue exports.
- Supplier-specific research rule profiles with reset-to-default behavior.
- Research queue population, priority scoring, and rejection reasons.
- Configurable `pipeline_settings` and `research_rules`.
- Help buttons for each research-rule metric in the UI.
- Mock Amazon EAN to ASIN matching.
- Keepa wrapper with mock mode, real Keepa mode, status checks, and
  not-configured handling.
- Mock fee estimation and deal candidate generation.
- Pipeline orchestration endpoints.
- Pipeline issue modals with CSV and real XLSX downloads.

Current stage:

- The backend and UI are being shaped into a supplier-driven operator console.
- Business rules are moving into `research_rules`.
- Operational/provider settings are moving into `pipeline_settings`.
- Supplier visibility now controls default UI/list behavior without deleting
  historical data.

Still not production-grade:

- Amazon matching is still mock unless real Keepa mode is enabled.
- Keepa metrics are mock unless real Keepa mode is enabled.
- Fee estimation is still simplified.
- No real FBA/VAT/shipping fee engine yet.
- No Grafana dashboards or candidate review enrichment tables yet.

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

## UI

Open the local control panel:

```text
http://localhost:8000/ui/
```

Main UI areas:

- `Overview`: summary metrics, pipeline issues, and scrollable deal candidates.
- `Pipeline`: batch pipeline run controls.
- `Settings`: technical pipeline settings.
- `Rules`: business and scoring rules, grouped by function, with help buttons.
- `Research`: research queue and Amazon match results.
- `Keepa`: explicit Keepa enrichment step, mode badge, and real/mock toggle.
- `Suppliers`: supplier management, details, import history, and visibility.
- `Upload`: supplier feed upload, preview, quality checks, and save.

The top supplier selector scopes Overview, Research, Deals, Pipeline issue
exports, and pipeline actions to one supplier. Hidden suppliers do not appear in
this selector.

The current UI is intentionally lightweight and FastAPI-hosted while the
pipeline concept is still being validated. Future UI rewrite preference:
React + Mantine, styled as a Grafana-like operations dashboard. Defer that work
until real Keepa/Amazon results prove the workflow.

## Supplier Management

Suppliers have an `is_visible` flag.

Visible suppliers:

- appear in the top supplier selector;
- appear in the supplier dashboard cards;
- are included in default Overview summaries and default list endpoints.

Hidden suppliers:

- remain in the database;
- remain available from Supplier Management and Supplier Details;
- are excluded from default summary/list views;
- can still be queried explicitly with `supplier_id`.

This is intended to keep the UI usable when many suppliers exist, without
deleting supplier history.

## Import Flow

Preferred UI/API flow:

```text
POST /upload/preview
POST /upload/commit
```

Preview returns:

- normalized columns;
- preview rows;
- mapping confidence;
- quality checks such as missing EAN, missing price, duplicate EAN, suspicious
  price, unmapped columns, and weak mappings.

Commit saves:

- supplier;
- ingestion run;
- supplier column mappings;
- normalized supplier offers.

Legacy direct import is still available:

```text
POST /upload
```

## Configuration Model

The project intentionally separates technical settings from business rules.

Technical settings live in `pipeline_settings`:

- `use_real_keepa`
- `default_batch_size`
- `default_marketplace`

Business rules live in `research_rules`:

- priority score threshold;
- stock thresholds;
- cost ranges;
- scoring weights;
- ROI and profit thresholds;
- fee assumptions;
- sales rank and monthly sales filters;
- Amazon-in-stock exclusion.

Stock is intentionally not a hard blocker for research queue population. Some
suppliers may allow ordering even when stock appears unavailable, so stock only
affects priority score.

## Provider Behavior

Current provider behavior:

- `pipeline_settings.use_real_keepa=false` uses mock Amazon matching and mock
  Keepa metrics.
- `pipeline_settings.use_real_keepa=true` uses Keepa for Amazon EAN to ASIN
  matching and Keepa metric enrichment.
- If real Keepa mode is enabled without a valid `KEEPA_API_KEY`, processing
  returns a controlled `not_configured` result instead of falling back to mock
  data or raising a server error.
- The Keepa UI shows the active mode, disables the run action when real mode is
  selected but not configured, and displays the metric source (`keepa_mock` or
  `keepa_real`) in the metrics table.

Temporary mock values should stay inside provider/mock code, not become
user-facing business settings.

Longer-term provider direction:

- Keepa is a research accelerator, not the strategic foundation for the whole
  product.
- Keep provider boundaries explicit so Keepa can be replaced or complemented by
  Amazon SP-API modules later.
- Planned provider boundaries:
  - product matcher provider;
  - market metrics provider;
  - fee provider;
  - future sales management provider.
- Amazon SP-API should be added module-by-module when needed: fees, catalog /
  listings, pricing, inventory, orders, and reports.

## Analytics And Grafana Direction

The Mirenelle UI should remain the operator workflow surface. Grafana is the
preferred future layer for dashboards and visual analysis.

Planned Grafana usage:

- pipeline health and processing trends;
- supplier performance and import quality;
- Keepa / market metric health;
- deal funnel and rejection trends;
- final candidate decision dashboards.

Do not pull deep Keepa history for every imported product. Detailed historical
Keepa data should be fetched only for deal candidates that pass filters and need
manual final review.

Future candidate-review flow:

```text
Deal candidate passed filters
    -> operator opens / prepares review
    -> fetch deeper Keepa history for this candidate only
    -> persist candidate metric snapshots / events
    -> open Grafana decision dashboard from the UI
```

Candidate review dashboards should help evaluate:

- Buy Box price history;
- supplier cost history;
- ROI / profit history;
- sales rank and sales velocity;
- Amazon in-stock periods;
- offer count changes;
- import and manual adjustment events.

This keeps Keepa token usage focused on products that are worth a human
decision, while Grafana handles the visual analysis.

## API Endpoints

Upload:

```text
POST /upload/preview
POST /upload/commit
POST /upload
```

Reports:

```text
GET /reports/unmapped-columns
```

Suppliers:

```text
GET   /suppliers/
GET   /suppliers/?include_hidden=true
GET   /suppliers/dashboard
GET   /suppliers/{supplier_id}
PATCH /suppliers/{supplier_id}/visibility
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
GET  /keepa/status
GET  /keepa/
```

Deals:

```text
POST /deals/create-candidates
GET  /deals/
```

Pipeline:

```text
POST /pipeline/run-research
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

Most research, matching, Keepa, deals, and pipeline endpoints accept
`supplier_id`. Without `supplier_id`, default read/list/summary endpoints only
include visible suppliers.

`PATCH /config/*` uses Pydantic schemas with partial updates, forbidden unknown
fields, and validation designed for UI clients.

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

Run supplier-scoped research:

```bash
curl -X POST "http://localhost:8000/pipeline/run-research?supplier_id=3"
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
│   │   ├── suppliers.py
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
│   │   ├── amazon_matchers/
│   │   ├── config_service.py
│   │   ├── deal_service.py
│   │   ├── import_draft_service.py
│   │   ├── ingestion_service.py
│   │   ├── keepa_client.py
│   │   ├── keepa_service.py
│   │   ├── marketplace.py
│   │   ├── pipeline_service.py
│   │   ├── research_queue_service.py
│   │   └── supplier_offer_service.py
│   ├── static/
│   │   ├── app.js
│   │   ├── favicon.png
│   │   ├── index.html
│   │   ├── mirenelle-logo.png
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
- Hidden suppliers should not appear in default UI lists, but their historical
  data should remain available through explicit supplier detail/scope access.
- Comparison engine work is postponed until multiple overlapping supplier
  catalogs exist.
- Keepa detailed history should be a candidate-review feature, not part of
  default catalog processing.
- Analytics should be designed for Grafana views or dashboards rather than
  bloating the operator UI.

## Near-Term Roadmap

1. Provider abstraction cleanup for mock / Keepa / future Amazon SP-API.
2. Real Keepa-based Amazon matching and metric enrichment.
3. Deal Candidate enrichment: title, brand, cost, Amazon price, filters.
4. Candidate review enrichment for final manual decisions, with Grafana links.
5. Real fee engine for FBA/VAT/shipping/marketplace rules.
6. Grafana dashboard layer backed by SQL views or snapshot/event tables.
7. Future UI rewrite after concept validation: React + Mantine,
   Grafana-like operations dashboard.
