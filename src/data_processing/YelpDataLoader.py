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
from ConfigParser import SafeConfigParser
import cPickle as pickle

sys.path.insert(0, '../../')
from model.YelpBusinessData import *
from model.YelpReviewData import *
from model.YelpUserData import *



''' ------------------------- '''
'''   DEFINE LIWC OBJECT      '''
''' ------------------------- '''
class YelpDataLoader:

  def __init__(self, CONFILE):
    config = SafeConfigParser()
    config.read(CONFILE)
    self.YB = config.get('DataProcessing', 'YelpBusiness')
    self.YR = config.get('DataProcessing', 'YelpReview')
    self.YU = config.get('DataProcessing', 'YelpUser')
    self.OUTFILE = config.get('DataProcessing', 'outFile')
    self.d_businessIds = {}

  '''
  Load/Build Business Yelp Dataset Container.
  '''
  def load_yelp_business(self):
    if self.YB is not None:
      YB_OUTFILE = self.OUTFILE.replace('TYPE','restaurants_business')
      if os.path.exists( YB_OUTFILE ):
        print '[found] Loading Business Container (%s)' %YB_OUTFILE
        businessContainer = pickle.load( open( YB_OUTFILE, "rb" ) )
        print '\t-> loaded %d business' %businessContainer.len()
      else:
        print 'Generating Business Container (from: %s)' %self.YB
        businessContainer = YelpBusinessContainer()
        businessContainer.load_dataset( self.YB, categories=['Restaurant'], verbose=False )
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
  #


  '''
  Load/Build Review Yelp Dataset Container.
  '''
  def load_yelp_review(self):
    if self.YR is not None:
      YR_OUTFILE = self.OUTFILE.replace('TYPE','restaurants_review')
      print 'Generating Review Container (from: %s)' %self.YR
      reviewContainer = YelpReviewContainer()
      discarded = reviewContainer.load_dataset( self.YR, business_ids=self.d_businessIds, verbose=False )
      print '\t-> loaded %d reviews (%d discarded)' %(reviewContainer.len(),discarded)
      ## get stats about categories
      print '\t-> saving review container (to "%s")' %YR_OUTFILE
      pickle.dump( reviewContainer, open( YR_OUTFILE, "wb" ) )
      ##
    else:
      print >> sys.stderr, 'Wrong Declaration of CONFIG FILE'
  #


  '''
  Load/Build Users Yelp Dataset Container.
  '''
  def load_yelp_users(self):
    if self.YU is not None:
      YU_OUTFILE = self.OUTFILE.replace('TYPE','restaurants_users')
      print 'Generating User Container (from: %s)' %self.YU
      userContainer = YelpUserContainer()
      userContainer.load_dataset( self.YU, verbose=False )
      print '\t-> loaded %d users' %userContainer.len()
      ## get stats about categories
      print '\t-> saving user container (to "%s")' %YU_OUTFILE
      pickle.dump( userContainer, open( YU_OUTFILE, "wb" ) )
      ##
    else:
      print >> sys.stderr, 'Wrong Declaration of CONFIG FILE'
  #