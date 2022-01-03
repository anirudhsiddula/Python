# Problem Set 2, hangman.py
# Name: Anirudh Siddula (C0830486)
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string
from itertools import groupby

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    #Function returns True if all letters guessed are in secret word.
    guess = True
    for i in secret_word:
        #And operation to check every letter in secret word is present in letters_guessed.
        guess = guess and (i in letters_guessed) 
    return guess



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    temp_string = ''
    for i in secret_word:
        #Iterating through each letter to append in temporary variable if letter is in secret word else appending '_ ' 
        temp_string += i if i in letters_guessed else '_ ' 
    return temp_string



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    #returns ascii lowercase letters with stripped letters from letters guessed
    #join method will convert list to string
    return string.ascii_lowercase.strip(''.join(letters_guessed)) 
    
    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    char_tracker = []
    chances_left = 6
    warnings = 3
    #Initantiating program output
    print('Welcome to the game Hangman!\nI am thinking of a word that is {} letters long.\n'.format(len(secret_word))+'-'*10)
    print('You have {} warnings left.'.format(warnings))
    
    #while loop untill the chances or warnings runs out
    while chances_left>0 and warnings>=0:
        print('You have {} guesses left.\nAvailable letters: {}'.format(chances_left,get_available_letters(char_tracker)))
        ip = input('Please guess a letter: ')
        
        #condition to check if the character has already been guessed
        if ip.lower() in char_tracker:
            print('The character has already been guessed.')
            warnings-=1
            if warnings >= 0:
                print('You have {} warnings left.\n'.format(warnings)+'-'*10)
            continue
        
        #condition to check if input is a valid ascii letter
        elif ip in string.ascii_letters:
            char_tracker.append(ip.lower())
        else:
            print('Please enter a valid alphabet')
            warnings-=1
            if warnings >= 0:
                print('You have {} warnings left.\n'.format(warnings)+'-'*10)
            continue
        
        #checking if the last character appended(input) is in secret word
        if char_tracker[-1] in secret_word:
            print('Good guess: {}'.format(get_guessed_word(secret_word,char_tracker))+'\n'+'-'*10)
        #checking if the input is a vowel
        elif char_tracker[-1] in 'aeiou':
            print('Incorrect Vowel has been guess. Double penalty !'+'-'*10)
            chances_left-=2
        else:
            print('Oops! That letter is not in the my word: {}'.format(get_guessed_word(secret_word,char_tracker))+'\n'+'-'*10)
            chances_left-=1
        
        #breaking loop condition to check if the word is guessed before the chances run out.
        if is_word_guessed(secret_word,char_tracker):
            break
    
    #Final condition to print out the program output if the user has won or lost
    if is_word_guessed(secret_word,char_tracker):
        print('Congratulations, you won!.\nYour score for the game is {}'.format(chances_left*len([i for i in groupby(secret_word)])))
    else:
        print('Sorry, you ran out of guesses. The word was : {}'.format(secret_word))


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    boo=True
    for i in range(len(my_word)):
        #checking index of user word and other word if they are equal or '_' and function return False if not
        if my_word[i] in ('_',other_word[i]):
            continue
        else:
            return False
    return boo



def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    possible_words = []
    #Removing empty spaces in we have put in for user readability
    my_word = my_word.replace(' ','')
    
    #iterating through all letters in words file
    for i in wordlist:
        #condition to run further code only if the length matches as initial pre-requisite
        if len(i) == len(my_word):
            if match_with_gaps(my_word,i):
                possible_words.append(i)
    
    #output print statement for matches
    print('No matches found') if not possible_words else print('Possible word matches are: \n'+', '.join(possible_words))



def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    char_tracker = []
    chances_left = 6
    warnings = 3
    #Initantiating program output
    print('Welcome to the game Hangman!\nI am thinking of a word that is {} letters long.\n'.format(len(secret_word))+'-'*10)
    print('You have {} warnings left.'.format(warnings))
    
    #while loop untill the chances or warnings runs out
    while chances_left>0 and warnings>=0:
        print('You have {} guesses left.\nAvailable letters: {}'.format(chances_left,get_available_letters(char_tracker)))
        ip = input('Please guess a letter: ')
        
        #condition to check if the character has already been guessed
        if ip.lower() in char_tracker:
            print('The character has already been guessed.')
            warnings-=1
            if warnings >= 0:
                print('You have {} warnings left.\n'.format(warnings)+'-'*10)
            continue
        
        #condition to check if input is a valid ascii letter
        elif ip in string.ascii_letters:
            char_tracker.append(ip.lower())
        
        #handling hint condition to show hints on possible words.
        elif ip == '*':
            show_possible_matches(get_guessed_word(secret_word,char_tracker))
            continue
        else:
            print('Please enter a valid alphabet')
            warnings-=1
            if warnings >= 0:
                print('You have {} warnings left.\n'.format(warnings)+'-'*10)
            continue
        
        #checking if the last character appended(input) is in secret word
        if char_tracker[-1] in secret_word:
            print('Good guess: {}'.format(get_guessed_word(secret_word,char_tracker))+'\n'+'-'*10)
        #checking if the input is a vowel
        elif char_tracker[-1] in 'aeiou':
            print('Incorrect Vowel has been guess. Double penalty !'+'-'*10)
            chances_left-=2
        else:
            print('Oops! That letter is not in the my word: {}'.format(get_guessed_word(secret_word,char_tracker))+'\n'+'-'*10)
            chances_left-=1
        
        #breaking loop condition to check if the word is guessed before the chances run out.
        if is_word_guessed(secret_word,char_tracker):
            break
    
    #Final condition to print out the program output if the user has won or lost
    if is_word_guessed(secret_word,char_tracker):
        print('Congratulations, you won!.\nYour score for the game is {}'.format(chances_left*len([i for i in groupby(secret_word)])))
    else:
        print('Sorry, you ran out of guesses. The word was : {}'.format(secret_word))



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
#     secret_word = choose_word(wordlist)
#     hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
