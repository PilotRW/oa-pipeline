import pandas as pd
from io import BytesIO


async def parse_csv(file) -> pd.DataFrame:
    content = await file.read()

    df = pd.read_csv(
        BytesIO(content)
    )

    return df