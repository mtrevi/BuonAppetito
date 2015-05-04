# -*- coding: utf-8 -*-
"""
Build model using GensimStatisticalProcessing
__author__ : Michele Trevisiol @trevi
"""

from optparse import OptionParser
from GensimStatisticalProcessing import *


## Important Params
parser = OptionParser()
parser.add_option( '-w', '--workers', dest='workers', help='No of CPUs', default=7 )
parser.add_option( '-c', '--minCount', dest='minCount', help='Min Count per Word', default=5 )
parser.add_option( '-f', '--features', dest='noFeatures', help='No of Features for word2vec', default=100 )
(options, args) = parser.parse_args()
#~ load params
WORKERS = int(options.workers)
MINCOUNT = int(options.minCount)
NOFEAT = int(options.noFeatures)
#~ paths
data1 = 'corpus/text8'
data2 = 'corpus/ucl-open-advertising-dataset.kw.adcopy.bz2'
data3 = 'corpus/yahoo-datapack-20150103-1m.kw.adcopy.bz2'
model1 = 'models/w2v-text8.%ssize.model' %NOFEAT
model2 = 'models/w2v-text8_ucl.%ssize.model' %NOFEAT
model3 = 'models/w2v-text8_ucl_yahoo.%ssize.model' %NOFEAT
##


''' 
Load Gensim models or build new one with given parameters 
'''
gs = GensimCore()
if os.path.exists( model3 ):
  # load model
  gs.load_model( model3 )
elif os.path.exists( model2 ):
  # load previous model
  gs.load_model( model2 )
  # load sentences of next data set
  sentences3 = gs.load_sentences( data3 )
  # update and store model
  gs.update_model( sentences3 )
  gs.store_model( model3 )
elif os.path.exists( model1 ):
  # load previous model
  gs.load_model( model1 )
  # load sentences of next data set
  sentences2 = gs.load_sentences( data2 )
  # update and store current model
  gs.update_model( sentences2 )
  gs.store_model( model2 )
  #
  ## same for model 3
  sentences3 = gs.load_sentences( data3 )
  gs.update_model( sentences3 )
  gs.store_model( model3 )
else:
  # load sentences
  sentences1 = gs.load_sentences( data1 )
  # build model
  gs.build_model( sentences1, min_count=MINCOUNT, size=NOFEAT, workers=WORKERS)
##