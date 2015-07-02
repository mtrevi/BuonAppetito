<h2>Graph approach</h2>

This module computes the graph of ingredients. The output is a Hypergraph in which recipes 
are hypernodes and hyperedges represent alternatives.

The code representation of the hypergraph is a directed graph in which
hypernodes and hyperedges are represented as nodes of different
'type'.
Note the distinction between hypernodes (hyperedges) belonging to the 
"conceptual" hypergraph, and nodes (edges) belonging to the code
representation.

Each node has the following attributes:
   - description: the description of the recipe
   - [image]: the URL of the image
   - ingredient_urls: the list of lists of urls of the ingredients. Each list represents alternatives of ingredients.
   - ingredients: the text of the ingredient lines in the HTML page
   - item_type [RecipeItem, IngredientItem, IngredientRecipeItem]': as in src/bbc_food_scraper/bbc_ingredients/spiders
   - name: the title of the recipe
   - parent_ingredient_urls: some ingredients of dishes in BBC Food have many recipes. E.g., pesto is an ingredient but
     has also many alternative recipes. This fields collects all ingredients that have this node as a recipe
   - preparation: the text of the preparation of the dish, as in the HTML page
   - type' [hypernode, hyperedge]: the conceptual type of the node
   - url: the URL to the ingredient page on BBC Food.


<h6>Common Functions</h6>
The output file is a gpickle file containing the complete graph.
It can be parsed using the networkx.read_gpickle() method.