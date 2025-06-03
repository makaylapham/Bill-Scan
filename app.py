import json
from flask import Flask, jsonify, request, abort
from http import HTTPStatus
from datetime import datetime
import uuid

app = Flask(__name__)

# In-memory storage (in a real app, this would be a database)
users = {}  # Store user information
transactions = {}  # Store transaction history
point_rules = {
    'default_rate': 1,  # 1 point per dollar by default
    'partner_rates': {
        'partner1': 2,  # 2 points per dollar for partner1
        'partner2': 1.5  # 1.5 points per dollar for partner2
    }
}

def calculate_points(amount, partner_id):
    """Calculate points based on transaction amount and partner rules"""
    rate = point_rules['partner_rates'].get(partner_id, point_rules['default_rate'])
    return int(amount * rate)

@app.route('/users', methods=['POST'])
def create_user():
    """Create a new user account"""
    if not request.is_json:
        abort(HTTPStatus.BAD_REQUEST, description="Content-Type must be application/json")
    
    data = request.get_json()
    required_fields = ['name', 'email']
    if not all(field in data for field in required_fields):
        abort(HTTPStatus.BAD_REQUEST, 
              description=f"Missing required fields. Required fields are: {', '.join(required_fields)}")
    
    user_id = str(uuid.uuid4())
    user = {
        'id': user_id,
        'name': data['name'],
        'email': data['email'],
        'points_balance': 0,
        'created_at': datetime.utcnow().isoformat()
    }
    
    users[user_id] = user
    return jsonify(user), HTTPStatus.CREATED

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get user details including points balance"""
    user = users.get(user_id)
    if user is None:
        abort(HTTPStatus.NOT_FOUND, description=f"User with ID {user_id} not found")
    return jsonify(user)

@app.route('/transactions', methods=['POST'])
def record_transaction():
    """Record a new transaction and update user points"""
    if not request.is_json:
        abort(HTTPStatus.BAD_REQUEST, description="Content-Type must be application/json")
    
    data = request.get_json()
    required_fields = ['user_id', 'partner_id', 'amount', 'transaction_reference']
    if not all(field in data for field in required_fields):
        abort(HTTPStatus.BAD_REQUEST, 
              description=f"Missing required fields. Required fields are: {', '.join(required_fields)}")
    
    user_id = data['user_id']
    if user_id not in users:
        abort(HTTPStatus.NOT_FOUND, description=f"User with ID {user_id} not found")
    
    # Calculate points for the transaction
    points_earned = calculate_points(data['amount'], data['partner_id'])
    
    # Create transaction record
    transaction_id = str(uuid.uuid4())
    transaction = {
        'id': transaction_id,
        'user_id': user_id,
        'partner_id': data['partner_id'],
        'amount': data['amount'],
        'points_earned': points_earned,
        'transaction_reference': data['transaction_reference'],
        'timestamp': datetime.utcnow().isoformat()
    }
    
    # Update user's points balance
    users[user_id]['points_balance'] += points_earned
    
    # Store transaction
    transactions[transaction_id] = transaction
    
    response = {
        'transaction': transaction,
        'user_points_balance': users[user_id]['points_balance']
    }
    
    return jsonify(response), HTTPStatus.CREATED

@app.route('/transactions/user/<user_id>', methods=['GET'])
def get_user_transactions(user_id):
    """Get all transactions for a specific user"""
    if user_id not in users:
        abort(HTTPStatus.NOT_FOUND, description=f"User with ID {user_id} not found")
    
    user_transactions = [
        trans for trans in transactions.values()
        if trans['user_id'] == user_id
    ]
    
    return jsonify(user_transactions)

@app.route('/points/rules', methods=['GET'])
def get_point_rules():
    """Get current point calculation rules"""
    return jsonify(point_rules)

@app.route('/points/rules/partner', methods=['POST'])
def update_partner_rate():
    """Update points rate for a specific partner"""
    if not request.is_json:
        abort(HTTPStatus.BAD_REQUEST, description="Content-Type must be application/json")
    
    data = request.get_json()
    required_fields = ['partner_id', 'points_rate']
    if not all(field in data for field in required_fields):
        abort(HTTPStatus.BAD_REQUEST, 
              description=f"Missing required fields. Required fields are: {', '.join(required_fields)}")
    
    point_rules['partner_rates'][data['partner_id']] = float(data['points_rate'])
    return jsonify(point_rules)

@app.errorhandler(HTTPStatus.NOT_FOUND)
def not_found_error(error):
    return jsonify({'error': str(error.description)}), HTTPStatus.NOT_FOUND

@app.errorhandler(HTTPStatus.BAD_REQUEST)
def bad_request_error(error):
    return jsonify({'error': str(error.description)}), HTTPStatus.BAD_REQUEST

if __name__ == '__main__':
    app.run(debug=True)