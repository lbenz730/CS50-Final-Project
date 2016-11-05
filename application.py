from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import gettempdir
import re
from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = gettempdir()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
    # determine user's cash
    cash = db.execute("SELECT cash FROM 'users' WHERE id = :user_id", user_id = session["user_id"])[0]["cash"]
    
    # sum shares of each stock
    data = db.execute("SELECT symbol, name, SUM(moved) FROM portfolio WHERE userid = :user_id GROUP BY symbol HAVING SUM(moved) > 0 ORDER BY symbol",
        user_id = session["user_id"])
    
    # get current value of each stock
    prices = []
    for i in range(len(data)):
        prices.append(lookup(data[i]["symbol"])["price"])
         
    # get value of all shares of stock
    values = []
    money = 0
    for j in range(len(data)):
        worth = float(prices[j] * data[j]["SUM(moved)"])
        values.append(usd(worth))
        money += worth
        
    # append all data together
    table = []
    for symbol in range(len(data)):
        table.append({"symbol":data[symbol]["symbol"],"name":data[symbol]["name"], "shares":int(data[symbol]["SUM(moved)"]), 
        "price":usd(prices[symbol]), "total":values[symbol]})
    
    # render home page
    return render_template("index.html", cash = usd(cash), table = table, total_value = usd(money + cash))

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    if request.method == "POST":
        # ensure valid stock symbol
        if lookup(request.form.get("symbol")) == None:
            return apology("Enter a valid stock symbol")
            
        # ensure valid number of shares
        if not str.isalnum(request.form.get("shares")):
            return apology ("Invalid Input: Must buy integer number of shares")
        if str.isalpha(request.form.get("shares")):
                return apology ("Invalid Input: Must buy at least one shares")
        if int(request.form.get("shares")) <= 0:
            return apology ("Invalid Input: Must buy at least one share")
            
        # ensure user has enough cash for purchase
        shares = int(request.form.get("shares"))
        purchase = float(lookup(request.form.get("symbol"))["price"]) * shares
        cash = db.execute("SELECT cash FROM 'users' WHERE id = :user_id", user_id = session["user_id"])[0]["cash"]
        if cash < purchase:
            return apology("Not enough cash for transaction")
            
        # update database
        db.execute("UPDATE 'users' SET cash = :tmp WHERE id = :user_id", tmp = cash - purchase, user_id = session["user_id"])
        db.execute("INSERT INTO 'portfolio' (name, symbol, moved, price, userid) VALUES(:name, :symbol, :moved, :price, :userid)",
            name = lookup(request.form.get("symbol"))["name"], symbol = lookup(request.form.get("symbol"))["symbol"],
            moved = shares, price = usd(lookup(request.form.get("symbol"))["price"]), userid = session["user_id"])
            
        return redirect(url_for("index"))
        
    else:
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    data = db.execute("SELECT timestamp, symbol, moved, price FROM portfolio WHERE userid = :userid", userid = session["user_id"])
    return render_template("history.html", table = data)
    
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username = request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        # ensure valid stock lookup
        stock = lookup(request.form.get("symbol"))
        if stock != None:
            print(stock["price"])
            stock["price"] = usd(stock["price"])[1:]
            return render_template("quoted.html", stock = stock)
        else:
            return apology("Enter a valid stock symbol")
    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    if request.method == "POST":
        # ensure username submitted
        if not request.form.get("username"):
            return apology("must provide username")
        
        # ensure username doesn't exist
        rows = db.execute("SELECT * FROM users WHERE username = :username", username = request.form.get("username"))
        if len(rows) != 0:
            return apology("username already exists")
        
        # ensure password fields submitted
        if not request.form.get("password"):
            return apology("must provide password")
        if not request.form.get("password2"):
            return apology("must retype password")
        
        # ensure passwords match
        if request.form.get("password") != request.form.get("password2"):
            return apology("passwords must match")
        
        # store user in database
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :password_hash)", username = request.form.get("username"), 
            password_hash = pwd_context.encrypt(request.form.get("password")))
            
        # automatically log user in
        session["user_id"] = db.execute("SELECT * FROM users WHERE username = :username", username = request.form.get("username"))[0]["id"]
            
        #return redirect for homepage
        return redirect(url_for("index"))
        
    # else if user reached route via GET 
    else:
        return render_template("register.html")
    
@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    if request.method == "POST":
        # ensure valid stock symbol
        stock = lookup(request.form.get("symbol"))
        if stock == None:
            return apology("Enter a valid stock symbol")
            
        # ensure valid number of shares
        if not str.isalnum(request.form.get("shares")):
            return apology ("Invalid Input: Must sell integer number of shares")
        if str.isalpha(request.form.get("shares")) or request.form.get("shares") == None:
                return apology ("Invalid Input: Must Sell at least one shares")
        
        shares = int(request.form.get("shares")) 
        tosell = db.execute("SELECT SUM(moved) FROM PORTFOLIO WHERE symbol = :symbol AND userid = :userid", 
            symbol = stock["symbol"], userid = session["user_id"])  
        
        if shares <= 0:
            return apology ("Must sell at least one share")
        if tosell[0]["SUM(moved)"] == None:
            return apology ("You don't have any shares of that stock")
        if shares > tosell[0]["SUM(moved)"]:
            return apology ("You don't have that many shares")
        
        # update databases
        cash = db.execute("SELECT cash FROM 'users' WHERE id = :user_id", user_id = session["user_id"])[0]["cash"]
        cash += shares * stock["price"]
        db.execute("UPDATE 'users' SET cash = :tmp WHERE id = :user_id", tmp = cash, user_id = session["user_id"])
        db.execute("INSERT INTO 'portfolio' (name, symbol, moved, price, userid) VALUES(:name, :symbol, :moved, :price, :userid)",
            name = lookup(request.form.get("symbol"))["name"], symbol = lookup(request.form.get("symbol"))["symbol"],
            moved = -shares, price = usd(lookup(request.form.get("symbol"))["price"]), userid = session["user_id"])
        
        return redirect(url_for("index"))
    else:
        return render_template("sell.html")

@app.route("/addcash", methods=["GET", "POST"])
@login_required
def addcash():
    '''Allows user to add cash to account'''
    if request.method == 'POST':
        # ensure proper usage
        if not str.isalnum(request.form.get("cash")) or str.isalpha(request.form.get("cash")):
            return apology("Must enter numeric value")
        if float(request.form.get("cash")) <= 0:
            return apology("Must enter positive value")
    
        # update cash
        cash = db.execute("SELECT cash FROM 'users' WHERE id = :user_id", user_id = session["user_id"])[0]["cash"]
        cash += float(request.form.get("cash"))
        
        # update databases
        db.execute("UPDATE 'users' SET cash = :tmp WHERE id = :user_id", tmp = cash, user_id = session["user_id"])
        db.execute("INSERT INTO 'portfolio' (symbol,  price, userid) VALUES(:symbol, :price, :userid)", symbol = "CASH", 
            price = usd(float(request.form.get("cash"))), userid = session["user_id"])
        
        # redirect to index
        return redirect(url_for("index"))
    
    else:
        return(render_template("addcash.html"))