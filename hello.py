from flask import Flask, jsonify, request
from datetime import datetime, timezone
import os
import logging
import uuid as uuid_module
import random
import sys
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

@app.route('/time')
def time() -> Tuple[Dict[str, str], int]:
    """Return the current server time in ISO 8601 format."""
    current_time = datetime.now(timezone.utc).isoformat()
    logger.info("Time endpoint accessed")
    return jsonify({"current_time": current_time}), 200


@app.route('/date')
def date() -> Tuple[Dict[str, str], int]:
    """Return the current date in ISO 8601 format."""
    current_date = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    logger.info("Date endpoint accessed")
    return jsonify({"date": current_date}), 200


@app.route('/uuid')
def generate_uuid() -> Tuple[Dict[str, str], int]:
    """Generate and return a random UUID."""
    new_uuid = str(uuid_module.uuid4())
    logger.info("UUID endpoint accessed")
    return jsonify({"uuid": new_uuid}), 200


@app.route('/echo')
def echo() -> Tuple[Dict[str, Any], int]:
    """Echo back all query parameters as JSON."""
    try:
        params = dict(request.args)
        logger.info(f"Echo endpoint accessed with params: {params}")
        return jsonify({"params": params}), 200
    except Exception as e:
        logger.error(f"Error in echo endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.route('/random')
def random_number() -> Tuple[Dict[str, Any], int]:
    """
    Generate a random integer within a range.

    Query parameters:
        min: Minimum value (default 1)
        max: Maximum value (default 100)
    """
    try:
        min_val = int(request.args.get('min', 1))
        max_val = int(request.args.get('max', 100))
        if min_val > max_val:
            logger.warning(
                "Invalid range: min > max in random endpoint"
            )
            return jsonify({
                "error": "min must be less than or equal to max"
            }), 400
        result = random.randint(min_val, max_val)
        logger.info(
            f"Random endpoint: generated {result} "
            f"in [{min_val}, {max_val}]"
        )
        return jsonify({
            "random": result,
            "min": min_val,
            "max": max_val,
        }), 200
    except ValueError:
        logger.warning("Non-integer values in random endpoint")
        return jsonify({
            "error": "min and max must be integers"
        }), 400
    except Exception as e:
        logger.error(f"Error in random endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.route('/reverse/<text>')
def reverse(text: str) -> Tuple[Dict[str, str], int]:
    """
    Reverse the given text string.

    Args:
        text: The text to reverse

    Returns:
        JSON response with original and reversed text
    """
    try:
        if not text or not text.strip():
            logger.warning("Empty text provided to reverse endpoint")
            return jsonify({"error": "Text cannot be empty"}), 400

        reversed_text = text[::-1]
        logger.info(f"Reverse endpoint: '{text}' -> '{reversed_text}'")
        return jsonify({
            "original": text,
            "reversed": reversed_text,
        }), 200
    except Exception as e:
        logger.error(f"Error in reverse endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port)
