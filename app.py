from flask import Flask, request, jsonify
from uuid import uuid4
from jsonschema import validate, ValidationError
import math

app = Flask(__name__)

# Local storage for receipts
receipts = {}

# Receipt schema
receipt_schema = {
    "type": "object",
    "required": ["retailer", "purchaseDate", "purchaseTime", "items", "total"],
    "properties": {
        "retailer": {
            "type": "string",
            "pattern": r"^[\w\s\-\&]+$"
        },
        "purchaseDate": {
            "type": "string",
            "format": "date"
        },
        "purchaseTime": {
            "type": "string",
            "format": "time"
        },
        "items": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["shortDescription", "price"],
                "properties": {
                    "shortDescription": {
                        "type": "string",
                        "pattern": r"^[\w\s\-]+$"
                    },
                    "price": {
                        "type": "string",
                        "pattern": r"^\d+\.\d{2}$"
                    }
                }
            }
        },
        "total": {
            "type": "string",
            "pattern": r"^\d+\.\d{2}$"
        }
    }
}

# Validate receipt
def validate_receipt(data):
    """
    Validates receipt according to schema included in API specifications.
    """
    try:
        validate(data, receipt_schema)
    except ValidationError:
        raise ValueError("The receipt is invalid.")

### ENDPOINTS ###

# Process receipts
@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    """
    Processes a receipt and returns its unique ID.
    """
    data = request.get_json()
    
    try:
        validate_receipt(data)
    except ValueError as e:
        return {
            'error': 'BadRequest',
            'message': str(e)
        }, 400

    # Generate random id
    receipt_id = str(uuid4())
    
    # Store receipt in local storage
    receipts[receipt_id] = data

    return jsonify({'id': receipt_id}), 200

# Get points
@app.route('/receipts/<string:id>/points', methods=['GET'])
def get_points(id):
    """
    Calculates and returns the point value for a given receipt.
    """
    if id not in receipts:
        return {
            'error': 'NotFound',
            'message': 'No receipt found for that ID.'
        }, 404

    points = 0

    # +1 point for every alphanumeric character in the retailer name
    for ch in receipts[id]['retailer']:
        if ch.isalnum():
            points += 1

    # +50 points if the total is a round dollar amount with no cents
    if receipts[id]['total'].endswith('.00'):
        points += 50

    # +25 points if the total is a multiple of '0.25'
    if (float(receipts[id]['total']) * 100) % 25 == 0:
        points += 25

    # +5 points for every two items on the receipt
    multiple_two = len(receipts[id]['items']) // 2
    points += (5 * multiple_two)

    # If the trimmed length of the item description is a multiple of 3, multiply the price by `0.2` and round up to the nearest integer. The result is the number of points earned
    for item in receipts[id]['items']:
        if len(item['shortDescription'].strip()) % 3 == 0:
            points += math.ceil(float(item['price']) * 0.2)
    
    # +6 points if the day in the purchase date is odd
    split_date = receipts[id]['purchaseDate'].split('-')
    if int(split_date[2]) % 2 != 0:
        points += 6

    # +10 points if the time of purchase is after 2:00pm and before 4:00pm
    split_time = receipts[id]['purchaseTime'].split(':')
    hour, minute = int(split_time[0]), int(split_time[1])
    if (hour == 14 and minute > 0) or (hour == 15):
        points += 10 

    return jsonify({'points': points}), 200


if __name__ == '__main__':
    app.run(debug=True)