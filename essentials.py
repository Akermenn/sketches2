import sys

# text = i1t2m3o4 it - mo i...t...mitmo
#text = input()
text = sys.stdin.read()
lines = text.split('\n')
itmo_groups = []
for line in lines:
    paths = []
    line_lwr = line.lower()
    i_positions = []
    for idx in range(len(line_lwr)):
        if line_lwr[idx] == 'i':
            i_positions.append(idx)
    for pos_i in i_positions:
        for distance in range(1, len(line_lwr) - pos_i):
            pos_t = pos_i + distance
            if line_lwr[pos_t] != 't':
                continue
            pos_m = pos_t + distance
            if pos_m >= len(line_lwr) or line_lwr[pos_m] != 'm':
                continue
            pos_o = pos_m + distance
            if pos_o >= len(line_lwr) or line_lwr[pos_o] != 'o':
                continue
            paths.append([pos_i, pos_t, pos_m, pos_o])
    if len(paths) != 0:
        # сортировка групп текущей строки
        for i in range(len(paths)):
            for j in range(i + 1, len(paths)):
                if paths[j][3] < paths[i][3]:
                    paths[i], paths[j] = paths[j], paths[i]
                elif paths[j][3] == paths[i][3] and paths[j][0] < paths[i][0]:
                    paths[i], paths[j] = paths[j], paths[i]
        itmo_groups.append(paths)
    else:
        itmo_groups.append([-1])
print(itmo_groups)
if len(itmo_groups) != 0:
    for line_groups in itmo_groups:
        if line_groups == [-1]:
            print(-1)
        else:
            output = [] # строки для вывода
            for group in line_groups:
                output.append(f"{group[0]},{group[1]},{group[2]},{group[3]}")
            print("\n".join(output))
else:
    print(-1)

