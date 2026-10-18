"""Build a reproducible, escaped LaTeX archive from retained Parse responses."""

import hashlib
import json
import re
import shutil
from pathlib import Path

HERMES = Path(__file__).resolve().parents[1]
OUT = HERMES / "archive"
manifest = json.loads((HERMES / "resources/upstream/britannica-manifest.json").read_text())
docs = {
    d["document_id"]: d
    for d in map(json.loads, (HERMES / "resources/corpus/documents.jsonl").read_text().splitlines())
}
for folder in ["assets", "scans", "pdfs", "latex/pages"]:
    (OUT / folder).mkdir(parents=True, exist_ok=True)


def tex(value):
    replacements = {
        "\\": r"\textbackslash{}",
        "{": r"\{",
        "}": r"\}",
        "$": r"\$",
        "&": r"\&",
        "#": r"\#",
        "%": r"\%",
        "_": r"\_",
        "^": r"\textasciicircum{}",
        "~": r"\textasciitilde{}",
    }
    return "".join(
        replacements.get(c, (r"{\fontspec{Kefa III}" + c + "}") if c == "ዬ" else c)
        for c in value
        if c >= " " or c == "\n"
    )


pages = []
for page in manifest["pages"]:
    row = page["row_index"]
    source = HERMES / "data/images" / page["filename"]
    if not source.exists():
        source = OUT / "scans" / page["filename"]
    assert hashlib.sha256(source.read_bytes()).hexdigest() == page["image_sha256"]
    if source.resolve() != (OUT / "scans" / page["filename"]).resolve():
        shutil.copy2(source, OUT / "scans" / page["filename"])
    doc = docs.get(page["page_id"], {})
    raw = doc.get("text", "")
    status = (
        "partial illustration extraction"
        if row == 2243
        else "non-text cover; no prose"
        if row == 452
        else "accepted full-page response; OCR not manually corrected"
    )
    blocks = []
    for part in re.split(r"\n\s*\n", raw):
        cls = re.findall(r"<class_([^>]+)>", part)
        coords = re.findall(r"<[xy]_([0-9.]+)>", part)
        content = re.sub(r"<(?:[xy]_[0-9.]+|class_[^>]+)>", "", part).strip()
        if content:
            blocks.append(
                {
                    "class": cls[-1] if cls else "Text",
                    "text": content,
                    "bounds": [float(x) for x in coords] if len(coords) == 4 else [],
                }
            )
    title = next(
        (b["text"][:90] for b in blocks if b["class"] in ["Page-header", "Section-header"]),
        f"Source page {row}",
    )
    item = {
        **page,
        "title": title,
        "status": status,
        "raw": raw,
        "blocks": blocks,
        "pdf": f"pdfs/page-{row}.pdf",
        "tex": f"latex/pages/page-{row}.tex",
        "scan": f"scans/{page['filename']}",
        "text_sha256": doc.get("text_sha256"),
        "parser_receipt_sha256": doc.get("parser_receipt_sha256"),
    }
    pages.append(item)
    lines = [
        r"\clearpage",
        rf"\section{{Source page {row}}}",
        rf"\textbf{{Extraction status:}} {tex(status)}\par",
        rf"\textbf{{Source volume:}} {tex(page['volume_id'])}\par",
        r"\textbf{Parser:} NVIDIA Nemotron Parse 3.5. Source scan and unchanged raw response accompany this PDF. OCR errors are retained.\par\medskip",
    ]
    if not blocks:
        lines += [
            r"\subsection*{No prose extracted}",
            r"This selected image is a non-text cover. It remains in the sample and is not replaced or treated as a successful article comparison.",
        ]
    for block in blocks:
        content = tex(block["text"])
        if block["class"] in ["Page-header", "Section-header"]:
            lines.append(r"\subsection*{" + content + "}")
        elif block["class"] in ["Caption", "Footnote"]:
            lines.append(r"{\small\itshape " + content + r"\par}\medskip")
        else:
            lines.append(content + r"\par\medskip")
    (OUT / item["tex"]).write_text("\n".join(lines) + "\n")

preamble = r"""\documentclass[10pt,a4paper]{article}
\usepackage[margin=20mm]{geometry}
\usepackage{fontspec}
\setmainfont{Arial Unicode MS}
\usepackage[unicode,colorlinks=true,linkcolor=blue]{hyperref}
\setlength{\parindent}{0pt}
\setlength{\emergencystretch}{5em}
\hypersetup{pdftitle={Tomi: 100-page Britannica Parse 3.5 archive},pdfauthor={Tomi}}
\begin{document}
\section*{Tomi: Britannica archive}
One hundred source images selected without replacement from 2,573 rows, seed 20261016. Dataset revision: \texttt{309f765b1ecc83e0a7f7762e44b4a927a7555443}. National Library of Scotland, CC0-1.0.\par
Each section is compiled from an actual retained Nemotron Parse 3.5 response. Layout classes and paragraph order are retained; the static viewer also provides original scans, coordinate metadata and untouched raw output. This reflowed edition is not a facsimile and does not correct OCR mistakes. Ninety-eight responses are accepted full-page responses, one illustrated page is partial, and one cover is non-text.\par
"""
(OUT / "latex/main.tex").write_text(
    preamble
    + "\n".join(r"\input{pages/page-" + str(p["row_index"]) + ".tex}" for p in pages)
    + "\n\\end{document}\n"
)
(OUT / "assets/pages.json").write_text(
    json.dumps(
        {
            "dataset": manifest["dataset"],
            "revision": manifest["revision"],
            "selection": manifest["selection"],
            "pages": pages,
        },
        ensure_ascii=False,
    )
    + "\n"
)
(OUT / "index.html").write_text(
    """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Tomi | Britannica Archive</title><link rel="stylesheet" href="archive.css"><script src="archive.js" defer></script></head><body><header><a href="/">tomi<span> • evidence archive</span></a><nav><a href="/chat">Chat</a><a href="/canvas">Canvas</a><a href="/deck/202610181800">Pitch</a></nav></header><main><section class="intro"><p class="eyebrow">NVIDIA NEMOTRON PARSE 3.5</p><h1>One hundred pages.<br>Every source inspectable.</h1><p>Original Britannica scans beside compiled LaTeX, retained OCR and extraction status. 98 full-page responses · 1 partial illustration · 1 non-text cover.</p><p class="muted">Reproducible sample: 100 of 2,573 rows · seed 20261016 · National Library of Scotland / CC0</p></section><div class="workbench"><aside><label for="search">Find a page or phrase</label><input id="search" placeholder="Ship-building, bleaching, page…"><p id="count" aria-live="polite"></p><div id="pages"></div></aside><article><div class="page-head"><div><h2 id="title">Loading archive…</h2><p id="status"></p></div><div id="links"></div></div><div class="views"><section><h3>Original scan</h3><img id="scan" alt="Selected original Britannica scan"></section><section><h3>Compiled LaTeX</h3><a id="pdf-link" target="_blank" rel="noopener"><img id="pdf-preview" alt="First page rendered from the compiled LaTeX PDF"></a><p class="muted">First compiled page shown. Open PDF for the complete extraction.</p></section></div><details><summary>Raw Parse response and provenance</summary><pre id="metadata"></pre><pre id="raw"></pre></details><p class="muted">OCR errors are retained. Accepted output does not mean perfect transcription. The partial illustration and non-text cover remain visible failures; they are never replaced by invented prose.</p></article></div></main></body></html>"""
)
(
    OUT / "archive.css"
).write_text("""*{box-sizing:border-box}body{margin:0;background:#f4f2eb;color:#1d2926;font:15px/1.5 system-ui,sans-serif}a{color:inherit}header{display:flex;justify-content:space-between;padding:24px 4vw;border-bottom:1px solid #d1d9cf}header>a{font-size:25px;font-weight:750;text-decoration:none}header span{font-size:13px;color:#4d6659}nav{display:flex;gap:24px;align-items:center}main{padding:25px 4vw 60px}.intro{max-width:900px}.eyebrow{color:#476c47;font-weight:700;letter-spacing:.16em;font-size:12px}h1{font-size:clamp(30px,4vw,55px);line-height:1.04;letter-spacing:-.04em;margin:18px 0}.muted{font-size:12px;color:#586c62}.workbench{display:grid;grid-template-columns:245px minmax(0,1fr);gap:24px;margin-top:30px}aside,article{border:1px solid #cad3c7;border-radius:16px;padding:18px;background:#fffef9}aside{align-self:start}label{font-weight:700}input{width:100%;padding:12px;margin-top:10px;border:1px solid #b6c5b3;border-radius:8px}#pages{max-height:660px;overflow:auto}#pages button{display:block;text-align:left;width:100%;margin:5px 0;padding:10px;border:1px solid transparent;background:#f3f5ee;border-radius:7px;cursor:pointer}#pages button.active{border-color:#759741;background:#e4efce}.page-head{display:flex;gap:15px;justify-content:space-between}h2{font-size:21px;margin:0 0 8px}#status{color:#456239;font-size:12px}.views{display:grid;grid-template-columns:1fr 1fr;gap:16px}.views section{min-width:0}.views img{width:100%;height:630px;object-fit:contain;background:#f3efe2}.views iframe{width:100%;height:630px;border:1px solid #d1d7cd}#links{display:flex;gap:10px;align-items:start;white-space:nowrap}details{margin:20px 0}summary{cursor:pointer;font-weight:700}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:11px;max-height:420px;overflow:auto;background:#f0f3eb;padding:14px;border-radius:8px}@media(max-width:850px){.workbench{grid-template-columns:1fr}.views{grid-template-columns:1fr}#pages{max-height:200px}.page-head{display:block}nav{gap:12px}header span{display:none}}
""")
(OUT / "archive.js").write_text(""""use strict";
const byId=id=>document.getElementById(id);let pages=[],selected=null;
function select(page){selected=page;byId("title").textContent=`Page ${page.row_index} · ${page.title}`;byId("status").textContent=page.status;byId("scan").src=page.scan;byId("pdf-link").href=page.pdf;byId("pdf-preview").src=`previews/page-${page.row_index}.jpg`;byId("raw").textContent=page.raw||"No prose returned for the non-text cover.";byId("metadata").textContent=JSON.stringify({page_id:page.page_id,image_sha256:page.image_sha256,text_sha256:page.text_sha256,parser_receipt_sha256:page.parser_receipt_sha256},null,2);byId("links").replaceChildren();for(const [label,key] of [["PDF","pdf"],["LaTeX","tex"],["Scan","scan"]]){const a=document.createElement("a");a.textContent=label;a.href=page[key];a.target="_blank";a.rel="noopener";byId("links").append(a)}history.replaceState(null,"",`#page-${page.row_index}`);render()}
function render(){const q=byId("search").value.toLowerCase();const matches=pages.filter(p=>`${p.row_index} ${p.title} ${p.raw}`.toLowerCase().includes(q));byId("count").textContent=`${matches.length} of ${pages.length} selected pages`;byId("pages").replaceChildren();for(const page of matches){const button=document.createElement("button");button.textContent=`${page.row_index} · ${page.title}`;button.className=selected===page?"active":"";button.addEventListener("click",()=>select(page));byId("pages").append(button)}}
byId("search").addEventListener("input",render);fetch("assets/pages.json").then(r=>{if(!r.ok)throw new Error("Archive data unavailable");return r.json()}).then(data=>{pages=data.pages;const id=Number(location.hash.replace("#page-",""));select(pages.find(p=>p.row_index===id)||pages[0])}).catch(e=>{byId("title").textContent=e.message});
""")
print(
    json.dumps(
        {"pages": len(pages), "archive": str(OUT), "source_scan_bytes": sum(p["image_bytes"] for p in pages)}
    )
)
