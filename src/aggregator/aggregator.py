import pandas as pd 
import os
from io import StringIO
import json


# Assign directory
RAW_DIRECTORY = r"C:\\Repositorios\\f1-analysis\\data\\raw"

AGG_DIRECTORY = r"C:\\Repositorios\\f1-analysis\\data\\aggregated"

# filenames_dict = {
#     "resultados" : {
#          "patterns" :["Pos", "Piloto", "Puntos.csv"]
#                     }
# }

with open("src\\aggregator\\aggregator_config.json") as f:
    config = json.load(f)
    print(config)

 
# Iterate over files in directory
for folder in os.listdir(RAW_DIRECTORY):
    # check if is file
    for file in os.listdir(os.path.join(RAW_DIRECTORY, folder)):
        for filename, configs in config.items():
            if all(pattern in file for pattern in configs["patterns"]):
                df = pd.read_csv(os.path.join(RAW_DIRECTORY, folder, file))
                df["Season"] = int(folder)
                if "N.º" in df.columns:
                    df = df.drop(columns=["N.º"])
                new_cols=[]    
                i=1    
                for column in df.columns:
                    if column not in configs["fix_cols"]:
                        column=str(i)
                        i+=1
                    new_cols.append(column)
                df.columns=new_cols
                print(df.head())
                if os.path.exists(f"{AGG_DIRECTORY}/{filename}.csv"):
                    old_df = pd.read_csv(f"{AGG_DIRECTORY}/{filename}.csv")
                    new_df = pd.concat([old_df, df], axis=0, join='outer')
                    new_df.drop_duplicates(inplace=True)
                    new_df.to_csv(f"{AGG_DIRECTORY}/{filename}.csv", mode="w", index=False, header=True)
                else:
                    df.to_csv(f"{AGG_DIRECTORY}/{filename}.csv", mode="w", index=False, header=True)
 
    print()