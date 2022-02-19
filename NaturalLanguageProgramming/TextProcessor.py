from calendar import c
from html import entities
from turtle import update
import nltk
import pandas as pd
import numpy as np
import contractions
import re
import math
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.featstruct import remove_variables
from nltk.tokenize import TreebankWordTokenizer
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.tokenize import TweetTokenizer
from nltk.tokenize import WhitespaceTokenizer
from textblob import TextBlob


class TextProcessor:
  """
  This is a class to preprocess natural language data(text).
  
  ...
  
  Attributes
  ----------
  raw_txt                              :   raw text feeded into object
  tokens(type==list)                   :   tokenized corpus
  filtered(type==list)                 :   list with removed stop words
  reduced(type==list)                  :   stemmed or lemmatized corpus
  corpus_dict(type==dict)              :   dictionary storing unique words in corpus
  onehotencoder(type=list(list))       :   one hot encoded bag of words
  raw_list_processed(type==list(list)) :   list of cleaned, tokenized and lemmatized class object for each document in corpus
  tfidf_out(type==list(list))          :   TF-IDF output
  
  
  Methods
  -------
  regular_exp():
      returns <simplyfid numbers and emails>
  
  tokeni(tokenizeon:str \\default = 'Whitespace'
            ):
      returns <tokenized data>
      tokenizeon() : [sent_tokenize, word_tokenize, TreebankWordTokenizer,wordpunct_tokenize, WhitespaceTokenizer, TweetTokenizer]

  remove_stopwords(language:str \\default ='english'
            ):
      returns <corpus after removing stopwords>
  
  
  sorl(method:str \\default = 'lemm'
            ):
      returns <stemmed or lemmatized corpus>
  
  get_preprocessed_text():
      returns <list of word tokens>

  auto_complete(method:str     \\default=='lemm'
                language:str   \\default=='english'
                tokenizeon:str \\default=='WhiteSpaceTokenizer'):
      returns <cleaned, tokenized and lemmatized corpus>
      
  bow(lang:str \\default = 'english'
            ):
      returns <one hot encoded bag of words>
  
  tfidf(lang:str \\default = 'english'
            ):
      returns <Term Frequency - Inverse Frequency 2D list>
  """
  def __init__(self,raw_txt):
    self.raw_txt      = raw_txt  #### Raw Input
    self.text         = ""
    self.tokens       = []       #### Tokenization Ouput
    self.filtered     = []       #### removed stopwords Ouput
    self.reduced      = []       #### Stemming or lemmatization output
    self.corpus_dict  = {}       #### Corpus Dictionary
    self.onehotencoder= []       #### Bag of words ouput
    self.raw_list_processed = [] #### list input processed ouput
    self.tfidf_out    = []       #### tfidf output 
    self.tf_idf_df    = pd.DataFrame() #### tfidf DataFrame
    self.bow_df       = pd.DataFrame() #### bag of words DataFrame
    self.pos_out      = []
    self.pos_tg       = []
    self.entities     = []
    self.n_grams      = []
  
  def clean(self) -> str:
    """
    Expanding contractions and cleaning of text is performed
      
      Parameters
      ----------
      None
    
      Returns
      -------
      string
      
    """
    self.FContrac = [contractions.fix(l) for l in self.raw_txt.split()]     #expanding contractions
    self.text = re.sub('[^A-Za-z0-9\s\.,\@]', '', ' '.join(self.FContrac))  #removes special characters
    self.text = re.sub('\s{2,}', ' ', self.text)                            #removes extra spaces
    # self.text = self.text.lower()
    return self.text
  
  def regular_exp(self) -> str:
    """
    simplifes numbers and emails
      
      Parameters
      ----------
      None
    
      Returns
      -------
      string
    """
    self.text = re.sub('\d+','<number>',self.text)                            #Simplifies numbers
    self.text = re.sub('\w[!-?A-~]*@\w[\w\.]*\w',  '<email_id>', self.text)   #Simplifies emails
    self.text = re.sub('[\.,]','',self.text)                                     #Removing "." & ","
    return self.text

  def regular_exp2(self) -> str:
    """
    simplifes numbers and emails
      
      Parameters
      ----------
      None
    
      Returns
      -------
      string
    """
    self.text = re.sub('\d+','<number>',self.text)                            #Simplifies numbers
    self.text = re.sub('\w[!-?A-~]*@\w[\w\.]*\w',  '<email_id>', self.text)   #Simplifies emails
    return self.text
  
  
  def tokeni(self, tokenizeon: str) -> list:
    """
    Tokenization is performed
    
      Parameters
      ----------
      tokenizeon : str
        any(sent_tokenize, word_tokenize, TreebankWordTokenizer,wordpunct_tokenize, WhitespaceTokenizer, TweetTokenizer)
      
      Returns
      -------
      list
    """    
    if tokenizeon == 'sent_tokenize':
      self.tokens = nltk.tokenize.sent_tokenize(self.text)                  
    elif tokenizeon == 'word_tokenize':
      self.tokens = nltk.tokenize.word_tokenize(self.text)                  
    elif tokenizeon == 'TreebankWordTokenizer':
      tk = TreebankWordTokenizer()
      self.tokens = tk.tokenize(self.text)
    elif tokenizeon == 'wordpunct_tokenize':
      self.tokens = nltk.tokenize.wordpunct_tokenize(self.text)
    elif tokenizeon == 'TweetTokenizer':
      tk = TweetTokenizer()
      self.tokens = tk.tokenize(self.text)
    elif tokenizeon == 'WhitespaceTokenizer':
      tk = WhitespaceTokenizer()
      self.tokens = tk.tokenize(self.text)  
    else:
      print("please check tokenizer provided")
    return self.tokens
  
  
  def remove_stopwords(self, language: str) -> list:
    """
    Function to remove stopwords using NLTK libraries
    
      Parameters
      ----------
      language : str   #default = WhitespaceTokenizer
      
      Returns
      -------
      list
    """
    stop_words = set(stopwords.words(language))                             #setting stop word langugage
    self.filtered = [w for w in self.tokens if not w.lower() in stop_words] #list comprehension to create a list without stop words.
    return self.filtered
  

  def sorl(self, method: str) -> list:
    """
    Stemming and lemmatization of data
    
      Parameters
      ----------
      method : str   #default = 'lemm'
      
      Returns
      -------
      list
      
    """
    if method == 'stem':
      ps = PorterStemmer()
      self.reduced = [ps.stem(w) for w in self.filtered]              #Stemming
    elif method == 'lemm':
      lem = WordNetLemmatizer()
      self.reduced = [lem.lemmatize(w) for w in self.filtered]        #Lemmatization
    else:
      print("please check method provided")
    return self.reduced
  

  def get_preprocessed_text(self) -> str:
    """
    Returns preprocessed data as list
    
      Parameters
      ----------
      None
      
      Returns
      -------
      list
    """
    return self.reduced
  
  def bow(self,lang:str = 'english') -> list:
    """
    Returns one hot encoded bag of words
    
      Parameters
      ----------
      lang : str   #default = 'english'
      
      Returns
      -------
      list(list)
    """
    # creating a list of cleaned, tokenized and lemmatized class object for each document in corpus 
    if not isinstance(self.raw_txt, list):
        self.raw_list_processed = [' '.join(TextProcessor(self.raw_txt).auto_complete(language = lang))]
    else:
        self.raw_list_processed = [' '.join(TextProcessor(i).auto_complete(language = lang)) for i in self.raw_txt]
    print("pre-processed_input: \n{}\n\n".format(self.raw_list_processed))

    #Finding unique word and storing as dictionary with defined values
    words = ""
    for i in self.raw_list_processed:
      words += ' ' + i
    unique_words = set(words[1:].split(' '))
    self.corpus_dict = dict(zip(unique_words, range(len(unique_words))))           #Corpus dictionary
    
    #Iterating through each document in processed corpus and one hot encoding them
    for i in self.raw_list_processed:
      self.onehotencoder.append(self.process_zero_array(i,len(unique_words)))
    self.bow_df = pd.DataFrame(self.onehotencoder, columns = list(self.corpus_dict.keys()))
    return self.onehotencoder
  
  def process_zero_array(self,document:list,unique_words_len:int)->list:
    """
    Returns one hot encoded list
    
      Parameters
      ----------
      document         : list
      unique_words_len : int
      
      Returns
      -------
      list
    """
    zero_array = np.zeros(unique_words_len)                 #Creating a zero array of number of unique words in corpus
    for i in document.split():                             #for each document sent from previous function as arguement 
      zero_array[self.corpus_dict[i]] = zero_array[self.corpus_dict[i]]+1  #self.corpus_dict[i] --> will give us location of word in list to increment
    return list(zero_array)
  
  
  #TF = No. of repetition of word in sentence/No. of words in Sentence
  #IDF = math.log(No. of sentences/ No. of sentences containing words, 2)
  #TF-IDF = TF*IDF
  
  
  def tfidf(self,lang:str = 'english'):
    """
    Returns Term Frequency - Inverse Document Frequency product vector
    
      Parameters
      ----------
      lang : str   #default = 'english'
      
      Returns
      -------
      list(list)
    """
    tf = self.bow(lang)         # getting bow() method one hot encoder output to further give intensity/importance of word in corpus
    print("initial tf : \n{}\n".format(tf))
                                                            #TF = No. of repetition of word in sentence/No. of words in Sentence
    for i in range(len(tf)):                                           #iterating through each one hot encoded vector
      for j in range(len(tf[i])):                                      #iteration index for each value in vector
        tf[i][j] = tf[i][j]/len(self.raw_list_processed[i].split())    #TF output is evaluated
    num_of_sentences = len(tf)
    count_dict = {key:0 for key,values in self.corpus_dict.items()}   #creating a zero values dictionary to increment values based on keys present in documents
    
    #Iterating through corpus dictionary and original list with words to find key and increment value if present
    for key,values in self.corpus_dict.items():
      for word in self.raw_list_processed:
        if key in word.split():
          count_dict[key] += 1
    print("count_dict: \n{}\n\n".format(count_dict))
    key_counts_in_document = list(count_dict.values())                     #Converting dictionary into list
    idf = [math.log(num_of_sentences/i) for i in key_counts_in_document]   #IDF = Natural_Logarithm(No. of sentences/ No. of sentences containing word)    
    print("tf = \n{}\n".format(tf))
    print("count dictionary: \n{}\n".format(count_dict))
    print("count in list for corpus: {}\n".format(key_counts_in_document))
    print("idf = \n{}\n".format(idf))
    tfidf_out = []
    for sent in tf:
      row = [sent[i]*idf[i] for i in range(len(sent))]
      tfidf_out.append(row)
    
    self.tf_idf_df = pd.DataFrame(tfidf_out, columns = list(self.corpus_dict.keys()))
#     print(df)
#     df.to_csv("maybeout1.csv")
    return tfidf_out
  
  
  
  def auto_complete(self,method: str = 'lemm', language: str = 'english', tokenizeon:str = 'WhitespaceTokenizer') -> str:
    """
    Auto pre-processes data
    
      Parameters
      ----------
      method: str     #default = 'lemm'
      language:str    #default = 'english'
      tokenizeon:str  #default = 'WhitespaceTokenizer'
      
      Returns
      -------
      list
    """
    self.clean()
    self.regular_exp()
    self.tokeni(tokenizeon)
    self.remove_stopwords(language)
    self.sorl(method)
    return self.get_preprocessed_text()
  
  def spell_correct1(self):
    tb = TextBlob(self.text)
    self.text = str(tb.correct())

  def spell_correct(self):
    self.text = re.sub('([A-Za-z]+)(\d+)',r'\g<1>', self.text)

  def spell_correct2(self):
    chunks = nltk.ne_chunk(self.pos_tg)
    updated_tokens = []
    for i in range(len(chunks)):
      print('chunk : {}'.format(chunks[i]))
      if not hasattr(chunks[i],'label'):
        if not re.match('(^N\w+|^PRP)',chunks[i][1]):
          # print('before: {} \n after: {}'.format(chunks[i][0],TextBlob(chunks[i][0]).correct()))
          chunks[i] = (str(TextBlob(chunks[i][0]).correct()),chunks[i][1])
        else:
          chunks[i] = (chunks[i][0], chunks[i][1])
        updated_tokens.append(chunks[i][0])
      else:
        updated_tokens.append(chunks[i][0][0])
    
    print('updated tokens : {}'.format(updated_tokens))
  
  def pos(self)->list:
    """Method to tag Parts of speech to words.

    Returns:
        list: POS tagged words
    
    Tag Description
    1.	CC	Coordinating conjunction
    2.	CD	Cardinal number
    3.	DT	Determiner
    4.	EX	Existential there
    5.	FW	Foreign word
    6.	IN	Preposition or subordinating conjunction
    7.	JJ	Adjective
    8.	JJR	Adjective, comparative
    9.	JJS	Adjective, superlative
    10.	LS	List item marker
    11.	MD	Modal
    12.	NN	Noun, singular or mass
    13.	NNS	Noun, plural
    14.	NNP	Proper noun, singular
    15.	NNPS	Proper noun, plural
    16.	PDT	Predeterminer
    17.	POS	Possessive ending
    18.	PRP	Personal pronoun
    19.	PRP$	Possessive pronoun
    20.	RB	Adverb
    21.	RBR	Adverb, comparative
    22.	RBS	Adverb, superlative
    23.	RP	Particle
    24.	SYM	Symbol
    25.	TO	to
    26.	UH	Interjection
    27.	VB	Verb, base form
    28.	VBD	Verb, past tense
    29.	VBG	Verb, gerund or present participle
    30.	VBN	Verb, past participle
    31.	VBP	Verb, non-3rd person singular present
    32.	VBZ	Verb, 3rd person singular present
    33.	WDT	Wh-determiner
    34.	WP	Wh-pronoun
    35.	WP$	Possessive wh-pronoun
    36.	WRB	Wh-adverb
    """
    self.pos_tg = nltk.pos_tag(self.tokens)
    self.pos_out = [pair[0]+'_'+pair[1] for pair in self.pos_tg]
    return self.pos_out

  
  def NameEntityRecognition(self)->list:
    """Method to tag Entites

    Returns:
        list: Tagged Entities
    """
    for chunk in nltk.ne_chunk(self.pos_tg):
      if hasattr(chunk, 'label'):
        self.entities.append((chunk.label(), chunk[0][0]+'_'+chunk[0][1]))
      else:
        self.entities.append((None,chunk[0]+'_'+chunk[1]))
    return self.entities
  
  def ngrams(self,n:int = 2)->list:
    """Method to create a list of n-grams

    Args:
        n (int, optional): Number of N-grams. Defaults to 2.

    Returns:
        list: list of n-grams
    """
    n_grms = nltk.ngrams(self.tokens,n)
    self.n_grams = [grams for grams in n_grms]
    return self.n_grams
  