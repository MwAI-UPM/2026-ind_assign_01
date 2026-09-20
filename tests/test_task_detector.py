from pathlib import Path

from assessment_pipeline.task_detector import (
    TaskDetector,
)

detector = TaskDetector()

examples = [
    "Task 1 Report.pdf",
    "Task_2_Map.pdf",
    "Task3.docx",
    "TASK4.pdf",
    "Task 5_Final_Report_AIDA.pdf",
    "Prompts of the tasks.pdf",
]

for name in examples:

    task = detector.detect(
        Path(name)
    )

    print(
        f"{name} -> {task}"
    )
