import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

urls = [
    "https://carros.tucarro.com.co/hibrido/",
    "https://carros.tucarro.com.co/hibrido/_Desde_49_NoIndex_True",
    "https://carros.tucarro.com.co/hibrido/_Desde_97_NoIndex_True",
    "https://carros.tucarro.com.co/hibrido/_Desde_145_NoIndex_True",
    "https://carros.tucarro.com.co/hibrido/_Desde_193_NoIndex_True",
]

scrape = []

for url in tqdm(urls, desc="Scraping URLs"):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    link_elements = soup.select("a[href]")
    urls = [link for link in link_elements if "articulo" in link["href"]]
    scrape.extend(urls)


df = pd.DataFrame(columns=["Nombre", "Precio", "Modelo", "Kilometraje", "Link"])


for current_url in tqdm(scrape, desc="Processing URLs"):
    response = requests.get(current_url["href"])
    soup = BeautifulSoup(response.text, "html.parser")

    nombre = soup.select_one("h1").text
    price = soup.select_one(".andes-money-amount__fraction").text
    price = int(price.replace(".", ""))
    info = soup.select_one(".ui-pdp-subtitle").text.split("|")
    modelo = info[0]
    kilometraje = info[1].split("·")[0].strip()
    link = current_url["href"]
    if link not in df["Link"].values:
        df = pd.concat([df, pd.DataFrame({"Nombre": [nombre], "Precio": [price], "Modelo": [modelo], "Kilometraje": [kilometraje], "Link": [link]})], ignore_index=True)


df.to_csv("tucarro.csv", index=False)
