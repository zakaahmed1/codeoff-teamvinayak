import math

# function to compute Manhattan distance between two points
def manhattan(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])


# convert "HH:MM" to minutes since 09:00 to allow us to use sample input directly
def hhmm_to_minutes_since_9am(hhmm):
    h, m = map(int, hhmm.split(":"))
    return (h - 9) * 60 + m

def minutes_since_9am_to_hhmm(m):
    total = 9*60 + m
    h, mm = divmod(total, 60)
    return f"{h:02d}:{mm:02d}"

def min_distance(points):
    """
    Use greedy algorithm to find a short route visiting all points and returning to origin.:
    - choose next stop that minimizes effective arrival time (max(t+travel, start)),
      tie-break by travel distance. Waiting is allowed.
    points: [(label, x, y, start_hhmm, end_hhmm), ...]
    """
    origin = (0, 0)
    labels  = [p[0] for p in points] # extract labels
    coords  = [(p[1], p[2]) for p in points] # extract coordinates
    windows = [(hhmm_to_minutes_since_9am(p[3]), hhmm_to_minutes_since_9am(p[4])) for p in points] # extract time windows

    # Initialise variables such as current position, time, total distance, and unvisited points
    n = len(points)
    unvisited = set(range(n))
    cur = origin
    t = 0
    total_dist = 0
    route = [("Depot", origin)]
    arrivals = ["09:00"]

    # Main greedy loop that goes through all points while calling the manhattan function to calculate distances and
    # using the time window constraints to determine the next best point to visit
    while unvisited:
        best = None
        best_key = (math.inf, math.inf)  # (effective_arrival, travel)
        for j in unvisited:
            travel = manhattan(cur, coords[j])
            eff_arrival = t + travel
            s, e = windows[j]
            if eff_arrival < s:
                eff_arrival = s  # wait
            if eff_arrival <= e:  # feasible now
                key = (eff_arrival, travel)
                if key < best_key:
                    best_key = key
                    best = j

        if best is None:
            # This is in case no feasible next stop is found, i.e. we cannot get to the next stop within its time window
            print("No feasible customer left. Remaining stops:")
            for j in sorted(unvisited):
                travel = manhattan(cur, coords[j])
                s, e = windows[j]
                earliest = max(t + travel, s)
                print(f"  {labels[j]} {coords[j]} window[{minutes_since_9am_to_hhmm(s)}–{minutes_since_9am_to_hhmm(e)}], "
                      f"arrive-if-next={minutes_since_9am_to_hhmm(earliest)}")
            break

        # Update current position, time, total distance, and route
        j = best
        travel = manhattan(cur, coords[j])
        total_dist += travel
        t += travel
        s, e = windows[j]
        if t < s:  # wait to open
            t = s
        route.append((labels[j], coords[j])) # add to route
        arrivals.append(minutes_since_9am_to_hhmm(t)) # add to arrivals
        cur = coords[j] # move to next point
        unvisited.remove(j) # mark as visited after we have used it

    # Return to depot (0,0) after visiting all points - this is a requirement of the problem
    total_dist += manhattan(cur, origin)
    t += manhattan(cur, origin)
    route.append(("Depot", origin))
    arrivals.append(minutes_since_9am_to_hhmm(t))
    return total_dist, route, arrivals

# Test our program with sample input given in the brief
if __name__ == "__main__":
    sample = [
        ("L1",   5, -10, "09:05", "10:05"),
        ("L2", -12,   8, "10:30", "11:30"),
        ("L3",  15,  20, "12:00", "13:00"),
        ("L4",  -8, -15, "13:30", "14:30"),
        ("L5",  25,  -5, "15:00", "16:00"),
        ("L6", -20,  18, "16:30", "17:30"),
        ("L7",  10,  30, "18:00", "19:00"),
        ("L8", -30, -22, "19:30", "20:30"),
        ("L9",  18,  14, "21:00", "22:00"),
        ("L10", -7,  28, "22:30", "23:30"),
    ]

    dist, route, arrivals = min_distance(sample)
    print("\nRoute (label + coordinates + arrival time):")
    for (label, coord), arr in zip(route, arrivals):
        print(f"{label} {coord} at {arr}")
    print("Total travel cost (Manhattan distance):", dist)
