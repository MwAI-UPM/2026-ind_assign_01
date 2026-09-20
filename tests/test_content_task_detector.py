import json

from pathlib import Path

from assessment_pipeline.content_task_detector import (
    ContentTaskDetector,
)

data = json.loads(
    Path(
        "data/normalized/80951.json"
    ).read_text(
        encoding="utf-8",
    )
)

detector = ContentTaskDetector()

for document in data["documents"]:

    tasks = detector.detect_tasks(
        document["text_content"]
    )

    print(
        document["file_name"],
        sorted(tasks),
    )
