# LogParser

This repository contains python scripts for parsing logs of the sshd daemon.

* `logparser_pd.py` - parses logs of the sshd and writes the result to the `output/access_logs.xlsx` Excel file
* `logparser_pd_formatted.py` - parses logs of the sshd and writes the formated result to the `output/access_logs_formated.xlsx` Excel file
* `logparser_pd_formatted_geoip.py` - parses logs of the sshd, adds information about country, city, isp, latitude and longitude of that who accessed the server and writes the formated result to the `output/access_logs_formated_geoip.xlsx` Excel file
* `logparser_sql.py` - parses logs of the sshd and writes the result to the `output/access.db` SQLite database using SQLAlchemy Core
* `logparser_sql_orm.py` - parses logs of the sshd and writes the result to `output/access_orm.db` SQLite database using SQLAlchemy ORM