<h2>Gensim Semantic</h2>

This is a collection of methods that help to use right away the word2vector implementation in the Gensim python package.

<h6>Dependences</h6>
The external library [TextProcessingLib](https://github.com/xarabas/TextProcessingLib) is required. Import it in the following way:

```
git submodule add https://github.com/xarabas/TextProcessingLib.git ext/TextProcessingLib
git submodule update --init --recursive
```

------------
<h3>Gensim Statistical Processing</h3>

This code allows the creation of the GensimCore object that is trained on a model optimized for advertising. It is based on different corpus:
* `text8.model`: standard corpus for word2vec
* `ucl-advertising.model`: [UCL Open Advertiser Dataset](https://code.google.com/p/open-advertising-dataset/)
* `models/yahoo-datapack-20150103-1m-kw-adcopy.model`: Yahoo Search Advertisement Dataset based on a month of clicks log.

The extention of the support to additional corpus is very easy. 
However, the models (as well as the corpuses) are not updated in the git repository for space issue, but if you are interested do not exitate to drop me an email.


<h4>Dependences</h4>
* `gensim` python package availanle here: [Gensim -topic modeling for humas](http://radimrehurek.com/gensim) 
