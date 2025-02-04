from database import db
from models.user import User
from flask import Flask, request, jsonify
from login_manager import login_manager, login_user, logout_user, login_required, current_user


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

@app.route('/user', methods=['POST'])
def create_user():
  data = request.json
  username = data['username']
  password = data['password']

  if(username and password):
    userInDabase = User.query.filter_by(username=username).first()

    if userInDabase:
      return jsonify({"message": "User with this username already exists"}), 400
    
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created"}), 201

  return jsonify({"message": "Invalid data"}), 400

@app.route('/user/<int:user_id>', methods=['GET'])
@login_required
def get_user(user_id):
  user = User.query.get(user_id)

  if user:
    return jsonify({"id:": user.id, "username": user.username}), 200

  return jsonify({"message": "User not found"}), 404

@app.route('/user/<int:user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
  user = User.query.get(user_id)
  data = request.json

  if user:
    if data.get('password'):
      user.password = data['password']
      db.session.commit()
    return jsonify({"message": "Invalid data"}), 400

  return jsonify({"message": "User not found"}), 404

@app.route('/user/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
  user = User.query.get(user_id)

  if user_id == current_user.id:
    return jsonify({"message": "You cannot delete yourself"}), 400

  if user:
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"User ${user.username} deleted"}), 200

  return jsonify({"message": "User not found"}), 404

if __name__ == '__main__':
  app.run(debug=True)