#!/usr/bin/python

def mystery(a, b, c, d):
  if c == 0:
    return d
  elif c % 2 == 0:
    return b + mystery(a, b, c - 2, d)
  else:
    return a + mystery(a, b, c - 1, d)

print("Warmup Exercise #1")
print(mystery("x", "y", 6, "z"))
print(mystery("x", "y", 5, "z"))
print()


def flip(s, a):
  if a == 0:
    return s
  for i in range(a):
    if s[i] == "*":
      s[i] = "-"
    else:
      s[i] = "*"
  return flip(s, a//2)

print("Warmup Exercise #2")
s = []
for i in range(64):
  s.append("*")
s = flip(s, 64)
t = ""
for c in s:
  t = t + c
print(t)
