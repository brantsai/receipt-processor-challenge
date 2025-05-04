from flask import Flask, request, jsonify
from uuid import uuid4
from jsonschema import validate, ValidationError

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
    try:
        validate(data, receipt_schema)
    except ValidationError as e:
        raise ValueError(f"The receipt is invalid: {e.message}.")

### ENDPOINTS ###

# Process receipts
@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    data = request.get_json()
    
    try:
        validate_receipt(data)
    except ValueError as e:
        return {
            "error": "BadRequest",
            "message": f"{str(e)}. Please verify input."
        }, 400

    # Generate random id
    receipt_id = str(uuid4())
    
    # Store receipt in local storage
    receipts[receipt_id] = data

    return jsonify({'id': receipt_id}), 200

if __name__ == '__main__':
    app.run(debug=True)