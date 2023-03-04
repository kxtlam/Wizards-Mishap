###Dodging objects game###
#Resolution used: 1536x864

import tkinter as tk
from tkinter import Canvas, Frame, Label
from PIL import Image, ImageTk
from random import randint


##Function that calls the menu screen 
def menu (canvas):

    canvas.destroy ()
    global bg           #Need to set bg image as global since is created local to menu function
    frame = Frame (root)
    frame.pack(expand=1, fill="both")

    #Preloading our graphics (background and button images)
    bg = Image.open ("images/startBg.png")
    bg = bg.resize ((1536,864))                 #Resizing background image to correct resolution
    bg = ImageTk.PhotoImage(bg)     

    #Generating label for bg image to place on root
    bgLabel= Label(frame, image=bg)
    bgLabel.place (x=0,y=0,relwidth=1, relheight=1)

    #Creates the buttons with an image and text
    button = Image.open ("images/menuButton.png")  
    button = button.resize ((360,120))
    button = ImageTk.PhotoImage(button)

    startBtn = tk.Button (frame, image=button, text= "Start game", font= ('Aerial 35 bold'), compound="center", command= lambda: startGame(frame))
    controlsBtn = tk.Button (frame, image=button, text= "Controls", font= ('Aerial 35 bold'), compound="center", command= lambda: controls(frame))
    leaderboardBtn = tk.Button (frame, image=button, text= "Leaderboards", font= ('Aerial 35 bold'), compound="center", command= lambda: leaderboard(frame))
    exitBtn = tk.Button (frame, image=button, text= "Exit game", font= ('Aerial 35 bold'), compound="center", command= lambda: root.destroy())


    startBtn.image = button         #References the image object- fixed my issue where button images weren't showing up
    controlsBtn.image = button
    leaderboardBtn.image = button
    exitBtn.image = button

    #Displays the buttons with pad spaces inbetween each of them
    startBtn.pack (pady=(200,20))           #Padded top by 200px and bottom by 40px
    controlsBtn.pack(pady=20)       
    leaderboardBtn.pack(pady=20)
    exitBtn.pack(pady=20)


##Class defining the attributes of the player controlled sprite
class Sprite:
    def __init__(self, root = None):        #Initialising class attributes
        self.root = root
        self.canvas = canvas
        self.x = 764                                 #Sets player beginning position to middle bottom of game screen
        self.y = 780

        #Preloading player sprite facing left
        self.imgL = Image.open ("images/playerCharacter_L.png")
        self.imgL = self.imgL.resize ((130,174))
        self.imgL = ImageTk.PhotoImage(self.imgL)    

        #Preloading player sprite facing right
        self.imgR = Image.open ("images/playerCharacter_R.png")
        self.imgR = self.imgR.resize ((130,174))
        self.imgR = ImageTk.PhotoImage(self.imgR)   

        self.player = self.canvas.create_image(self.x, self.y, image=self.imgL)
        self.currentCoordsPL = self.canvas.coords(self.player)

    #Player sprite will move left when left key is pressed
    def left (self):
        #Switches player sprite to face left
        coords= self.canvas.coords(self.player)
        if pause == False:
            self.canvas.delete(self.player)
            self.player = self.canvas.create_image(coords[0],coords[1], image=self.imgL)

        if coords [0] < 50:                          #Prevents player from going off visible screen on the left
            pass
        else:
            if pause == False:
                self.canvas.move (self.player,-40,0)    #Moves sprite left by 30 pixels only if game isn't paused

        self.currentCoordsPL = self.canvas.coords(self.player)

    #Player sprite will move right when right key is pressed
    def right (self):
        #Switches player sprite to face right
        coords= self.canvas.coords(self.player)
        if pause == False:
            self.canvas.delete(self.player)
            self.player = self.canvas.create_image(coords[0],coords[1], image=self.imgR)

        if coords [0] > 1480:                       #Prevents player from going off visible screen on the right
            pass
        else:
            if pause == False:
                self.canvas.move (self.player,40,0)     #Moves sprite right by 30 pixels only if game isn't paused

        self.currentCoordsPL = self.canvas.coords(self.player)


##Class defining the attributes of the falling fireballs that players have to dodge
class Fireballs:
    def __init__ (self, root = None):
        self.root = root
        self.canvas = canvas
        self.x = 0
        self.y = 0

        self.xPos = randint (0,1536)
        self.fireball = self.canvas.create_oval(self.xPos,0,self.xPos+35,50, outline = "white", fill = "red", width = 1)      #Displaying the fireball
        self.fireOrange = self.canvas.create_oval(self.xPos+5,15,self.xPos+30,50, outline = "white", fill = "orange", width = 1)    #Displaying orange fireball addition

        self.falling ()

    def unfreeze (self):          #Function that calls falling function again to make fireballs continue moving
        global freeze
        freeze = False
        self.falling ()

    #Makes the fireball fall on the screen
    def falling (self):
        coordsFire = self.canvas.coords(self.fireball)      #Gets current coordinates of fireball
        if coordsFire [1] < 10:                             #If fireball is at top of window, randomly generate a new falling speed and x position 
            self.speed = randint (0,35)         
            self.xPos = randint (0,1536)

        self.canvas.move(self.fireball, 0, 10)              #Repeatedly increase y by 10 to make fireball fall
        self.canvas.move(self.fireOrange, 0, 10)       
        self.currentCoords = self.canvas.coords(self.fireball)
        
        playerCoords = getattr(player,"currentCoordsPL")   
        player_x2 = playerCoords [0] + 87.5                 #Gets the x coordinates of the corners of player sprite (since playerCoords gets centre of sprite image)
        player_x1 = playerCoords [0] - 87.5
        player_y = playerCoords [1] - 87.5                  #Gets y coordinate of top of player sprite 

        ##Collision detection code:     
        touched = False
        #If the corners of player sprite touch fireball, then touched = True
        if (self.currentCoords[0] <= player_x1 <= self.currentCoords[2]) and (player_y <= self.currentCoords[1]):
            touched = True
        elif (self.currentCoords[0] <= player_x2 <= self.currentCoords[2]) and (player_y <= self.currentCoords[1]):
            touched = True
        #If fireball is inside the player sprite (i.e. between its two x values), then tcuched = True
        elif (player_x1 <= self.currentCoords[0]) and (self.currentCoords[2] <= player_x2) and (player_y <= self.currentCoords[1]):
            touched = True

        if coordsFire [3] > 864 or touched == True:                   #If fireball is at bottom of window, reset its coordinates to the top of the screen at x = xPos
            self.canvas.moveto(self.fireball,self.xPos,-50)             #Also resets if player touches fireball
            self.canvas.moveto(self.fireOrange,self.xPos+5,-35)       
            self.currentCoords = self.canvas.coords(self.fireball)

            #Lose a life if player sprite touches fireball and updates lives counter
            global score
            global lives
            if touched == True:         
                lives -= 1
                livesLabel.config (text="Lives: " + str(lives))
                
                #If you run out of lives, progress to the end game screen
                if lives == 0:
                    endGame(score)
            else:
                score += 1
                scoreLabel.config (text="Score: " + str(score))     #Incrementing score and updating it on screen

            #Difficulty increase- When below score of 100, a fireball is added every 25 points, when above 100 is added every 50 points instead
            if score <= 100 and score % 25 == 0:
                fire = Fireballs (root)
                fireList.append (fire)
            elif score > 100 and score % 60 == 0:
                fire = Fireballs (root)
                fireList.append (fire)

        if pause == False and freeze == False:               #Only runs if game isn't paused and if cheatCode_freeze hasnt been called
            self.canvas.after(self.speed, self.falling)         #Call falling function again to make it loop the falling animation
        if freeze == True:
            canvas.after(2000, self.unfreeze)   #Calls unfreeze function that sets freeze = False and makes fireballs fall again


##Main game function
def startGame(frame):
    frame.destroy ()                                     #Destroys menu frame to remove widgets and reset root 
    global canvas

    canvas = Canvas(root, bg="black")                    
    canvas.pack (expand=1, fill="both")                  #Created new global canvas that covers root window 

    #Setting base values for global variables
    global score, lives, scoreLabel, livesLabel, player, fireList, pauseCount, pause, bossPress, recoverLife, freeze, remainingFreezes, changed, resume, remainingRecoveryLabel, remainingFreezesLabel
    if resume == False:         #These values are set if start game is a new game (i.e. not an old save file)
        score = 0
        pauseCount = 0
        remainingFreezes = 5
        bossPress = 0
        lives = 5
        recoverLife = 3
        numFireballs = 3
        changed = False
    else:                       #This block of code runs if it is a continuation from a previous save
        file = open ("saveFile.txt")                   
        for x in file:
            all_data = x
        all_data_list = all_data.split ()                #Reads all the save data and stores them back into their respective variables
        numFireballs = int(all_data_list [2])
        score = int(all_data_list [3])
        lives = int(all_data_list [4])
        remainingFreezes = int(all_data_list [5])
        recoverLife = int(all_data_list [6])
        file.close ()

    pause = False
    freeze = False


    #Creating score and lives label at top right of game screen
    livesLabel = Label(canvas, text="Lives: " + str(lives), font=('Consolas', 15), bg = "black", fg = "white")
    livesLabel.pack(padx=20, pady=20, side="top", anchor="ne")
    scoreLabel = Label(canvas, text="Score: " + str(score), font=('Consolas', 15), bg = "black", fg = "white")
    scoreLabel.pack(padx=20, pady=10, side="top", anchor="ne")
    
    #Only displays remaining lives and freezes at the start of game if it is a continuation from save file and has been used before
    if resume == True and recoverLife != 3:
        remainingRecoveryLabel = Label(canvas, text="Life recoveries left: " + str(recoverLife), font=('Consolas', 15), bg = "black", fg = "white")
        remainingRecoveryLabel.pack(padx=20, pady=10, side="top", anchor="ne")
    if resume == True and remainingFreezes != 5:
        remainingFreezesLabel = Label(canvas, text="Freezes left: " + str(remainingFreezes), font=('Consolas', 15), bg = "black", fg = "white")
        remainingFreezesLabel.pack(padx=20, pady=10, side="top", anchor="ne")
    
    #Creating instances of player sprite and fireballs
    player = Sprite (canvas)     

    if resume == True:
        player.x = float(all_data_list [0])
        player.y = float(all_data_list [1])
        resume = False                           #Resets resume to false now
        
    fireList = []
    for x in range (int(numFireballs)):
        fire = Fireballs (canvas)
        fireList.append (fire)

    #Setting all player control keybinds 

    if changed == False:   
        root.bind ("<Left>", lambda event: player.left())    #Calls left function when left button is pressed, and right button when right button is pressed
        root.bind ("<Right>", lambda event: player.right())  
    root.bind ("<p>", lambda event: pauseGame())
    root.bind ("<b>", lambda event: bossKey())
    root.bind ("<c>", lambda event: cheatCode_recoverLife())
    root.bind ("<v>", lambda event: cheatCode_freeze())


##Displays the game over screen where you can see your score and save it onto the leaderboard
def endGame (score):
    #Deleting labels and layering a new canvas on top for the end game screen (have to delete labels otherwise canvas doesn't layer on properly)
    livesLabel.destroy()
    scoreLabel.destroy()
    if remainingFreezes < 5:
        remainingFreezesLabel.destroy()
    if recoverLife < 3:
        remainingRecoveryLabel.destroy()

    global pause    #Pauses the game underneath in the previous canvas so that it doesn't keep running
    pause = True
    root.unbind ("<p>") #Temporarily unbinding keys so that it doesn't activate while typing (previous game canvas is still underneath)
    root.unbind ("<b>")
    root.unbind ("<c>")
    root.unbind ("<v>")

    #Creating the new canvas
    canvas2 = Canvas (canvas, background="black")
    canvas2.pack(expand=1, fill="both")    

    #Displays all the text on the screen
    game_over = Label(canvas2, text="GAME OVER!", font=('Consolas', 45), bg = "black", fg = "white")
    score_text = Label(canvas2, text="Your score:", font=('Consolas', 45), bg = "black", fg = "white")
    score_result = Label(canvas2, text=score, font=('Consolas', 45), bg = "black", fg = "white")
    enter_name = Label(canvas2, text="Enter your name to add it to the leaderboard:", font=('Consolas', 20), bg = "black", fg = "white")
    game_over.pack (pady = 50, side = "top", anchor = "center")
    score_text.pack (pady = (100,20), side = "top", anchor = "center")
    score_result.pack (pady = 40, side = "top", anchor = "center")
    enter_name.pack (pady = 40, side = "top", anchor = "center")

    #Displays entry box for user to type username in
    save_name = tk.Entry(canvas2, font=('Consolas', 15), width = 20) 
    canvas2.create_window(760, 650, window=save_name)

    #Button takes input in entry box and passes them to save_score function
    return_to_menu = tk.Button(canvas2, text="Save name and return to menu", command= lambda: save_score(canvas, save_name))
    return_to_menu.pack(padx=300, pady=50, side="bottom", anchor="se")


##Saves the player entered name and score achieved in leaderboard.txt file to be used in the leaderboard
def save_score (canvas, save_name):
    userIN = save_name.get()
    #Produces an error popup window if player leaves the username box empty
    if userIN == "":
        error_win = tk.Toplevel (root, background="white")
        x = (error_win.winfo_screenwidth()/2) - 300       
        y = (root.winfo_screenheight()/2) - 25
        error_win.geometry ("200x50+%d+%d" % (x,y-25))
        error_win.title ("Error!")
        error_message = Label(error_win, text="Enter a name!", font=('Consolas', 12), bg = "white", fg = "red")
        error_message.pack ()
    else:
        #Saves the username and score in leaderboard.txt file
        file = open ("leaderboard.txt", "a")
        file.write (str(userIN)+ " ")
        file.write (str(score)+ " ")
        file.close()
        menu(canvas)


##Function that pauses the game when keyboard button 'p' is pressed
def pauseGame ():
    global pause, pauseCount, pausedLabel, return_to_menu
    pauseCount += 1
    if pauseCount % 2 == 1:      #If pause = odd, then next p button press will pause the game
        pause = True
        pausedLabel = Label(canvas, text="PAUSED", font=('Consolas',30),bg = "black", fg = "white")
        pausedLabel.pack(pady=100, anchor="center")

        return_to_menu = tk.Button(canvas, text="Save and return to menu",  font=('Consolas',15), command= lambda: save_game(canvas))
        return_to_menu.pack(pady=10, anchor="center")
           
    else:                   #If puase = even, then next p button press will unpause the game
        pause = False
        pausedLabel.destroy()         
        return_to_menu.destroy ()      
        
        for x in range (len(fireList)):         #Unfreezes the fireballs and continues the game and removes the PAUSED label
            Fireballs.falling(fireList[x])  


##Function that saves the current state of the game which players can resume from when they press start game
def save_game (canvas):
    #Unbinding keys so that they aren't still bound out of the game section
    global left_key, right_key, fireList, resume, pauseCount
    resume = True
    try:
        root.unbind (left_key)
        root.unbind (right_key)
    except: 
        root.unbind ("<Left>")
        root.unbind ("<Right>")

    root.unbind ("<p>") 
    root.unbind ("<b>")
    root.unbind ("<c>")
    root.unbind ("<v>")

    #Writing the player coordinates, number of fireballs on screen, score, lives, number of freezes remaining, number of extra lives remaining to saveFile.txt
    file = open("saveFile.txt", "w")
    x = player.currentCoordsPL [0]
    y = player.currentCoordsPL [1]
    num_fireballs = len (fireList)
    saveData = str(x) + " " + str(y) + " " + str(num_fireballs) + " " + str(score) + " " + str(lives) + " " + str(remainingFreezes) + " " + str(recoverLife) 
    file.write (saveData)
    file.close()
    pauseCount += 1      #Incremented pause so that next time pause is pressed, it doesn't try to unpause a game that isn't paused
    menu(canvas)
    pass


##Function that pauses game and displays an image mimicking productivity
def bossKey ():
    global bossPress, workImageLabel, pause, livesLabel, scoreLabel, remainingFreezes, remainingFreezesLabel, recoverLife, remainingRecoveryLabel
    bossPress += 1
    #Bosskey is activated- Pauses the game and displays the fake work image
    if bossPress % 2 == 1:
        pause = True
        livesLabel.destroy ()               #Removes lives and score label to avoid getting in the way of boss key image
        scoreLabel.destroy ()
        if remainingFreezes <= 4:
            remainingFreezesLabel.destroy ()
        if recoverLife <= 2:
            remainingRecoveryLabel.destroy()

        workImage = Image.open ("images/workImage.jpg")                         
        workImage = workImage.resize ((1537,864))           #Loads in and displays "work" image to hide the game screen
        workImage = ImageTk.PhotoImage(workImage)  
        workImageLabel = Label (canvas, image=workImage)
        workImageLabel.image = workImage
        workImageLabel.pack (anchor="center")
    #Bosskey is deactivated- Removes fake work image and resumes the game
    else:
        pause = False
        workImageLabel.destroy()
        livesLabel = Label(canvas, text="Lives: " + str(lives), font=('Consolas', 15), bg = "black", fg = "white")
        livesLabel.pack(padx=20, pady=20, side="top", anchor="ne")

        scoreLabel = Label(canvas, text="Score: " + str(score), font=('Consolas', 15), bg = "black", fg = "white")
        scoreLabel.pack(padx=20, pady=10, side="top", anchor="ne")

        if remainingFreezes <= 4:
            remainingFreezesLabel = Label(canvas, text="Freezes left: " + str(remainingFreezes), font=('Consolas', 15), bg = "black", fg = "white")
            remainingFreezesLabel.pack(padx=20, pady=10, side="top", anchor="ne")

        if recoverLife <= 2:
            remainingRecoveryLabel = Label(canvas, text="Life recoveries left: " + str(recoverLife), font=('Consolas', 15), bg = "black", fg = "white")
            remainingRecoveryLabel.pack(padx=20, pady=10, side="top", anchor="ne")
            
        for x in range (len(fireList)):         #Unfreezes the fireballs and continues the game and removes the PAUSED label
            Fireballs.falling(fireList[x])  


##Cheat code that temporarily freezes the fireballs for 2 seconds- max of 5 times
def cheatCode_freeze ():
    global freeze, remainingFreezes, remainingFreezesLabel
    if remainingFreezes <= 0:       #Only freezes if there are any remaining uses
        pass
    else:
        freeze = True
        remainingFreezes -= 1           #Decrements the number of remaining uses and introduces the "Freezes left" label to the screen
        if remainingFreezes == 4:
            remainingFreezesLabel = Label(canvas, text="Freezes left: " + str(remainingFreezes), font=('Consolas', 15), bg = "black", fg = "white")
            remainingFreezesLabel.pack(padx=20, pady=10, side="top", anchor="ne")
        else:
            remainingFreezesLabel.config (text="Freezes left: " + str(remainingFreezes))            


##Cheat code that lets you recoverLife max 3 lives by pressing the "c" key
def cheatCode_recoverLife ():
    global recoverLife, lives, remainingRecoveryLabel
    if lives == 5 or recoverLife <= 0:                   #Only lets you recover lives if you don't have full health and you have uses left
        pass
    else:
        recoverLife -= 1
        lives += 1
        livesLabel.config (text="Lives: " + str(lives))     #Updates number of lives and counter, and introduces remaining life recoveries to screen
        if recoverLife == 2:
            remainingRecoveryLabel = Label(canvas, text="Life recoveries left: " + str(recoverLife), font=('Consolas', 15), bg = "black", fg = "white")
            remainingRecoveryLabel.pack(padx=20, pady=10, side="top", anchor="ne")
        else:
            remainingRecoveryLabel.config (text="Life recoveries left: " + str(recoverLife))


##Gets user input and changes the buttons accordingly
def change_buttons(leftEntry, rightEntry):
    global left_key, right_key
    left_key = leftEntry.get()
    right_key = rightEntry.get()

    #If user inputs more than one character into box, produces an error pop-up window
    if len(left_key) > 1 or len(right_key) > 1:
        error_win = tk.Toplevel (root, background="white")
        x = (error_win.winfo_screenwidth()/2) - 300        #Places window at centre of screen
        y = (root.winfo_screenheight()/2) - 25
        error_win.geometry ("500x50+%d+%d" % (x,y-25))
        error_win.title ("Error!")
        error_message = Label(error_win, text="Controls can only be one character long!", font=('Consolas', 12), bg = "white", fg = "red")
        error_message.pack ()

    #If user inputs the same character for both boxes, produces an error pop-up window
    elif left_key == right_key:
        error_win = tk.Toplevel (root, background="white")
        x = (error_win.winfo_screenwidth()/2) - 300        
        y = (root.winfo_screenheight()/2) - 25
        error_win.geometry ("500x50+%d+%d" % (x,y-25))
        error_win.title ("Error!")
        error_message = Label(error_win, text="Cannot enter the same key for both left and right!", font=('Consolas', 12), bg = "white", fg = "red")
        error_message.pack ()
    
    #If user leaves either box plank when submitting, produces an error
    elif left_key == "" or right_key == "":
        error_win = tk.Toplevel (root, background="white")
        x = (error_win.winfo_screenwidth()/2) - 300       
        y = (root.winfo_screenheight()/2) - 25
        error_win.geometry ("500x50+%d+%d" % (x,y-25))
        error_win.title ("Error!")
        error_message = Label(error_win, text="Enter a key in both boxes!", font=('Consolas', 12), bg = "white", fg = "red")
        error_message.pack ()

    elif left_key in ["p", "c", "v", "b"] or right_key in ["p", "c", "v", "b"]:
        error_win = tk.Toplevel (root, background="white")
        x = (error_win.winfo_screenwidth()/2) - 300       
        y = (root.winfo_screenheight()/2) - 25
        error_win.geometry ("500x50+%d+%d" % (x,y-25))
        error_win.title ("Error!")
        error_message = Label(error_win, text="Key(s) already bound to another command!", font=('Consolas', 12), bg = "white", fg = "red")
        error_message.pack ()

    #If all inputs are valid, then the keys are changed
    else:
        #Unbinds the previous controls and rebinds the new ones
        try: 
            root.unbind (left_key)
            root.unbind (right_key)
        except:
            root.unbind ("<Left>")
            root.unbind ("<Right>")
        root.bind (left_key, lambda event: player.left()) 
        root.bind (right_key, lambda event: player.right())  
        root.focus_set()
        global changed
        changed = True

        #Creates popup window confirming that controls were successfully changed
        confirm_win = tk.Toplevel (root, background="white")
        x = (confirm_win.winfo_screenwidth()/2) - 300       
        y = (root.winfo_screenheight()/2) - 25
        confirm_win.geometry ("500x50+%d+%d" % (x,y-25))
        confirm_message = Label(confirm_win, text="Controls successfully changed :)", font=('Consolas', 12), bg = "white", fg = "black")
        confirm_message.pack ()


##Displays the control screen that lets player change their controls
def controls (frame):
    #Remaking the frame to clear the  widgets on the menu
    frame.destroy()
    canvas = Canvas (root, background="black")
    canvas.pack(expand=1, fill="both")

    #Creating all the text and entry boxes for player to enter new controls in
    title = Label(canvas, text="Controls", font=('Consolas', 45), bg="black", fg="white")
    title.pack(padx=20, pady=10, side="top")

    leftText = Label(canvas, text="Left", font=('Consolas', 30), bg="black", fg="white")
    rightText = Label(canvas, text="Right", font=('Consolas', 30), bg="black", fg="white")
  
    leftEntry = tk.Entry(canvas, font=('Consolas', 15), width = 10) 
    rightEntry = tk.Entry(canvas, font=('Consolas', 15), width = 10) 
    canvas.create_window(400, 223, window=leftEntry)
    canvas.create_window(400, 318, window=rightEntry)

    #Will call change button function when button is pressed and takes entry box inputs 
    changeKeyButton = tk.Button(canvas, text="Change keys", command= lambda: change_buttons(leftEntry, rightEntry))

    #Packing all widgets
    leftText.pack (padx=200, pady=(100,20), anchor="nw")
    rightText.pack (padx=200, pady=20, anchor="nw")
    changeKeyButton.pack (padx=480,pady=10,anchor="nw")

    #Adding a button that returns to the menu screen when clicked
    return_to_menu = tk.Button(canvas, text="Return back to menu", command= lambda: menu(canvas))
    return_to_menu.pack(padx=50, pady=50, side="bottom", anchor="se")


##Displays a leaderboard screen
def leaderboard(frame):
    frame.destroy()
    canvas = Canvas (root, background="black")  #Creating new blank canvas
    canvas.pack(expand=1, fill="both")

    #Displays leaderboard title and button to return to menu
    leaderboardText = Label(canvas, text="Leaderboard:", font=('Consolas', 40), bg="black", fg="white")
    leaderboardText.pack(pady=20, side="top",anchor="center")
    return_to_menu = tk.Button(canvas, text="Return back to menu", command= lambda: menu(canvas))
    return_to_menu.pack(padx=50, pady=50, side="bottom", anchor="se")

    #Reads all the scores in the leaderboard
    file = open ("leaderboard.txt")
    for x in file:                      #Fetches all text in leaderboard.txt and stores in variable all_scores
        all_scores = x
    try:
        scores_list = all_scores.split()    #Splits text according to spaces and is stored in array form

        ordered = []        #Array that holds all the ordered score numbers
        numbers = []        #Array that holds all the score numbers

        #Storing all the scores in an array called numbers (left out the names for now)
        y = 1
        while y < len(scores_list):
            numbers.append (int(scores_list[y]))
            y += 2

        #Ordering the scores and storing in array 'ordered'
        for z in range (len (numbers)):
            next_highest = max(numbers)
            ordered.append (next_highest)
            numbers.remove (next_highest)

        #Displaying the top 10 player scores
        count = 0
        while count < 10 and count <= len(ordered):     #Loops so that it only displays max 10 scores or all of the scores if there are less than 10 
            score = str(ordered[count])
            score_index = scores_list.index(score)
            name = scores_list[score_index - 1]         #Finds the name associated with the ordered score
            place = str(count + 1) + ") "
            scoreLabel = Label(canvas, text=place + name + "   " + score, font=("Consolas", 15), bg="black", fg="white")     #Displays the name and score on screen with a position number
            scoreLabel.pack (pady = 10, side="top", anchor="center")

            scores_list.remove (name)       #Once displayed, name and score is removed from scores_list so that there aren't duplicates on leaderboard if people have same scores
            scores_list.remove (score)
            count += 1
    except: 
        pass
    file.close()


#Creating tkinter window
root = tk.Tk()     
root.title("Dodging game")

#Centering the window on the screen
rootWidth = 1536
rootHeight = 864
x = (root.winfo_screenwidth()/2) - (rootWidth/2)        #Calculating x and y coordinates to place window at
y = (root.winfo_screenheight()/2) - (rootHeight/2)
root.geometry("1536x864+%d+%d" % (x,y-25))
root.resizable(False,False)                         #Prevents window from being resizable

canvas = Canvas(root, bg="black")    #Making a temporary canvas so that the return to menu button works in the controls page   

global resume       #Sets resume to false so program knows pressing start game isn't continuing from a previous save
resume = False

menu (canvas)   #Calls the menu screen

root.mainloop()
