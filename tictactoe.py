#! /usr/bin/env python

#tictactoe
# Tic Tac Toe game that will eventually have a computer player
#	Control is done with the mouse
#
# v1.0 - Game Works, Two humans only 
#


from Tkinter import *
from random import *
import sys

SECTIONSIZE = 100

WINNUM = int(sys.argv[2])


PLAYSIZE = int(sys.argv[1])


BOARDSIZE = SECTIONSIZE * PLAYSIZE

root = Tk()

Previous = 0

Table = []
for i in range(PLAYSIZE):
 	Row = []
	for j in range(PLAYSIZE):
		Row.append(0)	
	Table.append(Row)

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

def CheckWin(X,Y):
	global Table
	Type = Table[X][Y]  


	#Check Horizontal
	Top = (X,Y)
	Bottom = (X,Y)
	count = 1
	i = X
	j = Y
	i = i+1
	while(0 <= i <= (PLAYSIZE-1) and 0 <= j <= (PLAYSIZE-1) and Table[i][j] == Type):
		count = count + 1
		Top = (i,j)
		i= i+1


	i = X
	j = Y
	i = i -1
	while(0 <= i <= (PLAYSIZE-1) and 0 <= j <= (PLAYSIZE-1) and Table[i][j] == Type):
		count = count + 1
		Bottom = (i,j)
		i= i-1

	if (count >= WINNUM):
		return (Top,Bottom)

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

def play(event):

	global Previous
	global Table
	canvas = event.widget
	X = event.x
	Y = event.y
	Section = FindSection(X,Y)
	LineX = SECTIONSIZE * Section[0]
	LineY = SECTIONSIZE * Section[1]


	if Table[Section[0]][Section[1]] == 0:
		if (Previous == 0):
			canvas.create_line(LineX+SECTIONSIZE,LineY,LineX,LineY+SECTIONSIZE,width = 3)
			canvas.create_line(LineX,LineY,LineX+SECTIONSIZE,LineY+SECTIONSIZE,width = 3)
			Table[Section[0]][Section[1]] = 1
			Previous = 1
	 	else:
			canvas.create_oval(LineX+SECTIONSIZE,LineY,LineX,LineY+SECTIONSIZE,width = 3)
			Table[Section[0]][Section[1]] = 2
			Previous = 0

		Win = CheckWin(Section[0],Section[1])
		if Win != 0:
			canvas.create_line(Win[0][0]*SECTIONSIZE+SECTIONSIZE/2,Win[0][1]*SECTIONSIZE+SECTIONSIZE/2,Win[1][0]*SECTIONSIZE+SECTIONSIZE/2,Win[1][1]*SECTIONSIZE+SECTIONSIZE/2,width = 10, fill = "red")
			for i in range(PLAYSIZE):
				for j in range(PLAYSIZE):
					Table[i][j] = 1

page = Canvas(root, width = BOARDSIZE, height = BOARDSIZE)
page.grid()

for i in range(1,PLAYSIZE):
	page.create_line(SECTIONSIZE*i, 0,SECTIONSIZE*i, BOARDSIZE, width = 5)
	page.create_line(0, SECTIONSIZE*i,BOARDSIZE, SECTIONSIZE*i, width = 5)

page.bind("<Button-1>", play)

root.mainloop()
  
