

import re
import json
import requests
import time
from functools import lru_cache
import os

# Prevent SSL keylog permission issues on Windows
os.environ.pop("SSLKEYLOGFILE", None)

# =========================
# CONFIG
# =========================

EVO_FILE = "revo12000.txt"
OUTPUT_FILE = "random_bst_evolutions.json"
OVERRIDE_FILE = "bst_overrides.json"
FAILED_LOOKUPS_FILE = "failed_lookups.json"

TOTAL_RUNS = 12000
BST_LIMIT = 450
POKEAPI = "https://pokeapi.co/api/v2"

# =========================
# STATS / TIMING
# =========================

STATS = {
    "starters_seen": 0,
    "starters_kept": 0,
    "bst_lookups": 0,
    "failed_starters": [],
    "failed_evolutions": {},
}

# =========================
# LOAD OVERRIDES
# =========================

with open(OVERRIDE_FILE, "r", encoding="utf-8") as f:
    OVERRIDES = json.load(f)

FORCE_BST_STARTERS = {
    name.lower() for name in OVERRIDES.get("force_bst_starter", [])
}

# =========================
# FORCED BST/10 STARTERS
# =========================

FORCED_STARTERS = {
    "Wishiwashi": 175,
    "Wormadam": 424,
    "Wormadams": 424,
    "Wormadamt": 424,
    "Pikachup": 430,
    "Pikachuc": 430,
    "Eeveep": 435,
}

# =========================
# NAME ALIASES (COMPREHENSIVE)
# =========================

NAME_ALIASES = {
    # Regional Forms & Megas
    "Kangaskham": "kangaskhan-mega",
    "Lopunnym": "lopunny-mega",
    "Pidgeotm": "pidgeot-mega",
    "Audinom": "audino-mega",
    "Mawilem": "mawile-mega",
    "Growlitheh": "growlithe-hisui",
    "Zoroarkh": "zoroark-hisui",
    "Braviaryh": "braviary-hisui",
    "Electrodeh": "electrode-hisui",
    "Dudunsprce": "dudunsparce",
    "Squawkbily": "squawkabilly",
    "Miniorc": "minior-core",
    "Golema": "golem-alola",
    "Meowsticf": "meowstic",
    "Abomasnowm": "abomasnow-mega",
    "Absolutm": "absol-mega",
    "Absolm": "absol-mega",
    "Acidictm": "acid-mega",
    "Alakazamm": "alakazam-mega",
    "Altariam": "altaria-mega",
    "Ampharosm": "ampharos-mega",
    "Arctibaxm": "arctibax-mega",
    "Arcunonog": "articuno-galar",
    "Articunog": "articuno-galar",
    "Abomasnow": "abomasnow",
    "Abomasnowm": "abomasnow-mega",
    "Aerodactylm": "aerodactyl-mega",
    "Aggronm": "aggron-mega",
    "Alakazam": "alakazam",
    "Alakazamm": "alakazam-mega",
    "Altaria": "altaria",
    "Altariam": "altaria-mega",
    "Ampharos": "ampharos",
    "Ampharosm": "ampharos-mega",
    "Arcanine": "arcanine",
    "Arcanineh": "arcanine-hisui",
    "Arcaninea": "arcanine-alola",
    "Araquanid": "araquanid",
    "Articuno": "articuno",
    "Articunog": "articuno-galar",
    "Banette": "banette",
    "Banettem": "banette-mega",
    "Basculin": "basculin",
    "Basculinb": "basculin-blue-striped",
    "Basculinw": "basculin-white-striped",
    "Beedrillm": "beedrill-mega",
    "Blastoisem": "blastoise-mega",
    "Braviaryh": "braviary-hisui",
    "Cameruptm": "camerupt-mega",
    "Cameruptm": "camerupt-mega",
    "Centskorch": "centiskorch",
    "Charcadet": "charcadet",
    "Ceruledge": "ceruledge",
    "Charizardm": "charizard-mega-x",
    "Charizardy": "charizard-mega-y",
    "Cherrims": "cherrim",
    "Cherubis": "cherubi",
    "Chien-Pao": "chien-pao",
    "Chi-Yu": "chi-yu",
    "Cinccino": "cinccino",
    "Corsola": "corsola",
    "Corsolag": "corsola-galar",
    "Darmanitan": "darmanitan",
    "Darmanitag": "darmanitan-galar",
    "Darmanitaz": "darmanitan-zen",
    "Darmanitazg": "darmanitan-galar-zen",
    "Decidueye": "decidueye",
    "Decidueyeh": "decidueye-hisui",
    "Deoxys": "deoxys",
    "Deoxyss": "deoxys-speed",
    "Deoxysa": "deoxys-attack",
    "Deoxysd": "deoxys-defense",
    "Diarcie": "diancie",
    "Digletta": "diglett-alola",
    "Ditto": "ditto",
    "Dugtrioa": "dugtrio-alola",
    "Eiscuen": "eiscue",
    "Enamorust": "enamorus-therian",
    "Enamorus": "enamorus-therian",
    "Electrodeh": "electrode-hisui",
    "Exeggutoram": "exeggutor-alola",
    "Exeggutora": "exeggutor-alola",
    "Flabébé": "flabebe",
    "Fezandipti": "fezandipiti",
    "Floettee": "floette",
    "Florges": "florges",
    "Galatiam": "gallade-mega",
    "Galopidesm": "gallade-mega",
    "Garbodorm": "garbodor-mega",
    "Gardevoir": "gardevoir",
    "Gardevoirm": "gardevoir-mega",
    "Garlacier": "gardevoir",
    "Gastrodon": "gastrodon",
    "Gengarm": "gengar-mega",
    "Geodudea": "geodude-alola",
    "Gigaformm": "gigantamax",
    "Gimmighour": "gimmighoul",
    "Glaliem": "glalie-mega",
    "Glastrier": "glastrier",
    "Glelier": "glalie-mega",
    "Glebotom": "gloom",
    "Glimmom": "glimmet-form",
    "Golema": "golem-alola",
    "Golemga": "golem-galar",
    "Goodrah": "goodra-hisui",
    "Goresbyss": "gorebyss",
    "Gossifleur": "gossifleur",
    "Gravitez": "graveler",
    "Gravelera": "graveler-alola",
    "Great Tusk": "great-tusk",
    "Grimmsnarl": "grimmsnarl",
    "Grimer": "grimer",
    "Grimera": "grimer-alola",
    "Grovyle": "grovyle",
    "Growlithe": "growlithe",
    "Growlitheh": "growlithe-hisui",
    "Growtheath": "growlithe-hisui",
    "Grumpig": "grumpig",
    "Guzzlord": "guzzlord",
    "Hakamo-O": "hakamo-o",
    "Happiny": "happiny",
    "Hatterene": "hatterene",
    "Hattrem": "hattrem",
    "Haxorus": "haxorus",
    "Heatran": "heatran",
    "Heracrossm": "heracross-mega",
    "Heracross": "heracross",
    "Hitmonchan": "hitmonchan",
    "Hitmonlee": "hitmonlee",
    "Hitmontop": "hitmontop",
    "Honchkrow": "honchkrow",
    "Hoopa": "hoopa",
    "Houndoomm": "houndoom-mega",
    "Houndstone": "houndstone",
    "Hydreigon": "hydreigon",
    "Hypno": "hypno",
    "Iron Crown": "iron-crown",
    "Iron Hands": "iron-hands",
    "Iron Moth": "iron-moth",
    "Iron Bundle": "iron-bundle",
    "Ironbouldr": "iron-boulder",
    "Ironbundle": "iron-bundle",
    "Ironjuglis": "iron-jugulis",
    "Ironleaves": "iron-leaves",
    "Ironsmither": "iron-moth",
    "Ironthorns": "iron-thorns",
    "Irontreads": "iron-treads",
    "Ironvalian": "iron-valiant",
    "Jirachi": "jirachi",
    "Kartana": "kartana",
    "Kangaskhan": "kangaskhan",
    "Kangaskham": "kangaskhan-mega",
    "Kecleon": "kecleon",
    "Keldeo": "keldeo-resolute",
    "Kingambit": "kingambit",
    "Kingler": "kingler",
    "Kingdra": "kingdra",
    "Klawf": "klawf",
    "Klefki": "klefki",
    "Klinklang": "klinklang",
    "Komala": "komala",
    "Kommo-O": "kommo-o",
    "Krookodile": "krookodile",
    "Krokorok": "krokorok",
    "Landorus": "landorus-therian",
    "Landorust": "landorus-therian",
    "Lanturn": "lanturn",
    "Latias": "latias",
    "Latios": "latios",
    "Leaning": "lean-pokemon",
    "Leafeon": "leafeon",
    "Leavanny": "leavanny",
    "Lechonk": "lechonk",
    "Ledian": "ledian",
    "Ledyba": "ledyba",
    "Lickilicky": "lickilicky",
    "Liepard": "liepard",
    "Lilligant": "lilligant",
    "Lilliganth": "lilligant-hisui",
    "Lilligantg": "lilligant-hisui",
    "Linoone": "linoone",
    "Linooneg": "linoone-galar",
    "Litleo": "litleo",
    "Litten": "litten",
    "Lokix": "lokix",
    "Lombre": "lombre",
    "Lopunny": "lopunny",
    "Lopunnym": "lopunny-mega",
    "Loudred": "loudred",
    "Lucario": "lucario",
    "Lucarionm": "lucario-mega",
    "Ludicolo": "ludicolo",
    "Lumineon": "lumineon",
    "Lunatone": "lunatone",
    "Lurantis": "lurantis",
    "Luvdisc": "luvdisc",
    "Luxio": "luxio",
    "Luxray": "luxray",
    "Mabosstiff": "mabosstiff",
    "Machamp": "machamp",
    "Machoke": "machoke",
    "Machop": "machop",
    "Magby": "magby",
    "Magcargo": "magcargo",
    "Magearna": "magearna",
    "Magikarp": "magikarp",
    "Magmar": "magmar",
    "Magmortar": "magmortar",
    "Magnemite": "magnemite",
    "Magneton": "magneton",
    "Magnezone": "magnezone",
    "Makuhita": "makuhita",
    "Malamar": "malamar",
    "Mamoswine": "mamoswine",
    "Manaphy": "manaphy",
    "Mandibuzz": "mandibuzz",
    "Manectric": "manectric",
    "Manectricm": "manectric-mega",
    "Mantic": "manectric",
    "Mankey": "mankey",
    "Mantine": "mantine",
    "Mantyke": "mantyke",
    "Maractus": "maractus",
    "Mareanie": "mareanie",
    "Mareep": "mareep",
    "Marill": "marill",
    "Marowak": "marowak",
    "Marowaka": "marowak-alola",
    "Marowakg": "marowak-alola",
    "Marshadow": "marshadow",
    "Marshtomp": "marshtomp",
    "Maschiff": "maschiff",
    "Masquerain": "masquerain",
    "Mawile": "mawile",
    "Mawilem": "mawile-mega",
    "Mawilef": "mawile",
    "Medicham": "medicham",
    "Medichamm": "medicham-mega",
    "Medichamf": "medicham",
    "Meditite": "meditite",
    "Meganium": "meganium",
    "Melmetal": "melmetal",
    "Meltan": "meltan",
    "Meowstic": "meowstic-male",
    "Meowsticf": "meowstic-female",
    "Meowth": "meowth",
    "Meowthg": "meowth-galar",
    "Meowthg": "meowth-galar",
    "Meowthga": "meowth-alola",
    "Mesprit": "mesprit",
    "Metagross": "metagross",
    "Metagrossm": "metagross-mega",
    "Metang": "metang",
    "Metapod": "metapod",
    "Mew": "mew",
    "Mienfoo": "mienfoo",
    "Mienshao": "mienshao",
    "Mightyena": "mightyena",
    "Milcery": "milcery",
    "Milotic": "milotic",
    "Miltank": "miltank",
    "Mime Jr.": "mime-jr",
    "Minccino": "minccino",
    "Minior": "minior",
    "Miniorc": "minior-core",
    "Minun": "minun",
    "Misdreavus": "misdreavus",
    "Mismagius": "mismagius",
    "Mitsume": "misty-pokemon",
    "Moltres": "moltres",
    "Moltresg": "moltres-galar",
    "Monferno": "monferno",
    "Morellull": "morelull",
    "Morelull": "morelull",
    "Morgrem": "morgrem",
    "Morpeko": "morpeko",
    "Morpekoh": "morpeko-hangry",
    "Mothim": "mothim",
    "Mr. Mime": "mr-mime",
    "Mr. Mimeg": "mr-mime-galar",
    "Mr. Rime": "mr-rime",
    "Mudbray": "mudbray",
    "Mudkip": "mudkip",
    "Mudsdale": "mudsdale",
    "Muk": "muk",
    "Muka": "muk-alola",
    "Mukg": "muk-galar",
    "Mukla": "muk-alola",
    "Munchlax": "munchlax",
    "Munkidori": "munkidori",
    "Munna": "munna",
    "Murkrow": "murkrow",
    "Musharna": "musharna",
    "Nacli": "nacli",
    "Naclstack": "naclstack",
    "Naganadel": "naganadel",
    "Nait": "natu",
    "Natu": "natu",
    "Necrozma": "necrozma",
    "Necrozmaul": "necrozma-ultra",
    "Nickit": "nickit",
    "Nidoking": "nidoking",
    "Nidoqueen": "nidoqueen",
    "Nidoran♀": "nidoran-f",
    "Nidoran♂": "nidoran-m",
    "Nidorina": "nidorina",
    "Nidorino": "nidorino",
    "Nihilego": "nihilego",
    "Nincada": "nincada",
    "Ninetales": "ninetales",
    "Ninetalesa": "ninetales-alola",
    "Ninjask": "ninjask",
    "Noctowl": "noctowl",
    "Noibat": "noibat",
    "Noivern": "noivern",
    "Nosepass": "nosepass",
    "Numel": "numel",
    "Nuzleaf": "nuzleaf",
    "Nymble": "nymble",
    "Obstagoon": "obstagoon",
    "Octillery": "octillery",
    "Oddish": "oddish",
    "Ogerpon": "ogerpon",
    "Ogerponr": "ogerpon-water-mask",
    "Okidogi": "okidogi",
    "Omanyte": "omanyte",
    "Omastar": "omastar",
    "Onix": "onix",
    "Oranguru": "oranguru",
    "Orbeetle": "orbeetle",
    "Orthworm": "orthworm",
    "Oshawott": "oshawott",
    "Overqwil": "overqwil",
    "Pachirisu": "pachirisu",
    "Palafin": "palafin",
    "Palalosstiff": "pallossand",
    "Palossand": "pallossand",
    "Palpitoad": "palpitoad",
    "Pancham": "pancham",
    "Pangoro": "pangoro",
    "Pangorom": "pangoro-mega",
    "Panpour": "panpour",
    "Pansage": "pansage",
    "Pansear": "pansear",
    "Paras": "paras",
    "Parasect": "parasect",
    "Passimian": "passimian",
    "Patrat": "patrat",
    "Pawmi": "pawmi",
    "Pawmo": "pawmo",
    "Pawmot": "pawmot",
    "Pawniard": "pawniard",
    "Pecharunt": "pecharunt",
    "Pelipper": "pelipper",
    "Perrserker": "perrserker",
    "Persian": "persian",
    "Persiana": "persian-alola",
    "Petilil": "petilil",
    "Phanpy": "phanpy",
    "Phantump": "phantump",
    "Pheromosa": "pheromosa",
    "Phione": "phione",
    "Pichu": "pichu",
    "Pidgeot": "pidgeot",
    "Pidgeotm": "pidgeot-mega",
    "Pidgeotto": "pidgeotto",
    "Pidgey": "pidgey",
    "Pidove": "pidove",
    "Pignite": "pignite",
    "Pikachu": "pikachu",
    "Pikachuc": "pikachu-gmax",
    "Pikachup": "pikachu-partner",
    "Pikipek": "pikipek",
    "Piloswine": "piloswine",
    "Pincurchin": "pincurchin",
    "Pineco": "pineco",
    "Pinsir": "pinsir",
    "Pinsirm": "pinsir-mega",
    "Piplup": "piplup",
    "Plusle": "plusle",
    "Poipole": "poipole",
    "Politoed": "politoed",
    "Poliwag": "poliwag",
    "Poliwhirl": "poliwhirl",
    "Poliwrath": "poliwrath",
    "Ponyta": "ponyta",
    "Ponytag": "ponyta-galar",
    "Poochyena": "poochyena",
    "Popplio": "popplio",
    "Porygon": "porygon",
    "Porygon-Z": "porygon-z",
    "Porygon2": "porygon2",
    "Primarina": "primarina",
    "Primeape": "primeape",
    "Prinplup": "prinplup",
    "Probopass": "probopass",
    "Psyduck": "psyduck",
    "Pumpkaboo": "pumpkaboo",
    "Pumpkabool": "pumpkaboo-large",
    "Pumpkaboos": "pumpkaboo-small",
    "Pumpkaboox": "pumpkaboo-xlarge",
    "Pupitar": "pupitar",
    "Purrloin": "purrloin",
    "Purugly": "purugly",
    "Pyroar": "pyroar",
    "Pyukumuku": "pyukumuku",
    "Quagsire": "quagsire",
    "Quaquaval": "quaquaval",
    "Quaxly": "quaxly",
    "Quaxwell": "quaxwell",
    "Quilava": "quilava",
    "Quilladin": "quilladin",
    "Qwilfish": "qwilfish",
    "Qwilfishh": "qwilfish-hisui",
    "Raboot": "raboot",
    "Rabsca": "rabsca",
    "Raichu": "raichu",
    "Raichus": "raichu-alola",
    "Raikou": "raikou",
    "Ralts": "ralts",
    "Rampardos": "rampardos",
    "Rapidash": "rapidash",
    "Rapidashg": "rapidash-galar",
    "Raticate": "raticate",
    "Raticatea": "raticate-alola",
    "Rattata": "rattata",
    "Rattataa": "rattata-alola",
    "Regice": "regice",
    "Regidrago": "regidrago",
    "Regieleki": "regieleki",
    "Regirock": "regirock",
    "Registeel": "registeel",
    "Relicanth": "relicanth",
    "Rellor": "rellor",
    "Remoraid": "remoraid",
    "Reuniclus": "reuniclus",
    "Revavroom": "revavroom",
    "Rhydon": "rhydon",
    "Rhyhorn": "rhyhorn",
    "Rhyperior": "rhyperior",
    "Ribombee": "ribombee",
    "Rillaboom": "rillaboom",
    "Riolu": "riolu",
    "Roarinmoon": "roaring-moon",
    "Rockruff": "rockruff",
    "Roggenrola": "roggenrola",
    "Rolycoly": "rolycoly",
    "Rookidee": "rookidee",
    "Roselia": "roselia",
    "Roserade": "roserade",
    "Rotom": "rotom",
    "Rowlet": "rowlet",
    "Rufflet": "rufflet",
    "Sableyem": "sableye-mega",
    "Sableye": "sableye",
    "Salamence": "salamence",
    "Salamencem": "salamence-mega",
    "Salandit": "salandit",
    "Salazzle": "salazzle",
    "Salazzlem": "salazzle-mega",
    "Samurott": "samurott",
    "Samurotth": "samurott-hisui",
    "Sandaconda": "sandaconda",
    "Sandile": "sandile",
    "Sandshrew": "sandshrew",
    "Sandshrewa": "sandshrew-alola",
    "Sandslash": "sandslash",
    "Sandslasha": "sandslash-alola",
    "Sandygast": "sandygast",
    "Sandyshock": "sandy-shocks",
    "Sawk": "sawk",
    "Sawsbuck": "sawsbuck",
    "Scatterbug": "scatterbug",
    "Scapegoat": "sceptile",
    "Sceptile": "sceptile",
    "Scepilerm": "sceptile-mega",
    "Scizor": "scizor",
    "Scizorm": "scizor-mega",
    "Scolipede": "scolipede",
    "Scorbunny": "scorbunny",
    "Scovillain": "scovillain",
    "Scrafty": "scrafty",
    "Scraggy": "scraggy",
    "Scyther": "scyther",
    "Seadra": "seadra",
    "Seaking": "seaking",
    "Sealeo": "sealeo",
    "Seedot": "seedot",
    "Seel": "seel",
    "Seismitoad": "seismitoad",
    "Sentret": "sentret",
    "Serperior": "serperior",
    "Servine": "servine",
    "Seviper": "seviper",
    "Sewaddle": "sewaddle",
    "Sharpedo": "sharpedo",
    "Sharpedom": "sharpedo-mega",
    "Shaymin": "shaymin",
    "Shaymins": "shaymin-sky",
    "Shelgon": "shelgon",
    "Shellder": "shellder",
    "Shellos": "shellos",
    "Shelmet": "shelmet",
    "Shieldon": "shieldon",
    "Shiftry": "shiftry",
    "Shiinotic": "shiinotic",
    "Shinx": "shinx",
    "Shroodle": "shroodle",
    "Shroomish": "shroomish",
    "Shuckle": "shuckle",
    "Shuppet": "shuppet",
    "Sigilyph": "sigilyph",
    "Silcoon": "silcoon",
    "Silicobra": "silicobra",
    "Silvally": "silvally",
    "Simipour": "simipour",
    "Simisage": "simisage",
    "Simisear": "simisear",
    "Sinistcha": "sinistcha",
    "Sinistea": "sinistea",
    "Sirfetch'd": "sirfetchd",
    "Sizzlipede": "sizzlipede",
    "Skarmory": "skarmory",
    "Skeledirge": "skeledirge",
    "Skiddo": "skiddo",
    "Skiploom": "skiploom",
    "Skitty": "skitty",
    "Skorupi": "skorupi",
    "Skrelp": "skrelp",
    "Skuntank": "skuntank",
    "Skwovet": "skwovet",
    "Slakoth": "slakoth",
    "Sliggoo": "sliggoo",
    "Sliggooh": "sliggoo-hisui",
    "Slowbro": "slowbro",
    "Slowbrog": "slowbro-galar",
    "Slowbrom": "slowbro-mega",
    "Slowking": "slowking",
    "Slowkingg": "slowking-galar",
    "Slowpoke": "slowpoke",
    "Slowpokeg": "slowpoke-galar",
    "Slugma": "slugma",
    "Slurpuff": "slurpuff",
    "Slithrwing": "slither-wing",
    "Smeargle": "smeargle",
    "Smoliv": "smoliv",
    "Smoochum": "smoochum",
    "Sneasel": "sneasel",
    "Sneaselh": "sneasel-hisui",
    "Sneasler": "sneasler",
    "Snivy": "snivy",
    "Snom": "snom",
    "Snorlax": "snorlax",
    "Snorunt": "snorunt",
    "Snover": "snover",
    "Snubbull": "snubbull",
    "Sobble": "sobble",
    "Solosis": "solosis",
    "Solrock": "solrock",
    "Spearow": "spearow",
    "Spectrier": "spectrier",
    "Spewpa": "spewpa",
    "Spheal": "spheal",
    "Spidops": "spidops",
    "Spinarak": "spinarak",
    "Spinda": "spinda",
    "Spiritomb": "spiritomb",
    "Spoink": "spoink",
    "Sprigatito": "sprigatito",
    "Spritzee": "spritzee",
    "Squirtle": "squirtle",
    "Stakataka": "stakataka",
    "Stantler": "stantler",
    "Staraptor": "staraptor",
    "Staravia": "staravia",
    "Starly": "starly",
    "Starmie": "starmie",
    "Staryu": "staryu",
    "Steelix": "steelix",
    "Steelixm": "steelix-mega",
    "Steenee": "steenee",
    "Stoutland": "stoutland",
    "Stufful": "stufful",
    "Stunfisk": "stunfisk",
    "Stunfiskg": "stunfisk-galar",
    "Stunky": "stunky",
    "Sudowoodo": "sudowoodo",
    "Suicune": "suicune",
    "Sunflora": "sunflora",
    "Sunkern": "sunkern",
    "Surskit": "surskit",
    "Swablu": "swablu",
    "Swadloon": "swadloon",
    "Swalot": "swalot",
    "Swampert": "swampert",
    "Swampertm": "swampert-mega",
    "Swanna": "swanna",
    "Swellow": "swellow",
    "Swinub": "swinub",
    "Swirlix": "swirlix",
    "Swoobat": "swoobat",
    "Sylveon": "sylveon",
    "Tadbulb": "tadbulb",
    "Taillow": "taillow",
    "Talonflame": "talonflame",
    "Tandemaus": "tandemaus",
    "Tangela": "tangela",
    "Tangrowth": "tangrowth",
    "Tapu Bulu": "tapu-bulu",
    "Tapu Fini": "tapu-fini",
    "Tapu Koko": "tapu-koko",
    "Tapu Lele": "tapu-lele",
    "Tarountula": "tarountula",
    "Tauros": "tauros",
    "Taurosp": "tauros-paldean",
    "Teddiursa": "teddiursa",
    "Tentacool": "tentacool",
    "Tentacruel": "tentacruel",
    "Tepig": "tepig",
    "Terapagos": "terapagos",
    "Terrakion": "terrakion",
    "Thievul": "thievul",
    "Throh": "throh",
    "Thundurus": "thundurus-therian",
    "Thundurust": "thundurus-therian",
    "Thwackey": "thwackey",
    "Timburr": "timburr",
    "Ting-Lu": "ting-lu",
    "Tinkatink": "tinkatink",
    "Tinkaton": "tinkaton",
    "Tinkatuff": "tinkatuff",
    "Tirtouga": "tirtouga",
    "Toedscool": "toedscool",
    "Toedscruel": "toedscruel",
    "Togedemaru": "togedemaru",
    "Togekiss": "togekiss",
    "Togepi": "togepi",
    "Togetic": "togetic",
    "Torchic": "torchic",
    "Torkoal": "torkoal",
    "Tornadus": "tornadus-therian",
    "Tornadust": "tornadus-therian",
    "Torracat": "torracat",
    "Torterra": "torterra",
    "Totodile": "totodile",
    "Toucannon": "toucannon",
    "Toxapex": "toxapex",
    "Toxel": "toxel",
    "Toxicroak": "toxicroak",
    "Toxtricity": "toxtricity",
    "Toxtricitl": "toxtricity-lowkey",
    "Tranquill": "tranquill",
    "Trapinch": "trapinch",
    "Treecko": "treecko",
    "Trevenant": "trevenant",
    "Tropius": "tropius",
    "Trubbish": "trubbish",
    "Trumbeak": "trumbeak",
    "Tsareena": "tsareena",
    "Turtonator": "turtonator",
    "Turtwig": "turtwig",
    "Tympole": "tympole",
    "Tynamo": "tynamo",
    "Type: Null": "type-null",
    "Typhlosion": "typhlosion",
    "Typhlosioh": "typhlosion-hisui",
    "Tyranitar": "tyranitar",
    "Tyranitarm": "tyranitar-mega",
    "Tyrantrum": "tyrantrum",
    "Tyrogue": "tyrogue",
    "Tyrunt": "tyrunt",
    "Umbreon": "umbreon",
    "Unfezant": "unfezant",
    "Unown": "unown",
    "Ursaluna": "ursaluna",
    "Ursaring": "ursaring",
    "Urshifu": "urshifu-rapid-strike",
    "Urshifur": "urshifu-rapid-strike",
    "Uxie": "uxie",
    "Vanillish": "vanillish",
    "Vanillite": "vanillite",
    "Vanilluxe": "vanilluxe",
    "Vaporeon": "vaporeon",
    "Varoom": "varoom",
    "Veluza": "veluza",
    "Venipede": "venipede",
    "Venomoth": "venomoth",
    "Venonat": "venonat",
    "Venusaur": "venusaur",
    "Venusaurm": "venusaur-mega",
    "Vespiquen": "vespiquen",
    "Vibrava": "vibrava",
    "Victini": "victini",
    "Victreebel": "victreebel",
    "Vigoroth": "vigoroth",
    "Vikavolt": "vikavolt",
    "Vileplume": "vileplume",
    "Virizion": "virizion",
    "Vivillon": "vivillon",
    "Volbeat": "volbeat",
    "Volcanion": "volcanion",
    "Volcarona": "volcarona",
    "Voltorb": "voltorb",
    "Voltorbh": "voltorb-hisui",
    "Vullaby": "vullaby",
    "Vulpix": "vulpix",
    "Vulpixa": "vulpix-alola",
    "Walkinwake": "walking-wake",
    "Wailmer": "wailmer",
    "Wailord": "wailord",
    "Walrein": "walrein",
    "Wartortle": "wartortle",
    "Watchog": "watchog",
    "Wattrel": "wattrel",
    "Weavile": "weavile",
    "Weedle": "weedle",
    "Weepinbell": "weepinbell",
    "Weezing": "weezing",
    "Weezingg": "weezing-galar",
    "Whimsicott": "whimsicott",
    "Whirlipede": "whirlipede",
    "Whiscash": "whiscash",
    "Whismur": "whismur",
    "Wigglytuff": "wigglytuff",
    "Wiglett": "wiglett",
    "Wimpod": "wimpod",
    "Wingull": "wingull",
    "Wo-Chien": "wo-chien",
    "Wobbuffet": "wobbuffet",
    "Woobat": "woobat",
    "Wooloo": "wooloo",
    "Wooper": "wooper",
    "Wormadams": "wormadam-sandy",
    "Wormadam": "wormadam",
    "Wormadamt": "wormadam-trash",
    "Wormadamt": "wormadam-trash",
    "Wugtrio": "wugtrio",
    "Wurmple": "wurmple",
    "Wynaut": "wynaut",
    "Wyrdeer": "wyrdeer",
    "Xatu": "xatu",
    "Xurkitree": "xurkitree",
    "Yamask": "yamask",
    "Yamaskg": "yamask-galar",
    "Yamper": "yamper",
    "Yanma": "yanma",
    "Yanmega": "yanmega",
    "Yungoos": "yungoos",
    "Zangoose": "zangoose",
    "Zapdos": "zapdos",
    "Zapdosg": "zapdos-galar",
    "Zarude": "zarude",
    "Zebstrika": "zebstrika",
    "Zeraora": "zeraora",
    "Zigzagoon": "zigzagoon",
    "Zigzagoong": "zigzagoon-galar",
    "Zoroark": "zoroark",
    "Zoroarkh": "zoroark-hisui",
    "Zorua": "zorua",
    "Zoruah": "zorua-hisui",
    "Zubat": "zubat",
    "Zweilous": "zweilous",
    "Zygarde": "zygarde",
    "Zygarde10": "zygarde-10",
}

# =========================
# NAME NORMALIZATION
# =========================

def normalize_name(name: str) -> str:
    if name in NAME_ALIASES:
        return NAME_ALIASES[name]

    n = name.lower().strip()
    n = n.replace("'", "").replace("'", "")
    n = n.replace(".", "").replace(":", "")
    n = n.replace(" ", "-")
    n = re.sub(r"-+", "-", n)
    return n

# =========================
# PARSE EVO FILE
# =========================

def parse_evo_file(path):
    pattern = re.compile(r"\(([^,]+),\s*(\d+)\)")
    data = {}

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if "->" not in line:
                continue

            starter, rest = line.split("->", 1)
            evos = []

            for evo, count in pattern.findall(rest):
                evos.append({
                    "name": evo.strip(),
                    "count": int(count)
                })

            data[starter.strip()] = evos

    return data

# =========================
# BUILD VANILLA FORWARD EVO SET
# =========================

def build_vanilla_forward_evolvers():
    print("Building vanilla forward evolution set...")
    forward = set()

    r = requests.get(f"{POKEAPI}/evolution-chain?limit=600")
    chains = r.json()["results"]

    for entry in chains:
        chain = requests.get(entry["url"]).json()["chain"]

        def walk(node):
            parent = node["species"]["name"]
            for nxt in node["evolves_to"]:
                child = nxt["species"]["name"]
                forward.add(parent)
                walk(nxt)

        walk(chain)

    print(f"Vanilla forward evolvers found: {len(forward)}")
    return forward

VANILLA_FORWARD_EVOLVERS = build_vanilla_forward_evolvers()

def has_forward_vanilla_evolution(name: str) -> bool:
    return normalize_name(name) in VANILLA_FORWARD_EVOLVERS

# =========================
# BST LOOKUP
# =========================

@lru_cache(maxsize=None)
def get_bst(name: str):
    STATS["bst_lookups"] += 1
    if STATS["bst_lookups"] % 50 == 0:
        print(f"[BST] {STATS['bst_lookups']} lookups")

    n = normalize_name(name)
    r = requests.get(f"{POKEAPI}/pokemon/{n}")
    if not r.ok:
        raise ValueError(f"BST lookup failed for {name} (normalized: {n})")

    return sum(s["base_stat"] for s in r.json()["stats"])

# =========================
# MAIN BUILD LOGIC
# =========================

def build_random_bst_evo_table():
    evo_data = parse_evo_file(EVO_FILE)
    result = {}

    total = len(evo_data)
    kept = 0
    start_time = time.time()

    for i, (starter, evos) in enumerate(evo_data.items(), 1):
        STATS["starters_seen"] += 1

        if i % 10 == 0 or i == total:
            elapsed = int(time.time() - start_time)
            print(f"[STARTERS] {i}/{total} | kept {kept} | {elapsed}s")

        # ---------- BASE BST ----------
        if starter in FORCED_STARTERS:
            base_bst = FORCED_STARTERS[starter]
        else:
            try:
                base_bst = get_bst(starter)
            except Exception as e:
                STATS["failed_starters"].append({
                    "name": starter,
                    "reason": str(e)
                })
                continue

        if base_bst > BST_LIMIT:
            continue

        if starter not in FORCED_STARTERS:
            if has_forward_vanilla_evolution(starter):
                continue

        # ---------- PROCESS EVOS ----------
        processed = []

        for evo in evos:
            try:
                evo_bst = get_bst(evo["name"])
                evo_entry = {
                    "evolution": evo["name"],
                    "bst": evo_bst,
                    "evolution_level": evo_bst // 10,
                    "probability": evo["count"] / TOTAL_RUNS
                }
                processed.append(evo_entry)
            except Exception as e:
                # SKIP failed evolutions instead of keeping null placeholders
                if starter not in STATS["failed_evolutions"]:
                    STATS["failed_evolutions"][starter] = []
                STATS["failed_evolutions"][starter].append({
                    "evolution": evo["name"],
                    "reason": str(e)
                })

        if not processed:
            continue

        processed.sort(
            key=lambda x: (x["bst"] is None, x["bst"] if x["bst"] is not None else 0)
        )

        result[starter] = {
            "base_bst": base_bst,
            "rule": "bst/10",
            "forced": starter in FORCED_STARTERS,
            "evolutions": processed
        }

        kept += 1
        STATS["starters_kept"] += 1

    print("\n===== SUMMARY =====")
    print(f"Starters seen:  {STATS['starters_seen']}")
    print(f"Starters kept: {STATS['starters_kept']}")
    print(f"BST lookups:   {STATS['bst_lookups']}")
    print(f"Failed starters: {len(STATS['failed_starters'])}")
    print(f"Time:          {int(time.time() - start_time)}s")
    print("===================\n")

    return result

# =========================
# ENTRY POINT
# =========================

if __name__ == "__main__":
    print("Building BST-based random evolution table...")
    data = build_random_bst_evo_table()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    # Save failure logs
    with open(FAILED_LOOKUPS_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "failed_starters": STATS["failed_starters"],
            "failed_evolutions_by_starter": STATS["failed_evolutions"],
            "total_failed_starters": len(STATS["failed_starters"]),
            "total_failed_evolution_forms": sum(len(v) for v in STATS["failed_evolutions"].values())
        }, f, indent=2)

    print(f"\nDone. Wrote {len(data)} Pokémon to {OUTPUT_FILE}")
    print(f"Failed lookups saved to {FAILED_LOOKUPS_FILE}")
