# CS50-Final-Project
CS50 Final Project
Luke Benz
CS50 Final Project
December, 2016
documentation.txt

* [Video of me explaining my project](https://www.youtube.com/watch?v=CBKQNdGYGCc)
* [Article I wrote about this project](http://sports.sites.yale.edu/cs50-what-i-learned-0)

User's Manual for NBA Shot Charts: A Basketball Data Visualization

CONFIGURING
Note: For whatever reason, the colors used in this project's graphics display better in Safari than other browsers. If possible, 
please run CS50 IDE in Safari. Also, if the server seems to be running slowly, simply quit and try again. Upon closing and
reopening the web server, the program will run much faster.

1. Set  /finalproject as the working directory using the following command
~/workspace/ $ cd finalproject

2. Install all necceseary Python Packages as follows:
~/workspace/finalproject/ $ sudo pip3 install --user -r requirements.txt
NOTE: The python matplotlib can take a few minutes to install. Please be patient.

3. Get the SQL database nbadata.db from dropbox and place it in the directory /finalproject.

4. In one terminal, use phpliteadmin to open the SQL database nbadata.db, as follows:
~/workspace/ $ cd finalproject
~/workspace/finalproject/ $ phpliteadmin nbadata.db 

5. In a seperate terminal, start flask, as follows:
~/workspace/finalproject/ $ flask run

6. Open Web Sever by clicking CS50 IDE tab in upper left-hand corner of screen

TITLE SCREEN
1. Upon opening the local web server, you will be brought to the title screen of the project. Simply click the orange "Get Started"
button to begin


PLAYER SELECT
1.  Select an NBA player to examin
2.  The player must have been in the NBA during either the 2013-2014 season, or the 2014-2015 season.
3.  When entering the player's name, you need not worry about capitilzation, but do take care to spell the player's name correctly
4.  Should you misspell the name of your desired player, or enter an invalid player, you will be brought to an error screen 
    prompting you to reselect your player.
5.  Upon successful selecting a player you will be brought to the control panel


CONTROL PANEL
1.  The control panel gives you four buttons to choose from, each linking to a different page
2.  Click the green "Change Player" button to choose a new player from the player select page
3.  Click the orange "Shot Chart" button to render a graphic displaying the player's shooting success by location on the court
4.  Click the red "Assist Chart" button to render a graphic displaying the locations of shots which were assisted by your selected 
    player.
5.  Click the light blue "Rebound Chart" button to render a graphic displaying the locations of shots for whihc your selected player
    secured the rebound.
    

SHOT CHART
1.  This page renders a graphic of your chosen player's made and missed shot locations on an NBA court. Red markers indicate a 
    missed shot, while green markers indicated a made shot.
2.  To the right of the chart, you will notice some relevant shooting stats that have been calculated for your choosen player.
3.  In the bottom right hand corner of the screen, there is a navigation bar for the graphic.
    A. The Magnifying Glass: Allows user to draw a rectangle on the court to zoom-in on
    B. The Arrow Pad: Allows user to drag around and navigate their way around the court
    C. The Home Icon: Sets plot to original orientation
    Note: After selecting the magnifying glass or arrow pad icon, the user must click those respective icons again to de-select 
    them.
4.  Click the red "Assist Chart" button to render a graphic displaying the locations of shots which were assisted by your selected 
    player.
5.  Click the light blue "Rebound Chart" button to render a graphic displaying the locations of shots for whihc your selected player
    secured the rebound.
6.  Click the dark blue "Control Panel" button to return to the control panel.
7.  Click the green "Change Player" button to choose a new player from the player select page.


ASSIST CHART
1.  This page renders a graphic of the locations of shots for which your chosen player was credited with the assist.
2.  To the right of the chart, you will notice some relevant assisting stats that have been calculated for your choosen player.
3.  In the bottom right hand corner of the screen, there is a navigation bar for the graphic.
    A. The Magnifying Glass: Allows user to draw a rectangle on the court to zoom-in on
    B. The Arrow Pad: Allows user to drag around and navigate their way around the court
    C. The Home Icon: Sets plot to original orientation
    Note: After selecting the magnifying glass or arrow pad icon, the user must click those respective icons again to de-select 
    them.
4.  Click the orange "Shot Chart" button to render a graphic displaying the player's shooting success by location on the court
5.  Click the light blue "Rebound Chart" button to render a graphic displaying the locations of shots for whihc your selected player
    secured the rebound.
6.  Click the dark blue "Control Panel" button to return to the control panel
7.  Click the green "Change Player" button to choose a new player from the player select page


ASSIST CHART
1.  This page renders a graphic of the locations of shots for which your chosen player secured the rebound.
2.  To the right of the chart, you will notice some relevant assisting stats that have been calculated for your choosen player.
3.  In the bottom right hand corner of the screen, there is a navigation bar for the graphic.
    A. The Magnifying Glass: Allows user to draw a rectangle on the court to zoom-in on
    B. The Arrow Pad: Allows user to drag around and navigate their way around the court
    C. The Home Icon: Sets plot to original orientation
    Note: After selecting the magnifying glass or arrow pad icon, the user must click those respective icons again to de-select 
    them.
4.  Click the orange "Shot Chart" button to render a graphic displaying the player's shooting success by location on the court
5.  Click the red "Assist Chart" button to render a graphic displaying the locations of shots which were assisted by your selected 
    player.
6.  Click the dark blue "Control Panel" button to return to the control panel
7.  Click the green "Change Player" button to choose a new player from the player select page.
