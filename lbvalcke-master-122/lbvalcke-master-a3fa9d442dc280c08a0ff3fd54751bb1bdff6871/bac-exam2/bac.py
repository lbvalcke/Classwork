import re

def mystery0(N):
    if N < 1:
      return
    mystery0(N-1)
    print(N)
    mystery0(N-2)

print("Warmup exercise #1")
mystery0(4)
print()

def mystery1(s, c, d, x):
    if s == "":
        return x
    elif s[0] == c:
        return mystery1(s[1:], c, d, x+1)
    elif s[0] == d:
        if x > 0:
            return mystery1(s[1:], c, d, x-1)        
        return -1
    else:
        return mystery1(s[1:], c, d, x)


def recursion_warmup():
    output_str = 'mystery1("{}", "a", "b", 0): {}'
    for s in ["ab", "abab", "abaab", "ababb", "ababaa"]:
        print(output_str.format(s,  mystery1(s, "a", "b", 0)))

print("Warmup exercise #2")
recursion_warmup()
print()


def functional_programming_warmup():
    return map(lambda x: x + 1, 
               filter(lambda x: x % 3 == 0, range(0, 9)))

print("Warmup exercise #3")
l = functional_programming_warmup()
print(list(l))
print()


def mystery2(fn, N):
    def g(x):
        for i in range(N):
            x = fn(x)
        return x
    return lambda y: g(y*2)


print("Warmup exercise #4")
f = mystery2(lambda x: x+1, 10)
print(f(10))




