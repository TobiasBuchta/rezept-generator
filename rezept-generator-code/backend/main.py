from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import csv

# Gewichteter Zufallsalgorithmus
from algorithmus import gewichtetes_zufallsrezept

app = FastAPI()

# CORS für Frontend-Zugriff
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

DB_FILE = "rezepte.csv"


# -------------------------
# CSV dynamisch laden
# -------------------------
def lade_rezepte():
    rezepte = []
    with open(DB_FILE, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            rezepte.append(row)
    return rezepte


# -------------------------
# Neues Rezept dynamisch hinzufügen
# -------------------------
def add_rezept_dynamisch(row_dict):
    # 1) Header laden
    with open(DB_FILE, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=';')
        fieldnames = reader.fieldnames

    # 2) Fehlende Keys auffüllen
    for col in fieldnames:
        if col not in row_dict:
            row_dict[col] = ""

    # 3) Zeile anhängen
    with open(DB_FILE, 'a', newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
        writer.writerow(row_dict)


# -------------------------
# Zeile löschen über Index
# -------------------------
@app.delete("/delete/{row_index}")
def delete_rezept(row_index: int):
    with open(DB_FILE, newline='', encoding="utf-8") as f:
        reader = list(csv.DictReader(f, delimiter=';'))
        fieldnames = reader[0].keys() if reader else []

    if row_index < 0 or row_index >= len(reader):
        return {"msg": "Index ungültig"}

    del reader[row_index]

    with open(DB_FILE, 'w', newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(reader)

    return {"msg": "Zeile gelöscht"}


# -------------------------
# API Endpoints
# -------------------------

@app.get("/")
def root():
    return {"msg": "Backend läuft lokal!"}


@app.get("/all")
def alle_rezepte():
    return lade_rezepte()


@app.get("/columns")
def get_columns():
    with open(DB_FILE, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=';')
        return reader.fieldnames


@app.post("/add")
async def add_rezept(request: Request):
    data = await request.json()
    add_rezept_dynamisch(data)
    return {"msg": "OK"}


# -------------------------
# Gewichtetes Zufallsrezept
# -------------------------
@app.get("/zufall")
def zufall():
    rezepte = lade_rezepte()

    if not rezepte:
        return {
            "Rezept Name": "Keine Rezepte vorhanden",
            "Details": ""
        }

    return gewichtetes_zufallsrezept(rezepte)
