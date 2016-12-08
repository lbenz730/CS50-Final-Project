import matplotlib as mpl
# be able to show mpl plots without additional backend server running
mpl.use('Agg')

import matplotlib.pyplot as plt
import mpld3
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, url_for
from drawcourt import *
from helpers import *

# Create global variable to keep track of chosen player
def create_player():
    global PLAYER  
    PLAYER = "" 
create_player()

# Create a function that allows modification to global variable PLAYER
def update_player(new):
    global PLAYER
    PLAYER = new

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

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///nbadata.db")

@app.route("/")
def home():
    """render home screen."""
    return render_template("home.html")
    
@app.route("/playerselect", methods=["GET", "POST"])
def playerselect():
    """render page that allows user to choose player."""
    if request.method == "POST":
        # Ensure player entered
        update_player(request.form.get("player"))
        if request.form.get("player") == "" or request.form.get("player") == None:  
            return redirect(url_for("error"))
        
        # Ensure player is valid player
        rows = db.execute("SELECT player FROM playbyplay WHERE player LIKE :player", player = PLAYER)
        if len(rows) == 0:
            return redirect(url_for("error"))
        
        # Update PLAYER to reflect the way player is entered in database
        update_player(rows[0]["player"])
       
        # else redirect to controlpanel
        return redirect(url_for("controlpanel"))
        
    else:
        return render_template("playerselect.html")

@app.route("/controlpanel", methods=["GET", "POST"])
def controlpanel():
    """render controlpanel."""
    if request.method == "POST":
        return redirect(url_for("home"))
    else:
        print
        return render_template("controlpanel.html", player = PLAYER)

@app.route("/error")
def error():
    """display error message."""
    return render_template("error.html")

@app.route("/shotchart")
def shotchart():
    """render shot chart."""
    
    # Get all shots attempted by player
    sql = "SELECT * FROM playbyplay WHERE player = :player AND (event_type = 'shot' OR event_type = 'miss') AND"
    sql += "(data_set = '2013-2014 Regular Season' or data_set = '2014-2015 Regular Season')"
    rows = db.execute(sql, player = PLAYER)
    
    # Extract (x, y) coordinates of player's made shots
    shotXmade = []
    shotYmade = []
    for i in range(len(rows)):
        if rows[i]["event_type"] == "shot" and rows[i]["original_x"] != "unknown" and rows[i]["original_y"] != "unknown":
            shotXmade.append(rows[i]["original_x"])   
            shotYmade.append(rows[i]["original_y"])
    
    # Extract (x, y) coordinates of player's missed shots
    shotXmissed = []
    shotYmissed = []
    for i in range(len(rows)):
        if rows[i]["event_type"] == "miss" and rows[i]["original_x"] != "unknown" and rows[i]["original_y"] != "unknown":
            shotXmissed.append(rows[i]["original_x"])   
            shotYmissed.append(rows[i]["original_y"])
    
    # Plot Shots as scatterplot
    plt.figure(figsize = (10, 8.5))
    missed = plt.scatter(shotXmissed, shotYmissed, color = "red", marker = "o")
    made = plt.scatter(shotXmade, shotYmade, color = "green", marker = "o")
   
    # Create Legend
    labels = ['Made Shot','Missed Shot']
    colors = ['green','red']
    tmp = []
    for i in range(len(colors)):
        tmp.append(mpl.patches.Rectangle((0, 0), 1, 1, fc = colors[i]))
        plt.legend(tmp, labels, loc = 1)
    
    # Draw Court
    draw_court(outer_lines = True)
    plt.xlim(300, -300)
    plt.ylim(-100, 500)
    
    # Turn chart into html chunk
    chart = mpld3.fig_to_html(plt.gcf())
    
    # Get relevant stats 
    stats = shotStats(rows, shotXmade)
   
    # render chart
    return render_template("shotchart.html", chart = chart, player = PLAYER, stats = stats)
    
@app.route("/assistchart")
def assistchart():
    """render assist chart."""
    
    # Get all shots on which were assisted by player
    sql = "SELECT * FROM playbyplay WHERE assist = :player AND (data_set = '2013-2014 Regular Season' or data_set = '2014-2015 Regular Season')"
    rows = db.execute(sql, player = PLAYER)
    
    # Extract (x,y) coordinates of the shots for which player had the assist
    assistX = []
    assistY = []
    for i in range(len(rows)):
        if rows[i]["original_x"] != "unknown" and rows[i]["original_y"] != "unknown":
            assistX.append(rows[i]["original_x"])   
            assistY.append(rows[i]["original_y"])
    
        
    # Plot Shots for which player had the assist
    plt.figure(figsize=(10, 8.5))
    plt.scatter(assistX, assistY, marker = "o", color = "#FF4500")
    
    # Create Legend
    labels = ["Assisted Shot Location"]
    colors = ["#FF4500"]
    tmp = []
    for i in range(len(colors)):
        tmp.append(mpl.patches.Rectangle((0, 0), 1, 1, fc = colors[i]))
        plt.legend(tmp, labels, loc = 1)
    
    # Draw Court
    draw_court(outer_lines = True)
    plt.xlim(300, -300)
    plt.ylim(-100, 500)
    
    # Turn chart into html chunk
    chart = mpld3.fig_to_html(plt.gcf())
    
    # Get Relevant Stats
    stats = assistStats(rows)
    
    return render_template("assistchart.html", chart = chart, player = PLAYER, stats = stats)

@app.route("/reboundchart")
def reboundchart():
    """render rebound chart."""
    
    # Get all rebounds by player
    sql = "SELECT * FROM playbyplay WHERE rebound = :player AND"
    sql += " (data_set = '2013-2014 Regular Season' OR data_set = '2014-2015 Regular Season')"
    rows = db.execute(sql, player = PLAYER)
    
    # Get PLAYER's Team
    playerteam = db.execute("SELECT team FROM playbyplay WHERE player = :player", player = PLAYER)[0]
    # Get (x,y) coordinates of shots for which PLAYER secured the rebound
    orebX = []
    orebY = []
    drebX = []
    drebY = []
    
    # Classify rebounds as offensive/defensive and handle accordingly
    for i in range(len(rows)):
        if rows[i]["original_x"] != "unknown" and rows[i]["original_y"] != "unknown":
            # Offensive Rebounds
            if playerteam["team"] == rows[i]["team"]:
                orebX.append(rows[i]["original_x"])   
                orebY.append(rows[i]["original_y"])
            # Deffensive Rebounds
            else:
                drebX.append(rows[i]["original_x"])   
                drebY.append(rows[i]["original_y"])
                
    # Plot Shots for which player had the rebound
    plt.figure(figsize=(10, 8.5))
    plt.scatter(orebX, orebY, marker = "o", color = "magenta")
    plt.scatter(drebX, drebY, marker = "o", color = "#40E0D0")
    
    # Create Legend
    labels = ["Offensive Rebound", "Defensive Rebound"]
    colors = ["magenta", "#40E0D0"]
    tmp = []
    for i in range(len(colors)):
        tmp.append(mpl.patches.Rectangle((0, 0), 1, 1, fc = colors[i]))
        plt.legend(tmp, labels, loc = 1)
        
     # Draw Court
    draw_court(outer_lines = True)
    plt.xlim(300, -300)
    plt.ylim(-100, 500)
    
    # Turn chart into html chunk
    chart = mpld3.fig_to_html(plt.gcf())
    
    # Get Relevant Rebounding Stats
    stats = reboundStats(rows, orebX, drebX)
  
    return render_template("reboundchart.html", chart = chart, player = PLAYER, stats = stats)