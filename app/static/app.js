const state = {
  summary: null,
  settings: null,
  rules: null,
  suppliers: [],
  supplierDashboard: [],
  supplierId: localStorage.getItem("oaSupplierId") || "",
  importDraft: null,
  importPreview: null,
  issueExport: null,
  language: localStorage.getItem("oaLanguage") || "en",
  activeView: "overview",
};

const translations = {
  en: {
    "action.populate": "Populate",
    "action.process": "Process",
    "action.preview": "Preview",
    "action.refresh": "Refresh",
    "action.runBatch": "Run batch",
    "action.runResearch": "Run research",
    "action.save": "Save",
    "action.saveImport": "Save import",
    "action.upload": "Upload",
    "action.close": "Close",
    "action.downloadCsv": "CSV",
    "action.downloadXls": "XLSX",
    "api.checking": "Checking API",
    "api.offline": "API unavailable",
    "api.online": "API online",
    "app.eyebrow": "Backend control panel",
    "app.tagline": "Automation console",
    "field.allSuppliers": "All suppliers",
    "field.batchSize": "Batch size",
    "field.excludeAmazonStock": "Exclude Amazon stock",
    "field.feedFile": "CSV or Excel file",
    "field.file": "File",
    "field.fulfillmentFee": "Fulfillment fee",
    "field.highStock": "High stock",
    "field.lowStock": "Low stock",
    "field.marketplace": "Marketplace",
    "field.maxSalesRank": "Max sales rank",
    "field.mediumCostMax": "Medium cost max",
    "field.mediumStock": "Medium stock",
    "field.minCost": "Min cost",
    "field.minMonthlySales": "Min monthly sales",
    "field.minPriority": "Min priority",
    "field.minProfit": "Min profit",
    "field.minRoi": "Min ROI %",
    "field.preferredCostMax": "Preferred cost max",
    "field.preferredCostMin": "Preferred cost min",
    "field.realKeepa": "Real Keepa",
    "field.referralFee": "Referral fee %",
    "field.rows": "Rows",
    "field.scoreBrand": "Score brand",
    "field.scoreCostHigh": "Score cost high",
    "field.scoreCostLow": "Score cost low",
    "field.scoreCostMedium": "Score cost medium",
    "field.scoreCostPreferred": "Score cost preferred",
    "field.scoreEan": "Score EAN",
    "field.scoreStockHigh": "Score stock high",
    "field.scoreStockLow": "Score stock low",
    "field.scoreStockMedium": "Score stock medium",
    "field.scoreStockVeryLow": "Score stock very low",
    "field.scoreTitle": "Score title",
    "field.supplierName": "Supplier name",
    "field.columns": "Columns",
    "field.mapped": "Mapped",
    "message.createdQueueItems": "Created {count} queue items",
    "message.noRecords": "No records",
    "message.processedMatches": "Processed {count} matches",
    "message.researchRun": "Research completed: {count} matches processed",
    "message.previewReady": "Preview ready: {count} rows",
    "message.saved": "Saved",
    "message.savedImport": "Saved {count} offers",
    "message.uploaded": "Uploaded",
    "nav.pipeline": "Pipeline",
    "nav.overview": "Overview",
    "nav.research": "Research",
    "nav.rules": "Rules",
    "nav.settings": "Settings",
    "nav.suppliers": "Suppliers",
    "nav.upload": "Upload",
    "panel.recentImports": "Recent Imports",
    "panel.amazonMatches": "Amazon Matches",
    "panel.dealCandidates": "Deal Candidates",
    "panel.pipelineRun": "Pipeline Run",
    "panel.pipelineSettings": "Pipeline Settings",
    "panel.pipelineIssues": "Pipeline Issues",
    "panel.columnMapping": "Column Mapping",
    "panel.previewRows": "Preview Rows",
    "panel.researchQueue": "Research Queue",
    "panel.researchRules": "Research Rules",
    "panel.supplierFeed": "Supplier Feed",
    "status.done": "Done",
    "status.failed": "Failed",
    "status.idle": "Idle",
    "status.running": "Running",
    "summary.amazonMatches": "Amazon Matches",
    "summary.dealCandidates": "Deal Candidates",
    "summary.keepaMetrics": "Keepa Metrics",
    "summary.researchQueue": "Research Queue",
    "issue.amazonNotFound": "Amazon not found",
    "issue.available": "Available",
    "issue.dealCandidates": "Deal candidates",
    "issue.keepaPending": "Keepa pending",
    "issue.needsAmazonMatch": "Needs Amazon match",
    "issue.open": "Open",
    "issue.rejectedLowRoi": "Rejected low ROI",
    "issue.rejectedUnprofitable": "Rejected unprofitable",
    "table.brand": "Brand",
    "table.confidence": "Confidence",
    "table.detectedAs": "Detected as",
    "table.fileColumn": "File column",
    "table.priority": "Priority",
    "table.profit": "Profit",
    "table.reason": "Reason",
    "table.roi": "ROI",
    "table.sales": "Sales",
    "table.stock": "Stock",
    "table.status": "Status",
    "table.supplier": "Supplier",
    "table.file": "File",
    "table.rows": "Rows",
    "table.valid": "Valid",
  },
  de: {
    "action.populate": "Befüllen",
    "action.process": "Verarbeiten",
    "action.preview": "Vorschau",
    "action.refresh": "Aktualisieren",
    "action.runBatch": "Batch starten",
    "action.runResearch": "Recherche starten",
    "action.save": "Speichern",
    "action.saveImport": "Import speichern",
    "action.upload": "Hochladen",
    "action.close": "Schließen",
    "action.downloadCsv": "CSV",
    "action.downloadXls": "XLSX",
    "api.checking": "API wird geprüft",
    "api.offline": "API nicht erreichbar",
    "api.online": "API online",
    "app.eyebrow": "Backend-Steuerung",
    "app.tagline": "Automation-Konsole",
    "field.allSuppliers": "Alle Lieferanten",
    "field.batchSize": "Batchgröße",
    "field.excludeAmazonStock": "Amazon-Bestand ausschließen",
    "field.feedFile": "CSV- oder Excel-Datei",
    "field.file": "Datei",
    "field.fulfillmentFee": "Fulfillment-Gebühr",
    "field.highStock": "Hoher Bestand",
    "field.lowStock": "Niedriger Bestand",
    "field.marketplace": "Marktplatz",
    "field.maxSalesRank": "Max. Verkaufsrang",
    "field.mediumCostMax": "Mittlere Kosten max.",
    "field.mediumStock": "Mittlerer Bestand",
    "field.minCost": "Min. Kosten",
    "field.minMonthlySales": "Min. Monatsverkäufe",
    "field.minPriority": "Min. Priorität",
    "field.minProfit": "Min. Gewinn",
    "field.minRoi": "Min. ROI %",
    "field.preferredCostMax": "Bevorzugte Kosten max.",
    "field.preferredCostMin": "Bevorzugte Kosten min.",
    "field.realKeepa": "Echtes Keepa",
    "field.referralFee": "Vermittlungsgebühr %",
    "field.rows": "Zeilen",
    "field.scoreBrand": "Punkte Marke",
    "field.scoreCostHigh": "Punkte Kosten hoch",
    "field.scoreCostLow": "Punkte Kosten niedrig",
    "field.scoreCostMedium": "Punkte Kosten mittel",
    "field.scoreCostPreferred": "Punkte Kosten bevorzugt",
    "field.scoreEan": "Punkte EAN",
    "field.scoreStockHigh": "Punkte Bestand hoch",
    "field.scoreStockLow": "Punkte Bestand niedrig",
    "field.scoreStockMedium": "Punkte Bestand mittel",
    "field.scoreStockVeryLow": "Punkte Bestand sehr niedrig",
    "field.scoreTitle": "Punkte Titel",
    "field.supplierName": "Lieferantenname",
    "field.columns": "Spalten",
    "field.mapped": "Zugeordnet",
    "message.createdQueueItems": "{count} Queue-Einträge erstellt",
    "message.noRecords": "Keine Einträge",
    "message.processedMatches": "{count} Matches verarbeitet",
    "message.researchRun": "Recherche fertig: {count} Matches verarbeitet",
    "message.previewReady": "Vorschau bereit: {count} Zeilen",
    "message.saved": "Gespeichert",
    "message.savedImport": "{count} Angebote gespeichert",
    "message.uploaded": "Hochgeladen",
    "nav.pipeline": "Pipeline",
    "nav.overview": "Übersicht",
    "nav.research": "Recherche",
    "nav.rules": "Regeln",
    "nav.settings": "Einstellungen",
    "nav.suppliers": "Lieferanten",
    "nav.upload": "Upload",
    "panel.recentImports": "Letzte Importe",
    "panel.amazonMatches": "Amazon Matches",
    "panel.dealCandidates": "Deal-Kandidaten",
    "panel.pipelineRun": "Pipeline-Lauf",
    "panel.pipelineSettings": "Pipeline-Einstellungen",
    "panel.pipelineIssues": "Pipeline-Probleme",
    "panel.columnMapping": "Spaltenzuordnung",
    "panel.previewRows": "Vorschauzeilen",
    "panel.researchQueue": "Recherche-Queue",
    "panel.researchRules": "Recherche-Regeln",
    "panel.supplierFeed": "Lieferanten-Feed",
    "status.done": "Fertig",
    "status.failed": "Fehlgeschlagen",
    "status.idle": "Bereit",
    "status.running": "Läuft",
    "summary.amazonMatches": "Amazon Matches",
    "summary.dealCandidates": "Deal-Kandidaten",
    "summary.keepaMetrics": "Keepa-Metriken",
    "summary.researchQueue": "Recherche-Queue",
    "issue.amazonNotFound": "Amazon nicht gefunden",
    "issue.available": "Verfügbar",
    "issue.dealCandidates": "Deal-Kandidaten",
    "issue.keepaPending": "Keepa ausstehend",
    "issue.needsAmazonMatch": "Benötigt Amazon-Match",
    "issue.open": "Offen",
    "issue.rejectedLowRoi": "Abgelehnt: niedriger ROI",
    "issue.rejectedUnprofitable": "Abgelehnt: unprofitabel",
    "table.brand": "Marke",
    "table.confidence": "Konfidenz",
    "table.detectedAs": "Erkannt als",
    "table.fileColumn": "Dateispalte",
    "table.priority": "Priorität",
    "table.profit": "Gewinn",
    "table.reason": "Grund",
    "table.roi": "ROI",
    "table.sales": "Verkäufe",
    "table.stock": "Bestand",
    "table.status": "Status",
    "table.supplier": "Lieferant",
    "table.file": "Datei",
    "table.rows": "Zeilen",
    "table.valid": "Gültig",
  },
  uk: {
    "action.populate": "Заповнити",
    "action.process": "Обробити",
    "action.preview": "Превʼю",
    "action.refresh": "Оновити",
    "action.runBatch": "Запустити batch",
    "action.runResearch": "Запустити research",
    "action.save": "Зберегти",
    "action.saveImport": "Зберегти імпорт",
    "action.upload": "Завантажити",
    "action.close": "Закрити",
    "action.downloadCsv": "CSV",
    "action.downloadXls": "XLSX",
    "api.checking": "Перевірка API",
    "api.offline": "API недоступний",
    "api.online": "API онлайн",
    "app.eyebrow": "Панель керування backend",
    "app.tagline": "Консоль автоматизації",
    "field.allSuppliers": "Усі постачальники",
    "field.batchSize": "Розмір batch",
    "field.excludeAmazonStock": "Виключати Amazon in stock",
    "field.feedFile": "CSV або Excel файл",
    "field.file": "Файл",
    "field.fulfillmentFee": "Fulfillment fee",
    "field.highStock": "Високий stock",
    "field.lowStock": "Низький stock",
    "field.marketplace": "Маркетплейс",
    "field.maxSalesRank": "Макс. sales rank",
    "field.mediumCostMax": "Середня ціна макс.",
    "field.mediumStock": "Середній stock",
    "field.minCost": "Мін. ціна",
    "field.minMonthlySales": "Мін. продажі/міс.",
    "field.minPriority": "Мін. пріоритет",
    "field.minProfit": "Мін. profit",
    "field.minRoi": "Мін. ROI %",
    "field.preferredCostMax": "Бажана ціна макс.",
    "field.preferredCostMin": "Бажана ціна мін.",
    "field.realKeepa": "Реальний Keepa",
    "field.referralFee": "Referral fee %",
    "field.rows": "Рядки",
    "field.scoreBrand": "Бали за brand",
    "field.scoreCostHigh": "Бали за високу ціну",
    "field.scoreCostLow": "Бали за низьку ціну",
    "field.scoreCostMedium": "Бали за середню ціну",
    "field.scoreCostPreferred": "Бали за бажану ціну",
    "field.scoreEan": "Бали за EAN",
    "field.scoreStockHigh": "Бали за високий stock",
    "field.scoreStockLow": "Бали за низький stock",
    "field.scoreStockMedium": "Бали за середній stock",
    "field.scoreStockVeryLow": "Бали за дуже низький stock",
    "field.scoreTitle": "Бали за title",
    "field.supplierName": "Назва постачальника",
    "field.columns": "Колонки",
    "field.mapped": "Розпізнано",
    "message.createdQueueItems": "Створено {count} елементів черги",
    "message.noRecords": "Немає записів",
    "message.processedMatches": "Оброблено {count} matches",
    "message.researchRun": "Research завершено: оброблено {count} matches",
    "message.previewReady": "Превʼю готове: {count} рядків",
    "message.saved": "Збережено",
    "message.savedImport": "Збережено {count} offers",
    "message.uploaded": "Завантажено",
    "nav.pipeline": "Pipeline",
    "nav.overview": "Огляд",
    "nav.research": "Дослідження",
    "nav.rules": "Правила",
    "nav.settings": "Налаштування",
    "nav.suppliers": "Постачальники",
    "nav.upload": "Завантаження",
    "panel.recentImports": "Останні імпорти",
    "panel.amazonMatches": "Amazon збіги",
    "panel.dealCandidates": "Кандидати угод",
    "panel.pipelineRun": "Запуск pipeline",
    "panel.pipelineSettings": "Налаштування pipeline",
    "panel.pipelineIssues": "Проблеми pipeline",
    "panel.columnMapping": "Зіставлення колонок",
    "panel.previewRows": "Рядки превʼю",
    "panel.researchQueue": "Черга дослідження",
    "panel.researchRules": "Правила дослідження",
    "panel.supplierFeed": "Фід постачальника",
    "status.done": "Готово",
    "status.failed": "Помилка",
    "status.idle": "Очікує",
    "status.running": "Виконується",
    "summary.amazonMatches": "Amazon збіги",
    "summary.dealCandidates": "Кандидати угод",
    "summary.keepaMetrics": "Keepa метрики",
    "summary.researchQueue": "Черга дослідження",
    "issue.amazonNotFound": "Amazon не знайдено",
    "issue.available": "Доступно",
    "issue.dealCandidates": "Кандидати угод",
    "issue.keepaPending": "Keepa очікує",
    "issue.needsAmazonMatch": "Потрібен Amazon match",
    "issue.open": "Відкрито",
    "issue.rejectedLowRoi": "Відхилено: низький ROI",
    "issue.rejectedUnprofitable": "Відхилено: без прибутку",
    "table.brand": "Бренд",
    "table.confidence": "Впевненість",
    "table.detectedAs": "Розпізнано як",
    "table.fileColumn": "Колонка файлу",
    "table.priority": "Пріоритет",
    "table.profit": "Прибуток",
    "table.reason": "Причина",
    "table.roi": "ROI",
    "table.sales": "Продажі",
    "table.stock": "Stock",
    "table.status": "Статус",
    "table.supplier": "Постачальник",
    "table.file": "Файл",
    "table.rows": "Рядки",
    "table.valid": "Валідні",
  },
};

const moneyFields = new Set([
  "preferred_cost_min",
  "preferred_cost_max",
  "medium_cost_max",
  "min_cost",
  "min_roi_percent",
  "min_profit",
  "referral_fee_percent",
  "fulfillment_fee_fixed",
]);

function t(key, params = {}) {
  const template = translations[state.language]?.[key]
    || translations.en[key]
    || key;

  return Object.entries(params).reduce(
    (text, [name, value]) => text.replaceAll(`{${name}}`, value),
    template,
  );
}

function applyLanguage() {
  document.documentElement.lang = state.language;
  document.querySelector("#language-select").value = state.language;

  document.querySelectorAll("[data-i18n]").forEach((element) => {
    element.textContent = t(element.dataset.i18n);
  });

  document.querySelectorAll("[data-i18n-title]").forEach((element) => {
    element.title = t(element.dataset.i18nTitle);
  });

  document.querySelector("#view-title").textContent = t(
    `nav.${state.activeView}`,
  );

  setStatus(Boolean(state.summary));
  renderSummary();
  renderPipelineIssues();
  renderSuppliersDashboard();

  if (state.importPreview) {
    renderImportPreview(state.importPreview);
  }

  renderSupplierSelect();
  updateSupplierScopeVisibility();
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  const text = await response.text();
  const data = text ? JSON.parse(text) : null;

  if (!response.ok) {
    const message = data?.detail
      ? JSON.stringify(data.detail)
      : `Request failed with ${response.status}`;
    throw new Error(message);
  }

  return data;
}

function scopedPath(path) {
  if (!state.supplierId) return path;

  const separator = path.includes("?") ? "&" : "?";

  return `${path}${separator}supplier_id=${encodeURIComponent(state.supplierId)}`;
}

function showAlert(message, isError = false) {
  const alert = document.querySelector("#alert");
  alert.textContent = message;
  alert.classList.toggle("error", isError);
  alert.classList.remove("hidden");

  window.clearTimeout(showAlert.timer);
  showAlert.timer = window.setTimeout(() => {
    alert.classList.add("hidden");
  }, 4200);
}

function renderSupplierSelect() {
  const select = document.querySelector("#supplier-select");

  select.innerHTML = [
    `<option value="">${t("field.allSuppliers")}</option>`,
    ...state.suppliers.map((supplier) => `
      <option value="${supplier.id}">
        ${escapeHtml(supplier.name)} (${formatNumber(supplier.offers_count)})
      </option>
    `),
  ].join("");

  select.value = state.supplierId;
}

function updateSupplierScopeVisibility() {
  document.querySelector("#supplier-select").classList.toggle(
    "hidden",
    state.activeView === "suppliers",
  );
}

function selectedSupplierName() {
  if (!state.supplierId) return t("field.allSuppliers");

  const supplier = state.suppliers.find(
    (item) => String(item.id) === state.supplierId,
  );

  return supplier?.name || t("field.allSuppliers");
}

function setStatus(ok) {
  const status = document.querySelector("#api-status");
  status.textContent = ok ? t("api.online") : t("api.offline");
}

function formatNumber(value) {
  if (value === null || value === undefined) return "-";
  return Number(value).toLocaleString(undefined, {
    maximumFractionDigits: 2,
  });
}

function formatDate(value) {
  if (!value) return "-";
  return new Date(value).toLocaleString();
}

function statusClass(status) {
  if (!status) return "";
  if (String(status).includes("candidate") || status === "completed") return "ok";
  if (String(status).includes("reject") || String(status).includes("not")) return "bad";
  return "warn";
}

function renderSummary() {
  const grid = document.querySelector("#summary-grid");
  const summary = state.summary || {};

  const items = [
    ["summary.researchQueue", summary.research_queue],
    ["summary.amazonMatches", summary.amazon_matches],
    ["summary.keepaMetrics", summary.keepa_metrics],
    ["summary.dealCandidates", summary.deal_candidates],
  ];

  grid.innerHTML = items
    .map(([labelKey, value]) => {
      const statuses = value?.by_status || {};
      const statusText = Object.entries(statuses)
        .map(([key, count]) => `${key}: ${count}`)
        .join(" | ");

      return `
        <article class="metric">
          <span>${t(labelKey)}</span>
          <strong>${formatNumber(value?.total || 0)}</strong>
          <small>${statusText || t("message.noRecords")}</small>
        </article>
      `;
    })
    .join("");
}

function statusText(statuses = {}) {
  const text = Object.entries(statuses)
    .map(([key, count]) => `${key}: ${formatNumber(count)}`)
    .join(" | ");

  return text || t("message.noRecords");
}

function renderSuppliersDashboard() {
  const grid = document.querySelector("#suppliers-dashboard");

  if (!grid) return;

  if (!state.supplierDashboard.length) {
    grid.innerHTML = `<section class="panel">${t("message.noRecords")}</section>`;
    return;
  }

  grid.innerHTML = state.supplierDashboard
    .map((supplier) => {
      const imports = supplier.recent_imports || [];

      return `
        <section class="panel supplier-card">
          <div class="panel-header">
            <div>
              <h3>${escapeHtml(supplier.name)}</h3>
              <p>${formatNumber(supplier.offers_count)} offers</p>
            </div>
            <button class="ghost-button" data-select-supplier="${supplier.id}" type="button">
              ${t("nav.overview")}
            </button>
          </div>

          <div class="supplier-status-grid">
            <article>
              <span>${t("summary.researchQueue")}</span>
              <strong>${statusText(supplier.statuses?.research_queue)}</strong>
            </article>
            <article>
              <span>${t("summary.amazonMatches")}</span>
              <strong>${statusText(supplier.statuses?.amazon_matches)}</strong>
            </article>
            <article>
              <span>${t("summary.dealCandidates")}</span>
              <strong>${statusText(supplier.statuses?.deal_candidates)}</strong>
            </article>
          </div>

          <div class="preview-section">
            <h4>${t("panel.recentImports")}</h4>
            <div class="table-wrap">
              <table>
                <thead>
                  <tr>
                    <th>${t("table.file")}</th>
                    <th>${t("table.rows")}</th>
                    <th>${t("table.valid")}</th>
                    <th>${t("table.status")}</th>
                  </tr>
                </thead>
                <tbody>
                  ${imports.length
                    ? imports.map((run) => `
                      <tr>
                        <td>${escapeHtml(run.filename)}</td>
                        <td>${formatNumber(run.rows_total)}</td>
                        <td>${formatNumber(run.rows_valid)}</td>
                        <td><span class="badge ${statusClass(run.status)}">${escapeHtml(run.status)}</span></td>
                      </tr>
                    `).join("")
                    : `<tr><td colspan="4">${t("message.noRecords")}</td></tr>`}
                </tbody>
              </table>
            </div>
          </div>
        </section>
      `;
    })
    .join("");
}

function statusCount(section, status) {
  return state.summary?.[section]?.by_status?.[status] || 0;
}

function maxStatusCount(leftSection, leftStatus, rightSection, rightStatus) {
  return Math.max(
    statusCount(leftSection, leftStatus),
    statusCount(rightSection, rightStatus),
  );
}

function issueDefinitions() {
  return {
    needsAmazonMatch: {
      label: "issue.needsAmazonMatch",
      count: statusCount("research_queue", "needs_amazon_match"),
      tone: "warn",
      endpoint: scopedPath("/research-queue/?status=needs_amazon_match&limit=500"),
      columns: [
        { label: t("table.supplier"), key: "supplier_name", render: (row) => escapeHtml(row.supplier_name) || "-" },
        { label: "EAN", key: "ean" },
        { label: t("table.priority"), key: "priority_score", render: (row) => formatNumber(row.priority_score) },
        { label: t("table.brand"), key: "brand", render: (row) => escapeHtml(row.brand) || "-" },
        { label: t("table.stock"), key: "stock", render: (row) => formatNumber(row.stock) },
        { label: t("table.status"), key: "status", render: (row) => `<span class="badge ${statusClass(row.status)}">${escapeHtml(row.status)}</span>` },
      ],
    },
    amazonNotFound: {
      label: "issue.amazonNotFound",
      count: maxStatusCount(
        "amazon_matches",
        "not_found",
        "research_queue",
        "amazon_match_not_found",
      ),
      tone: "bad",
      endpoint: scopedPath("/amazon-matches/?match_status=not_found&limit=500"),
      columns: [
        { label: t("table.supplier"), key: "supplier_name", render: (row) => escapeHtml(row.supplier_name) || "-" },
        { label: "EAN", key: "ean" },
        { label: "ASIN", key: "asin", render: (row) => escapeHtml(row.asin) || "-" },
        { label: t("table.confidence"), key: "match_confidence", render: (row) => formatNumber(row.match_confidence) },
        { label: t("table.status"), key: "match_status", render: (row) => `<span class="badge ${statusClass(row.match_status)}">${escapeHtml(row.match_status)}</span>` },
      ],
    },
    keepaPending: {
      label: "issue.keepaPending",
      count: statusCount("keepa_metrics", "pending")
        + statusCount("research_queue", "keepa_pending"),
      tone: "warn",
      endpoint: scopedPath("/keepa/?data_status=pending&limit=500"),
      columns: [
        { label: t("table.supplier"), key: "supplier_name", render: (row) => escapeHtml(row.supplier_name) || "-" },
        { label: "ASIN", key: "asin" },
        { label: t("table.status"), key: "data_status", render: (row) => `<span class="badge ${statusClass(row.data_status)}">${escapeHtml(row.data_status)}</span>` },
        { label: t("table.sales"), key: "estimated_monthly_sales", render: (row) => formatNumber(row.estimated_monthly_sales) },
      ],
    },
    rejectedLowRoi: {
      label: "issue.rejectedLowRoi",
      count: maxStatusCount(
        "deal_candidates",
        "rejected_low_roi",
        "research_queue",
        "rejected_low_roi",
      ),
      tone: "bad",
      endpoint: scopedPath("/research-queue/?status=rejected_low_roi&limit=500"),
      columns: [
        { label: t("table.supplier"), key: "supplier_name", render: (row) => escapeHtml(row.supplier_name) || "-" },
        { label: "EAN", key: "ean" },
        { label: t("table.priority"), key: "priority_score", render: (row) => formatNumber(row.priority_score) },
        { label: t("table.reason"), key: "rejection_reason", render: (row) => escapeHtml(row.rejection_reason) || "-" },
        { label: t("table.status"), key: "status", render: (row) => `<span class="badge ${statusClass(row.status)}">${escapeHtml(row.status)}</span>` },
      ],
    },
    rejectedUnprofitable: {
      label: "issue.rejectedUnprofitable",
      count: maxStatusCount(
        "deal_candidates",
        "rejected_unprofitable",
        "research_queue",
        "rejected_unprofitable",
      ),
      tone: "bad",
      endpoint: scopedPath("/research-queue/?status=rejected_unprofitable&limit=500"),
      columns: [
        { label: t("table.supplier"), key: "supplier_name", render: (row) => escapeHtml(row.supplier_name) || "-" },
        { label: "EAN", key: "ean" },
        { label: t("table.priority"), key: "priority_score", render: (row) => formatNumber(row.priority_score) },
        { label: t("table.reason"), key: "rejection_reason", render: (row) => escapeHtml(row.rejection_reason) || "-" },
        { label: t("table.status"), key: "status", render: (row) => `<span class="badge ${statusClass(row.status)}">${escapeHtml(row.status)}</span>` },
      ],
    },
    dealCandidates: {
      label: "issue.dealCandidates",
      count: statusCount("deal_candidates", "candidate"),
      tone: "ok",
      doneLabel: "issue.available",
      endpoint: scopedPath("/deals/?status=candidate&limit=500"),
      columns: [
        { label: t("table.supplier"), key: "supplier_name", render: (row) => escapeHtml(row.supplier_name) || "-" },
        { label: "ASIN", key: "asin" },
        { label: t("table.roi"), key: "roi_percent", render: (row) => formatNumber(row.roi_percent) },
        { label: t("table.profit"), key: "estimated_profit", render: (row) => formatNumber(row.estimated_profit) },
        { label: t("table.status"), key: "status", render: (row) => `<span class="badge ${statusClass(row.status)}">${escapeHtml(row.status)}</span>` },
      ],
    },
  };
}

function renderPipelineIssues() {
  const grid = document.querySelector("#pipeline-issues");

  if (!grid) return;

  const items = Object.entries(issueDefinitions());

  grid.innerHTML = items
    .map(([key, item]) => `
      <article class="issue-card">
        <span>${t(item.label)}</span>
        <strong>${formatNumber(item.count)}</strong>
        <button class="badge ${item.count ? item.tone : "ok"}" data-issue-key="${key}" type="button">
          ${item.count ? t(item.doneLabel || "issue.open") : t("status.done")}
        </button>
      </article>
    `)
    .join("");
}

function fillForm(form, values) {
  for (const element of form.elements) {
    if (!element.name || !(element.name in values)) continue;

    const value = values[element.name];

    if (element.type === "checkbox") {
      element.checked = Boolean(value);
    } else {
      element.value = value ?? "";
    }
  }
}

function formPayload(form) {
  const payload = {};

  for (const element of form.elements) {
    if (!element.name) continue;

    if (element.type === "checkbox") {
      payload[element.name] = element.checked;
      continue;
    }

    if (element.value === "") {
      payload[element.name] = null;
      continue;
    }

    if (element.type === "number") {
      payload[element.name] = moneyFields.has(element.name)
        ? Number.parseFloat(element.value)
        : Number.parseInt(element.value, 10);
      continue;
    }

    payload[element.name] = element.value;
  }

  return payload;
}

function renderRows(selector, rows, columns) {
  const body = document.querySelector(selector);

  if (!rows.length) {
    body.innerHTML = `<tr><td colspan="${columns.length}">${t("message.noRecords")}</td></tr>`;
    return;
  }

  body.innerHTML = rows
    .map((row) => {
      const cells = columns
        .map((column) => {
          const value = column.render ? column.render(row) : row[column.key];
          return `<td>${column.render ? value : escapeHtml(value) || "-"}</td>`;
        })
        .join("");

      return `<tr>${cells}</tr>`;
    })
    .join("");
}

function renderTable(headSelector, bodySelector, rows, columns) {
  const head = document.querySelector(headSelector);
  const body = document.querySelector(bodySelector);

  head.innerHTML = `
    <tr>
      ${columns.map((column) => `<th>${escapeHtml(column.label)}</th>`).join("")}
    </tr>
  `;

  if (!rows.length) {
    body.innerHTML = `<tr><td colspan="${columns.length}">${t("message.noRecords")}</td></tr>`;
    return;
  }

  body.innerHTML = rows
    .map((row) => {
      const cells = columns
        .map((column) => {
          const value = column.render ? column.render(row) : row[column.key];
          return `<td>${value ?? "-"}</td>`;
        })
        .join("");

      return `<tr>${cells}</tr>`;
    })
    .join("");
}

function plainCellValue(row, column) {
  const value = row[column.key];

  if (value === null || value === undefined || value === "") return "";

  return String(value);
}

function csvEscape(value) {
  const text = String(value ?? "");

  if (/[",\n\r]/.test(text)) {
    return `"${text.replaceAll('"', '""')}"`;
  }

  return text;
}

function xmlEscape(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&apos;");
}

function filenameSafe(value) {
  return String(value || "export")
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    || "export";
}

function downloadBlob(filename, mimeType, content) {
  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");

  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

function textBytes(value) {
  return new TextEncoder().encode(value);
}

const crcTable = Array.from({ length: 256 }, (_, index) => {
  let crc = index;

  for (let bit = 0; bit < 8; bit += 1) {
    crc = (crc & 1) ? (0xEDB88320 ^ (crc >>> 1)) : (crc >>> 1);
  }

  return crc >>> 0;
});

function crc32(bytes) {
  let crc = 0xFFFFFFFF;

  for (const byte of bytes) {
    crc = crcTable[(crc ^ byte) & 0xFF] ^ (crc >>> 8);
  }

  return (crc ^ 0xFFFFFFFF) >>> 0;
}

function u16(value) {
  return [value & 0xFF, (value >>> 8) & 0xFF];
}

function u32(value) {
  return [
    value & 0xFF,
    (value >>> 8) & 0xFF,
    (value >>> 16) & 0xFF,
    (value >>> 24) & 0xFF,
  ];
}

function concatBytes(parts) {
  const length = parts.reduce((total, part) => total + part.length, 0);
  const output = new Uint8Array(length);
  let offset = 0;

  for (const part of parts) {
    output.set(part, offset);
    offset += part.length;
  }

  return output;
}

function zipDateParts() {
  const now = new Date();
  const time = (
    (now.getHours() << 11)
    | (now.getMinutes() << 5)
    | Math.floor(now.getSeconds() / 2)
  );
  const date = (
    ((now.getFullYear() - 1980) << 9)
    | ((now.getMonth() + 1) << 5)
    | now.getDate()
  );

  return { time, date };
}

function createZip(files) {
  const localParts = [];
  const centralParts = [];
  const { time, date } = zipDateParts();
  let offset = 0;

  for (const file of files) {
    const name = textBytes(file.name);
    const data = textBytes(file.content);
    const crc = crc32(data);
    const localHeader = new Uint8Array([
      ...u32(0x04034b50),
      ...u16(20),
      ...u16(0),
      ...u16(0),
      ...u16(time),
      ...u16(date),
      ...u32(crc),
      ...u32(data.length),
      ...u32(data.length),
      ...u16(name.length),
      ...u16(0),
    ]);
    const centralHeader = new Uint8Array([
      ...u32(0x02014b50),
      ...u16(20),
      ...u16(20),
      ...u16(0),
      ...u16(0),
      ...u16(time),
      ...u16(date),
      ...u32(crc),
      ...u32(data.length),
      ...u32(data.length),
      ...u16(name.length),
      ...u16(0),
      ...u16(0),
      ...u16(0),
      ...u16(0),
      ...u32(0),
      ...u32(offset),
    ]);

    localParts.push(localHeader, name, data);
    centralParts.push(centralHeader, name);
    offset += localHeader.length + name.length + data.length;
  }

  const centralDirectory = concatBytes(centralParts);
  const end = new Uint8Array([
    ...u32(0x06054b50),
    ...u16(0),
    ...u16(0),
    ...u16(files.length),
    ...u16(files.length),
    ...u32(centralDirectory.length),
    ...u32(offset),
    ...u16(0),
  ]);

  return concatBytes([
    ...localParts,
    centralDirectory,
    end,
  ]);
}

function columnName(index) {
  let name = "";
  let value = index + 1;

  while (value > 0) {
    const remainder = (value - 1) % 26;
    name = String.fromCharCode(65 + remainder) + name;
    value = Math.floor((value - 1) / 26);
  }

  return name;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

async function loadSummary() {
  state.summary = await api(scopedPath("/pipeline/summary"));
  renderSummary();
  renderPipelineIssues();
}

async function loadSuppliers() {
  state.suppliers = await api("/suppliers/");

  if (
    state.supplierId
    && !state.suppliers.some((supplier) => String(supplier.id) === state.supplierId)
  ) {
    state.supplierId = "";
    localStorage.removeItem("oaSupplierId");
  }

  renderSupplierSelect();
}

async function loadSuppliersDashboard() {
  state.supplierDashboard = await api("/suppliers/dashboard");
  renderSuppliersDashboard();
}

async function loadConfig() {
  const [settings, rules] = await Promise.all([
    api("/config/pipeline-settings"),
    api("/config/research-rules"),
  ]);

  state.settings = settings;
  state.rules = rules;

  fillForm(document.querySelector("#pipeline-settings-form"), settings);
  fillForm(document.querySelector("#research-rules-form"), rules);
}

async function loadDeals() {
  const deals = await api(scopedPath("/deals/?limit=500"));
  renderRows("#deals-table", deals, [
    { key: "supplier_name" },
    { key: "asin" },
    { key: "roi_percent", render: (row) => formatNumber(row.roi_percent) },
    { key: "estimated_profit", render: (row) => formatNumber(row.estimated_profit) },
    {
      key: "status",
      render: (row) => `<span class="badge ${statusClass(row.status)}">${row.status}</span>`,
    },
  ]);
}

async function loadResearch() {
  const [queue, matches] = await Promise.all([
    api(scopedPath("/research-queue/?limit=12")),
    api(scopedPath("/amazon-matches/?limit=12")),
  ]);

  renderRows("#queue-table", queue, [
    { key: "ean" },
    { key: "supplier_name" },
    { key: "priority_score", render: (row) => formatNumber(row.priority_score) },
    {
      key: "status",
      render: (row) => `<span class="badge ${statusClass(row.status)}">${row.status}</span>`,
    },
    { key: "brand" },
  ]);

  renderRows("#matches-table", matches, [
    { key: "ean" },
    { key: "supplier_name" },
    { key: "asin" },
    {
      key: "match_status",
      render: (row) => `<span class="badge ${statusClass(row.match_status)}">${row.match_status}</span>`,
    },
    { key: "match_confidence", render: (row) => formatNumber(row.match_confidence) },
  ]);
}

async function refreshAll() {
  try {
    await api("/");
    setStatus(true);
    await loadSuppliers();
    await Promise.all([
      loadSummary(),
      loadConfig(),
      loadDeals(),
      loadResearch(),
      loadSuppliersDashboard(),
    ]);
  } catch (error) {
    setStatus(false);
    showAlert(error.message, true);
  }
}

async function runBatch() {
  const button = document.querySelector("#run-batch-button");
  const status = document.querySelector("#last-run-status");
  const output = document.querySelector("#last-run-output");

  button.disabled = true;
  status.textContent = t("status.running");
  status.className = "badge warn";

  try {
    const result = await api(scopedPath("/pipeline/run-batch"), {
      method: "POST",
    });
    output.textContent = JSON.stringify(result, null, 2);
    status.textContent = result.status || t("status.done");
    status.className = `badge ${result.status === "ok" ? "ok" : "warn"}`;
    await Promise.all([loadSummary(), loadDeals(), loadResearch()]);
  } catch (error) {
    status.textContent = t("status.failed");
    status.className = "badge bad";
    showAlert(error.message, true);
  } finally {
    button.disabled = false;
  }
}

async function runResearch() {
  const button = document.querySelector("#run-research-button");

  button.disabled = true;

  try {
    const result = await api(scopedPath("/pipeline/run-research"), {
      method: "POST",
    });
    showAlert(t("message.researchRun", {
      count: result.amazon_processed?.processed_count || 0,
    }));
    await Promise.all([loadSummary(), loadResearch(), loadDeals()]);
  } catch (error) {
    showAlert(error.message, true);
  } finally {
    button.disabled = false;
  }
}

async function saveForm(form, endpoint) {
  const payload = formPayload(form);
  const result = await api(endpoint, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });

  fillForm(form, result);
  showAlert(t("message.saved"));
  await loadSummary();
}

function setImportDraft(draft) {
  state.importDraft = draft;
  document.querySelector("#save-import-button").classList.toggle(
    "hidden",
    !draft,
  );

  if (!draft) {
    state.importPreview = null;
    document.querySelector("#upload-preview").classList.add("hidden");
  }
}

function renderImportPreview(result) {
  state.importPreview = result;
  const preview = document.querySelector("#upload-preview");
  const summary = document.querySelector("#preview-summary");
  const tableHead = document.querySelector("#preview-table-head");
  const tableBody = document.querySelector("#preview-table-body");
  const mappingList = document.querySelector("#mapping-list");
  const columns = result.normalized_columns || [];
  const rows = result.preview || [];
  const mappedColumns = (result.normalization_report || [])
    .filter((item) => item.mapped_to)
    .length;

  summary.innerHTML = `
    <article>
      <span>${t("field.supplierName")}</span>
      <strong>${escapeHtml(result.supplier_name)}</strong>
    </article>
    <article>
      <span>${t("field.file")}</span>
      <strong>${escapeHtml(result.filename)}</strong>
    </article>
    <article>
      <span>${t("field.rows")}</span>
      <strong>${formatNumber(result.rows)}</strong>
    </article>
    <article>
      <span>${t("field.columns")}</span>
      <strong>${formatNumber(columns.length)}</strong>
    </article>
    <article>
      <span>${t("field.mapped")}</span>
      <strong>${formatNumber(mappedColumns)}</strong>
    </article>
  `;

  tableHead.innerHTML = `
    <tr>
      ${columns.map((column) => `<th>${escapeHtml(column)}</th>`).join("")}
    </tr>
  `;

  tableBody.innerHTML = rows.length
    ? rows
      .map((row) => `
        <tr>
          ${columns.map((column) => `<td>${escapeHtml(row[column]) || "-"}</td>`).join("")}
        </tr>
      `)
      .join("")
    : `<tr><td colspan="${columns.length || 1}">${t("message.noRecords")}</td></tr>`;

  mappingList.innerHTML = (result.normalization_report || [])
    .map((item) => {
      const status = item.mapped_to ? "ok" : "bad";
      const mappedTo = item.mapped_to || "-";

      return `
        <article class="mapping-item">
          <div>
            <span>${t("table.fileColumn")}</span>
            <strong>${escapeHtml(item.column)}</strong>
          </div>
          <div>
            <span>${t("table.detectedAs")}</span>
            <strong>${escapeHtml(mappedTo)}</strong>
          </div>
          <span class="badge ${status}">${formatNumber(item.confidence)}%</span>
        </article>
      `;
    })
    .join("");

  preview.classList.remove("hidden");
}

function closeIssueModal() {
  document.querySelector("#issue-modal").classList.add("hidden");
}

function setIssueExport(title, rows, columns) {
  state.issueExport = { title, rows, columns };

  const disabled = !rows.length;
  document.querySelector("#download-issue-csv").disabled = disabled;
  document.querySelector("#download-issue-xls").disabled = disabled;
}

function downloadIssueCsv() {
  if (!state.issueExport) return;

  const { title, rows, columns } = state.issueExport;
  const header = columns.map((column) => csvEscape(column.label)).join(",");
  const body = rows
    .map((row) => columns
      .map((column) => csvEscape(plainCellValue(row, column)))
      .join(","))
    .join("\n");

  downloadBlob(
    `${filenameSafe(selectedSupplierName())}-${filenameSafe(title)}.csv`,
    "text/csv;charset=utf-8",
    `\uFEFF${header}\n${body}`,
  );
}

function downloadIssueXls() {
  if (!state.issueExport) return;

  const { title, rows, columns } = state.issueExport;
  const sheetRows = [
    columns.map((column) => column.label),
    ...rows.map((row) => columns.map((column) => plainCellValue(row, column))),
  ];
  const sheetData = sheetRows
    .map((row, rowIndex) => {
      const cells = row
        .map((value, columnIndex) => {
          const ref = `${columnName(columnIndex)}${rowIndex + 1}`;
          return `
            <c r="${ref}" t="inlineStr">
              <is><t>${xmlEscape(value)}</t></is>
            </c>
          `;
        })
        .join("");

      return `<row r="${rowIndex + 1}">${cells}</row>`;
    })
    .join("");
  const files = [
    {
      name: "[Content_Types].xml",
      content: `<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
</Types>`,
    },
    {
      name: "_rels/.rels",
      content: `<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>`,
    },
    {
      name: "xl/workbook.xml",
      content: `<?xml version="1.0" encoding="UTF-8"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
  xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="${xmlEscape(filenameSafe(title).slice(0, 31))}" sheetId="1" r:id="rId1"/>
  </sheets>
</workbook>`,
    },
    {
      name: "xl/_rels/workbook.xml.rels",
      content: `<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
</Relationships>`,
    },
    {
      name: "xl/worksheets/sheet1.xml",
      content: `<?xml version="1.0" encoding="UTF-8"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <sheetData>${sheetData}</sheetData>
</worksheet>`,
    },
  ];

  downloadBlob(
    `${filenameSafe(selectedSupplierName())}-${filenameSafe(title)}.xlsx`,
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    createZip(files),
  );
}

async function openIssueModal(issueKey) {
  const definition = issueDefinitions()[issueKey];

  if (!definition) return;

  const modal = document.querySelector("#issue-modal");
  const title = document.querySelector("#issue-modal-title");
  const summary = document.querySelector("#issue-modal-summary");

  title.textContent = t(definition.label);
  summary.innerHTML = `
    <span class="badge ${definition.count ? definition.tone : "ok"}">
      ${formatNumber(definition.count)}
    </span>
  `;
  renderTable("#issue-modal-head", "#issue-modal-body", [], definition.columns);
  setIssueExport(t(definition.label), [], definition.columns);
  modal.classList.remove("hidden");

  try {
    const rows = await api(definition.endpoint);
    setIssueExport(t(definition.label), rows, definition.columns);
    renderTable(
      "#issue-modal-head",
      "#issue-modal-body",
      rows,
      definition.columns,
    );
  } catch (error) {
    showAlert(error.message, true);
  }
}

function bindNavigation() {
  document.querySelectorAll(".nav-item").forEach((button) => {
    button.addEventListener("click", () => {
      const view = button.dataset.view;
      document.querySelectorAll(".nav-item").forEach((item) => {
        item.classList.toggle("active", item === button);
      });
      document.querySelectorAll(".view").forEach((section) => {
        section.classList.toggle("active", section.id === `view-${view}`);
      });
      state.activeView = view;
      document.querySelector("#view-title").textContent = t(`nav.${view}`);
      updateSupplierScopeVisibility();
    });
  });
}

function bindActions() {
  document.querySelector("#refresh-button").addEventListener("click", refreshAll);
  document.querySelector("#language-select").addEventListener("change", (event) => {
    state.language = event.currentTarget.value;
    localStorage.setItem("oaLanguage", state.language);
    applyLanguage();
  });
  document.querySelector("#supplier-select").addEventListener("change", async (event) => {
    state.supplierId = event.currentTarget.value;

    if (state.supplierId) {
      localStorage.setItem("oaSupplierId", state.supplierId);
    } else {
      localStorage.removeItem("oaSupplierId");
    }

    try {
      await Promise.all([loadSummary(), loadDeals(), loadResearch()]);
    } catch (error) {
      showAlert(error.message, true);
    }
  });
  document.querySelector("#run-batch-button").addEventListener("click", runBatch);
  document.querySelector("#run-research-button").addEventListener("click", runResearch);
  document.querySelector("#refresh-deals-button").addEventListener("click", loadDeals);
  document.querySelector("#refresh-issues-button").addEventListener("click", loadSummary);
  document.querySelector("#pipeline-issues").addEventListener("click", (event) => {
    const button = event.target.closest("[data-issue-key]");

    if (!button) return;

    openIssueModal(button.dataset.issueKey);
  });
  document.querySelector("#suppliers-dashboard").addEventListener("click", async (event) => {
    const button = event.target.closest("[data-select-supplier]");

    if (!button) return;

    state.supplierId = button.dataset.selectSupplier;
    localStorage.setItem("oaSupplierId", state.supplierId);
    renderSupplierSelect();

    document.querySelector('[data-view="overview"]').click();

    try {
      await Promise.all([loadSummary(), loadDeals(), loadResearch()]);
    } catch (error) {
      showAlert(error.message, true);
    }
  });
  document.querySelectorAll("[data-close-modal]").forEach((element) => {
    element.addEventListener("click", closeIssueModal);
  });
  document.querySelector("#download-issue-csv").addEventListener("click", downloadIssueCsv);
  document.querySelector("#download-issue-xls").addEventListener("click", downloadIssueXls);
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeIssueModal();
    }
  });
  document.querySelector("#pipeline-settings-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
      await saveForm(event.currentTarget, "/config/pipeline-settings");
    } catch (error) {
      showAlert(error.message, true);
    }
  });

  document.querySelector("#research-rules-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
      await saveForm(event.currentTarget, "/config/research-rules");
    } catch (error) {
      showAlert(error.message, true);
    }
  });

  document.querySelector("#upload-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    const supplier = form.elements.supplier_name.value;
    const body = new FormData();
    body.append("file", form.elements.file.files[0]);
    setImportDraft(null);

    try {
      const response = await fetch(`/upload/preview?supplier_name=${encodeURIComponent(supplier)}`, {
        method: "POST",
        body,
      });
      const result = await response.json();

      if (!response.ok) {
        throw new Error(JSON.stringify(result.detail || result));
      }

      setImportDraft(result);
      renderImportPreview(result);
      showAlert(t("message.previewReady", { count: result.rows }));
    } catch (error) {
      showAlert(error.message, true);
    }
  });

  document.querySelector("#save-import-button").addEventListener("click", async (event) => {
    if (!state.importDraft?.import_token) return;

    const button = event.currentTarget;
    button.disabled = true;

    try {
      const result = await api("/upload/commit", {
        method: "POST",
        body: JSON.stringify({
          import_token: state.importDraft.import_token,
        }),
      });

      setImportDraft(null);
      renderImportPreview(result);
      showAlert(t("message.savedImport", { count: result.offers_saved }));
      await Promise.all([loadSummary(), loadResearch()]);
    } catch (error) {
      showAlert(error.message, true);
    } finally {
      button.disabled = false;
    }
  });

  document.querySelector("#upload-form").addEventListener("change", (event) => {
    if (!["file", "supplier_name"].includes(event.target.name)) return;

    setImportDraft(null);
  });

  document.querySelector("#upload-form input[name=\"supplier_name\"]").addEventListener("input", () => {
    setImportDraft(null);
  });
}

bindNavigation();
bindActions();
applyLanguage();
refreshAll();
