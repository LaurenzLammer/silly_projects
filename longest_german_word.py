# find the German word that requires the longest monodigital travel distance on a German keyboard (ignoring capitalisation)
# import requirements
import math
import codecs
import re
# set up the row of letters on the German keyboard
row1 = ["q","w","e","r","t","z","u","i","o","p","ü","ß"]
row2 = ["a","s","d","f","g","h","j","k","l","ö","ä", "'"]
row3 = ["y","x","c","v","b","n","m", ",", ".", "-"]
unit = 19.05
# calculate the distance between two consecutive letters
def letter_distance(letter1, letter2):
    # measure vertical distance of letters
    if (letter1 in row1 and letter2 in row1) or (letter1 in row2 and letter2 in row2) or (letter1 in row3 and letter2 in row3):
        vertical = 0
    elif (letter1 in row1 and letter2 in row2) or (letter1 in row2 and letter2 in row1) or (letter1 in row2 and letter2 in row3) or (letter1 in row3 and letter2 in row2):
        vertical = 1
    elif (letter1 in row1 and letter2 in row3) or (letter1 in row3 and letter2 in row1):
        vertical = 2
    for row in (row1, row2, row3):
        if letter1 in row:
            pos1 = row.index(letter1)
        if letter2 in row:
            pos2 = row.index(letter2)
    # measure horizontal distance of letters
    horizontal = (pos2 - pos1)
    if letter1 in row1 and letter2 in row2:
        horizontal += 1/4
    elif letter1 in row1 and letter2 in row3:
        horizontal += 3 / 4
    elif letter1 in row2 and letter2 in row3:
        horizontal += 1/2
    elif letter1 in row2 and letter2 in row3:
        horizontal += 3 / 4
    elif letter1 in row2 and letter2 in row1:
        horizontal -= 1/4
    elif letter1 in row3 and letter2 in row1:
        horizontal -= 3/4
    elif letter1 in row3 and letter2 in row2:
        horizontal -= 1/2
    # handle the special case of ß, which actually is in none of the three rows
    if letter1 == "ß" or letter2 == "ß":
        vertical += 1
        if letter1 == "ß":
            horizontal += (1 + 1/8)
        if letter2 == "ß":
            horizontal -= (1 + 1/8)
    return math.sqrt((vertical**2 + horizontal**2))

# calculate the cumulative distance of an entire word
def letters_distance(word):
    distance = 0
    # handle one-letter words
    if len(word) == 1:
        return distance
    else:
        for n in range(len(word)-1):
            distance += letter_distance(word[n], word[n+1])
        return distance

# open the collection of German words as provided by dict.cc (https://www1.dict.cc/translation_file_request.php)
with codecs.open('wortschatz.txt', 'r', encoding= 'utf-8', errors='ignore') as f:
    lines = f.readlines()
# remove unnecessary information and store all words in lowercase in the list words
starters = []
for line in lines:
    if line[0] not in starters:
        starters.append(line[0])
alphastarters = []
for n in range(len(starters)):
    if starters[n].isalpha():
        alphastarters.append(starters[n])
alphastarters = alphastarters[0:52]
truelines = []
for line in lines:
    if line[0] in alphastarters:
        truelines.append(line)
words = []
for line in truelines:
    words.append(re.split("[^a-zA-Z|'|-]", line)[0].lower())

# find the word with the longest monodigital distance
longest_dist = 0
longest_word = ""

for word in words:
    distance = letters_distance(word)
    if distance > longest_dist:
        longest_dist = distance
        longest_word = word

# find the word with the most letters
most_letters = 0
most_letter_word = ""
for word in words:
    if len(word) > most_letters:
        most_letter_word = word
        most_letters = len(word)
len(longest_word)
