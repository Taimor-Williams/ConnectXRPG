from backEndBoard_Module import *
import csv  
import random
import os

# create data

board = BackEndBoard(4)
class AI():
    def makeMove(self, color: InterFaceChip, moveList: list[tuple[str, int]]):
        return random.randint(0,8)



player1 = AI()
player2 = AI()

x = []
y = []
games = 0
while games<10:
    blacMove = player1.makeMove(BlackChip(), board.moveList)
    board.placeChip(blacMove, BlackChip())
    if board.victoryCheck(BlackChip()) == True:
        y.append('Win')
        x.append(board.showBoardList())
        board =  BackEndBoard(4)
        games+=1
    redMove = player1.makeMove(RedChip(), board.moveList)
    board.placeChip(redMove, RedChip())
    if board.victoryCheck(RedChip()) == True:
        y.append('Loss')
        x.append(board.showBoardList())
        board =  BackEndBoard(4)
        games+=1
    if len(board.moveList) == 81:
        y.append('Draw')
        x.append(board.showBoardList())
        board =  BackEndBoard(4)
        games+=1

    
# dump data
fields = ['BoardState', 'Outcome'] 
directory = 'MLsavedGames/'
# items in directory
# folder path
count = 0
# Iterate directory
for path in os.listdir(directory):
    # check if current path is a file
    if os.path.isfile(os.path.join(directory, path)):
        count += 1
itemsInDirectory = count
filename = directory+'GamesFile'+ str(count)+'.csv'
rows = []
for i in range(len(x)):
    rows.append((x[i],y[i]))

with open(filename, 'w') as csvfile:  
# creating a csv writer object  
    csvwriter = csv.writer(csvfile)  
    # writing the fields  
    csvwriter.writerow(fields)  
    # writing the data rows  
    csvwriter.writerows(rows) 
    

        
    


# unsupervised learning module 
