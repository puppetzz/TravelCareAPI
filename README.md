# TravelCareAPI

API for TravelCare app.

## Installation

Activate virtual environment

```bash
python -m venv env

#on mac
source env/bin/activate

#on windows
env/Scrips/activate
```

Install package

```bash
pip install -r requirements.txt
```

Create .env file in backend folder:

```
export DATABASE_USER = "your postgres user name database"
export DATABASE_PASSWORD = "your database password"
export SECURITY_KEY = "your secret key"
export EMAIL_HOST_USER = "your email use to send mail"
export EMAIL_HOST_PASSWORD = "your email password"
export CLOUD_NAME = "your cloudinanry product environment "
export API_KEY = "your cloudinary api key"
export API_SECRET = "your cloudinary secret key"
```

## Usage

Run local web server

```bash
cd backend
python manage.py runserver
```
