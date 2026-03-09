import sys
from itertools import permutations

data = list(map(int, sys.stdin.buffer.read().split()))
it = iter(data)

d = next(it)
t = next(it)

ans = [0.0] * d

for _ in range(t):
    n = next(it)
    pairs = []
    used = set()
    for _ in range(n):
        a = next(it) - 1
        b = next(it) - 1
        pairs.append((a, b))
        used.add(a)
        used.add(b)

    rows = []
    for _ in range(1 << n):
        row = [next(it) for _ in range(d)]
        rows.append(row)

    vals = list(used)
    k = len(vals)
    pos = {v: i for i, v in enumerate(vals)}

    cnt = [0] * (1 << n)

    for perm in permutations(range(k)):
        rank = [0] * k
        for r, p in enumerate(perm):
            rank[p] = r

        idx = 0
        for a, b in pairs:
            idx = (idx << 1) | (rank[pos[a]] > rank[pos[b]])
        cnt[idx] += 1

    total = 1
    for i in range(2, k + 1):
        total *= i

    for mask in range(1 << n):
        p = cnt[mask] / total
        row = rows[mask]
        for j in range(d):
            ans[j] += p * row[j]

print(*[f"{x:.10f}" for x in ans])
