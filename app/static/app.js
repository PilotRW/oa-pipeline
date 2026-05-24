const state = {
  summary: null,
  settings: null,
  rules: null,
  importDraft: null,
  importPreview: null,
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
    "action.save": "Save",
    "action.saveImport": "Save import",
    "action.upload": "Upload",
    "api.checking": "Checking API",
    "api.offline": "API unavailable",
    "api.online": "API online",
    "app.eyebrow": "Backend control panel",
    "app.tagline": "Automation console",
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
    "message.previewReady": "Preview ready: {count} rows",
    "message.saved": "Saved",
    "message.savedImport": "Saved {count} offers",
    "message.uploaded": "Uploaded",
    "nav.overview": "Overview",
    "nav.research": "Research",
    "nav.rules": "Rules",
    "nav.settings": "Settings",
    "nav.upload": "Upload",
    "panel.amazonMatches": "Amazon Matches",
    "panel.dealCandidates": "Deal Candidates",
    "panel.pipelineRun": "Pipeline Run",
    "panel.pipelineSettings": "Pipeline Settings",
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
    "table.brand": "Brand",
    "table.confidence": "Confidence",
    "table.detectedAs": "Detected as",
    "table.fileColumn": "File column",
    "table.priority": "Priority",
    "table.profit": "Profit",
    "table.roi": "ROI",
    "table.status": "Status",
  },
  de: {
    "action.populate": "Befüllen",
    "action.process": "Verarbeiten",
    "action.preview": "Vorschau",
    "action.refresh": "Aktualisieren",
    "action.runBatch": "Batch starten",
    "action.save": "Speichern",
    "action.saveImport": "Import speichern",
    "action.upload": "Hochladen",
    "api.checking": "API wird geprüft",
    "api.offline": "API nicht erreichbar",
    "api.online": "API online",
    "app.eyebrow": "Backend-Steuerung",
    "app.tagline": "Automation-Konsole",
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
    "message.previewReady": "Vorschau bereit: {count} Zeilen",
    "message.saved": "Gespeichert",
    "message.savedImport": "{count} Angebote gespeichert",
    "message.uploaded": "Hochgeladen",
    "nav.overview": "Übersicht",
    "nav.research": "Recherche",
    "nav.rules": "Regeln",
    "nav.settings": "Einstellungen",
    "nav.upload": "Upload",
    "panel.amazonMatches": "Amazon Matches",
    "panel.dealCandidates": "Deal-Kandidaten",
    "panel.pipelineRun": "Pipeline-Lauf",
    "panel.pipelineSettings": "Pipeline-Einstellungen",
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
    "table.brand": "Marke",
    "table.confidence": "Konfidenz",
    "table.detectedAs": "Erkannt als",
    "table.fileColumn": "Dateispalte",
    "table.priority": "Priorität",
    "table.profit": "Gewinn",
    "table.roi": "ROI",
    "table.status": "Status",
  },
  uk: {
    "action.populate": "Заповнити",
    "action.process": "Обробити",
    "action.preview": "Превʼю",
    "action.refresh": "Оновити",
    "action.runBatch": "Запустити batch",
    "action.save": "Зберегти",
    "action.saveImport": "Зберегти імпорт",
    "action.upload": "Завантажити",
    "api.checking": "Перевірка API",
    "api.offline": "API недоступний",
    "api.online": "API онлайн",
    "app.eyebrow": "Панель керування backend",
    "app.tagline": "Консоль автоматизації",
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
    "message.previewReady": "Превʼю готове: {count} рядків",
    "message.saved": "Збережено",
    "message.savedImport": "Збережено {count} offers",
    "message.uploaded": "Завантажено",
    "nav.overview": "Огляд",
    "nav.research": "Дослідження",
    "nav.rules": "Правила",
    "nav.settings": "Налаштування",
    "nav.upload": "Завантаження",
    "panel.amazonMatches": "Amazon збіги",
    "panel.dealCandidates": "Кандидати угод",
    "panel.pipelineRun": "Запуск pipeline",
    "panel.pipelineSettings": "Налаштування pipeline",
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
    "table.brand": "Бренд",
    "table.confidence": "Впевненість",
    "table.detectedAs": "Розпізнано як",
    "table.fileColumn": "Колонка файлу",
    "table.priority": "Пріоритет",
    "table.profit": "Прибуток",
    "table.roi": "ROI",
    "table.status": "Статус",
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

  if (state.importPreview) {
    renderImportPreview(state.importPreview);
  }
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
          return `<td>${value ?? "-"}</td>`;
        })
        .join("");

      return `<tr>${cells}</tr>`;
    })
    .join("");
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
  state.summary = await api("/pipeline/summary");
  renderSummary();
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
  const deals = await api("/deals/?limit=10");
  renderRows("#deals-table", deals, [
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
    api("/research-queue/?limit=12"),
    api("/amazon-matches/?limit=12"),
  ]);

  renderRows("#queue-table", queue, [
    { key: "ean" },
    { key: "priority_score", render: (row) => formatNumber(row.priority_score) },
    {
      key: "status",
      render: (row) => `<span class="badge ${statusClass(row.status)}">${row.status}</span>`,
    },
    { key: "brand" },
  ]);

  renderRows("#matches-table", matches, [
    { key: "ean" },
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
    await Promise.all([
      loadSummary(),
      loadConfig(),
      loadDeals(),
      loadResearch(),
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
    const result = await api("/pipeline/run-batch", {
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
  document.querySelector("#run-batch-button").addEventListener("click", runBatch);
  document.querySelector("#refresh-deals-button").addEventListener("click", loadDeals);
  document.querySelector("#populate-queue-button").addEventListener("click", async () => {
    const result = await api("/research-queue/populate", { method: "POST" });
    showAlert(t("message.createdQueueItems", { count: result.created_count }));
    await Promise.all([loadSummary(), loadResearch()]);
  });
  document.querySelector("#process-matches-button").addEventListener("click", async () => {
    const result = await api("/amazon-matches/process-pending", { method: "POST" });
    showAlert(t("message.processedMatches", { count: result.processed_count }));
    await Promise.all([loadSummary(), loadResearch()]);
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
