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

sys.path.insert(0, '../../')
from model.YelpBusinessData import *
from model.YelpReviewData import *
from model.YelpUserData import *
##
parser = OptionParser()
parser.add_option( '-c', '--config', dest='configFile', 
  default='../BuonAppetito.conf', help='Path of the configuration file')
##
(options, args) = parser.parse_args()
CONFILE = options.configFile
config = configparser.ConfigParser().read(CONFILE)
YBOFILE = config.get('ProfilesBuilder','YelpBusinessObj')
YROFILE = config.get('ProfilesBuilder','YelpReviewObj')
YUOFILE = config.get('ProfilesBuilder','YelpUserObj')
#
OUTUSRFILE = config.get('ProfilesBuilder','outUserObj')
OUTRSTFILE = config.get('ProfilesBuilder','outRestaurantObj')



''' ------------------------- '''
'''   DEFINE LIWC OBJECT      '''
''' ------------------------- '''
class YelpProfileBuilder:

  def __init__(self):
    self.d_businessIds = {} 

  def load_yelp_data():
    self.load_yelp_business()
    self.load_yelp_reviews()
    self.load_yelp_users()

  '''
  Load/Build Business Yelp Dataset Container. '''
  def load_yelp_business():
    if YBOFILE is not None:
      print 'Loading Business Container (%s)' %YBOFILE
      businessContainer = pickle.load( open( YBOFILE, "rb" ) )
      print '\t-> loaded %d business' %businessContainer.len()
    else:
      print >> sys.stderr, 'Business Container Not Found in %s' %YBFILE
  ##

  '''
  Load/Build Review Yelp Dataset Container. '''
  def load_yelp_reviews():
    if YROFILE is not None:
      print 'Loading Review Container (from: %s)' %YROFILE
      reviewContainer = pickle.load( open( YROFILE, "rb" ) )
      print '\t-> loaded %d reviews' %reviewContainer.len()
    else:
      print >> sys.stderr, 'Review Container Not Found in %s' %YROFILE


  '''
  Load/Build Users Yelp Dataset Container. '''
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
      print >> sys.stderr, 'User Container Not Found in %s' %YUFILE


  '''
  Parse profiles, get the food-words and extract the sentiments. '''