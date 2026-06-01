# Mirenelle Automation / OA Pipeline

Backend and local control panel for ecommerce Online Arbitrage automation.

The project ingests supplier catalog files, normalizes supplier offers, queues
offers for Amazon research, enriches matched products with marketplace metrics,
evaluates profitability, and produces ranked deal candidates.

## Current Status

Project is currently paused after Upload preview/filter hardening and Jacob
Makita import validation. See `PROJECT_STATE.md` for the exact resume point and
current working-tree expectations.

Implemented:

- FastAPI backend with PostgreSQL, async SQLAlchemy models, and Alembic
  migrations.
- Static FastAPI-hosted UI at `/ui/`, branded as Mirenelle Automation.
- UI localization for English, German, and Ukrainian.
- CSV and Excel supplier feed ingestion.
- Two-step import flow: preview first, then save.
- Human-readable import preview table, column mapping preview, and quality
  checks.
- Preview-driven import filters for excluding brands, title keywords, missing
  EAN rows, and supplier price ranges before commit.
- Import brand filters can either exclude selected brands or keep only selected
  brands, with select-all and clear-all controls.
- Import preview CSV export downloads the full confirmed filtered preview, not
  only the visible sample rows.
- Import preview marks rows stale after filter changes until the filtered
  preview is applied again.
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
- External lookup preflight showing eligible queue count, request batch size,
  estimated API calls, top brands, top title keywords, sample rows, and supplier
  costs before provider calls.
- Skipped-reason breakdown for Research lookup filters, so excluded rows are
  explainable without being stored as rejected deals.
- Research lookup preflight includes existing pending queue rows and
  not-yet-queued supplier offers, so newly imported offers are visible before
  mutating queue state.
- Research lookup filters for excluding brands, title keywords, and supplier
  cost ranges before external provider calls.
- Saved Research lookup filter defaults with status/helper UI, scoped globally
  or to the selected supplier through `research_rules`, plus a clear action for
  returning the scope to an unfiltered lookup plan.
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

Current simplified flow:

```text
Supplier feeds
    -> supplier_offers
    -> offer_research_queue
    -> amazon_product_matches
    -> keepa_product_metrics
    -> deal_candidates
```

Target decision funnel:

```text
Supplier price file
    -> import preview
    -> operator-selected import filters
    -> supplier_offers
    -> local eligibility / scoring prefilter
    -> external lookup preview and API budget check
    -> Amazon / Keepa / provider lookup
    -> market metrics enrichment
    -> deal candidate calculation
    -> manual candidate review
    -> optional deep Keepa history for finalists only
    -> Grafana decision dashboard link
    -> approve / reject / postpone
```

Principles for this funnel:

- Use local data first and avoid external API calls until rows pass local
  filters.
- Do not hardcode blocked brands or product types in code. Surface actual
  brands, keywords, product types, price ranges, and row counts in preview, then
  let the operator decide what to exclude.
- Keepa/API budget must be visible before calls are made.
- Deep Keepa history is not part of default processing. Fetch it only for final
  candidates that need manual decision support.
- Grafana is for visualization and decision dashboards; Mirenelle UI is for
  workflow and actions.

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

Planned future review states:

```text
local_prefiltered
external_lookup_pending
external_lookup_skipped
manual_review_pending
manual_review_ready
review_approved
review_rejected
review_postponed
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
- `Research`: lookup plan, pre-provider filters, research queue, and Amazon
  match results.
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
POST /upload/filter-preview
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

Future import filtering direction:

- Import should remain preview-first.
- After preview, the UI analyzes actual file values and proposes filters with
  row counts before commit.
- Operators can manually exclude brands, title keywords, rows without EAN,
  non-new/refurbished offers, and supplier price ranges.
- Import saves only the rows that remain after selected preview filters.
- After changing filters, the operator must apply a filtered preview before
  saving. The save action should commit the last confirmed filtered preview, not
  unconfirmed checkbox/input changes.
- CSV export should export that same confirmed filtered dataset.
- Selected filters may optionally be saved as reusable supplier/global rules.

This must not be hardcoded as a static list of forbidden brands or categories.
The file preview should surface what is present in the supplier feed, and the
operator chooses what to exclude.

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
- saved Research lookup filter defaults for brands, title keywords, and supplier
  cost ranges.

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

Before any paid or limited 3rd-party lookup, there is a second preview gate for
Amazon/Keepa matching:

```text
Imported offers
    -> local scoring / prefilter
    -> external lookup plan with counts
    -> operator adjusts filters, supplier cost range, and batch size
    -> only then call Keepa / Amazon / other providers
```

This should show:

- how many offers will be sent to external providers;
- how many offers were filtered out before external lookup;
- why offers were filtered out by the active Research filters;
- top brands and title keywords in the lookup batch;
- supplier scope and priority ranges;
- supplier cost ranges and sample row costs;
- estimated API/token usage where possible;
- exclusions applied before the call.

The goal is to avoid wasting Keepa tokens or future Amazon API quota on brands,
product types, or categories that the operator already knows are not worth
analyzing.

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
POST /upload/filter-preview
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
GET  /pipeline/external-lookup-preview
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
- Preview-driven filters should be used before import commit and before
  external provider calls. Avoid hardcoded exclusion lists unless they are
  operator-managed rules created from preview.

## Near-Term Roadmap

1. Add preview-driven import filters:
   show brands, title keywords, price ranges, missing EAN, and row counts before
   import commit. Initial MVP is implemented with an explicit filtered preview
   confirmation step; saved reusable rules are still future work.
2. Add local eligibility / scoring prefilter before external lookups:
   exclude operator-selected brands, keywords, and supplier cost ranges, keeping
   external API usage focused on viable rows. Initial UI/API support is
   implemented in the Research lookup plan, including saved defaults.
3. Expand external lookup preflight:
   show supplier scope, top brands/product types, priority ranges, batch size,
   sample rows, supplier costs, and estimated Keepa/API usage before calling
   providers. Initial operator-adjustable lookup filters are implemented; saved
   reusable filter profiles are still future work.
4. Clean up provider abstraction for mock / Keepa / future Amazon SP-API:
   product matcher provider, market metrics provider, fee provider, future sales
   management provider.
5. Real Keepa-based Amazon matching and metric enrichment with token-aware
   batching and controlled failure states.
6. Deal Candidate enrichment:
   title, brand, supplier cost, Amazon price, Buy Box presence, seller count,
   max sell price, margin/ROI clarity, rejection reasons, and filters.
7. Candidate review workflow:
   manual review states, reviewer notes, approve/reject/postpone actions, and
   final decision support.
8. Candidate review enrichment for finalists only:
   deep Keepa history, snapshots/events, and Grafana dashboard links.
9. Real fee engine for FBA/VAT/shipping/marketplace rules.
10. Grafana dashboard layer backed by SQL views or snapshot/event tables.
11. Future UI rewrite after concept validation: React + Mantine,
   Grafana-like operations dashboard.
