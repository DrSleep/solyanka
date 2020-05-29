"""
Reproducing the results of https://drsleep.github.io/solyanka/Number-of-Citations-of-Papers-Awarded-at-CVPR-Conferences/
"""

import argparse
import logging
import pandas as pd
import pickle
import numpy as np
import time
from pathlib import Path
from pprint import pprint

from get_citations_from_scholar import (
    get_citations_count_from_screen,
    paste_and_search,
)
from parse_raw_data import create_dataframe_frow_raw_data
from plot_data import plot_bar, plot_box, plot_scatter
from raw_data import (
    LH_prize_raw,
    best_paper_raw,
    best_honorable_mention_raw,
    best_student_paper_raw,
)


def get_arguments():
    parser = argparse.ArgumentParser(description="CVPR Awards Data Config")
    parser.add_argument(
        "--paper-to-citations-file-path",
        type=Path,
        default=Path("./paper_to_citations.dict"),
        help="Path to the dictionary of type (paper: number-of-citations)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        default=False,
        help="If the dictionary file exists, whether to overwrite it",
    )
    return parser.parse_args()


def main():
    args = get_arguments()
    logger = logging.getLogger(__name__)
    datasets = {
        "Longuet-Higgins": LH_prize_raw,
        "Best Paper": best_paper_raw,
        "Best Student Paper": best_student_paper_raw,
        "Honorable Mention Paper": best_honorable_mention_raw,
    }
    dataframes = []
    for award, data in datasets.items():
        dataframe = create_dataframe_frow_raw_data(raw_data=data)
        dataframe["Award"] = award
        dataframes.append(dataframe)
    dataframe = pd.concat(dataframes).reset_index()
    del datasets, dataframes

    logger.info(
        """
    Are there any papers that were recognised as best,
    and ten years later were also awarded the Longuet-Higgins (LH) Prize?
    """
    )
    LH_dataframe = dataframe.loc[
        dataframe.Award == "Longuet-Higgins",
    ]
    not_LH_dataframe = dataframe.loc[
        dataframe.Award != "Longuet-Higgins",
    ]
    LH_in_best_paper = LH_dataframe.Paper.isin(not_LH_dataframe.Paper)
    if any(LH_in_best_paper):
        (indices,) = np.where(LH_in_best_paper)
        for index in indices:
            logger.info("In LH")
            pprint(LH_dataframe.loc[index].values)

            logger.info("In BP")
            pprint(
                not_LH_dataframe.loc[
                    not_LH_dataframe.Paper == LH_dataframe.loc[index, "Paper"]
                ].values
            )

    if args.paper_to_citations_file_path.is_file() and not args.overwrite:
        with open(args.paper_to_citations_file_path, "rb") as f:
            paper_to_citations = pickle.load(f)
        logger.info(
            f"Loaded citations data from {args.paper_to_citations_file_path} "
            f"with total of {len(paper_to_citations)} entries"
        )
    else:
        logger.info("Creating empty citations dictionary")
        paper_to_citations = dict()

    logger.info(
        """
    This step may require access to the Google Scholar search page.
    Make sure the page is visible on your screen and you configured the settings in `get_citations_from_scholar.py`.
    """
    )
    any_citation_updates = False
    for i in range(len(dataframe)):
        paper = dataframe.loc[i, "Paper"]
        if paper not in paper_to_citations:
            logger.info(f"Looking up citations count for {paper}")
            search_query = paper + " " + dataframe.loc[i, "Authors"]
            paste_and_search(input_text=search_query)
            time.sleep(1)  # Allow the webpage to load
            paper_to_citations[paper] = get_citations_count_from_screen()
            time.sleep(10)  # Do not trigger the captcha
            any_citation_updates = True
        dataframe.loc[i, "Cites"] = paper_to_citations[paper]
    if args.overwrite or any_citation_updates:
        with open(args.paper_to_citations_file_path, "wb") as f:
            pickle.dump(paper_to_citations, f)
        logger.info(
            f"Saved citations data to {args.paper_to_citations_file_path} "
            f"with total of {len(paper_to_citations)} entries"
        )

    # As the size variable, we will simply take the log10 of the number of citations
    dataframe["Size"] = dataframe.loc[:, "Cites"].apply(np.log10)
    logger.info("Creating the scatterplot")
    plot_scatter(
        data_frame=dataframe,
        x="Year",
        y="Cites",
        symbol="Award",
        color="Award",
        size="Size",
        hover_name="Paper",
        hover_data={"Size": False, "Authors": True},
        log_y=True,
        range_y=[8, max(dataframe.Cites) * 2.5],
        height=700,
        labels={"Cites": "Number of Citations", "Year": "Year of Award"},
        template="simple_white",
        save_file=Path("./scatter.html"),
    )
    logger.info("Creating the boxplot")
    plot_box(
        data_frame=dataframe,
        x="Award",
        y="Cites",
        points="all",
        color="Award",
        hover_name="Paper",
        hover_data={"Size": False, "Authors": True, "Year": True},
        log_y=True,
        height=800,
        labels={"Cites": "Number of Citations", "Award": "Type of Award"},
        template="simple_white",
        save_file=Path("./boxplot.html"),
    )
    logger.info("Creating the barplot")
    dataframe_by_award = dataframe.groupby("Award").aggregate(sum).reset_index()
    dataframe_by_award.Size = dataframe_by_award.loc[:, "Cites"].apply(np.log10)
    dataframe_by_award.sort_values(by="Cites", inplace=True)
    plot_bar(
        data_frame=dataframe_by_award,
        x="Award",
        y="Cites",
        color="Award",
        hover_data={"Size": False, "Year": False},
        height=800,
        labels={"Cites": "Total number of Citations", "Award": "Type of Award"},
        template="simple_white",
        save_file=Path("./barplot.html"),
    )


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s :: %(levelname)s :: %(name)s :: %(message)s",
        level=logging.INFO,
    )
    main()
