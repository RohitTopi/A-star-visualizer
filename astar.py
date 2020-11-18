import pygame
import math
from queue import PriorityQueue

# color constants, these correspond to state of the node
CLOSED_COLOR = (154, 200, 255)		# blue
OPEN_COLOR = (196, 236, 255)		# cyan
PATH_COLOR = (20, 180, 20)			# green

TRAVERSABLE_COLOR = (254, 254, 254) # white
BARRIER_COLOR = (30, 30, 30)		# black
SRC_COLOR = (255, 32, 32)			# red 
DEST_COLOR = (255, 148, 52)			# orange
GRID_LINE_COLOR = (240,240,240)		# grey

class Node:
	def __init__(self, row, col, node_width, n_rows):
		self.row = row
		self.col = col
		self.x = row * node_width
		self.y = col * node_width
		self.color = TRAVERSABLE_COLOR	# initially grid is empty
		self.neighbors = []
		self.width = node_width
		self.n_rows = n_rows

	# returns the (row,col) position in the grid
	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == CLOSED_COLOR

	def is_open(self):
		return self.color == OPEN_COLOR

	def is_barrier(self):
		return self.color == BARRIER_COLOR

	# sets nodes' state to traversable
	def reset(self):
		self.color = TRAVERSABLE_COLOR

	def make_source(self):
		self.color = SRC_COLOR

	def make_closed(self):
		self.color = CLOSED_COLOR

	def make_open(self):
		self.color = OPEN_COLOR

	def make_barrier(self):
		self.color = BARRIER_COLOR

	def make_dest(self):
		self.color = DEST_COLOR

	def make_path(self):
		self.color = PATH_COLOR

	# draws the node
	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width), border_radius = 1)

	# updates neighbors in self.neighbor, barriers are not added
	def update_neighbors(self, grid):
		self.neighbors = []

		# down
		if self.row < self.n_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
			self.neighbors.append(grid[self.row + 1][self.col])

		# up
		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
			self.neighbors.append(grid[self.row - 1][self.col])

		# right
		if self.col < self.n_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
			self.neighbors.append(grid[self.row][self.col + 1])

		# left
		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
			self.neighbors.append(grid[self.row][self.col - 1])


	# comparison operator
	def __lt__(self, other):
		return False


# reconstruct the path
def reconstruct_path(prev_list, current, draw):
	while current in prev_list:
		current = prev_list[current]	# recursive
		current.make_path()
		draw()

# heuristic function, uses manhattan distance
def h_cost(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)


def astar(draw, grid, source, dest):
	count = 0

	# initialize the queue
	open_set = PriorityQueue()
	open_set.put((0, count, source))
	
	# keeps track of predecessor
	prev_list = {}

	# initialize all g-costs
	g_cost = {node: float("inf") for row in grid for node in row}
	g_cost[source] = 0
	
	# initialize all f-cost using g-cost and h-cost
	f_cost = {node: float("inf") for row in grid for node in row}
	f_cost[source] = h_cost(source.get_pos(), dest.get_pos())

	open_set_hash = {source}

	while not open_set.empty():

		# go through all events
		for evt in pygame.event.get():

			# user clicks the close button
			if evt.type == pygame.QUIT:
				pygame.quit()


		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == dest:
			reconstruct_path(prev_list, dest, draw)
			dest.make_dest()
			return True

		for neighbor in current.neighbors:
			temp_g_cost = g_cost[current] + 1

			if temp_g_cost < g_cost[neighbor]:
				prev_list[neighbor] = current
				g_cost[neighbor] = temp_g_cost
				f_cost[neighbor] = temp_g_cost + h_cost(neighbor.get_pos(), dest.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_cost[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != source:
			current.make_closed()

	return False


# creates and returns a grid of nodes
def create_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			node = Node(i, j, gap, rows)
			grid[i].append(node)

	return grid

# draws horizontal and vertical grid lines 
def draw_grid(win, rows, width):
	gap = width // rows

	# horizontal grid lines
	for i in range(rows):
		pygame.draw.line(win, GRID_LINE_COLOR, (0, i * gap), (width, i * gap))

	# vertical grid lines
	for j in range(rows):
		pygame.draw.line(win, GRID_LINE_COLOR, (j * gap, 0), (j * gap, width))


# draws the grid of nodes, and updates the display
def draw(win, grid, rows, width):
	win.fill(TRAVERSABLE_COLOR)

	for row in grid:
		for node in row:
			node.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()


# get the clicked node coordinate
#	convert (x,y) to (row,col)
def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col



def main():
	N_ROWS = 64
	w_width = 640
	win = pygame.display.set_mode((w_width, w_width))	# square grid
	pygame.display.set_caption("A* Visualizer")

	grid = create_grid(N_ROWS, w_width)

	source = None
	dest = None

	running = True

	while running:
		draw(win, grid, N_ROWS, w_width)
		for evt in pygame.event.get():
			if evt.type == pygame.QUIT:
				running = False

			# for the right mouse click
			# 	the order is enforced as to create a source node,
			# 	then the destination node and finally the barriers
			if pygame.mouse.get_pressed()[0]: # left mouse click
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, N_ROWS, w_width)
				node = grid[row][col]
				if not source and node != dest:
					source = node
					source.make_source()

				elif not dest and node != source:
					dest = node
					dest.make_dest()

				elif node != dest and node != source:
					node.make_barrier()

			# if user wants to change source and/or destination
			elif pygame.mouse.get_pressed()[2]:		# right mouse click
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, N_ROWS, w_width)
				node = grid[row][col]
				node.reset()
				if node == source:
					source = None
				elif node == dest:
					dest = None

			if evt.type == pygame.KEYDOWN:

				# start on 'SPACE' keypress
				if evt.key == pygame.K_SPACE and source and dest:
					for row in grid:
						for node in row:
							node.update_neighbors(grid)

					astar(lambda: draw(win, grid, N_ROWS, w_width), grid, source, dest)

				# clear the screen on 'c' keypress.
				if evt.key == pygame.K_c:
					source = None
					dest = None
					grid = create_grid(N_ROWS, w_width)

	pygame.quit()


main()

