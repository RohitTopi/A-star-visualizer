# A-star-visualizer

## About
A* visualizer written in python using pygame

A* pathfinding algorithm is a best-first search algorithm that finds one of the optimal path from a source node to a destination node. It relies on an open list and a closed list to find a path. It works by combining the benefits of the uniform-cost search and greedy search algorithms.  
A* makes use of both elements by including two separate path finding functions in its algorithm that take into account the cost from the root node to the current node and estimates the path cost from the current node to the goal node.  
`f(n) = g(n) + h(n)`  
It represents the cost of the path that is estimated to be most efficient towards the destination node. A* continues to re-evaluate both `g(n)` and `h(n)` throughout the search for all of the nodes that it encounters in order to arrive at the minimal cost path to the destination node.  
The function `g(n)` calculates the path cost between the source node and the current node. The second function `h(n)` is a heuristic to calculate the estimated path cost from the current node to the destination node.  

## Algorithm
The A* algorithms:  
1. Create an open list and a closed list that are both empty.  
2. Put the start node in the open list.
3. Loop this until the goal is found or the open list is empty:  
    a. Find the node with the lowest F cost in the open list and place it in the closed list.
    b. Expand this node and for the adjacent nodes to this node:
        i.   If they are on the closed list, ignore.
        ii.  If not on the open list, add to open list, store the current node as the parent for this 
                adjacent node, and calculate the F, G, H costs of the adjacent node.
        iii. If on the open list, compare the G costs of this path to the node and the old path to the 
                node. If the G cost of using the current node to get to the node is the lower cost, change 
                the parent node of the adjacent node to the current node. Recalculate F, G, H costs of the node.

## Implementation notes
This implementation uses priority queue for getting the minimum F-cost node

## Example run

![example1](./img/case1.gif)
