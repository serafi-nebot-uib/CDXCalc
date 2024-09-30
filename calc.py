from __future__ import annotations

# import graphviz

from math import log, ceil

def info(p: float) -> float: return log(1 / p, 2)
def entropy(f: list) -> float: return sum(s[1] * info(s[1]) for s in f)
def maxlong(f: list) -> int: return ceil(log(len(f), 2))
def long(f: list) -> float: return sum(s[1] * len(s[2]) for s in f)
def eff(f: list) -> float: return entropy(f) / long(f)
def k(f: list) -> float: return sum(2**(-len(s[2])) for s in f)
def compr(f: list) -> float: return maxlong(f) / long(f)
def proby(m: list, px: list) -> list: return [sum(a * b for a, b in zip(px, r)) for r in zip(*m)]
def probx(f: list) -> list: return [x[1] for x in f]
def noise(f: list, m: list) -> float: return entropy(f) - mutinfo(m, probx(f))

def mutinfo_single(src: int, dst: int, m: list, px: list, py: list | None = None) -> float:
  if py is None: py = proby(m, px)
  return log(m[src][dst] / py[dst], 2) if 0 not in (py[dst], m[src][dst]) else 0

def mutinfo_mat(m: list, px: list, py: list | None = None) -> list:
  if py is None: py = proby(m, px)
  return [[mutinfo_single(i, j, m, px, py) for j in range(len(m[i]))] for i in range(len(m))]

def mutinfo(m: list, px: list, py: list | None = None) -> float:
  if py is None: py = proby(m, px)
  return sum(px[i] * m[i][j] * log(m[i][j] / py[j], 2) for i in range(len(m)) for j in range(len(m[i])) if 0 not in (py[j], m[i][j]))

def stats(f: list, m: list | None = None):
  print("src:")
  for x in f: print(f"{x[0]:<4} prob: {x[1]:<8}", f"sym: {x[2]}" if len(x) > 2 else "")
  print(f"{'maxlong:':>15} {maxlong(f)}")
  print(f"{'entropy:':>15} {entropy(f)}")
  print(f"{'long:':>15} {long(f)}")
  print(f"{'eff:':>15} {eff(f)}")
  print(f"{'k:':>15} {k(f)}")
  print(f"{'compr:':>15} {compr(f)}")
  if m is not None:
    print(f"{'mutinfo:':>15} {mutinfo(m, probx(f))}")
    print(f"{'noise:':>15} {noise(f, m)}")
  print()

X = [
  ("x1", 0.35, "00"),
  ("x2", 0.15, "01"),
  ("x3", 0.50, "10"),
]
M = [
  [0.72, 0.04, 0.15, 0.09],
  [0.12, 0.75, 0.00, 0.13],
  [0.07, 0.08, 0.82, 0.03]
]

stats(X)

# X = [
#   ("A", 0.125),
#   ("B", 0.125),
#   ("C", 0.125),
#   ("D", 0.125),
#   ("E", 0.125),
#   ("F", 0.125),
#   ("G", 0.125),
#   ("H", 0.125)
# ]

# def huffman(f: list):
#   res = sorted((x[:2] for x in f), key=lambda x: x[1])
#   while len(res) > 1:
#     tmp = ((res[0], res[1]), res[0][1] + res[1][1])
#     i = next((i for i in range(2, len(res)) if tmp[1] < res[i][1]), len(res))
#     res = res[2:i] + [tmp] + res[i:]
#   return res
#
# h = huffman(X)
# print(h)
#
# def view(l, n="", depth=0):
#   for t, num in zip(l[:2], ("1", "0")):
#     base, value = t
#     print("\t" * depth, value, f"{base} {n}" if isinstance(base, str) else f"  ({n})")
#     if not isinstance(base, str): view(base, n + num, depth+1)
#
# view(h)

# d = graphviz.Digraph()
#
# def rec(base, root=None, depth=0):
#   for b, n in zip(base, (1, 0)):
#     childs, value = b
#     name = f"{n} ({value})"
#     if isinstance(root, str): d.edge(root, childs if isinstance(childs, str) else name, label=str(n))
#     print("\t" * depth, value, childs)
#     if not isinstance(childs, str): rec(childs, name, depth=depth+1)
# rec(h)
#
# d.view()
