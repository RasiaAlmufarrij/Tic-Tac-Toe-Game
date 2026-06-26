from tkinter import *
from tkinter import messagebox
def start():
    global t, game_started, s1, s2
    if secPlayer.get() == 0 or symbol.get() == 0 or turn.get() == 0:
        messagebox.showwarning("Incomplete Selection", "Please make ALL selections before starting!")
        return
    game_started = True
    if symbol.get() == 1:
        s1 = "X"
        s2 = "O"
    else:
        s1 = "O"
        s2 = "X"
    t = 1 if turn.get() == 1 else 2
    bttn1.config(state=DISABLED)
    r1.config(state=DISABLED)
    r2.config(state=DISABLED)
    r3.config(state=DISABLED)
    r4.config(state=DISABLED)
    r5.config(state=DISABLED)
    r6.config(state=DISABLED)
    if secPlayer.get() == 1 and turn.get() == 2:
        computer()
        return
def choice(event):
    global t
    clicked = event.widget
    if secPlayer.get() == 0 or symbol.get() == 0 or turn.get() == 0:
        messagebox.showwarning("Incomplete Selection", "Please make ALL selections before starting!")
        resetButtons()
        return
    if not game_started:
        messagebox.showwarning("Game not started", "Please press Start first!")
        resetButtons()
        return
    if not isAvailable(clicked.id):
        return
    button_num = clicked.id
    if secPlayer.get() == 2 and t == 2:
        doMove(s2, button_num)
        if result("Player 2"):
            return
        t = 3 - t
        return
    doMove(s1, button_num)
    if result("Player 1"):
         return
    t=2
    if secPlayer.get()==1:
          computer()
          if result("The Computer"):
             return


def computer():
    boardcopy = board.copy()
    for i in boardcopy:
        if isAvailable(i):
            boardcopy[i] = s2
            if checkWin(boardcopy):
                doMove(s2, i)
                return
            else:
                boardcopy[i] = " "

    for i in boardcopy:
        if isAvailable(i):
            boardcopy[i] = s1
            if checkWin(boardcopy):
                doMove(s2, i)
                return
            else:
                boardcopy[i] = " "

    if board[5] == " ":
        doMove(s2, 5)
        return

    for i in boardcopy:
        if i in (1, 3, 7, 9) and boardcopy[i] == " ":
            doMove(s2, i)
            return

    for i in boardcopy:
        if i in (2, 4, 6, 8) and boardcopy[i] == " ":
            doMove(s2, i)
            return

def doMove(s, num):
    all_buttons[num].config(text=s, font=("Arial", 9, "bold"), borderwidth=3, relief=SUNKEN, state=DISABLED)
    board[num] = s

def isAvailable(pos):
    return board[pos] == " "

def checkDraw(bo):
    for position in bo.values():
        if position == " ":
            return False
    return True

def checkWin(bo):
    global winorder
    place = [[1,2,3], [4,5,6], [7,8,9], [1,4,7], [2,5,8], [3,6,9], [1,5,9], [3,5,7]]
    for n in place:
        x1, x2, x3 = n
        if bo[x1] == bo[x2] == bo[x3] != " ":
            winorder = n
            return True
    return False

def displayresult():
    for pos in winorder:
        all_buttons[pos].config(bg="lightgreen")
      
def result(winner):
    global board, game_started
    if checkWin(board):
        displayresult()
        messagebox.showinfo("Result", f"{winner} has won the game!")

    elif checkDraw(board):
        messagebox.showinfo("Result", "It's a Draw!")

    if checkDraw(board) or checkWin(board):
        if messagebox.askyesno("Question", "Would you like to start another game?"):
            resetGame()
            return True
        else:
            messagebox.showinfo("Game over", "Game has Ended!")
            root.quit()
            return True
    return False

def resetGame():
    global board, game_started
    board = {
        1: " ", 2: " ", 3: " ",
        4: " ", 5: " ", 6: " ",
        7: " ", 8: " ", 9: " "
    }
    resetButtons()
    secPlayer.set(0)
    symbol.set(0)
    turn.set(0)
    bttn1.config(state=NORMAL)
    game_started = False

def resetButtons():
    for i in all_buttons:
        all_buttons[i].config(state=DISABLED,text=" ",borderwidth=3,relief=RAISED, bg="lightblue")
    r1.config(state=NORMAL)
    r2.config(state=NORMAL)
    r3.config(state=NORMAL)
    r4.config(state=NORMAL)
    r5.config(state=NORMAL)
    r6.config(state=NORMAL)


root = Tk()
board = {
    1: " ", 2: " ", 3: " ",
    4: " ", 5: " ", 6: " ",
    7: " ", 8: " ", 9: " "
}
secPlayer = IntVar()
symbol = IntVar()
turn = IntVar()
game_started = False
winorder = []
s1 = ""
s2 = ""

root.title("Tic Tac Toe")
root.geometry("400x400")

l1 = Label(root, text="Play with?")
l1.grid(column=0, row=0)

r1 = Radiobutton(root, text="Computer", variable=secPlayer, value=1)
r1.grid(column=1, row=0)

r2 = Radiobutton(root, text="Player2", variable=secPlayer, value=2)
r2.grid(column=2, row=0)

l2 = Label(root, text="Select?")
l2.grid(column=0, row=1)

r3 = Radiobutton(root, text="X", variable=symbol, value=1)
r3.grid(column=1, row=1)

r4 = Radiobutton(root, text="O", variable=symbol, value=2)
r4.grid(column=2, row=1)

l3 = Label(root, text="Start the game?")
l3.grid(column=0, row=2)

r5 = Radiobutton(root, text="Yes", variable=turn, value=1)
r5.grid(column=1, row=2)

r6 = Radiobutton(root, text="No", variable=turn, value=2)
r6.grid(column=2, row=2)

bttn1 = Button(root, text="Start", width=6, height=2, command=start)
bttn1.grid(column=3, row=3, pady=20)

all_buttons = {}
c = 1
r = 4
for i in range(1, 10):
    btn = Button(root,state=DISABLED, text=" ", width=12, height=4, borderwidth=3, relief=RAISED, bg="lightblue")
    btn.id = i
    btn.bind("<Button-1>", choice)
    btn.grid(column=c, row=r)
    all_buttons[i] = btn
    c += 1
    if c > 3:
        c = 1
        r += 1

root.mainloop()