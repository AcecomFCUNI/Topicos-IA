import torch
import torch.nn as nn
from torch.autograd import Variable
from data import *

DIM_EMBEDDING_CAR = 110
DIM_EMBEDDING_CAT = 18

class RNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(RNN, self).__init__()
        self.hidden_size = hidden_size

        self.embedding_car = nn.Embedding(input_size, DIM_EMBEDDING_CAR)
        self.embedding_cat = nn.Embedding(len(all_categories), DIM_EMBEDDING_CAT)
        self.lstm = nn.LSTM(DIM_EMBEDDING_CAT+DIM_EMBEDDING_CAR, hidden_size)
        self.toProbNextLetter = nn.Linear(hidden_size, output_size)
        #self.dropout = nn.Dropout(0.1)
        self.softmax = nn.LogSoftmax()

    def forward(self, category, input, hidden):

        car_embeds = self.embedding_car(input)
        cat_embeds = self.embedding_cat(category)
        # 28x28 -> 1 x 784
        cat_embeds = cat_embeds.view(1, -1).repeat(len(input), 1)

        combined_input = torch.cat((car_embeds, cat_embeds), 1)
        combined_input = combined_input.unsqueeze(1)

        lstm_out, hidden = self.lstm(combined_input, hidden)

        output = self.toProbNextLetter(lstm_out.view(-1, self.hidden_size))
        #output = self.dropout(output)
        output = self.softmax(output)

        return output, hidden

    def initHidden(self):
        return (Variable(torch.zeros(1, 1, self.hidden_size)), Variable(torch.zeros(1, 1, self.hidden_size)))
