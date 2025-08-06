from classes import *
from flask import *
from flask_socketio import SocketIO
from flask_cors import CORS

app= Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('frontend.html', 'systemScreen.html', 'addBook.html', 'searchBook.html', 'checkOutForm.html')

@socketio.on('login_check')
def handle_flag(data):
    print(data)
    return loginValidation().check_login(data)

@socketio.on('add_book')
def handle_flag(data):
    return library().add_book(data)

@socketio.on('search')
def handle_flag(data):
    print(data)
    return library().search_library(data)

@socketio.on('check_out')
def handle_flag(data):
    remove = library().remove_book(data)
    create_loan = library().create_loan(data)
    return remove, create_loan   

@socketio.on('view_out')
def handle_flag(data):
    return library().check_removed(data)

@socketio.on('create_user')
def handle_flag(data):
    return signUpValidate().add_user(data)
    
if __name__ == "__main__":  
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, use_reloader=False)    