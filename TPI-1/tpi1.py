#STUDENT NAME: João Nuno da Silva Luís
#STUDENT NUMBER: 107403

#DISCUSSED TPI-1 WITH: (names and numbers):
# José Gameiro, 108840
# Diogo Falcão, 108712
# Daniel Madureira, 107603

from tree_search import *
import math
class OrderDelivery(SearchDomain):

    def __init__(self,connections, coordinates):
        self.connections = connections
        self.coordinates = coordinates

    def actions(self,state):
        city = state[0]
        actlist = []
        for (C1,C2,D) in self.connections:
            if (C1==city):
                actlist += [(C1,C2)]
            elif (C2==city):
               actlist += [(C2,C1)]
        return actlist 

    def result(self,state,action):
        (C1,C2) = action
        if C1==state[0]:
            return (C2, state[1].copy())

    def satisfies(self, state, goal):
        if state[0] in goal[1] and state[0] not in state[1]:
            state[1].append(state[0])
        return set(goal[1]).issubset(state[1]) and goal[0] == state[0]

    def cost(self, state, action):
        (C1,C2) = action
        for InitialC, FinalC, dist in self.connections:
            if(InitialC, FinalC) in [(C1,C2), (C2,C1)]:
                return dist

    def heuristic(self, state, goal):
        currentC = state[0]
        goal_cp = state[1].copy()
        if state[0] == goal[0]:
            return 0
        if goal_cp == []:
            goal_cp.append(goal[0])
        while goal_cp != []:
            distances = []
            for city in goal_cp:
                distance = math.dist(self.coordinates[currentC], self.coordinates[city])
                
                distances.append(distance)
            min_distances = min(distances)
            currentC = goal_cp[distances.index(min_distances)]
            goal_cp.remove(currentC)
        return min_distances    
class MyNode(SearchNode):
    def __init__(self,state,parent,depth=0,cost=0,heuristic=0,eval=0, marked= False):
        super().__init__(state,parent)
        #ADD HERE ANY CODE YOU NEED
        self.depth = 0 if parent == None else parent.depth + 1 
        self.cost = cost
        self.heuristic = heuristic
        self.eval = eval
        self.marked = marked

class MyTree(SearchTree):
    def __init__(self,problem, strategy='breadth',maxsize=None):
        super().__init__(problem,strategy)
        #ADD HERE ANY CODE YOU NEED

        self.problem = problem
        root = MyNode(problem.initial, None, heuristic= problem.domain.heuristic(problem.initial, problem.goal), eval= problem.domain.heuristic(problem.initial, problem.goal) )
        self.open_nodes = [root]
        self.strategy = strategy
        self.solution = None
        self.terminals = len(self.open_nodes)
        self.non_terminals = 0
        self.treeSize = self.non_terminals + self.terminals
        self.max_size = maxsize
        self.children = None

    @property
    def length(self):
        return self.solution.depth
    
    @property
    def cost(self):
        return self.solution.cost

    def astar_add_to_open(self,lnewnodes):
        self.open_nodes.extend(lnewnodes)
        self.open_nodes.sort(key= lambda node: (node.eval, node.state ))
        pass

    def search2(self):
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)

            if self.problem.goal_test(node.state):
                self.solution = node
                self.terminals = len(self.open_nodes)+1
                return self.get_path(node)
            self.non_terminals += 1

            self.treeSize = self.non_terminals + len(self.open_nodes)
            lnewnodes = []

            for a in self.problem.domain.actions(node.state):
                newstate = self.problem.domain.result(node.state,a)

                if newstate not in self.get_path(node):
                    newnode = MyNode(newstate,node, 
                    cost= node.cost + self.problem.domain.cost(node.state,a), 
                    heuristic = round(self.problem.domain.heuristic(newstate, self.problem.goal)), 
                    eval= round(self.problem.domain.heuristic(newstate, self.problem.goal) + node.cost + self.problem.domain.cost(node.state,a) ))
                    lnewnodes.append(newnode)
            
            node.children = lnewnodes
            if self.strategy == "A*" and self.max_size != None and self.treeSize > self.max_size:
                    self.manage_memory()
            self.add_to_open(lnewnodes)            
        return None
    
    def manage_memory(self):
        while len(self.open_nodes) + self.non_terminals > self.max_size:
            nodes_Deletion = []
            self.open_nodes.sort(key = lambda node: node.eval, reverse=True)
            for node in self.open_nodes:
                if not node.marked:
                    nodes_Deletion.append(node)
                    node.marked = True
                    break
            nodes_for_removing = []
            parents_for_add = []
            for node in nodes_Deletion:
                parent = node.parent
                siblings = parent.children
                if all(sibling.marked for sibling in siblings):
                    nodes_for_removing.extend(siblings)
                    parent.eval = min(sibling.eval for sibling in siblings)
                    self.non_terminals -=1
                    parents_for_add.append(parent)
            
            if nodes_for_removing:
                self.open_nodes = [node for node in self.open_nodes if node not in nodes_for_removing]
                self.add_to_open(parents_for_add)

        for node in self.open_nodes:
            node.marked = False

def orderdelivery_search(domain,city,targetcities,strategy='breadth',maxsize=None):
    state = (city, [])
    goal = (city, targetcities)

    my_prob = SearchProblem(domain, state, goal)

    my_tree = MyTree(my_prob,strategy,maxsize)
    my_tree.search2()
    path = []
    for state, goals in my_tree.get_path(my_tree.solution):
        path.append(state)
    return (my_tree, path)