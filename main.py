
import requests
import xml.etree.ElementTree as ET
from flask import Flask, jsonify
import os

app = Flask(__name__)

XML_URL = "https://www.joyfashionhouse.com/rest-xml/get/linkwise"

@app.route("/")
def home():
    return "XML Scraper is running!"

@app.route("/products")
def get_products():
    try:
        response = requests.get(XML_URL, timeout=10)
        response.raise_for_status()
        tree = ET.ElementTree(ET.fromstring(response.content))
        root = tree.getroot()

        products = []
        for product in root.findall('product'):
            title = product.find('name').text if product.find('name') is not None else "No Title"
            price = product.find('price').text if product.find('price') is not None else "No Price"
            availability = product.find('availability').text if product.find('availability') is not None else "Unknown"
            link = product.find('deeplink').text if product.find('deeplink') is not None else "No Link"
            products.append({
                "title": title,
                "price": price,
                "availability": availability,
                "link": link
            })

        return jsonify(products)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)
