# Cited sources: 
# - Video regarding the A* algorithm and how it works/computes: https://www.youtube.com/watch?v=6TsL96NAZCo.
# - Information regarding tuples and how we can sort a list based on the second element in a tuple (used in lines 61 and 186):
#  https://learnpython.com/blog/sort-tuples-in-python/#:~:text=Sorting%20a%20List%20by%20the,lambda%20function%20as%20a%20key.
# - More information regarding tuples and how to iterate over a list of tuples: https://www.geeksforgeeks.org/how-we-can-iterate-through-list-of-tuples-in-python/.

# ******************************************************************************************************************************
# This Anagram class contains the following:
# - anagram_expand(state, goal): returns a list with all possible states, 
#   from initial states to goal states with their corresponding h' scores.
#   It's used for expanding strings, creating children until the goal state is found, 
#   which can be tracked from goal to state using the A* algorithm.

# - heuristics_score(start, goal): returns the heuristic score for a state to goal. 
#   It's a function that returns the estimated cost of the shortest path from a 
#   state to the goal state.

# - a_star(start, goal, expand): returns the a list of the solution path, 
#   from the start state to the goal state, using a heuristics function to help 
#   choose optimal states to the goal state. 

# - contain_same_chars(start, goal): helper function that returns True if both strings 
#   contain the same number of characters, False otherwise, as they're not solvable.

# - solve(start, goal): prints the optimal path from start to goal states, along with the states involved.
#   Also prints the number of A* iterations and steps taken from the start state to reach the goal state.
# ******************************************************************************************************************************

class Anagram:
    # Number of A* iterations. 
    num_iterations = 0

    # Returns a list with all possible states, from initial state to goal state with their corresponding h' scores.
    def anagram_expand(self, state, goal):
        node_list = []
        
        # Create each possible state that can be created from the current one in a single step.
        for pos in range(1, len(state)):
            # ex. 'TRACE' -> 1st iter. -> RTACE
            # 'TRACE'[1:1 + 1] + 'TRACE'[0] + 'TRACE'[1 + 1:]
            # 'R' + 'T' + 'ACE' -> new_state = 'RTACE', and so on until 'CRATE' is found
            # and we can track from the successors all the way to the start state and 
            # find solution in a_star() function.
            new_state = state[1:pos + 1] + state[0] + state[pos + 1:]

            # TO DO: c. Very simple h' function - please improve! 
            # If the new state is already the goal state, the heuristic score is 0.
            if new_state == goal:
                score = 0

            # Otherwise, calculate the h-score using a heuristics function, heuristic_score(),
            # from the new state and goal, and update score.    
            else:
                score = self.heuristic_score(new_state, goal)
                    
            # Append the tuple (new_state, new_score) to the node_list.
            node_list.append((new_state, score))

        # Return a list of pairs in the form: (new_state, h' score)
        # which is sorted, as we want to check the lowest score from other siblings.
        node_list.sort(key = lambda x: x[1])
        return node_list

    # A heuristics function that calculates the distance between a state to the goal state.
    def heuristic_score(self, start, goal):
        # Heuristic score.
        score = 0

        # For every character in both start and goal states, check if
        # 1. If there are duplicate letters, always choose most optimistic.
        # 2. If the start state character is positioned left of the goal state character,
        #    return the difference of the indeces.
        # 3. If the start state character is positioned right of the goal state character,
        #    return the index of the start state character + 1.
        for i in range(len(start)):
            # The goal_index is used to determine whether the current character is to the left or right
            # of the goal position. 
            goal_index = -1
            goal_indeces = []
            for j in range(len(goal)):
                # If same character is found in start and goal states, 
                # store j into goal_indeces for further comparison
                # after the iteration is done. We'll need to check which character is 
                # the closest to each other between start and goal states if duplicates are found.
                if start[i] == goal[j]:
                    goal_indeces.append(j)

            # Choose the most optimistic score.
            goal_index = min(goal_indeces[0], goal_indeces[-1])

            # If the character in start state is present in the goal state, check whether it is left or right
            # of the goal position.
            if goal_index >= 0:
                # This checks if the character is positioned on the left side of the goal state character.
                # Update score to the differences of the indeces.
                if i > goal_index:
                    score = i - goal_index
                
                # This checks if the character is positioned on the right side of the goal state character.
                # Update score to the index of the start state character + 1 
                elif i < goal_index:
                    score = i + 1
                
                # Just in case if something unexpected happens.
                else:
                    score = 0
        
        # Return score.
        return score

    # TO DO: b. Return either the solution as a list of states from start to goal or [] if there is no solution.
    def a_star(self, start, goal, expand):
        # Create a search graph consisting solely of the start node.
        # We can use a dictionary to represent the search graph, where
        # it is used to track the parent of each state, up until start.
        # ex. TRACE : None
        # RTACE : TRACE
        # RATCE : TRACE; and so on.
        searchGraph = {start: None}
        
        # Put start node on a list called OPEN and 
        # create a list called CLOSED that is initially empty.
        OPEN = [start]
        CLOSED = set()

        # Track f-scores and g-scores for each state.
        f_scores = {start: self.heuristic_score(start, goal)}
        g_scores = {start: 0}

        # While the OPEN is not empty...
        while OPEN:
            # Select the first node on OPEN, remove it from OPEN, and put it on CLOSED.
            # Call this node n.
            n = OPEN.pop(0)
            CLOSED.add(n)

            # If n is a goal node, exit successfully with the solution
            # obtained by tracing a path from n to start in searchGraph.
            if n == goal:    
                solution = []
                current = n
                while current != start:
                    solution.append(current)
                    current = searchGraph[current]
                solution.append(start)
                return solution[::-1]

            # Increment the number of iterations
            self.num_iterations += 1

            # Expand node n, generating the set of its successors that are not
            # already ancestors of n in searchGraph.
            successors = expand(n, goal)

            # For every node with its respective h' score from successors...
            for node, node_score in successors:
                # If the node is in CLOSED, continue to the next iteration.
                # This makes sure there's no search cycle.
                if node in CLOSED:
                    continue

                # If the node is not in the graph, 
                # connect n to the searchGraph at node.
                if node not in searchGraph:
                    searchGraph[node] = n

                # Calculate f-score of node.
                # Note: f = g + h.
                g_score = g_scores[n] + 1
                h_score = node_score
                f_score = g_score + h_score

                # If the node from successors is in f_scores and the f-score at node is smaller
                # than the already calculated f-score, then continue to the next sucessor.
                # This ensures that we don't change the f-score at node for something greater, 
                # as we want the lowest score.
                if node in f_scores and f_score >= f_scores[node]:
                    continue

                # Add these members of successors to OPEN and track their f-scores and g-scores.
                OPEN.append(node)
                f_scores[node] = f_score
                g_scores[node] = g_score

            # Reorder the list OPEN in order of increasing f values.
            OPEN.sort(key = lambda x: f_scores[x])

        # If solution is not found, return [].
        return []

    # Helper function to check if the strings contain the same characters.
    def contain_same_chars(self, start, goal):
        return sorted(start) == sorted(goal)

    # Finds a solution, i.e., a placement of all rectangles within the given field, for a rectangle puzzle
    def solve(self, start, goal):
        self.num_iterations = 0

        # TO DO: a. Add code below to check in advance whether the problem is solvable.
        # If the length of the state and goal do not match or they do not contain the same characters,
        # print an error message.
        if (len(start) != len(goal)) or not self.contain_same_chars(start, goal):
           print('This is clearly impossible. I am not even trying to solve this.')
           return "IMPOSSIBLE"

        self.solution = self.a_star(start, goal, self.anagram_expand)

        if not self.solution:
            print('No solution found. This is weird, I should have caught this before even trying A*.')
            return "NONE"

        print(str(len(self.solution) - 1) + ' steps from start to goal:')

        for step in self.solution:
            print(step)

        print(str(self.num_iterations) + ' A* iterations were performed to find this solution.')
        return str(self.num_iterations)

if __name__ == '__main__':
    anagram = Anagram()
#    anagram.solve('ALLERGY', 'LARGELY')
#    anagram.solve('TRACE', 'CRATE')
#    anagram.solve('THECLASSROOM', 'SCHOOLMASTER')
#    anagram.solve('TEARDROP', 'PREDATOR')
#    anagram.solve('DENTIST', 'DENTITS')
#    anagram.solve('ROMA', 'AMOR')
#    anagram.solve('NEPAL', 'PANEL')
#    anagram.solve('FRESA', 'FRASE')
    