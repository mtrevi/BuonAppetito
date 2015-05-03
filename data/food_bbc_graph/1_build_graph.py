
# coding: utf-8

# In[1]:

import networkx
import json
import collections
from bbc_graph import *


# In[2]:

# Load data from the scrape
# data = json.load(open('../bbc_ingredients/bbc_ingredients.2.json', 'r'));
data = json.load(open('../bbc_ingredients/bbc_ingredients.20150426_1328.json', 'r'));


# In[3]:

ingredient_recipe_data = []
recipe_data = []

for element in data:
    if element['item_type'] == 'IngredientRecipeItem':
        ingredient_recipe_data.append(element)
    else:
        recipe_data.append(element)


# In[4]:

G = networkx.DiGraph()
add_hypernodes(G, recipe_data)
print 'Nodes: %d, edges: %d' % (G.number_of_nodes(), G.number_of_edges())
add_hyperedges(G, recipe_data)
print 'Nodes: %d, edges: %d' % (G.number_of_nodes(), G.number_of_edges())
# Save check. The graph should be acyclic
assert len(list(networkx.algorithms.cycles.simple_cycles(G))) == 0


# In[5]:

# Split the pseudo-ingredient hypernodes
G_ingredient_split = G.copy()
ingredient_recipe_list = create_ingredient_recipe_list(ingredient_recipe_data)
split_pseudo_ingredient_hypernodes(G_ingredient_split, ingredient_recipe_list)
print 'Nodes: %d, edges: %d' % (G_ingredient_split.number_of_nodes(), G_ingredient_split.number_of_edges())


# In[6]:

# Now detect the cycles and remove them
parent_ingredient_urls_in_cycles = set()
for cycle in networkx.algorithms.cycles.simple_cycles(G_ingredient_split):
    for x in cycle:
        if G_ingredient_split.node[x]['type'] == 'hypernode':
            parent_ingredient_urls_in_cycles.update(set(G_ingredient_split.node[x]['parent_ingredient_urls']))
print 'Found %d ingredients generating cycles' % len(parent_ingredient_urls_in_cycles)


# In[7]:

# Filter out ingredients creating cycles
ingredient_recipe_list_without_cycles = {}
for x in ingredient_recipe_list:
    if x not in parent_ingredient_urls_in_cycles:
        ingredient_recipe_list_without_cycles[x] = ingredient_recipe_list[x]

# Split the pseudo-ingredient hypernodes
G_ingredient_split_without_cycles = G.copy()
split_pseudo_ingredient_hypernodes(G_ingredient_split_without_cycles, ingredient_recipe_list_without_cycles)
print 'Nodes: %d, edges: %d' % (G_ingredient_split_without_cycles.number_of_nodes(), G_ingredient_split_without_cycles.number_of_edges())
assert len(list(networkx.algorithms.cycles.simple_cycles(G_ingredient_split_without_cycles))) == 0


# In[19]:

graph_levels = list(get_graph_levels(G_ingredient_split_without_cycles))
graph_level_counts = map(len, graph_levels)
print 'Graph level cardinalities', graph_level_counts


# In[18]:

networkx.write_gpickle(G_ingredient_split_without_cycles, 'bbc_graph.graphml')

