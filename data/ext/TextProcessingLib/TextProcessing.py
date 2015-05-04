# -*- coding: utf-8 -*-
"""
Preprocessing text and html (Tokenizing words and sentences, clean HTML, clean text, removing stopwords, stemming and lemmatization)
__author__ : Michele Trevisiol @trevi
"""

from nltk import clean_html
from nltk import SnowballStemmer
from nltk import PorterStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize, wordpunct_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')
from sklearn.metrics import pairwise_distances
import numpy as np

import unicodedata
import string
import sys
import re


# =========== #
# TEXT CODING #
# =========== #
''' Convert from UNICODE to ASCII '''
def toASCII(string):
   import unicodedata
   return unicodedata.normalize('NFKD', string).encode('ASCII', 'ignore')


# ====================== #
# LANGUAGE RELATED TOOLS #
# ====================== #
''' Based on nltk, so the value of the language is compatible 
   with the dictionaries of nltk (e.g., 'english' not 'en')
   @input string:
   @output string with dictionary name '''
def get_language(string):
   languages_ratios = {}
   tokens = wordpunct_tokenize(string)
   words = [word.lower() for word in tokens]
   for language in stopwords.fileids():
      stopwords_set = set(stopwords.words(language))
      words_set = set(words)
      common_elements = words_set.intersection(stopwords_set)
      languages_ratios[language] = len(common_elements) # language "score"
   ## Finally, we only have to get the “key” with biggest “value”:
   return max(languages_ratios, key=languages_ratios.get)

''' Exploit the external package "langid" that you can find at the following link:
   https://github.com/saffsd/langid.py adapting the output to nltk. 
   '''
def get_language_langid(string, verbose=False):
   import langid
   ## dictionary
   lang_code = {'en':'english', 'es':'spanish', 'it':'italian', 'fr':'french', 'ru':'russian', 'tr':'turkish', 'no':'norwegian', 'da':'danish', 'fi':'finnish', 'nl':'dutch', 'de':'german', 'pt':'portuguese', 'hu':'hungarian', 'sv':'swedish'}
   ## detect language
   if len(string) == 0:
      return ''
   lang_score = langid.classify(string)
   ## get language code
   if not lang_code.has_key(lang_score[0]):
      if verbose:
         print >> sys.stderr, 'Language not supported: %s' %str(lang_score)
      return ''
   return lang_code[lang_score[0]]

''' Language Recognition based on two approaches. 
   First langid, then the stopwords trick. '''
def get_best_language(string, default='english', verbose=False):
   lang = get_language_langid(string, verbose=False)
   # if len(lang) <= 2:
      # lang = get_language(string)
   if len(lang) <= 2:
      return default
   return lang



# ========================= #
# CLEANING AND TOKENIZATION #
# ========================= # 
''' Tokenize text into words.
   @input text: string
   @param lower: flag for lowercase conversion
   @output: list of words '''
def tokenize2words(text, lower=False, return_as_str=False):
   toker = RegexpTokenizer(r'((?<=[^\w\s])\w(?=[^\w\s])|(\W))+', gaps=True)
   l_words = toker.tokenize(text.lower()) if lower else toker.tokenize(text)
   if return_as_str:
      return ' '.join(l_words)
   else:
      return l_words
   ##
##

''' Given a string, parse each character of each word and keep only the ones
   that actually belong to the ascii letters. '''
def keep_only_ascii_chars(data, lower=False):
   data = u'%s' %data
   new_data = ''
   if lower:
      data = data.lower()
   for w in data.strip().split(' '):
      new_data += ''.join(x for x in unicodedata.normalize('NFKD', w) if x in string.ascii_letters) + ' '
   return new_data.strip()
##

''' Tokenizes into sentences, strips punctuation/abbr, converts to lowercase and tokenizes words.
   @output: list of words '''
def tokenize2sentences2words(str, outputString=False):
   return [word_tokenize(" ".join(re.findall(r'\w+', t,flags = re.UNICODE | re.LOCALE)).lower()) for t in sent_tokenize(str.replace("'", ""))]
   ##
##




# ===================== #
# BASIC TEXT PROCESSING #
# ===================== #
''' Removing stopwords. 
   @input l_words: list of words
   @input lang: language
   @output content: outputs list of words '''
def remove_stopwords(l_words, lang=''):
   if len(l_words) == 0:
      return []
   test = ' '.join(l_words)
   ## get language if not defined
   if len(lang) == 0:
      lang = get_best_language(' '.join(l_words))
   ## set english as default if language is not identified
   if len(lang) <= 2:
      lang = 'english'
   ## remove stopwords
   l_stopwords = stopwords.words(lang)
   content = [w for w in l_words if w.lower() not in l_stopwords]
   return content
##

''' Removing stopwords from custom list. 
   @input l_words: list of words
   @input stopwords: custom list of stopword
   @output content: outputs list of words '''
def remove_custom_stopwords(l_words, stopwords=['www','com','it','fr','br','co']):
   out_words = []
   for w in l_words:
      if len(w) <=2 or w in kw_stopwords:
         continue
      else:
         out_words.append(w)
   return out_words
   ##
##

''' Stem all words with stemmer of type, return encoded as "encoding" '''
def stemming(words_l, type="PorterStemmer", lang="english", encoding="utf8"):
   supported_stemmers = ["PorterStemmer","SnowballStemmer","LancasterStemmer","WordNetLemmatizer"]
   if type is False or type not in supported_stemmers:
      return words_l
   else:
      l = []
      if type == "PorterStemmer":
         stemmer = PorterStemmer()
         for word in words_l:
            l.append(stemmer.stem(word).encode(encoding))
      if type == "SnowballStemmer":
         stemmer = SnowballStemmer(lang)
         for word in words_l:
            l.append(stemmer.stem(word).encode(encoding))
      if type == "LancasterStemmer":
         stemmer = LancasterStemmer()
         for word in words_l:
            l.append(stemmer.stem(word).encode(encoding))
      if type == "WordNetLemmatizer": #TODO: context
         wnl = WordNetLemmatizer()
         for word in words_l:
            l.append(wnl.lemmatize(word).encode(encoding))
      return l
   ##
##



# ==================== #
# HTML TEXT PROCESSING #
# ==================== # 
''' Clean HTML / strip tags TODO: remove page boilerplate (find main content), support email, pdf(?) '''
def html2text(str):
   return clean_html(str)
##

def extract_text_from_html(html):
   from BeautifulSoup import BeautifulSoup
   soup = BeautifulSoup(html)
   body = soup.find('body')
   text_list = [b.string for b in soup.findAll('p')]
   # text_list = [b.string for b in soup.findAll('div')]
   # combine all the elements
   text_list_clean = []
   for val in text_list:
      if val is not None and val is not '': 
         text_list_clean.append(val)
   text_string = ' '.join(text_list_clean)
   return text_string.strip()
##


# ==================== #
# PROCESSING PIPELINES #
# ==================== # 
''' Basic Text Processing Pipeline with 
   @input text: 
   @param lang:
   @param stemmer_type:
   @param return_as_str: return the procssed string or a list of words
   @param do_remove_stopwords:
   @output: string or list of words
   '''
def preprocess_pipeline(text, lang='', stemmer_type="PorterStemmer", return_as_str=False, do_remove_stopwords=False, lower=True, noAccents=True, custom_stopwords=[]):
   if len(text) == 0:
      return ''
   l_words = []
   # remove accents
   if noAccents:
      try:
         text = keep_only_ascii_chars( text )
      except:
         pass
   # detect language
   if lang == '':
      lang = get_language(text)
   # tokenize (remove also puntuation)
   l_words = tokenize2words(text, lower=lower)
   # remove stopwords
   if do_remove_stopwords and lang != '':
      l_words = remove_stopwords(l_words, lang)
   # clean words
   if len(custom_stopwords) > 0:
      l_words = remove_custom_stopwords(l_words)
   # apply stemming
   if stemmer_type is not None:
      l_words = stemming(l_words, stemmer_type, lang=lang)
   if return_as_str:
      return " ".join(l_words)
   else:
      return l_words
   ##
##


''' TermFrequency Text Processing Pipeline, Call the *preprocess_pipeline* and then compute TF
   @input test: 
   @param lang: if empty the module will detect automatically the language
   @param stemmer_type:
   @param return_as_str: return the procssed string or a list of words
   @param do_remove_stopwords:
   @output: string or list of words
   '''
def pipeline_tf(text, lang='', stemmer_type="PorterStemmer", do_remove_stopwords=False):
   if len(text) == 0:
      return ''
   # Get language with langid, it it fails, then use the nltk trick
   if len(lang) == 0:
      lang = get_best_language(text)
   # call the preprocess_pipeline
   return_as_str = False
   l_words = preprocess_pipeline(text=text, lang=lang, return_as_str=return_as_str, stemmer_type=stemmer_type, do_remove_stopwords=do_remove_stopwords)
   # compute TF for each words
   l_words_tf = compute_tf(l_words)
   # return
   return l_words_tf



# ================== #
# SIMILARITY METRICS #
# ================== #
def cosine_similarity(vect_1, vect_2):
   m = np.array([vect_1, vect_2])
   return (1-pairwise_distances(m, metric="cosine"))[0,1]

def jaccard_distance(a, b):
   # convert to set 
   if type(a) == list:
      a = set(a)
   if type(b) == list:
      b = set(b)
   # compute intersection
   c = a.intersection(b)
   #
   return float(len(c)) / (len(a) + len(b) - len(c))
   ##

''' Compute Similarity Score with Word2Vect (Gensim).
   @input gs: Gensim Object that contain the word2vec model
   @param of: Specify among what to compute the similarity
   @output: Cosine Similarity Score of the gensim vectors '''
def w2v_similarity(gs, l_1, l_2, NOFEAT=100):
   # compute vectors
   vect_1 = gs.makeFeatureVec( l_1, NOFEAT )
   vect_2 = gs.makeFeatureVec( l_2, NOFEAT )
   #
   return cosine_similarity(vect_1,vect_2)
   ##

''' Compute TF-score between of given text parts (Keywords, AdCopy, or Landing Page). 
   @input d_tf_1: dictionary of word-tf scores 
   @input d_tf_2: dictionary of word-tf scores 
   @param stemmer_type:
   @param do_remove_stopwords:
   @param of: Specify among what to compute the similarity
   @output: cosine similarity score '''
def tf_similarity(d_tf_1, d_tf_2):
   if len(d_tf_1.keys()) == 0 or len(d_tf_2.keys()) == 0:
      return 'NA'
   ## Compute Score
   vect_1, vect_2 = build_comparable_tf_vectors( d_tf_1, d_tf_2, normalize=True )
   return cosine_similarity(vect_1, vect_2)
   ##

def tfidf_similarity( collection_size, d_idf, d_tf_1, d_tf_2 ):
   if len(d_tf_1.keys()) == 0 or len(d_tf_2.keys()) == 0:
      return 'NA'
   ## compute TF*IDF for each term
   d_idf_1 = {}
   for t in d_tf_1.keys():
      t_idf = float(collection_size) / 1+len(d_idf[t])
      d_idf_1[t] = d_tf_1[t] * t_idf
   #
   d_idf_2 = {}
   for t in d_tf_2:
      t_idf = float(collection_size) / 1+len(d_idf[t])
      d_idf_2[t] = d_tf_2[t] * t_idf
   ## compute comparable vectors
   vect_1, vect_2 = build_comparable_tf_vectors( d_idf_1, d_idf_2, normalize=True )
   ## 
   return cosine_similarity(vect_1, vect_2)
   ##

''' Given a list of words comput the TF.
   @input l_words: list of words
   @output: dictionary with K:word and V:tf '''
def compute_tf(l_words):
   tf = {}
   for w in l_words:
      tf[w] = tf[w]+1 if tf.has_key(w) else 1
   ##
   return tf

''' Given two TF-words vectors, make them with the same length.
   @input tf_words_1: dictionary with word:tf
   @input tf_words_2: dictionary with word:tf '''
def build_comparable_tf_vectors(tf_words_1, tf_words_2, normalize=False):
   corpus = set(tf_words_1.keys()+tf_words_2.keys())
   vect_length = len(corpus)
   # define output vectors
   out_vect_1 = [0] * vect_length
   out_vect_2 = [0] * vect_length
   # 
   i = 0
   for w in corpus:
      if w in tf_words_1:
         out_vect_1[i] = tf_words_1[w]
      if w in tf_words_2:
         # print w, out_vect_2[i], tf_words_2[w]
         out_vect_2[i] = tf_words_2[w]
      i += 1
   #
   if normalize:
      return normalize_tf_list(out_vect_1), normalize_tf_list(out_vect_2)
   #
   return out_vect_1, out_vect_2
   ##

def normalize_tf_list(l_words, norm_type='l1'):
   ## check normalization type
   if norm_type == 'l1':
      l_sum = sum(l_words)
      for i in range(0,len(l_words)):
         l_words[i] = float(l_words[i])/l_sum
   ##
   return l_words

def normalize_tf_dict(d_words, norm_type='l1'):
   ## check normalization type
   if norm_type == 'l1':
      d_sum = sum(d_words.values())
      for k,v in d_words:
         d_words[k] = float(v)/d_sum
   ##
   return d_words




# =================== #
# SEMANTIC EXTRACTION #
# =================== #
''' Filter words that match the given POS_type.
   @input l_words: list of words
   @param pos_type: type of POS (e.g. 'NN', 'NNP', ..)
   @outout: list of words with POS equal to POS_type
   '''
def filter_POS_type(l_words, pos_type='NN'):
   from nltk import pos_tag, ne_chunk
   ## select only nouns from l_words
   return [word for word,pos in pos_tag( l_words ) if pos == pos_type]
