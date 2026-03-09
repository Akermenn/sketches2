import sys

data = list(map(int, sys.stdin.buffer.read().split()))
it = iter(data)

n = next(it)
m = next(it)
B = next(it)

cols = [[] for _ in range(m)]
for _ in range(n):
    for j in range(m):
        cols[j].append(next(it))

R = B - m
base_cost = 0.0
tasks = []
maxk = min(n, R + 1)

for col in cols:
    col.sort()
    s = col[0]
    c1 = float(s)
    base_cost += c1
    best = c1
    opts = []
    for k in range(2, maxk + 1):
        s += col[k - 1]
        c = s / (k * k)
        if c < best:
            opts.append((k - 1, c - c1))
            best = c
    if opts:
        tasks.append(opts)

tasks.sort(key=lambda x: (x[-1][0], len(x)))

if R == 0 or not tasks:
    print(f"{base_cost:.10f}")
    raise SystemExit

try:
    import numpy as np

    dp = np.full(R + 1, np.inf, dtype=np.float64)
    dp[0] = 0.0
    hi = 0

    for op in tasks:
        ndp = dp.copy()
        for r, delta in op:
            end = hi + r + 1
            if end > R + 1:
                end = R + 1
            if r < end:
                np.minimum(ndp[r:end], dp[:end - r] + delta, out=ndp[r:end])
        dp = ndp
        hi += op[-1][0]
        if hi > R:
            hi = R

    ans = base_cost + float(dp.min())
    print(f"{ans:.10f}")
except Exception:
    INF = 1e100
    prev = [0.0]
    hi = 0

    for op in tasks:
        maxr = op[-1][0]
        new_hi = hi + maxr
        if new_hi > R:
            new_hi = R
        ndp = prev + [INF] * (new_hi - hi)
        prevl = prev
        ndpl = ndp

        for r, delta in op:
            end = hi
            lim = new_hi - r
            if end > lim:
                end = lim
            for b in range(end + 1):
                v = prevl[b] + delta
                nb = b + r
                if v < ndpl[nb]:
                    ndpl[nb] = v

        prev = ndp
        hi = new_hi

    ans = base_cost + min(prev)
    print(f"{ans:.10f}")
