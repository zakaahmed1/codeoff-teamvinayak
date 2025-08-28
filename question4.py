from datetime import datetime, timedelta
import itertools

def parse_time(time_str):
    """Parse time string (HH:MM) to datetime object."""
    return datetime.strptime(time_str, "%H:%M")

def time_to_minutes(time_obj):
    """Convert time to minutes since midnight."""
    return time_obj.hour * 60 + time_obj.minute

def minutes_to_time_str(minutes):
    """Convert minutes since midnight to HH:MM format."""
    hours = (minutes // 60) % 24
    mins = minutes % 60
    return f"{hours:02d}:{mins:02d}"

def manhattan_distance(x1, y1, x2, y2):
    """Calculate Manhattan distance between two points."""
    return abs(x1 - x2) + abs(y1 - y2)

def get_time_multiplier(x, y, departure_minutes):
    """
    Calculate time-dependent multiplier based on destination and departure time.
    
    Args:
        x, y: destination coordinates
        departure_minutes: departure time in minutes since midnight
    
    Returns:
        multiplier: float value to multiply base cost
    """
    multiplier = 1.0
    
    # Convert to hours for easier comparison
    departure_hour = departure_minutes / 60
    
    # rush_east: if x > 0 and departure is between 17:00–19:00 → multiply by 2.0
    if x > 0 and 17.0 <= departure_hour < 19.0:
        multiplier *= 2.0
    
    # evening_north: if y > 10 and departure is between 16:00–18:00 → multiply by 1.5
    if y > 10 and 16.0 <= departure_hour < 18.0:
        multiplier *= 1.5
    
    return multiplier

def calculate_route_cost(route, start_time_minutes):
    """
    Calculate total cost for a given route with time-dependent multipliers.
    
    Args:
        route: list of (x, y, pizzas) tuples representing the route
        start_time_minutes: start time in minutes since midnight
    
    Returns:
        tuple: (total_cost, route_details)
    """
    current_time = start_time_minutes
    current_x, current_y = 0, 0  # Start at depot
    total_cost = 0
    route_details = []
    
    # Visit each location in the route
    for i, (x, y, pizzas) in enumerate(route):
        # Calculate base travel time (Manhattan distance)
        base_time = manhattan_distance(current_x, current_y, x, y)
        
        # Get time-dependent multiplier
        multiplier = get_time_multiplier(x, y, current_time)
        
        # Calculate leg cost
        leg_cost = base_time * multiplier
        total_cost += leg_cost
        
        # Record leg details
        route_details.append({
            'from': (current_x, current_y),
            'to': (x, y),
            'departure_time': minutes_to_time_str(current_time),
            'base_distance': base_time,
            'multiplier': multiplier,
            'leg_cost': leg_cost
        })
        
        # Update current position and time
        current_x, current_y = x, y
        current_time += base_time
    
    # Return to depot
    base_time = manhattan_distance(current_x, current_y, 0, 0)
    multiplier = get_time_multiplier(0, 0, current_time)
    leg_cost = base_time * multiplier
    total_cost += leg_cost
    
    route_details.append({
        'from': (current_x, current_y),
        'to': (0, 0),
        'departure_time': minutes_to_time_str(current_time),
        'base_distance': base_time,
        'multiplier': multiplier,
        'leg_cost': leg_cost
    })
    
    return total_cost, route_details

def find_optimal_route(locations, start_time_str):
    """
    Find the optimal route that minimizes total time-dependent travel cost.
    
    Uses a greedy nearest-neighbor approach with time-dependent cost consideration.
    
    Args:
        locations: list of (x, y, pizzas) tuples
        start_time_str: start time in HH:MM format
    
    Returns:
        tuple: (best_route, best_cost, best_details)
    """
    start_time_minutes = time_to_minutes(parse_time(start_time_str))
    
    # For small problem size (10 locations), we can try multiple approaches
    # Here we'll use a greedy approach with some optimization
    
    best_cost = float('inf')
    best_route = None
    best_details = None
    
    # Try different starting locations to find better routes
    for start_idx in range(len(locations)):
        remaining = locations.copy()
        current_route = [remaining.pop(start_idx)]
        current_x, current_y = current_route[0][0], current_route[0][1]
        current_time = start_time_minutes
        
        # Greedy selection for remaining locations
        while remaining:
            best_next_idx = 0
            best_next_cost = float('inf')
            
            for i, (x, y, pizzas) in enumerate(remaining):
                base_time = manhattan_distance(current_x, current_y, x, y)
                multiplier = get_time_multiplier(x, y, current_time)
                cost = base_time * multiplier
                
                if cost < best_next_cost:
                    best_next_cost = cost
                    best_next_idx = i
            
            # Add best next location
            next_location = remaining.pop(best_next_idx)
            current_route.append(next_location)
            
            # Update position and time
            base_time = manhattan_distance(current_x, current_y, next_location[0], next_location[1])
            current_x, current_y = next_location[0], next_location[1]
            current_time += base_time
        
        # Calculate total cost for this route
        total_cost, route_details = calculate_route_cost(current_route, start_time_minutes)
        
        if total_cost < best_cost:
            best_cost = total_cost
            best_route = current_route
            best_details = route_details
    
    return best_route, best_cost, best_details

def solve_time_dependent_delivery(locations, start_time_str):
    """
    Main function to solve the time-dependent delivery problem.
    
    Args:
        locations: list of (x, y, pizzas) tuples
        start_time_str: start time in HH:MM format
    
    Returns:
        dict: solution with route, costs, and details
    """
    print(f"\n=== Time-Dependent Travel Cost Optimization ===")
    print(f"Start time: {start_time_str}")
    print(f"Number of locations: {len(locations)}")
    print(f"Locations: {locations}")
    
    # Find optimal route
    best_route, best_cost, route_details = find_optimal_route(locations, start_time_str)
    
    print(f"\n=== Optimal Route ===")
    print(f"Route: Depot → ", end="")
    for i, (x, y, pizzas) in enumerate(best_route):
        print(f"({x},{y})", end="")
        if i < len(best_route) - 1:
            print(" → ", end="")
    print(" → Depot")
    
    print(f"\n=== Route Details ===")
    for i, leg in enumerate(route_details):
        print(f"Leg {i+1}: {leg['from']} → {leg['to']}")
        print(f"  Departure time: {leg['departure_time']}")
        print(f"  Base distance: {leg['base_distance']} minutes")
        print(f"  Time multiplier: {leg['multiplier']:.1f}")
        print(f"  Leg cost: {leg['leg_cost']:.1f} minutes")
        print()
    
    print(f"=== Summary ===")
    print(f"Total time-dependent travel cost: {best_cost:.1f} minutes")
    print(f"\nExplanation: This cost represents the total travel time including")
    print(f"time-dependent multipliers for rush hour traffic (eastbound 17:00-19:00)")
    print(f"and evening congestion (northbound y>10, 16:00-18:00). The route was")
    print(f"optimized using a greedy nearest-neighbor approach considering these")
    print(f"time-dependent factors.")
    
    return {
        'route': best_route,
        'total_cost': best_cost,
        'route_details': route_details,
        'start_time': start_time_str
    }

# Example usage and test
if __name__ == "__main__":
    # Example input: 10 delivery locations (x, y, pizzas)
    example_locations = [
        (2, 15, 3),   # North location (y > 10)
        (5, 8, 2),    # East location
        (-1, 12, 1),  # West-North location
        (8, 5, 4),    # East location
        (1, 3, 2),    # East location
        (-2, 6, 3),   # West location
        (6, 14, 1),   # East-North location (both multipliers possible)
        (3, 2, 2),    # East location
        (-3, 11, 3),  # West-North location
        (4, 16, 2)    # East-North location (both multipliers possible)
    ]
    
    # Start time during potential rush hour
    start_time = "16:30"
    
    # Solve the problem
    solution = solve_time_dependent_delivery(example_locations, start_time)