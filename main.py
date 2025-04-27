
from flask import Flask, jsonify
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)

XML_URL = "https://www.joyfashionhouse.com/rest-xml/get/linkwise"

@app.route("/")
def home():
    return "XML Scraper is running!"

@app.route("/products")
def products():
    try:
        response = requests.get(XML_URL)
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch XML"}), 500
        
        root = ET.fromstring(response.content)
        products = []

        for product in root.findall(".//product"):
            product_data = {child.tag: child.text for child in product}
            products.append(product_data)
        
        return jsonify(products)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
