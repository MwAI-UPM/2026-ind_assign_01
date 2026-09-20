from pathlib import Path

from assessment_pipeline.parsers.docx_parser import (
    DocxParser,
)

docx = Path(
    "../VAN LOMMEL JOOS_80986_assignsubmission_file/"
    "TASK1.docx"
)

parser = DocxParser()

text = parser.extract_text(docx)

print(
    f"Characters: {len(text)}"
)

print()
print(text[:1000])
