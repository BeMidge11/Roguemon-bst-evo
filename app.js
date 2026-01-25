let DATA = {};
let selectedPokemon = null;
let selectedLevel = null;

fetch("random_bst_evolutions.json")
  .then(r => r.json())
  .then(d => DATA = d);

const input = document.getElementById("pokemonInput");
const suggestionsBox = document.getElementById("suggestions");
const levelsDiv = document.getElementById("levels");
const resultsDiv = document.getElementById("results");
const currentLevelInput = document.getElementById("currentLevel");
const top5List = document.getElementById("top5List");

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
  selectedLevel = null;
  render();
}

currentLevelInput.addEventListener("input", render);

function getValidEvos() {
  const lvl = parseInt(currentLevelInput.value) || 1;
  return selectedPokemon.evolutions.filter(e => e.evolution_level > lvl);
}

function render() {
  if (!selectedPokemon) return;

  const lvl = parseInt(currentLevelInput.value) || 1;
  const valid = getValidEvos();
  const totalProb = valid.reduce((s, e) => s + e.probability, 0);

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
      // TOGGLE behavior
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

  // SORT BY REWEIGHTED % DESC
  filtered = [...filtered].sort((a, b) => b.probability - a.probability);

  for (const evo of filtered) {
    const p = evo.probability / totalProb;

    const card = document.createElement("div");
    card.className = "evo-card";

    card.innerHTML = `
      <div class="evo-name">${evo.evolution}</div>
      <div class="evo-level">${evo.evolution_level}</div>
      <div>
        <div class="bar">
          <div class="bar-fill" style="width:${(p * 100).toFixed(2)}%"></div>
        </div>
        <span class="percent">${(p * 100).toFixed(2)}%</span>
      </div>
    `;

    resultsDiv.appendChild(card);
  }

  renderTop5(valid, totalProb);
}

function renderTop5(valid, totalProb) {
  top5List.innerHTML = "";

  const top = [...valid]
    .sort((a, b) => b.probability - a.probability)
    .slice(0, 5);

  for (const evo of top) {
    const row = document.createElement("div");
    row.className = "top5-item";

    row.innerHTML = `
      <div class="top5-name">
        ${evo.evolution}
        <span style="color: var(--muted); font-size: 0.85rem;">
          (Lv. ${evo.evolution_level})
        </span>
      </div>
      <div class="top5-percent">
        ${((evo.probability / totalProb) * 100).toFixed(2)}%
      </div>
    `;

    top5List.appendChild(row);
  }
}
