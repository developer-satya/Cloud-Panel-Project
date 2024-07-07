from matplotlib.dviread import Page
from st_pages import hide_pages # type: ignore

hide_pages(
    [
        Page("pages/s3.py"),
     ]
)