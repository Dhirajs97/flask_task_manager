# Importing the required liabraries
from flask import Flask, request, json, jsonify, make_response
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy

import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from datetime import timezone
from functools import wraps
import re


# Initialize the app
app = Flask(__name__)

# Secret Key
app.config['SECRET_KEY'] = 'thisissecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/task_manager'


db = SQLAlchemy(app)


# *****  Database Tables *****
# User table to store users information
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(255))

# Task table to store the users tasks and files
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    due_date = db.Column(db.DateTime)
    attachment = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# create table with above model Product
with app.app_context():
    db.create_all()


# ****   JWT Token Authentication ****
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
          
        if not token:
            return jsonify({'Message': 'Token is missing'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            print(data)
            current_user = User.query.filter_by(public_id=data['public_id']).first()
            print(current_user)

        except jwt.ExpiredSignatureError as ex:
            return jsonify({'Message': 'Token has expired!',  'Error': str(ex)})
        except jwt.InvalidTokenError as e:
            return jsonify({'Message': 'Token is Invalid', 'Error': str(e)})

        return f(current_user, *args, **kwargs)

    return decorated


# *****  User *****
    
# Get all Users from the User table
@app.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):
    users = User.query.all()
    output = []
    for user in users:
        user_data = {}
        user_data['name'] = user.name
        user_data['email'] = user.email
        user_data['password'] = user.password
        output.append(user_data)
    return jsonify({'users': output})

# get user details by uder id
@app.route('/user/<id>', methods=['GET'])
@token_required
def get_user_detail(current_user, id):

    # Check if ID is passing as String
    if str.isdigit(id) == False:
        return jsonify(f"Message: The Id of the product cannot be a string.")
    
    else:
        user_data = {}
        user = User.query.filter_by(id=id).first()   #get function to fetch specific row

        # If User is not found
        if user_data is None:
            return jsonify(f"No User was found.")
        
        user_data['name'] = user.name
        user_data['email'] = user.email
        return jsonify({'user':user_data})



# Register new user / create new user to database
@app.route('/user/register', methods=['POST'])

def create_user():
    data = request.get_json()

    existing_user = User.query.filter_by(email= data['email']).first()
    if existing_user:
        return jsonify({'Message': 'Email already exists!'})
    
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], email=data['email'], password=hashed_password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'Message': 'New user has been registered!'})
    except:
        return jsonify({'Message': 'Error occured while registration, please try again.'})


# Delete user
@app.route('/user/<id>', methods=['DELETE'])
@token_required
def delete_user(current_user, id):
    user = User.query.filter_by(id=id).first()

    if not user:
        return jsonify({'Message': 'No user found.'})
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({'Message': 'The user has been deleted'})


# Login | User Authentication
@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify, please try again.', 401)
    
    email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
    if not email_pattern.match(auth.username):
        return make_response('Invalid email format', 401)

    user = User.query.filter_by(email=auth.username).first()
    print(user)
    print(f"Auth Username: {auth.username}")
    print(f"Auth Password: {auth.password}")

    if not user:
        return make_response('Email does not exist!', 401)
    
    print(f"Auth Password: {auth.password}")
    print(f"User Password: {user.password}")

    if check_password_hash(user.password, auth.password):
        print(f"Auth Password: {auth.password}")
        print(f"User Password: {user.password}")
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
       
        return make_response(jsonify({'token': token}), 201)
    
    return make_response('Could not verify, please try again.', 403)


# Logot the user and expiration of token
# to blacklist token
blacklist = set()

@app.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    token = request.headers['x-access-token']
    blacklist.add(token)
    return jsonify({'Message': 'Logout successful!'})



#  **** Task Management Work  *****

# get all task of the logged-in user 
@app.route('/my_tasks', methods=['GET'])
@token_required
def get_all_tasks(current_user):

    tasks = Task.query.filter_by(user_id=current_user.id).all()

    output = []
    for task in tasks:
        task_data = {}
        task_data['id'] = task.id
        task_data['title'] = task.title
        task_data['due_date'] = task.due_date
        task_data['attachment'] = task.attachment

        output.append(task_data)

    return jsonify({'tasks': output})


# Get all Tasks with Pagination
@app.route('/all_tasks', methods=['GET'])
@token_required
def get_my_tasks(current_user):

    page = request.args.get('page', 1, type=int)
    per_page = 5     # defining 5 tasks per page to be displayed

    # Calculate the offset based on the page number to determine which set of tasks to retrieve
    offset = (page - 1) * per_page

    # retrieve tasks with pagination    
    tasks = Task.query.filter_by(user_id=current_user.id).offset(offset).limit(per_page).all()

    output = []
    for task in tasks:
        task_data = {}
        task_data['id'] = task.id
        task_data['title'] = task.title
        task_data['due_date'] = task.due_date
        task_data['attachment'] = task.attachment

        output.append(task_data)

    total_tasks = Task.query.filter_by(user_id=current_user.id).count()

    return jsonify({'tasks': output, 'page':page, 'per_page':per_page, 'total_tasks':total_tasks, 'total_pages':(total_tasks + per_page -1)//per_page})



# get task of the logged-in user with Task ID
@app.route('/task/<task_id>', methods=['GET'])
@token_required
def get_task_by_id(current_user, task_id):

    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()

    if not task:
        return jsonify({'Message': 'No task found!'})
    
    task_data = {}
    task_data['id'] = task.id
    task_data['title'] = task.title
    task_data['due_date'] = task.due_date
    task_data['attachment'] = task.attachment

    return jsonify(task_data)


# Create a task and assign it to the current logged-in user.
@app.route('/task', methods=['POST'])
@token_required
def create_task(current_user):
    data = request.get_json()

    new_task = Task(title=data['title'], due_date=data['due_date'], attachment=data['attachment'], user_id=current_user.id)

    db.session.add(new_task)
    db.session.commit()

    return jsonify({'Message': 'New task has been created successfully!'})


# Edit Task- Update the task with given task ID
@app.route('/update_task/<task_id>', methods=['PUT'])
@token_required
def update_task(current_user, task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()

    if not task:
        return jsonify({'Message': 'No task found!'})
    
    data = request.get_json()
    
    # Check if the fields are present in the provided data
    if 'title' in data:
        task.title=data['title'] 
    
    if 'due_date' in data:
        task.due_date=data['due_date'] 
    if 'attachment' in data:
        task.attachment=data['attachment']

    db.session.commit()
    return jsonify({'Message': 'Task has been updated'})


# Delete Task- delete a task by task ID.
@app.route('/task/<task_id>', methods=['DELETE'])
@token_required
def delete_task(current_user, task_id):

    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()

    if not task:
        return jsonify({'Message': 'No task found!'})
    
    db.session.delete(task)
    db.session.commit()

    return jsonify({'Message': 'The task has been deleted!'})



if __name__ == '__main__':
    app.run(debug=True)
