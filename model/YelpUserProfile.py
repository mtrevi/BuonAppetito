# -*- coding: utf-8 -*-
"""
Define the Yelp User Data Objects.
__source__ : http://www.yelp.com/dataset_challenge
__source__ : https://github.com/Yelp/dataset-examples
__author__ : Michele Trevisiol @trevi
__creation__ : Apr 9, 2015
"""

import sys
import json
import codecs
import cPickle as pickle


''' -------------------------- '''
'''   DEFINE BUSINESS OBJECT   '''
''' -------------------------- '''
class YelpUserProfile:

  def __init__(self):
    self.userid = ''
    self.name = ''
    self.review_count = -1
    self.average_stars = -1
    self.votes = -1 # {(vote type): (count)}
    self.friends = [] # [(friend user_ids)]
    self.elite = [] # [(years_elite)]
    self.yelping_since = '' # (date, formatted like '2012-03')
    self.compliments = {} # [compliment_tye]: no_compliemnts, ..
    self.fans = 0
    self.restaurants = {} # business_id : no_visits
    ##
    self.reviews = {}
    ## 
    self.breakfast = {}
    self.launch = {}
    self.dinner = {}
    self.food_emo = {} # food : emo_count
  ##

  '''
  Update Emotions on the given dictionary. '''
  def update_dict_food_emo(self, dictionary, food, emo):
    if not self.dictionary.has_key(food):
      self.dictionary[food] = 0
    self.dictionary[food] += emo['posemo']
    self.dictionary[food] -= emo['negemo']
  ##


  ''' 
  Serialize into a string the entire object. '''
  def serialize2string(self):
    print \
    'name: "%s",'%self.name, 'userid: "%s",'%self.userid, \
    'average_stars: "%d",'%self.average_stars, 'review_count: "%s",'%self.review_count, \
    'votes: "%s",'%str(self.votes), 'friends: "%s",'%self.friends, \
    'elite: "%s",'%str(self.elite), 'yelping_since: "%s",'%self.yelping_since, \
    'compliments: "%s",'%str(self.compliments), 'fans: "%s"'%self.fans 
  ##


  '''
  Load into memory the Yelp User in json format. 
  @input jdata: Yelp User entry in json format '''
  def load_jdata( self, jdata ):
    # parsing data
    self.userid = jdata['user_id']
    self.name = jdata['name']
    self.review_count = jdata['review_count']
    self.average_stars = jdata['average_stars']
    self.votes = jdata['votes']
    self.friends = jdata['friends']
    self.elite = jdata['elite']
    self.yelping_since = jdata['yelping_since']
    self.compliments = jdata['compliments']
    self.fans = jdata['fans']
  ##
##



''' ------------------------- '''
'''   DEFINE USER CONTAINER   '''
''' ------------------------- '''
class YelpUserProfileContainer:

  def __init__(self):
    self.entries = {} 

  def len(self):
    return len(self.entries)
  ##

  def getIds(self):
    return self.entries.keys()
  ##

  def load_dataset(self, filepath, verbose=False):
    if verbose:
      print 'Loading Data from %s' %filepath
    # parsing data
    lines = 0
    total = 366715
    with codecs.open( filepath, 'rU', 'utf-8' ) as f:
      for line in f:
        lines += 1
        # create and load business entry
        uitem = YelpUserProfile()
        try:
          jdata = json.loads( line )
          uitem.load_jdata( jdata )
        except:
          e = sys.exc_info()[0]
          print '[!] ERROR [!] on %s : %s' %(uitem.serialize2string(),e)
        # update dicitonary
        userid = uitem.userid
        self.entries[ userid ] = uitem
        # stats
        if lines %30000 ==0:
          print '\t-> loaded %d reviews (%.2f%s)' %(len(self.entries), float(lines)/total*100, '%')
      #
    # print stats
    if verbose:
      print '\t-> loaded %d Yelp Business entries' %len(self.entries)
  ##
##


