import string
import re
from pickle import dump
from unicodedata import normalize
from numpy import array

# Load text data


def load_document(filename):
    # Opens file in read-only mode to read line by line and return
    with open(filename, mode='rt', encoding='utf-8') as file:
        text = file.read()
    return text

def create_pairs(text):
    lines = text.strip().split('\n')
    cleaned_lines = [line[:line.find("CC-BY")] if line.find("CC-BY") >= 0 else line for line in lines]
    pairs = [line.split('\t') for line in cleaned_lines]
    return pairs

def clean_pairs(pairs):
    cleaned = list()

    re_print = re.compile('[^%s]' % re.escape(string.printable))
    table = str.maketrans('', '', string.punctuation)
    for pair in pairs:
        clean_pair = list()
        for line in pair:
            line = normalize('NFD', line).encode('ascii', 'ignore')
            line = line.decode('UTF-8')
            line = line.split()
            line = [word.lower() for word in line]
            line = [word.translate(table) for word in line]
            line = [re_print.sub('', w) for w in line]
            line = [word for word in line if word.isalpha()]
            clean_pair.append(' '.join(line))
        cleaned.append(clean_pair)
    return array(cleaned)


def save_clean_data(sentences, filename):
    dump(sentences, open(filename, 'wb'))
    print('Saved: %s' % filename)


if __name__ == "__main__":
    lines = load_document("Data/fra.txt")
    print(len(lines))
    # print(lines)
    pairs = create_pairs(lines)
    print(len(pairs))
    # print(pairs)
    cleaned_pairs = clean_pairs(pairs)
    # save_clean_data(clean_pairs, 'english-french.pkl')
    print(len(cleaned_pairs))
    for i in range(10):
        print('[%s] => [%s]' % (cleaned_pairs[i, 0], cleaned_pairs[i, 1]))

