from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

URL = "https://blox-fruits.fandom.com/wiki/Stock"

cache = {
    "data": [],
    "last_update": 0
}

def obtener_stock():
    r = requests.get(URL, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    frutas = []
    for li in soup.select("li"):
        texto = li.get_text(strip=True)
        if "Fruit" in texto:
            frutas.append(texto.replace(" Fruit", ""))

    return frutas

@app.route("/stock")
def stock():
    ahora = time.time()

    # cache de 5 minutos (evita spam a la wiki)
    if ahora - cache["last_update"] > 300:
        cache["data"] = obtener_stock()
        cache["last_update"] = ahora

    return jsonify({
        "fruits": cache["data"],
        "count": len(cache["data"]),
        "updated": cache["last_update"]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)