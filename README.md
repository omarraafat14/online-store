# Introduction
This README file contains instructions for running the code associated with the Bit68 Task.

# Requirements
Before running the code, ensure that you have the following requirements installed:

- Python 3.x
- Django
- Django Rest Framework
- MySQL (or another relationaldatabase management system)


# Instructions
1. Clone the repository or download the files in zip format.

2. Navigate to the root directory of the project in a terminal or command prompt.

3. Create a virtual environment and activate it:
```bash
python3 -m venv env
env\Scripts\activate
```

4. Install the project requirements:
```bash
pip install -r requirements.txt
```

5. Create a MySQL database for the project and update the DATABASES setting in ```settings.py``` to reflect your database settings (e.g. database name, username, password, host, port).

6. Run the database migrations:
```bash
python manage.py migrate
```

7. Start the Django development server:
```bash
python manage.py runserver
```

8. Navigate to http://localhost:8000/ in a web browser to access the API endpoints.


# API Endpoints
Here are the API endpoints that you can access:

- 'GET /api/cart/': Returns the cart object associated with the currently authenticated user (or creates a new cart object if one does not exist).
- 'PUT /api/cart/': Updates the cart object associated with the currently authenticated user.
- 'POST /api/order/': Creates a new order object based on the contents of the user's cart and deletes the cart's items. Returns the newly created order object.
