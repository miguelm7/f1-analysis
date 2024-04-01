import pandas as pd 
import os
import requests 
from bs4 import BeautifulSoup
from io import StringIO
import argparse
import datetime

### PARSE ARGUMENTS ###
parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-l", "--last", action="store_true", help="extract data from last season")
group.add_argument("-r", "--range", help="extract data from a range of seasons")
group.add_argument("-y", "--year", help="extract data from a specific season")
group.add_argument("-a", "--all", action="store_true", help="extract data from al seasons")

# parser.add_argument("years", type=str,default=None, help="year or year range to extract. Eg: (2010 | 2010-2020)")
args = parser.parse_args()

if args.last:
    season_start = datetime.datetime.now().year
    season_end = season_start + 1
elif args.range:
    season_start = int(args.range.split("-")[0])
    season_end = int(args.range.split("-")[1])
elif args.year:
    season_start = int(args.year)
    season_end = season_start + 1
elif args.all:
    season_start = 1950
    season_end = datetime.datetime.now().year + 1
else:
    print("No valid arguments specified --> default extraction: last season")
    season_start = datetime.datetime.now().year
    season_end = season_start + 1

seasons = [i for i in range(season_start,season_end)]

print(f"Extacting seasons: {seasons}")

for season in seasons: 
    # get the response in the form of html
    wikiurl=f"https://es.wikipedia.org/wiki/Temporada_{season}_de_F%C3%B3rmula_1"
    table_class="wikitable sortable jquery-tablesorter"
    response=requests.get(wikiurl)
    # print(response.status_code)

    # parse data from the html into a beautifulsoup object
    soup = BeautifulSoup(response.text, 'html.parser')
    tables=soup.select('table',{'class':"wikitable"})

    for table in tables:
        if "class" in table.attrs:
            if table.attrs["class"]!=["wikitable"]:
                continue
        else:
            continue
        try:
            df=pd.read_html(StringIO(str(table)))
            # convert list to dataframe
            df=pd.DataFrame(df[0])
            # print(df.head())
            column_names = df.columns.astype(str)
            table_name = "_".join(column_names)
            # print(df.columns[0:3])
            directory = f"data/raw/{season}"
            if not os.path.exists(directory):
                os.makedirs(directory)
            df.to_csv(f"{directory}/{season}_{table_name}.csv",index=False)
        except Exception as e:
            print(f"No se pudo extraer la tabla: {e}")

    print(f"Finished loading season {season}")
