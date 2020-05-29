# Number of Citations of Papers Awarded at CVPR Conference

The source code to reproduce the results of [this blog post](https://drsleep.github.io/solyanka/Number-of-Citations-of-Papers-Awarded-at-CVPR-Conferences/).


## Installation

```
Ubuntu
Python>=3.6
pip3
```

To install the required python packages, execute `pip3 install -r requirements.txt`

To reproduce the results, simply run `python main.py`

## Structure

### raw_data(.py)

Raw datasets for each award with the name of the awardees, the title of the publication and the year of the award. All the data are from the Computer Vision Foundation [page](https://www.thecvf.com/).

### parse_raw_data.py

Creates pandas.DataFrame objects from the raw data.

### get_citations_from_scholar.py

(Semi-)automatically parses data from Google Scholar via controlling your mouse and the keyboard. You have to configure it based on your setup.

### plot_data.py

Utilities to create the plots as in the blog post.
