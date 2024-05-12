from flask import Blueprint, request
from flask import jsonify
from metadata_flask.db.models import Connection_manger
import json

m_layer = Blueprint("meta_layer", __name__, url_prefix="/")
metadata = []


# Function to insert metadata into the database
def insert_metadata(location, department, category, subcategory):
    conn = Connection_manger()
    conn.c.execute('''INSERT INTO metadata (Location, Department, Category, SubCategory) VALUES (?, ?, ?, ?)''', (location, department, category, subcategory))
    conn.conn.commit()
    conn.conn.close()

# Define endpoints for metadata
@m_layer.route('/api/v1/metadata', methods=['GET'])
def get_metadata():
    conn = Connection_manger()
    json_response = []
    result = conn.c.execute('''SELECT * FROM metadata''')
    response = result.fetchall()
    conn.conn.close()
    for item in response:
        json_response.append({"Location":item[1],"Department":item[2],"Category":item[3],"SubCategory":item[4]},)
    # Convert the list to JSON format
    return jsonify(json_response)

@m_layer.route('/api/v1/metadata', methods=['POST'])
def add_metadata():
    data = request.json['data']
    for meta in data:
        metadata.append(meta)
        insert_metadata(meta['Location'], meta['Department'], meta['Category'], meta['SubCategory'])
    return jsonify(request.json), 201

# Define endpoints for location, department, category, and subcategory
@m_layer.route('/api/v1/location/<string:location_id>/department', methods=['GET'])
def get_department_by_location(location_id):
    conn = Connection_manger()
    response = []
    conn.c.execute('''SELECT Department FROM metadata WHERE Location = ?''', (location_id,))
    departments = conn.c.fetchall()
    if departments:
        for item in departments:
            response.append({"Location":location_id,"Department":item[0]})
    else:
        conn.conn.close()
        return jsonify({'message': f'No Department found on this location - {location_id}'}), 404
    conn.c.close()
    return jsonify(response)

@m_layer.route('/api/v1/location/<string:location_id>/department/<string:department_id>/category', methods=['GET'])
def get_category_by_department(location_id, department_id):
    conn = Connection_manger()
    response = []
    conn.c.execute('SELECT Category FROM metadata WHERE Location = ? AND Department = ?', (location_id, department_id))
    categories = conn.c.fetchall()
    if categories:
        for item in categories:
            response.append({"Location":location_id,"Department":department_id,"Category":item[0]})
    else:
        conn.conn.close()
        return jsonify({'message': f'No categories found on this Department - {department_id}'}), 404
    conn.conn.close()
    return jsonify(response)

@m_layer.route('/api/v1/location/<string:location_id>/department/<string:department_id>/category/<string:category_id>/subcategory', methods=['GET'])
def get_subcategory_by_category(location_id, department_id, category_id):
    conn = Connection_manger()
    response = []
    conn.c.execute('SELECT SubCategory FROM metadata WHERE Location = ? AND Department = ? AND Category = ?', (location_id, department_id, category_id))
    subcategories = conn.c.fetchall()
    if subcategories:
        for item in subcategories:
            response.append({"Location":location_id,"Department":department_id,"Category":category_id,"SubCategory":item[0]})
    else:
        conn.conn.close()
        return jsonify({'message': f'No Subcategories found on Category - {category_id}'}), 404
    conn.conn.close()
    return jsonify(response)

@m_layer.route('/api/v1/location/<string:location_id>/department/<string:department_id>/category/<string:category_id>/subcategory/<string:subcategory_id>', methods=['GET'])
def get_subcategory(location_id, department_id, category_id, subcategory_id):
    conn = Connection_manger()
    response = []
    conn.c.execute('SELECT * FROM metadata WHERE Location = ? AND Department = ? AND Category = ? AND SubCategory = ?', (location_id, department_id, category_id, subcategory_id))
    subcategory = conn.c.fetchall()
    if subcategory:
        for item in subcategory:
            response.append({"Location":item[1],"Department":item[2],"Category":item[3],"SubCategory":item[4]})
    else:
        conn.conn.close()
        return jsonify({'message': f'No Subcategory found - {subcategory_id}'}), 404
    conn.conn.close()
    return jsonify(response)

