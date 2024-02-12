# About this project

If you need to use CapitalIQ for M&A transaction data but do not like the outdated and slow interface, maybe give Python a try if you have access to WRDS. You can save and run your favorite searches quickly and easily.

ciq_transactions.py - showcasing how to use complex SQL instructions to pull and combine data across multiple databases, deal with duplicates, and do basic filter and sort operations.

The code was written to run on JupyterHub on WRDS. If you want to run the code in a different setting, extra setups and tweaks may be required.

To learn more about WRDS APIs, please visit [the official WRDS github](https://github.com/wharton/wrds/) and [this short tutorial](https://matteocourthoud.github.io/post/wrds/).

# To-do list
- [ ] Support original python (i.e. no Jupyter Notebook required)
- [ ] Explore WRDS's SAS data source and wrds2pg package (h/t https://github.com/iangow/wrds_pg)
