from tkinter import messagebox
from tkinter import *
from random import randint

def addLength():
    global game, snake, direction
    x0, y0, x1, y1 = game.coords(snake[-1])
    snake.append(game.create_rectangle(x0+(-22*direction[0]), y0+(-22*direction[1]), x1+(-22*direction[0]), y1+(-22*direction[1]), fill="darkgreen"))
    # print(game.coords(snake[-1]))

def checkCollision(obj):
    global game
    x0, y0, x1, y1 = game.coords(obj)
    result = game.find_overlapping(x0, y0, x1, y1)
    if (len(result) > 1):
        return True
    return False

def newApple():
    global apple
    x = randint(10,591)
    y = randint(10,591)
    while ((x//10)%2 == 0 or (x//10)%2 == 0):
        x = randint(10,591)
        y = randint(10,591)
    apple = game.create_oval(x-9, y-9, x+9, y+9, fill="red")
    # apple = game.create_oval(340, 600, 360, 620, fill="red")

def keyPress(event):
    global direction, gameStarted
    if (gameStarted == False and event.keysym == 'space'):  gameStarted = True; startGame()
    elif (event.keysym == 'Up' and direction != [0,1]):     direction = [0,-1]
    elif (event.keysym == 'Down' and direction != [0,-1]):  direction = [0,1]
    elif (event.keysym == 'Left' and direction != [1,0]):   direction = [-1,0]
    elif (event.keysym == 'Right' and direction != [-1,0]): direction = [1,0]

def updateGame():
    global game, snake, apple, direction
    
    for i in range(len(snake)-1, 0, -1):
        # print(i, game.coords(snake[i]))
        px0, py0, px1, py1 = game.coords(snake[i-1])
        game.coords(snake[i], px0, py0, px1, py1)
    
    x0, y0, x1, y1 = game.coords(snake[0])
    if (x0 < 2):        game.coords(snake[0], 578, y0, 598, y1)
    elif (y0 < 2):      game.coords(snake[0], x0, 578, x1, 598)
    elif (x0 > 578):    game.coords(snake[0], 2, y0, 22, y1)
    elif (y0 > 578):    game.coords(snake[0], x0, 2, x1, 22)
    else:               game.move(snake[0], 22*direction[0], 22*direction[1])
    
    if (apple != None and checkCollision(apple)):
        global score
        # print("Ate apple")
        game.delete(apple)
        apple = None
        score += 1
        scoreLabel["text"] = "Score: {}".format(score)
        newApple()
        addLength()
    if (checkCollision(snake[0])):
        return
    
    game.after(80, updateGame)

# def gameOver():
#     global score
#     reply = messagebox.askquestion("You Lost :(", "Your score was {}! Would you like to try again?".format(score), icon="error")
#     if reply == "yes":  startGame()
#     else:               exit()

def startGame():
    global game, snake, direction, apple, score, startSpace
    # game.delete('all')
    snake = [game.create_rectangle((600//2)-10, (600//2)-10, (600//2)+10, (600//2)+10, fill="green")]
    # Up -> [0,-1]
    # Down -> [0,1]
    # Left -> [-1,0]
    # Right -> [1,0]
    direction = [0,-1]
    for x in range(2):
        addLength()
    apple = None
    score = 0
    startSpace.destroy()
    newApple()
    updateGame()

window = Tk()
window.title("Snake")
# window.geometry("600x600")
window.resizable(0,0)
window.configure(bg="black")
window.bind_all('<Key>', keyPress)

# Variables
snake = []
direction = []
apple = None
score = 0
gameStarted = False

# Score
scoreLabel = Label(window, text="Score: 0", bg="black", fg="white", font=(150), highlightthickness=0)
# score.grid(row=0, sticky="wens")
scoreLabel.pack()
# Game canvas
game = Canvas(window, width=600, height=600, bg="black", highlightthickness=0)
# game.grid(row=1, sticky="wens")
game.pack()
# Press Space to start game
startSpace = Label(window, text="Press <Space> to start.", bg="black", fg="white", font=(150), highlightthickness=0)
# startSpace.grid(row=2, sticky="wens")
startSpace.pack()

window.mainloop()