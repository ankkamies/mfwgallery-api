# MFWGallery
API for MFWGallery

# Installing:
This project requires python.

Create a new virtual environment:
```
virtualenv env
```

Activate it:
```
source env/bin/activate
```

Install required packages:
```
pip install -u requirements.txt
```

Prepare the database:
```
python manage.py migrate
```

Running a development server:
```
python manage.py runserver
```
