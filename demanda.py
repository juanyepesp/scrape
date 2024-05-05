import pandas as pd

df = pd.read_csv("tucarro.csv")

nombres = df["Nombre"].str.lower()

marcas = []

for n in nombres:
    n = n.split(" ")[0]
    if n not in marcas and n != "":
        marcas.append(n)

# demanda = {
#     'audi': 300,
#     'toyota': 500,
#     'mercedes-benz': 250,
#     'suzuki': 200,
#     'subaru': 150,
#     'mazda': 300,
#     'kia': 400,
#     'bmw': 250,
#     'ford': 450,
#     'mercedes': 200,
#     'nissan': 400,
#     'volvo': 150,
#     'hyundai': 500,
#     'byd': 100,
#     'mini': 100,
#     'renault': 300,
#     'dodge': 150,
#     'land': 100,
#     'jeep': 200,
#     'lexus': 150,
#     'grand': 100,
# }

depreciacion = {
    'audi': 0.12,
    'toyota': 0.10,
    'mercedes-benz': 0.15,
    'suzuki': 0.08,
    'subaru': 0.09,
    'mazda': 0.11,
    'kia': 0.09,
    'bmw': 0.14,
    'ford': 0.10,
    'mercedes': 0.15,
    'nissan': 0.10,
    'volvo': 0.12,
    'hyundai': 0.09,
    'byd': 0.07,
    'mini': 0.13,
    'renault': 0.08,
    'dodge': 0.11,
    'land': 0.14,
    'jeep': 0.12,
    'lexus': 0.13,
    'grand': 0.07,
}

df["Depreciacion"] = df["Nombre"].str.lower().apply(lambda x: depreciacion.get(x.split(" ")[0], 0.10))

df["Referencia"] = df["Nombre"].str.lower().apply(lambda x: x.split(" ")[0])

df.to_csv("tucarro+demanda+depreciacion.csv", index=False)


