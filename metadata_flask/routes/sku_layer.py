from flask import jsonify,request,Blueprint
from metadata_flask.db.models import Connection_manger
import json

s_layer = Blueprint("sku_layer", __name__, url_prefix="/")
sku_data = []

# Function to insert SKU data into the database
def insert_sku_data(sku, name, location, department, category, subcategory):
    conn = Connection_manger()
    conn.c.execute('''INSERT INTO sku_data (SKU, Name, Location, Department, Category, SubCategory) VALUES (?, ?, ?, ?, ?, ?)''', (sku, name, location, department, category, subcategory))
    conn.conn.commit()
    conn.conn.close()

@s_layer.route('/api/v1/sku', methods=['POST'])
def add_sku_data():
    data = request.json["data"]
    for sku in data:
        sku_data.append(sku)
        insert_sku_data(sku['SKU'], sku['Name'], sku['Location'], sku['Department'], sku['Category'],
                        sku['SubCategory'])
    return jsonify(request.json), 201

@s_layer.route('/api/v1/sku', methods=['GET'])
def get_sku_data():
    conn = Connection_manger()
    json_response = []
    result = conn.c.execute('''SELECT * FROM sku_data''')
    response = result.fetchall()
    conn.conn.close()
    for item in response:
        json_response.append(
            {"SKU": item[1],"Name":item[2],"Location":item[3],"Department": item[4], "Category": item[5], "SubCategory": item[6]}, )
    return jsonify(json_response)

@s_layer.route('/api/v1/query', methods=['POST'])
def query_sku_data():
    conn = Connection_manger()
    query_metadata = request.json['input']
    # Construct the SQL query based on the provided metadata
    response = []
    for item in query_metadata:
        Location = item["Location"]
        Department = item["Department"]
        Category = item["Category"]
        SubCategory = item["SubCategory"]
        conn.c.execute('SELECT * FROM sku_data WHERE Location = ? AND Department = ? AND Category = ? AND SubCategory = ?', (Location, Department, Category, SubCategory))
        matching_skus = conn.c.fetchall()
        if matching_skus:
            for match in matching_skus:
                response.append({"SKU":match[1],"Name":match[2],"Location":match[3],"Department":match[4],
                                 "Category":match[5],"SubCategory":match[6]})
        else:
            conn.conn.close()
            return jsonify({'message': 'No matching rows in sku_data rows found'})
    # Close the connection
    conn.conn.close()
    return jsonify(response)
