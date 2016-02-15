import csv

def parse_csv(filepath, id_field=None):
	datafile = open(filepath, 'r')
	datareader = csv.reader(datafile)
	records = []
	if id_field:
		records = {}
	headers = None
	for row in datareader:
		if headers is None:
			headers = row
		else:
			record = {}
			id = None
			for i in range(0, len(headers)):
				if headers[i] == id_field:
					id = row[i]
				else:
					record[headers[i]] = row[i]
			if id:
				records[id] = record
			else:
				records.append(record)
	return records

# load a list of all pokemon and their types
all_pokemon = parse_csv('./all-pokemon-types.csv')
all_type_combos = []
for poke in all_pokemon:
	poke['number'] = int(poke['number'])
	poke['types'] = set(poke['types'].split(' '))
	type_combo_exists = False
	for type_combo in all_type_combos:
		if len(type_combo) == len(poke['types']) and len(type_combo & poke['types']) == len(type_combo):
			type_combo_exists = True
			break
	if not type_combo_exists:
		all_type_combos.append(poke['types'])

# load a list of all type advantages
type_advantages = parse_csv('./poke-type-advantages.csv', 'type');
for offense_type in type_advantages:
	for defense_type in type_advantages[offense_type]:
		type_advantages[offense_type][defense_type] = float(type_advantages[offense_type][defense_type])

# read in the user's team of pokemon
input_string = 'Bulbasaur, Charmander, Squirtle'
pokemon_names = [x.strip() for x in input_string.split(',')]
pokemon_team = []
for name in pokemon_names:
	found_pokemon = False
	for poke in all_pokemon:
		if poke['name'] == name:
			found_pokemon = True
			pokemon_team.append(poke)
	if not found_pokemon:
		print 'Could not find a Pokemon named %s' % name

# for each type, figure out if this team is checked by it
doubly_advantageous_matchups = []
advantageous_matchups = []
standoff_matchups = []
disadvantageous_matchups = []
for opposing_type_combo in all_type_combos:
	best_matchup = None
	num_equivalent_matchups = 0
	for poke in pokemon_team:
		best_offense = None
		worst_defense = None
		for team_offense_type in poke['types']:
			multiplier = 1.0
			for opposing_defense_type in opposing_type_combo:
				multiplier *= type_advantages[team_offense_type][opposing_defense_type]
			if best_offense is None or multiplier > best_offense:
				best_offense = multiplier
		for opposing_offense_type in opposing_type_combo:
			multiplier = 1.0
			for team_defense_type in poke['types']:
				multiplier *= type_advantages[opposing_offense_type][team_defense_type]
			if worst_defense is None or multiplier > worst_defense:
				worst_defense = multiplier
		matchup = 0
		if best_offense > worst_defense:
			matchup = 1
		elif best_offense < worst_defense:
			matchup = -1
		if best_matchup is None or matchup > best_matchup:
			best_matchup = matchup
			num_equivalent_matchups = 0
		if best_matchup == matchup:
			num_equivalent_matchups += 1
	if best_matchup > 0:
		advantageous_matchups.append(opposing_type_combo)
		if best_matchup > 0 and num_equivalent_matchups >= 2:
			doubly_advantageous_matchups.append(opposing_type_combo)
	elif best_matchup < 0:
		disadvantageous_matchups.append(opposing_type_combo)
	else:
		standoff_matchups.append(opposing_type_combo)

print 'With a team of %s:' % ', '.join([poke['name'] for poke in pokemon_team])
print ' There are %i (%i%%) advantageous matchups (%i are covered by more than one pokemon)' % (len(advantageous_matchups), 100 * len(advantageous_matchups) / len(all_type_combos), len(doubly_advantageous_matchups))
print ' There are %i (%i%%) standoffs:' % (len(standoff_matchups), 100 * len(standoff_matchups) / len(all_type_combos))
for matchup in standoff_matchups:
	print '  vs. %s' % " ".join(matchup)
print ' There are %i (%i%%) disadvantageous matchups:' %(len(disadvantageous_matchups), 100 * len(disadvantageous_matchups) / len(all_type_combos))
for matchup in disadvantageous_matchups:
	print '  vs. %s' % " ".join(matchup)















