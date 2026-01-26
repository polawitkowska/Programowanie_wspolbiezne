points = {0: (1, 3), 1: (3, 1), 2: (3, 5), 3: (5, 1), 4: (5, 5), 5: (7, 3)}
# possible edges are (i, j) where i < j and i, j ∈ points

all_edges = set()

edges = {
    'R': set(),
    'B': set()
}

def is_edge_possible(edge):
    a, b = edge
    valid_points = range(6)

    if a == b:
        return False
    if a not in valid_points or b not in valid_points:
        return False
    if edge in all_edges:
        return False
    
    return True

def is_triangle(player, edge):
    a, b = edge
    for c in range(6):
        if c == a or c == b:
            continue

        edge_ac = tuple(sorted((a, c)))
        edge_cb = tuple(sorted((b, c)))

        if edge_ac in edges[player] and edge_cb in edges[player]:
            return True

    return False

def make_move(player, a, b):
    new_edge = tuple(sorted((a, b)))

    if not is_edge_possible(new_edge):
        return "Illegal move"

    edges[player].add(new_edge) # edge (1, 3) should be the same as (3, 1)
    all_edges.add(new_edge)

    if is_triangle(player, new_edge):
        return "Game ended"
    
    return "Move done"