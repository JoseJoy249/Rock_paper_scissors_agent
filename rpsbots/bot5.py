if input == "":
    import math
    log = math.log
    exp = math.exp
    log_half = log(0.5)
    third = 1.0 / 3.0
    log_third = log(1.0/3.0)
    log_two_thirds = log(2.0/3.0)

    def log_add(x, y):
        if y > x:
            x, y = y, x
        d = y - x
        if d < -60:
            return x
        return x + log(1.0 + exp(d))

    def log_sub(x, y):
        d = y - x
        return x + log(1.0 - exp(d))

    def log_mean(x, y):
        return log_half + log_add(x, y)

    def log_mean_3(x, y, z):
        return log_third + log_add(log_add(x, y), z)

    def meta(k, c):
        if k == c:
            d = 0
        elif k == beat[c]:
            d = 1
        else:
            d = 2
        return d

    class ContextTree:
        def __init__(self):
            self.p_self = 0.0
            self.p_meta = 0.0
            self.p = 0.0
            self.weights = [log_third for _ in range(3)]
            self.counts = [0, 0, 0]
            self.meta_counts = [0, 0, 0]
            self.children = [None, None, None]
        def update(self, k0, alpha, history, c, i=0):
            counts = self.counts
            meta_counts = self.meta_counts
            scores = [0.0 for _ in range(3)]
            for j in range(3):
                scores[j] = counts[beaten[j]] - counts[beat[j]]
            k = scores.index(max(scores))
            d = meta(k, c)
            rt = 1.0 / (sum(counts) + 1.0)
            self.p_self += log((counts[c] + third) * rt)
            self.p_meta += log((meta_counts[d] + third) * rt)
            counts[c] += 1
            meta_counts[d] += 1
            if i >= min(len(history) - 1, 10):
                self.p = log_mean(self.p_self, self.p_meta)
                return
            x = history[i]
            if self.children[x] is None:
                self.children[x] = ContextTree()
            self.children[x].update(k0, alpha, history, c, i + 1)
            p_children = 0.0
            for child in self.children:
                if child is not None:
                    p_children += child.p
            w0, w1, w2 = self.weights
            self.p = log_add(w0 + self.p_self, log_add(w1 + self.p_meta, w2 + p_children))
            probs = (self.p_self, self.p_meta, p_children)
            for i, (w, p) in enumerate(zip(self.weights, probs)):
                self.weights[i] = log_add(alpha + self.p, k0 + w + p) + log_half
            t = log_add(log_add(self.weights[0], self.weights[1]), self.weights[2])
            for i, w in enumerate(self.weights):
                self.weights[i] -= t
        def predict(self, history, ps, i=0):
            counts = self.counts
            meta_counts = self.meta_counts
            scores = [0.0 for _ in range(3)]
            for j in range(3):
                scores[j] = counts[beaten[j]] - counts[beat[j]]
            k = scores.index(max(scores))
            rt = 1.0 / (sum(counts) + 1.0)
            p_self = (self.p_self + log((counts[c] + third) * rt) for c in range(3))
            p_meta = (self.p_self + log((meta_counts[meta(k, c)] + third) * rt) for c in range(3))
            if i >= min(len(history) - 1, 10):
                for i, (p0, p1) in enumerate(zip(p_self, p_meta)):
                    ps[i] += log_mean(p0, p1)
                return
            x = history[i]
            p_children = [0.0 for _ in self.children]
            factor = 0.0
            for y, child in enumerate(self.children):
                if child is not None:
                    if y == x:
                        child.predict(history, p_children, i + 1)
                    else:
                        factor += child.p
                elif y == x:
                    factor += log_third
            for j, p in enumerate(p_children):
                p_children[j] = p + factor
            w0, w1, w2 = self.weights
            for i, (pse, pm, pc) in enumerate(zip(p_self, p_meta, p_children)):
                ps[i] += log_add(w0 + pse, log_add(w1 + pm, w2 + pc))

    import collections
    import random

    R, P, S = range(3)
    index = {"R": R, "P": P, "S": S}
    name = ("R", "P", "S")
    beat   = (P, S, R)
    beaten = (S, R, P)
    model = ContextTree()
    history = collections.deque([])
    output = random.choice(name)
    rnd = 0
else:
    rnd += 1
    i = index[input]
    j = index[output]
    alpha = 1.0 / (rnd + 1)
    k0 = (1 - alpha) * 3 - 1
    model.update(log(k0), log(alpha), history, i)
    history.appendleft(i)
    history.appendleft(j)
    ps = [0.0, 0.0, 0.0]
    model.predict(history, ps)
    p0 = min(ps)
    for i, p in enumerate(ps):
        ps[i] = exp(p - p0)
    scores = [0, 0, 0]
    t = sum(ps)
    for _ in range(3):
        x = 0
        r = random.uniform(0, t)
        for k, p in enumerate(ps):
            x += p
            if x >= r:
                break
        scores[beat[k]]   += 1
        scores[beaten[k]] -= 1
    m = max(scores)
    output = name[random.choice([k for k, x in enumerate(scores) if x == m])]