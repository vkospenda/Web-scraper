# Note to self: pri pandas dataframih lahko uporabljaš funkcijo query za pridobivanje specifičnih podatkov kot pri SQL bazi
# TODO: ugotovit kako praviln exctractat in uporabit 

import pandas as pd
import openpyxl
import os
import filecmp

# excel = "nepremicnine_obala.xlsx"
# df = pd.read_excel(excel)

max_cena = 350000

def compare_condition(df1, df2):
    # Najprej dodam končnice, da bom v združenem df ločil podatke
    df1 = df1.add_suffix("_1")
    df2 = df2.add_suffix("_2")

    # Ponastavim indekse obeh datafrejmov zato da jih da prilepi df2 zraven df1
    df1.reset_index(drop=True, inplace=True)
    df2.reset_index(drop=True, inplace=True)

    combined_df = pd.concat([df1, df2], axis=1)

    #Najdemo spremenjene vrstice
    changed_rows = combined_df[(combined_df["Cena_1"] != combined_df["Cena_2"])]

    # Če sta podobni, bo subset changed_rows prazen
    if changed_rows.empty:
        return True
    else:
        return False

def replace_and_check(string):
    split = string.split(" ")
    split[0] = split[0].replace(".", "")
    split[0] = split[0].replace(",", ".")
    return float(split[0])

def execute_replace(df):
    df["Cena"] = df["Cena"].apply(replace_and_check)


def execute_comparison(df_for_query):
    # Specifičen data frame za: KOPER, <350000€, 3,4,5 sobno
    spec_df = df_for_query[(df_for_query["Mesto"] == "KOPER") & (df_for_query["Cena"] < max_cena) & ((df_for_query["Število sob"] == "3-sobno") | (df_for_query["Število sob"] == "4-sobno") | (df_for_query["Število sob"] == "5 in večsobno"))]

    # Primerjava med datotekami
    if os.path.isfile("kp_nep.xlsx"):
        print("kp_nep.xlsx obstaja, opravljam primerjavo")

        # Odprem excel kot data frame in naredim primerjavo med data frami
        original_df = pd.read_excel("kp_nep.xlsx")
        #comparing_df = pd.read_excel("kp_nep-temp.xlsx")

        # Primerjam že obstoječ excel z začasnim. Če sta po vsebini enaka, začasni excel izbrišem
        if compare_condition(original_df, spec_df):
            print("Datoteki sta enaki")

        # Če excela nista enaka, prepišem novo vsebino in temp izbrišem
        else:
            print("Datoteki nista enaki, prepisujem novo vsebino")
            spec_df.to_excel("kp_nep.xlsx", index=False)
    else:
        print("kp_nep.xlsx ne obstaja, zapisujem")
        spec_df.to_excel("kp_nep.xlsx", index=False)

# if __name__ == "__main__":
#     execute_replace(df_for_query)
#     execute_comparison()