import sys
import math

data = sys.stdin.buffer.read().split()
it = iter(data)

n = int(next(it))
m = int(next(it))

gamma = [float(next(it)) for _ in range(n)]
cext = [float(next(it)) for _ in range(n)]

reactions = []
for _ in range(m):
    i = int(next(it))
    j = int(next(it))
    l = int(next(it))
    mm = int(next(it))
    k = float(next(it))
    ch = {}
    ch[i] = ch.get(i, 0) - 1
    if j != -1:
        ch[j] = ch.get(j, 0) - 1
    ch[l] = ch.get(l, 0) + 1
    if mm != -1:
        ch[mm] = ch.get(mm, 0) + 1
    items = [(s, v) for s, v in ch.items() if v]
    reactions.append((i, j, l, mm, k, items))

def eval_fj(c, lam):
    f = [gamma[i] * (cext[i] - c[i]) for i in range(n)]
    jm = [[0.0] * n for _ in range(n)]
    for i in range(n):
        jm[i][i] = -gamma[i]
    for i, j, l, mm, k, items in reactions:
        kk = k * lam
        if j == -1:
            rate = kk * c[i]
            di = kk
            for s, v in items:
                f[s] += v * rate
                jm[s][i] += v * di
        else:
            ci = c[i]
            cj = c[j]
            rate = kk * ci * cj
            di = kk * cj
            dj = kk * ci
            for s, v in items:
                f[s] += v * rate
                jm[s][i] += v * di
                jm[s][j] += v * dj
    return f, jm

def norm2(v):
    s = 0.0
    for x in v:
        s += x * x
    return s

def norm_inf(v):
    mx = 0.0
    for x in v:
        ax = abs(x)
        if ax > mx:
            mx = ax
    return mx

def gauss(a, b):
    a = [row[:] for row in a]
    b = b[:]
    for col in range(n):
        piv = col
        mx = abs(a[col][col])
        for r in range(col + 1, n):
            v = abs(a[r][col])
            if v > mx:
                mx = v
                piv = r
        if mx < 1e-14:
            return None
        if piv != col:
            a[col], a[piv] = a[piv], a[col]
            b[col], b[piv] = b[piv], b[col]
        pv = a[col][col]
        rowc = a[col]
        for r in range(col + 1, n):
            fac = a[r][col] / pv
            if fac == 0.0:
                continue
            rowr = a[r]
            for cc in range(col + 1, n):
                rowr[cc] -= fac * rowc[cc]
            b[r] -= fac * b[col]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = b[i]
        row = a[i]
        for j in range(i + 1, n):
            s -= row[j] * x[j]
        if abs(row[i]) < 1e-14:
            return None
        x[i] = s / row[i]
    return x

def gs_sweep(c, lam):
    md = 0.0
    for s in range(n):
        gain = 0.0
        loss = gamma[s]
        for i, j, l, mm, k, items in reactions:
            kk = k * lam
            react_has = i == s or j == s
            prod_has = l == s or mm == s
            if prod_has and not react_has:
                gain += kk * c[i] * (1.0 if j == -1 else c[j])
            elif react_has and not prod_has:
                if j == -1:
                    loss += kk
                else:
                    loss += kk * (c[j] if i == s else c[i])
        nv = (gain + gamma[s] * cext[s]) / loss
        d = abs(nv - c[s])
        if d > md:
            md = d
        c[s] = nv
    return md

def solve_stage(start, lam):
    c = start[:]
    for _ in range(15):
        if gs_sweep(c, lam) < 1e-12:
            break
    for _ in range(40):
        f, jm = eval_fj(c, lam)
        if norm_inf(f) < 1e-11:
            return c, True
        delta = gauss(jm, [-x for x in f])
        cand = None
        if delta is not None:
            cur = norm2(f)
            step = 1.0
            while step > 1e-10:
                cn = [c[i] + step * delta[i] for i in range(n)]
                ok = True
                for x in cn:
                    if x <= 0.0 or not math.isfinite(x):
                        ok = False
                        break
                if ok:
                    fn, _ = eval_fj(cn, lam)
                    if norm2(fn) < cur:
                        cand = cn
                        break
                step *= 0.5
        if cand is None:
            before = c[:]
            md = gs_sweep(c, lam)
            if md < 1e-12:
                break
            same = True
            for i in range(n):
                if abs(c[i] - before[i]) > 1e-14:
                    same = False
                    break
            if same:
                break
        else:
            c = cand
    f, _ = eval_fj(c, lam)
    return c, norm_inf(f) < 1e-7

c = cext[:]
lam = 0.0
step = 0.1

while lam < 1.0 - 1e-15:
    nxt = lam + step
    if nxt > 1.0:
        nxt = 1.0
    sol, ok = solve_stage(c, nxt)
    if ok:
        c = sol
        lam = nxt
        if lam < 1.0:
            step = min(step * 1.5, 1.0 - lam)
    else:
        step *= 0.5
        if step < 1e-6:
            c, _ = solve_stage(c, 1.0)
            break

c, _ = solve_stage(c, 1.0)
print(" ".join(f"{x:.10f}" for x in c))
