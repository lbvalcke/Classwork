# Examples for lists and loops lab

l0 = []
l1 = [1, "abc", 5.7, [1, 3, 5]]
l2 = [10, 11, 12, 13, 14, 15, 16]
l3 = [7, -5, 6, 27, -3, 0, 14]
l4 = [0, 1, 1, 3, 2, 4, 6, 1, 7, 8]
<<<<<<< HEAD

all_pos = []

for x in range(len(l3)): 
	if l3[x] < 0: 
		print("FALSE")
		break
else: 
	print("TRUE")

for x in range(len(l3)):
	if l3[x] >= 0: 
		all_pos.append(l3[x])
print(all_pos)

i = 0
nl = ["FALSE"] * len(l3)
while i < len(l3):
	if l3[i] >= 0:
		nl[i] = "TRUE"
	i += 1
print(nl)

max = max(l4)

count = list(range(max+2))
counting = [0] * (max+1)
for x in count: 
	y = l4[x]
	counting[y] = counting[y] + 1
print(counting)


=======
>>>>>>> 79ace3309267f29e028e155209d8a072a85de3ad
