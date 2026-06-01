const state = {
  summary: null,
  settings: null,
  keepaStatus: null,
  rules: null,
  suppliers: [],
  supplierManagement: [],
  supplierDashboard: [],
  supplierDetail: null,
  supplierId: localStorage.getItem("oaSupplierId") || "",
  importDraft: null,
  importFiltersConfirmed: false,
  importPreview: null,
  issueExport: null,
  tableExports: {},
  lookupPreview: null,
  lookupPlanDirty: false,
  language: localStorage.getItem("oaLanguage") || "en",
  activeView: "overview",
};

const translations = {
  en: {
    "action.populate": "Populate",
    "action.applyFilters": "Apply filters preview",
    "action.process": "Process",
    "action.preview": "Preview",
    "action.updateLookupPlan": "Apply research criteria",
    "action.refresh": "Refresh",
    "action.runBatch": "Run batch",
    "action.runKeepa": "Run Keepa",
    "action.runResearch": "Run research",
    "action.save": "Save",
    "action.clearLookupFilters": "Clear saved filters",
    "action.saveDefaultRules": "Save default rules",
    "action.saveLookupFilters": "Save filters as defaults",
    "action.saveSupplierRules": "Save supplier rules",
    "action.resetToDefault": "Reset to default",
    "action.resetToSystemDefaults": "Reset to system defaults",
    "action.saveImport": "Save import",
    "action.selectAll": "Select all",
    "action.clearAll": "Clear all",
    "action.excludeSelected": "Exclude selected",
    "action.keepOnlySelected": "Keep only selected",
    "action.upload": "Upload",
    "action.uploadFeed": "Upload feed",
    "action.close": "Close",
    "action.downloadCsv": "CSV",
    "action.downloadXls": "XLSX",
    "action.details": "Details",
    "action.hide": "Hide",
    "action.show": "Show",
    "action.setScope": "Set scope",
    "action.viewOverview": "Overview",
    "action.viewResearch": "Research",
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
    "field.filterBrands": "Exclude brands",
    "field.filterKeywords": "Exclude title keywords",
    "field.excludeMissingEan": "Exclude missing EAN",
    "field.excludeNonNew": "Exclude non-new / refurbished",
    "field.fulfillmentFee": "Fulfillment fee",
    "field.highStock": "High stock",
    "field.lowStock": "Low stock",
    "field.marketplace": "Marketplace",
    "field.maxSalesRank": "Max sales rank",
    "field.mediumCostMax": "Medium cost max",
    "field.mediumStock": "Medium stock",
    "field.minCost": "Min cost",
    "field.maxCost": "Max cost",
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
    "quality.duplicateEan": "Duplicate EAN",
    "quality.missingEan": "Missing EAN",
    "quality.missingPrice": "Missing price",
    "quality.suspiciousPrice": "Suspicious price",
    "quality.unmappedColumns": "Unmapped columns",
    "quality.weakMappings": "Weak mappings",
    "ruleSection.dealFilters": "Deal filters",
    "ruleSection.feeModel": "Fee model",
    "ruleSection.priorityScores": "Priority scoring",
    "ruleSection.thresholds": "Stock and cost thresholds",
    "message.createdQueueItems": "Created {count} queue items",
    "message.noRecords": "No records",
    "message.processedMatches": "Processed {count} matches",
    "message.keepaRun": "Keepa completed: {created} queued, {processed} processed",
    "message.keepaRunWithSource": "Keepa completed via {source}: {created} queued, {processed} processed",
    "message.keepaNotConfigured": "Real Keepa is enabled, but KEEPA_API_KEY is not configured",
    "message.researchRun": "Research completed: {count} matches processed",
    "message.lookupPlanHint": "These criteria define the next research run. Applying them updates the plan only; it does not call external APIs.",
    "message.lookupSaveHint": "Saved filters are applied automatically for this scope. Batch size stays run-specific.",
    "message.lookupFiltersCleared": "Research filters cleared",
    "message.lookupFilterResult": "{eligible} eligible, {batch} in next lookup batch",
    "message.suggestionsShown": "Showing {shown} of {total}",
    "message.previewReady": "Preview ready: {count} rows",
    "message.importFilterResult": "{after} of {before} rows will be imported",
    "message.applyFiltersToUpdatePreview": "Apply filters preview to update rows",
    "message.filteredPreviewReady": "Filtered preview ready: {count} rows",
    "message.saved": "Saved",
    "message.rulesReset": "Rules reset",
    "message.savedImport": "Saved {count} offers",
    "message.uploaded": "Uploaded",
    "nav.pipeline": "Pipeline",
    "nav.keepa": "Keepa",
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
    "panel.qualityChecks": "Quality Checks",
    "panel.researchQueue": "Research Queue",
    "panel.researchRules": "Research Rules",
    "panel.supplierFeed": "Supplier Feed",
    "panel.supplierDetails": "Supplier Details",
    "panel.supplierManagement": "Supplier Management",
    "panel.importHistory": "Import History",
    "panel.importFilters": "Import Filters",
    "panel.externalLookupPreview": "Research lookup plan",
    "panel.lookupSample": "Lookup sample",
    "panel.keepaMetrics": "Keepa Metrics",
    "panel.offerStats": "Offer Stats",
    "panel.recentOffers": "Recent Offers",
    "panel.pipelineStatus": "Pipeline Status",
    "panel.nextActions": "Next Actions",
    "status.done": "Done",
    "status.failed": "Failed",
    "status.idle": "Idle",
    "status.running": "Running",
    "summary.amazonMatches": "Amazon Matches",
    "summary.dealCandidates": "Deal Candidates",
    "summary.keepaMetrics": "Keepa Metrics",
    "summary.eligibleExternal": "Eligible",
    "summary.filteredOut": "Filtered out",
    "summary.willRequest": "Will request",
    "summary.estimatedRequests": "Estimated API calls",
    "summary.queuePending": "Queued",
    "summary.skippedReasons": "Skipped reasons",
    "summary.unqueuedOffers": "Not queued yet",
    "summary.researchQueue": "Research Queue",
    "issue.amazonNotFound": "Amazon not found",
    "issue.available": "Available",
    "issue.dealCandidates": "Deal candidates",
    "issue.keepaPending": "Keepa pending",
    "issue.needsAmazonMatch": "Needs Amazon match",
    "issue.open": "Open",
    "issue.rejectedLowRoi": "Rejected low ROI",
    "issue.rejectedUnprofitable": "Rejected unprofitable",
    "keepa.modeMock": "Mock mode",
    "keepa.modeReal": "Real Keepa",
    "keepa.modeRealMissing": "Real Keepa not configured",
    "keepa.sourceMock": "Mock",
    "keepa.sourceReal": "Real",
    "keepa.sourceUnknown": "Unknown",
    "table.brand": "Brand",
    "table.buyBox": "Buy Box",
    "table.confidence": "Confidence",
    "table.detectedAs": "Detected as",
    "table.fileColumn": "File column",
    "table.priority": "Priority",
    "table.profit": "Profit",
    "table.reason": "Reason",
    "table.roi": "ROI",
    "table.sales": "Sales",
    "table.salesRank": "Sales rank",
    "table.source": "Source",
    "table.keywords": "Keywords",
    "table.stock": "Stock",
    "table.status": "Status",
    "table.supplier": "Supplier",
    "table.file": "File",
    "table.rows": "Rows",
    "table.valid": "Valid",
    "table.actions": "Actions",
    "table.failed": "Failed",
    "table.importedAt": "Imported at",
    "table.sku": "SKU",
    "table.cost": "Cost",
    "table.title": "Title",
    "table.visibility": "Visibility",
    "status.hidden": "Hidden",
    "status.lookupPlanApplied": "Criteria applied to research plan",
    "status.lookupPlanChanged": "Criteria changed, apply to refresh the plan",
    "status.lookupFiltersSaved": "Filters saved",
    "status.lookupFiltersUnsaved": "Unsaved filters",
    "status.visible": "Visible",
    "skip.above_max_cost": "Above max cost",
    "skip.below_min_cost": "Below min cost",
    "skip.excluded_brand": "Brand",
    "skip.excluded_title_keyword": "Title keyword",
    "skip.missing_cost": "Missing cost",
    "metric.avgCost": "Avg cost",
    "metric.createdAt": "Created at",
    "metric.totalOffers": "Total offers",
    "metric.withBrand": "With brand",
    "metric.withEan": "With EAN",
    "metric.withStock": "With stock",
    "metric.withTitle": "With title",
  },
  de: {
    "action.populate": "Befüllen",
    "action.applyFilters": "Filtervorschau anwenden",
    "action.process": "Verarbeiten",
    "action.preview": "Vorschau",
    "action.updateLookupPlan": "Recherchekriterien anwenden",
    "action.refresh": "Aktualisieren",
    "action.runBatch": "Batch starten",
    "action.runKeepa": "Keepa starten",
    "action.runResearch": "Recherche starten",
    "action.save": "Speichern",
    "action.clearLookupFilters": "Gespeicherte Filter löschen",
    "action.saveDefaultRules": "Standardregeln speichern",
    "action.saveLookupFilters": "Filter als Standard speichern",
    "action.saveSupplierRules": "Lieferantenregeln speichern",
    "action.resetToDefault": "Auf Standard zurücksetzen",
    "action.resetToSystemDefaults": "Auf Systemstandard zurücksetzen",
    "action.saveImport": "Import speichern",
    "action.selectAll": "Alle auswählen",
    "action.clearAll": "Alle abwählen",
    "action.excludeSelected": "Ausgewählte ausschließen",
    "action.keepOnlySelected": "Nur ausgewählte behalten",
    "action.upload": "Hochladen",
    "action.uploadFeed": "Feed hochladen",
    "action.close": "Schließen",
    "action.downloadCsv": "CSV",
    "action.downloadXls": "XLSX",
    "action.details": "Details",
    "action.hide": "Ausblenden",
    "action.show": "Einblenden",
    "action.setScope": "Scope setzen",
    "action.viewOverview": "Übersicht",
    "action.viewResearch": "Recherche",
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
    "field.filterBrands": "Marken ausschließen",
    "field.filterKeywords": "Titel-Keywords ausschließen",
    "field.excludeMissingEan": "Fehlende EAN ausschließen",
    "field.excludeNonNew": "Nicht neue / refurbished ausschließen",
    "field.fulfillmentFee": "Fulfillment-Gebühr",
    "field.highStock": "Hoher Bestand",
    "field.lowStock": "Niedriger Bestand",
    "field.marketplace": "Marktplatz",
    "field.maxSalesRank": "Max. Verkaufsrang",
    "field.mediumCostMax": "Mittlere Kosten max.",
    "field.mediumStock": "Mittlerer Bestand",
    "field.minCost": "Min. Kosten",
    "field.maxCost": "Max. Kosten",
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
    "quality.duplicateEan": "Doppelte EAN",
    "quality.missingEan": "Fehlende EAN",
    "quality.missingPrice": "Fehlender Preis",
    "quality.suspiciousPrice": "Verdächtiger Preis",
    "quality.unmappedColumns": "Nicht zugeordnete Spalten",
    "quality.weakMappings": "Schwache Zuordnungen",
    "ruleSection.dealFilters": "Deal-Filter",
    "ruleSection.feeModel": "Gebührenmodell",
    "ruleSection.priorityScores": "Prioritäts-Scoring",
    "ruleSection.thresholds": "Bestands- und Kostenschwellen",
    "message.createdQueueItems": "{count} Queue-Einträge erstellt",
    "message.noRecords": "Keine Einträge",
    "message.processedMatches": "{count} Matches verarbeitet",
    "message.keepaRun": "Keepa fertig: {created} vorbereitet, {processed} verarbeitet",
    "message.keepaRunWithSource": "Keepa fertig über {source}: {created} vorbereitet, {processed} verarbeitet",
    "message.keepaNotConfigured": "Echtes Keepa ist aktiv, aber KEEPA_API_KEY ist nicht konfiguriert",
    "message.researchRun": "Recherche fertig: {count} Matches verarbeitet",
    "message.lookupPlanHint": "Diese Kriterien definieren den nächsten Recherchelauf. Anwenden aktualisiert nur den Plan und ruft keine externen APIs auf.",
    "message.lookupSaveHint": "Gespeicherte Filter werden automatisch für diesen Scope angewendet. Die Batchgröße bleibt laufbezogen.",
    "message.lookupFiltersCleared": "Recherchefilter gelöscht",
    "message.lookupFilterResult": "{eligible} geeignet, {batch} im nächsten Lookup-Batch",
    "message.suggestionsShown": "{shown} von {total} angezeigt",
    "message.previewReady": "Vorschau bereit: {count} Zeilen",
    "message.importFilterResult": "{after} von {before} Zeilen werden importiert",
    "message.applyFiltersToUpdatePreview": "Filtervorschau anwenden, um Zeilen zu aktualisieren",
    "message.filteredPreviewReady": "Gefilterte Vorschau bereit: {count} Zeilen",
    "message.saved": "Gespeichert",
    "message.rulesReset": "Regeln zurückgesetzt",
    "message.savedImport": "{count} Angebote gespeichert",
    "message.uploaded": "Hochgeladen",
    "nav.pipeline": "Pipeline",
    "nav.keepa": "Keepa",
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
    "panel.qualityChecks": "Qualitätsprüfung",
    "panel.researchQueue": "Recherche-Queue",
    "panel.researchRules": "Recherche-Regeln",
    "panel.supplierFeed": "Lieferanten-Feed",
    "panel.supplierDetails": "Lieferanten-Details",
    "panel.supplierManagement": "Lieferantenverwaltung",
    "panel.importHistory": "Importhistorie",
    "panel.importFilters": "Importfilter",
    "panel.externalLookupPreview": "Recherche-Lookup-Plan",
    "panel.lookupSample": "Lookup-Beispiele",
    "panel.keepaMetrics": "Keepa-Metriken",
    "panel.offerStats": "Angebotsstatistik",
    "panel.recentOffers": "Letzte Angebote",
    "panel.pipelineStatus": "Pipeline-Status",
    "panel.nextActions": "Nächste Aktionen",
    "status.done": "Fertig",
    "status.failed": "Fehlgeschlagen",
    "status.idle": "Bereit",
    "status.running": "Läuft",
    "summary.amazonMatches": "Amazon Matches",
    "summary.dealCandidates": "Deal-Kandidaten",
    "summary.keepaMetrics": "Keepa-Metriken",
    "summary.eligibleExternal": "Geeignet",
    "summary.filteredOut": "Ausgefiltert",
    "summary.willRequest": "Wird angefragt",
    "summary.estimatedRequests": "Geschätzte API-Calls",
    "summary.queuePending": "In Queue",
    "summary.skippedReasons": "Ausfilter-Gründe",
    "summary.unqueuedOffers": "Noch nicht in Queue",
    "summary.researchQueue": "Recherche-Queue",
    "issue.amazonNotFound": "Amazon nicht gefunden",
    "issue.available": "Verfügbar",
    "issue.dealCandidates": "Deal-Kandidaten",
    "issue.keepaPending": "Keepa ausstehend",
    "issue.needsAmazonMatch": "Benötigt Amazon-Match",
    "issue.open": "Offen",
    "issue.rejectedLowRoi": "Abgelehnt: niedriger ROI",
    "issue.rejectedUnprofitable": "Abgelehnt: unprofitabel",
    "keepa.modeMock": "Mock-Modus",
    "keepa.modeReal": "Echte Keepa",
    "keepa.modeRealMissing": "Echte Keepa nicht konfiguriert",
    "keepa.sourceMock": "Mock",
    "keepa.sourceReal": "Echt",
    "keepa.sourceUnknown": "Unbekannt",
    "table.brand": "Marke",
    "table.buyBox": "Buy Box",
    "table.confidence": "Konfidenz",
    "table.detectedAs": "Erkannt als",
    "table.fileColumn": "Dateispalte",
    "table.priority": "Priorität",
    "table.profit": "Gewinn",
    "table.reason": "Grund",
    "table.roi": "ROI",
    "table.sales": "Verkäufe",
    "table.salesRank": "Sales Rank",
    "table.source": "Quelle",
    "table.keywords": "Keywords",
    "table.stock": "Bestand",
    "table.status": "Status",
    "table.supplier": "Lieferant",
    "table.file": "Datei",
    "table.rows": "Zeilen",
    "table.valid": "Gültig",
    "table.actions": "Aktionen",
    "table.failed": "Fehler",
    "table.importedAt": "Importiert am",
    "table.sku": "SKU",
    "table.cost": "Kosten",
    "table.title": "Titel",
    "table.visibility": "Sichtbarkeit",
    "status.hidden": "Ausgeblendet",
    "status.lookupPlanApplied": "Kriterien im Rechercheplan angewendet",
    "status.lookupPlanChanged": "Kriterien geändert, anwenden zum Aktualisieren",
    "status.lookupFiltersSaved": "Filter gespeichert",
    "status.lookupFiltersUnsaved": "Ungespeicherte Filter",
    "status.visible": "Sichtbar",
    "skip.above_max_cost": "Über Max.-Kosten",
    "skip.below_min_cost": "Unter Min.-Kosten",
    "skip.excluded_brand": "Marke",
    "skip.excluded_title_keyword": "Titel-Keyword",
    "skip.missing_cost": "Fehlende Kosten",
    "metric.avgCost": "Ø Kosten",
    "metric.createdAt": "Erstellt am",
    "metric.totalOffers": "Angebote gesamt",
    "metric.withBrand": "Mit Marke",
    "metric.withEan": "Mit EAN",
    "metric.withStock": "Mit Bestand",
    "metric.withTitle": "Mit Titel",
  },
  uk: {
    "action.populate": "Заповнити",
    "action.applyFilters": "Застосувати фільтри для превʼю",
    "action.process": "Обробити",
    "action.preview": "Превʼю",
    "action.updateLookupPlan": "Застосувати критерії research",
    "action.refresh": "Оновити",
    "action.runBatch": "Запустити batch",
    "action.runKeepa": "Запустити Keepa",
    "action.runResearch": "Запустити research",
    "action.save": "Зберегти",
    "action.clearLookupFilters": "Очистити збережені фільтри",
    "action.saveDefaultRules": "Зберегти дефолтні правила",
    "action.saveLookupFilters": "Зберегти фільтри як дефолт",
    "action.saveSupplierRules": "Зберегти правила постачальника",
    "action.resetToDefault": "Скинути до дефолту",
    "action.resetToSystemDefaults": "Скинути до системного дефолту",
    "action.saveImport": "Зберегти імпорт",
    "action.selectAll": "Вибрати всі",
    "action.clearAll": "Зняти всі",
    "action.excludeSelected": "Виключити вибрані",
    "action.keepOnlySelected": "Залишити тільки вибрані",
    "action.upload": "Завантажити",
    "action.uploadFeed": "Завантажити фід",
    "action.close": "Закрити",
    "action.downloadCsv": "CSV",
    "action.downloadXls": "XLSX",
    "action.details": "Деталі",
    "action.hide": "Сховати",
    "action.show": "Показати",
    "action.setScope": "Зробити scope",
    "action.viewOverview": "Огляд",
    "action.viewResearch": "Research",
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
    "field.filterBrands": "Виключити бренди",
    "field.filterKeywords": "Виключити keywords у назві",
    "field.excludeMissingEan": "Виключити рядки без EAN",
    "field.excludeNonNew": "Виключити не нові / refurbished",
    "field.fulfillmentFee": "Fulfillment fee",
    "field.highStock": "Високий stock",
    "field.lowStock": "Низький stock",
    "field.marketplace": "Маркетплейс",
    "field.maxSalesRank": "Макс. sales rank",
    "field.mediumCostMax": "Середня ціна макс.",
    "field.mediumStock": "Середній stock",
    "field.minCost": "Мін. ціна",
    "field.maxCost": "Макс. ціна",
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
    "quality.duplicateEan": "Дублікати EAN",
    "quality.missingEan": "Без EAN",
    "quality.missingPrice": "Без ціни",
    "quality.suspiciousPrice": "Підозріла ціна",
    "quality.unmappedColumns": "Нерозпізнані колонки",
    "quality.weakMappings": "Слабкі mappings",
    "ruleSection.dealFilters": "Фільтри угод",
    "ruleSection.feeModel": "Модель комісій",
    "ruleSection.priorityScores": "Scoring пріоритету",
    "ruleSection.thresholds": "Пороги stock і cost",
    "message.createdQueueItems": "Створено {count} елементів черги",
    "message.noRecords": "Немає записів",
    "message.processedMatches": "Оброблено {count} matches",
    "message.keepaRun": "Keepa завершено: {created} поставлено в чергу, {processed} оброблено",
    "message.keepaRunWithSource": "Keepa завершено через {source}: {created} поставлено в чергу, {processed} оброблено",
    "message.keepaNotConfigured": "Real Keepa увімкнена, але KEEPA_API_KEY не налаштований",
    "message.researchRun": "Research завершено: оброблено {count} matches",
    "message.lookupPlanHint": "Ці критерії задають наступний research run. Застосування оновлює тільки план і не викликає зовнішні API.",
    "message.lookupSaveHint": "Збережені фільтри застосовуються автоматично для цього scope. Batch size лишається параметром конкретного запуску.",
    "message.lookupFiltersCleared": "Research filters очищено",
    "message.lookupFilterResult": "{eligible} підходять, {batch} у наступному lookup batch",
    "message.suggestionsShown": "Показано {shown} з {total}",
    "message.previewReady": "Превʼю готове: {count} рядків",
    "message.importFilterResult": "Буде імпортовано {after} з {before} рядків",
    "message.applyFiltersToUpdatePreview": "Застосуй фільтри для оновлення рядків preview",
    "message.filteredPreviewReady": "Відфільтроване превʼю готове: {count} рядків",
    "message.saved": "Збережено",
    "message.rulesReset": "Правила скинуто",
    "message.savedImport": "Збережено {count} offers",
    "message.uploaded": "Завантажено",
    "nav.pipeline": "Pipeline",
    "nav.keepa": "Keepa",
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
    "panel.qualityChecks": "Перевірка якості",
    "panel.researchQueue": "Черга дослідження",
    "panel.researchRules": "Правила дослідження",
    "panel.supplierFeed": "Фід постачальника",
    "panel.supplierDetails": "Деталі постачальника",
    "panel.supplierManagement": "Керування постачальниками",
    "panel.importHistory": "Історія імпортів",
    "panel.importFilters": "Фільтри імпорту",
    "panel.externalLookupPreview": "План research lookup",
    "panel.lookupSample": "Приклад lookup",
    "panel.keepaMetrics": "Keepa метрики",
    "panel.offerStats": "Статистика offers",
    "panel.recentOffers": "Останні offers",
    "panel.pipelineStatus": "Pipeline статус",
    "panel.nextActions": "Наступні дії",
    "status.done": "Готово",
    "status.failed": "Помилка",
    "status.idle": "Очікує",
    "status.running": "Виконується",
    "summary.amazonMatches": "Amazon збіги",
    "summary.dealCandidates": "Кандидати угод",
    "summary.keepaMetrics": "Keepa метрики",
    "summary.eligibleExternal": "Підходять",
    "summary.filteredOut": "Відфільтровано",
    "summary.willRequest": "Піде в запит",
    "summary.estimatedRequests": "Оцінка API calls",
    "summary.queuePending": "У черзі",
    "summary.skippedReasons": "Причини відсіву",
    "summary.unqueuedOffers": "Ще не в черзі",
    "summary.researchQueue": "Черга дослідження",
    "issue.amazonNotFound": "Amazon не знайдено",
    "issue.available": "Доступно",
    "issue.dealCandidates": "Кандидати угод",
    "issue.keepaPending": "Keepa очікує",
    "issue.needsAmazonMatch": "Потрібен Amazon match",
    "issue.open": "Відкрито",
    "issue.rejectedLowRoi": "Відхилено: низький ROI",
    "issue.rejectedUnprofitable": "Відхилено: без прибутку",
    "keepa.modeMock": "Mock mode",
    "keepa.modeReal": "Real Keepa",
    "keepa.modeRealMissing": "Real Keepa не налаштована",
    "keepa.sourceMock": "Mock",
    "keepa.sourceReal": "Real",
    "keepa.sourceUnknown": "Невідомо",
    "table.brand": "Бренд",
    "table.buyBox": "Buy Box",
    "table.confidence": "Впевненість",
    "table.detectedAs": "Розпізнано як",
    "table.fileColumn": "Колонка файлу",
    "table.priority": "Пріоритет",
    "table.profit": "Прибуток",
    "table.reason": "Причина",
    "table.roi": "ROI",
    "table.sales": "Продажі",
    "table.salesRank": "Sales rank",
    "table.source": "Джерело",
    "table.keywords": "Keywords",
    "table.stock": "Stock",
    "table.status": "Статус",
    "table.supplier": "Постачальник",
    "table.file": "Файл",
    "table.rows": "Рядки",
    "table.valid": "Валідні",
    "table.actions": "Дії",
    "table.failed": "Помилки",
    "table.importedAt": "Імпортовано",
    "table.sku": "SKU",
    "table.cost": "Ціна",
    "table.title": "Назва",
    "table.visibility": "Видимість",
    "status.hidden": "Приховано",
    "status.lookupPlanApplied": "Критерії застосовані до research plan",
    "status.lookupPlanChanged": "Критерії змінені, застосуй щоб оновити план",
    "status.lookupFiltersSaved": "Фільтри збережено",
    "status.lookupFiltersUnsaved": "Є незбережені фільтри",
    "status.visible": "Видимий",
    "skip.above_max_cost": "Вище макс. ціни",
    "skip.below_min_cost": "Нижче мін. ціни",
    "skip.excluded_brand": "Бренд",
    "skip.excluded_title_keyword": "Keyword у назві",
    "skip.missing_cost": "Без ціни",
    "metric.avgCost": "Середня ціна",
    "metric.createdAt": "Створено",
    "metric.totalOffers": "Усього offers",
    "metric.withBrand": "З brand",
    "metric.withEan": "З EAN",
    "metric.withStock": "З stock",
    "metric.withTitle": "З title",
  },
};

const ruleHelp = {
  en: {
    min_priority_score: "Minimum priority score required before an offer is sent to Amazon matching.",
    min_roi_percent: "Minimum ROI percent needed for an evaluated offer to become a deal candidate.",
    min_profit: "Minimum estimated profit needed after supplier cost and estimated fees.",
    referral_fee_percent: "Estimated Amazon referral fee as a percent of Amazon sell price.",
    fulfillment_fee_fixed: "Fixed fulfillment cost used in the temporary fee model.",
    max_sales_rank: "Maximum accepted Amazon sales rank. Higher rank can be rejected.",
    min_monthly_sales: "Minimum estimated monthly sales required from market metrics.",
    exclude_amazon_in_stock: "Reject deals when Amazon itself is in stock for the product.",
    low_stock_threshold: "Stock value treated as low for priority scoring.",
    medium_stock_threshold: "Stock value treated as medium for priority scoring.",
    high_stock_threshold: "Stock value treated as high for priority scoring.",
    preferred_cost_min: "Lower bound of the preferred supplier cost range.",
    preferred_cost_max: "Upper bound of the preferred supplier cost range.",
    medium_cost_max: "Upper bound of the medium supplier cost range.",
    min_cost: "Supplier cost below this value receives the low-cost score.",
    score_stock_high: "Priority points added when stock is at or above the high threshold.",
    score_stock_medium: "Priority points added when stock is at or above the medium threshold.",
    score_stock_low: "Priority points added when stock is above the low threshold.",
    score_stock_very_low: "Priority points added when stock is at or below the low threshold.",
    score_cost_preferred: "Priority points added when supplier cost is in the preferred range.",
    score_cost_medium: "Priority points added when supplier cost is in the medium range.",
    score_cost_high: "Priority points added when supplier cost is above the medium range.",
    score_cost_low: "Priority points added when supplier cost is below the minimum cost.",
    score_brand_present: "Priority points added when a supplier offer has a brand.",
    score_title_present: "Priority points added when a supplier offer has a title.",
    score_ean_present: "Priority points added when a supplier offer has an EAN.",
  },
  de: {
    min_priority_score: "Mindest-Priorität, bevor ein Angebot ins Amazon-Matching geht.",
    min_roi_percent: "Mindest-ROI, damit ein geprüftes Angebot Deal-Kandidat wird.",
    min_profit: "Mindestgewinn nach Einkaufskosten und geschätzten Gebühren.",
    referral_fee_percent: "Geschätzte Amazon-Vermittlungsgebühr als Prozent vom Verkaufspreis.",
    fulfillment_fee_fixed: "Fester Fulfillment-Kostenwert im temporären Gebührenmodell.",
    max_sales_rank: "Maximal akzeptierter Amazon Sales Rank. Höhere Werte können abgelehnt werden.",
    min_monthly_sales: "Mindestanzahl geschätzter Monatsverkäufe aus Marktdaten.",
    exclude_amazon_in_stock: "Deals ablehnen, wenn Amazon selbst für dieses Produkt auf Lager ist.",
    low_stock_threshold: "Bestandswert, der für das Scoring als niedrig gilt.",
    medium_stock_threshold: "Bestandswert, der für das Scoring als mittel gilt.",
    high_stock_threshold: "Bestandswert, der für das Scoring als hoch gilt.",
    preferred_cost_min: "Untere Grenze des bevorzugten Einkaufspreisbereichs.",
    preferred_cost_max: "Obere Grenze des bevorzugten Einkaufspreisbereichs.",
    medium_cost_max: "Obere Grenze des mittleren Einkaufspreisbereichs.",
    min_cost: "Einkaufspreis unter diesem Wert erhält den Low-Cost-Score.",
    score_stock_high: "Prioritätspunkte bei Bestand ab hoher Schwelle.",
    score_stock_medium: "Prioritätspunkte bei Bestand ab mittlerer Schwelle.",
    score_stock_low: "Prioritätspunkte bei Bestand über niedriger Schwelle.",
    score_stock_very_low: "Prioritätspunkte bei Bestand auf oder unter niedriger Schwelle.",
    score_cost_preferred: "Prioritätspunkte für Einkaufspreis im bevorzugten Bereich.",
    score_cost_medium: "Prioritätspunkte für Einkaufspreis im mittleren Bereich.",
    score_cost_high: "Prioritätspunkte für Einkaufspreis oberhalb des mittleren Bereichs.",
    score_cost_low: "Prioritätspunkte für Einkaufspreis unter Mindestkosten.",
    score_brand_present: "Prioritätspunkte, wenn ein Angebot eine Marke hat.",
    score_title_present: "Prioritätspunkte, wenn ein Angebot einen Titel hat.",
    score_ean_present: "Prioritätspunkte, wenn ein Angebot eine EAN hat.",
  },
  uk: {
    min_priority_score: "Мінімальний priority score, щоб offer пішов у Amazon matching.",
    min_roi_percent: "Мінімальний ROI %, щоб offer став deal candidate.",
    min_profit: "Мінімальний очікуваний profit після cost і estimated fees.",
    referral_fee_percent: "Оцінка Amazon referral fee у відсотках від Amazon price.",
    fulfillment_fee_fixed: "Фіксована fulfillment fee у тимчасовій моделі комісій.",
    max_sales_rank: "Максимальний Amazon sales rank. Вищий rank може відхиляти deal.",
    min_monthly_sales: "Мінімальна оцінка місячних продажів з market metrics.",
    exclude_amazon_in_stock: "Відхиляти deal, якщо Amazon сам має товар in stock.",
    low_stock_threshold: "Stock-рівень, який вважається low для priority scoring.",
    medium_stock_threshold: "Stock-рівень, який вважається medium для priority scoring.",
    high_stock_threshold: "Stock-рівень, який вважається high для priority scoring.",
    preferred_cost_min: "Нижня межа бажаного supplier cost діапазону.",
    preferred_cost_max: "Верхня межа бажаного supplier cost діапазону.",
    medium_cost_max: "Верхня межа середнього supplier cost діапазону.",
    min_cost: "Supplier cost нижче цього значення отримує low-cost score.",
    score_stock_high: "Бали priority, якщо stock на high threshold або вище.",
    score_stock_medium: "Бали priority, якщо stock на medium threshold або вище.",
    score_stock_low: "Бали priority, якщо stock вище low threshold.",
    score_stock_very_low: "Бали priority, якщо stock на low threshold або нижче.",
    score_cost_preferred: "Бали priority для cost у бажаному діапазоні.",
    score_cost_medium: "Бали priority для cost у середньому діапазоні.",
    score_cost_high: "Бали priority для cost вище середнього діапазону.",
    score_cost_low: "Бали priority для cost нижче мінімального cost.",
    score_brand_present: "Бали priority, якщо в offer є brand.",
    score_title_present: "Бали priority, якщо в offer є title.",
    score_ean_present: "Бали priority, якщо в offer є EAN.",
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

function renderRuleHelpButtons() {
  document
    .querySelectorAll("#research-rules-form input[name]")
    .forEach((input) => {
      const helpText =
        ruleHelp[state.language]?.[input.name] || ruleHelp.en[input.name];

      if (!helpText) {
        return;
      }

      const label = input.closest("label");
      const labelText = label?.querySelector("span");

      if (!labelText) {
        return;
      }

      const button = document.createElement("button");
      button.type = "button";
      button.className = "help-button";
      button.textContent = "?";
      button.title = helpText;
      button.setAttribute("aria-label", helpText);
      labelText.appendChild(button);
    });
}

function renderResearchRulesActions() {
  const saveButton = document.querySelector("#save-research-rules-button");
  const resetButton = document.querySelector("#reset-research-rules-button");

  if (!saveButton || !resetButton) return;

  saveButton.textContent = state.supplierId
    ? t("action.saveSupplierRules")
    : t("action.saveDefaultRules");
  resetButton.textContent = state.supplierId
    ? t("action.resetToDefault")
    : t("action.resetToSystemDefaults");
}

function renderKeepaModeBadge() {
  const badge = document.querySelector("#keepa-mode-badge");
  const toggle = document.querySelector("#keepa-real-toggle");
  const runButton = document.querySelector("#run-keepa-button");

  if (!badge && !toggle && !runButton) return;

  const useRealKeepa = Boolean(state.settings?.use_real_keepa);
  const notConfigured = Boolean(
    useRealKeepa
    && state.keepaStatus
    && !state.keepaStatus.api_key_configured,
  );

  if (badge) {
    badge.textContent = notConfigured
      ? t("keepa.modeRealMissing")
      : (
        useRealKeepa
          ? t("keepa.modeReal")
          : t("keepa.modeMock")
      );
    badge.classList.toggle("ok", useRealKeepa && !notConfigured);
    badge.classList.toggle("warn", !useRealKeepa);
    badge.classList.toggle("bad", notConfigured);
  }

  if (toggle) {
    toggle.checked = useRealKeepa;
  }

  if (runButton) {
    runButton.disabled = notConfigured;
    runButton.title = notConfigured ? t("message.keepaNotConfigured") : "";
  }
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
  renderSupplierManagement();
  renderSuppliersDashboard();
  renderSupplierDetail(state.supplierDetail);

  if (state.importPreview) {
    renderImportPreview(state.importPreview);
  }

  renderSupplierSelect();
  renderRuleHelpButtons();
  renderResearchRulesActions();
  renderKeepaModeBadge();
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

function withQuery(path, params = {}) {
  const query = new URLSearchParams();

  Object.entries(params).forEach(([key, value]) => {
    if (value === undefined || value === null || value === "") return;
    if (Array.isArray(value) && value.length === 0) return;
    query.set(key, value);
  });

  const queryString = query.toString();

  if (!queryString) return path;

  return `${path}${path.includes("?") ? "&" : "?"}${queryString}`;
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

async function setSupplierScope(supplierId) {
  state.supplierId = String(supplierId);
  localStorage.setItem("oaSupplierId", state.supplierId);
  renderSupplierSelect();
  await Promise.all([
    loadSummary(),
    loadDeals(),
    loadResearch(),
    loadKeepa(),
    loadConfig(),
  ]);
}

function navigateToView(view) {
  document.querySelector(`[data-view="${view}"]`)?.click();
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

function keepaSourceLabel(source) {
  if (source === "keepa_mock") return t("keepa.sourceMock");
  if (source === "keepa_real") return t("keepa.sourceReal");

  return t("keepa.sourceUnknown");
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
            <div class="button-row">
              <button class="ghost-button" data-open-supplier-details="${supplier.id}" type="button">
                ${t("action.details")}
              </button>
              <button class="ghost-button" data-select-supplier="${supplier.id}" type="button">
                ${t("nav.overview")}
              </button>
            </div>
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

function renderSupplierManagement() {
  const body = document.querySelector("#supplier-management-table");

  if (!body) return;

  const rows = state.supplierManagement || [];
  const columns = [
    { key: "name", label: t("table.supplier") },
    { key: "offers_count", label: t("field.rows") },
    {
      key: "is_visible",
      label: t("table.visibility"),
      export: (supplier) => supplier.is_visible
        ? t("status.visible")
        : t("status.hidden"),
    },
  ];

  registerTableExport(
    "#supplier-management-table",
    t("panel.supplierManagement"),
    rows,
    columns,
  );

  body.innerHTML = rows.length
    ? rows
      .map((supplier) => `
        <tr>
          <td>${escapeHtml(supplier.name)}</td>
          <td>${formatNumber(supplier.offers_count)}</td>
          <td>
            <span class="badge ${supplier.is_visible ? "ok" : "warn"}">
              ${supplier.is_visible ? t("status.visible") : t("status.hidden")}
            </span>
          </td>
          <td>
            <div class="button-row table-actions">
              <button
                class="ghost-button"
                data-toggle-supplier-visibility="${supplier.id}"
                data-visible="${supplier.is_visible ? "false" : "true"}"
                type="button"
              >
                ${supplier.is_visible ? t("action.hide") : t("action.show")}
              </button>
              <button class="ghost-button" data-open-supplier-details="${supplier.id}" type="button">
                ${t("action.details")}
              </button>
            </div>
          </td>
        </tr>
      `)
      .join("")
    : `<tr><td colspan="4">${t("message.noRecords")}</td></tr>`;
}

function importMappingSummary(run = {}) {
  const mapped = run.mapped_columns || 0;
  const total = run.total_columns || 0;

  if (!total) return "-";

  return `${formatNumber(mapped)} / ${formatNumber(total)}`;
}

function renderSupplierDetail(detail) {
  const panel = document.querySelector("#supplier-detail");
  const grid = document.querySelector("#suppliers-dashboard");
  const management = document.querySelector("#supplier-management");

  if (!panel) return;

  if (!detail) {
    panel.classList.add("hidden");
    panel.innerHTML = "";
    grid?.classList.remove("hidden");
    management?.classList.remove("hidden");
    return;
  }

  const stats = detail.offer_stats || {};
  const imports = detail.import_history || [];
  const offers = detail.recent_offers || [];

  grid?.classList.add("hidden");
  management?.classList.add("hidden");
  panel.classList.remove("hidden");
  panel.innerHTML = `
    <div class="panel-header">
      <div>
        <h3>${t("panel.supplierDetails")}: ${escapeHtml(detail.name)}</h3>
        <p>${t("metric.createdAt")}: ${formatDate(detail.created_at)}</p>
      </div>
      <div class="button-row supplier-detail-actions">
        <button class="ghost-button" data-supplier-scope="${detail.id}" type="button">${t("action.setScope")}</button>
        <button class="ghost-button" data-supplier-nav="overview" data-supplier-id="${detail.id}" type="button">${t("action.viewOverview")}</button>
        <button class="ghost-button" data-supplier-nav="research" data-supplier-id="${detail.id}" type="button">${t("action.viewResearch")}</button>
        <button class="primary-button" data-run-supplier-research="${detail.id}" type="button">${t("action.runResearch")}</button>
        <button class="ghost-button" data-close-supplier-details type="button">${t("action.close")}</button>
      </div>
    </div>

    <section class="supplier-detail-grid">
      <article class="supplier-detail-section">
        <h4>${t("panel.offerStats")}</h4>
        <div class="preview-summary">
          <article><span>${t("metric.totalOffers")}</span><strong>${formatNumber(stats.total || 0)}</strong></article>
          <article><span>${t("metric.withEan")}</span><strong>${formatNumber(stats.with_ean || 0)}</strong></article>
          <article><span>${t("metric.withBrand")}</span><strong>${formatNumber(stats.with_brand || 0)}</strong></article>
          <article><span>${t("metric.withTitle")}</span><strong>${formatNumber(stats.with_title || 0)}</strong></article>
          <article><span>${t("metric.withStock")}</span><strong>${formatNumber(stats.with_stock || 0)}</strong></article>
          <article><span>${t("metric.avgCost")}</span><strong>${formatNumber(stats.avg_cost)}</strong></article>
        </div>
      </article>

      <article class="supplier-detail-section">
        <h4>${t("panel.pipelineStatus")}</h4>
        <div class="supplier-status-grid">
          <article>
            <span>${t("summary.researchQueue")}</span>
            <strong>${statusText(detail.statuses?.research_queue)}</strong>
          </article>
          <article>
            <span>${t("summary.amazonMatches")}</span>
            <strong>${statusText(detail.statuses?.amazon_matches)}</strong>
          </article>
          <article>
            <span>${t("summary.dealCandidates")}</span>
            <strong>${statusText(detail.statuses?.deal_candidates)}</strong>
          </article>
        </div>
      </article>
    </section>

    <section class="supplier-detail-section">
      <div class="section-title-row">
        <h4>${t("panel.importHistory")}</h4>
        <button class="ghost-button compact-button" data-export-table="#supplier-import-history-table" type="button">CSV</button>
      </div>
      <div class="table-wrap scroll-table compact-table">
        <table>
          <thead>
            <tr>
              <th>${t("table.file")}</th>
              <th>${t("table.rows")}</th>
              <th>${t("table.valid")}</th>
              <th>${t("table.failed")}</th>
              <th>${t("field.mapped")}</th>
              <th>${t("table.status")}</th>
              <th>${t("metric.createdAt")}</th>
            </tr>
          </thead>
          <tbody id="supplier-import-history-table">
            ${imports.length
              ? imports.map((run) => `
                <tr>
                  <td>${escapeHtml(run.filename)}</td>
                  <td>${formatNumber(run.rows_total)}</td>
                  <td>${formatNumber(run.rows_valid)}</td>
                  <td>${formatNumber(run.rows_failed)}</td>
                  <td>${importMappingSummary(run)}</td>
                  <td><span class="badge ${statusClass(run.status)}">${escapeHtml(run.status)}</span></td>
                  <td>${formatDate(run.created_at)}</td>
                </tr>
              `).join("")
              : `<tr><td colspan="7">${t("message.noRecords")}</td></tr>`}
          </tbody>
        </table>
      </div>
    </section>

    <section class="supplier-detail-section">
      <div class="section-title-row">
        <h4>${t("panel.recentOffers")}</h4>
        <button class="ghost-button compact-button" data-export-table="#supplier-recent-offers-table" type="button">CSV</button>
      </div>
      <div class="table-wrap scroll-table compact-table">
        <table>
          <thead>
            <tr>
              <th>EAN</th>
              <th>${t("table.sku")}</th>
              <th>${t("table.brand")}</th>
              <th>${t("table.title")}</th>
              <th>${t("table.cost")}</th>
              <th>${t("table.stock")}</th>
              <th>${t("table.importedAt")}</th>
            </tr>
          </thead>
          <tbody id="supplier-recent-offers-table">
            ${offers.length
              ? offers.map((offer) => `
                <tr>
                  <td>${escapeHtml(offer.ean) || "-"}</td>
                  <td>${escapeHtml(offer.supplier_sku) || "-"}</td>
                  <td>${escapeHtml(offer.brand) || "-"}</td>
                  <td>${escapeHtml(offer.title) || "-"}</td>
                  <td>${formatNumber(offer.cost)} ${escapeHtml(offer.currency) || ""}</td>
                  <td>${formatNumber(offer.stock)}</td>
                  <td>${formatDate(offer.imported_at)}</td>
                </tr>
              `).join("")
              : `<tr><td colspan="7">${t("message.noRecords")}</td></tr>`}
          </tbody>
        </table>
      </div>
    </section>
  `;

  registerTableExport(
    "#supplier-import-history-table",
    `${detail.name}-${t("panel.importHistory")}`,
    imports,
    [
      { key: "filename", label: t("table.file") },
      { key: "rows_total", label: t("table.rows") },
      { key: "rows_valid", label: t("table.valid") },
      { key: "rows_failed", label: t("table.failed") },
      {
        key: "mapped_columns",
        label: t("field.mapped"),
        export: (run) => importMappingSummary(run),
      },
      { key: "status", label: t("table.status") },
      { key: "created_at", label: t("metric.createdAt") },
    ],
  );
  registerTableExport(
    "#supplier-recent-offers-table",
    `${detail.name}-${t("panel.recentOffers")}`,
    offers,
    [
      { key: "ean", label: "EAN" },
      { key: "supplier_sku", label: t("table.sku") },
      { key: "brand", label: t("table.brand") },
      { key: "title", label: t("table.title") },
      {
        key: "cost",
        label: t("table.cost"),
        export: (offer) => [offer.cost, offer.currency].filter(Boolean).join(" "),
      },
      { key: "stock", label: t("table.stock") },
      { key: "imported_at", label: t("table.importedAt") },
    ],
  );
}

function qualityTone(count) {
  return count > 0 ? "bad" : "ok";
}

function renderQualityChecks(report = {}) {
  const grid = document.querySelector("#quality-grid");
  const details = document.querySelector("#quality-details");
  const checks = [
    ["quality.missingEan", report.missing_ean_count || 0],
    ["quality.missingPrice", report.missing_price_count || 0],
    ["quality.duplicateEan", report.duplicate_ean_count || 0],
    ["quality.suspiciousPrice", report.suspicious_price_count || 0],
    ["quality.unmappedColumns", (report.unmapped_columns || []).length],
    ["quality.weakMappings", (report.weak_mappings || []).length],
  ];

  grid.innerHTML = checks
    .map(([label, count]) => `
      <article class="quality-card ${qualityTone(count)}">
        <span>${t(label)}</span>
        <strong>${formatNumber(count)}</strong>
      </article>
    `)
    .join("");

  const detailItems = [];
  const exampleLabels = {
    missing_ean: "quality.missingEan",
    missing_price: "quality.missingPrice",
    duplicate_ean: "quality.duplicateEan",
    suspicious_price: "quality.suspiciousPrice",
  };

  if (report.unmapped_columns?.length) {
    detailItems.push(`
      <article>
        <span>${t("quality.unmappedColumns")}</span>
        <strong>${report.unmapped_columns.map(escapeHtml).join(", ")}</strong>
      </article>
    `);
  }

  if (report.weak_mappings?.length) {
    detailItems.push(`
      <article>
        <span>${t("quality.weakMappings")}</span>
        <strong>${report.weak_mappings
          .map((item) => `${escapeHtml(item.column)} -> ${escapeHtml(item.mapped_to)} (${formatNumber(item.confidence)}%)`)
          .join(", ")}</strong>
      </article>
    `);
  }

  Object.entries(report.examples || {}).forEach(([key, rows]) => {
    if (!rows?.length) return;

    detailItems.push(`
      <article>
        <span>${t(exampleLabels[key] || key)}</span>
        <strong>${rows
          .map((row) => Object.entries(row)
            .map(([name, value]) => `${escapeHtml(name)}: ${escapeHtml(value) || "-"}`)
            .join(" | "))
          .join(" / ")}</strong>
      </article>
    `);
  });

  details.innerHTML = detailItems.join("");
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

function renderRows(selector, rows, columns, options = {}) {
  const body = document.querySelector(selector);

  if (options.exportTitle) {
    registerTableExport(selector, options.exportTitle, rows, columns);
  }

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

function registerTableExport(selector, title, rows, columns) {
  state.tableExports[selector] = {
    title,
    rows: rows || [],
    columns: (columns || []).filter((column) => column.export !== false),
  };

  document.querySelectorAll(`[data-export-table="${selector}"]`).forEach((button) => {
    button.disabled = !(rows || []).length;
  });
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
  const value = column.export
    ? column.export(row)
    : row[column.key];

  if (value === null || value === undefined || value === "") return "";

  return String(value);
}

function downloadTableCsv(selector) {
  const tableExport = state.tableExports[selector];

  if (!tableExport) {
    showAlert(t("message.noRecords"), true);
    return;
  }

  const { title, rows, columns } = tableExport;

  if (!rows.length) {
    showAlert(t("message.noRecords"), true);
    return;
  }

  const header = columns
    .map((column) => csvEscape(column.label || column.key))
    .join(",");
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

async function downloadUploadPreviewCsv(button) {
  if (!state.importDraft?.import_token) {
    showAlert(t("message.noRecords"), true);
    return;
  }

  if (!state.importFiltersConfirmed) {
    showAlert(t("message.applyFiltersToUpdatePreview"), true);
    return;
  }

  button.disabled = true;

  try {
    const filters = state.importPreview?.filter_summary?.filters || null;
    const response = await fetch("/upload/export-preview", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        import_token: state.importDraft.import_token,
        filters,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(JSON.stringify(error.detail || error));
    }

    const blob = await response.blob();
    const disposition = response.headers.get("Content-Disposition") || "";
    const filename = disposition.match(/filename="([^"]+)"/)?.[1]
      || `${filenameSafe(selectedSupplierName())}-upload-preview.csv`;
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");

    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
  } catch (error) {
    showAlert(error.message, true);
  } finally {
    button.disabled = false;
  }
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
  const [visibleSuppliers, allSuppliers] = await Promise.all([
    api("/suppliers/"),
    api("/suppliers/?include_hidden=true"),
  ]);

  state.suppliers = visibleSuppliers;
  state.supplierManagement = allSuppliers;

  if (
    state.supplierId
    && !state.suppliers.some((supplier) => String(supplier.id) === state.supplierId)
  ) {
    state.supplierId = "";
    localStorage.removeItem("oaSupplierId");
  }

  renderSupplierSelect();
  renderSupplierManagement();
  renderResearchRulesActions();
}

async function loadSuppliersDashboard() {
  state.supplierDashboard = await api("/suppliers/dashboard");
  renderSuppliersDashboard();

  if (state.supplierDetail?.id) {
    await loadSupplierDetail(state.supplierDetail.id, { silent: true });
  }
}

async function loadSupplierDetail(supplierId, options = {}) {
  if (!options.silent) {
    document.querySelector("#supplier-detail").classList.remove("hidden");
    document.querySelector("#supplier-detail").innerHTML = `
      <div class="panel-header">
        <h3>${t("panel.supplierDetails")}</h3>
        <span class="badge warn">${t("status.running")}</span>
      </div>
    `;
  }

  state.supplierDetail = await api(`/suppliers/${supplierId}`);
  renderSupplierDetail(state.supplierDetail);
}

async function toggleSupplierVisibility(supplierId, isVisible) {
  await api(`/suppliers/${supplierId}/visibility`, {
    method: "PATCH",
    body: JSON.stringify({ is_visible: isVisible }),
  });

  if (!isVisible && String(supplierId) === state.supplierId) {
    state.supplierId = "";
    localStorage.removeItem("oaSupplierId");
  }

  await Promise.all([
    loadSuppliers(),
    loadSuppliersDashboard(),
    loadSummary(),
    loadDeals(),
    loadResearch(),
    loadKeepa(),
  ]);
}

async function loadConfig() {
  const [settings, rules, keepaStatus] = await Promise.all([
    api("/config/pipeline-settings"),
    api(scopedPath("/config/research-rules")),
    api("/keepa/status"),
  ]);

  state.settings = settings;
  state.rules = rules;
  state.keepaStatus = keepaStatus;

  fillForm(document.querySelector("#pipeline-settings-form"), settings);
  fillForm(document.querySelector("#research-rules-form"), rules);
  renderResearchRulesActions();
  renderKeepaModeBadge();
  renderResearchControls();
}

async function loadDeals() {
  const deals = await api(scopedPath("/deals/?limit=500"));
  renderRows("#deals-table", deals, [
    { key: "supplier_name", label: t("table.supplier") },
    { key: "asin", label: "ASIN" },
    {
      key: "roi_percent",
      label: t("table.roi"),
      render: (row) => formatNumber(row.roi_percent),
    },
    {
      key: "estimated_profit",
      label: t("table.profit"),
      render: (row) => formatNumber(row.estimated_profit),
    },
    {
      key: "status",
      label: t("table.status"),
      render: (row) => `<span class="badge ${statusClass(row.status)}">${row.status}</span>`,
    },
  ], { exportTitle: t("panel.dealCandidates") });
}

async function loadResearch() {
  const researchParams = researchLookupParams();
  const [queue, matches, lookupPreview] = await Promise.all([
    api(scopedPath("/research-queue/?limit=12")),
    api(scopedPath("/amazon-matches/?limit=12")),
    api(scopedPath(withQuery("/pipeline/external-lookup-preview", researchParams))),
  ]);

  renderLookupPreview(lookupPreview);

  renderRows("#queue-table", queue, [
    { key: "ean", label: "EAN" },
    { key: "supplier_name", label: t("table.supplier") },
    {
      key: "priority_score",
      label: t("table.priority"),
      render: (row) => formatNumber(row.priority_score),
    },
    {
      key: "status",
      label: t("table.status"),
      render: (row) => `<span class="badge ${statusClass(row.status)}">${row.status}</span>`,
    },
    { key: "brand", label: t("table.brand") },
  ], { exportTitle: t("panel.researchQueue") });

  renderRows("#matches-table", matches, [
    { key: "ean", label: "EAN" },
    { key: "supplier_name", label: t("table.supplier") },
    { key: "asin", label: "ASIN" },
    {
      key: "match_status",
      label: t("table.status"),
      render: (row) => `<span class="badge ${statusClass(row.match_status)}">${row.match_status}</span>`,
    },
    {
      key: "match_confidence",
      label: t("table.confidence"),
      render: (row) => formatNumber(row.match_confidence),
    },
  ], { exportTitle: t("panel.amazonMatches") });
}

function researchLookupParams() {
  const limit = document.querySelector("#lookup-limit")?.value;
  const minPriorityScore = document.querySelector("#lookup-min-priority")?.value;
  const minCost = document.querySelector("#lookup-filter-min-cost")?.value;
  const maxCost = document.querySelector("#lookup-filter-max-cost")?.value;

  return {
    limit,
    min_priority_score: minPriorityScore,
    exclude_brands: selectedFilterValues("[data-lookup-filter-brand]"),
    exclude_title_keywords: selectedFilterValues("[data-lookup-filter-keyword]"),
    min_cost: minCost,
    max_cost: maxCost,
  };
}

function lookupFilterPayload() {
  const params = researchLookupParams();

  return {
    lookup_excluded_brands: params.exclude_brands || [],
    lookup_excluded_title_keywords: params.exclude_title_keywords || [],
    lookup_min_cost: params.min_cost ? Number(params.min_cost) : null,
    lookup_max_cost: params.max_cost ? Number(params.max_cost) : null,
  };
}

function clearLookupFilterInputs() {
  document
    .querySelectorAll("[data-lookup-filter-brand], [data-lookup-filter-keyword]")
    .forEach((input) => {
      input.checked = false;
    });

  const minCost = document.querySelector("#lookup-filter-min-cost");
  const maxCost = document.querySelector("#lookup-filter-max-cost");

  if (minCost) minCost.value = "";
  if (maxCost) maxCost.value = "";
}

function renderResearchControls(preview = state.lookupPreview) {
  const limitInput = document.querySelector("#lookup-limit");
  const minPriorityInput = document.querySelector("#lookup-min-priority");

  if (!limitInput || !minPriorityInput) return;

  const settings = preview?.settings || {};

  limitInput.placeholder = settings.limit ?? state.settings?.default_batch_size ?? "";
  minPriorityInput.placeholder = settings.min_priority_score ?? state.rules?.min_priority_score ?? "";
  renderLookupPlanStatus();
  renderLookupSaveStatus();
}

function renderLookupPlanStatus() {
  const status = document.querySelector("#lookup-plan-status");

  if (!status) return;

  status.textContent = state.lookupPlanDirty
    ? t("status.lookupPlanChanged")
    : t("status.lookupPlanApplied");
  status.className = `badge ${state.lookupPlanDirty ? "warn" : "ok"}`;
}

function markLookupPlanDirty() {
  state.lookupPlanDirty = true;
  renderLookupPlanStatus();
  renderLookupSaveStatus(false);
}

function normalizeStringList(values = []) {
  return [...new Set((values || [])
    .map((value) => String(value || "").trim())
    .filter(Boolean))]
    .sort((a, b) => a.localeCompare(b));
}

function sameStringList(left = [], right = []) {
  const leftList = normalizeStringList(left);
  const rightList = normalizeStringList(right);

  return leftList.length === rightList.length
    && leftList.every((value, index) => value === rightList[index]);
}

function numericOrNull(value) {
  return value === undefined || value === null || value === ""
    ? null
    : Number(value);
}

function lookupFiltersMatchSaved() {
  if (!state.rules) return false;

  const payload = lookupFilterPayload();

  return sameStringList(
    payload.lookup_excluded_brands,
    state.rules.lookup_excluded_brands || [],
  )
    && sameStringList(
      payload.lookup_excluded_title_keywords,
      state.rules.lookup_excluded_title_keywords || [],
    )
    && numericOrNull(payload.lookup_min_cost) === numericOrNull(state.rules.lookup_min_cost)
    && numericOrNull(payload.lookup_max_cost) === numericOrNull(state.rules.lookup_max_cost);
}

function renderLookupSaveStatus(isSaved = lookupFiltersMatchSaved()) {
  const status = document.querySelector("#lookup-save-status");

  if (!status) return;

  status.textContent = isSaved
    ? t("status.lookupFiltersSaved")
    : t("status.lookupFiltersUnsaved");
  status.className = `badge ${isSaved ? "ok" : "warn"}`;
}

function renderCountList(items = []) {
  if (!items.length) return t("message.noRecords");

  return items
    .map((item) => `${escapeHtml(item.value)}: ${formatNumber(item.count)}`)
    .join(" | ");
}

function skippedReasonLabel(reason) {
  return t(`skip.${reason}`);
}

function renderSkippedBreakdown(items = []) {
  if (!items.length) return t("message.noRecords");

  return items
    .map((item) => {
      const values = (item.values || [])
        .map((value) => `${escapeHtml(value.value)}: ${formatNumber(value.count)}`)
        .join(", ");
      const details = values ? ` (${values})` : "";

      return `${skippedReasonLabel(item.reason)}: ${formatNumber(item.count)}${details}`;
    })
    .join(" | ");
}

function renderLookupPreview(preview = {}) {
  const grid = document.querySelector("#lookup-preview");

  if (!grid) return;

  state.lookupPreview = preview;
  state.lookupPlanDirty = false;
  renderResearchControls(preview);
  renderLookupFilters(preview);
  renderRows("#lookup-sample-table", preview.sample || [], [
    { key: "supplier_name", label: t("table.supplier") },
    { key: "ean", label: "EAN" },
    { key: "brand", label: t("table.brand") },
    { key: "title", label: t("table.title") },
    {
      key: "cost",
      label: t("table.cost"),
      render: (row) => [formatNumber(row.cost), escapeHtml(row.currency)]
        .filter(Boolean)
        .join(" "),
      export: (row) => [row.cost, row.currency].filter(Boolean).join(" "),
    },
    {
      key: "priority_score",
      label: t("table.priority"),
      render: (row) => formatNumber(row.priority_score),
    },
    {
      key: "source",
      label: t("table.source"),
      render: (row) => row.source === "supplier_offers"
        ? t("summary.unqueuedOffers")
        : t("summary.queuePending"),
      export: (row) => row.source === "supplier_offers"
        ? t("summary.unqueuedOffers")
        : t("summary.queuePending"),
    },
  ], { exportTitle: t("panel.lookupSample") });

  grid.innerHTML = `
    <article class="metric">
      <span>${t("summary.eligibleExternal")}</span>
      <strong>${formatNumber(preview.total_eligible || 0)}</strong>
      <small>${t("summary.filteredOut")}: ${formatNumber(preview.filtered_out || 0)}</small>
    </article>
    <article class="metric">
      <span>${t("summary.willRequest")}</span>
      <strong>${formatNumber(preview.will_request || 0)}</strong>
      <small>${t("field.batchSize")}: ${formatNumber(preview.limit)}</small>
    </article>
    <article class="metric">
      <span>${t("summary.estimatedRequests")}</span>
      <strong>${formatNumber(preview.estimated_external_requests || 0)}</strong>
      <small>${preview.settings?.use_real_keepa ? "Keepa" : "Mock"}</small>
    </article>
    <article class="metric lookup-list">
      <span>${t("table.brand")}</span>
      <strong>${renderCountList(preview.top_brands)}</strong>
      <small>${t("table.keywords")}: ${renderCountList(preview.top_title_keywords)}</small>
    </article>
    <article class="metric lookup-list">
      <span>${t("summary.skippedReasons")}</span>
      <strong>${renderSkippedBreakdown(preview.skipped_breakdown)}</strong>
      <small>${t("summary.filteredOut")}: ${formatNumber(preview.filtered_out || 0)}</small>
    </article>
  `;
}

async function loadKeepa() {
  const metrics = await api(scopedPath("/keepa/?limit=500"));

  renderRows("#keepa-table", metrics, [
    { key: "supplier_name", label: t("table.supplier") },
    { key: "asin", label: "ASIN" },
    {
      key: "data_status",
      label: t("table.status"),
      render: (row) => `<span class="badge ${statusClass(row.data_status)}">${escapeHtml(row.data_status)}</span>`,
    },
    {
      key: "data_source",
      label: t("table.source"),
      render: (row) => `<span class="badge ${row.data_source === "keepa_real" ? "ok" : "warn"}">${keepaSourceLabel(row.data_source)}</span>`,
      export: (row) => keepaSourceLabel(row.data_source),
    },
    {
      key: "buy_box_price",
      label: t("table.buyBox"),
      render: (row) => [formatNumber(row.buy_box_price), escapeHtml(row.currency)]
        .filter(Boolean)
        .join(" "),
      export: (row) => [row.buy_box_price, row.currency].filter(Boolean).join(" "),
    },
    {
      key: "sales_rank",
      label: t("table.salesRank"),
      render: (row) => formatNumber(row.sales_rank),
    },
    {
      key: "estimated_monthly_sales",
      label: t("table.sales"),
      render: (row) => formatNumber(row.estimated_monthly_sales),
    },
  ], { exportTitle: t("panel.keepaMetrics") });
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
      loadKeepa(),
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
    await Promise.all([loadSummary(), loadDeals(), loadResearch(), loadKeepa()]);
  } catch (error) {
    status.textContent = t("status.failed");
    status.className = "badge bad";
    showAlert(error.message, true);
  } finally {
    button.disabled = false;
  }
}

async function runResearch(triggerButton = null) {
  const button = triggerButton || document.querySelector("#run-research-button");
  const researchParams = researchLookupParams();

  button.disabled = true;

  try {
    const result = await api(scopedPath(withQuery("/pipeline/run-research", researchParams)), {
      method: "POST",
    });
    showAlert(t("message.researchRun", {
      count: result.amazon_processed?.processed_count || 0,
    }));
    await Promise.all([loadSummary(), loadResearch(), loadDeals(), loadKeepa()]);
  } catch (error) {
    showAlert(error.message, true);
  } finally {
    button.disabled = false;
  }
}

async function saveLookupFilters(button) {
  button.disabled = true;

  try {
    const result = await api(scopedPath("/config/research-rules"), {
      method: "PATCH",
      body: JSON.stringify(lookupFilterPayload()),
    });

    state.rules = result;
    renderLookupSaveStatus(true);
    showAlert(t("message.saved"));
    await loadResearch();
  } catch (error) {
    showAlert(error.message, true);
  } finally {
    button.disabled = false;
  }
}

async function clearLookupFilters(button) {
  button.disabled = true;

  try {
    clearLookupFilterInputs();

    const result = await api(scopedPath("/config/research-rules"), {
      method: "PATCH",
      body: JSON.stringify({
        lookup_excluded_brands: [],
        lookup_excluded_title_keywords: [],
        lookup_min_cost: null,
        lookup_max_cost: null,
      }),
    });

    state.rules = result;
    state.lookupPlanDirty = false;
    renderLookupPlanStatus();
    renderLookupSaveStatus(true);
    showAlert(t("message.lookupFiltersCleared"));
    await loadResearch();
  } catch (error) {
    showAlert(error.message, true);
  } finally {
    button.disabled = false;
  }
}

async function runKeepa(triggerButton = null) {
  const button = triggerButton || document.querySelector("#run-keepa-button");

  if (
    state.settings?.use_real_keepa
    && state.keepaStatus
    && !state.keepaStatus.api_key_configured
  ) {
    showAlert(t("message.keepaNotConfigured"), true);
    renderKeepaModeBadge();
    return;
  }

  button.disabled = true;

  try {
    const pendingResult = await api(scopedPath("/keepa/create-pending"), {
      method: "POST",
    });
    const processResult = await api(scopedPath("/keepa/process-pending"), {
      method: "POST",
    });

    if (processResult.status === "not_configured") {
      showAlert(
        processResult.reason || t("message.keepaNotConfigured"),
        true,
      );
    } else {
      showAlert(t("message.keepaRunWithSource", {
        source: keepaSourceLabel(processResult.data_source),
        created: pendingResult.created_count || 0,
        processed: processResult.processed_count || 0,
      }));
    }

    await Promise.all([loadSummary(), loadConfig(), loadKeepa(), loadDeals()]);
  } catch (error) {
    showAlert(error.message, true);
  } finally {
    button.disabled = false;
  }
}

async function saveKeepaMode(useRealKeepa, toggle) {
  toggle.disabled = true;

  try {
    const result = await api("/config/pipeline-settings", {
      method: "PATCH",
      body: JSON.stringify({ use_real_keepa: useRealKeepa }),
    });

    state.settings = result;
    state.keepaStatus = await api("/keepa/status");
    fillForm(document.querySelector("#pipeline-settings-form"), result);
    renderKeepaModeBadge();
    showAlert(t("message.saved"));
  } catch (error) {
    toggle.checked = !useRealKeepa;
    showAlert(error.message, true);
  } finally {
    toggle.disabled = false;
  }
}

async function runSupplierResearch(supplierId, button) {
  const previousSupplierId = state.supplierId;

  button.disabled = true;

  try {
    await setSupplierScope(supplierId);
    const result = await api(scopedPath(withQuery("/pipeline/run-research", researchLookupParams())), {
      method: "POST",
    });
    showAlert(t("message.researchRun", {
      count: result.amazon_processed?.processed_count || 0,
    }));
    await Promise.all([
      loadSummary(),
      loadResearch(),
      loadKeepa(),
      loadDeals(),
      loadSuppliersDashboard(),
      loadSupplierDetail(supplierId, { silent: true }),
    ]);
  } catch (error) {
    if (previousSupplierId) {
      state.supplierId = previousSupplierId;
      localStorage.setItem("oaSupplierId", state.supplierId);
    } else {
      state.supplierId = "";
      localStorage.removeItem("oaSupplierId");
    }

    renderSupplierSelect();
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
  if (form.id === "pipeline-settings-form") {
    state.settings = result;
    state.keepaStatus = await api("/keepa/status");
    renderKeepaModeBadge();
  }
  showAlert(t("message.saved"));
  await loadSummary();
}

async function resetResearchRules(button) {
  button.disabled = true;

  try {
    const result = await api(scopedPath("/config/research-rules/reset"), {
      method: "POST",
    });
    state.rules = result;
    fillForm(document.querySelector("#research-rules-form"), result);
    renderRuleHelpButtons();
    renderResearchRulesActions();
    showAlert(t("message.rulesReset"));
    await loadSummary();
  } catch (error) {
    showAlert(error.message, true);
  } finally {
    button.disabled = false;
  }
}

function setImportDraft(draft) {
  state.importDraft = draft;
  state.importFiltersConfirmed = Boolean(draft);
  updateSaveImportButton();

  if (!draft) {
    state.importFiltersConfirmed = false;
    state.importPreview = null;
    document.querySelector("#upload-preview").classList.add("hidden");
    updateSaveImportButton();
  }
}

function updateSaveImportButton() {
  document.querySelector("#save-import-button").classList.toggle(
    "hidden",
    !state.importDraft || !state.importFiltersConfirmed,
  );
}

function markImportFiltersDirty() {
  state.importFiltersConfirmed = false;
  updateSaveImportButton();

  const tableBody = document.querySelector("#preview-table-body");
  const tableHead = document.querySelector("#preview-table-head");
  const columnCount = tableHead?.querySelectorAll("th").length || 1;

  if (tableBody) {
    tableBody.innerHTML = `
      <tr>
        <td colspan="${columnCount}">${t("message.applyFiltersToUpdatePreview")}</td>
      </tr>
    `;
  }

  registerTableExport("#preview-table-body", t("panel.previewRows"), [], []);
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

  renderQualityChecks(result.quality_report || {});
  renderImportFilters(result);

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

  registerTableExport(
    "#preview-table-body",
    `${result.supplier_name}-${t("panel.previewRows")}`,
    rows,
    columns.map((column) => ({
      key: column,
      label: column,
    })),
  );

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

function selectedFilterValues(selector) {
  return [...document.querySelectorAll(`${selector}:checked`)]
    .map((element) => element.value);
}

function importBrandFilterMode() {
  return document.querySelector("[name='import-brand-filter-mode']:checked")?.value
    || "exclude";
}

function importFilterPayload() {
  const minPrice = document.querySelector("#import-filter-min-price")?.value;
  const maxPrice = document.querySelector("#import-filter-max-price")?.value;
  const brandFilterMode = importBrandFilterMode();
  const selectedBrands = selectedFilterValues("[data-import-filter-brand]");

  return {
    brand_filter_mode: brandFilterMode,
    excluded_brands: brandFilterMode === "exclude" ? selectedBrands : [],
    included_brands: brandFilterMode === "include" ? selectedBrands : [],
    excluded_keywords: selectedFilterValues("[data-import-filter-keyword]"),
    exclude_missing_ean: Boolean(
      document.querySelector("#import-filter-missing-ean")?.checked,
    ),
    exclude_non_new: Boolean(
      document.querySelector("#import-filter-non-new")?.checked,
    ),
    min_price: minPrice ? Number(minPrice) : null,
    max_price: maxPrice ? Number(maxPrice) : null,
  };
}

function estimateImportFilterResult() {
  const summary = document.querySelector("#import-filter-summary");
  const result = state.importPreview;

  if (!summary || !result) return;

  if (result.filter_summary) {
    summary.innerHTML = `
      <article>
        <span>${t("field.rows")}</span>
        <strong>${t("message.importFilterResult", {
          before: formatNumber(result.filter_summary.rows_before),
          after: formatNumber(result.filter_summary.rows_after),
        })}</strong>
      </article>
    `;
    state.importFiltersConfirmed = Boolean(result.is_filtered_preview);
    updateSaveImportButton();
    return;
  }

  const filters = importFilterPayload();
  const suggestions = result.filter_suggestions || {};
  const rows = result.rows || 0;
  const selectedBrandCounts = (suggestions.brands || [])
    .filter((item) => (
      filters.brand_filter_mode === "include"
        ? filters.included_brands.includes(item.value)
        : filters.excluded_brands.includes(item.value)
    ))
    .map((item) => item.count);
  const brandEstimate = selectedBrandCounts.reduce(
    (total, count) => total + count,
    0,
  );

  const estimatedExcluded = [
    filters.brand_filter_mode === "include"
      ? Math.max(0, rows - brandEstimate)
      : brandEstimate,
    ...(suggestions.title_keywords || [])
      .filter((item) => filters.excluded_keywords.includes(item.value))
      .map((item) => item.count),
    filters.exclude_missing_ean
      ? suggestions.missing_ean_count || 0
      : 0,
    filters.exclude_non_new
      ? suggestions.non_new_count || 0
      : 0,
  ].reduce((total, count) => total + count, 0);

  const after = Math.max(0, rows - estimatedExcluded);

  summary.innerHTML = `
    <article>
      <span>${t("field.rows")}</span>
      <strong>${t("message.importFilterResult", {
        before: formatNumber(rows),
        after: formatNumber(after),
      })}</strong>
    </article>
  `;

  updateSaveImportButton();
}

function renderFilterChoices(items, attribute, emptyLabel, selectedValues = []) {
  const selected = new Set(
    selectedValues.map((value) => String(value).toLowerCase()),
  );
  const choices = [...(items || [])];

  selectedValues.forEach((value) => {
    if (!choices.some((item) => String(item.value).toLowerCase() === String(value).toLowerCase())) {
      choices.unshift({ value, count: 0 });
    }
  });

  if (!choices.length) {
    return `<p class="muted-note">${emptyLabel}</p>`;
  }

  return choices
    .map((item) => `
      <label class="filter-choice">
        <input ${attribute} type="checkbox" value="${escapeHtml(item.value)}" ${selected.has(String(item.value).toLowerCase()) ? "checked" : ""}>
        <span>${escapeHtml(item.value)}</span>
        <strong>${formatNumber(item.count)}</strong>
      </label>
    `)
    .join("");
}

function renderImportFilters(result) {
  const controls = document.querySelector("#import-filter-controls");
  const suggestions = result.filter_suggestions || {};
  const activeFilters = result.filter_summary?.filters || {};
  const brandCount = suggestions.brands?.length || 0;
  const brandTotal = suggestions.brand_total_unique || brandCount;
  const brandFilterMode = activeFilters.brand_filter_mode
    || (activeFilters.included_brands?.length ? "include" : "exclude");
  const selectedBrands = brandFilterMode === "include"
    ? activeFilters.included_brands || []
    : activeFilters.excluded_brands || [];

  if (!controls) return;

  controls.innerHTML = `
    <section class="filter-panel">
      <h5>${t("field.filterBrands")}</h5>
      <p class="muted-note">${t("message.suggestionsShown", {
        shown: formatNumber(brandCount),
        total: formatNumber(brandTotal),
      })}</p>
      <div class="filter-mode-row">
        <label class="inline-toggle">
          <input name="import-brand-filter-mode" type="radio" value="exclude" ${brandFilterMode === "exclude" ? "checked" : ""}>
          <span>${t("action.excludeSelected")}</span>
        </label>
        <label class="inline-toggle">
          <input name="import-brand-filter-mode" type="radio" value="include" ${brandFilterMode === "include" ? "checked" : ""}>
          <span>${t("action.keepOnlySelected")}</span>
        </label>
      </div>
      <div class="filter-actions">
        <button class="ghost-button compact-button" data-filter-select-all="[data-import-filter-brand]" type="button">${t("action.selectAll")}</button>
        <button class="ghost-button compact-button" data-filter-clear-all="[data-import-filter-brand]" type="button">${t("action.clearAll")}</button>
      </div>
      <div class="filter-choice-list">
        ${renderFilterChoices(suggestions.brands, "data-import-filter-brand", t("message.noRecords"), selectedBrands)}
      </div>
    </section>
    <section class="filter-panel">
      <h5>${t("field.filterKeywords")}</h5>
      <div class="filter-choice-list">
        ${renderFilterChoices(suggestions.title_keywords, "data-import-filter-keyword", t("message.noRecords"))}
      </div>
    </section>
    <section class="filter-panel">
      <h5>${t("field.rows")}</h5>
      <label class="filter-choice">
        <input id="import-filter-missing-ean" type="checkbox">
        <span>${t("field.excludeMissingEan")}</span>
        <strong>${formatNumber(suggestions.missing_ean_count || 0)}</strong>
      </label>
      <label class="filter-choice">
        <input id="import-filter-non-new" type="checkbox">
        <span>${t("field.excludeNonNew")}</span>
        <strong>${formatNumber(suggestions.non_new_count || 0)}</strong>
      </label>
      <div class="price-filter-row">
        <label>
          <span>${t("field.minCost")}</span>
          <input id="import-filter-min-price" type="number" min="0" step="0.01" placeholder="${formatNumber(suggestions.price?.min)}">
        </label>
        <label>
          <span>${t("field.maxCost")}</span>
          <input id="import-filter-max-price" type="number" min="0" step="0.01" placeholder="${formatNumber(suggestions.price?.max)}">
        </label>
      </div>
    </section>
  `;

  controls.querySelectorAll("input").forEach((input) => {
    input.addEventListener("input", () => {
      markImportFiltersDirty();
      estimateImportFilterResult();
    });
    input.addEventListener("change", () => {
      markImportFiltersDirty();
      estimateImportFilterResult();
    });
  });

  controls.querySelectorAll("[data-filter-select-all], [data-filter-clear-all]").forEach((button) => {
    button.addEventListener("click", () => {
      const selector = button.dataset.filterSelectAll || button.dataset.filterClearAll;
      const checked = Boolean(button.dataset.filterSelectAll);

      controls.querySelectorAll(selector).forEach((input) => {
        input.checked = checked;
      });

      markImportFiltersDirty();
      estimateImportFilterResult();
    });
  });

  estimateImportFilterResult();
}

function renderLookupFilters(preview) {
  const summary = document.querySelector("#lookup-filter-summary");
  const controls = document.querySelector("#lookup-filter-controls");
  const filters = preview.external_filters || {};
  const excludedBrands = filters.exclude_brands || [];
  const excludedKeywords = filters.exclude_title_keywords || [];
  const minCost = filters.min_cost ?? "";
  const maxCost = filters.max_cost ?? "";

  if (!summary || !controls) return;

  summary.innerHTML = `
    <article>
      <span>${t("field.rows")}</span>
      <strong>${t("message.lookupFilterResult", {
        eligible: formatNumber(preview.total_eligible || 0),
        batch: formatNumber(preview.will_request || 0),
      })}</strong>
    </article>
    <article>
      <span>${t("summary.filteredOut")}</span>
      <strong>${formatNumber(preview.filtered_out || 0)}</strong>
    </article>
    <article>
      <span>${t("summary.estimatedRequests")}</span>
      <strong>${formatNumber(preview.estimated_external_requests || 0)}</strong>
    </article>
    <article>
      <span>${t("summary.queuePending")}</span>
      <strong>${formatNumber(preview.queue_pending_count || 0)}</strong>
    </article>
    <article>
      <span>${t("summary.unqueuedOffers")}</span>
      <strong>${formatNumber(preview.unqueued_offer_count || 0)}</strong>
    </article>
  `;

  controls.innerHTML = `
    <section class="filter-panel">
      <h5>${t("field.filterBrands")}</h5>
      <div class="filter-choice-list">
        ${renderFilterChoices(
          preview.top_brands,
          "data-lookup-filter-brand",
          t("message.noRecords"),
          excludedBrands,
        )}
      </div>
    </section>
    <section class="filter-panel">
      <h5>${t("field.filterKeywords")}</h5>
      <div class="filter-choice-list">
        ${renderFilterChoices(
          preview.top_title_keywords,
          "data-lookup-filter-keyword",
          t("message.noRecords"),
          excludedKeywords,
        )}
      </div>
    </section>
    <section class="filter-panel">
      <h5>${t("table.cost")}</h5>
      <div class="price-filter-row">
        <label>
          <span>${t("field.minCost")}</span>
          <input id="lookup-filter-min-cost" type="number" min="0" step="0.01" value="${escapeHtml(minCost)}" placeholder="${formatNumber(preview.price?.min)}">
        </label>
        <label>
          <span>${t("field.maxCost")}</span>
          <input id="lookup-filter-max-cost" type="number" min="0" step="0.01" value="${escapeHtml(maxCost)}" placeholder="${formatNumber(preview.price?.max)}">
        </label>
      </div>
    </section>
  `;

  controls.querySelectorAll("input").forEach((input) => {
    input.addEventListener("input", markLookupPlanDirty);
    input.addEventListener("change", markLookupPlanDirty);
  });
  renderLookupSaveStatus();
}

async function applyImportFilters(button) {
  if (!state.importDraft?.import_token) return;

  button.disabled = true;

  try {
    const result = await api("/upload/filter-preview", {
      method: "POST",
      body: JSON.stringify({
        import_token: state.importDraft.import_token,
        filters: importFilterPayload(),
      }),
    });

    setImportDraft(result);
    renderImportPreview(result);
    showAlert(t("message.filteredPreviewReady", { count: result.rows }));
  } catch (error) {
    showAlert(error.message, true);
  } finally {
    button.disabled = false;
  }
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
  document.addEventListener("click", (event) => {
    const exportButton = event.target.closest("[data-export-table]");

    if (!exportButton) return;

    downloadTableCsv(exportButton.dataset.exportTable);
  });
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
      await Promise.all([
        loadSummary(),
        loadDeals(),
        loadResearch(),
        loadKeepa(),
        loadConfig(),
      ]);
    } catch (error) {
      showAlert(error.message, true);
    }
  });
  document.querySelector("#run-batch-button").addEventListener("click", runBatch);
  document.querySelector("#run-research-button").addEventListener("click", (event) => {
    runResearch(event.currentTarget);
  });
  document.querySelector("#run-keepa-button").addEventListener("click", (event) => {
    runKeepa(event.currentTarget);
  });
  document.querySelector("#refresh-lookup-preview-button").addEventListener("click", () => {
    loadResearch().catch((error) => showAlert(error.message, true));
  });
  document.querySelector("#apply-lookup-controls-button").addEventListener("click", () => {
    loadResearch().catch((error) => showAlert(error.message, true));
  });
  document.querySelector("#save-lookup-filters-button").addEventListener("click", (event) => {
    saveLookupFilters(event.currentTarget);
  });
  document.querySelector("#clear-lookup-filters-button").addEventListener("click", (event) => {
    clearLookupFilters(event.currentTarget);
  });
  document.querySelectorAll("#lookup-limit, #lookup-min-priority").forEach((input) => {
    input.addEventListener("input", markLookupPlanDirty);
    input.addEventListener("keydown", (event) => {
      if (event.key !== "Enter") return;
      event.preventDefault();
      loadResearch().catch((error) => showAlert(error.message, true));
    });
  });
  document.querySelector("#keepa-real-toggle").addEventListener("change", (event) => {
    saveKeepaMode(event.currentTarget.checked, event.currentTarget);
  });
  document.querySelector(".overview-actions").addEventListener("click", (event) => {
    const button = event.target.closest("[data-overview-action]");

    if (!button) return;

    const action = button.dataset.overviewAction;

    if (action === "upload" || action === "pipeline") {
      navigateToView(action);
      return;
    }

    if (action === "research") {
      runResearch(button);
      return;
    }

    if (action === "keepa") {
      runKeepa(button);
    }
  });
  document.querySelector("#refresh-deals-button").addEventListener("click", loadDeals);
  document.querySelector("#refresh-issues-button").addEventListener("click", loadSummary);
  document.querySelector("#pipeline-issues").addEventListener("click", (event) => {
    const button = event.target.closest("[data-issue-key]");

    if (!button) return;

    openIssueModal(button.dataset.issueKey);
  });
  document.querySelector("#suppliers-dashboard").addEventListener("click", async (event) => {
    const detailButton = event.target.closest("[data-open-supplier-details]");
    const button = event.target.closest("[data-select-supplier]");

    if (detailButton) {
      try {
        await loadSupplierDetail(detailButton.dataset.openSupplierDetails);
      } catch (error) {
        showAlert(error.message, true);
      }

      return;
    }

    if (!button) return;

    state.supplierId = button.dataset.selectSupplier;
    localStorage.setItem("oaSupplierId", state.supplierId);
    renderSupplierSelect();

    document.querySelector('[data-view="overview"]').click();

    try {
      await Promise.all([loadSummary(), loadDeals(), loadResearch(), loadKeepa()]);
    } catch (error) {
      showAlert(error.message, true);
    }
  });
  document.querySelector("#supplier-management").addEventListener("click", async (event) => {
    const detailButton = event.target.closest("[data-open-supplier-details]");
    const visibilityButton = event.target.closest("[data-toggle-supplier-visibility]");

    if (detailButton) {
      try {
        await loadSupplierDetail(detailButton.dataset.openSupplierDetails);
      } catch (error) {
        showAlert(error.message, true);
      }

      return;
    }

    if (!visibilityButton) return;

    visibilityButton.disabled = true;

    try {
      await toggleSupplierVisibility(
        visibilityButton.dataset.toggleSupplierVisibility,
        visibilityButton.dataset.visible === "true",
      );
    } catch (error) {
      showAlert(error.message, true);
    } finally {
      visibilityButton.disabled = false;
    }
  });
  document.querySelector("#supplier-detail").addEventListener("click", (event) => {
    const closeButton = event.target.closest("[data-close-supplier-details]");
    const scopeButton = event.target.closest("[data-supplier-scope]");
    const navButton = event.target.closest("[data-supplier-nav]");
    const researchButton = event.target.closest("[data-run-supplier-research]");

    if (scopeButton) {
      setSupplierScope(scopeButton.dataset.supplierScope)
        .catch((error) => showAlert(error.message, true));
      return;
    }

    if (navButton) {
      setSupplierScope(navButton.dataset.supplierId)
        .then(() => {
          state.supplierDetail = null;
          renderSupplierDetail(null);
          navigateToView(navButton.dataset.supplierNav);
        })
        .catch((error) => showAlert(error.message, true));
      return;
    }

    if (researchButton) {
      runSupplierResearch(
        researchButton.dataset.runSupplierResearch,
        researchButton,
      );
      return;
    }

    if (!closeButton) return;

    state.supplierDetail = null;
    renderSupplierDetail(null);
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
      await saveForm(
        event.currentTarget,
        scopedPath("/config/research-rules"),
      );
      await loadConfig();
    } catch (error) {
      showAlert(error.message, true);
    }
  });
  document.querySelector("#reset-research-rules-button").addEventListener("click", (event) => {
    resetResearchRules(event.currentTarget);
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

  document.querySelector("#apply-import-filters-button").addEventListener("click", (event) => {
    applyImportFilters(event.currentTarget);
  });
  document.querySelector("#download-upload-preview-csv").addEventListener("click", (event) => {
    downloadUploadPreviewCsv(event.currentTarget);
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
      await Promise.all([
        loadSummary(),
        loadResearch(),
        loadKeepa(),
        loadSuppliers(),
        loadSuppliersDashboard(),
      ]);
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
