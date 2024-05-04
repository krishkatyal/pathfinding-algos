import pygame
import sys
import heapq

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 600
BOX_WIDTH, BOX_HEIGHT = 20, 20
ROWS, COLS = HEIGHT // BOX_HEIGHT, WIDTH // BOX_WIDTH

# Set up some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Set up the display
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinding Algorithms")

class Box:
    id_counter = 0
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.wall = False
        self.target = False
        self.parent = None
        self.distance = float('inf')
        self.id = Box.id_counter
        Box.id_counter += 1

    def __lt__(self, other):
        return self.id < other.id

    def draw(self, window, color=WHITE):
        pygame.draw.rect(window, color, (self.j * BOX_WIDTH, self.i * BOX_HEIGHT, BOX_WIDTH, BOX_HEIGHT))

    def get_neighbours(self):
        neighbours = []
        if self.i > 0:
            neighbours.append(grid[self.i - 1][self.j])
        if self.i < ROWS - 1:
            neighbours.append(grid[self.i + 1][self.j])
        if self.j > 0:
            neighbours.append(grid[self.i][self.j - 1])
        if self.j < COLS - 1:
            neighbours.append(grid[self.i][self.j + 1])
        return neighbours

# Set up the grid
grid = [[Box(i, j) for j in range(COLS)] for i in range(ROWS)]

# Set up the start and target boxes
start_box = grid[0][0]
target_box = None

# Set up the open and closed lists
open_list = []
closed_list = set()

# Set up the path
path = []

# Function to draw the grid
def draw_grid():
    for row in grid:
        for box in row:
            box.draw(window)

# Function to draw the path
def draw_path():
    for box in path:
        box.draw(window, GREEN)

# Function to reconstruct the path
def reconstruct_path(current_box):
    while current_box != start_box:
        path.append(current_box)
        current_box = current_box.parent
    path.reverse()

# Dijkstra's Algorithm
def dijkstra():
    open_list = [(0, start_box)]
    closed_list = set()
    while open_list:
        current_distance, current_box = heapq.heappop(open_list)
        if current_box == target_box:
            reconstruct_path(current_box)
            break
        if current_box in closed_list:
            continue
        closed_list.add(current_box)
        for neighbour in current_box.get_neighbours():
            if neighbour not in closed_list and not neighbour.wall:
                distance = current_distance + 1
                if distance < neighbour.distance:
                    neighbour.distance = distance
                    neighbour.parent = current_box
                    heapq.heappush(open_list, (distance, neighbour))
        window.fill(BLACK)
        draw_grid()
        for box in closed_list:
            box.draw(window, YELLOW)
        if target_box:
            target_box.draw(window, RED)
        if path:
            draw_path()
        pygame.display.update()
        pygame.time.delay(50)

# Breadth-First Search (BFS)
def bfs():
    open_list = [start_box]
    closed_list = set()
    
    while open_list:
        current_box = open_list.pop(0)
        if current_box == target_box:
            reconstruct_path(current_box)
            break
        if current_box in closed_list:
            continue
        closed_list.add(current_box)
        for neighbour in current_box.get_neighbours():
            if neighbour not in closed_list and not neighbour.wall:
                neighbour.parent = current_box
                open_list.append(neighbour)
        window.fill(BLACK)
        draw_grid()
        for box in closed_list:
            box.draw(window, YELLOW)
        if target_box:
            target_box.draw(window, RED)
        if path:
            draw_path()
        pygame.display.update()
        pygame.time.delay(50)

# Depth-First Search (DFS)
def dfs():
    open_list = [start_box]
    closed_list = set()
    while open_list:
        current_box = open_list.pop()
        if current_box == target_box:
            reconstruct_path(current_box)
            break
        if current_box in closed_list:
            continue
        closed_list.add(current_box)
        for neighbour in current_box.get_neighbours():
            if neighbour not in closed_list and not neighbour.wall:
                neighbour.parent = current_box
                open_list.append(neighbour)
        window.fill(BLACK)
        draw_grid()
        for box in closed_list:
            box.draw(window, YELLOW)
        if target_box:
            target_box.draw(window, RED)
        if path:
            draw_path()
        pygame.display.update()
        pygame.time.delay(50)

# Best-First Search
def best_first_search():
    open_list = [(0, start_box)]
    closed_list = set()
    while open_list:
        current_distance, current_box = heapq.heappop(open_list)
        if current_box == target_box:
            reconstruct_path(current_box)
            break
        if current_box in closed_list:
            continue
        closed_list.add(current_box)
        for neighbour in current_box.get_neighbours():
            if neighbour not in closed_list and not neighbour.wall:
                distance = abs(neighbour.i - target_box.i) + abs(neighbour.j - target_box.j)
                heapq.heappush(open_list, (distance, neighbour))
                neighbour.parent = current_box
        window.fill(BLACK)
        draw_grid()
        for box in closed_list:
            box.draw(window, YELLOW)
        if target_box:
            target_box.draw(window, RED)
        if path:
            draw_path()
        pygame.display.update()
        pygame.time.delay(50)


# A* Search
def a_star_search():
    open_list = []
    heapq.heappush(open_list, (0, start_box))
    closed_list = set()
    came_from = {}
    g_score = {box: float('inf') for row in grid for box in row}
    g_score[start_box] = 0
    f_score = {box: float('inf') for row in grid for box in row}
    f_score[start_box] = heuristic(start_box, target_box)
    while open_list:
        current = heapq.heappop(open_list)[1]
        if current == target_box:
            reconstruct_path(came_from, current)
            break
        closed_list.add(current)
        for neighbour in current.get_neighbours():
            if neighbour in closed_list or neighbour.wall:
                continue
            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = tentative_g_score
                f_score[neighbour] = tentative_g_score + heuristic(neighbour, target_box)
                heapq.heappush(open_list, (f_score[neighbour], neighbour))
    window.fill(BLACK)
    draw_grid()
    for box in closed_list:
        box.draw(window, YELLOW)
    if start_box:
        start_box.draw(window, GREEN)
    if target_box:
        target_box.draw(window, RED)
    if path:
        draw_path()
    pygame.display.update()
    pygame.time.delay(50)

def heuristic(a, b):
    return abs(a.i - b.i) + abs(a.j - b.j)

def reconstruct_path(came_from, current):
    global path
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.append(start_box)
    path.reverse()

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            i, j = pygame.mouse.get_pos()
            i //= BOX_HEIGHT
            j //= BOX_WIDTH
            # Check if the clicked position is within the grid boundaries
            if 0 <= i < len(grid) and 0 <= j < len(grid[0]):
                if event.button == 1:  # Left mouse button
                    grid[i][j].wall = True
                elif event.button == 3:  # Right mouse button
                    if not start_box:
                        start_box = grid[i][j]
                    elif not target_box:
                        target_box = grid[i][j]
                    else:
                        grid[i][j].wall = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bfs()
            elif event.key == pygame.K_d:
                dfs()
            elif event.key == pygame.K_b:
                best_first_search()
            elif event.key == pygame.K_a:
                a_star_search()
            elif event.key == pygame.K_r:
                reset()
    window.fill(BLACK)
    draw_grid()
    if start_box:
        start_box.draw(window, GREEN)
    if target_box:
        target_box.draw(window, RED)
    if path:
        draw_path()
    pygame.display.update()
