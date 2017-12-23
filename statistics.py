import json

#file = 'result_bear.txt'
filename = 'result_bear2.txt'
file = open(filename, 'r')
lines = file.readlines()

# local variables
name = [' ', ' ', ' ']
value = [0, 0, 0]
nameStart = [-1, -1, -1]
nameEnd = [-1, -1, -1]
probabilityStart = [-1, -1, -1]
probabilityEnd = [-1, -1, -1]

# statistics data
count = 0
sum = 0
accuracy = 0

# analyze line by line
for line in lines:
	# find name index
	nameStart[0] = line.find('Name:') + 5
	nameStart[1] = line.find('Name:', nameStart[0]) + 5
	nameStart[2] = line.find('Name:', nameStart[1]) + 5
	nameEnd[0] = line.find(', Probability:')
	nameEnd[1] = line.find(', Probability', nameEnd[0]+1)
	nameEnd[2] = line.find(', Probability', nameEnd[1]+1)
	
	# insert name into variable
	for i in range(0,3):
		name[i] = line[ nameStart[i] : nameEnd[i] ]

	# find probability index
	probabilityStart[0] = line.find('Probability:') + 12
	probabilityStart[1] = line.find('Probability:', probabilityStart[0]) + 12
	probabilityStart[2] = line.find('Probability:', probabilityStart[1]) + 12
	probabilityEnd[0] = line.find('}')
	probabilityEnd[0] = line.find('}', probabilityEnd[0]+1)
	probabilityEnd[0] = line.find('}', probabilityEnd[1]+1)

	# insert probability into variable
	for i in range(0,3):
		value[i] = float( line[ probabilityStart[0] : probabilityEnd[0] ] )
	
	
	if name[0].find('bear') >= 0:
		count += 1
		accuracy
		sum += value[0]
	elif name[1].find('bear') >= 0:
		count += 1
		sum += value[1]
	elif name[2].find('bear') >= 0:
		count += 1
		sum += value[2]
#	for i in range(0,3):
#		print(name[i] + "     " + str(value[i]))
#	print('-------------------------------------')

print(count)
print(sum)
