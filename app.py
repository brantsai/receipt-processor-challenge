from flask import Flask, request, jsonify
from uuid import uuid4

app = Flask(__name__)

# Local storage for receipts
receipts = {}

### ENDPOINTS ###

# Process receipts
@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    data = request.get_json()
    
    # Generate random id
    receipt_id = str(uuid4())
    
    # Store receipt in local storage
    receipts[receipt_id] = data

    return jsonify({'id': receipt_id}), 201


if __name__ == '__main__':
    app.run(debug=True)