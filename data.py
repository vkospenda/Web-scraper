# Note to self: pri pandas dataframih lahko uporabljaš funkcijo query za pridobivanje specifičnih podatkov kot pri SQL bazi
# TODO: ugotovit kako praviln exctractat in uporabit 

import pandas as pd
import openpyxl
import os
import filecmp

excel = "nepremicnine_obala.xlsx"
df = pd.read_excel(excel)

max_cena = 350000

def replace_and_check(string):
    split = string.split(" ")
    split[0] = split[0].replace(".", "")
    split[0] = split[0].replace(",", ".")
    return float(split[0])

df["Cene"] = df["Cene"].apply(replace_and_check)

# Specifičen data frame za: KOPER, <350000€, 3,4,5 sobno
spec_df = df[(df["Mesta"] == "KOPER") & (df["Cene"] < max_cena) & ((df["Število sob"] == "3-sobno") | (df["Število sob"] == "4-sobno") | (df["Število sob"] == "5 in večsobno"))]
# Primerjava med datotekami
# TODO: reši primerjavo med datotekami
if os.path.isfile("kp_nep.xlsx"):
    print("kp_nep.xlsx obstaja")
    spec_df.to_excel("kp_nep-temp.xlsx")
    # Odprem excel kot data frame in naredim primerjavo med data frami
    original_df = pd.read_excel("kp_nep.xlsx")
    comparing_df = pd.read_excel("kp_nep-temp.xlsx")

    comparing_df = comparing_df[original_df.columns]
    original_df.reset_index(drop=True, inplace=True)
    comparing_df.reset_index(drop=True, inplace=True)

    print(original_df.index)
    print(comparing_df.index)    
    
    comparison = original_df.compare(spec_df)

    # Primerjam že obstoječ excel z začasnim. Če sta po vsebini enaka, začasni excel izbrišem
    if comparison.empty:
        print("Datoteki sta enaki, brišem kp_nep-temp.xlsx")
        os.remove("kp_nep-temp.xlsx")
    # Če excela nista enaka, prepišem novo vsebino in temp izbrišem
    else:
        print("Datoteki nista enaki, prepisujem novo vsebino")
        spec_df.to_excel("kp_nep.xlsx")
        os.remove("kp_nep-temp.xlsx")
else:
    spec_df.to_excel("kp_nep.xlsx")