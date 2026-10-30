import heapq
import matplotlib.pyplot as plt

# 1. Road network: location -> [(neighbour, distance), ...]
graph = {
    "A": [("B", 4), ("C", 2)],
    "B": [("A", 4), ("C", 1), ("D", 5)],
    "C": [("A", 2), ("B", 1), ("D", 8), ("E", 10)],
    "D": [("B", 5), ("C", 8), ("E", 2)],
    "E": [("C", 10), ("D", 2)]
}


# 2. Dijkstra's shortest path algorithm
def dijkstra(graph, source, destination):
    distances = {node: float("inf") for node in graph}
    previous = {node: None for node in graph}

    distances[source] = 0
    priority_queue = [(0, source)]

    while priority_queue:
        current_distance, current = heapq.heappop(priority_queue)

        # Ignore outdated entries
        if current_distance > distances[current]:
            continue

        if current == destination:
            break

        for neighbour, weight in graph[current]:
            new_distance = current_distance + weight

            if new_distance < distances[neighbour]:
                distances[neighbour] = new_distance
                previous[neighbour] = current

                heapq.heappush(
                    priority_queue,
                    (new_distance, neighbour)
                )

    # Check whether destination is reachable
    if distances[destination] == float("inf"):
        return None, float("inf")

    # Reconstruct shortest route
    path = []
    current = destination

    while current is not None:
        path.append(current)
        current = previous[current]

    path.reverse()
    return path, distances[destination]


# 3. Draw road network and highlight shortest route
def draw_graph(graph, path, distance):
    positions = {
        "A": (0, 2),
        "B": (2, 4),
        "C": (2, 0),
        "D": (5, 2),
        "E": (8, 2)
    }

    plt.figure(figsize=(10, 6))

    # Draw all roads and their distances
    for node in graph:
        for neighbour, weight in graph[node]:
            if node < neighbour:
                x1, y1 = positions[node]
                x2, y2 = positions[neighbour]

                plt.plot(
                    [x1, x2], [y1, y2],
                    color="gray", linewidth=2, zorder=1
                )

                # Display road distance
                mx = (x1 + x2) / 2
                my = (y1 + y2) / 2

                plt.text(
                    mx, my, str(weight),
                    fontsize=11,
                    ha="center",
                    va="center",
                    backgroundcolor="white"
                )

    # Highlight the shortest route
    if path:
        for i in range(len(path) - 1):
            u = path[i]
            v = path[i + 1]

            x1, y1 = positions[u]
            x2, y2 = positions[v]

            plt.plot(
                [x1, x2], [y1, y2],
                color="red", linewidth=4, zorder=2
            )

        # Show route and total distance
        plt.title(
            f"Shortest Route: {' -> '.join(path)} "
            f"(Distance: {distance} km)",
            fontsize=14
        )
    else:
        plt.title("No route exists between these locations")

    # Draw all locations
    for node, (x, y) in positions.items():
        plt.scatter(
            x, y,
            s=1100,
            color="skyblue",
            edgecolors="black",
            zorder=3
        )

        plt.text(
            x, y, node,
            fontsize=13,
            ha="center",
            va="center",
            weight="bold",
            zorder=4
        )

    # Legend
    plt.plot([], [], color="gray", linewidth=2, label="Road")
    plt.plot([], [], color="red", linewidth=4, label="Shortest Path")
    plt.legend(loc="upper right")

    plt.text(
        0.5, 0.02,
        "Road distances are in kilometres (km)",
        transform=plt.gca().transAxes,
        ha="center"
    )

    plt.axis("off")
    plt.tight_layout()

    # Save graph image in project folder
    plt.savefig("smart_route_graph.png", dpi=150)
    print("\nGraph saved as smart_route_graph.png")

    # Display graph
    plt.show()


# 4. Main program
def main():
    print("=" * 50)
    print("          SMART ROUTE FINDER")
    print("   Dijkstra's Shortest Path Algorithm")
    print("=" * 50)

    print("\nAvailable locations:", ", ".join(graph.keys()))
    print("Road distances are in kilometres (km).")

    source = input("\nEnter starting location: ").strip().upper()
    destination = input("Enter destination: ").strip().upper()

    # Validate input
    if source not in graph or destination not in graph:
        print("Error: Please enter valid locations A, B, C, D, or E.")
        return

    # Calculate shortest path
    path, distance = dijkstra(graph, source, destination)

    # Display results
    if path is None:
        print("\nNo route exists between these locations.")
    else:
        print("\nShortest Route:", " -> ".join(path))
        print("Total Distance:", distance, "km")

        # Display and save graph
        draw_graph(graph, path, distance)


# 5. Run the program
if __name__ == "__main__":
    main()

