import math, itertools

types = ["Normal", "Fire", "Water", "Grass", "Electric", "Ice", "Fighting", "Poison", "Ground", "Flying", "Psychic", "Bug", "Rock", "Ghost", "Dragon", "Dark", "Steel", "Fairy"]
advantages = ["............-x..-.", ".--+.+.....+-.-.+.", ".+--....+...+.-...", ".-+-...-+-.-+.-.-.", "..+--...x+....-...", ".--+.-..++....+.-.", "+....+.-.---+x.++-", "...+...--...--..x+", ".+.-+..+.x.-+...+.", "...+-.+....+-...-.", "......++..-....x-.", ".-.+..--.-+..-.+--", ".+...+-.-+.+....-.", "x.........+..+.-..", "..............+.-x", "......-...+..+.-.-", ".--.-+......+...-+", ".-....+-......++-."]

n = len(types)
types_advantage_bytes = []
for i in range(0, n):
	byte = 0
	for j in range(0, n):
		byte = byte + ((2 ** j) if advantages[i][j] == "+" else 0)
	types_advantage_bytes.append({ 'type': types[i], 'byte': byte })

for k in range(1, n):
	best_in_show = []
	num_advantages = 0
	alternatives = []
	for subset in itertools.combinations(types_advantage_bytes, k):
		byte = 0
		for x in subset:
			byte = byte | x['byte']
		if bin(byte).count("1") > num_advantages:
			best_in_show = subset
			num_advantages = bin(byte).count("1")
			alternatives = []
		elif bin(byte).count("1") == num_advantages:
			alternatives.append(subset)
	print "%s advantages when using %s" % (num_advantages, ", ".join([x['type'] for x in best_in_show]))
	for alt in alternatives:
		print " " * (len("%s advantages when using" % (num_advantages)) - 2) + "or %s" % ", ".join([x['type'] for x in alt])
	if num_advantages >= n:
		break
