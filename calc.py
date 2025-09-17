from __future__ import annotations

from typing import NamedTuple
from math import log, ceil

class Symbol(NamedTuple): sym:str; prob:float; code:str

def info(p:float) -> float: return log(1 / p, 2)
def entropy(f:list[Symbol]) -> float: return sum(s.prob * info(s.prob) for s in f)
def maxlong(f:list[Symbol]) -> int: return ceil(log(len(list(f)), 2))
def long(f:list[Symbol]) -> float: return sum(s.prob * len(s.code) for s in f)
def eff(f:list[Symbol]) -> float: return entropy(f) / long(f)
def k(f:list[Symbol]) -> float: return sum(2**(-len(s.code)) for s in f)
def compr(f:list[Symbol]) -> float: return maxlong(f) / long(f)
def proby(m:list[list[float]], px:list[float]) -> list[float]: return [sum(a * b for a, b in zip(px, r)) for r in zip(*m)]
def probx(f:list[Symbol]) -> list[float]: return [x.prob for x in f]
def noise(f:list[Symbol], m:list[list[float]]) -> float: return entropy(f) - mutinfo(m, probx(f))
def pe(f:list[Symbol], m:list[list[float]]) -> float: return sum(m[i][i] * f[i].prob for i in range(len(f)))
def pc(f:list[Symbol], m:list[list[float]]) -> float: return 1 - pe(f, m)

def mutinfo_single(src:int, dst:int, m:list[list[float]], px:list[float], py:list[float]|None = None) -> float:
  if py is None: py = proby(m, px)
  return log(m[src][dst] / py[dst], 2) if 0 not in (py[dst], m[src][dst]) else 0

def mutinfo_mat(m:list[list[float]], px:list[float], py:list[float]|None = None) -> list[list[float]]:
  if py is None: py = proby(m, px)
  return [[mutinfo_single(i, j, m, px, py) for j in range(len(m[i]))] for i in range(len(m))]

def mutinfo(m:list[list[float]], px:list[float], py:list[float]|None = None) -> float:
  if py is None: py = proby(m, px)
  return sum(px[i] * m[i][j] * log(m[i][j] / py[j], 2) for i in range(len(m)) for j in range(len(m[i])) if 0 not in (py[j], m[i][j]))

# TODO: rewrite Huffman
# def _huffman_build(l, name:str="") -> list[Symbol]:
#   ret: list[Symbol] = []
#   for tmp, n in zip(l, ("0", "1")):
#     base, value = tmp
#     if isinstance(base, str): ret.append(Symbol(base, value, (name+n)[1:]))
#     else: ret += _huffman_build(base, name+n)
#   return ret

# def huffman(f:list[Symbol]) -> list[Symbol]:
#   res = sorted((x[:2] for x in f), key=lambda x: x.prob)
#   while len(res) > 1:
#     tmp = ((res[0], res[1]), res[0][1] + res[1][1])
#     i = next((i for i in range(2, len(res)) if tmp[1] < res[i][1]), len(res))
#     res = res[2:i] + [tmp] + res[i:]
#   return sorted(_huffman_build(res), key=lambda x: x[1], reverse=True)

def stats(f:list[Symbol], m:list[list[float]] | None = None):
  for x in f: print(f"sym: {x[0]:<4} prob: {x[1]:<8.4f}", f"cod: {x[2]}" if len(x) > 2 else "")
  print(f"{'maxlong:':>15} {maxlong(f)}")
  print(f"{'entropy:':>15} {entropy(f):.6f}")
  print(f"{'long:':>15} {long(f):.6f}")
  print(f"{'eff:':>15} {eff(f):.6f}")
  print(f"{'k:':>15} {k(f):.6f}")
  print(f"{'compr:':>15} {compr(f):.6f}")
  if m is not None:
    print(f"{'pe:':>15} {pe(f, m):.6f}")
    print(f"{'pc:':>15} {pc(f, m):.6f}")
    print(f"{'mutinfo:':>15} {mutinfo(m, probx(f)):.6f}")
    print(f"{'noise:':>15} {noise(f, m):.6f}")

if __name__ == "__main__":
  x = [
    Symbol("x1", 0.35, "00"),
    Symbol("x2", 0.15, "01"),
    Symbol("x3", 0.50, "10"),
  ]
  m = [
    [0.72, 0.04, 0.15, 0.09],
    [0.12, 0.75, 0.00, 0.13],
    [0.07, 0.08, 0.82, 0.03]
  ]
  stats(x, m)
  print()

  x = [
    Symbol("A", 0.50, "1"),
    Symbol("B", 0.15, "011"),
    Symbol("C", 0.15, "010"),
    Symbol("D", 0.08, "001"),
    Symbol("E", 0.08, "0001"),
    Symbol("F", 0.02, "00001"),
    Symbol("G", 0.01, "000001"),
    Symbol("H", 0.01, "000000")
  ]
  # x = huffman(x)
  stats(x)
  print()

  # x = [
  #   Symbol("A", 0.385, ""),
  #   Symbol("B", 0.179, ""),
  #   Symbol("C", 0.154, ""),
  #   Symbol("D", 0.154, ""),
  #   Symbol("E", 0.128, "")
  # ]
  # x = huffman(x)
  # stats(x)
