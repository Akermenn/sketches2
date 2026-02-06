import sys

def hanoi(n, s, e, m):
    if n == 0:
        return 0
    pos = disks[n-1]
    if pos == s:
        return hanoi(n-1, s, m, e)
    elif pos == e:
        x = 1
        for i in range(n-1):
            x = x * 2
        a = x - 1
        b = 1
        c = hanoi(n-1, m, e, s)
        return a + b + c
    else:
        return 0

line = sys.stdin.readline().strip()
disks = list(map(int, line.split()))
N = len(disks)
result = hanoi(N, 0, 2, 1)
print(result)