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

        <button id="submit-button" type="submit">Generate report</button>
      </form>
      <div id="status" aria-live="polite"></div>
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
    const status = document.querySelector('#status');
    const button = document.querySelector('#submit-button');

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
        body: JSON.stringify({ topic, depth }),
      });

      const payload = await response.json();

      if (!response.ok) {
        const message = payload?.detail?.[0]?.msg || payload?.detail || 'Request failed.';
        throw new Error(message);
      }

      renderReport(payload);
      status.textContent = 'Research brief ready.';
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

  document.querySelector('#report-title').textContent = title;
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
