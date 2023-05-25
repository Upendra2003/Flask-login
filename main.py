from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
import pymongo

app = Flask(__name__)


app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
client=pymongo.MongoClient('mongodb://localhost:27017')
db=client['registered_users']
collections=db['users']

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register',methods=['POST','GET'])
def register():
    if request.method=='POST':
        hash_and_salted_password=generate_password_hash(
            request.form.get('password'),
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user={
            "name":request.form.get('name'),
            "email":request.form.get('email'),
            "password":hash_and_salted_password
        }
        collections.insert_one(new_user)
        return redirect(url_for('secrets',name=request.form.get('name')))
    return render_template("register.html")


@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        find_user=collections.find_one({"email":email})
        if check_password_hash(find_user['password'],password):
            return redirect(url_for('secrets',name=find_user['name']))
    return render_template("login.html")


@app.route('/secrets/<name>',methods=['GET','POST'])
def secrets(name):
    return render_template("secrets.html",name=name)


@app.route('/logout')
def logout():
    return redirect(url_for('home'))


@app.route('/download')
def download():
    return send_from_directory('static',path='files/cheat_sheet.pdf')


if __name__ == "__main__":
    app.run(debug=True)
