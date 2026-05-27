# Mirenelle Automation - Project State

Last updated: 2026-05-27

## Current Position

Project is paused after implementing the preview-driven Research prefilter and
the skipped-reason breakdown for Research lookup filters.

Resume from here:

1. Commit or review the current working tree.
2. Continue with category/product-type filtering if enough source data exists.
3. After local filters are stable, move toward real Keepa-based matching and
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

After cleanup, a new `makita` supplier/feed was imported and used for testing
the Research prefilter.

## Implemented Today

### Import Preview Filters

The Upload flow is preview-first and supports operator-selected filters before
commit:

- exclude brands;
- exclude title keywords;
- exclude rows without EAN;
- exclude non-new / refurbished rows;
- min/max supplier cost.

The operator must apply a filtered preview before saving.

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
node --check app/static/app.js
docker compose exec app python -m py_compile app/services/amazon_match_service.py app/services/pipeline_service.py app/api/pipeline.py
git diff --check
```

## Working Tree At Pause

Expected modified files:

```text
PROJECT_STATE.md
README.md
app/api/config.py
app/api/config_schemas.py
app/models/research_rule.py
app/services/amazon_match_service.py
app/services/config_service.py
app/services/pipeline_service.py
app/static/app.js
app/static/index.html
app/static/styles.css
```

Expected untracked migration:

```text
alembic/versions/3f1a9c2d8b71_add_research_lookup_filters.py
```

The migration has already been applied locally with `alembic upgrade head`.

## Next Recommended Step

Continue from Research UX / logic hardening:

1. Add category/product-type filtering once product type can be detected or
   inferred reliably from imported fields.
2. Then proceed toward real Keepa-based matching/enrichment with token-aware
   batching.

## Important Product Decisions

- Do not hardcode blocked brands, categories, or product types in code.
- Surface actual values in preview, then let the operator choose exclusions.
- Stock is not a hard blocker; it affects scoring only.
- Keepa tokens should be protected by local/import/research prefilters.
- Deep Keepa history should be fetched only for final manual-review candidates.
- Future UI rewrite preference: React + Mantine, Grafana-like operations
  dashboard, after concept validation.
