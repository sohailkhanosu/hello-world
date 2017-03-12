"""
    Word Statistics
    Author: Sohail Khan

    This program is free software: you can redistribute it and/or modify it
    under the terms of the MIT License. A copy of the license is included with
    this project. If you cannot find the license, please contact the authors.


    Word Statistics
    You can input a file or enter text on command line for processing
"""
import getopt
import sys
import os
import re
import string
import StringIO

from collections import defaultdict

def usage():
    print("Word Statistics Usage")
    print("q1.py [-f --file file_to_count_statistics]")
    print("      [-o --out  file to output stats to]")
    print("      [-i --input]")
    print("      [-h]")
    

def getArgs(args):
    """ Get the args from stdin
    Args:
        args (list): list of args from stdin
    Returns:
        (dict): dict of args and values """

    args_dict = {'file': None}
    try:
        opts, args = getopt.getopt(args,'hif:o:', ["help","input",  "file=","out="])
    except getopt.GetoptError as error:
        print(str(error))
        usage()
        sys.exit(2)

    # parse the opts
    for o,a in opts:
        if o in ['-h', 'help']:
            usage()
            sys.exit(1)
        elif o in ['-f', '--file']: 
            if not os.path.exists(a):
                print("That file does not exist")
                sys.exit(1)
            args_dict['file'] = a
        elif o in ['-o', '--out']:
            args_dict['out'] = a
        elif o in ['-i', '--input']:
            args_dict['content'] = raw_input("Enter your text: ")
        else:
            print("command not recognized")
            usage()
            sys.exit(1)

    return args_dict            

def openFile(file_name):
    """Opens file and returns the contents unmodified
    Args:
        file_name (str): file name
    Returns:
        (str): file content
    """    
    with open(file_name, 'r') as fp:
        return fp.read()    

def print_results(result_dict):
    """ prints result of statistics
    Args:
        result_dict (dict): statistics """
    for (statistic, value) in result_dict.items():
        print("{:40}: {:10}".format(statistic, value))
    print("")

        

def get_word_count(content):
    return len(filter(lambda word: word != "", re.split(r'\W', content)))

def get_sentence_count(content):
    return len(re.split(r'[?.!]', content))

def get_unique_words(content):
    return len( set( map(
                    lambda word: word.strip(string.punctuation),
                                 re.split(r'\W', content))))
    
def get_n_common_phrases(content, n, threshold=3):
    """ returns dictionary of common phrases of length up to n.
        Specify threshold to ignore less frequent words
    Args:
        content (str): content
        n (int): phrase length
        threshold (int): ignore phrases with counts less than this
    Returns:
        (dict): phrase dict of form phrase:count
    """
    words = filter(lambda word: word != "", re.split(r'\W', content))
    content = content.lower()

    phrases_dict = {}
    for i in range(len(words) - n):
        current_phrase = " ".join(words[i:i+n])
        current_phrase = current_phrase.strip().lower()
        current_phrase_count = content.count(current_phrase) 
        if current_phrase_count > threshold:
            phrases_dict[current_phrase] = current_phrase_count
    return phrases_dict
            

def get_word_frequencies(content):
    """ returns frequency dict of words """
    
    def add_to_dict(d, word):
        """ helper function to add to default dict """
        d[word] += 1

    word_counts_dict = defaultdict(int)

    words = filter(lambda word: word != "", re.split(r'\W', content))
    words_lowered = map(lambda word: word.lower(), words)
    
    total_words = len(words_lowered)
    
    map(lambda word: add_to_dict(word_counts_dict, word), words_lowered)

    return dict(map(lambda (k,v): (k, v/float(total_words)), 
                word_counts_dict.items()))

    

if __name__ == "__main__":
    args_dict = getArgs(sys.argv[1:])
    
    if args_dict.get('file'):
        content = openFile(args_dict.get('file'))
    elif args_dict.get('content'):
        content = args_dict.get('content')
    else:
        usage()
        sys.exit(1)

    if args_dict.get('out'):
        sys.stdout = open(args_dict.get('out'),'w')

    statistics_dict = {} 
    
    statistics_dict['Total word count'] = get_word_count(content)
    statistics_dict['Sentences'] = get_sentence_count(content)
    statistics_dict['Unique words'] = get_unique_words(content)
    statistics_dict['Words/Sentence'] = (statistics_dict['Total word count']/
                                         float(statistics_dict['Sentences']))

    print_results(statistics_dict)

    common_phrases = get_n_common_phrases(content, 4, 2)

    print("common phrases:")
    for k in sorted(common_phrases, key=common_phrases.__getitem__, 
                     reverse=True):
        print "{}:{:10}".format(k, common_phrases[k])
    else:
        print("None")
        print("")

    word_frequencies = get_word_frequencies(content)

    print("Words in order of descending frequency")
    for word in sorted(word_frequencies, key=word_frequencies.__getitem__,
                       reverse=True)[:100]:
        print(word)

    

