"""
Logic to do with "box detection"
(IE enclosed spaces)
"""

import networkx


def strip_edges_at_and_above_weight(g, edge_weight_cutoff):
    """
    :param g: graph
    :param edge_weight_cutoff: remove edges with this weight of higher (lowest unacceptable weight)
    :return: subgraph of g
    """

    for edge_info in g.edges(data=True):
        if edge_info[2]['weight'] >= edge_weight_cutoff:
            g.remove_edge(edge_info[0], edge_info[1])

    return g


def get_box_containing_node(g, node, wall_weight_cutoff):
    """
    :param g: graph of the board
    :param node: node to check
    :param wall_weight_cutoff: node weight to consider "solid"
    :return: subgraph of g that is a box
    """

    edge_induced_subgraph = strip_edges_at_and_above_weight(g, wall_weight_cutoff)
    return networkx.node_connected_component(
        edge_induced_subgraph,
        node
    )


def get_size_of_box_containing_node(g, node, edge_weight_cuttoff):
    print "EDGES:", len(g.edges())
    subgraph = get_box_containing_node(g, node, edge_weight_cuttoff)
    print subgraph
    return len(subgraph)
