const TYPE_COLORS = {
  normal: '#9fa19f', fire: '#e62829', water: '#2980ef', electric: '#fac000',
  grass: '#3fa129', ice: '#3dcef3', fighting: '#ff8000', poison: '#9141cb',
  ground: '#915121', flying: '#81b9ef', psychic: '#ef4179', bug: '#91a119',
  rock: '#afa981', ghost: '#704170', dragon: '#5060e1', dark: '#624d4e',
  steel: '#60a1b8', fairy: '#ef70ef', unknown: '#475569'
};

function blendColors(color1, color2) {
  const hex = (c) => parseInt(c, 16);
  const r1 = hex(color1.slice(1, 3)), g1 = hex(color1.slice(3, 5)), b1 = hex(color1.slice(5, 7));
  const r2 = hex(color2.slice(1, 3)), g2 = hex(color2.slice(3, 5)), b2 = hex(color2.slice(5, 7));
  const r = Math.round((r1 + r2) / 2).toString(16).padStart(2, '0');
  const g = Math.round((g1 + g2) / 2).toString(16).padStart(2, '0');
  const b = Math.round((b1 + b2) / 2).toString(16).padStart(2, '0');
  return `#${r}${g}${b}`;
}

function getTypeColor(typeCombo) {
  const types = typeCombo.toLowerCase().split('/');
  if (types.length === 1) return TYPE_COLORS[types[0]] || TYPE_COLORS.unknown;
  const c1 = TYPE_COLORS[types[0]] || TYPE_COLORS.unknown;
  const c2 = TYPE_COLORS[types[1]] || TYPE_COLORS.unknown;
  return blendColors(c1, c2);
}

let DATA = {};
let selectedPokemon = null;
let selectedPokemonName = null;
let selectedLevel = null;

let evoChart = null;
let typeChart = null;

fetch("random_bst_evolutions.json")
  .then(r => r.json())
  .then(data => {
    DATA = data;
  });

const input = document.getElementById("pokemonInput");
const suggestionsBox = document.getElementById("suggestions");
const levelsDiv = document.getElementById("levels");
const resultsDiv = document.getElementById("results");
const resultMeta = document.getElementById("resultMeta");
const starterInfoDiv = document.getElementById("starterInfo");
const currentLevelInput = document.getElementById("currentLevel");

const evoCtx = document.getElementById('evoChart').getContext('2d');
const typeCtx = document.getElementById('typeChart').getContext('2d');

function getBstColor(bst) {
  if (bst <= 450) return 'rgb(74, 222, 128)';
  if (bst < 500) {
    const ratio = (bst - 451) / (500 - 451);
    return `hsl(${ratio * 35}, 85%, 50%)`;
  }
  const ratio = Math.min((bst - 500) / 150, 1);
  return `hsl(${70 + (ratio * 50)}, 80%, 45%)`;
}

function toSpriteSlug(name) {
  const SPRITE_ALIASES = {
    "farfetch\u2019d": "farfetchd", "sirfetch\u2019d": "sirfetchd", "mr. mime": "mr-mime",
    "mr. rime": "mr-rime", "mime jr.": "mime-jr", "type: null": "type-null",
    "nidoran\u2642": "nidoran-m", "nidoran\u2640": "nidoran-f", "porygon-z": "porygon-z",
    "ursalunab": "ursaluna-bloodmoon", "maushold": "maushold", "dudunsprce": "dudunsparce",
    "pecharunt": "pecharunt"
  };

  let slug = name.toLowerCase().trim().replace(/\s+/g, "").replace(/[.''\u2019:]/g, "").replace(/\d+$/, "");

  if (SPRITE_ALIASES[name.toLowerCase()]) return SPRITE_ALIASES[name.toLowerCase()];
  if (SPRITE_ALIASES[slug]) return SPRITE_ALIASES[slug];

  // Robust Suffix Engine for ROM names
  if (slug.startsWith("taurosp")) {
    if (slug.endsWith("w")) return "tauros-paldea-water";
    if (slug.endsWith("f")) return "tauros-paldea-fire";
    if (slug.endsWith("c")) return "tauros-paldea-combat";
  }
  if (slug.startsWith("rotom") && slug.length > 5) {
    const s = slug.charAt(5);
    const m = { 'w': 'wash', 'h': 'heat', 'f': 'frost', 'm': 'mow', 's': 'fan' };
    if (m[s]) return "rotom-" + m[s];
  }
  if (slug.endsWith("f") && ["basclegio", "basculegio", "pyroar", "meowstic", "indeedee"].some(b => slug.startsWith(b))) return slug.replace(/f$/, "") + "-female";
  if (slug.endsWith("t") && ["enamorus", "landorus", "thundurus", "tornadus"].some(b => slug.startsWith(b))) return slug.replace(/t$/, "") + "-therian";
  if (slug.endsWith("i") && ["enamorus", "landorus", "thundurus", "tornadus"].some(b => slug.startsWith(b))) return slug.replace(/i$/, "") + "-incarnate";

  if (slug.endsWith('m') && slug.length > 5) {
    const base = slug.slice(0, -1);
    const megas = ["altaria", "mawile", "audino", "lucario", "garchomp", "salamence", "metagross", "tyranitar", "gyarados", "alakazam", "gengar", "gardevoir", "gallade", "lopunny", "medicham", "beedrill", "pidgeot", "sharpedo", "camerupt", "glalie", "heracross", "pinsir", "scizor", "houndoom", "manectric", "aerodactyl", "aggron", "steelix", "banette", "absol", "sableye", "ampharos", "slowbro"];
    const match = megas.find(m => base.startsWith(m));
    if (match) return match + "-mega";
  }

  const fixes = {
    "ironvalian": "ironvaliant", "fluttrmane": "fluttermane", "ironjuglis": "ironjugulis",
    "roarinmoon": "roaringmoon", "walkinwake": "walkingwake", "ragingbolt": "ragingbolt",
    "gouginfire": "gougingfire", "ironbouldr": "ironboulder", "fezandipti": "fezandipiti"
  };
  for (const [short, full] of Object.entries(fixes)) if (slug.startsWith(short)) return full;

  // Regional Handlers
  if (slug.endsWith('a')) {
    const b = slug.slice(0, -1);
    if (["raticate", "rattata", "raichu", "sandshrew", "sandslash", "vulpix", "ninetales", "diglett", "dugtrio", "meowth", "persian", "geodude", "graveler", "golem", "grimer", "muk", "exeggutor", "marowak"].includes(b)) return b + "-alola";
  }
  if (slug.endsWith('g')) {
    const b = slug.slice(0, -1);
    if (["meowth", "ponyta", "rapidash", "farfetchd", "weezing", "mrmime", "corsola", "zigzagoon", "linoone", "darumaka", "darmanitan", "yamask", "stunfisk", "slowpoke", "slowbro", "slowking", "articuno", "zapdos", "moltres"].includes(b)) return b + "-galar";
  }
  if (slug.endsWith('h')) {
    const b = slug.slice(0, -1);
    if (["growlithe", "arcanine", "voltorb", "electrode", "typhlosion", "qwilfish", "sneasel", "samurott", "lilligant", "basculin", "zorua", "zoroark", "braviary", "sliggoo", "goodra", "avalugg", "decidueye", "overqwil", "sneasler", "kleavor"].includes(b)) return b + "-hisui";
  }
  if (slug.endsWith('p')) {
    const b = slug.slice(0, -1);
    if (["wooper", "tauros"].includes(b)) return b + "-paldea";
  }

  return slug;
}

function buildSpriteUrl(name) {
  return `https://play.pokemonshowdown.com/sprites/ani/${toSpriteSlug(name)}.gif`;
}

function typeBadgeHTML(typeName) {
  return `<span class="type-badge type-${typeName.toLowerCase()}">${typeName}</span>`;
}

function initCharts() {
  evoChart = new Chart(evoCtx, {
    type: 'line',
    data: { labels: [], datasets: [{ label: 'Evolution Frequency', data: [], borderColor: '#38bdf8', backgroundColor: 'rgba(56, 189, 248, 0.08)', fill: true, tension: 0.4 }] },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: { display: false }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: { color: '#64748b' },
          grid: { color: '#1e293b' }
        },
        x: {
          ticks: { color: '#64748b' },
          grid: { color: '#1e293b' }
        }
      }
    }
  });
  typeChart = new Chart(typeCtx, {
    type: 'doughnut',
    data: { labels: [], datasets: [{ data: [], backgroundColor: [] }] },
    options: { responsive: true, cutout: '65%', plugins: { legend: { display: false } } }
  });
}

input.addEventListener("input", () => {
  const q = input.value.toLowerCase().trim();
  suggestionsBox.innerHTML = "";
  if (!q) { suggestionsBox.hidden = true; return; }

  const blacklist = ["frillish", "sneasel", "pumpkaboo"];
  const matches = Object.keys(DATA)
    .filter(name => {
      const entry = DATA[name];
      const isBlacklisted = blacklist.some(b => name.toLowerCase().includes(b));
      return name.toLowerCase().startsWith(q) && entry.base_bst <= 450 && !entry.forced && !isBlacklisted;
    })
    .slice(0, 20);

  if (matches.length > 0) {
    suggestionsBox.innerHTML = matches.map(name => `
      <div class="suggestion-item" onclick="selectPokemon('${name.replace(/'/g, "\\'")}')">
        <span>${name}</span>
        <span class="bst-badge">${DATA[name].base_bst} BST</span>
      </div>
    `).join("");
    suggestionsBox.hidden = false;
  } else {
    suggestionsBox.hidden = true;
  }
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

function render() {
  if (!selectedPokemon) return;
  if (!evoChart) initCharts();

  const lvl = parseInt(currentLevelInput.value) || 1;
  const valid = selectedPokemon.evolutions.filter(e => e.evolution_level > lvl);
  const totalProb = valid.reduce((s, e) => s + e.probability, 0);

  const starterSlug = toSpriteSlug(selectedPokemonName);
  starterInfoDiv.innerHTML = `
    <div class="starter-info">
      <img src="${buildSpriteUrl(selectedPokemonName)}" alt="${selectedPokemonName}"
           onerror="
             if(this.src.includes('ani')) this.src='https://play.pokemonshowdown.com/sprites/gen9/${starterSlug}.png';
             else if(this.src.includes('gen9')) this.src='https://play.pokemonshowdown.com/sprites/dex/${starterSlug}.png';
             else if(this.src.includes('dex')) this.src='https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${starterSlug}.png';
           ">
      <div class="starter-details">
        <div class="starter-name">${selectedPokemonName}</div>
        <div class="starter-bst">Base BST: <span>${selectedPokemon.base_bst}</span></div>
      </div>
    </div>
  `;

  levelsDiv.innerHTML = "";
  const uniqueLevels = [...new Set(selectedPokemon.evolutions.map(e => e.evolution_level))].sort((a, b) => a - b);
  for (const l of uniqueLevels) {
    const pill = document.createElement("div");
    pill.className = `level-pill ${l <= lvl ? 'disabled' : ''} ${l === selectedLevel ? 'active' : ''}`;
    pill.textContent = l;
    pill.onclick = () => { selectedLevel = (selectedLevel === l) ? null : l; render(); };
    levelsDiv.appendChild(pill);
  }

  resultsDiv.innerHTML = "";
  let filtered = selectedLevel ? valid.filter(e => e.evolution_level === selectedLevel) : valid;
  filtered = [...filtered].sort((a, b) => b.probability - a.probability);

  const lowBstProb = valid.filter(e => e.bst <= 450).reduce((s, e) => s + (e.probability / totalProb), 0);
  const expectedBst = valid.reduce((s, e) => s + (e.bst * (e.probability / totalProb)), 0);
  
  resultMeta.hidden = false;
  resultMeta.innerHTML = `
    <div class="meta-main"><span><strong>${filtered.length}</strong> outcomes</span></div>
    <div class="meta-stats">
      <div class="stat-box" style="--stat-color: ${getBstColor(expectedBst)}"><span class="label">Avg BST</span><span class="value">${Math.round(expectedBst)}</span></div>
      <div class="stat-box" style="--stat-color: hsl(${lowBstProb * 120}, 80%, 50%)"><span class="label">≤ 450 Chance</span><span class="value">${(lowBstProb * 100).toFixed(1)}%</span></div>
    </div>
  `;

  for (const evo of filtered) {
    const p = totalProb > 0 ? evo.probability / totalProb : 0;
    const slug = toSpriteSlug(evo.evolution);
    const card = document.createElement("div");
    card.className = "evo-card";
    card.innerHTML = `
      <img class="evo-sprite" src="${buildSpriteUrl(evo.evolution)}" 
           onerror="
             if(this.src.includes('ani')) this.src='https://play.pokemonshowdown.com/sprites/gen9/${slug}.png';
             else if(this.src.includes('gen9')) this.src='https://play.pokemonshowdown.com/sprites/dex/${slug}.png';
             else if(this.src.includes('dex')) this.src='https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${slug}.png';
           ">
      <div class="evo-name-col"><div class="evo-name">${evo.evolution}</div><div class="evo-types">${(evo.types || ["Normal"]).map(t => typeBadgeHTML(t)).join("")}</div></div>
      <div class="evo-bst">BST <span>${evo.bst}</span></div>
      <div class="evo-level">${evo.evolution_level}</div>
      <div class="bar-col"><div class="bar"><div class="bar-fill" style="width:${(p * 100).toFixed(2)}%"></div></div><span class="percent">${(p * 100).toFixed(2)}%</span></div>
    `;
    resultsDiv.appendChild(card);
  }
  updateCharts(valid, totalProb);
}

function updateCharts(valid, totalProb) {
  const levelDist = {};
  valid.forEach(e => { levelDist[e.evolution_level] = (levelDist[e.evolution_level] || 0) + (e.probability / totalProb); });
  const levels = Object.keys(levelDist).map(Number).sort((a, b) => a - b);
  evoChart.data.labels = levels;
  evoChart.data.datasets[0].data = levels.map(l => levelDist[l] * 100);
  evoChart.update();

  const typeDist = {};
  valid.forEach(e => {
    const typeCombo = (e.types || ["Unknown"]).sort().join("/");
    typeDist[typeCombo] = (typeDist[typeCombo] || 0) + (e.probability / totalProb);
  });
  const sorted = Object.entries(typeDist).sort((a, b) => b[1] - a[1]);
  typeChart.data.labels = sorted.map(t => t[0]);
  typeChart.data.datasets[0].data = sorted.map(t => t[1] * 100);
  typeChart.data.datasets[0].backgroundColor = sorted.map(t => getTypeColor(t[0]));
  typeChart.update();

  const legendBox = document.getElementById('typeLegend');
  legendBox.innerHTML = sorted.map(([label, prob], i) => `
    <div class="legend-item">
      <span class="legend-color" style="background:${getTypeColor(label)}"></span>
      <span class="legend-label">${label} (${(prob * 100).toFixed(1)}%)</span>
    </div>
  `).join("");
}
