import torch
import random
import numpy as np
from collections import deque
from backEndBoard_Module import *
from model_Module import LinearQNet, QTrainer
from helper import plot
from solvedAI_Module import solvedAI

maxMemory = 100_000
batchSize = 1000
LR = 0.001

class Agent():
    """
    
    """
    def __init__(self) -> None:
        self.number_games =0
        self.epsilon = 1 # randomness 
        self.gamma = 0.95 #discount rate <1
        self.memory = deque(maxlen=maxMemory)
        inputSize = 7*7 #size of the state
        hiddenSize = 600 # can be anything
        outputsize = 7 # size of the actions you can make
        self.model = LinearQNet(inputSize, hiddenSize, outputsize)
        self.trainer = QTrainer(self.model, lr =LR, gamma= self.gamma)
        #TODO: model, trianer


    def getState(self, game: BackEndBoard)->np.ndarray[int]:
        """
        
        """
        listState: list[list[int]] = game.showBoardList()
        arrayState: np.ndarray = np.array(listState)
        stateVector = arrayState.flatten()
        return stateVector

    def remember(self, state, action, reward, nextState, done):
        """
        """
        self.memory.append((state,action,reward,nextState,done)) # popleft if  max memory reached


    
    def trainLongMemory(self):
        """
        """
        if len(self.memory) > batchSize:
            miniSample: list[tuple] = random.sample(self.memory, batchSize) 
        else:
            miniSample = self.memory
        states, actions,rewards,nextStates, dones = zip(*miniSample)
        self.trainer.trainStep(states, actions, rewards, nextStates, dones)
        for state, action, reward, nextState, done in miniSample:
            self.trainer.trainStep(state, action, reward, nextState, done)



    
    def trainShortMemory(self, state, action, reward, nextState, done):
        """
        """
        self.trainer.trainStep(state, action, reward, nextState, done)

    
    def getAction(self, state):
        """
        @effects, do random moves sometimes other times calc your turn
        """
        self.epsilon = 80-self.number_games
        finalMove = [0,0,0,0,0,0,0] # we have 7 potential moves or columns we can make
        if random.randint(0,200)< self.epsilon:
            move = random.randint(0,2)
            finalMove[move] = 1 # make that move
        else:
            state0 = torch.tensor(state, dtype = torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            print(move)
            finalMove[move] = 1
        
        count = 0
        for loc in finalMove:
            if loc == 0:
                count+=1
            else:
                return count
    
    
    
def train():
    """
    """

    plotScores = []
    plotMeanScores = []
    totalScore = 0
    record = 0
    agent = Agent()
    opp = solvedAI()
    game = BackEndBoard(4)
    # wins by both colors
    redCount =0
    blackCount =0 
    while redCount+blackCount <100:
        # code i added
        npBoard = np.array(game.showBoardList())
        move,score = opp.minMaxAlgorithimNumpy(npBoard,1,True)
        game.placeChip(move, BlackChip())
        # code i added
        # get old state
        stateOld = agent.getState(game)
        # get move
        finalMove = agent.getAction(stateOld)

        # perform move and get new state
        reward, done, score = game.MLplaceChip(finalMove, RedChip())

        stateNew = agent.getState(game)

        #train memory
        agent.trainShortMemory(stateOld, finalMove, reward, stateNew, done)
        
        #remember
        agent.remember(stateOld, finalMove, reward, stateNew, done)
        if done:
            #train long memeory 
            if game.victoryCheck(RedChip()):
                print(np.array(game.showBoardList()))
                redCount +=1
            else:
                blackCount+=1
            game.restart()
            agent.number_games +=1
            agent.trainLongMemory()

            if score > record:
                record = score 
            print("Game", agent.number_games, 'Score', score, 'Record', record )
            print(blackCount, redCount)
            # TODO: plot 
            plotScores.append(score)
            print('Score:{score}')
            totalScore +=score
            meanScore =totalScore/agent.number_games
            plotMeanScores.append(meanScore)
            plot(plotScores, plotMeanScores)



def mainLoop():
    totalGames = 0
    plotScores = []
    plotMeanScores = []
    totalScore = 0
    record = 0
    agent = Agent()
    opp = solvedAI()
    game = BackEndBoard(4)
    # wins by both colors
    redCount =0
    blackCount =0 
    while totalGames < 100:
        state = agent.getState(game)
        totalReward = 0
        while not (game.victoryCheck(RedChip()) or game.victoryCheck(BlackChip())):
            # opps move
            npBoard = np.array(game.showBoardList())
            move = opp.minMaxAlgorithimNumpy(npBoard,1,True)[0]
            print('AImove', move)
            game.placeChip(move, BlackChip())
            state = agent.getState(game)
            oldScore = game.mlScore(RedChip())

            if not (game.victoryCheck(RedChip()) or game.victoryCheck(BlackChip())):

                # agents move
                finalMove = agent.getAction(state)
                game.placeChip(finalMove, RedChip())
                print('MLmove', finalMove)

           
            score = game.mlScore(RedChip())
            stateNew = agent.getState(game)
            # reward = 1 if game.victoryCheck(RedChip()) else 0
            reward = score - oldScore
            if game.victoryCheck(BlackChip()):
                reward = oldScore
            print('reward', reward)
            print(np.array(game.showBoardList()))
            done = (game.victoryCheck(RedChip()) or game.victoryCheck(BlackChip()))

            #train memory
            agent.trainShortMemory(state, finalMove, reward, stateNew, done)
        
            #remember
            agent.remember(state, finalMove, reward, stateNew, done)
            state = stateNew
            totalReward +=reward

        # when game is over
        print('Game!')
        totalGames +=1
        score = game.mlScore(RedChip())
        game.restart()
        agent.number_games +=1
        agent.trainLongMemory()

        if score > record:
            record = score 
        print("Game", agent.number_games, 'Score', score, 'Record', record )
        print(blackCount, redCount)
        # TODO: plot 
        plotScores.append(score)
        print('Score:{score}')
        totalScore +=score
        meanScore =totalScore/agent.number_games
        plotMeanScores.append(meanScore)
        plot(plotScores, plotMeanScores)

if __name__ == '__main__':
    mainLoop()

