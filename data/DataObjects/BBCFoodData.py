# -*- coding: utf-8 -*-
"""
Define the BBC Food Data Objects.
__author__ : Michele Trevisiol @trevi
__creation__ : Apr 2, 2015
"""

import json
import codecs
import cPickle as pickle
from ext.TextProcessingLib.TextProcessing import *


''' --------------------- '''
'''   DEFINE BBC OBJECT   '''
''' --------------------- '''
class BBCFood:

  def __init__(self):
    self.name = None  # e.g. "Whitecurrant"
    self.desc = None  # e.g. "Whitecurrants are transluscent pinkish-white berries that are similar in taste to redcurrants but slightly sweeter. "
    self.url = None   # e.g. "http://www.bbc.co.uk/food/whitecurrant"
  ##

  ''' '''
  def load_jdata( self, jdata ):
    # parsing data
    self.name = jdata['name']
    self.desc = jdata['description']
    self.url = jdata['url']
  ##

  def valid( self ):
    return False if self.name is None or self.desc is None else True
  ##

  ''' Copy all the words of the name together underscore-separated, 
    and split the words by space ''' 
  def getName( self, lower=False, stem="PorterStemmer" ):
    name = ''
    for block in self.name.encode('utf-8').strip().split(','):
      if lower:
        block = block.lower()
      processed = preprocess_pipeline( block.strip(), lang='english', \
      stemmer_type=stem, return_as_str=True, noAccents=True, \
      do_remove_stopwords=True, lower=False)
      # name += '%s %s ' %(processed,processed.strip().replace(' ','_'))
      name += '%s ' %processed
    return name.strip()

  def getDesc( self ):
    return self.desc.encode('utf-8')

##

