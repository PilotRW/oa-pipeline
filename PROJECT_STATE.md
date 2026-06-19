# Mirenelle Automation - Project State

Last updated: 2026-06-15

## Current Position

Project is paused after adding Amazon Presence Service as a separate provider
step for checking whether Amazon itself is present on a listing.

Resume from here:

1. Commit or review the current working tree.
2. Test Amazon Presence on a non-empty pipeline run:
   import offers -> run research/Amazon matching -> open Keepa tab -> Check
   Amazon presence -> verify `amazon_presence_checks` rows and the UI table.
3. Re-upload the Cyberport feed and retest:
   preview -> keep only Kingston, Rain Design, Satechi -> apply filtered preview
   -> export CSV -> open in Numbers/Excel -> verify EAN search with leading
   zero.
4. Re-import the Jacob feed from a clean database and test the operator flow:
   preview -> keep only Makita -> exclude non-new/refurbished -> apply filtered
   preview -> export CSV -> save import.
5. Continue with category/product-type filtering if enough source data exists.
6. After local filters are stable, move toward real Keepa-based matching and
   enrichment with token-aware batching.

The current local workflow is:

```text
Upload supplier file
  -> preview
  -> import filters
  -> filtered preview
  -> save offers
  -> Research lookup plan
  -> operator-selected Research filters
  -> Run research
  -> Amazon match provider (mock or Keepa)
  -> Amazon Presence check
  -> Keepa market metrics
  -> Deal candidates
```

## Local Database State

The local database was cleaned before the latest test import:

- supplier offers removed;
- research queue removed;
- Amazon matches removed;
- Keepa metrics removed;
- deal candidates removed;
- ingestion runs removed;
- suppliers removed;
- supplier column mappings removed.

System defaults were kept:

- default research rule profile;
- pipeline settings.

After cleanup, no supplier/product data should be considered persistent test
state. The latest exported Makita preview from the Jacob feed was validated
from Downloads, not relied on as durable DB state.

## Implemented Today

### Amazon Presence Service

Implemented a separate Amazon Presence workflow for checking whether Amazon is
present on each matched listing.

New persistence:

```text
amazon_presence_checks
```

New model/service/API:

```text
app/models/amazon_presence_check.py
app/services/amazon_presence_service.py
app/api/amazon_presence.py
```

New endpoints:

```text
POST /amazon-presence/create-pending
POST /amazon-presence/process-pending
GET  /amazon-presence/
```

Behavior:

- Creates pending checks from matched ASIN rows in `amazon_product_matches`.
- Respects supplier scope via `supplier_id`.
- In mock mode, writes deterministic `presence_mock` results for UI/pipeline
  testing.
- In real Keepa mode, uses the existing Keepa client and treats current Keepa
  `AMAZON` price as the Amazon-presence signal.
- If a matching `keepa_product_metrics` row already exists, the service updates
  `keepa_product_metrics.amazon_in_stock` so existing deal rules can use the
  presence result.
- If real Keepa is enabled but `KEEPA_API_KEY` is missing, processing returns
  controlled `not_configured` instead of silently falling back to mock data.

UI:

- Added an `Amazon Presence` panel in the Keepa tab.
- Added `Check Amazon presence` action.
- Added CSV export for the presence table.

Migration:

```text
8c2d9a1f0b34_add_amazon_presence_checks.py
```

Local migration applied:

```text
3f1a9c2d8b71 -> 8c2d9a1f0b34
```

Smoke checks on empty local data:

```text
GET  /amazon-presence/?limit=5 -> []
POST /amazon-presence/create-pending?limit=5 -> created_count 0
POST /amazon-presence/process-pending?limit=5 -> processed_count 0
```

Important next validation:

- Run the service after real or mock Amazon matching has produced matched ASINs.
- Confirm deal rejection behavior when `exclude_amazon_in_stock` is enabled and
  presence checks have synced `keepa_product_metrics.amazon_in_stock`.

### Cyberport EAN Export Check

The Cyberport file checked during this pause:

```text
/Users/pilotrw/Downloads/cyberport-feedsmitmengen_synaxonvertriebcude (5).csv
```

User-selected filter criteria:

```text
brand filter mode: keep only selected
brands: Kingston, Rain Design, Satechi
exclude non-new/refurbished: enabled/checked as part of the test flow
```

Target EANs reported as missing by spreadsheet search:

```text
0879961008178
0740617328295
0891607000995
```

Verification result:

- All three target EANs exist in the original source CSV.
- All three also existed in the exported filtered preview CSV.
- Rows in the exported preview:
  - `0879961008178` -> Satechi, row 7.
  - `0891607000995` -> Rain Design, row 25.
  - `0740617328295` -> Kingston, row 87.
- The likely cause was spreadsheet auto-conversion of EAN values to numbers,
  which drops leading zeroes and makes exact search for the original EAN fail.

Implemented fix:

- `/upload/export-preview` now exports EAN-like identifier columns as
  spreadsheet-safe text formulas, for example `="0879961008178"`.
- Client-side CSV exports now use the same handling for identifier columns:
  `ean`, `gtin`, `upc`, and `barcode`.
- This affects downloaded CSV presentation only. Internal normalized data and
  database values remain plain EAN strings.

Important operational note:

- Upload preview drafts are in memory. The app container was restarted after
  this fix, so the operator must upload the file again before retesting export.

### Upload Brand Filter Ordering

The Upload brand filter list is now sorted alphabetically in the UI before
rendering. Keyword suggestions remain frequency-based.

### Jacob Upload / Makita Filter Checks

The Jacob file checked during this pause:

```text
/Users/pilotrw/Downloads/haendler_netto.csv
```

Source file facts:

- `849,971` rows.
- One actual supplier price column: `Preis netto`.
- `Preis netto` maps to canonical `price` with confidence `100`.
- Price distribution includes very expensive enterprise/service/license rows,
  so high `Max cost` values in the UI are real source data, not a price mapping
  bug.
- Overall source price max observed: `1,245,426.48`.
- Makita subset: `2,143` rows, median `26.93`, max `1,708.45`.

Exported filtered preview checked during this pause:

```text
/Users/pilotrw/Downloads/jacob-haendler-netto-csv-preview.csv
```

Validation result:

- `2,143` rows.
- Brand values: only `Makita`.
- Non-new/refurbished keyword matches: `0`.
- Price min/max: `4.14` / `1,708.45`.

The large Makita max price is a real Makita row, not a parser issue.

### Import Preview Filters

The Upload flow is preview-first and supports operator-selected filters before
commit:

- exclude brands;
- exclude title keywords;
- exclude rows without EAN;
- exclude non-new / refurbished rows;
- min/max supplier cost.
- CSV export of the full confirmed filtered preview, not only the visible
  preview sample.

The operator must apply a filtered preview before saving.

The visible Upload preview sample was raised to 50 rows. If filter controls are
changed after a confirmed preview, the UI marks the preview as stale and blocks
CSV export/save until the operator applies the filtered preview again.

Brand filters support both modes:

- exclude selected brands;
- keep only selected brands.

The Upload brand list is rendered alphabetically.

The brand suggestion list was expanded so large feeds expose more real brand
options, with select-all and clear-all controls.

Price parsing was hardened for both decimal styles:

```text
1.234,56 -> 1234.56
1,234.56 -> 1234.56
```

The explicit German synonym `preis netto` was added for `price`.

Delivery-time mapping was also hardened:

```text
Min Lieferzeit Werktage -> lead_time_days
Max Lieferzeit Werktage -> lead_time_days
```

This prevents those columns from being confused with MOQ-style fields.

### Research Lookup Plan

The Research tab now has a preflight plan before external lookup calls.

Implemented controls:

- batch size;
- minimum priority score;
- exclude brands;
- exclude title keywords;
- min/max supplier cost.
- save Research filters as global or supplier defaults, with saved/unsaved
  status and helper text.
- clear saved Research filters for the current scope.

Implemented outputs:

- eligible rows after active Research filters;
- rows filtered out by active Research filters;
- skipped reason breakdown for rows excluded by Research filters;
- split between already queued offers and not-yet-queued supplier offers;
- next lookup batch size;
- estimated external API calls;
- top brands in the lookup batch;
- top title keywords in the lookup batch;
- lookup sample table with supplier, EAN, brand, title, cost, and priority.

Important: the same filters are used for preview and for `Run research`, so the
operator sees what will actually be sent to the provider.

The Research lookup plan is a dry-run of the next research step: it includes
existing `needs_amazon_match` queue rows plus not-yet-queued supplier offers
that would be added by `Run research`, without mutating the database.

### Research Skipped Accounting

The Research lookup preview now explains why rows were excluded by the active
Research filters, without writing those rows into deal rejection states.

Current skipped reasons:

- `excluded_brand`
- `excluded_title_keyword`
- `below_min_cost`
- `above_max_cost`
- `missing_cost`

The UI shows this in the Research lookup plan as a skipped-reason card. This is
intentionally preview/accounting only, not a persistent rejection workflow.

### API/Service Support

Research prefilter parameters currently supported by pipeline endpoints:

```text
limit
min_priority_score
supplier_id
exclude_brands
exclude_title_keywords
min_cost
max_cost
```

Saved Research filter defaults live in `research_rules`:

```text
lookup_excluded_brands
lookup_excluded_title_keywords
lookup_min_cost
lookup_max_cost
```

Affected endpoints:

```text
GET  /pipeline/external-lookup-preview
POST /pipeline/run-research
PATCH /config/research-rules
```

## Verified

Commands run:

```bash
docker compose exec app python -m py_compile app/models/amazon_presence_check.py app/services/amazon_presence_service.py app/api/amazon_presence.py app/main.py
docker compose exec app alembic upgrade head
curl -sS 'http://localhost:8000/amazon-presence/?limit=5'
curl -sS -X POST 'http://localhost:8000/amazon-presence/create-pending?limit=5'
curl -sS -X POST 'http://localhost:8000/amazon-presence/process-pending?limit=5'
/Users/pilotrw/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check app/static/app.js
node --check app/static/app.js
docker compose exec app python -m py_compile app/api/upload.py
docker compose exec app python -m py_compile app/ingestion/synonyms.py app/ingestion/cleaners.py
docker compose exec app python -m py_compile app/api/upload.py app/services/import_draft_service.py
docker compose exec app python -m py_compile app/api/pipeline.py app/services/pipeline_service.py app/services/amazon_match_service.py
node --check app/static/app.js
git diff --check
```

Manual/API checks:

- Research prefilter without price filter returned eligible rows.
- `min_cost=100` narrowed eligible rows.
- `max_cost=50` narrowed eligible rows.
- `min_cost=100` returned a skipped breakdown showing rows below the minimum
  cost.
- UI shows Research filters in the same checkbox/panel style as Upload filters.
- UI lookup sample shows supplier cost and currency.
- UI shows the skipped-reason card in the Research lookup plan.

Latest API spot checks:

- `exclude_brands=Makita` returned `excluded_brand: 1197`.
- `min_cost=100` returned `below_min_cost: 785`.

Latest checks passed:

```bash
docker compose exec app python -m py_compile app/models/amazon_presence_check.py app/services/amazon_presence_service.py app/api/amazon_presence.py app/main.py
/Users/pilotrw/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check app/static/app.js
docker compose exec app alembic upgrade head
curl -sS 'http://localhost:8000/amazon-presence/?limit=5'
curl -sS -X POST 'http://localhost:8000/amazon-presence/create-pending?limit=5'
curl -sS -X POST 'http://localhost:8000/amazon-presence/process-pending?limit=5'
git diff --check
docker compose exec app python -m py_compile app/api/upload.py
docker compose exec app python -m py_compile app/ingestion/synonyms.py app/ingestion/cleaners.py
docker compose exec app python -m py_compile app/api/upload.py app/services/import_draft_service.py
docker compose exec app python -m py_compile app/services/amazon_match_service.py app/services/pipeline_service.py app/api/pipeline.py
git diff --check
```

## Working Tree At Pause

Expected modified files:

```text
PROJECT_STATE.md
README.md
alembic/env.py
app/main.py
app/api/upload.py
app/api/amazon_presence.py
app/models/amazon_presence_check.py
app/services/amazon_presence_service.py
app/ingestion/cleaners.py
app/ingestion/synonyms.py
app/services/import_draft_service.py
app/static/app.js
app/static/index.html
app/static/styles.css
```

Expected untracked migration:

```text
alembic/versions/8c2d9a1f0b34_add_amazon_presence_checks.py
```

## Next Recommended Step

Continue from Upload/import validation:

1. Run Amazon Presence against actual matched ASINs and verify the UI/table plus
   `keepa_product_metrics.amazon_in_stock` sync.
2. Retest Cyberport CSV export after re-uploading the file, because the restart
   cleared the previous in-memory upload draft.
3. Re-import Jacob Makita with the confirmed filter flow.
4. Use `Max cost` deliberately if the operator wants to avoid high-ticket
   Makita rows before external lookup.
5. Add category/product-type filtering once product type can be detected or
   inferred reliably from imported fields.
6. Then proceed toward real Keepa-based matching/enrichment with token-aware
   batching.

## Important Product Decisions

- Do not hardcode blocked brands, categories, or product types in code.
- Surface actual values in preview, then let the operator choose exclusions.
- Stock is not a hard blocker; it affects scoring only.
- Keepa tokens should be protected by local/import/research prefilters.
- Deep Keepa history should be fetched only for final manual-review candidates.
- Future UI rewrite preference: React + Mantine, Grafana-like operations
  dashboard, after concept validation.
