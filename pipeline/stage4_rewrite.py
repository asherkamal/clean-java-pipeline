import logging
import re

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

from pipeline.config import MODEL_ID, HF_TOKEN, SGCR_PROMPT

log = logging.getLogger(__name__)


def load_model():
    log.info("Loading %s with 4-bit quantisation...", MODEL_ID)
    bnb_cfg = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
    )
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, token=HF_TOKEN)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        quantization_config=bnb_cfg,
        device_map="auto",
        token=HF_TOKEN,
    )
    model.eval()
    return model, tokenizer


def sgcr_rewrite(source: str, model, tokenizer) -> str:
    messages = [{"role": "user", "content": SGCR_PROMPT.format(code=source)}]
    text     = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    inputs = tokenizer(text, return_tensors="pt").to(model.device)
    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=4096,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )
    generated = tokenizer.decode(
        output_ids[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True
    )
    fence_match = re.search(r"```(?:java)?\n(.*?)```", generated, re.DOTALL)
    return fence_match.group(1).strip() if fence_match else generated.strip()
