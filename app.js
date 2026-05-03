let DATA = {};
let selectedPokemon = null;
let selectedPokemonName = null;
let selectedLevel = null;
let evoChart = null;
let typeChart = null;

fetch("random_bst_evolutions.json")
  .then(r => r.json())
  .then(d => DATA = d);

const input = document.getElementById("pokemonInput");
const suggestionsBox = document.getElementById("suggestions");
const levelsDiv = document.getElementById("levels");
const resultsDiv = document.getElementById("results");
const resultMeta = document.getElementById("resultMeta");
const starterInfoDiv = document.getElementById("starterInfo");
const currentLevelInput = document.getElementById("currentLevel");
const evoCtx = document.getElementById('evoChart').getContext('2d');
const typeCtx = document.getElementById('typeChart').getContext('2d');

// =========================
// SPRITE URL HELPERS
// =========================

/** Normalize a revo name to a PokeAPI sprite-compatible slug */
function toSpriteSlug(name) {
  const SPRITE_ALIASES = {
    "farfetch\u2019d": "farfetchd",
    "sirfetch\u2019d": "sirfetchd",
    "mr. mime": "mr-mime",
    "mr. mimeg": "mr-mime-galar",
    "mr. rime": "mr-rime",
    "mime jr.": "mime-jr",
    "type: null": "type-null",
    "nidoran\u2642": "nidoran-m",
    "nidoran\u2640": "nidoran-f",
    "great tusk": "great-tusk",
    "iron hands": "iron-hands",
    "iron moth": "iron-moth",
    "iron bundle": "iron-bundle",
    "iron crown": "iron-crown",
    "tapu koko": "tapu-koko",
    "tapu lele": "tapu-lele",
    "tapu bulu": "tapu-bulu",
    "tapu fini": "tapu-fini",
    "chi-yu": "chi-yu",
    "chien-pao": "chien-pao",
    "ting-lu": "ting-lu",
    "wo-chien": "wo-chien",
    "kommo-o": "kommo-o",
    "hakamo-o": "hakamo-o",
    "porygon-z": "porygon-z",
  };

  let slug = name.toLowerCase().trim()
    .replace(/\s+/g, "-")
    .replace(/[.''\u2019:]/g, "")
    .replace(/\d+$/, "");

  if (SPRITE_ALIASES[name.toLowerCase()]) return SPRITE_ALIASES[name.toLowerCase()];
  if (SPRITE_ALIASES[slug]) return SPRITE_ALIASES[slug];

  // Regional suffix mapping
  const REGIONAL_MAP = {
    h: "-hisui", g: "-galar", p: "-paldea", a: "-alola",
    w: "-water", f: "-female",
  };

  // Known multi-form slugs
  const FORM_SLUGS = {
    "castformf": "castform-sunny", "castformw": "castform-rainy", "castformi": "castform-snowy",
    "eeveep": "eevee", "pikachup": "pikachu", "pikachuc": "pikachu",
    "pichus": "pichu", "burmys": "burmy", "burmyt": "burmy",
    "floettee": "floette", "cherrims": "cherrim",
    "miniorc": "minior-red-meteor", "minior": "minior-red-meteor",
    "morpekoh": "morpeko-hangry", "morpeko": "morpeko-full-belly",
    "terapagost": "terapagos-terastal",
    "squawkbily": "squawkabilly", "dudunsprce": "dudunsparce",
    "fluttrmane": "flutter-mane", "ironbundle": "iron-bundle",
    "ironjuglis": "iron-jugulis", "ironleaves": "iron-leaves",
    "ironthorns": "iron-thorns", "irontreads": "iron-treads",
    "ironvalian": "iron-valiant", "ironbouldr": "iron-boulder",
    "roarinmoon": "roaring-moon", "walkinwake": "walking-wake",
    "sandyshock": "sandy-shocks", "screamtail": "scream-tail",
    "slithrwing": "slither-wing", "brutebonet": "brute-bonnet",
    "ragingbolt": "raging-bolt",
    "corvknight": "corviknight", "baraskewda": "barraskewda",
    "kilowattrl": "kilowattrel", "fezandipti": "fezandipiti",
    "crabminble": "crabominable", "centskorch": "centiskorch",
    "poltegeist": "polteageist", "stonjorner": "stonjourner",
    "bramblgast": "brambleghast", "meowscrada": "meowscarada",
    "blacphalon": "blacephalon",
    "toxtricitl": "toxtricity-low-key",
    "taurospw": "tauros-paldea-aqua-breed",
    "taurosp": "tauros-paldea-combat-breed",
    "taurospf": "tauros-paldea-blaze-breed",
    "basclegion": "basculegion-male", "basclegiof": "basculegion-female",
    "indeedeef": "indeedee-female", "indeedeem": "indeedee-male",
    "oinkolognf": "oinkologne-female", "oinkologne": "oinkologne-male",
    "meloettap": "meloetta-pirouette", "meloetta": "meloetta-aria",
    "oricoriog": "oricorio-sensu", "oricorioe": "oricorio-pom-pom",
    "oricoriop": "oricorio-pau", "oricorio": "oricorio-baile",
    "ursalunab": "ursaluna-bloodmoon",
    "urshifur": "urshifu-rapid-strike", "urshifu": "urshifu-single-strike",
    "rotomw": "rotom-wash", "rotomh": "rotom-heat", "rotomfa": "rotom-fan",
    "rotomfr": "rotom-frost", "rotomm": "rotom-mow",
    "mimikyu": "mimikyu-disguised", "maushold": "maushold-family-of-four",
    "toxtricity": "toxtricity-amped", "tatsugiri": "tatsugiri-curly",
    "basculinb": "basculin-blue-striped", "basculinw": "basculin-white-striped",
    "basculin": "basculin-red-striped",
    "aegislash": "aegislash-shield", "aegislashb": "aegislash-blade",
    "darmanitan": "darmanitan-standard",
    "darmanitag": "darmanitan-galar-standard",
    "darmanitaz": "darmanitan-zen", "darmanitzg": "darmanitan-galar-zen",
    "lycanroc": "lycanroc-midday", "lycanrocd": "lycanroc-dusk", "lycanrocm": "lycanroc-midnight",
    "zygarde": "zygarde-50", "zygarde10": "zygarde-10",
    "gourgeist": "gourgeist-average", "gourgeistl": "gourgeist-large",
    "gourgeists": "gourgeist-small", "gourgeistx": "gourgeist-super",
    "pumpkaboo": "pumpkaboo-average",
    "eiscuen": "eiscue-noice", "eiscue": "eiscue-ice",
    "wishiwashi": "wishiwashi-solo",
    "wormadam": "wormadam-plant", "wormadams": "wormadam-sandy", "wormadamt": "wormadam-trash",
    "palafin": "palafin-zero",
    "landorust": "landorus-therian", "thundurust": "thundurus-therian",
    "tornadust": "tornadus-therian", "enamorust": "enamorus-therian",
    "shaymin": "shaymin-land", "shaymins": "shaymin-sky",
    "keldeo": "keldeo-ordinary",
    "pyroar": "pyroar",
    "ogerponr": "ogerpon-hearthflame-mask", "ogerponw": "ogerpon-wellspring-mask",
    "ogerponf": "ogerpon-hearthflame-mask",
    "kangaskham": "kangaskhan-mega",
    "lopunnym": "lopunny-mega", "pidgeotm": "pidgeot-mega", "audinom": "audino-mega",
    "absolm": "absol-mega", "alakazamm": "alakazam-mega", "altariam": "altaria-mega",
    "ampharosm": "ampharos-mega", "sableyem": "sableye-mega", "mawilem": "mawile-mega",
    "gengarm": "gengar-mega", "glaliem": "glalie-mega", "heracrossm": "heracross-mega",
    "houndoomm": "houndoom-mega", "manectricm": "manectric-mega",
    "medichamm": "medicham-mega", "sharpedom": "sharpedo-mega", "scizorm": "scizor-mega",
    "cameruptm": "camerupt-mega", "slowbrom": "slowbro-mega", "steelixm": "steelix-mega",
    "beedrillm": "beedrill-mega", "blastoisem": "blastoise-mega",
    "venusaurm": "venusaur-mega", "pinsirm": "pinsir-mega",
    "abomasnowm": "abomasnow-mega", "salamencem": "salamence-mega",
    "metagrossm": "metagross-mega", "tyranitarm": "tyranitar-mega",
    "banettem": "banette-mega", "aerodactylm": "aerodactyl-mega",
    "aggronm": "aggron-mega", "gardevoirm": "gardevoir-mega",
    "charizardm": "charizard-mega-x", "charizardy": "charizard-mega-y",
    "scepilerm": "sceptile-mega", "swampertm": "swampert-mega",
    "galatiam": "gallade-mega",
    "raichua": "raichu-alola", "golema": "golem-alola",
    "exeggutora": "exeggutor-alola",
    "marowaka": "marowak-alola",
    "muka": "muk-alola", "persiana": "persian-alola",
    "ninetalesa": "ninetales-alola",
    "sandslasha": "sandslash-alola",
    "raticatea": "raticate-alola",
    "slowbrog": "slowbro-galar", "slowkingg": "slowking-galar",
    "weezingg": "weezing-galar", "stunfiskg": "stunfisk-galar",
    "rapidashg": "rapidash-galar",
    "articunog": "articuno-galar", "zapdosg": "zapdos-galar", "moltresg": "moltres-galar",
    "goodrah": "goodra-hisui", "braviaryh": "braviary-hisui",
    "decidueyeh": "decidueye-hisui", "lilliganth": "lilligant-hisui",
    "typhlosioh": "typhlosion-hisui", "samurotth": "samurott-hisui",
    "avaluggh": "avalugg-hisui", "electrodeh": "electrode-hisui",
    "zoroarkh": "zoroark-hisui",
    "flab\u00e9b\u00e9": "flabebe", "flabebe": "flabebe",
    "gouginfire": "gouging-fire",
    "frillish": "frillish",
    "jellicent": "jellicent",
  };

  if (FORM_SLUGS[slug]) return FORM_SLUGS[slug];

  return slug;
}

function getSpriteUrl(name) {
  const slug = toSpriteSlug(name);
  return `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${getPokedexNumber(slug) || slug}.png`;
}

/** Attempt to get sprite by slug — fallback to name-based URL */
function getSpriteUrlBySlug(slug) {
  return `https://img.pokemondb.net/sprites/home/normal/${slug}.png`;
}

function getPokedexNumber(slug) {
  // We don't have a dex number lookup, so use slug-based URLs
  return null;
}

/** Get a working sprite URL with fallback chain */
function buildSpriteUrl(name) {
  const slug = toSpriteSlug(name);
  // PokemonDB has the most reliable sprite coverage for all forms
  return `https://img.pokemondb.net/sprites/home/normal/${slug}.png`;
}

// =========================
// TYPE BADGE HELPER
// =========================

function typeBadgeHTML(typeName) {
  const cls = `type-${typeName.toLowerCase()}`;
  return `<span class="type-badge ${cls}">${typeName}</span>`;
}

// =========================
// CHARTS
// =========================

function initCharts() {
  evoChart = new Chart(evoCtx, {
    type: 'line',
    data: {
      labels: [],
      datasets: [{
        label: 'Evolution Frequency',
        data: [],
        borderColor: '#38bdf8',
        backgroundColor: 'rgba(56, 189, 248, 0.08)',
        fill: true,
        tension: 0.4,
        pointRadius: 3,
        pointBackgroundColor: '#38bdf8',
        pointHoverRadius: 5,
        borderWidth: 2,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#1e293b',
          borderColor: '#334155',
          borderWidth: 1,
          titleColor: '#e5e7eb',
          bodyColor: '#9ca3af',
          callbacks: {
            label: (ctx) => `Probability: ${ctx.raw.toFixed(2)}%`
          }
        }
      },
      scales: {
        x: {
          display: true,
          title: { display: true, text: 'Level', color: '#64748b', font: { size: 10, weight: '500' } },
          grid: { color: '#1e293b' },
          ticks: { color: '#64748b', font: { size: 9 } }
        },
        y: {
          display: false,
          beginAtZero: true
        }
      }
    }
  });

  typeChart = new Chart(typeCtx, {
    type: 'bar',
    data: {
      labels: [],
      datasets: [{
        data: [],
        backgroundColor: [
          '#38bdf8', '#a78bfa', '#f472b6', '#34d399', '#fbbf24',
          '#fb923c', '#f87171', '#60a5fa', '#c084fc', '#2dd4bf'
        ],
        borderRadius: 5,
        borderSkipped: false,
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#1e293b',
          borderColor: '#334155',
          borderWidth: 1,
          titleColor: '#e5e7eb',
          bodyColor: '#9ca3af',
          callbacks: {
            label: (ctx) => `Probability: ${ctx.raw.toFixed(2)}%`
          }
        }
      },
      scales: {
        x: {
          display: true,
          title: { display: true, text: 'Probability (%)', color: '#64748b', font: { size: 10, weight: '500' } },
          grid: { color: '#1e293b' },
          ticks: { color: '#64748b', font: { size: 9 } },
          beginAtZero: true,
          max: 100
        },
        y: {
          grid: { display: false },
          ticks: { color: '#e5e7eb', font: { size: 10 } }
        }
      }
    }
  });
}

// =========================
// SEARCH / SELECT
// =========================

input.addEventListener("input", () => {
  const q = input.value.toLowerCase();
  suggestionsBox.innerHTML = "";

  if (!q) {
    suggestionsBox.hidden = true;
    return;
  }

  const matches = Object.keys(DATA)
    .filter(n => n.toLowerCase().startsWith(q))
    .slice(0, 20);

  for (const name of matches) {
    const div = document.createElement("div");
    div.className = "suggestion";
    div.textContent = name;
    div.onclick = () => selectPokemon(name);
    suggestionsBox.appendChild(div);
  }

  suggestionsBox.hidden = matches.length === 0;
});

function selectPokemon(name) {
  input.value = name;
  suggestionsBox.hidden = true;
  selectedPokemon = DATA[name];
  selectedPokemonName = name;
  selectedLevel = null;
  render();
}

currentLevelInput.addEventListener("input", render);

// =========================
// RENDER
// =========================

function getValidEvos() {
  const lvl = parseInt(currentLevelInput.value) || 1;
  return selectedPokemon.evolutions.filter(e => e.evolution_level > lvl);
}

function render() {
  if (!selectedPokemon) return;
  if (!evoChart) initCharts();

  const lvl = parseInt(currentLevelInput.value) || 1;
  const valid = getValidEvos();
  const totalProb = valid.reduce((s, e) => s + e.probability, 0);

  // ===== STARTER INFO =====
  const spriteUrl = buildSpriteUrl(selectedPokemonName);
  starterInfoDiv.innerHTML = `
    <div class="starter-info">
      <img src="${spriteUrl}" alt="${selectedPokemonName}"
           onerror="this.style.display='none'">
      <div class="starter-details">
        <div class="starter-name">${selectedPokemonName}</div>
        <div class="starter-bst">
          Base BST: <span>${selectedPokemon.base_bst}</span>
          &nbsp;·&nbsp; Evo rule: BST/10
        </div>
      </div>
    </div>
  `;

  // ===== LEVEL PILLS =====
  levelsDiv.innerHTML = "";
  const uniqueLevels = [...new Set(selectedPokemon.evolutions.map(e => e.evolution_level))]
    .sort((a, b) => a - b);

  for (const l of uniqueLevels) {
    const pill = document.createElement("div");
    pill.className = "level-pill";
    pill.textContent = l;

    if (l <= lvl) pill.classList.add("disabled");
    if (l === selectedLevel) pill.classList.add("active");

    pill.onclick = () => {
      selectedLevel = (selectedLevel === l) ? null : l;
      render();
    };

    levelsDiv.appendChild(pill);
  }

  // ===== RESULTS =====
  resultsDiv.innerHTML = "";

  let filtered = selectedLevel
    ? valid.filter(e => e.evolution_level === selectedLevel)
    : valid;

  filtered = [...filtered].sort((a, b) => b.probability - a.probability);

  // Result meta
  resultMeta.hidden = false;
  resultMeta.innerHTML = `
    <span><strong>${filtered.length}</strong> possible evolution${filtered.length !== 1 ? 's' : ''}${selectedLevel ? ` at level ${selectedLevel}` : ''}</span>
    <span>${valid.length} total above level ${lvl}</span>
  `;

  for (const evo of filtered) {
    const p = totalProb > 0 ? evo.probability / totalProb : 0;
    const types = evo.types || ["Normal"];
    const typeBadges = types.map(t => typeBadgeHTML(t)).join("");
    const sprite = buildSpriteUrl(evo.evolution);

    const card = document.createElement("div");
    card.className = "evo-card";

    card.innerHTML = `
      <img class="evo-sprite" src="${sprite}" alt="${evo.evolution}"
           onerror="this.style.opacity='0.15'">
      <div class="evo-name-col">
        <div class="evo-name">${evo.evolution}</div>
        <div class="evo-types">${typeBadges}</div>
      </div>
      <div class="evo-bst">BST <span>${evo.bst}</span></div>
      <div class="evo-level">${evo.evolution_level}</div>
      <div class="bar-col">
        <div class="bar">
          <div class="bar-fill" style="width:${(p * 100).toFixed(2)}%"></div>
        </div>
        <span class="percent">${(p * 100).toFixed(2)}%</span>
      </div>
    `;

    resultsDiv.appendChild(card);
  }

  updateCharts(valid, totalProb);
}

// =========================
// CHARTS UPDATE
// =========================

function updateCharts(valid, totalProb) {
  // 1. LEVEL DISTRIBUTION
  const levelDist = {};
  valid.forEach(e => {
    levelDist[e.evolution_level] = (levelDist[e.evolution_level] || 0) + (e.probability / totalProb);
  });

  const levels = Object.keys(levelDist).map(Number).sort((a, b) => a - b);
  const levelData = levels.map(l => levelDist[l] * 100);

  evoChart.data.labels = levels;
  evoChart.data.datasets[0].data = levelData;
  evoChart.update();

  // 2. TYPE DISTRIBUTION
  const typeDist = {};
  valid.forEach(e => {
    const typeCombo = (e.types || ["Unknown"]).join("/");
    typeDist[typeCombo] = (typeDist[typeCombo] || 0) + (e.probability / totalProb);
  });

  const sortedTypes = Object.entries(typeDist)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10); // Show top 10 combos

  typeChart.data.labels = sortedTypes.map(t => t[0]);
  typeChart.data.datasets[0].data = sortedTypes.map(t => t[1] * 100);
  typeChart.update();
}
