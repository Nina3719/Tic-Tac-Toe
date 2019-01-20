from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp
 
app = Flask(__name__)
 
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def check_end(board, row, col, turn):
    # check row
    for i in range(3):
        if board[row][i] != turn:
            break
        if i == 2:
            return turn
    
    # check col
    for i in range(3):
        if board[i][col] != turn:
            break
        if i == 2:
            return turn
    
    # check diagonal
    if row == col:
        for i in range(3):
            if board[i][i] != turn:
                break
            if i == 2:
                return turn
    
    # check full board
    if not any(None in sublist for sublist in board):
        return "Tie"
    
    return False

 
@app.route("/")
@app.route("/<int:row>/<int:col>")
def index(row = None, col = None):
    end_game = False
    if "board" not in session:
        session["board"] = [[None, None, None], 
                            [None, None, None], 
                            [None, None, None]]
        session["turn"] = "X"
    elif row != None and col != None:
        session["board"][row][col] = session["turn"]
        end_game = check_end(session["board"], row, col, session["turn"])
        if not end_game:
            session["turn"] = "O" if session["turn"] == "X" else "X"
    return render_template("game.html", game=session["board"], turn=session["turn"], end_game = end_game)
 


@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    return redirect(url_for("index", row = row, col = col))


# finish game
# and reset game button


    # return "play"

# @app.route('/')
# def index():
#     return "Hello World"

# # flask will always go to the more specific one!
# @app.route("/<string:name>")
# def hello(name):
#     name = name.capitalize()
#     return f"Hello, {name}!"

# @app.route("/<string:name1>/<string:name2>")
# def hello2(name1, name2):
#     name1 = name1.capitalize()
#     name2 = name2.capitalize()
#     return f"Hello, {name1} and {name2}!"

# @app.route("/athena")
# def athena():
#     return "Good Bye"

# @app.route("/template/<string:name>")
# def welcome(name):
#     return render_template("index.html", name = name.capitalize())