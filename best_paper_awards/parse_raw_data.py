"""Create Pandas.DataFrame objects from raw data"""

import pandas as pd
import re
from io import StringIO
from typing import List, Optional


def create_dataframe_frow_raw_data(
    raw_data: str,
    names: List[str] = ["Year", "Paper", "Authors"],
    sep: Optional[str] = "\t",
) -> pd.DataFrame:
    dataframe = pd.read_csv(
        filepath_or_buffer=StringIO(raw_data), sep=sep, names=names,
    )
    if "Paper" in names:
        # Keep only title of the paper within the quotation marks
        dataframe.loc[:, "Paper"] = dataframe.Paper.apply(
            lambda title: re.findall(pattern="^“(.*)”", string=title)[0]
        )
    return dataframe
