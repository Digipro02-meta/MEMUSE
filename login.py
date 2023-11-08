from flask import Flask, request, jsonify, render_template, url_for, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
import sqlite3
import logging

# from models import User

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app)

conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()

# 데이터베이스 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "123123123"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

conn.commit()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    birthdate = db.Column(db.String(128), nullable=False)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        if password is None:
            return False
        return check_password_hash(self.password, password)

    def __init__(self, name, birthdate, username, password):
        self.name = name
        self.birthdate = birthdate
        self.username = username
        self.password = generate_password_hash(password)

@app.route('/')
def index():
    return render_template('intro.html')

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}

@app.context_processor
def inject_user():
    if 'username' in session:
        return dict(username=session['username'])
    return dict(username=None)

@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        name = request.form.get('name')
        birthdate = request.form.get('birthdate')
        username = request.form.get('username')
        password = request.form.get('password')
        print("get 저장")

        # 뉴유저 생성
        new_user = User(name=name, birthdate=birthdate, username=username, password=password)
        print("new 저장")

        # 데베에 뉴유저 추가
        try:
            # 데베에 뉴유저 추가
            db.session.add(new_user)
            db.session.commit()
            flash('Successfully signed up! Please login.', 'success')
            print("데베 저장")
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            
            flash('Username already exists. Please choose a different one.', 'error')
            print("Username already exists. Please choose a different one.")
            
            return redirect(url_for('join'))

    return render_template('join.html')
        

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print("gerror")
         # Check if user exists and the password is correct
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['logged_in'] = True
            print("s")
            session['username'] = username
            return render_template('workplace.html')
        elif user is None:
            flash('Invalid username', 'error')
            print("Username not found")
        else:
            flash('Invalid password', 'error')
            print("Incorrect password")
            
    return render_template('login.html')

# @app.route('/join_success')
# def join_success():
#     if not session.get('logged_in'):
#         return redirect(url_for('login'))
#     else:
#         # 세션에서 username을 가져와서 dashboard.html에 전달합니다.
#         username = session.get('username')
#         return render_template('join_success.html', username=username)
    
@app.route('/workplace')
def workplace():
    if not session.get('logged_in'):
        flash('Please login to view this page.', 'error')
        return redirect(url_for('login'))
    username = session.get('username', 'Guest')
    return render_template('workplace.html',  username=username)

@app.route('/voice_login_join_choice')
def voice_login_join_choice():
    # Your logic here
    return render_template('voice_login_join_choice.html')

@app.route('/cartoon_gallery1')
def cartoon_gallery1():
    return render_template('cartoon_gallery1.html')

@app.route('/cartoon_gallery2')
def cartoon_gallery2():
    return render_template('cartoon_gallery2.html')

@app.route('/cartoon_gallery3')
def cartoon_gallery3():
    return render_template('cartoon_gallery3.html')

@app.route('/guide')
def guide():
    return render_template('guide.html')



@app.route('/live_gallery1')
def live_gallery1():
    return render_template('live_gallery1.html')

@app.route('/live_gallery2')
def live_gallery2():
    return render_template('live_gallery2.html')

@app.route('/live_gallery3')
def live_gallery3():
    return render_template('live_gallery3.html')

@app.route('/my_page')
def my_page():
    if 'user_id' not in session:
        flash('Please login to view this page.', 'danger')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    return render_template('my_page.html', user=user)

@app.route('/my_page_my_gallery1')
def my_page_my_gallery1():
    
    
    return render_template('my_page_my_gallery1.html')

@app.route('/my_page_my_gallery2')
def my_page_my_gallery2():
    return render_template('my_page_my_gallery2.html')

@app.route('/my_page_my_gallery3')
def my_page_my_gallery3():
    return render_template('my_page_my_gallery3.html')

@app.route('/new_back')
def new_back():
    return render_template('new_back.html')

@app.route('/new_complete')
def new_complete():
    return render_template('new_complete.html')

@app.route('/new_filter')
def new_filter():
    return render_template('new_filter.html')

@app.route('/new_no_save')
def new_no_save():
    return render_template('new_no_save.html')

@app.route('/new_object')
def new_object():
    return render_template('new_object.html')

@app.route('/new_save_success')
def new_save_success():
    return render_template('new_save_success.html')

@app.route('/new_shot')
def new_shot():
    return render_template('new_shot.html')

@app.route('/new_style')
def new_style():
    return render_template('new_style.html')

@app.route('/pastel_gallery1')
def pastel_gallery1():
    return render_template('pastel_gallery1.html')

@app.route('/pastel_gallery2')
def pastel_gallery2():
    return render_template('pastel_gallery2.html')

@app.route('/pastel_gallery3')
def pastel_gallery3():
    return render_template('pastel_gallery3.html')

@app.route('/pro_back')
def pro_back():
    return render_template('pro_back.html')

@app.route('/pro_back_complete')
def pro_back_complete():
    return render_template('pro_back_complete.html')

@app.route('/pro_complete')
def pro_complete():
    return render_template('pro_complete.html')

@app.route('/pro_edit_obj_check')
def pro_edit_obj_check():
    return render_template('pro_edit_obj_check.html')

@app.route('/pro_edit_obj_num')
def pro_edit_obj_num():
    return render_template('pro_edit_obj_num.html')
@app.route('/pro_edit_object')
def pro_edit_object():
    return render_template('pro_edit_object.html')

@app.route('/pro_edit_shot_check')
def pro_edit_shot_check():
    return render_template('pro_edit_shot_check.html')

@app.route('/pro_edit_shot_num')
def pro_edit_shot_num():
    return render_template('pro_edit_shot_num.html')

@app.route('/pro_filter')
def pro_filter():
    return render_template('pro_filter.html')

@app.route('/pro_lora')
def pro_lora():
    return render_template('pro_lora.html')

@app.route('/pro_lora_num')
def pro_lora_num():
    return render_template('pro_lora_num.html')

@app.route('/pro_more_edit_obj')
def pro_more_edit_obj():
    return render_template('pro_more_edit_obj.html')

@app.route('/pro_more_object')
def pro_more_object():
    return render_template('pro_more_object.html')

@app.route('/pro_more_specify_obj')
def pro_more_specify_obj():
    return render_template('pro_more_specify_obj.html')

@app.route('/pro_no_save')
def pro_no_save():
    return render_template('pro_no_save.html')

@app.route('/pro_object')
def pro_object():
    return render_template('pro_object.html')

@app.route('/pro_object_complete')
def pro_object_complete():
    return render_template('pro_object_complete.html')

@app.route('/pro_save_success')
def pro_save_success():
    return render_template('pro_save_success.html')

@app.route('/pro_specify_obj')
def pro_specify_obj():
    return render_template('pro_specify_obj.html')

@app.route('/pro_specify_obj_check')
def pro_specify_obj_check():
    return render_template('pro_specify_obj_check.html')

@app.route('/pro_specify_obj_check2')
def pro_specify_obj_check2():
    return render_template('pro_specify_obj_check2.html')

@app.route('/pro_specify_obj_num')
def pro_specify_obj_num():
    return render_template('pro_specify_obj_num.html')

@app.route('/pro_specify_obj_num2')
def pro_specify_obj_num2():
    return render_template('pro_specify_obj_num2.html')

@app.route('/pro_style')
def pro_style():
    return render_template('pro_style.html')

@app.route('/voice_join_success')
def voice_join_success():
    return render_template('voice_join_success.html')

@app.route('/voice_join1')
def voice_join1():
    return render_template('voice_join1.html')

@app.route('/voice_join2')
def voice_join2():
    return render_template('voice_join2.html')

@app.route('/voice_login')
def voice_login():
    return render_template('voice_login.html')

@app.route('/watercolor_gallery1')
def watercolor_gallery1():
    return render_template('watercolor_gallery1.html')

@app.route('/watercolor_gallery2')
def watercolor_gallery2():
    return render_template('watercolor_gallery2.html')

@app.route('/watercolor_gallery3')
def watercolor_gallery3():
    return render_template('watercolor_gallery3.html')

@app.route('/whole_gallery1')
def whole_gallery1():
    return render_template('whole_gallery1.html')

@app.route('/whole_gallery2')
def whole_gallery2():
    return render_template('whole_gallery2.html')

@app.route('/whole_gallery3')
def whole_gallery3():
    return render_template('whole_gallery3.html')

@app.route('/intro')
def intro():
 
    return render_template('intro.html')


# @app.route('/logout')
# def logout():
#     session.pop('user_id', None)
#     flash('You have been logged out.', 'success')
#     return redirect(url_for('index'))

if __name__ == '__main__':
    print(app.config['SQLALCHEMY_DATABASE_URI'])
    with app.app_context():
        if db.engine.url.drivername == "sqlite":
            migrate.init_app(app, db, render_as_batch=True)
        else:
            migrate.init_app(app, db)
        db.create_all()
        # try:
        #     db.create_all()  # 첫 실행에서만 필요하고 그 다음부터는 주석 처리
        # except Exception as e:
        #     print(f"An error occurred while creating tables: {e}")

    app.run(debug=True)