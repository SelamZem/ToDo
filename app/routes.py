from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, ToDo
from . import db

routes = Blueprint('routes', __name__)

# Home Page
@routes.route('/')
def home():
    return render_template('home.html')

# Register
@routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['FirstName']
        last_name = request.form['LastName']


        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('routes.register'))

        user = User(
            username=username,
            FirstName=first_name,
            LastName=last_name,
            password=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()

        flash('Registered successfully. Please log in.', 'success')
        return redirect(url_for('routes.login'))

    return render_template('register.html')

# Login
@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('routes.todos'))
        else:
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('routes.login'))

    return render_template('login.html')

# Logout
@routes.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('routes.home'))

# View Todos
@routes.route('/todos')
def todos():
    if 'user_id' not in session:
        flash('Please log in to view todos.', 'warning')
        return redirect(url_for('routes.login'))

    user_id = session['user_id']
    todos = ToDo.query.filter_by(userId=user_id).all()
    return render_template('Todo.html', todos=todos)

# Add Todo
@routes.route('/add', methods=['GET', 'POST'])
def add_todo():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))

    if request.method == 'POST':
        title = request.form['Title']
        description = request.form['Description']
        user_id = session['user_id']

        todo = ToDo(Title=title, Description=description, userId=user_id)
        db.session.add(todo)
        db.session.commit()
        flash('Todo added.', 'success')
        return redirect(url_for('routes.todos'))

    return render_template('addToDo.html')

# Update Todo
@routes.route('/update/<int:todo_id>', methods=['GET', 'POST'])
def update_todo(todo_id):
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))

    todo = ToDo.query.get_or_404(todo_id)
    if todo.userId != session['user_id']:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('routes.todos'))

    if request.method == 'POST':
        todo.Title = request.form['Title']
        todo.Description = request.form['Description']
        todo.IsDone = 'IsDone' in request.form
        db.session.commit()
        flash('Todo updated.', 'success')
        return redirect(url_for('routes.todos'))

    return render_template('update.html', todo=todo)

# Delete Todo
@routes.route('/delete/<int:todo_id>', methods=['GET', 'POST'])
def delete_todo(todo_id):
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))

    todo = ToDo.query.get_or_404(todo_id)
    if todo.userId != session['user_id']:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('routes.todos'))

    db.session.delete(todo)
    db.session.commit()
    flash('Todo deleted.', 'info')
    return redirect(url_for('routes.todos'))
