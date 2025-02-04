from database import db
from models.user import User
from flask import Flask, request, jsonify
from login_manager import login_manager, login_user, logout_user, login_required


app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)

@app.route('/login', methods=['POST'])
def login():
  data = request.json
  username = data['username']
  password = data['password']

  if username and password:
    user = User.query.filter_by(username=username).first()

    if user and user.password == password:
      login_user(user)
      return jsonify({'message': "Authenticated!"}), 200

  
  return jsonify({'message': 'Invalid Credentials'}), 400

@app.route('/logout', methods=['GET'])
@login_required
def logout():
  logout_user()
  return jsonify({'message': 'Logged out'}), 200


if __name__ == '__main__':
  app.run(debug=True)