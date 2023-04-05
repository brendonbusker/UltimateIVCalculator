import requests

#Fox example
'''
response = requests.get("https://randomfox.ca/floof")

fox = response.json()
print(fox['image'])
'''


#Testing with PokeAPI
'''
response = requests.get("https://pokeapi.co/api/v2/pokemon/ditto")

ditto = response.json()

print(ditto['stats'][0])
print(ditto['stats'][0]['base_stat'])
'''
'''
#Testing with user input now
usr_input = input("Type pokemon name: ").lower()

response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{usr_input}")

pokemon = response.json()

hp = pokemon['stats'][0]['base_stat']
atk = pokemon['stats'][1]['base_stat']
defense = pokemon['stats'][2]['base_stat']
sp_atk = pokemon['stats'][3]['base_stat']
sp_defense = pokemon['stats'][4]['base_stat']
spd = pokemon['stats'][5]['base_stat']

print(f"HP: {hp}, ATTACK: {atk}, DEFENSE: {defense}, SPECIAL ATTACK: {sp_atk}, SPECIAL DEFENSE: {sp_defense}, SPEED: {spd}")

iv = ((372/1.1 - 5) * 100) / 100 - 2 * 120 - 252/4
print(iv)

#Test w/loop

for i in range(0,5):
    stat = pokemon['stats'][i]['base_stat']
    print(f"stats: {stat}")
'''

response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0")

pokemon = response.json()

all_pokemon_list = []

for i in range(0, len(pokemon['results'])):
    all_pokemon_list.append(pokemon['results'][i]['name'].title())

print(all_pokemon_list[999])
