import logging
import subprocess
import tempfile
from pathlib import Path

from pipeline.config import CHECKSTYLE_JAR, CHECKSTYLE_CFG

log = logging.getLogger(__name__)


def passes_checkstyle(source: str) -> bool:
    with tempfile.TemporaryDirectory() as tmpdir:
        java_file = Path(tmpdir) / "Check.java"
        java_file.write_text(source, encoding="utf-8")
        result = subprocess.run(
            ["java", "-jar", CHECKSTYLE_JAR, "-c", CHECKSTYLE_CFG, str(java_file)],
            capture_output=True,
            timeout=30,
        )
    return result.returncode == 0
