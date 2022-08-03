"""
    Question 2.1
"""

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

# Now print out the probabilities of each word-tag pair. Order by occurrences descending for more sense
for word, obj in sorted(probabilities.items(), key=lambda x: x[1]['occurrences'], reverse=True):
    occurrences = obj['occurrences']
    for tag in obj:
        if tag == 'occurrences':
            continue

        probability = obj[tag] / occurrences
        print(word, tag, probability)
