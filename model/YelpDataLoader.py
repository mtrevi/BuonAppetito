# -*- coding: utf-8 -*-
"""
Parse the review with text processing, get sentences 
and infer positive and negative emotions with EmotionsLIWClib
__source__ : http://www.yelp.com/dataset_challenge
__source__ : https://github.com/Yelp/dataset-examples
__author__ : Michele Trevisiol @trevi
"""

import os
import json
import codecs
import cPickle as pickle
from optparse import OptionParser
from DataObjects.YelpBusinessData import *
from DataObjects.YelpReviewData import *
from DataObjects.YelpUserData import *

##
parser = OptionParser()
parser.add_option( '--yBusiness', dest='yBusiness', help='yelp_academic_dataset_business.json' )
parser.add_option( '--yReview', dest='yReview', help='yelp_academic_dataset_review.json' )
parser.add_option( '--yUser', dest='yUser', help='yelp_academic_dataset_user.json' )
parser.add_option( '--outFile', dest='outFile', default='yelp_TYPE.p' )
##
(options, args) = parser.parse_args()
YBFILE = options.yBusiness
YRFILE = options.yReview
YUFILE = options.yUser
OUTFILE = options.outFile


'''
Load/Build Business Yelp Dataset Container.
'''
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
  d_businessIds = {}
  print 'Copying Business Ids into a Dictionary'
  for bid in businessContainer.getIds():
    if not d_businessIds.has_key( bid ):
      d_businessIds[ bid ] = 0
    d_businessIds[ bid ] += 1
  print '\t-> get %d business ids' %len(d_businessIds)


'''
Load/Build Review Yelp Dataset Container.
'''
if YRFILE is not None:
  YR_OUTFILE = OUTFILE.replace('TYPE','restaurants_review')
  print 'Generating Review Container (from: %s)' %YRFILE
  reviewContainer = YelpReviewContainer()
  discarded = reviewContainer.load_dataset( YRFILE, business_ids=d_businessIds, verbose=False )
  print '\t-> loaded %d reviews (%d discarded)' %(reviewContainer.len(),discarded)
  ## get stats about categories
  print '\t-> saving review container (to "%s")' %YR_OUTFILE
  pickle.dump( reviewContainer, open( YR_OUTFILE, "wb" ) )
  ##


'''
Load/Build Users Yelp Dataset Container.
'''
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
