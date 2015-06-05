# -*- coding: utf-8 -*-
"""
Train the word2vec models given the words/descriptions of the dishes.
__author__ : Michele Trevisiol @trevi
__creation__ : Apr 2, 2015
"""

import codecs
from optparse import OptionParser
from ext.GensimSemantic.GensimStatisticalProcessing import *


##
parser = OptionParser()
parser.add_option( '--phrases', dest='foodPhrases', default='food_dataset/bbc_menupages.phrases' )
parser.add_option( '--out', dest='outW2V', \
  default='food_dataset.w2v/w2v-food-bbc_menupages-MINCcount_SIZEsize.model')
parser.add_option( '--count', dest='count', default=3 ) 
parser.add_option( '--size', dest='size', default=100 ) 
##
(options, args) = parser.parse_args()
FOODFILE = options.foodPhrases
W2VCOUNT = int(options.count)
W2VSIZE = int(options.size)

W2VFILE = options.outW2V.replace('MINC','%d'%W2VCOUNT).replace('SIZE','%d'%W2VSIZE)
print 'loading dataset from %s' %FOODFILE

gs = GensimCore()

sentences = gs.load_sentences( FOODFILE, keep_only_ascii=False )
gs.build_model( sentences, min_count=W2VCOUNT, size=W2VSIZE, workers=6, downsampling=1e-3 )

gs.store_model( W2VFILE )
print 'stored model to %s' %W2VFILE