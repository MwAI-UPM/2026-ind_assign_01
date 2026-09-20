from pathlib import Path

from assessment_pipeline.parsers.pdf_parser import (
    PdfParser,
)

pdf = Path(
    "../GOÑI OTAZU MIKEL_80964_assignsubmission_file/"
    "Tasks1-5_Mikel_Goni/"
    "Tasks1-5/"
    "Task 1 Report.pdf"
)

parser = PdfParser()

text = parser.extract_text(pdf)

print(
    f"Pages: {parser.get_page_count(pdf)}"
)

print(
    f"Characters: {len(text)}"
)

print()
print(text[:1000])
