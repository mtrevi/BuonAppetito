# -*- coding: utf-8 -*-
"""
Define the Yelp Business Data Objects.
__source__ : http://www.yelp.com/dataset_challenge
__source__ : https://github.com/Yelp/dataset-examples
__author__ : Michele Trevisiol @trevi
"""

import json
import codecs
import cPickle as pickle


''' -------------------------- '''
'''   DEFINE BUSINESS OBJECT   '''
''' -------------------------- '''
class YelpBusiness:

  def __init__(self):
    self.id = ''            # encrypted business id
    self.name = ''          # business name
    self.neighborhoods = [] # hood names
    self.full_address = ''  # localized address
    self.city = ''          # city
    self.state = ''         # state
    self.latitude = -1      # latitude
    self.longitude = -1     # longitude
    self.stars = -1         # star rating, rounded to half-stars
    self.review_count = -1  # review count
    self.categories = []    # (localized category names
    self.hours = {}         # day_of_week: {'open':(HH:MM), 'close':(HH:MM)}
    self.attributes = {}    # attributes (not often available)
  ##


  ''' 
  Serialize into a string the entire object. '''
  def serialize2string(self):
    print 'id: "%s",'%str(self.id), 'name: "%s",'%str(self.name), \
    'neighborhoods: "%s",'%str(self.neighborhoods), 'full_address: "%s",'%str(self.full_address), \
    'city: "%s",'%str(self.city), 'state: "%s",'%str(self.state), 'latitude: "%s",'%str(self.latitude), \
    'longitude: "%s",'%str(self.longitude), 'stars: "%s",'%str(self.stars), \
    'review_count: "%s",'%str(self.review_count), 'categories: "%s",'%str(self.categories), \
    'hours: "%s",'%str(self.hours), 'attributes: "%s"' %str(self.attributes)
  ##


  '''
  Load into memory the Yelp Business in json format. 
  @input jdata: Yelp Business entry in json format '''
  def load_jdata( self, jdata ):
    # parsing data
    self.id = jdata['business_id']
    self.name = jdata['name']
    self.neighborhoods = jdata['neighborhoods']
    self.full_address = jdata['full_address'].replace('\n',',')
    self.city = jdata['city']
    self.state = jdata['state']
    self.latitude = jdata['latitude']
    self.longitude = jdata['longitude']
    self.stars = jdata['stars']
    self.review_count = jdata['review_count']
    self.categories = jdata['categories']
    self.hours = jdata['hours']
    self.attributes = jdata['attributes']
  ##

  def get_type( self ):
    return self.categories[-1]
  ##




''' ----------------------------- '''
'''   DEFINE BUSINESS CONTAINER   '''
''' ----------------------------- '''
class YelpBusinessContainer:

  def __init__(self):
    self.entries = {} # diz{business_id} -> YelpBusiness

  def len(self):
    return len(self.entries)
  ##

  def getIds(self):
    return self.entries.keys()
  ##

  def load_dataset(self, filepath, categories=[], verbose=False):
    if verbose:
      print 'Loading Data from %s' %filepath
    # parsing data
    with codecs.open( filepath, 'rU', 'utf-8' ) as f:
      for line in f:
        save = True
        # create and load business entry
        bitem = YelpBusiness()
        try:
          jdata = json.loads( line )
          bitem.load_jdata( jdata )
          # skip if it does not belong to any given categories
          if len(categories) > 0:
            save = False
            bCat = [bc.lower() for bc in bitem.categories]
            categories = [c.lower() for c in categories]
            for c in categories:
              for bc in bCat:
                if c in bc:
                  save = True
        except:
          print '[!] ERROR [!] on %s' %bitem.serialize()
        # update dicitonary
        if save:
          if not self.entries.has_key( bitem.id ):
            self.entries[ bitem.id ] = bitem
          else:
            print '[!] ERROR [!] duplicate element with id %d' %bitem.id
      #
    # print stats
    if verbose:
      print '\t-> loaded %d Yelp Business entries' %len(self.entries)
    #
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