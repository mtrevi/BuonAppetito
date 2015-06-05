<h2>Food-Words Recognition</h2>

This module contains functions that detect and recognize food-words within a given piece of text (e.g., sentence, entire review). 


<h6>Common Functions</h6>
The Food-Words Recognition module interacts with different modules that manage the Food DB previously cralwed. However these are the common function that this module contains. Note that these functions will be called by the Profiles Builder module.

```
def get_food_items( text, method ):
    @input text: 
        receives a string (might be a sentence or a group of sentences)
    @input method:
        receives a string (or integer) of the methods requested for the food identification
        (e.g., 'graph', 'trie', 'w2v')
    @output list(food_items): 
        returns a list of food_items 
```

A food_item is an object that contains (at least):
```
* food_id: numerical id
* food_name: string name
* type: type of the item (i.e., ingredient or dish)
```
