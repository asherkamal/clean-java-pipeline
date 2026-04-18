import logging

from datasets import Dataset

from pipeline.config import OUTPUT_DIR, HF_REPO_ID, HF_TOKEN

log = logging.getLogger(__name__)


def save_and_push(rows: list[dict]) -> None:
    log.info("Saving %d rows to %s...", len(rows), OUTPUT_DIR)
    ds = Dataset.from_list(rows)
    ds.save_to_disk(OUTPUT_DIR)
    log.info("Saved to disk: %s", OUTPUT_DIR)
    if HF_REPO_ID:
        log.info("Pushing to HuggingFace Hub: %s", HF_REPO_ID)
        ds.push_to_hub(HF_REPO_ID, token=HF_TOKEN)
        log.info("Published at https://huggingface.co/datasets/%s", HF_REPO_ID)
