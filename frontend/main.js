const root = document.querySelector('#root');

const app = document.createElement('div');
app.className = 'app';
root.appendChild(app);

const API_BASE = 'http://localhost:8000/api';

function render() {
  app.innerHTML = `
    <header class="hero">
      <h1>ResearchMind</h1>
      <p>Turn a topic into a structured research brief and Obsidian-ready markdown note.</p>
    </header>

    <section class="panel">
      <form id="research-form">
        <div class="form-row">
          <label>
            Topic
            <input id="topic" name="topic" type="text" placeholder="Impact of Generative AI on software development" required minlength="3" />
          </label>

          <label>
            Depth
            <select id="depth" name="depth">
              <option value="quick">Quick</option>
              <option value="standard" selected>Standard</option>
              <option value="deep">Deep</option>
            </select>
          </label>
        </div>

        <div class="form-row secondary-row">
          <label>
            Number of sources
            <select id="number-of-sources" name="number_of_sources">
              <option value="3">3</option>
              <option value="5" selected>5</option>
              <option value="8">8</option>
              <option value="10">10</option>
            </select>
          </label>

          <label>
            Output format
            <select id="output-format" name="output_format">
              <option value="markdown" selected>Markdown</option>
              <option value="json">JSON</option>
            </select>
          </label>
        </div>

        <div class="focus-wrap">
          <span class="focus-label">Focus areas</span>
          <div class="focus-grid">
            <label><input type="checkbox" name="focus_areas" value="productivity" checked /> Productivity</label>
            <label><input type="checkbox" name="focus_areas" value="security" checked /> Security</label>
            <label><input type="checkbox" name="focus_areas" value="governance" /> Governance</label>
            <label><input type="checkbox" name="focus_areas" value="trends" /> Trends</label>
          </div>
        </div>

        <button id="submit-button" type="submit">Generate report</button>
      </form>
      <div id="status" aria-live="polite"></div>
      <div class="progress-list" aria-live="polite">
        <span>Planning</span>
        <span>Searching</span>
        <span>Analyzing</span>
        <span>Fact-checking</span>
        <span>Exporting</span>
      </div>
    </section>

    <section id="results" class="result-grid" hidden>
      <article>
        <div class="summary-box">
          <h2 id="report-title">Report</h2>
          <p id="executive-summary"></p>
          <ul id="key-findings" class="key-findings"></ul>
        </div>
      </article>

      <aside>
        <div class="source-list-panel panel">
          <h2>Sources</h2>
          <ul id="sources" class="source-list"></ul>
        </div>
      </aside>
    </section>

    <section id="markdown-panel" class="panel" hidden>
      <h2>Markdown preview</h2>
      <pre id="markdown" class="markdown-box"></pre>
    </section>
  `;

  const form = document.querySelector('#research-form');
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const topic = document.querySelector('#topic').value.trim();
    const depth = document.querySelector('#depth').value;
    const numberOfSources = Number(document.querySelector('#number-of-sources').value);
    const outputFormat = document.querySelector('#output-format').value;
    const focusAreas = [...document.querySelectorAll('input[name="focus_areas"]:checked')].map((input) => input.value);
    const status = document.querySelector('#status');
    const button = document.querySelector('#submit-button');
    const researchId = (globalThis.crypto && crypto.randomUUID) ? crypto.randomUUID() : `research-${Date.now()}`;

    if (!topic) {
      status.innerHTML = '<span class="error">Please enter a topic.</span>';
      return;
    }

    button.disabled = true;
    status.textContent = 'Generating research brief...';

    try {
      const response = await fetch(`${API_BASE}/research`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic, depth, research_id: researchId, focus_areas: focusAreas, number_of_sources: numberOfSources, output_format: outputFormat }),
      });

      const payload = await response.json();

      if (!response.ok) {
        const message = payload?.detail?.[0]?.msg || payload?.detail || 'Request failed.';
        throw new Error(message);
      }

      renderReport(payload);
      status.textContent = `Research brief ready. Research ID: ${payload.research_id || researchId}`;
    } catch (error) {
      status.innerHTML = `<span class="error">${error.message}</span>`;
    } finally {
      button.disabled = false;
    }
  });
}

function renderReport(data) {
  const report = data.report || {};
  const title = report.title || 'Untitled research brief';
  const summary = report.executive_summary || '';
  const findings = report.key_findings || [];
  const sources = report.sources || [];

  const researchId = data.research_id || 'research-local';
  document.querySelector('#report-title').textContent = `${title} · ${researchId}`;
  document.querySelector('#executive-summary').textContent = summary;
  document.querySelector('#key-findings').innerHTML = findings
    .map((item) => `<li>${item}</li>`)
    .join('');

  document.querySelector('#sources').innerHTML = sources
    .map(
      (source) => `
        <li>
          <strong>${source.title}</strong><br />
          <a href="${source.url}" target="_blank" rel="noreferrer">${source.url}</a><br />
          <span>${source.publisher}</span>
        </li>
      `
    )
    .join('');

  document.querySelector('#markdown').textContent = data.markdown || '';

  document.querySelector('#results').hidden = false;
  document.querySelector('#markdown-panel').hidden = false;
}

render();
