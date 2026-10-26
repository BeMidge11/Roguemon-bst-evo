import json, re

with open('species_data.json', 'r', encoding='utf-8') as f:
    sdata = {int(k): v for k, v in json.load(f).items()}

def to_sprite_slug(name):
    SPRITE_ALIASES = {
        "farfetch'd": "farfetchd", "sirfetch'd": "sirfetchd", "mr. mime": "mr-mime",
        "mr. rime": "mr-rime", "mime jr.": "mime-jr", "type: null": "type-null",
        "nidoran♀": "nidoran-m", "nidoran♂": "nidoran-f", "porygon-z": "porygon-z",
        "ursalunab": "ursaluna-bloodmoon", "maushold": "maushold", "dudunsprce": "dudunsparce",
        "pecharunt": "pecharunt"
    }

    slug = name.lower().trim() if hasattr(name, 'trim') else name.lower().strip()
    slug = re.sub(r'\s+', '', slug)
    slug = re.sub(r"[.'’:]", '', slug)
    slug = re.sub(r'\d+$', '', slug)

    if name.lower() in SPRITE_ALIASES: return SPRITE_ALIASES[name.lower()]
    if slug in SPRITE_ALIASES: return SPRITE_ALIASES[slug]

    if slug.startswith("taurosp"):
        if slug.endswith("w"): return "tauros-paldea-water"
        if slug.endswith("f"): return "tauros-paldea-fire"
        if slug.endswith("c"): return "tauros-paldea-combat"

    if slug.startswith("rotom") and len(slug) > 5:
        s = slug[5]
        m = {'w': 'wash', 'h': 'heat', 'f': 'frost', 'm': 'mow', 's': 'fan'}
        if s in m: return "rotom-" + m[s]

    if slug.endswith("f") and any(slug.startswith(b) for b in ["basclegio", "basculegio", "pyroar", "meowstic", "indeedee"]):
        return re.sub(r'f$', '-female', slug)
    if slug.endswith("t") and any(slug.startswith(b) for b in ["enamorus", "landorus", "thundurus", "tornadus"]):
        return re.sub(r't$', '-therian', slug)
    if slug.endswith("i") and any(slug.startswith(b) for b in ["enamorus", "landorus", "thundurus", "tornadus"]):
        return re.sub(r'i$', '-incarnate', slug)

    if slug.endswith('m') and len(slug) > 5:
        base = slug[:-1]
        megas = ["altaria", "mawile", "audino", "lucario", "garchomp", "salamence", "metagross", "tyranitar", "gyarados", "alakazam", "gengar", "gardevoir", "gallade", "lopunny", "medicham", "beedrill", "pidgeot", "sharpedo", "camerupt", "glalie", "heracross", "pinsir", "scizor", "houndoom", "manectric", "aerodactyl", "aggron", "steelix", "banette", "absol", "sableye", "ampharos", "slowbro"]
        for m in megas:
            if base.startswith(m): return m + "-mega"

    # Regional handlers
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

# Test some names from sdata
sample_names = ['Ponyta-G', 'Basculin-W', 'Growlithe-H', 'Wooper-P', 'Farfetch’d-G', 'Mr. Mime-G', 'Gengar-Mega', 'Dudunsparce', 'Flutter Mane']
for name in sample_names:
    print(f"'{name}' -> slug: '{to_sprite_slug(name)}'")
