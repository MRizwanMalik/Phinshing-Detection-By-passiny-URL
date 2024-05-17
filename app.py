from flask import Flask, render_template, request, redirect, url_for, flash
from models import User, create_user, get_user_by_email
from werkzeug.security import check_password_hash
import secrets
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from fyp import app as dash_app
import mysql.connector 
import re 
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)   #this secrete is used for secure user password in encoding form

# Flask-Login setup
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')
# Function to validate email format

##############################    This code checking that email write correct or not   #####################################
###################                                                                                     ####################

def is_valid_email(email):
    email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
    return bool(re.match(email_regex, email))

##############################           Register Route for successfull Register                ############################
###################                                                                                     ####################



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if not is_valid_email(email):
            flash('Invalid email format. Please provide a valid email address.', 'error')
        else:
            existing_user = get_user_by_email(email)
            if existing_user:
                flash('Email already exists. Please choose another one.')
            else:
                create_user(email, password)
                flash('Registration successful. Please log in.', 'success')
                return redirect(url_for('login'))

    return render_template('register.html')


##############################          Login Route for successfull Login                       ############################
###################                                                                                     ####################


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if not is_valid_email(email):
            flash('Invalid email format. Please provide a valid email address.', 'error')
        else:
            user = get_user_by_email(email)

            if user and check_password_hash(user.password, password):
                # Use Flask-Login to log in the user
                login_user(user)

                # flash('Login successful.')
                # Redirect to the 'http://127.0.0.1:8050/' URL
                return redirect('http://127.0.0.1:8050/')
            else:
                flash('Login failed. Check your email and password.', 'error')

    return render_template('login.html')


##############################           Function to check if admin login is valid              ############################
###################                                                                                     ####################



def is_valid_admin(email, password):
    connection = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='fyp'
    )

    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM admin WHERE email = %s"
    values = (email,)

    cursor.execute(query, values)

    admin_data = cursor.fetchone()

    cursor.close()
    connection.close()

    if admin_data and admin_data['password'] == password:
        return True
    else:
        return False
    
    
##############################           Rout for admin login is valid                          ############################
###################                                                                                     ####################



@app.route('/admin', methods=['GET', 'POST'])
def admin():
    error_message = None  # Initialize error message
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Simulate admin login
        if is_valid_admin(email,password):
            
            
            # flash('Login successful.')
            return redirect(url_for('admin_login', admin_login_success=True))
        else:
            
            error_message = 'Login failed. Check your email and password.'
            flash(error_message,'error')  # Flash the error message

    return render_template('admin.html',error_message=error_message)
# Database configuration (replace with your actual database configuration)
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'database': 'fyp'
}


# ##############################           Function to fetch data from the comments table         ############################
# ###################                                                                                     ####################



# def fetch_comments_data_from_database():
#     connection = mysql.connector.connect(**db_config)
#     cursor = connection.cursor(dictionary=True)

#     query = "SELECT * FROM comments"
#     cursor.execute(query)

#     comments_data = cursor.fetchall()

#     cursor.close()
#     connection.close()

#     return comments_data


##############################           Function to fetch data from the users table            ############################
###################                                                                                     ####################


def fetch_users_data_from_database():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM users"
    cursor.execute(query)

    users_data = cursor.fetchall()

    cursor.close()
    connection.close()

    return users_data

# ##############################           Function to fetch data from the contact_form table     ############################
# ###################                                                                                     ####################


# def fetch_contact_form_data_from_database():
#     connection = mysql.connector.connect(**db_config)
#     cursor = connection.cursor(dictionary=True)

#     query = "SELECT * FROM contact_form"
#     cursor.execute(query)

#     contact_form_data = cursor.fetchall()

#     cursor.close()
#     connection.close()

#     return contact_form_data


##############################           Function to fetch data from the user_history table     ############################
###################                                                                                     ####################


def fetch_user_history_data_from_database():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM user_history"
    cursor.execute(query)

    user_history_data = cursor.fetchall()

    cursor.close()
    connection.close()

    return user_history_data

##############################           Routes to display all fetch table data in admin panel  ############################
###################                                                                                     ####################


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    admin_login_success = request.args.get('admin_login_success')
    # comments_data = fetch_comments_data_from_database()
    users_data = fetch_users_data_from_database()
    # contact_form_data = fetch_contact_form_data_from_database()
    user_history_data = fetch_user_history_data_from_database()

    return render_template(
        'admin_login.html',
        # comments_data=comments_data,
        users_data=users_data,
        # contact_form_data=contact_form_data,
        user_history_data=user_history_data,
        admin_login_success=admin_login_success
    )



@app.route('/flask_index')
def flask_index():
    return render_template('index.html')

def run_flask_app():
    app.run(debug=False)

if __name__ == '__main__':
    app.run(debug=False)
    
    
    
    
    
    
    