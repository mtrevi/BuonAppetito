import collections

def add_hypernodes(G, recipe_data):
    # Create all nodes in the graph
    for recipe in recipe_data:
        G.add_node(
            recipe['url'],
            recipe)
        G.node[recipe['url']]['type'] = 'hypernode'

def add_hyperedges(G, recipe_data):
    # Create all edges between nodes
    for recipe in recipe_data:
        recipe_url = recipe['url']
        assert G.has_node(recipe_url)
        for ingredient_ids, ingredient_text in zip(recipe.get('ingredient_urls', []), recipe.get('ingredients', [])):
            ingredient_ids = list(set(ingredient_ids))
            if len(ingredient_ids) == 0:
                continue
            hyperedge_sources = [ingredient_ids]
            # If the line only contains one ingredient, just create 1 hyperedge
            if len(ingredient_ids) > 1:
                if ingredient_text.find(' or ') >= 0:
                    # If the line is an 'OR' of ingredient, create one hyperedge
                    pass
                else:
                    # Else, create one hyperedge for each ingredient.
                    hyperedge_sources = map(lambda x : [x], ingredient_ids)
            for hyperedge_source in hyperedge_sources:
                hyperedge_name = 'E(%s)' % ', '.join(hyperedge_source)
                if not G.has_node(hyperedge_name):
                    G.add_node(
                        hyperedge_name,
                        {
                            'sources': hyperedge_source,
                            'targets': []
                        })
                    G.node[hyperedge_name]['type'] = 'hyperedge'
                    # Connect the hyperedge to the source
                    for ingredient_id in hyperedge_source:
                        assert G.has_node(ingredient_id)
                        G.add_edge(ingredient_id, hyperedge_name)
                # Connect to the target
                G.node[hyperedge_name]['targets'].append(recipe_url)
                G.add_edge(hyperedge_name, recipe_url)

def create_ingredient_recipe_list(ingredient_recipe_data):
    # Group together the recipes of the ingredients
    ingredient_recipe_list = collections.defaultdict(set)
    for ingredient_recipe in ingredient_recipe_data:
        # Find the ingredient node
        ingredient_url = ingredient_recipe['ingredient_url']
        recipe_url = ingredient_recipe['recipe_url']
        ingredient_recipe_list[ingredient_url].add(recipe_url)
    return ingredient_recipe_list

def split_pseudo_ingredient_hypernodes(G, ingredient_recipe_list):
    for ingredient_url, recipe_urls in ingredient_recipe_list.iteritems():
    #     print 'Ingredient: %s, recipes: %s' % (ingredient_url, ', '.join(recipe_urls))
        assert G.has_node(ingredient_url)
        assert G.in_degree(ingredient_url) == 0

        # Extract the outgoing and incoming edges
        out_edges = G.out_edges(ingredient_url)
        for recipe_url in recipe_urls:
            assert G.has_node(recipe_url), 'Unable to find node %s' % recipe_url
    #         print 'Ingredient: %s, recipe: %s' % (ingredient_url, recipe_url)
            if 'parent_ingredient_urls' not in G.node[recipe_url]:
                G.node[recipe_url]['parent_ingredient_urls'] = []
            # Annotate the recipe node with the ingredient url
            G.node[recipe_url]['parent_ingredient_urls'].append(ingredient_url)

            if len(G.node[recipe_url]['parent_ingredient_urls']) > 1:
                print 'Warning: recipe %s is shared (%s) ' % (recipe_url, ', '.join(G.node[recipe_url]['parent_ingredient_urls'])) 

            # Connect outgoing nodes
            for _, hyperedge in out_edges:
                G.add_edge(recipe_url, hyperedge)
        # Remove the ingredient node
        G.remove_node(ingredient_url)

def get_graph_levels(G):
    G = G.copy()
    prev_number_of_nodes = None
    number_of_nodes = G.number_of_nodes()
    while number_of_nodes > 0 and prev_number_of_nodes != number_of_nodes:
        level = []
        for x in G.nodes():
            if G.in_degree(x) == 0:
                level.append(x)
        yield level
        G.remove_nodes_from(level)
        # Remove also hyperedge nodes
        for y in G.nodes():
            if G.in_degree(y) == 0 and G.node[y]['type'] == 'hyperedge':
                G.remove_node(y)
        
        prev_number_of_nodes = number_of_nodes
        number_of_nodes = G.number_of_nodes()

def ingredienticity(G):
    number_of_nodes_above_cache = {}
    ret = {}
    def ingredienticity_helper(G, number_of_nodes_below, x):
        '''
        Computes the ingredienticity of the node and 
        returns the number of nodes above the node.
        '''
        if x in number_of_nodes_above_cache:
            return number_of_nodes_above_cache[x]
        number_of_nodes_above = 0.0
        for _, y in G.out_edges(x):
            for _, z in G.out_edges(y):
                number_of_nodes_above += ingredienticity_helper(G, number_of_nodes_below + 1, z)
        number_of_nodes_above_cache[x] = number_of_nodes_above
        ret[x] = 1 - number_of_nodes_below / max(1, (number_of_nodes_below + number_of_nodes_above))
        return number_of_nodes_above + 1
    for x in G.nodes():
        if len(G.in_edges(x)) == 0:
            ingredienticity_helper(G, 0.0, x)
    return ret

def remove_simple_hyperedges(G):
    # Removes hyperedges with one source and one target
    for x, d in G.nodes(data=True):
        if d['type'] == 'hyperedge':
            in_edges = G.in_edges(x)
            out_edges = G.out_edges(x)
            assert len(in_edges) > 0
            assert len(out_edges) > 0
            if len(in_edges) == 1 and len(out_edges) == 1:
                # Remove hyperedge
                G.add_edge(in_edges[0][0], out_edges[0][1], {'type': 'hyperedge'})
                G.remove_node(x)