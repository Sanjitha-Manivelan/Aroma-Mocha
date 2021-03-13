import os
from form import AddForm,DelForm
from flask import Flask, render_template,url_for,redirect,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

class Users(db.Model):

  __tablename__ = 'users'
  username = db.Column(db.Text,primary_key=True)
  password = db.Column(db.Text)
  userType=db.Column(db.Text)

  def __init__(self,username, password, userType):
      self.username = username
      self.password = password
      self.userType=userType

  def __repr__(self):
      return f"User name: {self.username} {self.password} {self.userType}"



#@app.route('/')
#def index():
 # return render_template('Homepage.html')

#@app.route('/home')
#def home():
#    return render_template('home.html')



@app.route('/signup', methods=['GET'])
def sign_up():

    return render_template('register_customer.html')


@app.route('/signup', methods=['POST'])
def sign_up_post():
    email=request.form.get("email")
    pwd=request.form.get("pwd")
    user=Users(email,pwd,'C')
    user_email=Users.query.get(email)
    fail=False
    if user_email is None:
        db.session.add(user)
        db.session.commit()
        return render_template('login_customer.html',fail=fail)
    else:
        fail=True
        error_message="Username already exists"
        return render_template('register_customer.html',error_message=error_message,fail=fail)


@app.route('/login', methods=['GET','POST'])
def login():
    return render_template('login_customer.html')

@app.route('/val', methods=['GET','POST'])
def val():
    email=request.form.get("email2")
    pwd=request.form.get("pwd2")
    print(email)
    print(pwd)
    user = Users.query.get(email)
    if(user is not None and user.password == pwd and user.userType=='C'):
        fail=False
        print('success')
        return render_template('placeOrder.html', email=email, pwd=pwd, fail=fail)
    else:
        fail=True
        print('fail')
        return render_template('login_customer.html', fail=fail)

@app.route('/sign-out', methods=['GET','POST'])
def sign_out():
    return render_template('sign_out.html')

@app.route('/employee/signup', methods=['GET'])
def employee_sign_up():

    return render_template('register_employee.html')


@app.route('/employee/signup', methods=['POST'])
def employee_sign_up_post():
    email=request.form.get("email")
    pwd=request.form.get("pwd")
    user=Users(email,pwd,'E')
    fail=False
    user_email=Users.query.get(email)
    if user_email is None:
        db.session.add(user)
        db.session.commit()
        return render_template('login_employee.html')
    else:
        fail=True
        error_message="Username already exists"
        return render_template('register_employee.html',error_message=error_message, fail=fail)


@app.route('/employee/login', methods=['GET','POST'])
def employee_login():
    return render_template('login_employee.html')

@app.route('/employee/val', methods=['GET','POST'])
def employee_val():
    email=request.form.get("email2")
    pwd=request.form.get("pwd2")
    print(email)
    print(pwd)
    user = Users.query.get(email)
    if(user is not None and user.password == pwd and user.userType=='E'):
        fail=False
        print('success')
        return render_template('viewOrder.html', email=email, pwd=pwd)
    else:
        fail=True
        print('fail')
        return render_template('login_employee.html', fail=fail)

@app.route('/viewOrder', methods=['GET','POST'])
def checkout_drink():
    list=[]
    form=AddForm()
    #all_drinks=['cookies','cookies & cream','chocolate cake','chocolate fudge brownies', "blueberry drink", "mango and raspberry drink", "tropical drink", "cherry milk shake"]
    if(request.args.get("Cookies")=="on"):
        list.append("Cookies")
    if(request.args.get("Cookies&Cream")=="on"):
        list.append("Cookies&Cream")
    if(request.args.get("Chocolate Cake")=="on"):
        list.append("Chocolate Cake")
    if(request.args.get("Chocolate Fudge Brownies")=="on"):
        list.append("Chocolate Fudge Brownies")
    if(request.args.get("Blueberry Drink")=="on"):
        list.append("Blueberry Drink")
    if(request.args.get("Mango & Raspberry Drink")=="on"):
        list.append("Mango & Raspberry Drink")
    if(request.args.get("The Tropical Drink")=="on"):
        list.append("The Tropical Drink")
    length=len(list)
    print(list)
    return render_template('viewOrder.html',list=list,length=length)


if __name__ == "__main__":
    app.run()
