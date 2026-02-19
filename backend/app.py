"""
Telegram Mini App Backend API
Simple Flask server for the clicker game mini app
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)

# In-memory storage (use a real database in production)
users_data = {}


@app.route('/api/user', methods=['POST'])
def get_user():
    """Get or create a user."""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Invalid JSON'}), 400
        
        user_id = data.get('user_id')
        if not user_id:
            return jsonify({'error': 'user_id is required'}), 400
        
        # Create new user if doesn't exist
        if user_id not in users_data:
            users_data[user_id] = {
                'user_id': user_id,
                'first_name': data.get('first_name', 'User'),
                'username': data.get('username', 'unknown'),
                'balance': 0,
                'clicks': 0,
                'created_at': datetime.now().isoformat()
            }
        
        return jsonify(users_data[user_id])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/click', methods=['POST'])
def handle_click():
    """Process a user click and award coins."""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Invalid JSON'}), 400
        
        user_id = data.get('user_id')
        if not user_id:
            return jsonify({'error': 'user_id is required'}), 400
        
        if user_id not in users_data:
            return jsonify({'error': 'User not found'}), 404
        
        # Award 10 coins per click
        users_data[user_id]['clicks'] += 1
        users_data[user_id]['balance'] += 10
        
        return jsonify({
            'success': True,
            'clicks': users_data[user_id]['clicks'],
            'balance': users_data[user_id]['balance']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/withdraw', methods=['POST'])
def withdraw():
    """Withdraw coins from user balance."""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Invalid JSON'}), 400
        
        user_id = data.get('user_id')
        amount = data.get('amount', 100)
        
        if not user_id:
            return jsonify({'error': 'user_id is required'}), 400
        
        if user_id not in users_data:
            return jsonify({'error': 'User not found'}), 404
        
        if users_data[user_id]['balance'] < amount:
            return jsonify({'error': 'Insufficient balance'}), 400
        
        # Deduct from balance (in production, log this to a database)
        users_data[user_id]['balance'] -= amount
        
        return jsonify({
            'success': True,
            'message': f'Withdrawal of {amount} coins completed',
            'balance': users_data[user_id]['balance']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats', methods=['POST'])
def get_stats():
    """Get user statistics."""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Invalid JSON'}), 400
        
        user_id = data.get('user_id')
        if not user_id:
            return jsonify({'error': 'user_id is required'}), 400
        
        if user_id not in users_data:
            return jsonify({'error': 'User not found'}), 404
        
        user = users_data[user_id]
        return jsonify({
            'user_id': user['user_id'],
            'first_name': user['first_name'],
            'username': user['username'],
            'total_clicks': user['clicks'],
            'current_balance': user['balance'],
            'created_at': user['created_at']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get top 10 players by balance."""
    try:
        sorted_users = sorted(
            users_data.values(),
            key=lambda x: x['balance'],
            reverse=True
        )[:10]
        
        return jsonify({'leaderboard': sorted_users})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    print("[INFO] Starting Flask API server on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
