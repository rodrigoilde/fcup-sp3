"""Generate ARX-compatible hierarchy CSVs for the Adult dataset.

Each output file has one row per leaf value; columns left-to-right are
generalisation levels (level 0 = original value, last level = '*').

Run:  python3 scripts/build_hierarchies.py
"""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "hierarchies"
OUT.mkdir(parents=True, exist_ok=True)


def write(name: str, rows: list[list[str]]) -> None:
    path = OUT / name
    with path.open("w", newline="", encoding="utf-8") as fh:
        csv.writer(fh, delimiter=";").writerows(rows)
    print(f"wrote {path.relative_to(ROOT)}  leaves={len(rows)} levels={len(rows[0])}")


# --- age ---------------------------------------------------------------------
# 5 levels: raw -> 5yr bin -> 10yr bin -> 20yr bin -> *
def age_rows() -> list[list[str]]:
    rows = []
    for a in range(17, 91):
        b5 = f"[{(a // 5) * 5}-{(a // 5) * 5 + 4}]"
        b10 = f"[{(a // 10) * 10}-{(a // 10) * 10 + 9}]"
        if a < 20:
            b20 = "[0-19]"
        elif a < 40:
            b20 = "[20-39]"
        elif a < 60:
            b20 = "[40-59]"
        elif a < 80:
            b20 = "[60-79]"
        else:
            b20 = "[80+]"
        rows.append([str(a), b5, b10, b20, "*"])
    return rows


# --- education ---------------------------------------------------------------
EDU_L1 = {
    "Preschool": "Primary", "1st-4th": "Primary", "5th-6th": "Primary",
    "7th-8th": "LowerSecondary", "9th": "LowerSecondary",
    "10th": "LowerSecondary", "11th": "LowerSecondary", "12th": "LowerSecondary",
    "HS-grad": "UpperSecondary",
    "Some-college": "HigherEd", "Assoc-acdm": "HigherEd",
    "Assoc-voc": "HigherEd", "Bachelors": "HigherEd",
    "Masters": "HigherEd", "Prof-school": "HigherEd", "Doctorate": "HigherEd",
}
EDU_L2 = {
    "Primary": "Compulsory", "LowerSecondary": "Compulsory",
    "UpperSecondary": "PostCompulsory", "HigherEd": "PostCompulsory",
}


def education_rows() -> list[list[str]]:
    return [[k, EDU_L1[k], EDU_L2[EDU_L1[k]], "*"] for k in EDU_L1]


# --- marital-status ----------------------------------------------------------
MARITAL_L1 = {
    "Married-civ-spouse": "Married", "Married-AF-spouse": "Married",
    "Married-spouse-absent": "Married",
    "Divorced": "NotMarried", "Never-married": "NotMarried",
    "Separated": "NotMarried", "Widowed": "NotMarried",
}


def marital_rows() -> list[list[str]]:
    return [[k, v, "*"] for k, v in MARITAL_L1.items()]


# --- native-country ----------------------------------------------------------
COUNTRY_REGION = {
    # North America
    "United-States": "NorthAmerica", "Canada": "NorthAmerica",
    "Mexico": "NorthAmerica", "Outlying-US(Guam-USVI-etc)": "NorthAmerica",
    # Central America & Caribbean
    "Cuba": "Caribbean", "Jamaica": "Caribbean", "Puerto-Rico": "Caribbean",
    "Dominican-Republic": "Caribbean", "Haiti": "Caribbean",
    "Trinadad&Tobago": "Caribbean",
    "Guatemala": "CentralAmerica", "Honduras": "CentralAmerica",
    "Nicaragua": "CentralAmerica", "El-Salvador": "CentralAmerica",
    # South America
    "Columbia": "SouthAmerica", "Ecuador": "SouthAmerica",
    "Peru": "SouthAmerica",
    # Western Europe
    "England": "WesternEurope", "Scotland": "WesternEurope",
    "Ireland": "WesternEurope", "France": "WesternEurope",
    "Germany": "WesternEurope", "Italy": "WesternEurope",
    "Portugal": "WesternEurope", "Holand-Netherlands": "WesternEurope",
    # Eastern / Southern Europe
    "Greece": "EastSouthEurope", "Hungary": "EastSouthEurope",
    "Poland": "EastSouthEurope", "Yugoslavia": "EastSouthEurope",
    # East / SE Asia
    "China": "EastAsia", "Hong": "EastAsia", "Taiwan": "EastAsia",
    "Japan": "EastAsia", "South": "EastAsia",
    "Philippines": "SoutheastAsia", "Vietnam": "SoutheastAsia",
    "Cambodia": "SoutheastAsia", "Laos": "SoutheastAsia",
    "Thailand": "SoutheastAsia",
    # South & West Asia
    "India": "SouthAsia", "Iran": "WestAsia",
}
REGION_CONTINENT = {
    "NorthAmerica": "Americas", "Caribbean": "Americas",
    "CentralAmerica": "Americas", "SouthAmerica": "Americas",
    "WesternEurope": "Europe", "EastSouthEurope": "Europe",
    "EastAsia": "Asia", "SoutheastAsia": "Asia",
    "SouthAsia": "Asia", "WestAsia": "Asia",
}


def country_rows() -> list[list[str]]:
    rows = []
    for c, region in COUNTRY_REGION.items():
        rows.append([c, region, REGION_CONTINENT[region], "*"])
    # '?' (missing) handled separately so ARX accepts the import
    rows.append(["?", "Unknown", "Unknown", "*"])
    return rows


# --- race / sex --------------------------------------------------------------
RACE_LEAVES = ["White", "Black", "Asian-Pac-Islander",
               "Amer-Indian-Eskimo", "Other"]
SEX_LEAVES = ["Female", "Male"]


def race_rows() -> list[list[str]]:
    return [[v, "*"] for v in RACE_LEAVES]


def sex_rows() -> list[list[str]]:
    return [[v, "*"] for v in SEX_LEAVES]


# --- workclass ---------------------------------------------------------------
WORKCLASS_L1 = {
    "Federal-gov": "Government", "Local-gov": "Government",
    "State-gov": "Government",
    "Private": "Private",
    "Self-emp-inc": "SelfEmployed", "Self-emp-not-inc": "SelfEmployed",
    "Without-pay": "NoIncome", "Never-worked": "NoIncome",
    "?": "Unknown",
}


def workclass_rows() -> list[list[str]]:
    return [[k, v, "*"] for k, v in WORKCLASS_L1.items()]


# --- occupation --------------------------------------------------------------
OCC_L1 = {
    "Exec-managerial": "WhiteCollar", "Prof-specialty": "WhiteCollar",
    "Adm-clerical": "WhiteCollar", "Sales": "WhiteCollar",
    "Tech-support": "WhiteCollar",
    "Craft-repair": "BlueCollar", "Machine-op-inspct": "BlueCollar",
    "Transport-moving": "BlueCollar", "Handlers-cleaners": "BlueCollar",
    "Farming-fishing": "BlueCollar",
    "Other-service": "Service", "Priv-house-serv": "Service",
    "Protective-serv": "Service",
    "Armed-Forces": "Other", "?": "Other",
}


def occupation_rows() -> list[list[str]]:
    return [[k, v, "*"] for k, v in OCC_L1.items()]


def main() -> None:
    write("age.csv", age_rows())
    write("education.csv", education_rows())
    write("marital-status.csv", marital_rows())
    write("native-country.csv", country_rows())
    write("race.csv", race_rows())
    write("sex.csv", sex_rows())
    write("workclass.csv", workclass_rows())
    write("occupation.csv", occupation_rows())


if __name__ == "__main__":
    main()
