import json

from pathlib import Path

from assessment_pipeline.task_splitter import (
    TaskSplitter,
)

data = json.loads(
    Path(
        "data/normalized/80951.json"
    ).read_text(
        encoding="utf-8",
    )
)

splitter = TaskSplitter()

for document in data["documents"]:

    sections = splitter.split(
        document["text_content"]
    )

    print()

    print(
        document["file_name"]
    )

    print(
        sorted(sections.keys())
    )

    for task_number, content in (
        sections.items()
    ):

        print(
            task_number,
            len(content),
        )
