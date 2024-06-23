# Note to self: pri pandas dataframih lahko uporabljaš funkcijo query za pridobivanje specifičnih podatkov kot pri SQL bazi
# TODO: ugotovit kako praviln exctractat in uporabit 

import pandas as pd
import openpyxl

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
spec_df.to_excel("kp_nep.xlsx")