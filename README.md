# Python Flask Application

A simple Flask web application with CI/CD pipeline deployed to AWS EC2.

## Application Structure

- `hello.py` - Flask application with API endpoints
- `test_hello.py` - Unit tests for all endpoints
- `requirements.txt` - Python dependencies (Flask + Gunicorn)
- `buildspec.yml` - AWS CodeBuild configuration for running tests
- `appspec.yml` - AWS CodeDeploy configuration for EC2 deployment
- `scripts/` - Deployment lifecycle scripts

## API Endpoints

- `GET /` - Returns a hello world message
- `GET /health` - Health check endpoint
- `GET /greet/<name>` - Greets a user by name

## Local Development

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the application:
```bash
python hello.py
```

Run tests:
```bash
python -m unittest test_hello.py
```

## CI/CD Pipeline

The project uses a 3-stage AWS CodePipeline:

### Pipeline Architecture
1. Source: GitHub (via CodeStar Connection)
2. Build: AWS CodeBuild (runs unit tests)
3. Deploy: AWS CodeDeploy (deploys to EC2)

### Pipeline Resources Created

The pipeline was created using AWS CLI commands with the following resources:

#### IAM Roles
- `flask-codebuild-role` - CodeBuild service role
- `flask-codedeploy-role` - CodeDeploy service role  
- `flask-codepipeline-role` - CodePipeline service role

#### CodeBuild
- Project: `flask-app-build`
- Configuration: `codebuild-project.json`
- Image: `aws/codebuild/amazonlinux2-x86_64-standard:5.0`
- Buildspec: `buildspec.yml` (runs unit tests)

#### CodeDeploy
- Application: `flask-app`
- Deployment Group: `flask-deployment-group`
- Target: EC2 instances with tag `Name=DataDogtest`

#### CodePipeline
- Pipeline: `flask-app-pipeline`
- Configuration: `pipeline-structure.json`
- Artifact Store: S3 bucket `codepipeline-us-east-1-864668041946`
- GitHub Connection: CodeStar connection `maheshcg853`

### How It Works

1. Push code to GitHub main branch
2. CodePipeline detects change via CodeStar connection
3. CodeBuild runs tests from buildspec.yml
4. If tests pass, CodeDeploy deploys to EC2 using appspec.yml
5. Deployment scripts install dependencies and start Gunicorn

### Deployment Scripts

Located in `scripts/` directory:

- `before_install.sh` - Installs Python and pip3
- `after_install.sh` - Installs Python dependencies
- `stop_application.sh` - Stops running application
- `start_application.sh` - Starts application with Gunicorn

## Production Deployment

The application runs on EC2 with Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 hello:app
```

Logs are available at: `/var/log/flask-app.log`

## GitHub Repository

https://github.com/maheshcg853/kir0-pythonproject.git
