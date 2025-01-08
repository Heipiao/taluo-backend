from flask import Blueprint, request, jsonify
from services.user_service import register_user, login_user

bp = Blueprint('system', __name__)

# Health check endpoint
@bp.route('/healthy', methods=['GET'])
def healthy():
    """
    Endpoint to check if the system is healthy.
    """
    return jsonify({
        "status": "healthy",
        "message": "The system is running smoothly."
    }), 200

# Liveness check endpoint
@bp.route('/liveness', methods=['GET'])
def liveness():
    """
    Endpoint to check if the application is live.
    """
    return jsonify({
        "status": "alive",
        "message": "The application is live and ready."
    }), 200
