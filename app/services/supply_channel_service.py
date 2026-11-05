import re
from html import unescape
from zipfile import BadZipFile, ZipFile
from io import BytesIO


SUPPLY_CHANNELS = {"stock", "incoming", "preorder"}
WEEK_RANGE = re.compile(
    r"(\d+)\s*(?:-|–|—|to)\s*(\d+)\s*weeks?",
    re.IGNORECASE,
)
SINGLE_WEEK = re.compile(r"(\d+)\s*weeks?", re.IGNORECASE)


def searchable_file_text(filename: str, content: bytes) -> str:
    parts = [str(filename or "")]
    if str(filename).lower().endswith(".xlsx"):
        try:
            with ZipFile(BytesIO(content)) as archive:
                for name in archive.namelist():
                    if name in {
                        "xl/workbook.xml",
                        "xl/sharedStrings.xml",
                    } or name.startswith("xl/worksheets/sheet"):
                        parts.append(
                            archive.read(name).decode("utf-8", errors="ignore")
                        )
        except (BadZipFile, KeyError):
            pass
    else:
        parts.append(content[:100_000].decode("utf-8", errors="ignore"))

    text = unescape(" ".join(parts))
    return re.sub(r"<[^>]+>", " ", text)


def infer_supply_channel(filename: str, content: bytes) -> dict:
    text = searchable_file_text(filename, content)
    normalized = re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()
    filename_normalized = re.sub(
        r"[^a-z0-9]+",
        " ",
        str(filename or "").lower(),
    ).strip()
    evidence = []
    confidence = 0
    channel = None

    channel_terms = [
        ("preorder", ("preorder", "pre order")),
        ("incoming", ("incoming", "inbound")),
        ("stock", ("stocklist", "stock list", "skundys stock")),
    ]
    for candidate, terms in channel_terms:
        filename_match = next(
            (term for term in terms if term in filename_normalized),
            None,
        )
        content_match = next(
            (term for term in terms if term in normalized),
            None,
        )
        if filename_match or content_match:
            channel = candidate
            if filename_match:
                confidence += 60
                evidence.append(f'filename contains "{filename_match}"')
            if content_match:
                confidence += 35
                evidence.append(f'workbook contains "{content_match}"')
            break

    immediate = "immediate delivery" in normalized
    range_match = WEEK_RANGE.search(text)
    single_match = SINGLE_WEEK.search(text) if not range_match else None
    lead_time_min_days = None
    lead_time_max_days = None
    if immediate:
        lead_time_min_days = 0
        lead_time_max_days = 0
        evidence.append("available for immediate delivery")
        if channel is None:
            channel = "stock"
            confidence += 70
    elif range_match:
        lead_time_min_days = int(range_match.group(1)) * 7
        lead_time_max_days = int(range_match.group(2)) * 7
        evidence.append(
            f"{range_match.group(1)}-{range_match.group(2)} weeks lead time"
        )
        confidence += 5
    elif single_match:
        lead_time_min_days = int(single_match.group(1)) * 7
        lead_time_max_days = lead_time_min_days
        evidence.append(f"{single_match.group(1)} weeks lead time")
        confidence += 5

    return {
        "filename": str(filename or "supplier-file"),
        "channel": channel,
        "confidence": min(confidence, 100),
        "lead_time_min_days": lead_time_min_days,
        "lead_time_max_days": lead_time_max_days,
        "evidence": evidence,
    }


def validate_supply_channel_assignments(
    filenames: list[str],
    assignments: dict[str, str] | None,
) -> dict[str, str]:
    values = assignments or {}
    normalized = {
        str(filename): str(channel).strip().lower()
        for filename, channel in values.items()
    }
    missing = [filename for filename in filenames if filename not in normalized]
    invalid = {
        filename: channel
        for filename, channel in normalized.items()
        if filename in filenames and channel not in SUPPLY_CHANNELS
    }
    if missing:
        raise ValueError(
            "Confirm a supply category for every file: " + ", ".join(missing)
        )
    if invalid:
        raise ValueError("Supply category must be stock, incoming, or preorder")
    return {filename: normalized[filename] for filename in filenames}
