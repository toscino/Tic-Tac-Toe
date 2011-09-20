#! /usr/bin/env python

#tictactoe
# Tic Tac Toe game that will eventually have a computer player
#	Control is done with the mouse
#
# v1.0 - Game Works, Two humans only 
# v2.0 - Added Computer Player, but it just picks the first available space
#

from Tkinter import *
from random import *
import sys

######################################
#Constants

#The size of each section, ie where the X or O goes
SECTIONSIZE = 75

#The number in a row it takes to win
WINNUM = int(sys.argv[2])

#The sqrt of the number of playing spaces, or the length of one side
PLAYSIZE = int(sys.argv[1])

#The dimensions of the board in pixels
BOARDSIZE = SECTIONSIZE * PLAYSIZE

#PLACEHOLDERS to use in the games storage tables
EMPTY = 0  
CIRCLE = 1
CROSS = 2
GAMEOVER = 3

root = Tk()

#Set the initial player, CIRLCE was Previous so CROSS is up
Previous = CIRCLE

#initialize the storage table, 2D array initialization is one of the few things that is a pain in python, using it is standard though
Table = []
for i in range(PLAYSIZE):
 	Row = []
	for j in range(PLAYSIZE):
		Row.append(0)	
	Table.append(Row)

################################
#      FindSection(X,Y)
# Converts Pixel coordinates into Section Coordinates
# Inputs (X,Y)
# X - X Coordinate in Pixels
# Y - Y Coordinate in Pixels
#
# Outputs
# (X,Y)
# X - X Coordinate in Sections
# Y - Y Coordinate in Sections

def FindSection(X,Y):
	section = []
	for i in range(BOARDSIZE):
		if X < SECTIONSIZE * (i+1):
			section.append(i)
			break
	for i in range(BOARDSIZE):
		if Y < SECTIONSIZE * (i+1):
			section.append(i)
			break
	return section



################################
#      Checkwin(X,Y)
# Takes a section and determines if that section is involved in a Win Scenario (WINNUM in a row)
# Inputs (X,Y)
# X - X Coordinate in Sections
# Y - Y Coordinate in Sections
#
# Outputs
# ((X1,Y1),(X2,Y2))
# X1 - X Coordinate in Sections of one of the endpoints of a line
# Y1 - Y Coordinate in Sections of one of the endpoints of a line
# X2 - X Coordinate in Sections of one of the endpoints of a line
# Y2 - Y Coordinate in Sections of one of the endpoints of a line

def CheckWin(X,Y):
	global Table
	Type = Table[X][Y]  

	######################
	#Check Horizontal

	Top = (X,Y)	
	Bottom = (X,Y)
	count = 1
	i = X
	j = Y
	i = i+1

	while(0 <= i <= (PLAYSIZE-1) and 0 <= j <= (PLAYSIZE-1) and Table[i][j] == Type): #While the range is in bounds and the Type (X or O) is the same
		count = count + 1
		Top = (i,j)
		i= i+1


	i = X
	j = Y
	i = i -1
	while(0 <= i <= (PLAYSIZE-1) and 0 <= j <= (PLAYSIZE-1) and Table[i][j] == Type): #Same as above, but it is checking the opposite direction
		count = count + 1
		Bottom = (i,j)
		i= i-1

	if (count >= WINNUM):
		return (Top,Bottom)

	######################
	#Check Vertical

	Top = (X,Y)
	Bottom = (X,Y)
	count = 1
	i = X
	j = Y
	j = j+1
	while(0 <= i <= (PLAYSIZE-1) and 0 <= j <= (PLAYSIZE-1) and Table[i][j] == Type):
		count = count + 1
		Top = (i,j)
		j= j+1

	i = X
	j = Y
	j = j -1
	while(0 <= i <= (PLAYSIZE-1) and 0 <= j <= (PLAYSIZE-1) and Table[i][j] == Type):
		count = count + 1
		Bottom = (i,j)
		j= j-1

	if (count >= WINNUM):
		return (Top,Bottom)


	######################
	#Check /

	Top = (X,Y)
	Bottom = (X,Y)
	count = 1
	i = X
	j = Y
	i = i+1
	j = j-1
 
	while(0 <= i <= (PLAYSIZE-1) and 0 <= j <= (PLAYSIZE-1) and Table[i][j] == Type):
		count = count + 1
		Top = (i,j)
		i = i+1
		j = j-1
		

	i = X
	j = Y
	i = i - 1
	j = j + 1

	while(0 <= i <= (PLAYSIZE-1) and 0 <= j <= (PLAYSIZE-1) and Table[i][j] == Type):
		count = count + 1
		Bottom = (i,j)
		j = j + 1
		i = i - 1

	if (count >= WINNUM):
		return (Top,Bottom)

	#############################
	#Check \

	Top = (X,Y)
	Bottom = (X,Y)
	count = 1
	i = X
	j = Y
	i = i + 1
	j = j + 1
 
	while(0 <= i <= (PLAYSIZE-1) and 0 <= j <= (PLAYSIZE-1) and Table[i][j] == Type):
		count = count + 1
		Top = (i,j)
		i = i + 1
		j = j + 1
		

	i = X
	j = Y
	i = i - 1
	j = j - 1
	while(0 <= i <= (PLAYSIZE-1) and 0 <= j <= (PLAYSIZE-1) and Table[i][j] == Type):
		count = count + 1
		Bottom = (i,j)
		j = j - 1
		i = i - 1

	if (count >= WINNUM):
		return (Top,Bottom)

	return 0;

def redline(Canvas, Top, Bottom):
	Canvas.create_line(Top[0]*SECTIONSIZE+SECTIONSIZE/2,Top[1]*SECTIONSIZE+SECTIONSIZE/2,Bottom[0]*SECTIONSIZE+SECTIONSIZE/2,Bottom[1]*SECTIONSIZE+SECTIONSIZE/2,width = 10, fill = "red")
	for i in range(PLAYSIZE):
		for j in range(PLAYSIZE):
			Table[i][j] = GAMEOVER

def DrawCross(Canvas, X,Y):
	X1 = X*SECTIONSIZE
	Y1 = Y*SECTIONSIZE
	EXTRA = SECTIONSIZE

	Canvas.create_line(X1,Y1,X1 + EXTRA,Y1+EXTRA,width = 3)
	Canvas.create_line(X1+EXTRA,Y1,X1,Y1+EXTRA,width = 3)

def DrawCircle(Canvas, X,Y):
	X1 = X*SECTIONSIZE
	Y1 = Y*SECTIONSIZE
	EXTRA = SECTIONSIZE

	Canvas.create_oval(X1,Y1,X1+EXTRA,Y1+EXTRA,width = 3)


def AI(Canvas):
	global Table
	global Previous
	
	OpenSpaces = []
	SpaceCost = []
	for i in range(PLAYSIZE):
		for j in range(PLAYSIZE):
			if (Table[i][j] == EMPTY):
				OpenSpaces.append((i,j))
				
	DrawCircle(Canvas,OpenSpaces[0][0],OpenSpaces[0][1])
	Table[OpenSpaces[0][0]][OpenSpaces[0][1]] = CIRCLE
	Previous = CIRCLE
	return(OpenSpaces[0])


def play(event):

	global Previous
	global Table
	Canvas = event.widget
	X = event.x
	Y = event.y
	Section = FindSection(X,Y)
	LineX = SECTIONSIZE * Section[0]
	LineY = SECTIONSIZE * Section[1]


	if Table[Section[0]][Section[1]] == EMPTY:
		if (Previous == CIRCLE):
			DrawCross(Canvas,Section[0],Section[1])
			Table[Section[0]][Section[1]] = CROSS
			Previous = CROSS

			Win = CheckWin(Section[0],Section[1])
			if Win != 0: #Human Win
				redline(Canvas, Win[0], Win[1])
			else:			
				Section = AI(Canvas)
				Win = CheckWin(Section[0],Section[1])
				if Win != 0: #Human Win
					redline(Canvas, Win[0], Win[1])

page = Canvas(root, width = BOARDSIZE, height = BOARDSIZE)
page.grid()

for i in range(1,PLAYSIZE):
	page.create_line(SECTIONSIZE*i, 0,SECTIONSIZE*i, BOARDSIZE, width = 5)
	page.create_line(0, SECTIONSIZE*i,BOARDSIZE, SECTIONSIZE*i, width = 5)

page.bind("<Button-1>", play)

root.mainloop()
  
