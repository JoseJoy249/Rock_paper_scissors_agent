import numpy as np
def chars_to_dict(chars):
    chars = sorted(list(set(chars)))
    char_to_index  = {x: i for i, x in enumerate(chars)}
    return char_to_index


class Node:
    def __init__(self,code ='' ):
        '''Function for initialising node'''
        self.code = code
        self.child = {}
        self.num_desc = 0

    def add_child(self, char_to_index ):
        '''Function for adding children to a node, given parent '''
        for w in char_to_index:
            self.child[char_to_index[w]] = Node(self.code+w)
        self.num_desc += len(char_to_index)


class Tree(Node):
    def __init__(self,char_to_index):
        '''function for initialising tree, with all alphabets as children'''
        self.nodes = Node()
        self.nodes.add_child(char_to_index)
        self.char_to_index = char_to_index
        self.num_desc = len(char_to_index)

    def add_nodes(self, parent ):
        '''function to add children, given a parent node
        input
        parent : code word of parent  node (str)'''
        assert (self.calc_leafs(parent)==0)
        temp1 = self.nodes
        char_to_index = self.char_to_index
        for w in parent :
            temp1.num_desc += len(char_to_index)-1
            temp1 = temp1.child[char_to_index[w] ]
        temp1.add_child(char_to_index)

    def is_present(self, code):
        '''function to check if a particular code word is present in tree
        Input
        code : code word (str)'''
        char_to_index = self.char_to_index
        temp1 = self.nodes
        for w in code:
            if char_to_index[w] in temp1.child:
                temp1 = temp1.child[char_to_index[w] ]
            else:
                return False
        return True

    def calc_leafs(self,parent ):
        '''function to calculate leafs under a particular parent node
        Input
        parent : codeword of parent(str)'''
        char_to_index = self.char_to_index
        temp1 = self.nodes
        for w in parent :
            temp1 = temp1.child[char_to_index[w] ]
        return temp1.num_desc

    def calc_prob(self, code):
        '''function to calculate probability of next alphabet (probabulity of last 0 in
        100, given 10), given code words
        Input
        code : code word (str) '''
        char_to_index = self.char_to_index
        probs = np.zeros(len(char_to_index))
        for w in char_to_index :
            val = self.calc_leafs(code+w)
            if val == 0:
                val = 1
            probs[char_to_index[w]] = val/float(self.calc_leafs(code))
        return probs

    def get_leaf_nodes(self):
        '''function to get number of total leaf nodes of the tree'''
        leafs = []
        self._collect_leaf_nodes(self.nodes,leafs)
        return leafs

    def _collect_leaf_nodes(self, nodes, leafs):
        '''private function to help get_leaf_nodes to recursively access leafs'''
        if type(nodes) == Node:
            if self.calc_leafs(nodes.code) == 0:
                leafs.append(nodes.code)
            for n in nodes.child:
                self._collect_leaf_nodes( nodes.child[n], leafs)

# Create classes for building context tree, where each node can store the code word, children and weights
class CTNode:
    def __init__(self,char_to_index,code ='' ):
        '''Function for initialising node'''
        self.code = code # code sequence
        self.child = {} # dictionary of children
        self.num_desc = 0 # number of leafs under the node
        self.beta = 1. # context tree weight
        self.counts = {w:0.5 for w in char_to_index} # initialise counts of all alphabets to 1/2

    def add_child(self, char_to_index ):
        '''Function for adding children to a node, given parent '''
        for w in char_to_index:
            # create new nodes and add as children
            self.child[char_to_index[w]] = CTNode(char_to_index, self.code+w)
        self.num_desc += len(char_to_index) # update number of leafs nodes under current node

class CTree(CTNode):
    def __init__(self,char_to_index, max_depth=5, full = False):
        '''function for initialising tree, with all alphabets as children
        input
        char_to_index : dictionary with index values of each alphabet
        max_depth : maximum depth of context tree (int)
        full : if Tree, the entire tree is created during initlialisation'''
        self.nodes = CTNode(char_to_index = char_to_index,code = '')
        self.nodes.add_child(char_to_index)
        self.char_to_index = char_to_index
        self.num_desc = len(char_to_index)
        self.max_depth = max_depth
        if full:
            for i in range(max_depth-1):
                leafs = self.get_leaf_nodes()
                for c in leafs:
                    self.add_nodes(c)

    def add_nodes(self, parent ):
        '''function to add children (all alphabets), given a parent node
        input
        parent : code word of parent  node (str)'''
        assert (self.calc_leafs(parent)==0)
        temp1 = self.nodes
        char_to_index = self.char_to_index
        for w in parent :
            temp1.num_desc += len(char_to_index)-1
            temp1 = temp1.child[char_to_index[w] ]
        temp1.add_child(char_to_index)

    def add_branch(self, code ):
        '''function to add a single branch from root to leaf node at max_depth'''
        if self.is_present(code ) == False: # if a particular node doesnt exist in the tree
            temp1 = self.nodes # start from the root
            char_to_index = self.char_to_index
            for i,w in enumerate(code):
                if char_to_index[w] in temp1.child :
                    temp1.num_desc += 1
                    temp1 = temp1.child[char_to_index[w]]

                else :
                    temp1.child[char_to_index[w]] = CTNode(char_to_index, code = code[:i+1])
                    temp1.num_desc += 1
                    temp1 = temp1.child[char_to_index[w]]

    def calc_leafs(self,parent ):
        '''function to calculate leafs under a particular parent node
        Input
        parent : codeword of parent(str)'''
        char_to_index = self.char_to_index
        temp1 = self.nodes
        for w in parent :
            temp1 = temp1.child[char_to_index[w] ]
        return temp1.num_desc

    def get_leaf_nodes(self):
        '''function to get number of total leaf nodes of the tree'''
        leafs = []
        self._collect_leaf_nodes(self.nodes,leafs)
        return leafs

    def _collect_leaf_nodes(self, nodes, leafs):
        '''private function to help get_leaf_nodes to recursively access leafs'''
        if type(nodes) == CTNode:
            if self.calc_leafs(nodes.code) == 0:
                leafs.append(nodes.code)
            for n in nodes.child:
                self._collect_leaf_nodes( nodes.child[n], leafs)

    def get_node(self,code):
        '''function to get access to a particular node in the tree, which has code word = code (str)'''
        char_to_index = self.char_to_index
        temp1 = self.nodes
        for w in code :
            if char_to_index[w] in temp1.child:
                temp1 = temp1.child[char_to_index[w]]
            else:
                print('Node doesnt exist')
                return None
        return temp1

    def is_present(self,code):
        '''function to check if a node with context, code is present in the tree'''
        char_to_index = self.char_to_index
        temp1 = self.nodes
        for w in code:
            if char_to_index[w] in temp1.child:
                temp1 = temp1.child[char_to_index[w] ]
            else:
                return False
        return True

    def calc_prob(self,context, char):
        '''function to sequentially calculate weighted probability of an alphabet given its context
        input
        context : context/state of length max_depth (str)
        char : alphabet that follows the context (str)'''

        # starting from leaf node, move up the tree, calculating weighted probabilities
        counter = len(context)
        char_to_index = self.char_to_index
        prob1 = np.zeros(len(char_to_index)) # contains probability values following a particular context

        while counter>=0:
            if counter == self.max_depth: # starting from leaf node
                leaf1 = self.get_node(context)
                for w in leaf1.counts:

                    # calculate KT probability, if state is a leaf ( we are at max_depth)
                    prob1[char_to_index[w]] = leaf1.counts[w]/ sum(leaf1.counts.values())
                leaf1.counts[char]+=1 # update counts store in the node

            else : # going up the tree, till root
                if self.is_present(context)==False:
                    self.add_branch(context)
                node1 = self.get_node(context) # get the node
                temp_prob = np.copy(prob1)
                for w in node1.counts:
                    # calculate KT probability at the node
                    p_se = node1.counts[w]/ sum(node1.counts.values())

                    #  outgoing conditional weighted probability
                    temp_prob[char_to_index[w]] = (node1.beta*p_se + prob1[char_to_index[w]])/(node1.beta+1)

                # update weight and count paramters in the node
                p_se = ( node1.counts[char]/ sum(node1.counts.values()) )
                node1.beta = node1.beta*p_se/( prob1[char_to_index[char]] )
                node1.counts[char]+=1
                prob1 = temp_prob

            context = context[1:] # going up the tree, context size decreases by one
            counter -= 1
        return prob1


alph = ["R","P","S"]
dict1 = chars_to_dict(alph)
output = 'R'
i = 0
if input == "": # initialize variables for the first round
    string=""

    # CTW
    max_depth = 10
    code_tree = CTree(dict1, max_depth,full= False)
    temp = list(dict1.keys())[0]
    s0 = temp*max_depth

    # LZ
    temp1 = '' # temporary to find code words
    alphabet = alph # set of alphabets
    code_tree1 = Tree(dict1) # initalising LZ code tree


else :
    # string += input
    char = input
    i += 1
    res = []

    # CTW
    state = s0
    # if a new state is found, create nodes corresponding to that state
    if code_tree.is_present(state) == False:
        code_tree.add_branch(state)
    res.append( code_tree.calc_prob(state,char) + np.random.normal(0,10/np.sqrt(i),3) )
    s0 = s0[1:]+char

    # LZ
    temp1 += input
    res.append( code_tree1.calc_prob(temp1[:-1]) + np.random.normal(0,10/np.sqrt(i),3) )
    # if a new code word has to be created (unique sequence never before seen)
    if code_tree1.calc_leafs(temp1)==0: # when we find new code words
        code_tree1.add_nodes(temp1)
        temp1 = "" # for finding new code words, by going back to the root of the tree
        
    res = np.array(res)
    
    # Weighted combination
    output = alph[ np.argmax( (10*res[0,:]/np.sqrt(i)) + (res[1,:]) ) ]



