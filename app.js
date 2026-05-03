let DATA = {};
let selectedPokemon = null;
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
const currentLevelInput = document.getElementById("currentLevel");
const evoCtx = document.getElementById('evoChart').getContext('2d');
const typeCtx = document.getElementById('typeChart').getContext('2d');

function initCharts() {
  evoChart = new Chart(evoCtx, {
    type: 'line',
    data: {
      labels: [],
      datasets: [{
        label: 'Evolution Frequency',
        data: [],
        borderColor: '#38bdf8',
        backgroundColor: 'rgba(56, 189, 248, 0.1)',
        fill: true,
        tension: 0.4,
        pointRadius: 2,
        pointBackgroundColor: '#38bdf8'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (ctx) => `Probability: ${ctx.raw.toFixed(2)}%`
          }
        }
      },
      scales: {
        x: {
          display: true,
          title: { display: true, text: 'Level', color: '#9ca3af', font: { size: 10 } },
          grid: { color: '#1f2937' },
          ticks: { color: '#9ca3af', font: { size: 9 } }
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
        backgroundColor: '#f472b6',
        borderRadius: 4
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (ctx) => `Probability: ${ctx.raw.toFixed(2)}%`
          }
        }
      },
      scales: {
        x: {
          display: true,
          title: { display: true, text: 'Probability (%)', color: '#9ca3af', font: { size: 10 } },
          grid: { color: '#1f2937' },
          ticks: { color: '#9ca3af', font: { size: 9 } },
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
  if (!evoChart) initCharts();

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

  for (const evo of filtered) {
    const p = evo.probability / totalProb;
    const typeString = (evo.types || []).join(" / ");

    const card = document.createElement("div");
    card.className = "evo-card";

    card.innerHTML = `
      <div class="evo-name">
        ${evo.evolution}
        <div style="font-size: 0.75rem; opacity: 0.7; font-weight: normal; margin-top: 2px;">
          ${typeString}
        </div>
      </div>
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

  updateCharts(valid, totalProb);
}

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
