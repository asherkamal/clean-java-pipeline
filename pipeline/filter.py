import logging

log = logging.getLogger(__name__)

_DROP_COLUMNS = {"is_generated", "src_encoding", "extension"}


def prefilter_stream(ds):
    log.info("Applying pre-filter (is_generated, src_encoding, extension)...")
    return ds.filter(
        lambda row: (
            not row.get("is_generated", False)
            and (row.get("src_encoding") or "").upper() == "UTF-8"
            and (row.get("extension") or "").lower().lstrip(".") == "java"
        )
    )


def drop_filter_columns(row: dict) -> dict:
    return {k: v for k, v in row.items() if k not in _DROP_COLUMNS}
