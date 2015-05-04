# -*- coding: utf-8 -*-
"""
Preprocessing text for statistical semantics using gensim: http://radimrehurek.com/gensim/
__author__ : Michele Trevisiol @trevi
URL: http://radimrehurek.com/2014/02/word2vec-tutorial/
"""

## import modules and set up logging
# %load_ext autoreload
# %autoreload 2
from ext.TextProcessingLib.TextProcessing import *
from gensim.models import word2vec
from time import time
import numpy as np
import logging
import sys
import os
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
##



''' -------------------------- '''
'''   DEFINE CREATIVE OBJECT   '''
''' -------------------------- '''
class GensimCore:

  def __init__(self):
    self.model = None

  def load_model(self, model_path, createdBy='gensim', binary=False):
    if createdBy == 'gensim':
      logging.info('--- loading model (gensim) [%s]' %model_path)
      self.model = word2vec.Word2Vec.load( model_path )
    #
    elif createdBy == 'google': # C binary format
      logging.info('--- loading binary model (google) [%s]' %model_path)
      self.model = word2vec.Word2Vec.load_word2vec_format(model_path, binary=binary)
    ##

  def store_model(self, model_path, static=False):
    # If you don't plan to train the model any further, calling 
    # init_sims will make the model much more memory-efficient.
    if static:
      self.model.init_sims(replace=True)
    self.model.save( model_path )
    logging.info('--- storing model (%s)'%model_path)
    ##

  ''' Load Sentences '''
  def load_sentences(self, CORPUS_PATH, keep_only_ascii=True):
    if not os.path.isfile(CORPUS_PATH):
      logging.error('[!] Corpus Not Found (%s)' %CORPUS_PATH)
      return
    else:
      logging.info('--- loading sentences from %s' %CORPUS_PATH)
      if 'text8' in CORPUS_PATH: # Load standard text8 
        sentences = word2vec.Text8Corpus(CORPUS_PATH)## 
      else: # Load custom corpus
        sentences = self.load_sentences_from_file(CORPUS_PATH, keep_only_ascii=keep_only_ascii)
    #
    return sentences
    ##

  ''' Create a model from scratch. 
    @param size = 300      # Word vector dimensionality                      
    @param min_count = 40  # Minimum word count                        
    @param workers = 4     # Number of threads to run in parallel
    @param context = 10    # Context window size
    @param downsampling = 1e-3   # Downsample setting for frequent words
  '''
  def build_model(self, sentences, \
      min_count=5, size=100, workers=6, context=10, downsampling=1e-3):
    logging.info('--- building model')
    logging.info('-- min_count: %d, size: %d, workers: %d' %(min_count,size,workers))
    self.model = word2vec.Word2Vec( sentences, workers=workers,\
                      size=size, min_count=min_count,  \
                      window = context, sample = downsampling ) 
    ##

  ''' Update model with the given corpus. '''
  def update_model(self, sentences):
    ## Update the model
    ## train the skip-gram model; default window=5 - min_count of words frequency
    logging.info('--- updating model')
    self.model.train( sentences )
    ##


  ''' Given a file path load and pre-process the sentences '''
  def load_sentences_from_file(self, file_path, keep_only_ascii=True, custom_stopwords=[]):
    ## Loading and cleaning input file
    sentences = []
    n_words = 0
    s = time()
    tpast = 0
    logging.info('loading dataset %s' %file_path)
    if 'bz2' in file_path:
      import bz2
      FSTREAM = open( bz2.BZ2File(file_path), 'r' )
    elif 'gz' in file_path:
      import gzip
      FSTREAM = open( gzip.open(file_path), 'r' )
    else:
      FSTREAM = open( file_path, 'r' )
    for line in FSTREAM:
      text = line.strip()
      ## Get language
      lang = get_best_language(text)
      ## Clean Text
      if keep_only_ascii:
        text = keep_only_ascii_chars(text,lower=True)
      else:
        text = text.lower()
      l_words = tokenize2words(text)
      if len(custom_stopwords) > 0:
        l_words = remove_custom_stopwords(l_words, stopwords=custom_stopwords)
      ## Remove Stopwords
      l_words = remove_stopwords(l_words,lang)
      ## Update list
      if len(l_words) > 0:
        sentences.append(l_words)
        n_words += len(l_words)
      ## Stats Update
      tstop = int(time()-s)
      if tstop%60 == 0 and tpast!=tstop:
        tpast = tstop
        logging.info('loaded %d sentences with %d words   ~%.2f seconds'%(len(sentences),n_words,time()-s) )
    logging.info('loaded %d sentences with %d words   ~%.2f seconds'%(len(sentences),n_words,time()-s) )
    FSTREAM.close()
    return sentences
    ## 


  ''' Evaluate the model: http://word2vec.googlecode.com/svn/trunk/questions-words.txt '''
  def evaluate(self, eval_file_path=''):
    if eval_file_path == '':
      eval_file_path = '%sext/evaluation-questions-words.txt'%self.path
    self.model.accuracy(eval_file_path)
  ##


  ''' Function to average all of the word vectors in a given paragraph '''
  def makeFeatureVec(self, words, num_features):
    # Pre-initialize an empty numpy array (for speed)
    featureVec = np.zeros((num_features,),dtype="float32")
    #
    nwords = 0.
    # 
    # Index2word is a list that contains the names of the words in 
    # the model's vocabulary. Convert it to a set, for speed 
    index2word_set = set(self.model.index2word)
    #
    # Loop over each word in the review and, if it is in the model's
    # vocaublary, add its feature vector to the total
    for word in words:
      if word in index2word_set: 
        nwords = nwords + 1.
        featureVec = np.add(featureVec,self.model[word])
    # 
    # Divide the result by the number of words to get the average
    featureVec = np.divide(featureVec,nwords)
    return featureVec


  ''' Given a set of reviews (each one a list of words), calculate 
      the average feature vector for each one and return a 2D numpy array '''
  def getAvgFeatureVecs(self, reviews, num_features):
    # Initialize a counter
    counter = 0.
    # 
    # Preallocate a 2D numpy array, for speed
    reviewFeatureVecs = np.zeros((len(reviews),num_features),dtype="float32")
    # 
    # Loop through the reviews
    for review in reviews:
      #
      # Print a status message every 1000th review
      if counter%1000. == 0.:
        print "Review %d of %d" % (counter, len(reviews))
      # 
      # Call the function (defined above) that makes average feature vectors
      reviewFeatureVecs[counter] = makeFeatureVec(review, self.model, num_features)
      #
      # Increment the counter
      counter = counter + 1.
    return reviewFeatureVecs
    ##


  # ****************************************************************
  # Calculate average feature vectors for given set of words.
  # def computeFeature
  # list_of_sentences = []
  # data_vecs = self.getAvgFeatureVecs( clean_train_reviews, model, num_features )

  ##
##


# gs = GensimCore()
# gs.load_model()


def devel():
  ##
  ## Ho to use the word-vector to compare two sets of text.
  ## https://www.kaggle.com/c/word2vec-nlp-tutorial/details/part-3-more-fun-with-word-vectors
  model['king'] # returns the feature vector for that word

  # ... and some hours later... just as advertised...
  model.most_similar(positive=['woman', 'king'], negative=['man'], topn=1)
  [('queen', 0.5359965)]
   
  # pickle the entire model to disk, so we can load&resume training later
  model.save('/tmp/text8.model')
  # store the learned weights, in a format the original C tool understands
  model.save_word2vec_format('/tmp/text8.model.bin', binary=True)
  # or, import word weights created by the (faster) C word2vec
  # this way, you can switch between the C/Python toolkits easily
  model = word2vec.Word2Vec.load_word2vec_format('/tmp/vectors.bin', binary=True)
   
  # "boy" is to "father" as "girl" is to ...?
  model.most_similar(['girl', 'father'], ['boy'], topn=3)
  more_examples = ["he his she", "big bigger bad", "going went being"]
  for example in more_examples:
    a, b, x = example.split()
    predicted = model.most_similar([x, b], [a])[0][0]
    print "'%s' is to '%s' as '%s' is to '%s'" % (a, b, x, predicted)
   
  # which word doesn't go with the others?
  model.doesnt_match("breakfast cereal dinner lunch".split())
  'cereal'