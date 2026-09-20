from pathlib import Path

from assessment_pipeline.parsers.xlsx_parser import (
    XlsxParser,
)

xlsx = Path(
    "../DESPINASSE HELENE_80982_assignsubmission_file/"
    "Managing with AI task 1.xlsx"
)

parser = XlsxParser()

text = parser.extract_text(xlsx)

print(
    f"Characters: {len(text)}"
)

print()
print(text[:1000])
