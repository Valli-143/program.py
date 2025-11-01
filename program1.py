from collections import deque
import sys

def read_input():
    lines = [line.strip() for line in sys.stdin if line.strip()]
    # Find the first integer line
    for i, line in enumerate(lines):
        if line.isdigit():
            n = int(line)
            break
    else:
        return 0, [], []

    # Find "shuffled" and "original" markers
    try:
        shuffled_index = lines.index("shuffled", i + 1) + 1
        original_index = lines.index("original", shuffled_index + n) + 1
    except ValueError:
        return 0, [], []

    shuffled = lines[shuffled_index : shuffled_index + n]
    original = lines[original_index : original_index + n]
    return n, shuffled, original

def build_permutation(shuffled, original):
    pos_map = {}
    for idx, val in enumerate(original):
        pos_map.setdefault(val, []).append(idx)
    used = {}
    perm = []
    for val in shuffled:
        if val not in pos_map:
            return None
        count = used.get(val, 0)
        if count >= len(pos_map[val]):
            return None
        perm.append(pos_map[val][count])
        used[val] = count + 1
    return perm

def min_cut_insert(perm):
    start = tuple(perm)
    target = tuple(sorted(perm))
    if start == target:
        return 0
    n = len(perm)
    q = deque([start])
    dist = {start: 0}
    while q:
        cur = q.popleft()
        d = dist[cur]
        for i in range(n):
            for j in range(i, n):
                seg = cur[i:j+1]
                rest = cur[:i] + cur[j+1:]
                for k in range(len(rest)+1):
                    if k == i:
                        continue
                    new = rest[:k] + seg + rest[k:]
                    new_t = tuple(new)
                    if new_t == target:
                        return d + 1
                    if new_t not in dist:
                        dist[new_t] = d + 1
                        q.append(new_t)
    return -1

def main():
    n, shuffled, original = read_input()
    if n == 0 or len(shuffled) != n or len(original) != n:
        print(0)
        return
    perm = build_permutation(shuffled, original)
    if perm is None:
        print(0)
    else:
        print(min_cut_insert(perm))

if __name__ == "__main__":
    main()
