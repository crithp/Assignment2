"""
    Question 2.1
"""
import re
from sys import argv

if len(argv) < 1:
    raise Exception("Please give file as input")

input_file = argv[1]

# Read the training file in
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

# Split up punctuation from words
fixed_input = ''
for word in text.split():
    word = word.strip()

    # Split up attached punctuation, got to do it both ways because of that ``a
    word = re.sub(r"([\w-]*)([^\w-]*)", r"\1 \2", word).strip()
    word = re.sub(r"([^\w-]*)([\w-]*)", r"\1 \2", word).strip()

    fixed_input += word + ' '

with open('output_tagged.txt', 'w+') as outfile:
    for word in fixed_input.split():
        tag = 'NN'  # Default tag

        if word in most_probable:
            tag = most_probable[word][0].upper()

        outfile.write(word + "/" + tag + ' ')

# Time to compare the output to the golden standard file
# Read the golden standard file in
with open('pos_golden_standard.txt', 'r') as infile:
    golden_text = infile.read()

# Just make sure the golden text matches our format, noticed it's lowercase too
fixed_golden = ''
for pair in golden_text.split():
    pair = pair.strip()
    if pair == '' or len(pair.split('/')) < 2:
        continue
    word, tag = pair.split('/')

    fixed_golden += word + "/" + tag.upper() + ' '

# Read in our output
with open('output_tagged.txt', 'r') as infile:
    our_text = infile.read()

# Stat variables for tracking error counts
error_count = 0
wrong_tags = {}  # Correct_tag: (wrong_tag, count)
all_tags = []

# Now compare
ours_split = our_text.split()
gold_split = fixed_golden.split()
total_words = len(gold_split)
for index in range(0, total_words):

    word1, tag1 = ours_split[index].split('/')
    word2, tag2 = gold_split[index].split('/')

    # Just make very sure we are parsing the right word
    if word1 != word2:
        raise Exception(f"Got lost somewhere: w1={word1}, w2={word2}")

    # Add to all tags if we haven't seen it yet
    if tag1 not in all_tags:
        all_tags.append(tag1)
    if tag2 not in all_tags:
        all_tags.append(tag2)

    if tag1 != tag2:
        error_count += 1
        if tag2 not in wrong_tags:
            wrong_tags[tag2] = {}
        if tag1 not in wrong_tags[tag2]:
            wrong_tags[tag2][tag1] = 0

        wrong_tags[tag2][tag1] += 1

print("\nConfusion matrix -----------------\n")

# Create the confusion matrix
print(f"{'':>6}", *[f"{x:>6}" for x in all_tags])
for right_tag in all_tags:
    print(f"{right_tag:>6}", end='')
    for wrong_tag in all_tags:
        if right_tag == wrong_tag:
            print(f"{'-':>6}", end='')
        elif right_tag not in wrong_tags:
            print(f"{'':>6}", end='')
        elif wrong_tag in wrong_tags[right_tag]:
            print(f"{round(wrong_tags[right_tag][wrong_tag]/error_count, 2):>6}", end='')
        else:
            print(f"{'':>6}", end='')
    print()
