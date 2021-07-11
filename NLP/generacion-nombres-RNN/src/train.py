import random
from model import *
from data import *
import torch.nn as nn
import torch.optim as optim

EOS = n_letters - 2

# Random item from a list
def randomChoice(l):
    return l[random.randint(0, len(l) - 1)]

# Get a random category and random line from that category
def randomTrainingPair():
    category = randomChoice(all_categories)
    line = randomChoice(category_lines[category])
    return category, line


# LongTensor of second letter to end (EOS) for target
def targetTensor(line):
    letter_indexes = [all_letters.index(line[li]) for li in range(0, len(line))]
    letter_indexes.append(EOS)
    return torch.LongTensor(letter_indexes)


def randomTrainingExample():
    category, line = randomTrainingPair()
    category_tensor = Variable(categoryTensor(category))
    input_line_tensor = Variable(inputTensor(line))
    target_line_tensor = Variable(targetTensor(line))
    return category_tensor, input_line_tensor, target_line_tensor

rnn = RNN(n_letters, 128, n_letters)
criterion = nn.NLLLoss()
learning_rate = 0.0003
optimizer = optim.Adam(rnn.parameters(), learning_rate)

def train(category_tensor, input_line_tensor, target_line_tensor):

    optimizer.zero_grad()
    loss = 0
    hidden = rnn.initHidden()
    for i in range(input_line_tensor.size(0)):
        output, hidden = rnn(category_tensor, input_line_tensor[i], hidden)
        loss += criterion(output, target_line_tensor[i])
    loss.backward()
    optimizer.step()

    return output, loss.data[0] / input_line_tensor.size(0)



import time
import math

def timeSince(since):
    now = time.time()
    s = now - since
    m = math.floor(s / 60)
    s -= m * 60
    return '%dm %ds' % (m, s)




n_iters = 100000
print_every = 500
save_every = 50000
all_losses = []
total_loss = 0
saves = 0

start = time.time()

for iter in range(1, n_iters + 1):

    output, loss = train(*randomTrainingExample())
    total_loss += loss

    if iter % print_every == 0:
        print('%s (%d %d%%) %.4f' % (timeSince(start), iter, iter / n_iters * 100, total_loss))
        total_loss = 0

    if iter % save_every == 0:
        torch.save(rnn, 'char-rnn-generation{}.pt'.format(saves))
        saves+=1
