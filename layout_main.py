import sys

#nrl = "8 1 -1"
#lineA = "1 -1 1 0 -1 1 -1 0"

nrl = sys.stdin.readline().strip().split()
lineA = sys.stdin.readline().strip().split()
n = int(nrl[0])
R = int(nrl[1])
L = int(nrl[2])
A = []
for a in lineA:
    A.append(int(a))
    
energy_sum = [0] * (n + 1)
for i in range(1, n + 1):
    energy_sum[i] = energy_sum[i - 1] + A[i - 1]
balance = [0] * (n + 1)
for i in range(1, n + 1):
    balance[i] = balance[i - 1]
    if A[i - 1] == R:
        balance[i] += 1
    elif A[i - 1] == L:
        balance[i] -= 1
max_len = 0
first_got = {}
for i in range(n + 1):
    key = (energy_sum[i], balance[i])
    if key in first_got:
        length = i - first_got[key]
        if length > max_len:
            max_len = length
    else:
        first_got[key] = i
print(max_len)