from pathlib import Path
import html
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / 'products' / 'ai-job-search-kit-for-women'
MD = BASE / 'workbook.md'
READER_DIR = ROOT / 'job-search-kit' / 'reader'
READER_DIR.mkdir(parents=True, exist_ok=True)

body = subprocess.check_output(['pandoc', str(MD), '-t', 'html'], text=True)
body = re.sub(r'^<h1[^>]*>AI Job Search Kit for Women</h1>\s*', '', body, count=1)

# Add copy buttons to every prompt/code block.
def add_prompt(match):
    cls = match.group(1) or ''
    code = match.group(2)
    return f'''<div class="prompt-card">
  <div class="prompt-topline"><span>Copy/paste prompt</span><button type="button" class="copy-btn">Copy prompt</button></div>
  <pre{cls}><code>{code}</code></pre>
</div>'''
body = re.sub(r'<pre([^>]*)><code>(.*?)</code></pre>', add_prompt, body, flags=re.S)

# Turn empty worksheet bullets into clean fill lines.
body = body.replace('<li></li>', '<li class="fill-line"><span></span></li>')

# Build nav items from h2 headings. Pandoc may wrap heading text across lines, so use DOTALL.
headings = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body, flags=re.S)
nav_items = []
for i, (hid, title) in enumerate(headings):
    clean = re.sub('<.*?>', '', title)
    clean = re.sub(r'\s+', ' ', clean).strip()
    label = clean.replace('Part ', '').replace(': ', ' · ')
    nav_items.append(f'<a href="#{hid}" data-section="{hid}" data-page-index="{i+1}"><span>{i+1:02d}</span>{html.escape(label)}</a>')
nav_html = '\n'.join(nav_items)

# Insert small chapter numbers before H2s for reader rhythm.
def decorate_h2(match):
    hid, title = match.group(1), match.group(2)
    idx = next((i + 1 for i, (h, _) in enumerate(headings) if h == hid), 1)
    return f'<section class="reader-section" data-section="{hid}"><p class="chapter-kicker">Chapter {idx:02d}</p><h2 id="{hid}">{title}</h2>'
body = re.sub(r'<h2 id="([^"]+)">(.*?)</h2>', decorate_h2, body, flags=re.S)
# Close sections before each hr and at the end. Pandoc uses hr between sections.
body = body.replace('<hr />', '</section><hr class="section-break" />') + '</section>'

pdf_src = BASE / 'dist' / 'ai-job-search-kit-for-women-sellable.pdf'
pdf_dest = READER_DIR / 'ai-job-search-kit-for-women-sellable.pdf'
if pdf_src.exists():
    shutil.copy2(pdf_src, pdf_dest)

css = r'''
:root{
  --paper:#f5efe5;
  --paper2:#fbf6ee;
  --sheet:#fffaf1;
  --ink:#201813;
  --espresso:#2d211a;
  --moss:#5c6144;
  --olive:#74785a;
  --clay:#a4634b;
  --sand:#d7c3aa;
  --muted:#6f6258;
  --line:rgba(45,33,26,.16);
  --shadow:0 28px 70px rgba(45,33,26,.11);
  --radius:28px;
  --reader-font:18px;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth;background:var(--paper)}
body{
  margin:0;
  color:var(--ink);
  background:radial-gradient(circle at 14% 0%,rgba(164,99,75,.10),transparent 28rem),linear-gradient(180deg,var(--paper),var(--paper2) 48%,#e8dccb);
  font-family:"DM Sans",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  line-height:1.65;
  -webkit-font-smoothing:antialiased;
  text-rendering:optimizeLegibility;
}
body:before{content:"";position:fixed;inset:0;pointer-events:none;opacity:.32;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 240 240' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.95' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='.16'/%3E%3C/svg%3E");mix-blend-mode:multiply}
a{color:inherit;text-decoration:none}button{font:inherit}.progress{position:fixed;top:0;left:0;height:4px;width:0;background:var(--clay);z-index:100}
.reader-header{position:sticky;top:0;z-index:80;display:flex;align-items:center;justify-content:space-between;gap:16px;padding:14px clamp(16px,4vw,44px);border-bottom:1px solid var(--line);background:rgba(245,239,229,.88);backdrop-filter:blur(18px)}
.brand{display:inline-flex;align-items:center;gap:10px;font-weight:800;letter-spacing:-.02em}.brand-mark{width:34px;height:34px;border:1px solid var(--ink);border-radius:50%;display:grid;place-items:center;font-family:"Instrument Serif",Georgia,serif;font-size:22px}.reader-actions{display:flex;gap:10px;align-items:center}.pill-btn{border:1px solid var(--line);background:rgba(255,250,241,.62);border-radius:999px;padding:10px 14px;color:#46382e;font-weight:800;font-size:13px;cursor:pointer}.pill-btn.dark{background:var(--ink);border-color:var(--ink);color:var(--sheet)}
.layout{display:grid;grid-template-columns:280px minmax(0,760px) 220px;gap:34px;align-items:start;max-width:1360px;margin:0 auto;padding:34px clamp(16px,3vw,34px) 80px}.sidebar{position:sticky;top:82px;max-height:calc(100vh - 100px);overflow:auto;padding:20px;border:1px solid var(--line);border-radius:22px;background:rgba(255,250,241,.48)}.sidebar p{margin:0 0 14px;color:var(--moss);font-size:11px;font-weight:900;letter-spacing:.14em;text-transform:uppercase}.sidebar nav{display:grid;gap:4px}.sidebar a{display:grid;grid-template-columns:34px 1fr;gap:8px;align-items:start;padding:9px 8px;border-radius:12px;color:#64574b;font-size:13px;line-height:1.25}.sidebar a span{font-family:"Instrument Serif",Georgia,serif;font-size:20px;line-height:.95;color:var(--clay)}.sidebar a.active,.sidebar a:hover{background:#efe3d2;color:var(--ink)}
.book{min-width:0}.cover{min-height:calc(100vh - 120px);display:flex;flex-direction:column;justify-content:space-between;padding:clamp(34px,7vw,74px);margin-bottom:22px;border:1px solid var(--line);border-radius:var(--radius);background:var(--sheet);box-shadow:var(--shadow);position:relative;overflow:hidden}.cover:before{content:"";position:absolute;inset:0;background:radial-gradient(circle at 72% 8%,rgba(116,120,90,.12),transparent 18rem);pointer-events:none}.cover>*{position:relative}.cover-kicker{color:var(--moss);font-size:12px;font-weight:900;letter-spacing:.15em;text-transform:uppercase;margin:0}.cover h1{font-family:"Instrument Serif",Georgia,serif;font-size:clamp(58px,9vw,104px);line-height:.9;letter-spacing:-.055em;font-weight:400;margin:56px 0 20px}.cover-lede{font-family:"Instrument Serif",Georgia,serif;font-size:clamp(28px,4vw,42px);line-height:1.04;letter-spacing:-.035em;color:#3b3028;max-width:680px;margin:0}.cover-note{max-width:620px;margin-top:30px;padding-top:22px;border-top:1px solid var(--line);font-size:18px;color:#5a4c40}.cover-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:46px}.cover-card{border:1px solid var(--line);padding:18px;background:rgba(255,255,255,.26)}.cover-card span{display:block;color:var(--moss);font-size:11px;font-weight:900;letter-spacing:.13em;text-transform:uppercase;margin-bottom:8px}.cover-card strong{font-family:"Instrument Serif",Georgia,serif;font-weight:400;font-size:24px;line-height:1.05}
.reader-card{padding:clamp(28px,5vw,58px);margin-bottom:22px;border:1px solid var(--line);border-radius:var(--radius);background:rgba(255,250,241,.82);box-shadow:0 18px 44px rgba(45,33,26,.07)}.reader-section{scroll-margin-top:96px}.chapter-kicker{color:var(--clay);font-size:12px;font-weight:900;letter-spacing:.15em;text-transform:uppercase;margin:0 0 12px}.reader-card h2{font-family:"Instrument Serif",Georgia,serif;font-size:clamp(42px,6vw,68px);line-height:.98;letter-spacing:-.05em;font-weight:400;margin:0 0 22px;color:var(--ink)}.reader-card h3{font-size:clamp(24px,3vw,34px);letter-spacing:-.035em;line-height:1.05;margin:34px 0 14px;color:#2b211b}.reader-card p,.reader-card li{font-size:var(--reader-font);color:#51463c}.reader-card p{margin:0 0 16px}.reader-card ul,.reader-card ol{padding-left:22px;margin:12px 0 20px}.reader-card li{margin:7px 0}.reader-card strong{color:var(--ink)}.reader-card hr,.section-break{display:none}.fill-line{list-style:none;border-bottom:1px solid rgba(45,33,26,.22);height:28px;margin-left:-18px;color:transparent}.reader-card p:has(strong:only-child){margin-top:18px;color:var(--ink)}
.prompt-card{margin:22px 0;border:1px solid rgba(92,97,68,.28);background:#f0e5d5;border-radius:18px;overflow:hidden}.prompt-topline{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:10px 12px 10px 16px;background:#e5d6bf;border-bottom:1px solid rgba(92,97,68,.22)}.prompt-topline span{color:var(--moss);font-size:11px;font-weight:900;letter-spacing:.13em;text-transform:uppercase}.copy-btn{border:1px solid rgba(45,33,26,.18);background:var(--sheet);border-radius:999px;padding:8px 12px;font-size:12px;font-weight:900;color:var(--espresso);cursor:pointer}.copy-btn.copied{background:var(--moss);color:var(--sheet)}pre{margin:0;white-space:pre-wrap;word-break:break-word;padding:20px;font:14px/1.55 ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace;color:#2a241e}.reader-footer-nav{display:flex;justify-content:space-between;gap:14px;margin:22px 0 0}.reader-footer-nav a{flex:1;border:1px solid var(--line);background:rgba(255,250,241,.62);border-radius:16px;padding:14px 16px;font-weight:900;color:#473a31}.reader-footer-nav a:last-child{text-align:right}.toolbox{position:sticky;top:82px;display:grid;gap:12px}.tool-card{border:1px solid var(--line);border-radius:22px;background:rgba(255,250,241,.50);padding:18px}.tool-card h2{font-family:"Instrument Serif",Georgia,serif;font-weight:400;font-size:28px;line-height:1;margin:0 0 10px}.tool-card p{font-size:14px;color:var(--muted);margin:0 0 14px}.mini-action{display:block;text-align:center;border-radius:999px;background:var(--espresso);color:var(--sheet);font-weight:900;padding:12px 14px;font-size:13px}.font-controls{display:flex;gap:8px}.font-controls button{flex:1;border:1px solid var(--line);background:var(--sheet);border-radius:999px;padding:9px;font-weight:900;cursor:pointer}
.toast{position:fixed;left:50%;bottom:24px;transform:translateX(-50%) translateY(20px);opacity:0;pointer-events:none;background:var(--ink);color:var(--sheet);border-radius:999px;padding:11px 16px;font-weight:900;z-index:100;transition:.2s}.toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
html,body{height:100%;overflow:hidden}.reader-header{height:63px}.layout{height:calc(100vh - 63px);overflow:hidden}.book{height:100%;display:grid;grid-template-rows:minmax(0,1fr) auto}.reader-page{display:none}.reader-page.active{display:flex}.cover.reader-page.active{min-height:0;height:100%;margin:0}.reader-card{display:block;min-height:0;height:100%;overflow:hidden;margin:0}.reader-section{display:none;height:100%;overflow:auto;padding-right:8px;scrollbar-width:thin}.reader-section.active{display:block}.page-controls{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:14px;padding:14px 2px 0}.page-btn{border:1px solid var(--line);background:rgba(255,250,241,.72);border-radius:999px;padding:11px 16px;font-weight:900;color:#46382e;cursor:pointer}.page-btn:last-child{justify-self:end}.page-btn:disabled{opacity:.38;cursor:not-allowed}.page-count{color:var(--muted);font-size:12px;font-weight:900;letter-spacing:.12em;text-transform:uppercase}.sidebar a[data-page-index="0"]{display:none}.mini-action{cursor:pointer}.reader-footer-nav{display:none}
@media(max-width:1080px){.layout{grid-template-columns:1fr}.sidebar{position:static;max-height:none}.sidebar nav{grid-template-columns:repeat(2,1fr)}.toolbox{position:static;grid-template-columns:1fr 1fr}.book{order:-1}}
@media(max-width:700px){.reader-header{height:auto;min-height:63px;align-items:center;flex-wrap:wrap}.brand{min-width:110px}.reader-actions{gap:6px;max-width:100%;overflow:auto;padding-bottom:2px}.pill-btn{padding:9px 11px;white-space:nowrap;font-size:12px}.layout{height:calc(100vh - 106px);padding:16px 0 18px}.cover,.reader-card{border-radius:0;border-left:0;border-right:0;margin-bottom:0}.cover{min-height:0;padding:34px 24px}.reader-card{padding:32px 24px}.cover-grid,.toolbox{grid-template-columns:1fr}.sidebar{display:none}.toolbox{display:none}.reader-card p,.reader-card li{font-size:17px}.reader-card h2{font-size:34px;line-height:1.02;letter-spacing:-.04em}.reader-card h3{font-size:25px}.prompt-topline{align-items:flex-start;flex-direction:column}.copy-btn{width:100%}.reader-footer-nav{flex-direction:column}.reader-footer-nav a:last-child{text-align:left}.cover h1{font-size:38px;line-height:1;letter-spacing:-.045em;overflow-wrap:normal}.cover-lede{font-size:22px;line-height:1.12}.cover-note{font-size:16px}.cover-card strong{font-size:22px}.page-controls{padding:10px 16px 0}.page-btn{padding:10px 12px}.page-count{font-size:11px}}
'''

js = r'''
const progress = document.querySelector('.progress');
const navLinks = [...document.querySelectorAll('.sidebar a')];
const cover = document.querySelector('.cover');
const readerCard = document.querySelector('.reader-card');
const sections = [...document.querySelectorAll('.reader-section')];
const pages = [cover, ...sections];
const toast = document.querySelector('.toast');
const prevBtn = document.querySelector('[data-page="prev"]');
const nextBtn = document.querySelector('[data-page="next"]');
const pageCount = document.querySelector('.page-count');
let currentPage = Number(localStorage.getItem('canopyReaderPage') || 0);

function clampPage(index){ return Math.min(pages.length - 1, Math.max(0, index)); }
function pageTitle(index){
  if (index === 0) return 'Cover';
  const heading = pages[index].querySelector('h2');
  return heading ? heading.textContent.replace(/\s+/g, ' ').trim() : `Chapter ${index}`;
}
function setPage(index){
  currentPage = clampPage(index);
  localStorage.setItem('canopyReaderPage', currentPage);
  cover.classList.toggle('active', currentPage === 0);
  readerCard.classList.toggle('active', currentPage > 0);
  sections.forEach((section, i) => {
    const active = i + 1 === currentPage;
    section.classList.toggle('active', active);
    if (active) section.scrollTop = 0;
  });
  navLinks.forEach(a => a.classList.toggle('active', Number(a.dataset.pageIndex) === currentPage));
  progress.style.width = ((currentPage + 1) / pages.length * 100) + '%';
  prevBtn.disabled = currentPage === 0;
  nextBtn.disabled = currentPage === pages.length - 1;
  prevBtn.textContent = currentPage === 0 ? 'Previous' : 'Previous';
  nextBtn.textContent = currentPage === pages.length - 1 ? 'Finished' : 'Next';
  pageCount.textContent = `${currentPage + 1} / ${pages.length} · ${pageTitle(currentPage)}`;
}
setPage(currentPage);

prevBtn.addEventListener('click', () => setPage(currentPage - 1));
nextBtn.addEventListener('click', () => setPage(currentPage + 1));
navLinks.forEach(link => {
  link.addEventListener('click', event => {
    event.preventDefault();
    setPage(Number(link.dataset.pageIndex));
  });
});
document.querySelectorAll('[data-go-to]').forEach(link => {
  link.addEventListener('click', event => {
    event.preventDefault();
    const target = sections.findIndex(section => section.dataset.section === link.dataset.goTo);
    if (target >= 0) setPage(target + 1);
  });
});
document.addEventListener('keydown', event => {
  if (event.key === 'ArrowLeft') setPage(currentPage - 1);
  if (event.key === 'ArrowRight') setPage(currentPage + 1);
});

document.querySelectorAll('.copy-btn').forEach(btn => {
  btn.addEventListener('click', async () => {
    const code = btn.closest('.prompt-card').querySelector('code').innerText;
    try { await navigator.clipboard.writeText(code); }
    catch(e){
      const ta = document.createElement('textarea'); ta.value = code; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); ta.remove();
    }
    btn.classList.add('copied'); btn.textContent = 'Copied';
    toast.classList.add('show');
    setTimeout(()=>{ btn.classList.remove('copied'); btn.textContent='Copy prompt'; toast.classList.remove('show'); }, 1400);
  });
});

const root = document.documentElement;
let size = Number(localStorage.getItem('canopyReaderFont') || 18);
function setSize(next){ size = Math.min(22, Math.max(16, next)); root.style.setProperty('--reader-font', size + 'px'); localStorage.setItem('canopyReaderFont', size); }
setSize(size);
document.querySelector('[data-font="minus"]').addEventListener('click',()=>setSize(size-1));
document.querySelector('[data-font="plus"]').addEventListener('click',()=>setSize(size+1));
'''

html_doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>AI Job Search Kit for Women — Canopy Reader</title>
  <meta name="robots" content="noindex,nofollow" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800;900&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet" />
  <style>{css}</style>
</head>
<body>
  <div class="progress" aria-hidden="true"></div>
  <header class="reader-header">
    <a class="brand" href="../../../index.html"><span class="brand-mark">C</span><span>Canopy</span></a>
    <div class="reader-actions">
      <a class="pill-btn" href="ai-job-search-kit-for-women-sellable.pdf" download>Download PDF</a>
      <a class="pill-btn dark" href="mailto:meetcanopy@gmail.com?subject=AI%20Job%20Search%20Kit%20question">Ask Stephanie</a>
    </div>
  </header>

  <div class="layout">
    <aside class="sidebar" aria-label="Reader chapters">
      <p>Chapters</p>
      <nav>{nav_html}</nav>
    </aside>

    <main class="book" id="reader">
      <section class="cover reader-page active" aria-label="Cover" data-section="cover">
        <div>
          <p class="cover-kicker">Canopy private reader</p>
          <h1>AI Job Search Kit for Women</h1>
          <p class="cover-lede">A calmer way to rebuild your resume, LinkedIn, applications, and interview prep with AI.</p>
          <p class="cover-note">Read straight through like a small digital book, or jump to the chapter you need. Every prompt is copyable.</p>
          <div class="cover-grid">
            <div class="cover-card"><span>Best for</span><strong>Remote searches, pivots, and getting unstuck.</strong></div>
            <div class="cover-card"><span>Use time</span><strong>One focused 90-minute reset.</strong></div>
          </div>
        </div>
      </section>

      <article class="reader-card reader-page">
        {body}
        <div class="reader-footer-nav"><a href="#reader">↑ Back to top</a><a href="ai-job-search-kit-for-women-sellable.pdf" download>Download the PDF →</a></div>
      </article>
      <nav class="page-controls" aria-label="Reader pages">
        <button class="page-btn" type="button" data-page="prev">Previous</button>
        <span class="page-count">1 / {len(headings) + 1} · Cover</span>
        <button class="page-btn" type="button" data-page="next">Next</button>
      </nav>
    </main>

    <aside class="toolbox" aria-label="Reader tools">
      <div class="tool-card">
        <h2>Reader tools</h2>
        <p>Adjust the text size while you work through the guide.</p>
        <div class="font-controls"><button type="button" data-font="minus">A-</button><button type="button" data-font="plus">A+</button></div>
      </div>
      <div class="tool-card">
        <h2>Use it fast</h2>
        <p>Start with the context prompt, then move chapter by chapter. Do not perfect everything on the first pass.</p>
        <a class="mini-action" href="#before-you-paste-anything-into-ai" data-go-to="before-you-paste-anything-into-ai">Start the prompts</a>
      </div>
    </aside>
  </div>
  <div class="toast">Prompt copied</div>
  <script>{js}</script>
</body>
</html>
'''

(READER_DIR / 'index.html').write_text(html_doc)
print(READER_DIR / 'index.html')
print('chapters', len(headings))
print('pdf copied', pdf_dest.exists(), pdf_dest.stat().st_size if pdf_dest.exists() else None)
