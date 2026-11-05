const state = {
  summary: null,
  settings: null,
  keepaStatus: null,
  rules: null,
  suppliers: [],
  supplierManagement: [],
  supplierDashboard: [],
  savedImports: [],
  supplierDetail: null,
  procurementComparison: null,
  procurementGrid: null,
  procurementGridLanguage: null,
  supplierId: localStorage.getItem("oaSupplierId") || "",
  importDraft: null,
  importFiltersConfirmed: false,
  supplyChannelsConfirmed: false,
  importPreview: null,
  issueExport: null,
  tableExports: {},
  lookupPreview: null,
  lookupPlanDirty: false,
  maintenance: null,
  authUser: null,
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
    "action.loadLatestPrice": "Load latest price",
    "action.checkPriceUpdate": "Check for update",
    "action.runAmazonPresence": "Check Amazon presence",
    "action.runKeepa": "Run Keepa",
    "action.runMarketSnapshot": "Run snapshot",
    "action.createDeals": "Create deals",
    "action.runResearch": "Run research",
    "action.save": "Save",
    "action.savePriceLink": "Save link",
    "action.clearLookupFilters": "Clear saved filters",
    "action.saveDefaultRules": "Save default rules",
    "action.saveLookupFilters": "Save filters as defaults",
    "action.saveSupplierRules": "Save supplier rules",
    "action.resetToDefault": "Reset to default",
    "action.resetToSystemDefaults": "Reset to system defaults",
    "action.resetColumns": "Reset columns",
    "action.newUpload": "New upload",
    "action.saveImport": "Save import",
    "action.deleteImport": "Delete import",
    "action.deleteOldImports": "Delete imports older than 30 days",
    "action.selectAll": "Select all",
    "action.clearAll": "Clear all",
    "action.search": "Search",
    "action.searchPreview": "Search",
    "action.clearSearch": "Clear search",
    "action.clear": "Clear",
    "action.compare": "Compare",
    "action.clearWorkspace": "Clear preview workspace",
    "action.clearDatabase": "Clear database data",
    "action.managePrice": "Price & filters",
    "action.addSupplier": "Add supplier",
    "action.excludeSelected": "Exclude selected",
    "action.keepOnlySelected": "Keep only selected",
    "action.upload": "Upload",
    "action.uploadFeed": "Upload feed",
    "action.close": "Close",
    "action.logout": "Logout",
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
    "field.feedFile": "CSV, Excel or ZIP files",
    "field.fileCount": "Files",
    "field.skippedFiles": "Skipped archive entries",
    "field.file": "File",
    "field.supplyChannel": "Supply category",
    "field.leadTime": "Lead time",
    "field.leadTimeMinDays": "Lead time min (days)",
    "field.leadTimeMaxDays": "Lead time max (days)",
    "field.filterBrands": "Exclude brands",
    "field.filterKeywords": "Exclude title keywords",
    "field.excludeMissingEan": "Exclude missing EAN",
    "field.excludeNonNew": "Exclude non-new / refurbished",
    "field.excludeTesters": "Tester products are always skipped",
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
    "field.priceUrl": "Latest price URL",
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
    "field.productList": "Product list",
    "field.targetCurrency": "Currency",
    "field.includeHiddenSuppliers": "Include hidden suppliers",
    "field.pricesIncludeVat": "Prices already include VAT",
    "field.defaultVatRate": "Default VAT rate %",
    "field.purchaseQuantity": "Quantity",
    "field.columns": "Columns",
    "field.mapped": "Mapped",
    "quality.duplicateEan": "Duplicate EAN",
    "quality.missingEan": "Missing EAN",
    "quality.invalidEan": "Invalid EAN",
    "quality.supplierCode": "Supplier code (not GTIN)",
    "quality.testerRows": "Tester products (skipped)",
    "quality.missingPrice": "Missing price",
    "quality.suspiciousPrice": "Suspicious price",
    "quality.unmappedColumns": "Unmapped columns",
    "quality.weakMappings": "Weak mappings",
    "ruleSection.dealFilters": "Deal filters",
    "ruleSection.feeModel": "Fee model",
    "ruleSection.priorityScores": "Priority scoring",
    "ruleSection.thresholds": "Stock and cost thresholds",
    "message.createdQueueItems": "Created {count} queue items",
    "message.maintenanceHint": "Release memory or remove imported catalog data.",
    "message.clearWorkspaceHint": "Removes active upload previews and releases their memory. Saved database data is preserved.",
    "message.clearDatabaseHint": "Removes imported offers, import history, research, matches, metrics, presence checks, and deals. Supplier links, filters, rules, and settings are preserved.",
    "message.confirmClearWorkspace": "Clear all active upload previews? Saved database data will not be changed.",
    "message.confirmClearDatabase": "Clear all imported catalog and pipeline data? Supplier setup, links, filters, rules, and settings will remain.",
    "message.workspaceCleared": "Preview workspace cleared: {drafts} drafts, {rows} rows released",
    "message.databaseCleared": "Database data cleared: {rows} rows removed",
    "message.maintenanceResult": "{action}: {rows} rows removed, {size} released",
    "message.noSuppliersYet": "No suppliers yet. Add one above with an optional price URL, or preview and save the first price file in Upload.",
    "message.noRecords": "No records",
    "message.productListPlaceholder": "1. Product name — EAN 4006381333931",
    "message.comparisonComplete": "Compared {count} products",
    "message.invalidProductLines": "Lines without a valid EAN: {count}",
    "message.supplierPricingSaved": "Supplier VAT settings saved",
    "message.processedMatches": "Processed {count} matches",
    "message.keepaRun": "Keepa completed: {created} queued, {processed} processed",
    "message.keepaRunWithSource": "Keepa completed via {source}: {created} queued, {processed} processed",
    "message.keepaNotConfigured": "Real Keepa is enabled, but KEEPA_API_KEY is not configured",
    "message.keepaPermissionRequired": "Live Keepa access is limited to the authorized Keepa seat",
    "message.keepaRateLimited": "Keepa tokens are not available yet. Tokens left: {tokens}. Try again in about {wait} seconds.",
    "message.marketSnapshotRun": "Market snapshot completed via {source}: {created} queued, {processed} processed",
    "message.dealsCreated": "Deal candidates created: {count}",
    "message.amazonPresenceRun": "Amazon presence completed via {source}: {created} queued, {processed} processed",
    "message.researchRun": "Research completed: {count} matches processed",
    "message.lookupPlanHint": "These criteria define the next research run. Applying them updates the plan only; it does not call external APIs.",
    "message.lookupSaveHint": "Saved filters are applied automatically for this scope. Batch size stays run-specific.",
    "message.lookupFiltersCleared": "Research filters cleared",
    "message.lookupFilterResult": "{eligible} eligible, {batch} in next lookup batch",
    "message.suggestionsShown": "Showing {shown} of {total}",
    "message.previewReady": "Preview ready: {count} rows",
    "message.batchPreviewReady": "Preview ready: {files} files, {count} rows",
    "message.importFilterResult": "{after} of {before} rows will be imported",
    "message.testersSkipped": "Tester products skipped: {count}",
    "message.applyFiltersToUpdatePreview": "Apply filters preview to update rows",
    "message.filteredPreviewReady": "Filtered preview ready: {count} rows",
    "message.searchPlaceholder": "Search all filtered rows by SKU, EAN, title, brand...",
    "message.searchResults": "Found {total}; showing {shown}",
    "message.saved": "Saved",
    "message.priceLinkSaved": "Supplier price link saved",
    "message.pricePreviewReady": "Latest supplier price loaded: {count} rows",
    "message.priceCheckResult": "{supplier}: {status}. Checked {checked}",
    "message.savedSupplierFilters": "Last supplier filters will be applied automatically",
    "message.noSavedSupplierFilters": "No saved supplier filters yet",
    "message.rulesReset": "Rules reset",
    "message.savedImport": "Saved {count} offers",
    "message.supplyChannelHint": "The category is detected from the filename and workbook content. Review it before saving.",
    "message.confirmSupplyChannels": "I confirm the supply category for every file",
    "message.confirmDeleteImport": "Delete this saved import from history?",
    "message.confirmDeleteActiveImport": "Delete the current saved price list? Current supplier offers and derived pipeline data will also be removed.",
    "message.confirmDeleteOldImports": "Delete all imports older than 30 days? If the current catalog is older, its offers and derived pipeline data will also be removed.",
    "message.importsDeleted": "Deleted {imports} imports and {offers} current offers",
    "message.savedPriceListsHint": "Manage imported supplier price lists without opening a supplier first.",
    "message.uploaded": "Uploaded",
    "nav.pipeline": "Pipeline",
    "nav.keepa": "Keepa",
    "nav.overview": "Overview",
    "nav.research": "Research",
    "nav.rules": "Rules",
    "nav.settings": "Settings",
    "nav.suppliers": "Suppliers",
    "nav.upload": "Upload",
    "nav.procurement": "Price comparison",
    "panel.recentImports": "Recent Imports",
    "panel.amazonMatches": "Amazon Matches",
    "panel.dealCandidates": "Deal Candidates",
    "panel.pipelineRun": "Pipeline Run",
    "panel.pipelineSettings": "Pipeline Settings",
    "panel.pipelineIssues": "Pipeline Issues",
    "panel.columnMapping": "Column Mapping",
    "panel.previewRows": "Preview Rows",
    "panel.supplyChannels": "Supply categories",
    "supply.stock": "In stock",
    "supply.incoming": "Incoming",
    "supply.preorder": "Preorder",
    "panel.qualityChecks": "Quality Checks",
    "panel.fileDiagnostics": "Quality by file",
    "panel.researchQueue": "Research Queue",
    "panel.researchRules": "Research Rules",
    "panel.supplierFeed": "Supplier Feed",
    "panel.supplierDetails": "Supplier Details",
    "panel.supplierManagement": "Supplier Management",
    "panel.procurementComparison": "Supplier price comparison",
    "procurement.gridHint": "Drag columns to reorder them and drag their borders to resize.",
    "panel.comparisonResults": "Comparison results",
    "panel.vatSettings": "VAT settings",
    "panel.importHistory": "Import History",
    "panel.savedPriceLists": "Saved price lists",
    "panel.importFilters": "Import Filters",
    "panel.externalLookupPreview": "Research lookup plan",
    "panel.lookupSample": "Lookup sample",
    "panel.marketSnapshots": "Market Snapshots",
    "panel.keepaMetrics": "Keepa Metrics",
    "panel.amazonPresence": "Amazon Presence",
    "panel.offerStats": "Offer Stats",
    "panel.recentOffers": "Recent Offers",
    "panel.pipelineStatus": "Pipeline Status",
    "panel.maintenance": "Maintenance",
    "panel.priceSource": "Price Source",
    "maintenance.workspaceUsage": "Preview workspace",
    "maintenance.databaseUsage": "Operational database",
    "panel.nextActions": "Next Actions",
    "status.done": "Done",
    "status.failed": "Failed",
    "status.idle": "Idle",
    "status.running": "Running",
    "priceStatus.not_configured": "Not configured",
    "priceStatus.never_downloaded": "Never downloaded",
    "priceStatus.current": "Current",
    "priceStatus.no_changes": "No changes",
    "priceStatus.new_available": "New price available",
    "priceStatus.verification_required": "Download required to verify",
    "priceStatus.check_failed": "Check failed",
    "summary.amazonMatches": "Amazon Matches",
    "summary.marketSnapshots": "Market Snapshots",
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
    "summary.requestedProducts": "Requested",
    "summary.locatedProducts": "Offers found",
    "summary.matchedProducts": "Ready to compare",
    "summary.needsConfiguration": "Needs setup",
    "summary.unmatchedProducts": "Not found",
    "summary.invalidLines": "Invalid lines",
    "issue.amazonNotFound": "Amazon not found",
    "issue.available": "Available",
    "issue.dealCandidates": "Deal candidates",
    "issue.keepaPending": "Keepa pending",
    "issue.marketSnapshotPending": "Market snapshot pending",
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
    "comparison.matched": "Matched",
    "comparison.not_found": "Not found",
    "comparison.currency_mismatch": "Currency mismatch",
    "comparison.missing_cost": "Missing cost",
    "comparison.minimum_quantity": "Below minimum quantity",
    "comparison.minimumQuantityValue": "minimum {count}",
    "table.brand": "Brand",
    "table.buyBox": "Buy Box",
    "table.confidence": "Confidence",
    "table.currentPrice": "Current price",
    "table.detectedAs": "Detected as",
    "table.fileColumn": "File column",
    "table.priority": "Priority",
    "table.profit": "Profit",
    "table.reason": "Reason",
    "table.roi": "ROI",
    "table.sales": "Sales",
    "table.salesRank": "Sales rank",
    "table.sellerCount": "Sellers",
    "table.source": "Source",
    "table.keywords": "Keywords",
    "table.stock": "Stock",
    "table.status": "Status",
    "table.supplier": "Supplier",
    "table.requestedProduct": "Requested product",
    "table.bestSupplier": "Supplier / best offer",
    "table.sourceCost": "Price",
    "table.offers": "Offers",
    "table.winner": "Winner",
    "table.file": "File",
    "table.rows": "Rows",
    "table.valid": "Valid",
    "table.actions": "Actions",
    "table.amazonPresent": "Amazon present",
    "table.failed": "Failed",
    "table.importedAt": "Imported at",
    "table.priceDate": "Price imported",
    "freshness.today": "today",
    "freshness.oneDayAgo": "1 day ago",
    "freshness.daysAgo": "{count} days ago",
    "table.sku": "SKU",
    "table.cost": "Cost",
    "table.title": "Title",
    "table.visibility": "Visibility",
    "table.priceSource": "Price source",
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
    "metric.lastChecked": "Last checked",
    "metric.lastDownloaded": "Last downloaded",
    "metric.fileSize": "File size",
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
    "action.loadLatestPrice": "Aktuelle Preisliste laden",
    "action.checkPriceUpdate": "Auf Update prüfen",
    "action.runAmazonPresence": "Amazon Presence prüfen",
    "action.runKeepa": "Keepa starten",
    "action.runMarketSnapshot": "Snapshot starten",
    "action.createDeals": "Deals erstellen",
    "action.runResearch": "Recherche starten",
    "action.save": "Speichern",
    "action.savePriceLink": "Link speichern",
    "action.clearLookupFilters": "Gespeicherte Filter löschen",
    "action.saveDefaultRules": "Standardregeln speichern",
    "action.saveLookupFilters": "Filter als Standard speichern",
    "action.saveSupplierRules": "Lieferantenregeln speichern",
    "action.resetToDefault": "Auf Standard zurücksetzen",
    "action.resetToSystemDefaults": "Auf Systemstandard zurücksetzen",
    "action.resetColumns": "Spalten zurücksetzen",
    "action.newUpload": "Neuer Upload",
    "action.saveImport": "Import speichern",
    "action.deleteImport": "Import löschen",
    "action.deleteOldImports": "Importe älter als 30 Tage löschen",
    "action.selectAll": "Alle auswählen",
    "action.clearAll": "Alle abwählen",
    "action.search": "Suchen",
    "action.searchPreview": "Suchen",
    "action.clearSearch": "Suche löschen",
    "action.clear": "Leeren",
    "action.compare": "Vergleichen",
    "action.clearWorkspace": "Vorschau-Workspace leeren",
    "action.clearDatabase": "Datenbankdaten leeren",
    "action.managePrice": "Preis & Filter",
    "action.addSupplier": "Lieferant hinzufügen",
    "action.excludeSelected": "Ausgewählte ausschließen",
    "action.keepOnlySelected": "Nur ausgewählte behalten",
    "action.upload": "Hochladen",
    "action.uploadFeed": "Feed hochladen",
    "action.close": "Schließen",
    "action.logout": "Abmelden",
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
    "field.feedFile": "CSV-, Excel- oder ZIP-Dateien",
    "field.fileCount": "Dateien",
    "field.skippedFiles": "Übersprungene Archiveinträge",
    "field.file": "Datei",
    "field.supplyChannel": "Lieferkategorie",
    "field.leadTime": "Lieferzeit",
    "field.leadTimeMinDays": "Lieferzeit min. (Tage)",
    "field.leadTimeMaxDays": "Lieferzeit max. (Tage)",
    "field.filterBrands": "Marken ausschließen",
    "field.filterKeywords": "Titel-Keywords ausschließen",
    "field.excludeMissingEan": "Fehlende EAN ausschließen",
    "field.excludeNonNew": "Nicht neue / refurbished ausschließen",
    "field.excludeTesters": "Tester-Produkte werden immer übersprungen",
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
    "field.priceUrl": "URL der aktuellen Preisliste",
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
    "field.productList": "Produktliste",
    "field.targetCurrency": "Währung",
    "field.includeHiddenSuppliers": "Ausgeblendete einbeziehen",
    "field.pricesIncludeVat": "Preise enthalten bereits MwSt.",
    "field.defaultVatRate": "Standard-MwSt. %",
    "field.purchaseQuantity": "Menge",
    "field.columns": "Spalten",
    "field.mapped": "Zugeordnet",
    "quality.duplicateEan": "Doppelte EAN",
    "quality.missingEan": "Fehlende EAN",
    "quality.invalidEan": "Ungültige EAN",
    "quality.supplierCode": "Lieferantencode (kein GTIN)",
    "quality.testerRows": "Tester-Produkte (übersprungen)",
    "quality.missingPrice": "Fehlender Preis",
    "quality.suspiciousPrice": "Verdächtiger Preis",
    "quality.unmappedColumns": "Nicht zugeordnete Spalten",
    "quality.weakMappings": "Schwache Zuordnungen",
    "ruleSection.dealFilters": "Deal-Filter",
    "ruleSection.feeModel": "Gebührenmodell",
    "ruleSection.priorityScores": "Prioritäts-Scoring",
    "ruleSection.thresholds": "Bestands- und Kostenschwellen",
    "message.createdQueueItems": "{count} Queue-Einträge erstellt",
    "message.maintenanceHint": "Arbeitsspeicher freigeben oder importierte Katalogdaten entfernen.",
    "message.clearWorkspaceHint": "Entfernt aktive Upload-Vorschauen und gibt deren Speicher frei. Gespeicherte Datenbankdaten bleiben erhalten.",
    "message.clearDatabaseHint": "Entfernt importierte Angebote, Importhistorie, Recherche, Matches, Metriken, Presence-Prüfungen und Deals. Lieferanten-Links, Filter, Regeln und Einstellungen bleiben erhalten.",
    "message.confirmClearWorkspace": "Alle aktiven Upload-Vorschauen leeren? Gespeicherte Datenbankdaten werden nicht geändert.",
    "message.confirmClearDatabase": "Alle importierten Katalog- und Pipeline-Daten leeren? Lieferanten-Setup, Links, Filter, Regeln und Einstellungen bleiben erhalten.",
    "message.workspaceCleared": "Vorschau-Workspace geleert: {drafts} Entwürfe, {rows} Zeilen freigegeben",
    "message.databaseCleared": "Datenbankdaten geleert: {rows} Zeilen entfernt",
    "message.maintenanceResult": "{action}: {rows} Zeilen entfernt, {size} freigegeben",
    "message.noSuppliersYet": "Noch keine Lieferanten. Oben mit optionaler Preis-URL anlegen oder die erste Preisliste unter Upload prüfen und speichern.",
    "message.noRecords": "Keine Einträge",
    "message.productListPlaceholder": "1. Produktname — EAN 4006381333931",
    "message.comparisonComplete": "{count} Produkte verglichen",
    "message.invalidProductLines": "Zeilen ohne gültige EAN: {count}",
    "message.supplierPricingSaved": "MwSt.-Einstellungen gespeichert",
    "message.processedMatches": "{count} Matches verarbeitet",
    "message.keepaRun": "Keepa fertig: {created} vorbereitet, {processed} verarbeitet",
    "message.keepaRunWithSource": "Keepa fertig über {source}: {created} vorbereitet, {processed} verarbeitet",
    "message.keepaNotConfigured": "Echtes Keepa ist aktiv, aber KEEPA_API_KEY ist nicht konfiguriert",
    "message.keepaPermissionRequired": "Live-Keepa ist auf den autorisierten Keepa-Seat beschränkt",
    "message.keepaRateLimited": "Noch keine Keepa-Tokens verfügbar. Tokens übrig: {tokens}. In ca. {wait} Sekunden erneut versuchen.",
    "message.marketSnapshotRun": "Market Snapshot fertig über {source}: {created} vorbereitet, {processed} verarbeitet",
    "message.dealsCreated": "Deal-Kandidaten erstellt: {count}",
    "message.amazonPresenceRun": "Amazon Presence fertig über {source}: {created} vorbereitet, {processed} verarbeitet",
    "message.researchRun": "Recherche fertig: {count} Matches verarbeitet",
    "message.lookupPlanHint": "Diese Kriterien definieren den nächsten Recherchelauf. Anwenden aktualisiert nur den Plan und ruft keine externen APIs auf.",
    "message.lookupSaveHint": "Gespeicherte Filter werden automatisch für diesen Scope angewendet. Die Batchgröße bleibt laufbezogen.",
    "message.lookupFiltersCleared": "Recherchefilter gelöscht",
    "message.lookupFilterResult": "{eligible} geeignet, {batch} im nächsten Lookup-Batch",
    "message.suggestionsShown": "{shown} von {total} angezeigt",
    "message.previewReady": "Vorschau bereit: {count} Zeilen",
    "message.batchPreviewReady": "Vorschau bereit: {files} Dateien, {count} Zeilen",
    "message.importFilterResult": "{after} von {before} Zeilen werden importiert",
    "message.testersSkipped": "Übersprungene Tester-Produkte: {count}",
    "message.applyFiltersToUpdatePreview": "Filtervorschau anwenden, um Zeilen zu aktualisieren",
    "message.filteredPreviewReady": "Gefilterte Vorschau bereit: {count} Zeilen",
    "message.searchPlaceholder": "Alle gefilterten Zeilen nach SKU, EAN, Titel, Marke suchen...",
    "message.searchResults": "{total} gefunden; {shown} angezeigt",
    "message.saved": "Gespeichert",
    "message.priceLinkSaved": "Preislisten-Link gespeichert",
    "message.pricePreviewReady": "Aktuelle Preisliste geladen: {count} Zeilen",
    "message.priceCheckResult": "{supplier}: {status}. Geprüft {checked}",
    "message.savedSupplierFilters": "Die letzten Lieferantenfilter werden automatisch angewendet",
    "message.noSavedSupplierFilters": "Noch keine gespeicherten Lieferantenfilter",
    "message.rulesReset": "Regeln zurückgesetzt",
    "message.savedImport": "{count} Angebote gespeichert",
    "message.supplyChannelHint": "Die Kategorie wird aus Dateiname und Inhalt erkannt. Bitte vor dem Speichern prüfen.",
    "message.confirmSupplyChannels": "Ich bestätige die Lieferkategorie für jede Datei",
    "message.confirmDeleteImport": "Diesen gespeicherten Import aus der Historie löschen?",
    "message.confirmDeleteActiveImport": "Die aktuelle gespeicherte Preisliste löschen? Aktuelle Lieferantenangebote und abgeleitete Pipeline-Daten werden ebenfalls entfernt.",
    "message.confirmDeleteOldImports": "Alle Importe löschen, die älter als 30 Tage sind? Ist der aktuelle Katalog älter, werden auch seine Angebote und Pipeline-Daten entfernt.",
    "message.importsDeleted": "{imports} Importe und {offers} aktuelle Angebote gelöscht",
    "message.savedPriceListsHint": "Importierte Preislisten verwalten, ohne zuerst einen Lieferanten zu öffnen.",
    "message.uploaded": "Hochgeladen",
    "nav.pipeline": "Pipeline",
    "nav.keepa": "Keepa",
    "nav.overview": "Übersicht",
    "nav.research": "Recherche",
    "nav.rules": "Regeln",
    "nav.settings": "Einstellungen",
    "nav.suppliers": "Lieferanten",
    "nav.upload": "Upload",
    "nav.procurement": "Preisvergleich",
    "panel.recentImports": "Letzte Importe",
    "panel.amazonMatches": "Amazon Matches",
    "panel.dealCandidates": "Deal-Kandidaten",
    "panel.pipelineRun": "Pipeline-Lauf",
    "panel.pipelineSettings": "Pipeline-Einstellungen",
    "panel.pipelineIssues": "Pipeline-Probleme",
    "panel.columnMapping": "Spaltenzuordnung",
    "panel.previewRows": "Vorschauzeilen",
    "panel.supplyChannels": "Lieferkategorien",
    "supply.stock": "Auf Lager",
    "supply.incoming": "Im Zulauf",
    "supply.preorder": "Vorbestellung",
    "panel.qualityChecks": "Qualitätsprüfung",
    "panel.fileDiagnostics": "Qualität nach Datei",
    "panel.researchQueue": "Recherche-Queue",
    "panel.researchRules": "Recherche-Regeln",
    "panel.supplierFeed": "Lieferanten-Feed",
    "panel.supplierDetails": "Lieferanten-Details",
    "panel.supplierManagement": "Lieferantenverwaltung",
    "panel.procurementComparison": "Lieferanten-Preisvergleich",
    "procurement.gridHint": "Spalten zum Verschieben ziehen und ihre Ränder zum Ändern der Breite verwenden.",
    "panel.comparisonResults": "Vergleichsergebnisse",
    "panel.vatSettings": "MwSt.-Einstellungen",
    "panel.importHistory": "Importhistorie",
    "panel.savedPriceLists": "Gespeicherte Preislisten",
    "panel.importFilters": "Importfilter",
    "panel.externalLookupPreview": "Recherche-Lookup-Plan",
    "panel.lookupSample": "Lookup-Beispiele",
    "panel.marketSnapshots": "Market Snapshots",
    "panel.keepaMetrics": "Keepa-Metriken",
    "panel.amazonPresence": "Amazon Presence",
    "panel.offerStats": "Angebotsstatistik",
    "panel.recentOffers": "Letzte Angebote",
    "panel.pipelineStatus": "Pipeline-Status",
    "panel.maintenance": "Wartung",
    "panel.priceSource": "Preisquelle",
    "maintenance.workspaceUsage": "Vorschau-Workspace",
    "maintenance.databaseUsage": "Operative Datenbank",
    "panel.nextActions": "Nächste Aktionen",
    "status.done": "Fertig",
    "status.failed": "Fehlgeschlagen",
    "status.idle": "Bereit",
    "status.running": "Läuft",
    "priceStatus.not_configured": "Nicht konfiguriert",
    "priceStatus.never_downloaded": "Noch nie geladen",
    "priceStatus.current": "Aktuell",
    "priceStatus.no_changes": "Keine Änderungen",
    "priceStatus.new_available": "Neue Preisliste verfügbar",
    "priceStatus.verification_required": "Download zur Prüfung nötig",
    "priceStatus.check_failed": "Prüfung fehlgeschlagen",
    "summary.amazonMatches": "Amazon Matches",
    "summary.marketSnapshots": "Market Snapshots",
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
    "summary.requestedProducts": "Angefragt",
    "summary.locatedProducts": "Angebote gefunden",
    "summary.matchedProducts": "Vergleichbar",
    "summary.needsConfiguration": "Einrichtung nötig",
    "summary.unmatchedProducts": "Nicht gefunden",
    "summary.invalidLines": "Ungültige Zeilen",
    "issue.amazonNotFound": "Amazon nicht gefunden",
    "issue.available": "Verfügbar",
    "issue.dealCandidates": "Deal-Kandidaten",
    "issue.keepaPending": "Keepa ausstehend",
    "issue.marketSnapshotPending": "Market Snapshot ausstehend",
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
    "comparison.matched": "Gefunden",
    "comparison.not_found": "Nicht gefunden",
    "comparison.currency_mismatch": "Andere Währung",
    "comparison.missing_cost": "Preis fehlt",
    "comparison.minimum_quantity": "Unter Mindestmenge",
    "comparison.minimumQuantityValue": "mindestens {count}",
    "table.brand": "Marke",
    "table.buyBox": "Buy Box",
    "table.confidence": "Konfidenz",
    "table.currentPrice": "Aktueller Preis",
    "table.detectedAs": "Erkannt als",
    "table.fileColumn": "Dateispalte",
    "table.priority": "Priorität",
    "table.profit": "Gewinn",
    "table.reason": "Grund",
    "table.roi": "ROI",
    "table.sales": "Verkäufe",
    "table.salesRank": "Sales Rank",
    "table.sellerCount": "Verkäufer",
    "table.source": "Quelle",
    "table.keywords": "Keywords",
    "table.stock": "Bestand",
    "table.status": "Status",
    "table.supplier": "Lieferant",
    "table.requestedProduct": "Gesuchtes Produkt",
    "table.bestSupplier": "Lieferant / bestes Angebot",
    "table.sourceCost": "Preis",
    "table.offers": "Angebote",
    "table.winner": "Gewinner",
    "table.file": "Datei",
    "table.rows": "Zeilen",
    "table.valid": "Gültig",
    "table.actions": "Aktionen",
    "table.amazonPresent": "Amazon präsent",
    "table.failed": "Fehler",
    "table.importedAt": "Importiert am",
    "table.priceDate": "Preis importiert",
    "freshness.today": "heute",
    "freshness.oneDayAgo": "vor 1 Tag",
    "freshness.daysAgo": "vor {count} Tagen",
    "table.sku": "SKU",
    "table.cost": "Kosten",
    "table.title": "Titel",
    "table.visibility": "Sichtbarkeit",
    "table.priceSource": "Preisquelle",
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
    "metric.lastChecked": "Zuletzt geprüft",
    "metric.lastDownloaded": "Zuletzt geladen",
    "metric.fileSize": "Dateigröße",
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
    "action.loadLatestPrice": "Завантажити свіжий прайс",
    "action.checkPriceUpdate": "Перевірити оновлення",
    "action.runAmazonPresence": "Перевірити Amazon presence",
    "action.runKeepa": "Запустити Keepa",
    "action.runMarketSnapshot": "Запустити зріз ринку",
    "action.createDeals": "Створити deals",
    "action.runResearch": "Запустити research",
    "action.save": "Зберегти",
    "action.savePriceLink": "Зберегти лінк",
    "action.clearLookupFilters": "Очистити збережені фільтри",
    "action.saveDefaultRules": "Зберегти дефолтні правила",
    "action.saveLookupFilters": "Зберегти фільтри як дефолт",
    "action.saveSupplierRules": "Зберегти правила постачальника",
    "action.resetToDefault": "Скинути до дефолту",
    "action.resetToSystemDefaults": "Скинути до системного дефолту",
    "action.resetColumns": "Скинути колонки",
    "action.newUpload": "Нове завантаження",
    "action.saveImport": "Зберегти імпорт",
    "action.deleteImport": "Видалити імпорт",
    "action.deleteOldImports": "Видалити імпорти старші 30 днів",
    "action.selectAll": "Вибрати всі",
    "action.clearAll": "Зняти всі",
    "action.search": "Шукати",
    "action.searchPreview": "Пошук",
    "action.clearSearch": "Очистити пошук",
    "action.clear": "Очистити",
    "action.compare": "Порівняти",
    "action.clearWorkspace": "Очистити preview workspace",
    "action.clearDatabase": "Очистити дані бази",
    "action.managePrice": "Прайс і фільтри",
    "action.addSupplier": "Додати постачальника",
    "action.excludeSelected": "Виключити вибрані",
    "action.keepOnlySelected": "Залишити тільки вибрані",
    "action.upload": "Завантажити",
    "action.uploadFeed": "Завантажити фід",
    "action.close": "Закрити",
    "action.logout": "Вийти",
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
    "field.feedFile": "CSV, Excel або ZIP файли",
    "field.fileCount": "Файли",
    "field.skippedFiles": "Пропущені файли архіву",
    "field.file": "Файл",
    "field.supplyChannel": "Категорія постачання",
    "field.leadTime": "Термін постачання",
    "field.leadTimeMinDays": "Мін. термін постачання (дні)",
    "field.leadTimeMaxDays": "Макс. термін постачання (дні)",
    "field.filterBrands": "Виключити бренди",
    "field.filterKeywords": "Виключити keywords у назві",
    "field.excludeMissingEan": "Виключити рядки без EAN",
    "field.excludeNonNew": "Виключити не нові / refurbished",
    "field.excludeTesters": "Tester-позиції завжди пропускаються",
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
    "field.priceUrl": "Лінк на свіжий прайс",
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
    "field.productList": "Список товарів",
    "field.targetCurrency": "Валюта",
    "field.includeHiddenSuppliers": "Включити прихованих",
    "field.pricesIncludeVat": "Ціни вже включають ПДВ",
    "field.defaultVatRate": "Ставка ПДВ за замовчуванням, %",
    "field.purchaseQuantity": "Кількість",
    "field.columns": "Колонки",
    "field.mapped": "Розпізнано",
    "quality.duplicateEan": "Дублікати EAN",
    "quality.missingEan": "Без EAN",
    "quality.invalidEan": "Невалідний EAN",
    "quality.supplierCode": "Код постачальника (не GTIN)",
    "quality.testerRows": "Tester-позиції (пропущено)",
    "quality.missingPrice": "Без ціни",
    "quality.suspiciousPrice": "Підозріла ціна",
    "quality.unmappedColumns": "Нерозпізнані колонки",
    "quality.weakMappings": "Слабкі mappings",
    "ruleSection.dealFilters": "Фільтри угод",
    "ruleSection.feeModel": "Модель комісій",
    "ruleSection.priorityScores": "Scoring пріоритету",
    "ruleSection.thresholds": "Пороги stock і cost",
    "message.createdQueueItems": "Створено {count} елементів черги",
    "message.maintenanceHint": "Звільнити памʼять або видалити імпортовані дані каталогів.",
    "message.clearWorkspaceHint": "Видаляє активні upload preview та звільняє їх памʼять. Збережені дані бази не змінюються.",
    "message.clearDatabaseHint": "Видаляє імпортовані offers, історію імпортів, research, matches, metrics, presence checks і deals. Лінки, фільтри постачальників, Rules та Settings зберігаються.",
    "message.confirmClearWorkspace": "Очистити всі активні upload preview? Збережені дані бази не зміняться.",
    "message.confirmClearDatabase": "Очистити всі імпортовані каталоги та pipeline data? Налаштування постачальників, лінки, фільтри, Rules і Settings залишаться.",
    "message.workspaceCleared": "Preview workspace очищено: {drafts} drafts, звільнено {rows} рядків",
    "message.databaseCleared": "Дані бази очищено: видалено {rows} рядків",
    "message.maintenanceResult": "{action}: видалено {rows} рядків, звільнено {size}",
    "message.noSuppliersYet": "Постачальників ще немає. Додай постачальника вище з необовʼязковим URL прайсу або зроби preview і збережи перший прайс у Upload.",
    "message.noRecords": "Немає записів",
    "message.productListPlaceholder": "1. Назва товару — EAN 4006381333931",
    "message.comparisonComplete": "Порівняно товарів: {count}",
    "message.invalidProductLines": "Рядків без валідного EAN: {count}",
    "message.supplierPricingSaved": "Налаштування ПДВ постачальника збережено",
    "message.processedMatches": "Оброблено {count} matches",
    "message.keepaRun": "Keepa завершено: {created} поставлено в чергу, {processed} оброблено",
    "message.keepaRunWithSource": "Keepa завершено через {source}: {created} поставлено в чергу, {processed} оброблено",
    "message.keepaNotConfigured": "Real Keepa увімкнена, але KEEPA_API_KEY не налаштований",
    "message.keepaPermissionRequired": "Live Keepa доступна тільки авторизованому Keepa seat",
    "message.keepaRateLimited": "Keepa tokens ще недоступні. Залишилось токенів: {tokens}. Спробуй ще раз приблизно за {wait} секунд.",
    "message.marketSnapshotRun": "Зріз ринку завершено через {source}: {created} поставлено в чергу, {processed} оброблено",
    "message.dealsCreated": "Створено кандидатів угод: {count}",
    "message.amazonPresenceRun": "Amazon presence завершено через {source}: {created} поставлено в чергу, {processed} оброблено",
    "message.researchRun": "Research завершено: оброблено {count} matches",
    "message.lookupPlanHint": "Ці критерії задають наступний research run. Застосування оновлює тільки план і не викликає зовнішні API.",
    "message.lookupSaveHint": "Збережені фільтри застосовуються автоматично для цього scope. Batch size лишається параметром конкретного запуску.",
    "message.lookupFiltersCleared": "Research filters очищено",
    "message.lookupFilterResult": "{eligible} підходять, {batch} у наступному lookup batch",
    "message.suggestionsShown": "Показано {shown} з {total}",
    "message.previewReady": "Превʼю готове: {count} рядків",
    "message.batchPreviewReady": "Превʼю готове: {files} файлів, {count} рядків",
    "message.importFilterResult": "Буде імпортовано {after} з {before} рядків",
    "message.testersSkipped": "Пропущено tester-позицій: {count}",
    "message.applyFiltersToUpdatePreview": "Застосуй фільтри для оновлення рядків preview",
    "message.filteredPreviewReady": "Відфільтроване превʼю готове: {count} рядків",
    "message.searchPlaceholder": "Пошук по всіх відфільтрованих рядках: SKU, EAN, назва, бренд...",
    "message.searchResults": "Знайдено {total}; показано {shown}",
    "message.saved": "Збережено",
    "message.priceLinkSaved": "Лінк на прайс збережено",
    "message.pricePreviewReady": "Свіжий прайс завантажено: {count} рядків",
    "message.priceCheckResult": "{supplier}: {status}. Перевірено {checked}",
    "message.savedSupplierFilters": "Останні фільтри постачальника застосуються автоматично",
    "message.noSavedSupplierFilters": "Збережених фільтрів постачальника ще немає",
    "message.rulesReset": "Правила скинуто",
    "message.savedImport": "Збережено {count} offers",
    "message.supplyChannelHint": "Категорія визначається з назви та вмісту файла. Перевір її перед збереженням.",
    "message.confirmSupplyChannels": "Підтверджую категорію постачання для кожного файла",
    "message.confirmDeleteImport": "Видалити цей збережений імпорт з історії?",
    "message.confirmDeleteActiveImport": "Видалити поточний збережений прайс? Поточні offers постачальника та похідні pipeline data також будуть видалені.",
    "message.confirmDeleteOldImports": "Видалити всі імпорти старші 30 днів? Якщо поточний каталог теж застарів, його offers і похідні pipeline data також буде видалено.",
    "message.importsDeleted": "Видалено імпортів: {imports}; поточних offers: {offers}",
    "message.savedPriceListsHint": "Керування імпортованими прайсами без попереднього відкриття постачальника.",
    "message.uploaded": "Завантажено",
    "nav.pipeline": "Pipeline",
    "nav.keepa": "Keepa",
    "nav.overview": "Огляд",
    "nav.research": "Дослідження",
    "nav.rules": "Правила",
    "nav.settings": "Налаштування",
    "nav.suppliers": "Постачальники",
    "nav.upload": "Завантаження",
    "nav.procurement": "Порівняння цін",
    "panel.recentImports": "Останні імпорти",
    "panel.amazonMatches": "Amazon збіги",
    "panel.dealCandidates": "Кандидати угод",
    "panel.pipelineRun": "Запуск pipeline",
    "panel.pipelineSettings": "Налаштування pipeline",
    "panel.pipelineIssues": "Проблеми pipeline",
    "panel.columnMapping": "Зіставлення колонок",
    "panel.previewRows": "Рядки превʼю",
    "panel.supplyChannels": "Категорії постачання",
    "supply.stock": "В наявності",
    "supply.incoming": "Очікується",
    "supply.preorder": "Передзамовлення",
    "panel.qualityChecks": "Перевірка якості",
    "panel.fileDiagnostics": "Якість по файлах",
    "panel.researchQueue": "Черга дослідження",
    "panel.researchRules": "Правила дослідження",
    "panel.supplierFeed": "Фід постачальника",
    "panel.supplierDetails": "Деталі постачальника",
    "panel.supplierManagement": "Керування постачальниками",
    "panel.procurementComparison": "Порівняння цін постачальників",
    "procurement.gridHint": "Перетягуйте колонки для зміни порядку, а їхні межі — для зміни ширини.",
    "panel.comparisonResults": "Результати порівняння",
    "panel.vatSettings": "Налаштування ПДВ",
    "panel.importHistory": "Історія імпортів",
    "panel.savedPriceLists": "Збережені прайси",
    "panel.importFilters": "Фільтри імпорту",
    "panel.externalLookupPreview": "План research lookup",
    "panel.lookupSample": "Приклад lookup",
    "panel.marketSnapshots": "Зріз ринку",
    "panel.keepaMetrics": "Keepa метрики",
    "panel.amazonPresence": "Amazon presence",
    "panel.offerStats": "Статистика offers",
    "panel.recentOffers": "Останні offers",
    "panel.pipelineStatus": "Pipeline статус",
    "panel.maintenance": "Обслуговування",
    "panel.priceSource": "Джерело прайсу",
    "maintenance.workspaceUsage": "Preview workspace",
    "maintenance.databaseUsage": "Операційна база",
    "panel.nextActions": "Наступні дії",
    "status.done": "Готово",
    "status.failed": "Помилка",
    "status.idle": "Очікує",
    "status.running": "Виконується",
    "priceStatus.not_configured": "Не налаштовано",
    "priceStatus.never_downloaded": "Ще не завантажувався",
    "priceStatus.current": "Актуальний",
    "priceStatus.no_changes": "Без змін",
    "priceStatus.new_available": "Доступний новий прайс",
    "priceStatus.verification_required": "Для перевірки треба завантажити",
    "priceStatus.check_failed": "Помилка перевірки",
    "summary.amazonMatches": "Amazon збіги",
    "summary.marketSnapshots": "Зріз ринку",
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
    "summary.requestedProducts": "У запиті",
    "summary.locatedProducts": "Офери знайдено",
    "summary.matchedProducts": "Готові до порівняння",
    "summary.needsConfiguration": "Потрібне налаштування",
    "summary.unmatchedProducts": "Не знайдено",
    "summary.invalidLines": "Невалідні рядки",
    "issue.amazonNotFound": "Amazon не знайдено",
    "issue.available": "Доступно",
    "issue.dealCandidates": "Кандидати угод",
    "issue.keepaPending": "Keepa очікує",
    "issue.marketSnapshotPending": "Зріз ринку очікує",
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
    "comparison.matched": "Знайдено",
    "comparison.not_found": "Не знайдено",
    "comparison.currency_mismatch": "Інша валюта",
    "comparison.missing_cost": "Немає ціни",
    "comparison.minimum_quantity": "Менше мінімальної кількості",
    "comparison.minimumQuantityValue": "мінімум {count}",
    "table.brand": "Бренд",
    "table.buyBox": "Buy Box",
    "table.confidence": "Впевненість",
    "table.currentPrice": "Поточна ціна",
    "table.detectedAs": "Розпізнано як",
    "table.fileColumn": "Колонка файлу",
    "table.priority": "Пріоритет",
    "table.profit": "Прибуток",
    "table.reason": "Причина",
    "table.roi": "ROI",
    "table.sales": "Продажі",
    "table.salesRank": "Sales rank",
    "table.sellerCount": "Продавці",
    "table.source": "Джерело",
    "table.keywords": "Keywords",
    "table.stock": "Stock",
    "table.status": "Статус",
    "table.supplier": "Постачальник",
    "table.requestedProduct": "Запитаний товар",
    "table.bestSupplier": "Постачальник / кращий офер",
    "table.sourceCost": "Ціна",
    "table.offers": "Пропозиції",
    "table.winner": "Переможець",
    "table.file": "Файл",
    "table.rows": "Рядки",
    "table.valid": "Валідні",
    "table.actions": "Дії",
    "table.amazonPresent": "Amazon присутній",
    "table.failed": "Помилки",
    "table.importedAt": "Імпортовано",
    "table.priceDate": "Прайс імпортовано",
    "freshness.today": "сьогодні",
    "freshness.oneDayAgo": "1 день тому",
    "freshness.daysAgo": "{count} днів тому",
    "table.sku": "SKU",
    "table.cost": "Ціна",
    "table.title": "Назва",
    "table.visibility": "Видимість",
    "table.priceSource": "Джерело прайсу",
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
    "metric.lastChecked": "Остання перевірка",
    "metric.lastDownloaded": "Останнє завантаження",
    "metric.fileSize": "Розмір файлу",
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
  const realKeepaAllowed = canUseRealKeepa();
  const notConfigured = Boolean(
    useRealKeepa
    && state.keepaStatus
    && !state.keepaStatus.api_key_configured,
  );
  const blockedByPermission = useRealKeepa && !realKeepaAllowed;

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
    toggle.disabled = !realKeepaAllowed;
    toggle.title = realKeepaAllowed ? "" : t("message.keepaPermissionRequired");
  }

  if (runButton) {
    runButton.disabled = notConfigured || blockedByPermission;
    runButton.title = blockedByPermission
      ? t("message.keepaPermissionRequired")
      : (notConfigured ? t("message.keepaNotConfigured") : "");
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

  document.querySelectorAll("[data-i18n-placeholder]").forEach((element) => {
    element.placeholder = t(element.dataset.i18nPlaceholder);
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
  renderProcurementComparison(state.procurementComparison);

  if (state.importPreview) {
    renderImportPreview(state.importPreview);
  }

  renderSupplierSelect();
  renderRuleHelpButtons();
  renderResearchRulesActions();
  renderSettingsPermissions();
  renderKeepaModeBadge();
  renderAuthUser();
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
  let data = null;
  if (text) {
    try {
      data = JSON.parse(text);
    } catch (_error) {
      data = { detail: text };
    }
  }

  if (!response.ok) {
    if (response.status === 401) {
      window.location.href = "/auth/login";
      return null;
    }
    const detail = data?.detail;
    const message = detail
      ? `Request failed with ${response.status}: ${
        typeof detail === "string" ? detail : JSON.stringify(detail)
      }`
      : `Request failed with ${response.status}`;
    throw new Error(message);
  }

  return data;
}

function hasPermission(permission) {
  return Boolean(state.authUser?.permissions?.includes(permission));
}

function canUseRealKeepa() {
  return hasPermission("automation:use_keepa_real")
    || hasPermission("automation:admin");
}

function renderAuthUser() {
  const container = document.querySelector("#auth-user");
  const label = document.querySelector("#auth-user-label");
  const logoutButton = document.querySelector("#auth-logout-button");

  if (!container || !label || !logoutButton) return;

  if (!state.authUser) {
    container.classList.add("hidden");
    return;
  }

  label.textContent = state.authUser.email || state.authUser.name || "User";
  logoutButton.textContent = t("action.logout");
  container.classList.remove("hidden");

  document.querySelectorAll("[data-view=\"rules\"], [data-view=\"settings\"]").forEach((element) => {
    element.classList.toggle("hidden", !hasPermission("automation:configure"));
  });
  document.querySelectorAll("#clear-database-button").forEach((element) => {
    element.classList.toggle("hidden", !hasPermission("automation:admin"));
  });
}

function renderSettingsPermissions() {
  const realKeepaInput = document.querySelector(
    "#pipeline-settings-form input[name='use_real_keepa']",
  );

  if (!realKeepaInput) return;

  const allowed = canUseRealKeepa();
  realKeepaInput.disabled = !allowed;
  realKeepaInput.title = allowed ? "" : t("message.keepaPermissionRequired");
}

async function loadAuthUser() {
  state.authUser = await api("/auth/me");
  renderAuthUser();
  renderSettingsPermissions();
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
    ["suppliers", "procurement"].includes(state.activeView),
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
    loadMarketSnapshots(),
    loadAmazonPresence(),
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

function priceUpdateLabel(status) {
  return t(`priceStatus.${status || "not_configured"}`);
}

function keepaSourceLabel(source) {
  if (source === "keepa_mock") return t("keepa.sourceMock");
  if (source === "keepa_real") return t("keepa.sourceReal");
  if (source === "presence_mock") return t("keepa.sourceMock");
  if (source === "market_snapshot_mock") return t("keepa.sourceMock");

  return t("keepa.sourceUnknown");
}

function keepaRateLimitMessage(result) {
  const tokenStatus = result?.token_status || {};
  const tokens = tokenStatus.tokens_left ?? 0;
  const wait = Math.ceil(tokenStatus.time_to_refill_seconds || 0);

  return t("message.keepaRateLimited", { tokens, wait });
}

function renderSummary() {
  const grid = document.querySelector("#summary-grid");
  const summary = state.summary || {};

  const items = [
    ["summary.researchQueue", summary.research_queue],
    ["summary.amazonMatches", summary.amazon_matches],
    ["summary.marketSnapshots", summary.market_snapshots],
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

function renderSavedImports() {
  const body = document.querySelector("#saved-imports-table");
  if (!body) return;

  body.innerHTML = state.savedImports.length
    ? state.savedImports.map((run) => `
      <tr>
        <td>${escapeHtml(run.supplier_name)}</td>
        <td>${escapeHtml(run.filename)}</td>
        <td>${formatNumber(run.rows_total)}</td>
        <td>${formatNumber(run.rows_valid)}</td>
        <td>
          <span class="badge ${statusClass(run.status)}">${escapeHtml(run.status)}</span>
          ${run.is_active ? `<span class="badge ok">${t("priceStatus.current")}</span>` : ""}
        </td>
        <td>${formatDate(run.created_at)}</td>
        <td>
          <button
            class="ghost-button danger-button compact-button"
            data-delete-supplier-import="${run.id}"
            data-supplier-id="${run.supplier_id}"
            data-active-import="${run.is_active ? "true" : "false"}"
            type="button"
          >${t("action.deleteImport")}</button>
        </td>
      </tr>
    `).join("")
    : `<tr><td colspan="7">${t("message.noRecords")}</td></tr>`;
}

async function loadSavedImports() {
  state.savedImports = await api("/suppliers/imports/history");
  renderSavedImports();
}

function renderSuppliersDashboard() {
  const grid = document.querySelector("#suppliers-dashboard");

  if (!grid) return;

  if (!state.supplierDashboard.length) {
    grid.innerHTML = `
      <section class="panel supplier-empty-state">
        <h3>${t("panel.priceSource")}</h3>
        <p>${t("message.noSuppliersYet")}</p>
        <button class="primary-button" data-focus-supplier-create type="button">${t("action.addSupplier")}</button>
      </section>
    `;
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
              <p>
                ${formatNumber(supplier.offers_count)} offers ·
                <span class="badge ${priceUpdateClass(supplier.price_update_status)}">
                  ${priceUpdateLabel(supplier.price_update_status)}
                </span>
              </p>
            </div>
            <div class="button-row">
              <button
                class="ghost-button"
                data-check-supplier-price="${supplier.id}"
                type="button"
                ${supplier.price_url ? "" : "disabled"}
              >
                ${t("action.checkPriceUpdate")}
              </button>
              <button
                class="${priceDownloadButtonClass(supplier.price_update_status)}"
                data-download-supplier-price="${supplier.id}"
                type="button"
                ${supplier.price_url ? "" : "disabled"}
              >
                ${t("action.loadLatestPrice")}
              </button>
              <button class="ghost-button" data-open-supplier-details="${supplier.id}" type="button">
                ${t("action.managePrice")}
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
              <span>${t("summary.marketSnapshots")}</span>
              <strong>${statusText(supplier.statuses?.market_snapshots)}</strong>
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
    {
      key: "price_url",
      label: t("table.priceSource"),
      export: (supplier) => [
        supplier.price_url || "",
        supplier.has_saved_import_filters ? "filters saved" : "",
      ].filter(Boolean).join(" | "),
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
            <div class="supplier-source-status">
              <span class="badge ${supplier.price_url ? "ok" : "warn"}">
                URL: ${supplier.price_url ? t("message.saved") : t("message.noRecords")}
              </span>
              <span class="badge ${supplier.has_saved_import_filters ? "ok" : "warn"}">
                ${t("panel.importFilters")}: ${supplier.has_saved_import_filters ? t("message.saved") : t("message.noRecords")}
              </span>
              <span class="badge ${priceUpdateClass(supplier.price_update_status)}">
                ${priceUpdateLabel(supplier.price_update_status)}
              </span>
            </div>
            <small class="supplier-source-meta">
              ${supplier.price_last_checked_at
                ? `${t("metric.lastChecked")}: ${formatDate(supplier.price_last_checked_at)}`
                : ""}
            </small>
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
                ${t("action.managePrice")}
              </button>
              <button
                class="ghost-button"
                data-check-supplier-price="${supplier.id}"
                type="button"
                ${supplier.price_url ? "" : "disabled"}
              >
                ${t("action.checkPriceUpdate")}
              </button>
              <button
                class="${priceDownloadButtonClass(supplier.price_update_status)}"
                data-download-supplier-price="${supplier.id}"
                type="button"
                ${supplier.price_url ? "" : "disabled"}
              >
                ${t("action.loadLatestPrice")}
              </button>
            </div>
          </td>
        </tr>
      `)
      .join("")
    : `
      <tr>
        <td colspan="5">
          <div class="supplier-table-empty">
            <span>${t("message.noSuppliersYet")}</span>
            <button class="primary-button" data-focus-supplier-create type="button">${t("action.addSupplier")}</button>
          </div>
        </td>
      </tr>
    `;
}

function renderMaintenanceStatus() {
  const workspace = state.maintenance?.workspace || {};
  const database = state.maintenance?.database || {};
  const workspaceBytes = Number(workspace.estimated_bytes || 0);
  const databaseBytes = Number(database.estimated_bytes || 0);
  const largest = Math.max(workspaceBytes, databaseBytes, 1);

  document.querySelector("#maintenance-workspace-size").textContent = formatBytes(workspaceBytes);
  document.querySelector("#maintenance-database-size").textContent = formatBytes(databaseBytes);
  document.querySelector("#maintenance-workspace-details").textContent = (
    `${formatNumber(workspace.drafts || 0)} drafts · ${formatNumber(workspace.rows || 0)} rows`
  );
  document.querySelector("#maintenance-database-details").textContent = (
    `${formatNumber(database.rows || 0)} rows`
  );
  document.querySelector("#maintenance-workspace-meter").style.width = (
    `${workspaceBytes ? Math.max(3, (workspaceBytes / largest) * 100) : 0}%`
  );
  document.querySelector("#maintenance-database-meter").style.width = (
    `${databaseBytes ? Math.max(3, (databaseBytes / largest) * 100) : 0}%`
  );
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

    <section class="supplier-price-source">
      <div class="section-title-row">
        <div>
          <h4>${t("panel.priceSource")}</h4>
          <p class="muted-note">
            ${detail.has_saved_import_filters
              ? t("message.savedSupplierFilters")
              : t("message.noSavedSupplierFilters")}
          </p>
        </div>
        <span class="badge ${detail.has_saved_import_filters ? "ok" : "warn"}">
          ${detail.has_saved_import_filters ? t("message.saved") : t("message.noRecords")}
        </span>
      </div>
      <div class="supplier-price-source-form">
        <label>
          <span>${t("field.priceUrl")}</span>
          <input
            data-supplier-price-url
            type="url"
            value="${escapeHtml(detail.price_url || "")}"
            placeholder="https://supplier.example/catalog.csv"
          >
        </label>
        <button class="ghost-button" data-save-supplier-price-url="${detail.id}" type="button">
          ${t("action.savePriceLink")}
        </button>
        <button
          class="${priceDownloadButtonClass(detail.price_update_status)}"
          data-load-supplier-price="${detail.id}"
          type="button"
        >
          ${t("action.loadLatestPrice")}
        </button>
      </div>
      <div class="supplier-price-tracking">
        <span class="badge ${priceUpdateClass(detail.price_update_status)}">
          ${priceUpdateLabel(detail.price_update_status)}
        </span>
        <span>${t("metric.lastChecked")}: ${formatDate(detail.price_last_checked_at)}</span>
        <span>${t("metric.lastDownloaded")}: ${formatDate(detail.price_last_downloaded_at)}</span>
        <span>${t("field.file")}: ${escapeHtml(detail.price_last_filename || "-")}</span>
        <span>${t("metric.fileSize")}: ${formatBytes(detail.price_content_length || 0)}</span>
        <button class="ghost-button" data-check-supplier-price="${detail.id}" type="button">
          ${t("action.checkPriceUpdate")}
        </button>
      </div>
    </section>

    <section class="supplier-vat-settings">
      <div class="section-title-row">
        <h4>${t("panel.vatSettings")}</h4>
        <button class="ghost-button" data-save-supplier-pricing="${detail.id}" type="button">
          ${t("action.save")}
        </button>
      </div>
      <div class="supplier-vat-form">
        <label class="inline-toggle">
          <span>${t("field.pricesIncludeVat")}</span>
          <input
            data-supplier-prices-include-vat
            type="checkbox"
            ${detail.prices_include_vat ? "checked" : ""}
          >
        </label>
        <label>
          <span>${t("field.defaultVatRate")}</span>
          <input
            data-supplier-default-vat-rate
            type="number"
            min="0"
            max="100"
            step="0.01"
            value="${detail.default_vat_rate ?? ""}"
          >
        </label>
      </div>
    </section>

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
            <span>${t("summary.marketSnapshots")}</span>
            <strong>${statusText(detail.statuses?.market_snapshots)}</strong>
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
        <div class="button-row">
          <button class="ghost-button danger-button compact-button" data-delete-old-supplier-imports="${detail.id}" type="button">
            ${t("action.deleteOldImports")}
          </button>
          <button class="ghost-button compact-button" data-export-table="#supplier-import-history-table" type="button">CSV</button>
        </div>
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
              <th>${t("table.actions")}</th>
            </tr>
          </thead>
          <tbody id="supplier-import-history-table">
            ${imports.length
              ? imports.map((run) => `
                <tr>
                  <td>${escapeHtml((run.files || [run.filename]).join(", "))}</td>
                  <td>${formatNumber(run.rows_total)}</td>
                  <td>${formatNumber(run.rows_valid)}</td>
                  <td>${formatNumber(run.rows_failed)}</td>
                  <td>${importMappingSummary(run)}</td>
                  <td><span class="badge ${statusClass(run.status)}">${escapeHtml(run.status)}</span></td>
                  <td>${formatDate(run.created_at)}</td>
                  <td>
                    <button
                      class="ghost-button danger-button compact-button"
                      data-delete-supplier-import="${run.id}"
                      data-supplier-id="${detail.id}"
                      data-active-import="${run.is_active ? "true" : "false"}"
                      type="button"
                    >${t("action.deleteImport")}</button>
                  </td>
                </tr>
              `).join("")
              : `<tr><td colspan="8">${t("message.noRecords")}</td></tr>`}
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
              <th>${t("table.file")}</th>
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
                  <td>${escapeHtml(offer.source_file) || "-"}</td>
                  <td>${formatDate(offer.imported_at)}</td>
                </tr>
              `).join("")
              : `<tr><td colspan="8">${t("message.noRecords")}</td></tr>`}
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
      {
        key: "filename",
        label: t("table.file"),
        export: (run) => (run.files || [run.filename]).join(", "),
      },
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
      { key: "source_file", label: t("table.file") },
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
    ["quality.invalidEan", report.invalid_ean_count || 0],
    ["quality.supplierCode", report.supplier_code_count || 0],
    ["quality.testerRows", report.tester_count || 0],
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
    invalid_ean: "quality.invalidEan",
    supplier_code: "quality.supplierCode",
    tester: "quality.testerRows",
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
    marketSnapshotPending: {
      label: "issue.marketSnapshotPending",
      count: statusCount("market_snapshots", "pending")
        + statusCount("research_queue", "market_snapshot_pending"),
      tone: "warn",
      endpoint: scopedPath("/market-snapshots/?snapshot_status=pending&limit=500"),
      columns: [
        { label: t("table.supplier"), key: "supplier_name", render: (row) => escapeHtml(row.supplier_name) || "-" },
        { label: "ASIN", key: "asin" },
        { label: t("table.status"), key: "snapshot_status", render: (row) => `<span class="badge ${statusClass(row.snapshot_status)}">${escapeHtml(row.snapshot_status)}</span>` },
        { label: t("table.source"), key: "snapshot_source", render: (row) => keepaSourceLabel(row.snapshot_source) },
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

function registerTableExport(selector, title, rows, columns, options = {}) {
  state.tableExports[selector] = {
    title,
    filename: options.filename || null,
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

function csvCellValue(row, column) {
  const value = plainCellValue(row, column);
  const identifierColumns = new Set(["ean", "gtin", "upc", "barcode"]);
  const columnName = String(column.key || column.label || "").trim().toLowerCase();

  if (identifierColumns.has(columnName) && /^\d{8,14}$/.test(value)) {
    return `="${value}"`;
  }

  return value;
}

function downloadTableCsv(selector) {
  const tableExport = state.tableExports[selector];

  if (!tableExport) {
    showAlert(t("message.noRecords"), true);
    return;
  }

  const { title, filename, rows, columns } = tableExport;

  if (!rows.length) {
    showAlert(t("message.noRecords"), true);
    return;
  }

  const header = columns
    .map((column) => csvEscape(column.label || column.key))
    .join(",");
  const body = rows
    .map((row) => columns
      .map((column) => csvEscape(csvCellValue(row, column)))
      .join(","))
    .join("\n");

  downloadBlob(
    filename || `${filenameSafe(selectedSupplierName())}-${filenameSafe(title)}.csv`,
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

function localDateStamp(value = new Date()) {
  const year = value.getFullYear();
  const month = String(value.getMonth() + 1).padStart(2, "0");
  const day = String(value.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
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

function comparisonStatusLabel(status) {
  return t(`comparison.${status || "not_found"}`);
}

function comparisonStatusClass(status) {
  if (status === "matched") return "ok";
  if (status === "not_found") return "bad";
  return "warn";
}

function comparisonMoney(value, currency) {
  if (value === null || value === undefined) return "-";
  return `${formatNumber(value)} ${escapeHtml(currency || "")}`.trim();
}

function comparisonTierLabel(offer) {
  if (!offer || !offer.tier_min_quantity) return "";
  return `≥ ${formatNumber(offer.tier_min_quantity)}`;
}

function importAgeDays(value) {
  if (!value) return null;
  const timestamp = new Date(value).getTime();
  if (!Number.isFinite(timestamp)) return null;
  return Math.max(0, Math.floor((Date.now() - timestamp) / 86400000));
}

function comparisonImportDate(offer) {
  if (!offer?.imported_at) return "-";
  const days = importAgeDays(offer.imported_at);
  let age = "";
  if (days === 0) age = t("freshness.today");
  else if (days === 1) age = t("freshness.oneDayAgo");
  else if (days !== null) age = t("freshness.daysAgo", { count: days });

  return `
    <span class="procurement-date">
      ${escapeHtml(formatDate(offer.imported_at))}
      ${age ? `<small>${escapeHtml(age)}</small>` : ""}
    </span>
  `;
}

function procurementOfferMarkup(offer, winnerId) {
  let unavailable = offer.unavailable_reason
    ? comparisonStatusLabel(offer.unavailable_reason)
    : "";
  if (offer.unavailable_reason === "minimum_quantity" && offer.minimum_quantity) {
    unavailable += `: ${t("comparison.minimumQuantityValue", {
      count: formatNumber(offer.minimum_quantity),
    })}`;
  }

  return `
    <div class="procurement-offer ${offer.offer_id === winnerId ? "winner" : ""}">
      <strong>${escapeHtml(offer.supplier) || "-"}</strong>
      <span>${comparisonMoney(offer.source_cost, offer.currency)} <small>${comparisonTierLabel(offer)}</small></span>
      <span>${formatNumber(offer.stock)}</span>
      <span>${escapeHtml(offer.source_file) || "-"}</span>
      ${comparisonImportDate(offer)}
      <span>${unavailable ? escapeHtml(unavailable) : `+${formatNumber(offer.difference_to_best || 0)}`}</span>
    </div>
  `;
}

function procurementOffersSummary(offers) {
  const prices = offers
    .map((offer) => Number(offer.source_cost))
    .filter(Number.isFinite);
  const currencies = [...new Set(
    offers.map((offer) => offer.currency).filter(Boolean),
  )];
  let priceSummary = "";

  if (prices.length) {
    const minimum = Math.min(...prices);
    const maximum = Math.max(...prices);
    const range = minimum === maximum
      ? formatNumber(minimum)
      : `${formatNumber(minimum)}–${formatNumber(maximum)}`;
    priceSummary = ` · ${range} ${escapeHtml(currencies.length === 1 ? currencies[0] : "")}`;
  }

  return `${formatNumber(offers.length)} ${t("table.offers")}${priceSummary}`;
}

function procurementGridRows(data) {
  return (data.results || []).flatMap((result) => {
    const productName = result.title
      || result.winner?.title
      || result.offers?.[0]?.title
      || result.input;
    const offers = result.offers || [];

    if (!offers.length) {
      return [{
        id: `line-${result.line}`,
        product_name: productName,
        ean: result.ean,
        supplier: null,
        source_cost: null,
        currency: data.target_currency,
        stock: null,
        supply_channel: null,
        lead_time_min_days: null,
        lead_time_max_days: null,
        source_file: null,
        imported_at: null,
        status: result.status,
        is_winner: false,
      }];
    }

    return offers.map((offer, index) => ({
      id: `${result.line}-${offer.offer_id || index}`,
      product_name: productName,
      ean: result.ean,
      supplier: offer.supplier,
      source_cost: offer.source_cost,
      currency: offer.currency,
      stock: offer.stock,
      supply_channel: offer.supply_channel,
      lead_time_min_days: offer.lead_time_min_days,
      lead_time_max_days: offer.lead_time_max_days,
      source_file: offer.source_file,
      imported_at: offer.imported_at,
      status: offer.unavailable_reason || result.status,
      is_winner: offer.offer_id === result.winner?.offer_id,
      tier_min_quantity: offer.tier_min_quantity,
    }));
  });
}

function procurementMoneyFormatter(cell, showTier = false) {
  const row = cell.getRow().getData();
  const money = comparisonMoney(cell.getValue(), row.currency);
  const tier = showTier ? comparisonTierLabel(row) : "";
  return `<span class="procurement-grid-money">${money}${tier ? ` <small>${tier}</small>` : ""}</span>`;
}

function procurementGridColumns() {
  return [
    {
      title: t("table.requestedProduct"),
      field: "product_name",
      width: 300,
      minWidth: 220,
      frozen: true,
      variableHeight: true,
      formatter: (cell) => {
        const value = String(cell.getValue() || "-");
        return `<div class="procurement-grid-product" title="${escapeHtml(value)}">${escapeHtml(value)}</div>`;
      },
    },
    {
      title: "EAN",
      field: "ean",
      width: 145,
      minWidth: 125,
      frozen: true,
    },
    {
      title: t("table.supplier"),
      field: "supplier",
      width: 160,
      minWidth: 120,
      formatter: (cell) => {
        const row = cell.getRow().getData();
        const supplier = escapeHtml(cell.getValue()) || "-";
        return row.is_winner
          ? `<div class="procurement-grid-supplier"><strong>${supplier}</strong><span class="badge ok">${t("table.winner")}</span></div>`
          : supplier;
      },
    },
    {
      title: t("table.sourceCost"),
      field: "source_cost",
      sorter: "number",
      hozAlign: "right",
      headerHozAlign: "right",
      width: 130,
      minWidth: 110,
      formatter: (cell) => procurementMoneyFormatter(cell, true),
    },
    {
      title: t("table.stock"),
      field: "stock",
      sorter: "number",
      hozAlign: "right",
      headerHozAlign: "right",
      width: 86,
      minWidth: 72,
      formatter: (cell) => formatNumber(cell.getValue()),
    },
    {
      title: t("field.supplyChannel"),
      field: "supply_channel",
      width: 145,
      minWidth: 120,
      formatter: (cell) => {
        const value = cell.getValue();
        return value ? t(`supply.${value}`) : "-";
      },
    },
    {
      title: t("field.leadTime"),
      field: "lead_time_max_days",
      sorter: "number",
      width: 115,
      minWidth: 95,
      formatter: (cell) => supplyLeadTime(cell.getRow().getData()),
    },
    {
      title: t("table.priceDate"),
      field: "imported_at",
      sorter: "datetime",
      width: 170,
      minWidth: 145,
      formatter: (cell) => comparisonImportDate(cell.getRow().getData()),
    },
    {
      title: t("table.file"),
      field: "source_file",
      width: 210,
      minWidth: 140,
      formatter: (cell) => {
        const value = String(cell.getValue() || "-");
        return `<div class="procurement-grid-file" title="${escapeHtml(value)}">${escapeHtml(value)}</div>`;
      },
    },
    {
      title: t("table.status"),
      field: "status",
      width: 170,
      minWidth: 145,
      formatter: (cell) => `<span class="badge ${comparisonStatusClass(cell.getValue())}">${escapeHtml(comparisonStatusLabel(cell.getValue()))}</span>`,
    },
  ];
}

function renderProcurementGrid(data) {
  const element = document.querySelector("#procurement-results-table");
  if (!element) return;
  if (typeof Tabulator === "undefined") {
    element.innerHTML = `<div class="procurement-grid-error">Tabulator failed to load.</div>`;
    return;
  }

  if (state.procurementGrid && state.procurementGridLanguage !== state.language) {
    state.procurementGrid.destroy();
    state.procurementGrid = null;
    element.innerHTML = "";
  }

  const rows = procurementGridRows(data);
  if (!state.procurementGrid) {
    state.procurementGridLanguage = state.language;
    state.procurementGrid = new Tabulator(element, {
      data: rows,
      index: "id",
      height: "100%",
      layout: "fitDataStretch",
      movableColumns: true,
      resizableRows: true,
      resizableColumnGuide: true,
      placeholder: t("message.noRecords"),
      persistence: { columns: true, sort: true },
      persistenceMode: "local",
      persistenceID: "mirenelle-procurement-grid-v2",
      columnDefaults: {
        resizable: true,
        headerSort: true,
        headerWordWrap: true,
        vertAlign: "middle",
      },
      columns: procurementGridColumns(),
    });
  } else {
    state.procurementGrid.replaceData(rows);
  }
}

function resetProcurementGrid() {
  Object.keys(localStorage)
    .filter((key) => key.includes("mirenelle-procurement-grid-v2"))
    .forEach((key) => localStorage.removeItem(key));

  if (state.procurementGrid) {
    state.procurementGrid.destroy();
    state.procurementGrid = null;
    document.querySelector("#procurement-results-table").innerHTML = "";
  }
  if (state.procurementComparison) {
    renderProcurementGrid(state.procurementComparison);
  }
}

function procurementExportRows(data) {
  return (data.results || []).flatMap((result) => {
    const productName = result.title
      || result.winner?.title
      || result.offers?.[0]?.title
      || result.input;
    if (!result.offers.length) {
      return [{
        requested_product: productName,
        ean: result.ean,
        status: comparisonStatusLabel(result.status),
      }];
    }

    return result.offers.map((offer) => ({
      requested_product: productName,
      ean: result.ean,
      status: comparisonStatusLabel(result.status),
      best: offer.offer_id === result.winner?.offer_id ? "yes" : "",
      supplier: offer.supplier,
      supplier_sku: offer.supplier_sku,
      source_file: offer.source_file,
      source_cost: offer.source_cost,
      imported_at: offer.imported_at,
      age_days: importAgeDays(offer.imported_at),
      purchase_quantity: offer.purchase_quantity,
      tier_min_quantity: offer.tier_min_quantity,
      price_tier_source: offer.price_tier_source,
      available_tiers: offer.available_tiers,
      currency: offer.currency,
      stock: offer.stock,
      supply_channel: offer.supply_channel,
      lead_time_min_days: offer.lead_time_min_days,
      lead_time_max_days: offer.lead_time_max_days,
      difference_to_best: offer.difference_to_best,
      unavailable_reason: offer.unavailable_reason,
    }));
  });
}

function renderProcurementComparison(data) {
  const panel = document.querySelector("#procurement-results-panel");
  const grid = document.querySelector("#procurement-results-table");
  const summary = document.querySelector("#procurement-summary");
  const invalid = document.querySelector("#procurement-invalid-lines");

  if (!panel || !grid || !summary || !invalid) return;
  if (!data) {
    panel.classList.add("hidden");
    registerTableExport("#procurement-results-table", t("panel.comparisonResults"), [], []);
    return;
  }

  panel.classList.remove("hidden");
  summary.innerHTML = [
    ["summary.requestedProducts", data.requested],
    ["summary.locatedProducts", data.offers_found ?? data.located ?? data.matched],
    ["summary.matchedProducts", data.matched],
    ["summary.needsConfiguration", data.needs_configuration ?? 0],
    ["summary.unmatchedProducts", data.not_found ?? data.unmatched],
    ["summary.invalidLines", data.invalid_lines?.length || 0],
  ].map(([label, value]) => `
    <article><span>${t(label)}</span><strong>${formatNumber(value)}</strong></article>
  `).join("");

  renderProcurementGrid(data);

  const invalidLines = data.invalid_lines || [];
  invalid.classList.toggle("hidden", !invalidLines.length);
  invalid.innerHTML = invalidLines.length
    ? `<strong>${t("message.invalidProductLines", { count: invalidLines.length })}</strong>
       <span>${invalidLines.map((item) => `${item.line}: ${escapeHtml(item.text)}`).join(" · ")}</span>`
    : "";

  registerTableExport(
    "#procurement-results-table",
    t("panel.comparisonResults"),
    procurementExportRows(data),
    [
      { key: "requested_product", label: t("table.requestedProduct") },
      { key: "ean", label: "EAN" },
      { key: "status", label: t("table.status") },
      { key: "best", label: t("table.winner") },
      { key: "supplier", label: t("table.supplier") },
      { key: "supplier_sku", label: t("table.sku") },
      { key: "source_file", label: t("table.file") },
      { key: "source_cost", label: t("table.sourceCost") },
      { key: "imported_at", label: t("table.priceDate") },
      { key: "age_days", label: "Age (days)" },
      { key: "purchase_quantity", label: t("field.purchaseQuantity") },
      { key: "tier_min_quantity", label: "Tier min qty" },
      { key: "price_tier_source", label: "Tier source" },
      { key: "available_tiers", label: "Tiers" },
      { key: "currency", label: t("field.targetCurrency") },
      { key: "stock", label: t("table.stock") },
      { key: "supply_channel", label: t("field.supplyChannel") },
      { key: "lead_time_min_days", label: t("field.leadTimeMinDays") },
      { key: "lead_time_max_days", label: t("field.leadTimeMaxDays") },
      { key: "difference_to_best", label: "Delta" },
      { key: "unavailable_reason", label: t("table.reason") },
    ],
    { filename: `price_compare_${localDateStamp()}.csv` },
  );
}

async function runProcurementComparison(form) {
  const button = form.querySelector("button[type='submit']");
  const products = form.elements.products.value.trim();
  if (!products) return;

  button.disabled = true;
  try {
    state.procurementComparison = await api("/procurement/compare", {
      method: "POST",
      body: JSON.stringify({
        products,
        target_currency: form.elements.target_currency.value,
        purchase_quantity: Number(form.elements.purchase_quantity.value),
        include_hidden_suppliers: form.elements.include_hidden_suppliers.checked,
      }),
    });
    renderProcurementComparison(state.procurementComparison);
    showAlert(t("message.comparisonComplete", {
      count: state.procurementComparison.requested,
    }));
  } catch (error) {
    showAlert(error.message, true);
  } finally {
    button.disabled = false;
  }
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

async function createSupplier(form) {
  const submitButton = form.querySelector("button[type='submit']");
  const payload = formPayload(form);

  submitButton.disabled = true;

  try {
    const supplier = await api("/suppliers/", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    form.reset();
    await Promise.all([
      loadSuppliers(),
      loadSuppliersDashboard(),
    ]);
    await loadSupplierDetail(supplier.id);
    showAlert(t("message.saved"));
  } catch (error) {
    showAlert(error.message, true);
  } finally {
    submitButton.disabled = false;
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

async function refreshAfterSupplierImportDelete(result) {
  const refreshes = [
    loadSuppliers(),
    loadSuppliersDashboard(),
    loadSavedImports(),
  ];
  if (result.current_catalog_deleted || result.current_catalogs_deleted) {
    refreshes.push(
      loadSummary(),
      loadDeals(),
      loadResearch(),
      loadKeepa(),
      loadMarketSnapshots(),
      loadAmazonPresence(),
    );
  }
  await Promise.all(refreshes);
}

async function deleteSupplierImport(button) {
  const supplierId = button.dataset.supplierId;
  const runId = button.dataset.deleteSupplierImport;
  const confirmationKey = button.dataset.activeImport === "true"
    ? "message.confirmDeleteActiveImport"
    : "message.confirmDeleteImport";
  if (!window.confirm(t(confirmationKey))) return;

  button.disabled = true;
  try {
    const result = await api(
      `/suppliers/${supplierId}/imports/${runId}`,
      { method: "DELETE" },
    );
    await refreshAfterSupplierImportDelete(result);
    showAlert(t("message.importsDeleted", {
      imports: result.deleted_imports || 0,
      offers: result.deleted_catalog?.supplier_offers || 0,
    }));
  } catch (error) {
    showAlert(error.message, true);
  } finally {
    button.disabled = false;
  }
}

async function deleteOldSupplierImports(button) {
  const supplierId = button.dataset.deleteOldSupplierImports;
  if (!window.confirm(t("message.confirmDeleteOldImports"))) return;

  button.disabled = true;
  try {
    const result = await api(
      `/suppliers/${supplierId}/imports?older_than_days=30`,
      { method: "DELETE" },
    );
    await refreshAfterSupplierImportDelete(result);
    showAlert(t("message.importsDeleted", {
      imports: result.deleted_imports || 0,
      offers: result.deleted_catalog?.supplier_offers || 0,
    }));
  } catch (error) {
    showAlert(error.message, true);
  } finally {
    button.disabled = false;
  }
}

async function deleteOldImportsGlobal(button) {
  if (!window.confirm(t("message.confirmDeleteOldImports"))) return;

  button.disabled = true;
  try {
    const result = await api(
      "/suppliers/imports/history?older_than_days=30",
      { method: "DELETE" },
    );
    await refreshAfterSupplierImportDelete(result);
    showAlert(t("message.importsDeleted", {
      imports: result.deleted_imports || 0,
      offers: result.deleted_catalog?.supplier_offers || 0,
    }));
  } catch (error) {
    showAlert(error.message, true);
  } finally {
    button.disabled = false;
  }
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
    loadMarketSnapshots(),
    loadAmazonPresence(),
  ]);
}

async function saveSupplierPriceSource(
  supplierId,
  priceUrl,
  options = {},
) {
  const result = await api(`/suppliers/${supplierId}/price-source`, {
    method: "PATCH",
    body: JSON.stringify({
      price_url: priceUrl || null,
    }),
  });

  if (!options.silent) {
    showAlert(t("message.priceLinkSaved"));
  }

  return result;
}

async function saveSupplierPricing(supplierId, button) {
  const panel = document.querySelector("#supplier-detail");
  const pricesIncludeVat = panel.querySelector(
    "[data-supplier-prices-include-vat]",
  ).checked;
  const vatInput = panel.querySelector("[data-supplier-default-vat-rate]");
  const defaultVatRate = vatInput.value === "" ? null : Number(vatInput.value);

  button.disabled = true;
  try {
    await api(`/suppliers/${supplierId}/pricing`, {
      method: "PATCH",
      body: JSON.stringify({
        prices_include_vat: pricesIncludeVat,
        default_vat_rate: defaultVatRate,
      }),
    });
    await Promise.all([
      loadSuppliers(),
      loadSupplierDetail(supplierId, { silent: true }),
    ]);
    showAlert(t("message.supplierPricingSaved"));
  } catch (error) {
    showAlert(error.message, true);
  } finally {
    button.disabled = false;
  }
}

async function checkSupplierPriceUpdate(
  supplierId,
  button,
) {
  button.disabled = true;

  try {
    const result = await api(
      `/suppliers/${supplierId}/check-price-update`,
      { method: "POST" },
    );
    showAlert(t("message.priceCheckResult", {
      supplier: result.name || `#${supplierId}`,
      status: priceUpdateLabel(result.price_update_status),
      checked: formatDate(result.price_last_checked_at || result.checked_at),
    }));
    await Promise.all([
      loadSuppliers(),
      loadSuppliersDashboard(),
    ]);

    if (state.supplierDetail?.id) {
      await loadSupplierDetail(state.supplierDetail.id, { silent: true });
    }
  } catch (error) {
    showAlert(error.message, true);
    await Promise.all([
      loadSuppliers(),
      loadSuppliersDashboard(),
    ]);
  } finally {
    button.disabled = false;
  }
}

async function loadSupplierPricePreview(
  supplierId,
  button,
  options = {},
) {
  const input = document.querySelector(
    "#supplier-detail [data-supplier-price-url]",
  );
  const supplier = state.supplierManagement.find(
    (item) => String(item.id) === String(supplierId),
  );
  const priceUrl = options.useSavedUrl
    ? supplier?.price_url || ""
    : input?.value.trim() || "";

  if (!priceUrl) {
    showAlert(t("field.priceUrl"), true);
    input?.focus();
    return;
  }

  button.disabled = true;

  try {
    if (!options.useSavedUrl) {
      await saveSupplierPriceSource(
        supplierId,
        priceUrl,
        { silent: true },
      );
    }

    const result = await api(
      `/upload/supplier-price-preview?supplier_id=${encodeURIComponent(supplierId)}`,
      { method: "POST" },
    );
    const uploadForm = document.querySelector("#upload-form");

    uploadForm.elements.supplier_name.value = result.supplier_name;
    uploadForm.elements.file.value = "";
    setImportDraft(result);
    renderImportPreview(result);
    state.supplierDetail = null;
    renderSupplierDetail(null);
    navigateToView("upload");

    showAlert(
      result.saved_filter_warning
        || t("message.pricePreviewReady", { count: result.rows }),
      Boolean(result.saved_filter_warning),
    );

    await Promise.all([
      loadSuppliers(),
      loadSuppliersDashboard(),
    ]);
  } catch (error) {
    showAlert(error.message, true);
  } finally {
    button.disabled = false;
  }
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
  renderSettingsPermissions();
  renderKeepaModeBadge();
  renderResearchControls();
}

async function loadMaintenanceStatus() {
  state.maintenance = await api("/maintenance/status");
  renderMaintenanceStatus();
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

async function loadMarketSnapshots() {
  const snapshots = await api(scopedPath("/market-snapshots/?limit=500"));

  renderRows("#market-snapshot-table", snapshots, [
    { key: "supplier_name", label: t("table.supplier") },
    { key: "asin", label: "ASIN" },
    {
      key: "snapshot_status",
      label: t("table.status"),
      render: (row) => `<span class="badge ${statusClass(row.snapshot_status)}">${escapeHtml(row.snapshot_status)}</span>`,
    },
    {
      key: "snapshot_source",
      label: t("table.source"),
      render: (row) => `<span class="badge ${row.snapshot_source === "keepa_real" ? "ok" : "warn"}">${keepaSourceLabel(row.snapshot_source)}</span>`,
      export: (row) => keepaSourceLabel(row.snapshot_source),
    },
    {
      key: "current_price",
      label: t("table.currentPrice"),
      render: (row) => formatNumber(row.current_price),
    },
    {
      key: "buy_box_price",
      label: t("table.buyBox"),
      render: (row) => formatNumber(row.buy_box_price),
    },
    {
      key: "sales_rank",
      label: t("table.salesRank"),
      render: (row) => formatNumber(row.sales_rank),
    },
    {
      key: "seller_count",
      label: t("table.sellerCount"),
      render: (row) => formatNumber(row.seller_count),
    },
    {
      key: "amazon_present",
      label: t("table.amazonPresent"),
      render: (row) => `<span class="badge ${row.amazon_present ? "bad" : "ok"}">${formatBoolean(row.amazon_present)}</span>`,
      export: (row) => formatBoolean(row.amazon_present),
    },
  ], { exportTitle: t("panel.marketSnapshots") });
}

async function loadAmazonPresence() {
  const checks = await api(scopedPath("/amazon-presence/?limit=500"));

  renderRows("#amazon-presence-table", checks, [
    { key: "supplier_name", label: t("table.supplier") },
    { key: "asin", label: "ASIN" },
    {
      key: "amazon_present",
      label: t("table.amazonPresent"),
      render: (row) => `<span class="badge ${row.amazon_present ? "bad" : "ok"}">${formatBoolean(row.amazon_present)}</span>`,
      export: (row) => formatBoolean(row.amazon_present),
    },
    {
      key: "presence_status",
      label: t("table.status"),
      render: (row) => `<span class="badge ${statusClass(row.presence_status)}">${escapeHtml(row.presence_status)}</span>`,
    },
    {
      key: "data_source",
      label: t("table.source"),
      render: (row) => `<span class="badge ${row.data_source === "keepa_real" ? "ok" : "warn"}">${keepaSourceLabel(row.data_source)}</span>`,
      export: (row) => keepaSourceLabel(row.data_source),
    },
    { key: "marketplace", label: t("field.marketplace") },
  ], { exportTitle: t("panel.amazonPresence") });
}

async function refreshAll() {
  try {
    await api("/");
    setStatus(true);
    await loadAuthUser();
    await loadSuppliers();
    await Promise.all([
      loadSummary(),
      loadConfig(),
      loadDeals(),
      loadResearch(),
      loadKeepa(),
      loadMarketSnapshots(),
      loadAmazonPresence(),
      loadSuppliersDashboard(),
      loadSavedImports(),
      loadMaintenanceStatus(),
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
    await Promise.all([
      loadSummary(),
      loadDeals(),
      loadResearch(),
      loadKeepa(),
      loadMarketSnapshots(),
      loadAmazonPresence(),
    ]);
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
    if (result.amazon_processed?.status === "rate_limited") {
      showAlert(keepaRateLimitMessage(result.amazon_processed), true);
    } else {
      showAlert(t("message.researchRun", {
        count: result.amazon_processed?.processed_count || 0,
      }));
    }
    await Promise.all([
      loadSummary(),
      loadResearch(),
      loadDeals(),
      loadKeepa(),
      loadMarketSnapshots(),
      loadAmazonPresence(),
    ]);
  } catch (error) {
    showAlert(error.message, true);
  } finally {
    button.disabled = false;
  }
}

async function runMarketSnapshot(triggerButton = null) {
  const button = triggerButton || document.querySelector("#run-market-snapshot-button");

  if (state.settings?.use_real_keepa && !canUseRealKeepa()) {
    showAlert(t("message.keepaPermissionRequired"), true);
    renderKeepaModeBadge();
    return;
  }

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
    const pendingResult = await api(scopedPath("/market-snapshots/create-pending"), {
      method: "POST",
    });
    const processResult = await api(scopedPath("/market-snapshots/process-pending"), {
      method: "POST",
    });

    if (processResult.status === "not_configured") {
      showAlert(
        processResult.reason || t("message.keepaNotConfigured"),
        true,
      );
    } else if (processResult.status === "rate_limited") {
      showAlert(keepaRateLimitMessage(processResult), true);
    } else {
      showAlert(t("message.marketSnapshotRun", {
        source: keepaSourceLabel(processResult.data_source),
        created: pendingResult.created_count || 0,
        processed: processResult.processed_count || 0,
      }));
    }

    await Promise.all([
      loadSummary(),
      loadConfig(),
      loadMarketSnapshots(),
      loadResearch(),
      loadDeals(),
      loadSuppliersDashboard(),
    ]);
  } catch (error) {
    showAlert(error.message, true);
  } finally {
    button.disabled = false;
  }
}

async function createDealCandidates(triggerButton = null) {
  const button = triggerButton;

  if (button) button.disabled = true;

  try {
    const result = await api(scopedPath("/deals/create-candidates"), {
      method: "POST",
    });

    showAlert(t("message.dealsCreated", {
      count: result.created_count || 0,
    }));

    await Promise.all([
      loadSummary(),
      loadDeals(),
      loadResearch(),
      loadMarketSnapshots(),
      loadSuppliersDashboard(),
    ]);
  } catch (error) {
    showAlert(error.message, true);
  } finally {
    if (button) button.disabled = false;
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

  if (state.settings?.use_real_keepa && !canUseRealKeepa()) {
    showAlert(t("message.keepaPermissionRequired"), true);
    renderKeepaModeBadge();
    return;
  }

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
    } else if (processResult.status === "rate_limited") {
      showAlert(keepaRateLimitMessage(processResult), true);
    } else {
      showAlert(t("message.keepaRunWithSource", {
        source: keepaSourceLabel(processResult.data_source),
        created: pendingResult.created_count || 0,
        processed: processResult.processed_count || 0,
      }));
    }

    await Promise.all([
      loadSummary(),
      loadConfig(),
      loadKeepa(),
      loadMarketSnapshots(),
      loadDeals(),
    ]);
  } catch (error) {
    showAlert(error.message, true);
  } finally {
    button.disabled = false;
  }
}

async function runAmazonPresence(triggerButton = null) {
  const button = triggerButton || document.querySelector("#run-amazon-presence-button");

  if (state.settings?.use_real_keepa && !canUseRealKeepa()) {
    showAlert(t("message.keepaPermissionRequired"), true);
    renderKeepaModeBadge();
    return;
  }

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
    const pendingResult = await api(scopedPath("/amazon-presence/create-pending"), {
      method: "POST",
    });
    const processResult = await api(scopedPath("/amazon-presence/process-pending"), {
      method: "POST",
    });

    if (processResult.status === "not_configured") {
      showAlert(
        processResult.reason || t("message.keepaNotConfigured"),
        true,
      );
    } else if (processResult.status === "rate_limited") {
      showAlert(keepaRateLimitMessage(processResult), true);
    } else {
      showAlert(t("message.amazonPresenceRun", {
        source: keepaSourceLabel(processResult.data_source),
        created: pendingResult.created_count || 0,
        processed: processResult.processed_count || 0,
      }));
    }

    await Promise.all([
      loadSummary(),
      loadConfig(),
      loadKeepa(),
      loadMarketSnapshots(),
      loadAmazonPresence(),
      loadDeals(),
    ]);
  } catch (error) {
    showAlert(error.message, true);
  } finally {
    button.disabled = false;
  }
}

async function saveKeepaMode(useRealKeepa, toggle) {
  if (useRealKeepa && !canUseRealKeepa()) {
    toggle.checked = false;
    showAlert(t("message.keepaPermissionRequired"), true);
    renderKeepaModeBadge();
    return;
  }

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
    if (result.amazon_processed?.status === "rate_limited") {
      showAlert(keepaRateLimitMessage(result.amazon_processed), true);
    } else {
      showAlert(t("message.researchRun", {
        count: result.amazon_processed?.processed_count || 0,
      }));
    }
    await Promise.all([
      loadSummary(),
      loadResearch(),
      loadKeepa(),
      loadMarketSnapshots(),
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

  if (
    form.id === "pipeline-settings-form"
    && payload.use_real_keepa
    && !canUseRealKeepa()
  ) {
    throw new Error(t("message.keepaPermissionRequired"));
  }

  const result = await api(endpoint, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });

  fillForm(form, result);
  if (form.id === "pipeline-settings-form") {
    state.settings = result;
    state.keepaStatus = await api("/keepa/status");
    renderKeepaModeBadge();
    renderSettingsPermissions();
  }
  showAlert(t("message.saved"));
  await loadSummary();
}

async function clearPreviewWorkspace(button) {
  if (!window.confirm(t("message.confirmClearWorkspace"))) return;

  button.disabled = true;

  try {
    const result = await api("/maintenance/clear-workspace", {
      method: "POST",
      body: JSON.stringify({
        confirmation: "CLEAR WORKSPACE",
      }),
    });

    setImportDraft(null);
    document.querySelector("#upload-form").reset();
    const resultBox = document.querySelector("#maintenance-result");
    resultBox.textContent = t("message.maintenanceResult", {
      action: t("action.clearWorkspace"),
      rows: formatNumber(result.rows_released || 0),
      size: formatBytes(result.estimated_bytes_released || 0),
    });
    resultBox.classList.remove("hidden");
    showAlert(t("message.workspaceCleared", {
      drafts: formatNumber(result.drafts_cleared || 0),
      rows: formatNumber(result.rows_released || 0),
    }));
    await loadMaintenanceStatus();
  } catch (error) {
    showAlert(error.message, true);
  } finally {
    button.disabled = false;
  }
}

async function clearDatabaseData(button) {
  if (!window.confirm(t("message.confirmClearDatabase"))) return;

  button.disabled = true;

  try {
    const result = await api("/maintenance/clear-database", {
      method: "POST",
      body: JSON.stringify({
        confirmation: "CLEAR DATABASE",
      }),
    });

    state.supplierDetail = null;
    renderSupplierDetail(null);
    const resultBox = document.querySelector("#maintenance-result");
    resultBox.textContent = t("message.maintenanceResult", {
      action: t("action.clearDatabase"),
      rows: formatNumber(result.rows_cleared || 0),
      size: formatBytes(result.estimated_bytes_released || 0),
    });
    resultBox.classList.remove("hidden");
    showAlert(t("message.databaseCleared", {
      rows: formatNumber(result.rows_cleared || 0),
    }));
    await refreshAll();
  } catch (error) {
    showAlert(error.message, true);
  } finally {
    button.disabled = false;
  }
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
  state.supplyChannelsConfirmed = false;
  updateUploadActionButtons();

  if (!draft) {
    state.importFiltersConfirmed = false;
    state.importPreview = null;
    document.querySelector("#upload-preview").classList.add("hidden");
    updateUploadActionButtons();
  }
}

function updateUploadActionButtons() {
  document.querySelector("#save-import-button").classList.toggle(
    "hidden",
    !state.importDraft
      || !state.importFiltersConfirmed
      || !state.supplyChannelsConfirmed,
  );
  document.querySelector("#reset-upload-button").classList.toggle(
    "hidden",
    !state.importDraft && !state.importPreview,
  );
}

function supplyChannelAssignments() {
  return Object.fromEntries(
    Array.from(document.querySelectorAll("[data-supply-channel-file]"))
      .map((select) => [select.dataset.supplyChannelFile, select.value]),
  );
}

function supplyLeadTime(item) {
  const min = item.lead_time_min_days;
  const max = item.lead_time_max_days;
  if (min == null || max == null) return "-";
  if (min === 0 && max === 0) return "0 d";
  return min === max ? `${min} d` : `${min}-${max} d`;
}

function renderSupplyChannels(items = []) {
  const list = document.querySelector("#supply-channel-list");
  const confirmation = document.querySelector("#confirm-supply-channels");
  if (!list || !confirmation) return;

  list.innerHTML = items.map((item) => `
    <article class="supply-channel-item">
      <div class="supply-channel-file">
        <strong>${escapeHtml(item.filename)}</strong>
        <span>${escapeHtml((item.evidence || []).join(" · ") || "-")}</span>
      </div>
      <label>
        <span>${t("field.supplyChannel")}</span>
        <select data-supply-channel-file="${escapeHtml(item.filename)}">
          <option value="" ${item.channel ? "" : "selected"}>-</option>
          <option value="stock" ${item.channel === "stock" ? "selected" : ""}>${t("supply.stock")}</option>
          <option value="incoming" ${item.channel === "incoming" ? "selected" : ""}>${t("supply.incoming")}</option>
          <option value="preorder" ${item.channel === "preorder" ? "selected" : ""}>${t("supply.preorder")}</option>
        </select>
      </label>
      <div class="supply-channel-meta">
        <span>${t("field.leadTime")}</span>
        <strong>${supplyLeadTime(item)}</strong>
        <span class="badge ${item.confidence >= 60 ? "ok" : "warn"}">${formatNumber(item.confidence || 0)}%</span>
      </div>
    </article>
  `).join("");

  confirmation.checked = false;
  confirmation.disabled = items.length === 0 || items.some((item) => !item.channel);
  state.supplyChannelsConfirmed = false;
  list.querySelectorAll("select").forEach((select) => {
    select.addEventListener("change", () => {
      confirmation.checked = false;
      confirmation.disabled = Array.from(list.querySelectorAll("select"))
        .some((element) => !element.value);
      state.supplyChannelsConfirmed = false;
      updateUploadActionButtons();
    });
  });
  confirmation.onchange = () => {
    state.supplyChannelsConfirmed = confirmation.checked;
    updateUploadActionButtons();
  };
  updateUploadActionButtons();
}

function previewColumnClass(column) {
  const name = String(column || "").toLowerCase();

  if (["price", "cost", "stock", "moq"].includes(name)) return "numeric";
  if (["ean", "gtin", "upc", "barcode"].includes(name)) return "identifier";
  if (name.includes("sku") || name.includes("mpn") || name.includes("part")) return "code";
  if (name.includes("description")) return "description";
  if (name.includes("title") || name.includes("name")) return "title";
  if (name.includes("category")) return "category";
  if (name.includes("brand") || name.includes("manufacturer")) return "brand";

  return "default";
}

function renderPreviewRows(rows, columns) {
  const tableHead = document.querySelector("#preview-table-head");
  const tableBody = document.querySelector("#preview-table-body");

  tableHead.innerHTML = `
    <tr>
      ${columns.map((column) => `<th class="preview-col-${previewColumnClass(column)}">${escapeHtml(column)}</th>`).join("")}
    </tr>
  `;

  tableBody.innerHTML = rows.length
    ? rows
      .map((row) => `
        <tr>
          ${columns.map((column) => `<td class="preview-col-${previewColumnClass(column)}">${escapeHtml(row[column]) || "-"}</td>`).join("")}
        </tr>
      `)
      .join("")
    : `<tr><td colspan="${columns.length || 1}">${t("message.noRecords")}</td></tr>`;
}

function setUploadSearchStatus(message = "") {
  const status = document.querySelector("#upload-preview-search-status");

  if (status) {
    status.textContent = message;
  }
}

function resetUploadSearchPanel() {
  const input = document.querySelector("#upload-preview-search-input");

  if (input) {
    input.value = "";
    input.placeholder = t("message.searchPlaceholder");
  }

  setUploadSearchStatus("");
}

function resetUploadForm() {
  const form = document.querySelector("#upload-form");
  form?.reset();
  setImportDraft(null);
  resetUploadSearchPanel();
  registerTableExport("#preview-table-body", t("panel.previewRows"), [], []);
  showAlert(t("action.newUpload"));
}

function markImportFiltersDirty() {
  state.importFiltersConfirmed = false;
  updateUploadActionButtons();

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
  const mappingList = document.querySelector("#mapping-list");
  const columns = result.normalized_columns || [];
  const rows = result.preview || [];
  const mappedColumns = new Set(
    (result.normalization_report || [])
      .map((item) => item.mapped_to)
      .filter(Boolean),
  ).size;
  const filenames = result.filenames || [result.filename];

  summary.innerHTML = `
    <article>
      <span>${t("field.supplierName")}</span>
      <strong>${escapeHtml(result.supplier_name)}</strong>
    </article>
    <article>
      <span>${t("field.file")}</span>
      <strong title="${escapeHtml(filenames.join(", "))}">${escapeHtml(filenames.join(", "))}</strong>
    </article>
    <article>
      <span>${t("field.fileCount")}</span>
      <strong>${formatNumber(result.file_count || filenames.length)}</strong>
    </article>
    <article>
      <span>${t("field.skippedFiles")}</span>
      <strong title="${escapeHtml((result.skipped_files || []).join(", "))}">${formatNumber(result.skipped_file_count || 0)}</strong>
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
  renderFileDiagnostics(result.file_diagnostics || []);
  renderSupplyChannels(result.supply_channel_suggestions || []);
  renderImportFilters(result);
  resetUploadSearchPanel();
  renderPreviewRows(rows, columns);

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
            <strong>${escapeHtml(item.file ? `${item.file}: ${item.column}` : item.column)}</strong>
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

function renderFileDiagnostics(diagnostics) {
  const container = document.querySelector("#upload-file-diagnostics");
  if (!container) return;
  if (!diagnostics.length) {
    container.innerHTML = "";
    return;
  }

  const rows = [...diagnostics].sort((left, right) => (
    (right.missing_ean + right.missing_price + right.unmapped_columns)
    + (right.invalid_ean || 0)
    - (left.missing_ean + left.missing_price + left.unmapped_columns
      + (left.invalid_ean || 0))
  ));

  container.innerHTML = `
    <details class="file-diagnostics" ${rows.length <= 10 ? "open" : ""}>
      <summary>${t("panel.fileDiagnostics")} · ${formatNumber(rows.length)}</summary>
      <div class="table-wrap file-diagnostics-table">
        <table>
          <thead>
            <tr>
              <th>${t("table.file")}</th>
              <th>${t("table.rows")}</th>
              <th>${t("quality.missingEan")}</th>
              <th>${t("quality.invalidEan")}</th>
              <th>${t("quality.supplierCode")}</th>
              <th>${t("quality.testerRows")}</th>
              <th>${t("quality.missingPrice")}</th>
              <th>${t("quality.duplicateEan")}</th>
              <th>${t("field.mapped")}</th>
              <th>${t("quality.unmappedColumns")}</th>
            </tr>
          </thead>
          <tbody>
            ${rows.map((item) => `
              <tr>
                <td>${escapeHtml(item.filename)}</td>
                <td>${formatNumber(item.rows)}</td>
                <td>${formatNumber(item.missing_ean)}</td>
                <td>${formatNumber(item.invalid_ean || 0)}</td>
                <td>${formatNumber(item.supplier_code || 0)}</td>
                <td>${formatNumber(item.tester || 0)}</td>
                <td>${formatNumber(item.missing_price)}</td>
                <td>${formatNumber(item.duplicate_ean)}</td>
                <td>${formatNumber(item.mapped_columns)}</td>
                <td>${formatNumber(item.unmapped_columns)}</td>
              </tr>
            `).join("")}
          </tbody>
        </table>
      </div>
    </details>
  `;
}

async function searchUploadPreview(button) {
  if (!state.importDraft?.import_token) {
    showAlert(t("message.noRecords"), true);
    return;
  }

  if (!state.importFiltersConfirmed) {
    showAlert(t("message.applyFiltersToUpdatePreview"), true);
    return;
  }

  const input = document.querySelector("#upload-preview-search-input");
  const query = input?.value.trim() || "";

  if (!query) {
    input?.focus();
    return;
  }

  button.disabled = true;

  try {
    const filters = state.importPreview?.filter_summary?.filters || null;
    const result = await api("/upload/search-preview", {
      method: "POST",
      body: JSON.stringify({
        import_token: state.importDraft.import_token,
        filters,
        query,
        limit: 100,
      }),
    });
    const columns = result.columns || state.importPreview?.normalized_columns || [];
    const rows = result.rows || [];

    renderPreviewRows(rows, columns);
    registerTableExport(
      "#preview-table-body",
      `${state.importPreview?.supplier_name || "upload"}-${query}`,
      rows,
      columns.map((column) => ({
        key: column,
        label: column,
      })),
    );
    setUploadSearchStatus(t("message.searchResults", {
      total: formatNumber(result.total_matches || 0),
      shown: formatNumber(rows.length),
    }));
  } catch (error) {
    showAlert(error.message, true);
  } finally {
    button.disabled = false;
  }
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
        <small>${t("message.testersSkipped", {
          count: formatNumber(result.filter_summary.tester_rows_skipped || 0),
        })}</small>
      </article>
    `;
    state.importFiltersConfirmed = Boolean(result.is_filtered_preview);
    updateUploadActionButtons();
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
    suggestions.tester_count || 0,
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

  updateUploadActionButtons();
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

function sortFilterChoicesByValue(items) {
  return [...(items || [])].sort((first, second) => (
    String(first.value || "").localeCompare(
      String(second.value || ""),
      undefined,
      { sensitivity: "base" },
    )
  ));
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
        ${renderFilterChoices(sortFilterChoicesByValue(suggestions.brands), "data-import-filter-brand", t("message.noRecords"), selectedBrands)}
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
        <input id="import-filter-missing-ean" type="checkbox" ${activeFilters.exclude_missing_ean ? "checked" : ""}>
        <span>${t("field.excludeMissingEan")}</span>
        <strong>${formatNumber(suggestions.missing_ean_count || 0)}</strong>
      </label>
      <label class="filter-choice">
        <input id="import-filter-non-new" type="checkbox" ${activeFilters.exclude_non_new ? "checked" : ""}>
        <span>${t("field.excludeNonNew")}</span>
        <strong>${formatNumber(suggestions.non_new_count || 0)}</strong>
      </label>
      <label class="filter-choice locked-filter">
        <input type="checkbox" checked disabled>
        <span>${t("field.excludeTesters")}</span>
        <strong>${formatNumber(suggestions.tester_count || 0)}</strong>
      </label>
      <div class="price-filter-row">
        <label>
          <span>${t("field.minCost")}</span>
          <input id="import-filter-min-price" type="number" min="0" step="0.01" value="${escapeHtml(activeFilters.min_price ?? "")}" placeholder="${formatNumber(suggestions.price?.min)}">
        </label>
        <label>
          <span>${t("field.maxCost")}</span>
          <input id="import-filter-max-price" type="number" min="0" step="0.01" value="${escapeHtml(activeFilters.max_price ?? "")}" placeholder="${formatNumber(suggestions.price?.max)}">
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
      .map((column) => csvEscape(csvCellValue(row, column)))
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
  const shell = document.querySelector(".app-shell");
  const savedSidebarState = localStorage.getItem("oaSidebarCollapsed") === "true";

  shell?.classList.toggle("sidebar-collapsed", savedSidebarState);

  document.querySelector("#sidebar-toggle")?.addEventListener("click", () => {
    const collapsed = shell.classList.toggle("sidebar-collapsed");
    localStorage.setItem("oaSidebarCollapsed", String(collapsed));
  });

  document.querySelectorAll(".nav-group-toggle").forEach((button) => {
    button.addEventListener("click", () => {
      const group = button.closest(".nav-group");
      const expanded = group.classList.toggle("expanded");
      button.setAttribute("aria-expanded", String(expanded));
    });
  });

  document.querySelectorAll(".nav-item").forEach((button) => {
    button.addEventListener("click", () => {
      const view = button.dataset.view;
      document.querySelectorAll(".nav-item").forEach((item) => {
        item.classList.toggle("active", item === button);
      });
      document.querySelectorAll(".nav-group").forEach((group) => {
        group.classList.toggle(
          "active-group",
          group.contains(button),
        );
      });
      document.querySelectorAll(".view").forEach((section) => {
        section.classList.toggle("active", section.id === `view-${view}`);
      });
      state.activeView = view;
      document.querySelector("#view-title").textContent = t(`nav.${view}`);
      updateSupplierScopeVisibility();
    });
  });

  const activeItem = document.querySelector(".nav-item.active");
  activeItem?.closest(".nav-group")?.classList.add("active-group");
}

function bindActions() {
  document.querySelector("#auth-logout-button")?.addEventListener("click", async () => {
    const form = document.createElement("form");
    form.method = "POST";
    form.action = "/auth/logout";
    document.body.appendChild(form);
    form.submit();
  });

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
        loadMarketSnapshots(),
        loadAmazonPresence(),
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
  document.querySelector("#run-market-snapshot-button").addEventListener("click", (event) => {
    runMarketSnapshot(event.currentTarget);
  });
  document.querySelector("#run-amazon-presence-button").addEventListener("click", (event) => {
    runAmazonPresence(event.currentTarget);
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

    if (action === "snapshot") {
      runMarketSnapshot(button);
      return;
    }

    if (action === "deals") {
      createDealCandidates(button);
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
    const downloadButton = event.target.closest("[data-download-supplier-price]");
    const checkButton = event.target.closest("[data-check-supplier-price]");
    const createButton = event.target.closest("[data-focus-supplier-create]");
    const button = event.target.closest("[data-select-supplier]");

    if (createButton) {
      document.querySelector("#supplier-create-form input[name='name']")?.focus();
      return;
    }

    if (downloadButton) {
      loadSupplierPricePreview(
        downloadButton.dataset.downloadSupplierPrice,
        downloadButton,
        { useSavedUrl: true },
      );
      return;
    }

    if (checkButton) {
      checkSupplierPriceUpdate(
        checkButton.dataset.checkSupplierPrice,
        checkButton,
      );
      return;
    }

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
      await Promise.all([
        loadSummary(),
        loadDeals(),
        loadResearch(),
        loadKeepa(),
        loadMarketSnapshots(),
        loadAmazonPresence(),
      ]);
    } catch (error) {
      showAlert(error.message, true);
    }
  });
  document.querySelector("#supplier-management").addEventListener("click", async (event) => {
    const detailButton = event.target.closest("[data-open-supplier-details]");
    const visibilityButton = event.target.closest("[data-toggle-supplier-visibility]");
    const downloadButton = event.target.closest("[data-download-supplier-price]");
    const checkButton = event.target.closest("[data-check-supplier-price]");
    const createButton = event.target.closest("[data-focus-supplier-create]");

    if (createButton) {
      document.querySelector("#supplier-create-form input[name='name']")?.focus();
      return;
    }

    if (downloadButton) {
      loadSupplierPricePreview(
        downloadButton.dataset.downloadSupplierPrice,
        downloadButton,
        { useSavedUrl: true },
      );
      return;
    }

    if (checkButton) {
      checkSupplierPriceUpdate(
        checkButton.dataset.checkSupplierPrice,
        checkButton,
      );
      return;
    }

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
  document.querySelector("#supplier-create-form").addEventListener("submit", (event) => {
    event.preventDefault();
    createSupplier(event.currentTarget);
  });
  document.querySelector("#supplier-detail").addEventListener("click", (event) => {
    const closeButton = event.target.closest("[data-close-supplier-details]");
    const scopeButton = event.target.closest("[data-supplier-scope]");
    const navButton = event.target.closest("[data-supplier-nav]");
    const researchButton = event.target.closest("[data-run-supplier-research]");
    const savePriceButton = event.target.closest("[data-save-supplier-price-url]");
    const loadPriceButton = event.target.closest("[data-load-supplier-price]");
    const checkPriceButton = event.target.closest("[data-check-supplier-price]");
    const savePricingButton = event.target.closest("[data-save-supplier-pricing]");
    const deleteImportButton = event.target.closest("[data-delete-supplier-import]");
    const deleteOldImportsButton = event.target.closest("[data-delete-old-supplier-imports]");

    if (deleteImportButton) {
      deleteSupplierImport(deleteImportButton);
      return;
    }

    if (deleteOldImportsButton) {
      deleteOldSupplierImports(deleteOldImportsButton);
      return;
    }

    if (savePricingButton) {
      saveSupplierPricing(
        savePricingButton.dataset.saveSupplierPricing,
        savePricingButton,
      );
      return;
    }

    if (checkPriceButton) {
      checkSupplierPriceUpdate(
        checkPriceButton.dataset.checkSupplierPrice,
        checkPriceButton,
      );
      return;
    }

    if (savePriceButton) {
      const input = document.querySelector(
        "#supplier-detail [data-supplier-price-url]",
      );

      savePriceButton.disabled = true;
      saveSupplierPriceSource(
        savePriceButton.dataset.saveSupplierPriceUrl,
        input?.value.trim() || "",
      )
        .then(() => loadSupplierDetail(
          savePriceButton.dataset.saveSupplierPriceUrl,
          { silent: true },
        ))
        .catch((error) => showAlert(error.message, true))
        .finally(() => {
          savePriceButton.disabled = false;
        });
      return;
    }

    if (loadPriceButton) {
      loadSupplierPricePreview(
        loadPriceButton.dataset.loadSupplierPrice,
        loadPriceButton,
      );
      return;
    }

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
  document.querySelector("#saved-imports-panel").addEventListener("click", (event) => {
    const deleteImportButton = event.target.closest("[data-delete-supplier-import]");
    const deleteOldButton = event.target.closest("#delete-old-imports-global");

    if (deleteImportButton) {
      deleteSupplierImport(deleteImportButton);
      return;
    }

    if (deleteOldButton) {
      deleteOldImportsGlobal(deleteOldButton);
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
  document.querySelector("#clear-workspace-button").addEventListener("click", (event) => {
    clearPreviewWorkspace(event.currentTarget);
  });
  document.querySelector("#clear-database-button").addEventListener("click", (event) => {
    clearDatabaseData(event.currentTarget);
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

  document.querySelector("#procurement-form").addEventListener("submit", (event) => {
    event.preventDefault();
    runProcurementComparison(event.currentTarget);
  });
  document.querySelector("#clear-procurement-button").addEventListener("click", () => {
    document.querySelector("#procurement-form").reset();
    state.procurementComparison = null;
    renderProcurementComparison(null);
  });
  document.querySelector("#reset-procurement-grid").addEventListener("click", resetProcurementGrid);

  document.querySelector("#upload-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    const button = form.querySelector("button[type='submit']");
    if (button.disabled) return;

    const supplier = form.elements.supplier_name.value;
    const files = Array.from(form.elements.file.files || []);
    if (!files.length) return;
    const body = new FormData();
    files.forEach((file) => body.append("file", file));
    setImportDraft(null);
    button.disabled = true;

    try {
      const response = await fetch(`/upload/preview?supplier_name=${encodeURIComponent(supplier)}`, {
        method: "POST",
        body,
      });
      const text = await response.text();
      let result;
      try {
        result = text ? JSON.parse(text) : null;
      } catch (_error) {
        result = { detail: text || `Request failed with ${response.status}` };
      }

      if (!response.ok) {
        throw new Error(JSON.stringify(result.detail || result));
      }

      setImportDraft(result);
      renderImportPreview(result);
      showAlert(t(
        result.file_count > 1
          ? "message.batchPreviewReady"
          : "message.previewReady",
        { files: result.file_count, count: result.rows },
      ));
    } catch (error) {
      showAlert(error.message, true);
    } finally {
      button.disabled = false;
    }
  });

  document.querySelector("#apply-import-filters-button").addEventListener("click", (event) => {
    applyImportFilters(event.currentTarget);
  });
  document.querySelector("#download-upload-preview-csv").addEventListener("click", (event) => {
    downloadUploadPreviewCsv(event.currentTarget);
  });
  document.querySelector("#toggle-upload-preview-search").addEventListener("click", () => {
    const panel = document.querySelector("#upload-preview-search");
    const input = document.querySelector("#upload-preview-search-input");

    panel.classList.toggle("hidden");
    if (!panel.classList.contains("hidden")) {
      input.placeholder = t("message.searchPlaceholder");
      input.focus();
    }
  });
  document.querySelector("#run-upload-preview-search").addEventListener("click", (event) => {
    searchUploadPreview(event.currentTarget);
  });
  document.querySelector("#upload-preview-search-input").addEventListener("keydown", (event) => {
    if (event.key !== "Enter") return;

    event.preventDefault();
    searchUploadPreview(document.querySelector("#run-upload-preview-search"));
  });
  document.querySelector("#clear-upload-preview-search").addEventListener("click", () => {
    if (state.importPreview) {
      resetUploadSearchPanel();
      renderImportPreview(state.importPreview);
    }
  });
  document.querySelector("#reset-upload-button").addEventListener("click", () => {
    resetUploadForm();
  });

  document.querySelector("#save-import-button").addEventListener("click", async (event) => {
    const button = event.currentTarget;
    if (button.disabled || !state.importDraft?.import_token) return;

    button.disabled = true;

    try {
      const result = await api("/upload/commit", {
        method: "POST",
        body: JSON.stringify({
          import_token: state.importDraft.import_token,
          supply_channels: supplyChannelAssignments(),
        }),
      });

      setImportDraft(null);
      renderImportPreview(result);
      showAlert(t("message.savedImport", { count: result.offers_saved }));
      await Promise.all([
        loadSummary(),
        loadResearch(),
        loadKeepa(),
        loadMarketSnapshots(),
        loadSuppliers(),
        loadSuppliersDashboard(),
        loadSavedImports(),
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
