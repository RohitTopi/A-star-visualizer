# A-star-visualizer
A* visualizer written in python using pygame

A* pathfinding algorithm is a best-first search algorithm that finds one of the optimal path from a source node to a destination node. It relies on an open list and a closed list to find a path. It works by combining the benefits of the uniform-cost search and greedy search algorithms.  
A* makes use of both elements by including two separate path finding functions in its algorithm that take into account the cost from the root node to the current node and estimates the path cost from the current node to the goal node.  
F(n) = g(n) + h(n)  
It represents the cost of the path that is estimated to be most efficient towards the destination node. A* continues to re-evaluate both g(n) and h(n) throughout the search for all of the nodes that it encounters in order to arrive at the minimal cost path to the destination node.  
The function `g(n)` calculates the path cost between the source node and the current node. The second function `h(n)` is a heuristic to calculate the estimated path cost from the current node to the destination node.

example:
![example1](./img/case1.gif)
