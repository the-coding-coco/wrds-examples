# Created and maintained by coco.lin at chicagobooth.edu
# 
# This code can be run on JupyterHub on WRDS' server. Copy the code below and past it to a Jupyter Notebook (.ipynb).
# Learn more and enter WRDS' JupyterHub via
#   https://wrds-www.wharton.upenn.edu/pages/support/programming-wrds/programming-python/jupyterhub-wrds/
#   if your organization provides access to WRDS.

import wrds
import html
import pandas as pd
from IPython.display import HTML
pd.set_option('display.max_colwidth', 50)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
conn = wrds.Connection()

css_style=""" <style>
td, th {
  text-align: left !important;
}
</style>"""

announceddate = "2018-01-01"
relcompanyname = "________" # fill the blank with the firm you want to search as buyer OR seller
comments_length = 750

# WRDS Databases involved:
# - https://wrds-www.wharton.upenn.edu/data-dictionary/ciq_transactions/
# - https://wrds-www.wharton.upenn.edu/data-dictionary/ciq_common/
# You can find tables and table descriptions on these pages.
# Feel free to go to https://wrds-www.wharton.upenn.edu/pages/about/data-vendors/sp-global-market-intelligence/#products
#   to explore other databases.

sql_str = """SELECT
    MAX(t.announceddate) as announceddate,
    MAX(CASE WHEN t.compreltotrans ~ 'Buyer' THEN t.relcompanyname END) AS buyer,
    MAX(CASE WHEN t.compreltotrans ~ 'Seller' THEN t.relcompanyname END) AS seller,
    MAX(t.tgtcompanyname) as tgtcompanyname, 
    MAX(r.country) as country,
    STRING_AGG(DISTINCT i.sicdescription, ', ') AS industries,
    MAX(t.transactionsize) as transactionsize,
    MAX(CASE WHEN LENGTH(t.comments) > {} THEN CONCAT(LEFT(t.comments, {}), ' ...') ELSE t.comments END) AS comments
    FROM ciq_transactions.wrds_transactions t
    INNER JOIN ciq_transactions.wrds_trans_advisors a ON t.transactionid = a.transactionid
    INNER JOIN ciq_common.ciqcompany c ON t.tgtcompanyid = c.companyid
    INNER JOIN ciq_common.ciqcountrygeo r ON c.countryid = r.countryid
    INNER JOIN ciq_common.ciqcompanyindustrytree it ON c.companyid = it.companyid
    INNER JOIN ciq_common.ciqindustrytosic i ON it.subtypeid = i.subtypeid
    WHERE t.announceddate > '{}' AND t.relcompanyname ~ '{}'
    -- to filter by advisor: AND a.advisorcompanyname ~ '_________'
    -- to filter by country/region: AND r.country ~ '________'
    GROUP BY t.transactionid
    ORDER BY announceddate DESC
    LIMIT 25
    """.format(comments_length, comments_length, announceddate, relcompanyname)

df = conn.raw_sql(sql_str)
HTML(css_style + df.to_html(escape=False).replace("$", "\\$")) # Jupyter Notebook regards $ as LaTeX symbol so be sure to escape it.
