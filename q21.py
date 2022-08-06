"""
    Question 2.1
"""
from sys import argv

if len(argv) < 1:
    raise Exception("Please give file as input")

input_file = argv[1]

# Read the file in
with open('pos_tagged.txt', 'r') as infile:
    text = infile.read()

# Instantiate a data structure in which to store probabilities
# This will be in the form: {word: {occurrences: X, tag1: count, tag2: count, ...}}
probabilities = {}

for pair in text.split():
    pair = pair.strip()
    if pair == '' or len(pair.split('/')) < 2:
        continue

    word, tag = pair.split('/')

    # Add the word to the data structure if not exists and then increment its value
    if word not in probabilities:
        probabilities[word] = {
            'occurrences': 0
        }
    probabilities[word]['occurrences'] += 1

    # Add the tag to the data structure if not exists and then increment its value
    if tag not in probabilities[word]:
        probabilities[word][tag] = 0
    probabilities[word][tag] += 1

print("word", "tag", "probability")

# Stores the most probable tag per word
most_probable = {}

# Now print out the probabilities of each word-tag pair. Order by occurrences descending for more sense
for word, obj in sorted(probabilities.items(), key=lambda x: x[1]['occurrences'], reverse=True):
    occurrences = obj['occurrences']
    for tag in obj:
        if tag == 'occurrences':
            continue

        probability = obj[tag] / occurrences
        print(word, tag, probability)

        # Store the highest probability for the word
        if word not in most_probable or probability > most_probable[word][1]:
            most_probable[word] = (tag, probability)

# Now mark every word in the input file
# Read the file in
with open(input_file, 'r') as infile:
    text = infile.read()

with open('output_tagged.txt', 'w+') as outfile:
    for word in text.split():
        word = word.strip()

        tag = 'NN'  # Default tag

        if word in most_probable:
            tag = most_probable[word][0]

        outfile.write(word + "/" + tag + ' ')
