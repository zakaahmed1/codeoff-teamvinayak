#import the library to be useful in permutations for calculating
import itertools

# Manhattan distance function based on the question
def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

# Delivery locations (x, y, P) — P is ignored for cost calculation from this
locations = [
    (5, -10, 3), (-12, 8, 5), (15, 20, 2), (-8, -15, 7), (25, -5, 4),
    (-20, 18, 6), (10, 30, 1), (-30, -22, 8), (18, 14, 2), (-7, 28, 5)
]

# Extract coordinates only
coords = [(x, y) for x, y, _ in locations]
depot = (0, 0)

# Initialize minimum cost and best route variable
min_cost = float('inf')
best_route = None

# Try all permutations of delivery locations
for perm in itertools.permutations(coords):
    cost = manhattan(depot, perm[0])  # Start from depot
    for i in range(len(perm) - 1):
        cost += manhattan(perm[i], perm[i + 1])  # Between locations
    cost += manhattan(perm[-1], depot)  # Return to depot

    if cost < min_cost:
        min_cost = cost
        best_route = perm

# Output result
print("Minimum total travel cost:", min_cost)
print("Best route:")
print([depot] + list(best_route) + [depot])