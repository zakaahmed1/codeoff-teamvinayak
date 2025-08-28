def calculate_total_travel_cost(locations, capacity):
    """
    Calculate total travel cost for delivering pizzas using greedy approach.
    
    Strategy:
    - Use greedy approach to fill vehicle efficiently
    - Start each trip at depot (0,0)
    - Add locations until capacity is reached
    - Return to depot after each trip
    - Repeat until all locations are delivered
    
    Args:
        locations: List of tuples (x, y, P) where P = number of pizzas
        capacity: Vehicle capacity (C pizzas per trip)
    
    Returns:
        Total travel cost (sum of Manhattan distances)
    """
    
    def manhattan_distance(x1, y1, x2, y2):
        """Calculate Manhattan distance between two points."""
        return abs(x1 - x2) + abs(y1 - y2)
    
    # Copy locations to avoid modifying original list
    remaining_locations = locations.copy()
    total_cost = 0
    depot_x, depot_y = 0, 0
    
    while remaining_locations:
        # Start new trip from depot
        current_capacity = 0
        trip_locations = []
        current_x, current_y = depot_x, depot_y
        
        # Greedy selection: add locations until capacity is reached
        i = 0
        while i < len(remaining_locations):
            x, y, pizzas = remaining_locations[i]
            
            # Check if we can add this location to current trip
            if current_capacity + pizzas <= capacity:
                # Add location to current trip
                trip_locations.append((x, y, pizzas))
                current_capacity += pizzas
                remaining_locations.pop(i)
            else:
                i += 1
        
        # Calculate cost for this trip
        # Travel from depot to first location, then between locations
        if trip_locations:
            # Go from depot to first location
            first_x, first_y, _ = trip_locations[0]
            total_cost += manhattan_distance(current_x, current_y, first_x, first_y)
            current_x, current_y = first_x, first_y
            
            # Travel between locations in the trip
            for i in range(1, len(trip_locations)):
                next_x, next_y, _ = trip_locations[i]
                total_cost += manhattan_distance(current_x, current_y, next_x, next_y)
                current_x, current_y = next_x, next_y
            
            # Return to depot
            total_cost += manhattan_distance(current_x, current_y, depot_x, depot_y)
    
    return total_cost


# Example usage and test
if __name__ == "__main__":
    # Example input: 10 delivery locations (x, y, pizzas)
    example_locations = [
        (1, 2, 3),
        (4, 1, 2),
        (2, 5, 1),
        (6, 3, 4),
        (1, 1, 2),
        (3, 4, 3),
        (5, 2, 1),
        (2, 3, 2),
        (4, 5, 3),
        (6, 1, 2)
    ]
    
    # Vehicle capacity
    vehicle_capacity = 8
    
    # Calculate and output total travel cost
    result = calculate_total_travel_cost(example_locations, vehicle_capacity)
    
    # Output with value, unit, and explanation
    print(f"Total Travel Cost: {result} distance units")
    print(f"\nExplanation: This represents the sum of all Manhattan distances traveled")
    print(f"across multiple delivery trips. The greedy algorithm groups locations")
    print(f"into trips based on vehicle capacity ({vehicle_capacity} pizzas), with each")
    print(f"trip starting and ending at the depot (0,0). The total includes all")
    print(f"movements between locations and return trips to the depot.")