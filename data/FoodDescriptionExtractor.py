# -*- coding: utf-8 -*-
"""
Parse the crawled food data sets and build up the sentences for w2v.
__author__ : Michele Trevisiol @trevi
__creation__ : Apr 2, 2015
"""

import os
import sys
import json
from optparse import OptionParser
from DataObjects.BBCFoodData import *
from ext.TextProcessingLib.TextProcessing import *
reload(sys)
sys.setdefaultencoding('utf8')


##
parser = OptionParser()
parser.add_option( '--bbc', dest='bbcData', default='food_dataset/food_bbc_crawled_dataset.json' )
parser.add_option( '--mp', dest='menuPages', default='food_dataset/menupages-name_url_desc_price.tsv' )
##
(options, args) = parser.parse_args()
BBCFILE = options.bbcData
MPFILE = options.menuPages


'''
Extract BBC food-ingredients data set.
'''
if BBCFILE != 'None':
  BBCOUT = BBCFILE.replace('json','phrases')
  outstream = open( BBCOUT, 'w+' )
  print 'Loading BBC food-ingredients (from: %s)' %BBCFILE
  lines = 0
  valid = 0
  uncompleted = 0
  ## load entire json
  jdata = json.load(open(BBCFILE, 'r'))
  for j in range(0,len(jdata)):
    lines += 1
    bbc = BBCFood()
    bbc.load_jdata( jdata[j] )
    ## check desc
    if bbc.valid():
      ## tokenize and store
      name = bbc.getName( lower=True, stem=None )
      name.replace(' ', '_')
      desc = preprocess_pipeline( bbc.getDesc(), lang='english', \
        stemmer_type=None, return_as_str=True, \
        do_remove_stopwords=True )
      desc_stem = preprocess_pipeline( bbc.getDesc(), lang='english', \
        stemmer_type="PorterStemmer", return_as_str=True, \
        do_remove_stopwords=True )
      outstream.write( '%s\t%s\t%s\n' %(name, desc, desc_stem) )
      valid += 1
    else:
      uncompleted += 1
  outstream.close()
  print '\t-> parsed %d food-ingredients (%d valid, %d uncompleted)' %(lines, valid, uncompleted)
  ## get stats about categories
  print '\t-> saved BBC food-ingredients phrases to "%s"' %BBCOUT



'''
Extract MenuPages food data set.
'''
if MPFILE != 'None':
  MPOUT = MPFILE.replace('tsv','phrases')
  outstream = open( MPOUT, 'w+' )
  print 'Loading MenuPages food (from: %s)' %MPFILE
  lines = 0
  valid = 0
  uncompleted = 0
  ## 
  for line in open(MPFILE):
    b = line.strip().split('\t')
    if len(b) < 4:
      uncompleted += 1
      continue
    dish_name = b[2].strip().replace(' ','_')
    dish_desc = preprocess_pipeline( b[3].strip(), \
        stemmer_type=None, return_as_str=True, \
        do_remove_stopwords=True )
    dish_desc_stem = preprocess_pipeline( b[3].strip(), \
        stemmer_type="PorterStemmer", return_as_str=True, \
        do_remove_stopwords=True )
    lines += 1
    ## 
    outstream.write( '%s\t%s\t%s\n' %(dish_name, dish_desc, dish_desc_stem) )
  outstream.close()
  print '\t-> parsed %d food (%d uncompleted)' %(lines,uncompleted)
  ## get stats about categories
  print '\t-> saved MenuPages food phrases to "%s"' %MPOUT
