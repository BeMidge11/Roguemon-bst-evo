import re

def to_sprite_slug_original(name):
    SPRITE_ALIASES = {
        "farfetch'd": "farfetchd", "sirfetch'd": "sirfetchd", "mr. mime": "mr-mime",
        "mr. rime": "mr-rime", "mime jr.": "mime-jr", "type: null": "type-null",
        "nidoran♀": "nidoran-m", "nidoran♂": "nidoran-f", "porygon-z": "porygon-z",
        "ursalunab": "ursaluna-bloodmoon", "maushold": "maushold", "dudunsprce": "dudunsparce",
        "pecharunt": "pecharunt"
    }

    slug = name.lower().strip().replace(" ", "").replace(".", "").replace("'", "").replace("’", "").replace(":", "")
    slug = re.sub(r"\d+$", "", slug)

    if name.lower() in SPRITE_ALIASES: return SPRITE_ALIASES[name.lower()]
    if slug in SPRITE_ALIASES: return SPRITE_ALIASES[slug]

    if slug.startswith("taurosp"):
        if slug.endswith("w"): return "tauros-paldea-water"
        if slug.endswith("f"): return "tauros-paldea-fire"
        if slug.endswith("c"): return "tauros-paldea-combat"

    if slug.endswith("f") and any(slug.startswith(b) for b in ["basclegio", "basculegio", "pyroar", "meowstic", "indeedee"]):
        return re.sub(r"f$", "-female", slug)

    # Regional Handlers in app.js:
    if slug.endswith('a'):
        b = slug[:-1]
        if b in ["raticate", "rattata", "raichu", "sandshrew", "sandslash", "vulpix", "ninetales", "diglett", "dugtrio", "meowth", "persian", "geodude", "graveler", "golem", "grimer", "muk", "exeggutor", "marowak"]:
            return b + "-alola"
    if slug.endswith('g'):
        b = slug[:-1]
        if b in ["meowth", "ponyta", "rapidash", "farfetchd", "weezing", "mrmime", "corsola", "zigzagoon", "linoone", "darumaka", "darmanitan", "yamask", "stunfisk", "slowpoke", "slowbro", "slowking", "articuno", "zapdos", "moltres"]:
            return b + "-galar"
    if slug.endswith('h'):
        b = slug[:-1]
        if b in ["growlithe", "arcanine", "voltorb", "electrode", "typhlosion", "qwilfish", "sneasel", "samurott", "lilligant", "basculin", "zorua", "zoroark", "braviary", "sliggoo", "goodra", "avalugg", "decidueye", "overqwil", "sneasler", "kleavor"]:
            return b + "-hisui"
    if slug.endswith('p'):
        b = slug[:-1]
        if b in ["wooper", "tauros"]:
            return b + "-paldea"

    return slug

test_forms = [
    'Ponyta-G', 'Corsola-G', 'Darumaka-G', 'Growlithe-H', 'Basculin-W', 'Wooper-P',
    'Diglett-A', 'Dugtrio-A', 'Eevee-P', 'Farfetch\'d-G', 'Geodude-A', 'Graveler-A',
    'Grimer-A', 'Linoone-G', 'Marowak-A', 'Meowth-A', 'Meowth-G', 'Mr. Mime-G',
    'Persian-A', 'Pikachu-P', 'Qwilfish-H', 'Raticate-A', 'Rattata-A', 'Rockruff-OT',
    'Sandshrew-A', 'Sandslash-A', 'Sliggoo-H', 'Slowpoke-G', 'Sneasel-H', 'Voltorb-H',
    'Vulpix-A', 'Wormadam-S', 'Wormadam-T', 'Yamask-G', 'Zigzagoon-G', 'Zorua-H'
]

for name in test_forms:
    res = to_sprite_slug_original(name)
    print(f"'{name}' -> '{res}'")
