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
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        products_list = []

        for product in root.findall("product"):
            products_list.append({
                "product_id": product.findtext("PRODUCTID", default=""),
                "name": product.findtext("name", default=""),
                "description": product.findtext("description", default=""),
                "color": product.findtext("color", default=""),
                "size": product.findtext("size", default=""),
                "price": product.findtext("price", default=""),
                "regular_price": product.findtext("regular_price", default=""),
                "availability": product.findtext("availability", default=""),
                "image": product.findtext("image", default=""),
                "url": product.findtext("url", default=""),
                "category_name": product.findtext("category_name", default="")
            })

        return jsonify(products_list)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
