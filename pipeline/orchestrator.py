import logging

from tqdm import tqdm

from pipeline.config import MAX_OUTPUT_BYTES, MAX_OUTPUT_GB
from pipeline.fetch import stream_java_files
from pipeline.filter import prefilter_stream, drop_filter_columns
from pipeline.compile import download_content, compiles
from pipeline.lint import passes_checkstyle
from pipeline.rewrite import load_model, sgcr_rewrite
from pipeline.output import save_and_push

log = logging.getLogger(__name__)


def run_pipeline() -> None:
    model, tokenizer = load_model()
    java_stream = prefilter_stream(stream_java_files())

    results: list[dict] = []
    counts = {"fetched": 0, "compiled": 0, "linted": 0, "rewritten": 0}
    total_bytes = 0

    pbar = tqdm(java_stream, desc="Pipeline", unit=" files")
    for row in pbar:
        counts["fetched"] += 1

        source = download_content(row)
        if source is None:
            continue

        if not compiles(source):
            continue
        counts["compiled"] += 1

        if not passes_checkstyle(source):
            continue
        counts["linted"] += 1

        rewritten = sgcr_rewrite(source, model, tokenizer)
        counts["rewritten"] += 1

        total_bytes += len(source.encode()) + len(rewritten.encode())

        results.append({
            **drop_filter_columns(row),
            "content":           source,
            "rewritten_content": rewritten,
        })

        pbar.set_postfix({**counts, "size_gb": f"{total_bytes / 1024**3:.2f}"})

        if MAX_OUTPUT_BYTES and total_bytes >= MAX_OUTPUT_BYTES:
            log.info("Reached MAX_OUTPUT_GB=%.1f (%.2f GB collected), stopping.",
                     MAX_OUTPUT_GB, total_bytes / 1024 ** 3)
            break

    log.info("Final counts: %s", counts)
    if results:
        save_and_push(results)
    else:
        log.warning("No rows survived the pipeline — nothing saved.")
