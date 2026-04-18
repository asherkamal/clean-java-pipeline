import os
from pathlib import Path

CHECKSTYLE_JAR   = os.environ.get("CHECKSTYLE_JAR", "checkstyle.jar")
CHECKSTYLE_CFG   = str(Path(__file__).parent.parent / "checkstyle-config.xml")
MODEL_ID         = "Qwen/Qwen2.5-Coder-7B-Instruct"
OUTPUT_DIR       = "output_dataset"
MAX_OUTPUT_GB    = float(os.environ.get("MAX_OUTPUT_GB", 0))
MAX_OUTPUT_BYTES = int(MAX_OUTPUT_GB * 1024 ** 3)
HF_TOKEN         = os.environ.get("HF_TOKEN")
HF_REPO_ID       = os.environ.get("HF_REPO_ID", "")

SGCR_PROMPT = """\
You are a Java code style expert. Rewrite the following Java code following the Google Java Style Guide:
1. Add Javadoc comments to all public classes, interfaces, and methods
2. Ensure class/interface/enum names use UpperCamelCase
3. Ensure method and variable names use lowerCamelCase
4. Ensure constants use UPPER_SNAKE_CASE
5. Unify variable reassignment patterns for clarity
6. Do NOT change functionality or logic

Return ONLY the rewritten Java code with no explanation.

```java
{code}
```"""
