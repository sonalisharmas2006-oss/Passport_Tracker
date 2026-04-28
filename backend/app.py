from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# =====================================
# ENABLE CORS
# =====================================

CORS(app)

# =====================================
# DATABASE CONFIGURATION
# =====================================

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reports.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =====================================
# EMAIL CONFIGURATION
# =====================================

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

# YOUR EMAIL
app.config['MAIL_USERNAME'] = 'sonalisharma.s2006@gmail.com'

# YOUR GOOGLE APP PASSWORD
app.config['MAIL_PASSWORD'] = 'pmdghgnqigeltqdy'

mail = Mail(app)

# =====================================
# DATABASE MODELS
# =====================================

class Report(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))

    city = db.Column(db.String(100))

    issueType = db.Column(db.String(100))

    description = db.Column(db.Text)


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(200))

    email = db.Column(db.String(200), unique=True)

    password = db.Column(db.String(300))


class LoginHistory(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(200))

    email = db.Column(db.String(200))


# =====================================
# HOME ROUTE
# =====================================

@app.route('/')
def home():

    return "Backend Running Successfully"


# =====================================
# REPORT SUBMISSION ROUTE
# =====================================

@app.route('/submit-report', methods=['POST'])
def submit_report():

    try:

        data = request.get_json()

        print("REPORT DATA:", data)

        report = Report(
            name=data.get('name'),
            city=data.get('city'),
            issueType=data.get('issueType'),
            description=data.get('description')
        )

        db.session.add(report)

        db.session.commit()

        print("REPORT STORED SUCCESSFULLY")

        # EMAIL NOTIFICATION
        msg = Message(
            'New Anonymous Report',
            sender='sonalisharma.s2006@gmail.com',
            recipients=['sonalisharma.s2006@gmail.com']
        )

        msg.body = f"""
New Report Submitted

Name: {data.get('name')}

City: {data.get('city')}

Issue Type: {data.get('issueType')}

Description:
{data.get('description')}
"""

        mail.send(msg)

        print("REPORT EMAIL SENT")

        return jsonify({
            "message": "Report submitted successfully"
        })

    except Exception as e:

        print("REPORT ERROR:", str(e))

        return jsonify({
            "message": "Report failed"
        }), 500


# =====================================
# USER REGISTRATION ROUTE
# =====================================

@app.route('/register', methods=['POST'])
def register():

    try:

        data = request.get_json()

        print("REGISTER DATA:", data)

        if not data:
            return jsonify({
                "message": "No data received"
            }), 400

        name = data.get('name')

        email = data.get('email')

        password = data.get('password')

        if not name or not email or not password:
            return jsonify({
                "message": "All fields are required"
            }), 400

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:
            return jsonify({
                "message": "User already exists"
            }), 400

        hashed_password = generate_password_hash(password)

        new_user = User(
            name=name,
            email=email,
            password=hashed_password
        )

        db.session.add(new_user)

        db.session.commit()

        print("USER REGISTERED SUCCESSFULLY")

        # EMAIL NOTIFICATION
        msg = Message(
            'New User Registered',
            sender='sonalisharma.s2006@gmail.com',
            recipients=['sonalisharma.s2006@gmail.com']
        )

        msg.body = f"""
New User Registered

Name: {name}

Email: {email}
"""

        mail.send(msg)

        print("REGISTER EMAIL SENT")

        return jsonify({
            "message": "Registration successful"
        })

    except Exception as e:

        print("REGISTER ERROR:", str(e))

        return jsonify({
            "message": "Signup failed"
        }), 500


# =====================================
# USER LOGIN ROUTE
# =====================================

@app.route('/login', methods=['POST'])
def login():

    try:

        data = request.get_json()

        print("LOGIN DATA:", data)

        if not data:
            return jsonify({
                "message": "No data received"
            }), 400

        email = data.get('email')

        password = data.get('password')

        user = User.query.filter_by(
            email=email
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):

            print("USER LOGIN SUCCESSFUL")

            # STORE LOGIN HISTORY
            login_record = LoginHistory(
                name=user.name,
                email=email
            )

            db.session.add(login_record)

            db.session.commit()

            print("LOGIN HISTORY SAVED")

            # EMAIL NOTIFICATION
            msg = Message(
                'User Logged In',
                sender='sonalisharma.s2006@gmail.com',
                recipients=['sonalisharma.s2006@gmail.com']
            )

            msg.body = f"""
User Logged In

Name: {user.name}

Email: {email}
"""

            mail.send(msg)

            print("LOGIN EMAIL SENT")

            return jsonify({
                "message": "Login successful",
                "name": user.name,
                "email": user.email
            })

        return jsonify({
            "message": "Invalid credentials"
        }), 401

    except Exception as e:

        print("LOGIN ERROR:", str(e))

        return jsonify({
            "message": "Login failed"
        }), 500


# =====================================
# CREATE DATABASE
# =====================================

with app.app_context():

    db.create_all()

    print("DATABASE CREATED")


# =====================================
# RUN APP
# =====================================

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000)