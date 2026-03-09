import sys

a = list(map(int, sys.stdin.read().split()))
n, t = a[0], a[1]
p = a[2:2 + n]
d = a[2 + n:2 + 2 * n]
h = a[2 + 2 * n:2 + 2 * n + t]

ans = set()

for wp in (-2, -1, 0, 1, 2):
    for wd in (-2, -1, 0, 1, 2):
        for wr in (-2, -10, -20):
            c = [0] * n
            ok = True
            for x in h:
                best = 0
                val = wp * p[0] + wd * d[0] + wr * c[0]
                for i in range(1, n):
                    cur = wp * p[i] + wd * d[i] + wr * c[i]
                    if cur > val:
                        val = cur
                        best = i
                if best != x:
                    ok = False
                    break
                c[x] += 1
            if ok:
                best = 0
                val = wp * p[0] + wd * d[0] + wr * c[0]
                for i in range(1, n):
                    cur = wp * p[i] + wd * d[i] + wr * c[i]
                    if cur > val:
                        val = cur
                        best = i
                ans.add(best)

print(ans.pop())
