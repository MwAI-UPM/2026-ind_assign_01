# csv_to_md.py

from pathlib import Path
import pandas as pd
import sys

csv_file = Path(sys.argv[1])

df = pd.read_csv(csv_file)

print(
    df.to_markdown(
        index=False
    )
)
