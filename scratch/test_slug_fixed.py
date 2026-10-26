import re

def to_sprite_slug_fixed(name):
    SPRITE_ALIASES = {
        "farfetch'd": "farfetchd", "sirfetch'd": "sirfetchd", "mr. mime": "mr-mime",
        "mr. rime": "mr-rime", "mime jr.": "mime-jr", "type: null": "type-null",
        "nidoran♀": "nidoran-f", "nidoran♂": "nidoran-m", "nidoran-f": "nidoran-f", "nidoran-m": "nidoran-m",
        "porygon-z": "porygon-z", "ursalunab": "ursaluna-bloodmoon", "maushold": "maushold",
        "dudunsprce": "dudunsparce", "pecharunt": "pecharunt", "basculin-w": "basculin-whitestriped",
        "wormadam-s": "wormadam-sandy", "wormadam-t": "wormadam-trash", "rockruff-ot": "rockruff",
        "eevee-p": "eevee-starter", "pikachu-p": "pikachu-starter", "tauros-p": "tauros-paldea",
        "flabébé": "flabebe"
    }

    raw_lower = name.lower().strip()
    if raw_lower in SPRITE_ALIASES: return SPRITE_ALIASES[raw_lower]

    slug = raw_lower.replace(" ", "").replace(".", "").replace("'", "").replace("’", "").replace(":", "")
    slug = re.sub(r"\d+$", "", slug)

    if slug in SPRITE_ALIASES: return SPRITE_ALIASES[slug]

    # Paldean Tauros
    if slug.startswith("taurosp") or slug.startswith("tauros-p"):
        if slug.endswith("w"): return "tauros-paldea-water"
        if slug.endswith("f"): return "tauros-paldea-fire"
        if slug.endswith("c"): return "tauros-paldea-combat"
        return "tauros-paldea"

    # Rotom forms
    if slug.startswith("rotom") and len(slug) > 5:
        sub = slug.replace("rotom-", "").replace("rotom", "")
        m = {'w': 'wash', 'h': 'heat', 'f': 'frost', 'm': 'mow', 's': 'fan'}
        if sub and sub[0] in m: return "rotom-" + m[sub[0]]

    # Gender & Form forms
    if re.search(r"-?f$", slug) and any(slug.startswith(b) for b in ["basclegio", "basculegio", "pyroar", "meowstic", "indeedee", "oinkologne"]):
        return re.sub(r"-?f$", "-female", slug)
    if re.search(r"-?m$", slug) and any(slug.startswith(b) for b in ["basclegio", "basculegio", "meowstic", "indeedee"]):
        return re.sub(r"-?m$", "", slug)
    if re.search(r"-?t$", slug) and any(slug.startswith(b) for b in ["enamorus", "landorus", "thundurus", "tornadus"]):
        return re.sub(r"-?t$", "-therian", slug)
    if re.search(r"-?i$", slug) and any(slug.startswith(b) for b in ["enamorus", "landorus", "thundurus", "tornadus"]):
        return re.sub(r"-?i$", "-incarnate", slug)

    # Mega
    if (slug.endswith("-mega") or slug.endswith("mega")):
        return slug
    if (slug.endswith('m') or slug.endswith('-m')) and len(slug) > 5:
        base = re.sub(r"-?m$", "", slug)
        megas = ["altaria", "mawile", "audino", "lucario", "garchomp", "salamence", "metagross", "tyranitar", "gyarados", "alakazam", "gengar", "gardevoir", "gallade", "lopunny", "medicham", "beedrill", "pidgeot", "sharpedo", "camerupt", "glalie", "heracross", "pinsir", "scizor", "houndoom", "manectric", "aerodactyl", "aggron", "steelix", "banette", "absol", "sableye", "ampharos", "slowbro"]
        for mg in megas:
            if base.startswith(mg): return mg + "-mega"

    # Regional Handlers: -a, -g, -h, -p (with or without hyphen)
    if re.search(r"-?a$", slug):
        b = re.sub(r"-?a$", "", slug)
        if b in ["raticate", "rattata", "raichu", "sandshrew", "sandslash", "vulpix", "ninetales", "diglett", "dugtrio", "meowth", "persian", "geodude", "graveler", "golem", "grimer", "muk", "exeggutor", "marowak"]:
            return b + "-alola"
    if re.search(r"-?g$", slug):
        b = re.sub(r"-?g$", "", slug)
        if b in ["meowth", "ponyta", "rapidash", "farfetchd", "weezing", "mrmime", "corsola", "zigzagoon", "linoone", "darumaka", "darmanitan", "yamask", "stunfisk", "slowpoke", "slowbro", "slowking", "articuno", "zapdos", "moltres"]:
            return ("mr-mime" if b == "mrmime" else b) + "-galar"
    if re.search(r"-?h$", slug):
        b = re.sub(r"-?h$", "", slug)
        if b in ["growlithe", "arcanine", "voltorb", "electrode", "typhlosion", "qwilfish", "sneasel", "samurott", "lilligant", "basculin", "zorua", "zoroark", "braviary", "sliggoo", "goodra", "avalugg", "decidueye", "overqwil", "sneasler", "kleavor"]:
            return b + "-hisui"
    if re.search(r"-?p$", slug):
        b = re.sub(r"-?p$", "", slug)
        if b in ["wooper", "tauros"]:
            return b + "-paldea"

    return slug

test_forms = [
    'Ponyta-G', 'Corsola-G', 'Darumaka-G', 'Growlithe-H', 'Basculin-W', 'Wooper-P',
    'Diglett-A', 'Dugtrio-A', 'Eevee-P', 'Farfetch\'d-G', 'Geodude-A', 'Graveler-A',
    'Grimer-A', 'Linoone-G', 'Marowak-A', 'Meowth-A', 'Meowth-G', 'Mr. Mime-G',
    'Persian-A', 'Pikachu-P', 'Qwilfish-H', 'Raticate-A', 'Rattata-A', 'Rockruff-OT',
    'Sandshrew-A', 'Sandslash-A', 'Sliggoo-H', 'Slowpoke-G', 'Sneasel-H', 'Voltorb-H',
    'Vulpix-A', 'Wormadam-S', 'Wormadam-T', 'Yamask-G', 'Zigzagoon-G', 'Zorua-H',
    'Gengar-Mega', 'Gengarm', 'Flabébé', 'Nidoran-F', 'Nidoran-M'
]

for name in test_forms:
    res = to_sprite_slug_fixed(name)
    print(f"'{name}' -> '{res}'")
