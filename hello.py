from flask import Flask, jsonify, request
import os
import logging
from typing import Tuple, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def hello() -> Tuple[Dict[str, str], int]:
    """Return a hello world message."""
    logger.info("Hello endpoint accessed")
    return jsonify({"message": "Hello, World!"}), 200


@app.route('/health')
def health() -> Tuple[Dict[str, str], int]:
    """Health check endpoint."""
    return jsonify({"status": "healthy"}), 200


@app.route('/greet/<name>')
def greet(name: str) -> Tuple[Dict[str, Any], int]:
    """
    Greet a user by name with error handling.
    
    Args:
        name: The name to greet
        
    Returns:
        JSON response with greeting message
    """
    try:
        if not name or not name.strip():
            logger.warning("Empty name provided to greet endpoint")
            return jsonify({"error": "Name cannot be empty"}), 400
        
        logger.info(f"Greeting user: {name}")
        return jsonify({"message": f"Hello, {name}!"}), 200
    
    except Exception as e:
        logger.error(f"Error in greet endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port)
