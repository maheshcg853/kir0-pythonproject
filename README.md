# Python Flask Application

A simple Flask web application ready for EC2 deployment.

## Local Development

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the application:
```bash
python hello.py
```

## Production Deployment

Run with Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 hello:app
```

## Endpoints

- `GET /` - Returns a hello world message
- `GET /health` - Health check endpoint
