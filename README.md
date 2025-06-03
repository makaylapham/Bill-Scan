# Purchase Tracking API

A Flask-based REST API for tracking purchases and automatically managing user points. Partners can send real-time transaction data to credit points to users' accounts.

## Features

- User account management
- Real-time transaction processing
- Automatic point calculation
- Partner-specific point rates
- Transaction history tracking

## Setup

1. Create a virtual environment (optional but recommended):
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Users

#### Create a new user
```
POST /users
Content-Type: application/json

{
    "name": "John Doe",
    "email": "john@example.com"
}
```

#### Get user details
```
GET /users/<user_id>
```

### Transactions

#### Record a new transaction
```
POST /transactions
Content-Type: application/json

{
    "user_id": "user_id_here",
    "partner_id": "partner1",
    "amount": 100.00,
    "transaction_reference": "ORDER123"
}
```

#### Get user's transaction history
```
GET /transactions/user/<user_id>
```

### Points Rules

#### Get current point rules
```
GET /points/rules
```

#### Update partner point rate
```
POST /points/rules/partner
Content-Type: application/json

{
    "partner_id": "partner1",
    "points_rate": 2.5
}
```

## Point Calculation Rules

- Default rate: 1 point per dollar
- Partner-specific rates:
  - partner1: 2 points per dollar
  - partner2: 1.5 points per dollar

## Example Usage

1. Create a new user:
```bash
curl -X POST http://localhost:5000/users \
    -H "Content-Type: application/json" \
    -d '{
        "name": "John Doe",
        "email": "john@example.com"
    }'
```

2. Record a purchase:
```bash
curl -X POST http://localhost:5000/transactions \
    -H "Content-Type: application/json" \
    -d '{
        "user_id": "USER_ID",
        "partner_id": "partner1",
        "amount": 100.00,
        "transaction_reference": "ORDER123"
    }'
```

3. Check user's points:
```bash
curl http://localhost:5000/users/USER_ID
```

## Development Notes

This is a development version using in-memory storage. For production use, consider:
- Adding a proper database
- Implementing authentication
- Adding input validation
- Adding rate limiting
- Adding logging and monitoring 