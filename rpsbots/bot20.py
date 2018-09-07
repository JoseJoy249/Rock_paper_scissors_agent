if input == "":

    import collections
    import math
    import random

    gamma = random.gammavariate
    sqrt = math.sqrt
    log = math.log
    R, P, S = 0, 1, 2
    index = {"R": R, "P": P, "S": S}
    beat = (P, S, R)
    name = ("R", "P", "S")

    def ucb(pos, neg, n, t):
        a = gamma(pos + 1, 1)
        b = gamma(neg + 1, 1)
        s = a - b
        n = n + 1
        return (s / n) + sqrt(2 * log(t) / n)

    class MarkovTree:
        def __init__(self, counts = None):
            self.pos = [0.0 for _ in range(3)]
            self.neg = [0.0 for _ in range(3)]
            self.visits = [0.0 for _ in range(3)]
            self.children = None

        def score(self, t):
            return ucb(self.pos_total, self.neg_total, self.total_visits, t)

        def select_move(self, t):
            scores = [ucb(pos, neg, n, t) for pos, neg, n in zip(self.pos, self.neg, self.visits)]
            best = max(scores)
            return (best, scores.index(best))

        def update(self, i):
            for j in range(3):
                if j == beat[i]:
                    self.pos[j] += 1
                elif i == beat[j]:
                    self.neg[j] += 1

        def predict(self, h):
            path = []
            stop = False
            path.append(self)
            for d, n in enumerate(h):
                if stop or d >= 16:
                    break
                if self.children is None:
                    self.children = [None for _ in range(3)]
                if self.children[n] is None:
                    self.children[n] = MarkovTree()
                    stop = True
                child = self.children[n]
                self = child
                path.append(self)
            t = sum(3 + sum(node.visits) for node in path)
            best_score = float("-inf")
            for n in path:
                score, move = n.select_move(t)
                if score >= best_score:
                    best_score = score
                    best_node = n
                    best_move = move
            return (best_node, best_move)

    tree = MarkovTree()
    history = collections.deque([])

    node = tree

else:

    i = index[input]
    j = index[output]

    node.visits[j] += 1
    node.update(i)

    history.appendleft(i)
    history.appendleft(j)

node, k = tree.predict(history)
output = name[k]