import pandas as pd
import openpyxl

excel = "nepremicnine_obala.xlsx"
df = pd.read_excel(excel)

def replace(string):
    split = string.split(" ")
    split[0] = split[0].replace(".", "")
    split[0] = split[0].replace(",", ".")
    return split[0]

# stringe pretvorim v številke, kjer je to potrebno
# for i in df["Cene"]:
#     split_str = i.split(" ")
#     split_str[0] = split_str[0].replace(".", "")
#     split_str[0] = split_str[0].replace(",", ".")
df["Cene"] = df["Cene"].apply(replace)
print(df["Cene"])

print(df)

# # Specifiečn meni za "KOPER"
# kp_df = df[df["Mesta"] == "KOPER" & df["Cene"] < 350000]