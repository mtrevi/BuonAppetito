# -*- coding: utf-8 -*-
"""
Define the Yelp Review Data Objects.
__source__ : http://www.yelp.com/dataset_challenge
__source__ : https://github.com/Yelp/dataset-examples
__author__ : Michele Trevisiol @trevi
"""

import sys
import json
import codecs
import cPickle as pickle


''' -------------------------- '''
'''   DEFINE BUSINESS OBJECT   '''
''' -------------------------- '''
class YelpReview:

  def __init__(self):
    self.busid = ''           # encrypted business id
    self.userid = ''          # encrypted user id
    self.stars = -1           # star rating, rounded to half-stars
    self.text = ''            # review text
    self.date = '0000-00-00'  # date, formatted like '2012-03-14'
    self.votes = -1           # {(vote type): (count)}
  ##

  ''' 
  Serialize into a string the entire object. '''
  def serialize2string(self):
    print \
    'busid: "%s",'%self.busid, 'userid: "%s",'%self.userid, \
    'stars: "%d",'%self.stars, 'date: "%s",'%self.date, \
    'votes: "%s",'%str(self.votes), 'text: "%s",'%self.text
  ##


  '''
  Load into memory the Yelp Review in json format. 
  @input jdata: Yelp Review entry in json format '''
  def load_jdata( self, jdata ):
    # parsing data
    self.busid = jdata['business_id']
    self.userid = jdata['user_id']
    self.stars = jdata['stars']
    self.text = jdata['text']
    self.date = jdata['date']
    self.votes = jdata['votes']
  ##
##



''' --------------------------- '''
'''   DEFINE REVIEW CONTAINER   '''
''' --------------------------- '''
class YelpReviewContainer:

  def __init__(self):
    self.entries = [] 

  def len(self):
    return len(self.entries)
  ##

  def getIds(self):
    return self.entries.values()
  ##

  def load_dataset(self, filepath, business_ids=[], verbose=False):
    if verbose:
      print 'Loading Data from %s' %filepath
    # parsing data
    discarded = 0
    lines = 0
    total = 1569264
    with codecs.open( filepath, 'rU', 'utf-8' ) as f:
      for line in f:
        save = True
        lines += 1
        # create and load business entry
        ritem = YelpReview()
        try:
          jdata = json.loads( line )
          ritem.load_jdata( jdata )
          # skip if it does not belong to any given categories
          if len(business_ids) > 0:
            save = False
            if business_ids.has_key( ritem.busid ):
              save = True
        except:
          e = sys.exc_info()[0]
          print '[!] ERROR [!] on %s : %s' %(ritem.serialize2string(),e)
        # update dicitonary
        if save:
          self.entries.append( ritem )
        else:
          discarded += 1
        # stats
        if lines %100000 ==0:
          print '\t-> loaded %d reviews (%.2f%s)' %(len(self.entries), float(lines)/total*100, '%')
      #
    # print stats
    if verbose:
      print '\t-> loaded %d Yelp Business entries' %len(self.entries)
    #
    return discarded
  ##

  def getStatsType(self):
    types = {}
    for bitem in self.entries.values():
      # get type
      for c in bitem.categories:
        if not types.has_key( c ):
          types[ c ] = 0
        types[ c ] += 1
    return types
  ##

  # def ComputeSentenceSentiment(self):
  #   ...
  ##
##




  # ''' ------------------------ '''
  # '''   DEFINE REVIEW OBJECT   '''
  # ''' ------------------------ '''
  # class YelpReview:

  #  def __init__(self):
  #     self.id = ''            # encrypted business id
  #     self.name = ''          # business name
  #     self.neighborhoods = [] # hood names
  #     self.full_address = ''  # localized address
  #     self.city = ''          # city
  #     self.state = ''         # state
  #     self.latitude = -1      # latitude
  #     self.longitude = -1     # longitude
  #     self.stars = -1         # star rating, rounded to half-stars
  #     self.review_count = -1  # review count
  #     self.categories = ''    # (localized category names
  #     self.hours = {}         # day_of_week: {'open':(HH:MM), 'close':(HH:MM)}
  #     self.attributes = {}    # attributes (not often available)


  #     ''' Serialize into string the object. '''
  #     def serialize():
  #       print 'id: %s,'%str(self.id), 'name: %s,'%str(self.na)me, \
  #       'neighborhoods: %s,'%str(self.neighborhoods), 'full_address: %s,'%str(self.full_address), \
  #       'city: %s,'%str(self.city), 'state: %s,'%str(self.state), 'latitude: %s,'%str(self.latitude), \
  #       'longitude: %s,'%str(self.longitude), 'stars: %s,'%str(self.stars), \
  #       'review_count: %s,'%str(self.review_count), 'categories: %s,'%str(self.categories), \
  #       'hours: %s,'%str(self.hours), 'attributes: %s' %str(self.attributes)


  #       '''
  #       Load into memory the Yelp Accademid Dataset Business. 
  #       @input filepath:
  #       @param language: if given, filter out entries of any different language
  #       '''
  #       def load_business( self, filepath, language=None ):
  #         with codecs.open( filepath, 'rU', 'utf-8' ) as f:
  #           for line in f:
  #             try:
  #               jdata = json.loads( line )
  #               self.id = jdata['business_id']
  #               self.name = jdata['name']
  #               self.neighborhoods = jdata['neighborhoods']
  #               self.full_address = jdata['full_address']
  #               self.city = jdata['city']
  #               self.state = jdata['state']
  #               self.latitude = jdata['latitude']
  #               self.longitude = jdata['longitude']
  #               self.starts = jdata['stars']
  #               self.review_count = jdata['review_count']
  #               self.categories = jdata['categories']
  #               self.hours = jdata['stars']
  #               self.attributes = jdata['attributes']
  #             except:
  #               print '[!] ERROR on %s' %self.serialize()
  #               }