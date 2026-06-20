#!/usr/bin/env python3
# Author: Tom Sapletta · https://tom.sapletta.com
# Part of the ifURI solution.

"""Render the ifURI docs (markdown) into a brand static site for docs.ifuri.com."""
import os, re, html, sys, shutil, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/"_site"
ORDER=["index","getting-started","naming","commands","registry-and-bindings","connectors","connector-authoring","transports","mcp","host-node-lan","novnc-demo","project-structure-audit-2026-06-20","logo","roadmap","release-checklist"]
def md(text):
    out=[];i=0;lines=text.replace("\r","").split("\n");n=len(lines)
    def inl(s):
        s=html.escape(s)
        s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',lambda m:f'<a href="{m.group(2)}">{m.group(1)}</a>',s)
        s=re.sub(r'`([^`]+)`',r'<code>\1</code>',s);s=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',s);return s
    while i<n:
        ln=lines[i]
        if ln.startswith("```"):
            i+=1;buf=[]
            while i<n and not lines[i].startswith("```"):buf.append(html.escape(lines[i]));i+=1
            i+=1;out.append("<pre><code>"+"\n".join(buf)+"</code></pre>");continue
        m=re.match(r'(#{1,6})\s+(.*)',ln)
        if m:l=len(m.group(1));out.append(f"<h{l}>{inl(m.group(2))}</h{l}>");i+=1;continue
        if re.match(r'\s*[-*]\s+',ln):
            it=[]
            while i<n and re.match(r'\s*[-*]\s+',lines[i]):
                item=[re.sub(r'\s*[-*]\s+','',lines[i],count=1)];i+=1
                while i<n and lines[i].strip() and not re.match(r'(#{1,6}\s|```|\s*[-*]\s)',lines[i]):
                    item.append(lines[i].strip());i+=1
                it.append(inl(" ".join(item)))
            out.append("<ul>"+"".join(f"<li>{x}</li>" for x in it)+"</ul>");continue
        if ln.strip()=="":i+=1;continue
        p=[ln];i+=1
        while i<n and lines[i].strip() and not re.match(r'(#{1,6}\s|```|\s*[-*]\s)',lines[i]):p.append(lines[i]);i+=1
        out.append("<p>"+inl(" ".join(p))+"</p>")
    return "\n".join(out)
def md_to_html_links(s):  # turn slug.md links into slug.html
    return re.sub(r'href="([a-z0-9-]+)\.md"',r'href="\1.html"',s)
slugs=[s for s in ORDER if (ROOT/f"{s}.md").exists()]
slugs+= [p.stem for p in ROOT.glob("*.md") if p.stem not in slugs and p.stem not in ("README","LICENSE","TODO","CHANGELOG")]
titles={}
for s in slugs:
    t=None
    for ln in (ROOT/f"{s}.md").read_text(encoding="utf-8").split("\n"):
        if ln.startswith("# "):t=ln[2:].strip();break
    titles[s]=t or s
nav="".join(f'<a href="{s}.html">{html.escape(titles[s])}</a>' for s in slugs)
def page(slug):
    body=md_to_html_links(md((ROOT/f"{slug}.md").read_text(encoding="utf-8")))
    return f"""<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(titles[slug])} · ifURI docs</title><meta name="theme-color" content="#1E1B4B">
<link rel="icon" href="https://ifuri.com/assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="style.css">
</head><body>
<header><a class="brand" href="index.html">ifURI <span>docs</span></a>
<nav><a href="https://ifuri.com/">ifuri.com</a><a href="https://examples.ifuri.com/">Examples</a><a href="https://roadmap.ifuri.com/">Roadmap</a><a href="https://github.com/if-uri/docs">GitHub</a></nav></header>
<div class="wrap"><aside>{nav}</aside><main>{body}</main></div>
<footer>ifURI docs · <a href="https://ifuri.com/">ifuri.com</a></footer>
<script src="copy.js"></script><script src="https://ifuri.com/assets/ifuri-ecobar.js" defer></script></body></html>"""
if OUT.exists():shutil.rmtree(OUT)
OUT.mkdir(parents=True)
for s in slugs:(OUT/f"{s}.html").write_text(page(s),encoding="utf-8")
(OUT/"style.css").write_text(""":root{--bg:#1E1B4B;--card:rgba(255,255,255,.06);--text:#EEF2FF;--muted:#A5B4FC;--line:rgba(255,255,255,.14);--green:#34D399}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(900px 520px at 88% -8%,rgba(79,70,229,.2),transparent 60%),linear-gradient(180deg,#1E1B4B,#191640);color:var(--text);font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",Arial,sans-serif;line-height:1.6;min-height:100vh}
a{color:var(--green);text-decoration:none}a:hover{text-decoration:underline}
header{position:sticky;top:0;display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px;align-items:center;padding:14px 24px;border-bottom:1px solid var(--line);background:rgba(30,27,75,.82);backdrop-filter:blur(12px);z-index:5}
.brand{font-weight:800;font-size:18px;color:var(--text)}.brand span{color:var(--green)}
header nav a{color:var(--muted);font-weight:700;font-size:14px;margin-left:16px}
.wrap{max-width:1040px;margin:0 auto;padding:28px 24px;display:grid;grid-template-columns:220px 1fr;gap:30px;align-items:start}
aside{position:sticky;top:84px;border:1px solid var(--line);background:var(--card);border-radius:14px;padding:10px;display:grid;gap:2px}
aside a{padding:8px 12px;border-radius:9px;color:var(--muted);font-weight:650;font-size:14px}aside a:hover{background:rgba(52,211,153,.1);color:var(--text);text-decoration:none}
main{min-width:0;border:1px solid var(--line);background:var(--card);border-radius:14px;padding:30px 34px}
h1{font-size:clamp(28px,4vw,40px);letter-spacing:-.02em;margin:0 0 4px}h2{font-size:23px;margin:28px 0 0}h3{font-size:18px;margin:20px 0 0}
p,li{color:#cdd6ee}
code{background:rgba(52,211,153,.08);border:1px solid rgba(52,211,153,.2);color:#6EE7B7;border-radius:6px;padding:.06rem .35rem;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:.92em}
pre{position:relative;background:#0F172A;border:1px solid var(--line);border-radius:12px;padding:18px;overflow:auto}pre code{background:none;border:0;color:#E0E7FF;padding:0}
.copy-btn{position:absolute;top:10px;right:10px;font-size:11px;font-weight:800;color:#0F172A;background:var(--green);border:0;border-radius:999px;padding:5px 11px;cursor:pointer;opacity:.6}.copy-btn:hover,.copy-btn:focus-visible{opacity:1}
footer{max-width:1040px;margin:0 auto;padding:24px;border-top:1px solid var(--line);color:var(--muted);font-size:13px}
@media(max-width:760px){.wrap{grid-template-columns:1fr}aside{position:static}}""",encoding="utf-8")
(OUT/"copy.js").write_text("""(function(){var en=document.documentElement.lang==='en';var L='Copy',D='Copied';document.querySelectorAll('pre').forEach(function(p){if(p.querySelector('.copy-btn'))return;var c=p.querySelector('code');var b=document.createElement('button');b.type='button';b.className='copy-btn';b.textContent=L;b.addEventListener('click',function(){navigator.clipboard.writeText((c||p).textContent).then(function(){b.textContent=D;setTimeout(function(){b.textContent=L},1200)})});p.appendChild(b)})})();""",encoding="utf-8")
print(f"built {len(slugs)} docs -> {OUT}")
