import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os


class LinearQNet(nn.Module):
    def __init__(self, inputSize, hiddenSize, outputSize) -> None:
        """
        """
        super().__init__()
        self.linear1 = nn.Linear(inputSize, hiddenSize)
        self.linear2 = nn.Linear(hiddenSize, outputSize)

    def forward(self, x):
        """
        this is the prediciton that is called when 
        """
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x

    def save(self, fileName = 'model.pth'):
        """
        """ 
        modelFolderPath = './model'
        if not os.path.exists(modelFolderPath):
            os.makedirs(modelFolderPath)
        fileName = os.path.join(modelFolderPath, fileName)
        torch.save(self.state_dict(), fileName)

class QTrainer():
    def __init__(self, model, lr, gamma) -> None:
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr =self.lr)
        self.criterion = nn.MSELoss()
        
    def trainStep(self, state, action, reward, nextState, done):
        """
        
        """
        state = torch.tensor(state, dtype=torch.float)
        nextState = torch.tensor(nextState, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype= torch.float)
        # (n,x)
        if len(state.shape) == 1:
            # (1,x)
            state = torch.unsqueeze(state,0)
            nextState = torch.unsqueeze(nextState, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

            #1: predicted Q values with current state
            pred = self.model(state)
            target = pred.clone()
            for idx in range(len(done)):
                Qnew = reward[idx]
                if not done[idx]:
                    Qnew = reward[idx] +self.gamma*torch.max(self.model(nextState[idx]))
                target[idx][torch.argmax(action).item()]= Qnew

            #2: Qnew = r + y * max(nextPredicted Q value)
            # pred.clone()
            # preds[argmax(action)] = QNew
            self.optimizer.zero_grad()
            loss = self.criterion(target, pred)
            loss.backward()
            self.optimizer.step()