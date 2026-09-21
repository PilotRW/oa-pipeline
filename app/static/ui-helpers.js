function formatNumber(value) {
  if (value === null || value === undefined) return "-";
  return Number(value).toLocaleString(undefined, { maximumFractionDigits: 2 });
}

function formatBytes(value) {
  let bytes = Number(value || 0);
  const units = ["B", "KB", "MB", "GB", "TB"];
  let unitIndex = 0;
  while (bytes >= 1024 && unitIndex < units.length - 1) {
    bytes /= 1024;
    unitIndex += 1;
  }
  return `${bytes.toLocaleString(undefined, {
    maximumFractionDigits: unitIndex ? 1 : 0,
  })} ${units[unitIndex]}`;
}

function formatDate(value) {
  if (!value) return "-";
  return new Date(value).toLocaleString();
}

function formatBoolean(value) {
  if (value === true) return "Yes";
  if (value === false) return "No";
  return "-";
}

function statusClass(status) {
  if (!status) return "";
  if (String(status).includes("candidate") || status === "completed") {
    return "ok";
  }
  if (String(status).includes("reject") || String(status).includes("not")) {
    return "bad";
  }
  return "warn";
}

function priceUpdateClass(status) {
  if (["current", "no_changes"].includes(status)) return "ok";
  if (status === "new_available") return "bad";
  return "warn";
}

function priceDownloadButtonClass(status) {
  return status === "new_available"
    ? "primary-button"
    : "ghost-button price-download-muted";
}
