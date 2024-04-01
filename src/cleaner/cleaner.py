import pandas as pd 
import os
from io import StringIO
import json


AGG_DIRECTORY = r"C:\\Repositorios\\f1-analysis\\data\\aggregated"

CLEAN_DIRECTORY = r"C:\\Repositorios\\f1-analysis\\data\\clean"

with open("src\\cleaner\\cleaner_config.json") as f:
    config = json.load(f)
    print(config)


for filename, configs in config.items():

    df = pd.read_csv(os.path.join(AGG_DIRECTORY,f"{filename}.csv"))

    if "cols_tonumeric" in configs:
        for col in configs["cols_tonumeric"]:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df = df.dropna(subset=[col])
            df[col] = df[col].astype('int')

    if "fix_cols" in configs:    

        df = df.melt(id_vars=configs["fix_cols"], 
                var_name=configs["var_name"], 
                value_name=configs["value_name"])
        
        df = df.dropna(subset=[configs["value_name"]]) 
        
    if "cols_id" in configs:
        for col, ids in configs["cols_id"].items():
            df[col] = df[ids].astype(str).apply(lambda x: "_".join(x), axis=1)

    print(df.head())

    df.to_csv(os.path.join(CLEAN_DIRECTORY,f"{filename}.csv"), mode="w", index=False, header=True)

