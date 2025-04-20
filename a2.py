import numpy as np
import time

# Mendefinisikan peta kota
city_map = [
    ["S", ".", ".", "T", "."],
    [".", ".", "T", ".", "."],
    ["", ".", ".", ".", "."],
    [".", "T", "T", ".", "T"],
    [".", ".", "T", ".", "H"]
]

# Inisialisasi posisi Start dan Hospital
start = None
goal = None

# Mencari posisi Start (S) dan Hospital (H) dalam grid
for i in range(len(city_map)):
    for j in range(len(city_map[0])):
        if city_map[i][j] == "S":
            start = (i, j)
        elif city_map[i][j] == "H":
            goal = (i, j)

#  Pastikan posisi Start dan Hospital ditemukan
def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

# Fungsi untuk mencari jalur menggunakan A*
def a_star(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    visited = set()
    open_list = [(0 + manhattan(start, goal), 0, start, [start])]
    node_count = 0

    while open_list:
        open_list.sort()  # sort by f(n) = g(n) + h(n)
        f, g, current, path = open_list.pop(0)
        node_count += 1
        if current == goal:
            return path, node_count
        if current in visited:
            continue
        visited.add(current)
        x, y = current
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if grid[nx][ny] != "T" and (nx, ny) not in visited:
                    new_g = g + 1  # Assume uniform cost for each step
                    new_f = new_g + manhattan((nx, ny), goal)
                    open_list.append((new_f, new_g, (nx, ny), path + [(nx, ny)]))
    return None, node_count

def visualize_grid(grid, path):
    """
    Visualisasi grid dengan jalur yang ditemukan.
    """
    visual_grid = [row[:] for row in grid]  # Salin grid
    for x, y in path:
        if visual_grid[x][y] not in ("S", "H"):
            visual_grid[x][y] = "*"
    print("\nGrid Visualization:")
    for row in visual_grid:
        print(" ".join(row))

# Fungsi untuk mencari jalur menggunakan GBFS
def gbfs(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    visited = set()
    open_list = [(manhattan(start, goal), start, [start])]
    node_count = 0

    while open_list:
        open_list.sort()  # sort by heuristic value
        h, current, path = open_list.pop(0)
        node_count += 1
        if current == goal:
            return path, node_count
        if current in visited:
            continue
        visited.add(current)
        x, y = current
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if grid[nx][ny] != "T" and (nx, ny) not in visited:
                    open_list.append((manhattan((nx, ny), goal), (nx, ny), path + [(nx, ny)]))
    return None, node_count

# Menjalankan A*
start_time = time.time()
astar_path, astar_nodes = a_star(city_map, start, goal)
end_time = time.time()
astar_time_ms = (end_time - start_time) * 1000

# Menjalankan GBFS
start_time = time.time()
gbfs_path, gbfs_nodes = gbfs(city_map, start, goal)
end_time = time.time()
gbfs_time_ms = (end_time - start_time) * 1000

# Tampilkan hasil A*
print("A*")
if astar_path:
    print(f"Path: {astar_path}")
    print(f"Nodes explored: {astar_nodes}")
    print(f"Elapsed time: {astar_time_ms:.2f} ms")
    visualize_grid(city_map, astar_path)
else:
    print("No path found using A*.")


# Tampilkan hasil GBFS
print("\nGBFS")
if gbfs_path:
    print(f"Path: {gbfs_path}")
    print(f"Nodes explored: {gbfs_nodes}")
    print(f"Elapsed time: {gbfs_time_ms:.2f} ms")
    visualize_grid(city_map, gbfs_path)
else:
    print("No path found using GBFS.")

