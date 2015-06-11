# -*- coding: utf-8 -*-
"""
Parse the review with text processing, get sentences 
and infer positive and negative emotions with EmotionsLIWClib
__source__ : http://www.yelp.com/dataset_challenge
__source__ : https://github.com/Yelp/dataset-examples
__author__ : Michele Trevisiol @trevi
"""

import os
import sys
import json
import codecs
import configparser
import cPickle as pickle
from optparse import OptionParser
from DataObjects.YelpBusinessData import *
from DataObjects.YelpReviewData import *
from DataObjects.YelpUserData import *

sys.path.append("../")
##
parser = OptionParser()
parser.add_option( '-c', '--config', dest='configFile', 
  default='../BuonAppetito.conf', help='Path of the configuration file')
##
(options, args) = parser.parse_args()
CONFILE = options.configFile
config = configparser.ConfigParser().read(CONFILE)
YBOFILE = config.get('ProfilesBuilder', 'YelpBusinessObj')
YROFILE = config.get('ProfilesBuilder', 'YelpReviewObj')
YUOFILE = config.get('ProfilesBuilder', 'YelpUserObj')
OUTFILE = config['DataProcessing']['outFile']

''' ------------------------- '''
'''   DEFINE LIWC OBJECT      '''
''' ------------------------- '''
class YelpProfile:

   def __init__(self):
      self.d_businessIds = {} 

  '''
  Load/Build Business Yelp Dataset Container.
  '''
  def load_yelp_business():
    if YBFILE is not None:
      YB_OUTFILE = OUTFILE.replace('TYPE','restaurants_business')
      if os.path.exists( YB_OUTFILE ):
        print '[found] Loading Business Container (%s)' %YB_OUTFILE
        businessContainer = pickle.load( open( YB_OUTFILE, "rb" ) )
        print '\t-> loaded %d business' %businessContainer.len()
      else:
        print 'Generating Business Container (from: %s)' %YBFILE
        businessContainer = YelpBusinessContainer()
        businessContainer.load_dataset( YBFILE, categories=['Restaurant'], verbose=False )
        print '\t-> loaded %d business (belonging to categories: "restaurant")' %businessContainer.len()
        ## get stats about categories
        print '\t-> saving business container to "%s"' %YB_OUTFILE
        pickle.dump( businessContainer, open( YB_OUTFILE, "wb" ) )
      ##
    ''' Extract Dictionary of Business Ids '''
    print 'Copying Business Ids into a Dictionary'
    for bid in businessContainer.getIds():
      if not self.d_businessIds.has_key( bid ):
        self.d_businessIds[ bid ] = 0
      self.d_businessIds[ bid ] += 1
    print '\t-> get %d business ids' %len(self.d_businessIds)


  '''
  Load/Build Review Yelp Dataset Container.
  '''
  def load_yelp_review():
    if YRFILE is not None:
      YR_OUTFILE = OUTFILE.replace('TYPE','restaurants_review')
      print 'Generating Review Container (from: %s)' %YRFILE
      reviewContainer = YelpReviewContainer()
      discarded = reviewContainer.load_dataset( YRFILE, business_ids=self.d_businessIds, verbose=False )
      print '\t-> loaded %d reviews (%d discarded)' %(reviewContainer.len(),discarded)
      ## get stats about categories
      print '\t-> saving review container (to "%s")' %YR_OUTFILE
      pickle.dump( reviewContainer, open( YR_OUTFILE, "wb" ) )
      ##
    else:
      print >> sys.stderr, 'Wrong Declaration of CONFIG FILE'


  '''
  Load/Build Users Yelp Dataset Container.
  '''
  def load_yelp_users():
    if YUFILE is not None:
      YU_OUTFILE = OUTFILE.replace('TYPE','restaurants_users')
      print 'Generating User Container (from: %s)' %YUFILE
      userContainer = YelpUserContainer()
      userContainer.load_dataset( YUFILE, verbose=False )
      print '\t-> loaded %d users' %userContainer.len()
      ## get stats about categories
      print '\t-> saving user container (to "%s")' %YU_OUTFILE
      pickle.dump( userContainer, open( YU_OUTFILE, "wb" ) )
      ##
    else:
      print >> sys.stderr, 'Wrong Declaration of CONFIG FILE'
