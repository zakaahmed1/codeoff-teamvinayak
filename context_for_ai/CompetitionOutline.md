

GCO Aug 2025 Challenge
Hi, Niall. When you submit this form, the owner will see your name and email address.
1
Optimal Pizza Delivery 

You are operating a pizza delivery vehicle that starts at a central depot located at coordinates (0,0). Your task is to plan delivery routes to visit multiple locations while optimizing travel under different constraints. The cost of travel between any two points (x1, y1) and (x2, y2) is calculated using 

Manhattan distance:

distance=∣x1−x2∣+∣y1−y2∣ 

The vehicle must visit all delivery locations and may need to return to the depot depending on constraints. 

Base Problem Goal: 
Find the minimum possible total travel cost to deliver all pizzas and return to the depot. 

Input: A list of N = 10 locations, each represented as a tuple (x, y, P), where x and y are coordinates, and P is the number of pizzas to deliver. 

Sample Input: (5, -10, 3) (-12, 8, 5) (15, 20, 2) (-8, -15, 7) (25, -5, 4) (-20, 18, 6) (10, 30, 1) (-30, -22, 8) (18, 14, 2) (-7, 28, 5)
Output: Minimum total travel cost (sum of Manhattan distances) for visiting all locations and returning to the depot.
Enter your answer
2
Capacity-Constrained Delivery 
 
 The delivery vehicle has a maximum carrying capacity C pizzas per trip. 
 
 It can make multiple trips to the depot if needed. 
 
 Goal: Minimize the total travel cost across all trips. 
 
 Example Input: 
 
 Capacity: C = 10 pizzas 
 
 Locations: same as above 
 
 Example Output: 
 
 Number of trips and which locations are visited per trip. 
 
 Total travel cost for all trips combined. 
 
Enter your answer
3
 Time-Window Delivery 
 
 Each location now has a time window (start_time, end_time) in which pizzas must be delivered. 
 
 Travel time is equal to Manhattan distance (1 minute per unit). 
 
 Goal: Find a feasible route visiting all locations within their time windows and returning to the depot.

Output: 
 
 Route visiting all locations respecting time windows. 
 
 Arrival times at each location. 
 
 Total travel cost.

Sample Input:


Enter your answer
4
Time-Dependent Travel Costs 
 
 Travel cost between two points depends on departure time from the starting location. 
 
 Example rules: 
 
 rush_east: if x > 0 and departure is between 17:00–19:00 → multiply leg cost by 2.0. 
 
 evening_north: if y > 10 and departure is between 16:00–18:00 → multiply leg cost by 1.5. 
 
 
 
 Goal: Find a route that minimizes total time-dependent cost. 
 
 Sample Input: 
 
 Start time: 16:30 
 
 Locations: same as above 
 
 Multipliers: as described 
 
 Output: 
 
 Route visiting all locations. 
 
 Departure times, applied multiplier, and cost for each leg. 
 
 Total time-dependent travel cost.
Enter your answer
5
Team Name
Enter your answer
6
Git url

