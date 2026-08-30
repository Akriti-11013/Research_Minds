(function(){const o=document.createElement("link").relList;if(o&&o.supports&&o.supports("modulepreload"))return;for(const e of document.querySelectorAll('link[rel="modulepreload"]'))i(e);new MutationObserver(e=>{for(const t of e)if(t.type==="childList")for(const r of t.addedNodes)r.tagName==="LINK"&&r.rel==="modulepreload"&&i(r)}).observe(document,{childList:!0,subtree:!0});function s(e){const t={};return e.integrity&&(t.integrity=e.integrity),e.referrerPolicy&&(t.referrerPolicy=e.referrerPolicy),e.crossOrigin==="use-credentials"?t.credentials="include":e.crossOrigin==="anonymous"?t.credentials="omit":t.credentials="same-origin",t}function i(e){if(e.ep)return;e.ep=!0;const t=s(e);fetch(e.href,t)}})();const p=document.querySelector("#root"),l=document.createElement("div");l.className="app";p.appendChild(l);const m="http://localhost:8000/api";function f(){l.innerHTML=`
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
  `,document.querySelector("#research-form").addEventListener("submit",async o=>{var r,d;o.preventDefault();const s=document.querySelector("#topic").value.trim(),i=document.querySelector("#depth").value,e=document.querySelector("#status"),t=document.querySelector("#submit-button");if(!s){e.innerHTML='<span class="error">Please enter a topic.</span>';return}t.disabled=!0,e.textContent="Generating research brief...";try{const a=await fetch(`${m}/research`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({topic:s,depth:i})}),n=await a.json();if(!a.ok){const u=((d=(r=n==null?void 0:n.detail)==null?void 0:r[0])==null?void 0:d.msg)||(n==null?void 0:n.detail)||"Request failed.";throw new Error(u)}h(n),e.textContent="Research brief ready."}catch(a){e.innerHTML=`<span class="error">${a.message}</span>`}finally{t.disabled=!1}})}function h(c){const o=c.report||{},s=o.title||"Untitled research brief",i=o.executive_summary||"",e=o.key_findings||[],t=o.sources||[];document.querySelector("#report-title").textContent=s,document.querySelector("#executive-summary").textContent=i,document.querySelector("#key-findings").innerHTML=e.map(r=>`<li>${r}</li>`).join(""),document.querySelector("#sources").innerHTML=t.map(r=>`
        <li>
          <strong>${r.title}</strong><br />
          <a href="${r.url}" target="_blank" rel="noreferrer">${r.url}</a><br />
          <span>${r.publisher}</span>
        </li>
      `).join(""),document.querySelector("#markdown").textContent=c.markdown||"",document.querySelector("#results").hidden=!1,document.querySelector("#markdown-panel").hidden=!1}f();
