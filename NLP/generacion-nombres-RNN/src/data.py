import torch
import glob
import unicodedata
import string

def letterToIndex(letter):
    return all_letters.index(letter)

all_letters = list(string.ascii_letters + " .,;'")

all_letters += ['<EOS>', '<SOS>']
n_letters = len(all_letters) #all_letters

def findFiles(path): return glob.glob(path)

# Turn a Unicode string to plain ASCII, thanks to http://stackoverflow.com/a/518232/2809427
def unicodeToAscii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
        and c in all_letters
    )

# Read a file and split into lines
def readLines(filename):
    lines = open(filename, encoding="utf8").read().strip().split("\n")
    return [unicodeToAscii(line) for line in lines]

# Build the category_lines dictionary, a list of lines per category
category_lines = {}
all_categories = []
for filename in findFiles('../data/names/*.txt'):
    category = filename.split('/')[-1].split('.')[0]
    all_categories.append(category)
    lines = readLines(filename)
    category_lines[category] = lines

n_categories = len(all_categories)

def nameToTensor(name):
    res = []
    for car in name:
        res.append(letterToIndex(car))
    return torch.LongTensor(res)

def categoryTensor(category):
    li = all_categories.index(category)
    return torch.LongTensor([li])

def inputTensor(line):
    res = []
    res.append(letterToIndex('<SOS>'))
    for li in range(len(line)):
        letter = line[li]
        res.append(letterToIndex(letter))
    tensor = torch.LongTensor(res)
    return tensor
