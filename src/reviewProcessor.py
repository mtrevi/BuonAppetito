# -*- coding: utf-8 -*-
"""
Parse the review with text processing, get sentences 
and infer positive and negative emotions with EmotionsLIWClib
__source__ : 
__author__ : Michele Trevisiol @trevi
__creation__ : Apr 8, 2015
"""

import json
from optparse import OptionParser
from ConfigParser import SafeConfigParser
from nltk import pos_tag, ne_chunk

##
parser = OptionParser()
parser.add_option( '--config', dest='configFile', 
  default='../BuonAppetito.conf', help='Path of the configuration file')
##
(options, args) = parser.parse_args()
CONFILE = options.configFile
config = SafeConfigParser()
config.read(CONFILE)
YBFILE = config.get('DataProcessing', 'YelpBusiness')
YRFILE = config.get('DataProcessing', 'YelpReview')
YUFILE = config.get('DataProcessing', 'YelpUser')
OUTFILE = config.get('DataProcessing', 'outFile')


'''
Create and train the EmotionLIWC
'''
myLIWC = LIWCObj()
myLIWC.build_model( 'ext/LIWClib/dictionary/LIWC2007_English100131.dic' )



'''
Load Business, Review and User processed data
'''
print >> sys.stderr, 'Loading Business Container (%s)' %YBFILE
businessContainer = pickle.load( open( YBFILE, "rb" ) )
print >> sys.stderr, '\t-> loaded %d business' %businessContainer.len()
#
print >> sys.stderr, 'Loading Review Container (%s)' %YRFILE
reviewContainer = pickle.load( open( YRFILE, "rb" ) )
print >> sys.stderr, '\t-> loaded %d reviews' %reviewContainer.len()
#
print >> sys.stderr, 'Loading User Container (%s)' %YUFILE
userContainer = pickle.load( open( YUFILE, "rb" ) )
print >> sys.stderr, '\t-> loaded %d users' %userContainer.len()


'''
Parse Food Names and Description and build FoodTrie
'''
print >> sys.stderr, 'Loading Food Trie (%s)' %FOODTRIEFILE
trie = json.load(open('data/food_dataset/bbc_menupages-trie.json'))
trie_finder = TrieFinder(trie)
print >> sys.stderr, '\t-> done'



'''
Parse Review Objects searching for food items
'''
print >> sys.stderr, 'Searching food-items in reviews'
rev_no_text = 0
food_sentences = 0
updated_user_profile = 0
lines = 0
for revObj in reviewContainer.entries:
  rev = revObj.text
  if len(rev.split(' ')) < 3:
    rev_no_text += 1
    print >> sys.stderr, "no text"
    continue
  lines += 1
  userid = revObj.userid
  ## splint in sentences, then in words
  for sent in tokenize2sentences2words( rev ):
    l_words = remove_stopwords( sent )
    ## select only nouns from l_words
    l_nouns = filter_POS_type( l_words, 'NN' )
    ## match using trie
    nouns_food_tmp = trie_finder.find( l_words )
    ## clean
    nouns_food = []
    for nf in nouns_food_tmp:
      if len(filter_POS_type(nf, 'NN')) > 0:
        nouns_food.append(nf)
    ## found food items with at least a noun
    if len(nouns_food) > 0:
      food_sentences += 1
      emot = myLIWC.getCategoriesFromText(' '.join(sent))
      if emot['posemo'] != emot['negemo']:
        ## update user profile
        if userContainer.entries.has_key(userid):
          for nf in nouns_food:
            userContainer.entries[userid].update_food_emo(nf, emot)
            updated_user_profile += 1
      ##
    ##
  ##
  if lines % 600 == 0:
    print >> sys.stderr, '\t-> parsed %.2f reviews, found %s tot_food_sentences (%d updated_user_profile, %d rev_no_text)' \
    %((lines/reviewContainer.len()*100), food_sentences, updated_user_profile, rev_no_text)
##
print >> sys.stderr, '\t-> parsed %.2f reviews, found %s tot_food_sentences (%d updated_user_profile, %d rev_no_text)' \
%((lines/reviewContainer.len()*100), food_sentences, updated_user_profile, rev_no_text)


## get stats about categories
YU_OUTFILE = YUFILE.replace('.p','.profile.p')
print '\t-> saving user-profile container (to "%s")' %YU_OUTFILE
pickle.dump( userContainer, open( YU_OUTFILE, "wb" ) )