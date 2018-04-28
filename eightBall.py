#!/usr/bin/env python
import nltk
from nltk.parse.stanford import StanfordParser
import random
import os
script_path = os.path.abspath(__file__) # i.e. /path/to/dir/foobar.py
script_dir = os.path.split(script_path)[0] #i.e. /path/to/dir/
jar_loc = 'nlptools/stanford-parser/stanford-parser.jar'
models_loc= 'nlptools/stanford-parser/stanford-parser-3.5.2-models.jar'
path_to_jar = os.path.join(script_dir, jar_loc)
path_to_models_jar = os.path.join(script_dir, models_loc)
dependency_parser = StanfordParser(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)
ROOT = 'Root'
eightBallChoices = [
'it is certain',
'It is decidedly so',
'Without a doubt',
'Yes definitely',
'You may rely on it',
'As I see it, yes',
'Most likely',
'Outlook good',
'Yes',
'Signs point to yes',
'Reply hazy try again',
'Ask again later',
'Better not tell you now',
'Cannot predict now',
'Concentrate and ask again',
'Don\'t count on it',
'My reply is no',
'My sources say no',
'Outlook not so good',
'Very doubtful'
]

def random_response():
    return random.choice(eightBallChoices)

def main():
    #print random_response()
    print isQuestion("Is it raining?")
    #print path_to_jar
    #print path_to_models_jar

def isQuestion(sentence):
    sentence = addQuestionMark(sentence)
    #print sentence
    result = dependency_parser.raw_parse(sentence)
    
    #print type(result)
    for line in result:
        line.draw()
        if(isValidQuestion(line, 'SQ')):
            return random_response()
        return "I don't think I can answer that."
def isValidQuestion(parent, x):
    WHADJPPresent = False
    SQPresent = False
    for node in parent.subtrees():
        if type(node) is nltk.Tree:
            if (node.label() == x):
                #print "SQ found"
                SQPresent = True
            if (node.label() == "WHADJP" or node.label() == "WHNP" or node.label() == "WHADVP" ):
               #print "WHADJP found!"
               WHADJPPresent = True
    return (SQPresent and WHADJPPresent == False)
def addQuestionMark(sentence):
    if (sentence.endswith('?') == False):
        sentence = sentence + '?'
    return sentence
if __name__ == '__main__':
    main()
