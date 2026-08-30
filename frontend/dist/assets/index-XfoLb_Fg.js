(function(){const o=document.createElement("link").relList;if(o&&o.supports&&o.supports("modulepreload"))return;for(const e of document.querySelectorAll('link[rel="modulepreload"]'))c(e);new MutationObserver(e=>{for(const t of e)if(t.type==="childList")for(const s of t.addedNodes)s.tagName==="LINK"&&s.rel==="modulepreload"&&c(s)}).observe(document,{childList:!0,subtree:!0});function a(e){const t={};return e.integrity&&(t.integrity=e.integrity),e.referrerPolicy&&(t.referrerPolicy=e.referrerPolicy),e.crossOrigin==="use-credentials"?t.credentials="include":e.crossOrigin==="anonymous"?t.credentials="omit":t.credentials="same-origin",t}function c(e){if(e.ep)return;e.ep=!0;const t=a(e);fetch(e.href,t)}})();const b=document.querySelector("#root"),u=document.createElement("div");u.className="app";b.appendChild(u);const y="http://localhost:8000/api";function v(){u.innerHTML=`
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
  `,document.querySelector("#research-form").addEventListener("submit",async o=>{var m,f;o.preventDefault();const a=document.querySelector("#topic").value.trim(),c=document.querySelector("#depth").value,e=Number(document.querySelector("#number-of-sources").value),t=document.querySelector("#output-format").value,s=[...document.querySelectorAll('input[name="focus_areas"]:checked')].map(i=>i.value),r=document.querySelector("#status"),d=document.querySelector("#submit-button"),p=globalThis.crypto&&crypto.randomUUID?crypto.randomUUID():`research-${Date.now()}`;if(!a){r.innerHTML='<span class="error">Please enter a topic.</span>';return}d.disabled=!0,r.textContent="Generating research brief...";try{const i=await fetch(`${y}/research`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({topic:a,depth:c,research_id:p,focus_areas:s,number_of_sources:e,output_format:t})}),n=await i.json();if(!i.ok){const h=((f=(m=n==null?void 0:n.detail)==null?void 0:m[0])==null?void 0:f.msg)||(n==null?void 0:n.detail)||"Request failed.";throw new Error(h)}g(n),r.textContent=`Research brief ready. Research ID: ${n.research_id||p}`}catch(i){r.innerHTML=`<span class="error">${i.message}</span>`}finally{d.disabled=!1}})}function g(l){const o=l.report||{},a=o.title||"Untitled research brief",c=o.executive_summary||"",e=o.key_findings||[],t=o.sources||[],s=l.research_id||"research-local";document.querySelector("#report-title").textContent=`${a} · ${s}`,document.querySelector("#executive-summary").textContent=c,document.querySelector("#key-findings").innerHTML=e.map(r=>`<li>${r}</li>`).join(""),document.querySelector("#sources").innerHTML=t.map(r=>`
        <li>
          <strong>${r.title}</strong><br />
          <a href="${r.url}" target="_blank" rel="noreferrer">${r.url}</a><br />
          <span>${r.publisher}</span>
        </li>
      `).join(""),document.querySelector("#markdown").textContent=l.markdown||"",document.querySelector("#results").hidden=!1,document.querySelector("#markdown-panel").hidden=!1}v();
