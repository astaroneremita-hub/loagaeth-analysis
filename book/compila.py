# -*- coding: utf-8 -*-
"""Compila o livro: EPUB (pandoc nativo, capa por metadado), HTML standalone
(capa de página inteira via include-before-body, imagens embutidas) e PDF
(Chrome headless imprimindo o HTML). Parametrizado por idioma + volume único."""
import os, sys, glob, re, base64, subprocess, shutil
import pypandoc

HERE = os.path.dirname(os.path.abspath(__file__))
FIG  = os.path.join(HERE, "figuras")
OUT  = os.path.join(HERE, "dist")
os.makedirs(OUT, exist_ok=True)
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
EDGE   = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

CSS = """
:root { color-scheme: light; }
@page { size: A4; margin: 2.3cm 2cm; }
html { font-size: 11.6pt; background: #ffffff; }
body { font-family: 'Georgia','Cambria',serif; line-height: 1.52; color: #1b1a17;
       background: #ffffff; max-width: 42em; margin: 0 auto; text-align: justify; hyphens: auto; }
.coverpage { margin: 0; padding: 0; page-break-after: always; text-align: center; }
.coverpage img { width: 100%; height: auto; display: block; margin: 0; }
h1 { font-family: 'Helvetica','Arial',sans-serif; font-size: 1.75em; color: #6b4e13;
     border-bottom: 2.5px solid #b8912f; padding-bottom: .22em; margin-top: 2.2em;
     page-break-before: always; page-break-after: avoid; }
h1.unnumbered:first-of-type { page-break-before: avoid; }
h2 { font-family: 'Helvetica','Arial',sans-serif; font-size: 1.28em; color: #1b1a17;
     margin-top: 1.7em; border-left: 4px solid #b8912f; padding-left: .55em; page-break-after: avoid; }
h3 { font-family: 'Helvetica','Arial',sans-serif; font-size: 1.06em; color: #4a3d1a; page-break-after: avoid; }
p { margin: .55em 0; }
blockquote { border-left: 3px solid #b8912f; margin: 1.1em 0; padding: .4em 1em;
             color: #554; font-style: italic; background: #faf7ef; }
code { background: #f2efe6; padding: .05em .3em; border-radius: 3px; font-size: .9em; }
table { border-collapse: collapse; margin: 1.3em auto; font-size: .88em; width: 100%; page-break-inside: avoid; }
th, td { border: 1px solid #cbb; padding: .32em .6em; vertical-align: top; }
th { background: #f0e9d6; font-family: 'Helvetica',sans-serif; text-align: left; }
tr:nth-child(even) td { background: #fbf9f3; }
figure { margin: 1.4em auto; text-align: center; page-break-inside: avoid; }
img { max-width: 100%; display: block; margin: .6em auto; }
figcaption { color: #666; font-size: .84em; text-align: center; font-style: italic; margin: .35em auto 0; max-width: 34em; }
a { color: #6b4e13; text-decoration: none; }
hr { border: none; border-top: 1px solid #ddd; margin: 2em 0; }
nav#TOC, #TOC { page-break-after: always; }
nav#TOC > ul { list-style: none; padding-left: 0; }
nav#TOC ul ul { list-style: none; padding-left: 1.2em; font-size: .92em; color: #555; }
nav#TOC::before { content: "Sumário"; display: block; font-family: 'Helvetica',sans-serif;
                  font-size: 1.6em; color: #6b4e13; border-bottom: 2px solid #b8912f; padding-bottom: .2em; margin-bottom: .6em; }
"""

def strip_yaml(t): return re.sub(r"^---\n.*?\n---\n", "", t, count=1, flags=re.S)

def cover_html():
    p = os.path.join(FIG, "cover.png")
    if not os.path.exists(p): return None
    b64 = base64.b64encode(open(p, "rb").read()).decode()
    path = os.path.join(OUT, "_cover.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(f'<div class="coverpage"><img src="data:image/png;base64,{b64}" alt="capa"></div>')
    return path

def write_css():
    p = os.path.join(OUT, "estilo.css")
    with open(p, "w", encoding="utf-8") as f: f.write(CSS)
    return p

def render_html_pdf(md_text, base, pagetitle):
    """HTML (capa via include-before-body, antes do TOC) + PDF via Chrome."""
    css = write_css(); cov = cover_html()
    tmp = os.path.join(OUT, f"_src_{base}.md")
    with open(tmp, "w", encoding="utf-8") as f: f.write(md_text)
    html = os.path.join(OUT, base + ".html")
    args = ["--toc", "--toc-depth=2", "--standalone", "--embed-resources",
            "--resource-path", f"{HERE}{os.pathsep}{OUT}", "--css", css,
            "--metadata", f"pagetitle={pagetitle}"]
    if cov: args += ["--include-before-body", cov]
    pypandoc.convert_file(tmp, "html5", format="markdown", outputfile=html, extra_args=args)
    size = os.path.getsize(html)//1024
    pdf = os.path.join(OUT, base + ".pdf")
    browser = CHROME if os.path.exists(CHROME) else EDGE
    prof = os.path.join(OUT, f".chrome_{base}")
    subprocess.run([browser, "--headless=new", "--disable-gpu", "--no-sandbox",
                    f"--user-data-dir={prof}", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf}", "file:///" + html.replace("\\", "/")],
                   capture_output=True, text=True, timeout=240)
    shutil.rmtree(prof, ignore_errors=True)
    print(f"  HTML {size} KB | PDF {'OK '+str(os.path.getsize(pdf)//1024)+' KB' if os.path.exists(pdf) else 'FALHOU'}")

def build(lang):
    src = os.path.join(HERE, lang)
    files = sorted(glob.glob(os.path.join(src, "*.md")))
    if not files: print(f"[{lang}] vazio"); return
    base = f"Liber_Loagaeth_{lang.upper()}"
    title = "Liber Loagaeth — Anatomia de uma Língua Selada" if lang=="pt" else "Liber Loagaeth — Anatomy of a Sealed Language"
    # EPUB (YAML dá metadados; capa por imagem)
    epub = os.path.join(OUT, base + ".epub")
    a = ["--toc", "--toc-depth=2", "--resource-path", f"{src}{os.pathsep}{HERE}"]
    cov = os.path.join(FIG, "cover.png")
    if os.path.exists(cov): a += ["--epub-cover-image", cov]
    pypandoc.convert_file(files, "epub", format="markdown", outputfile=epub, extra_args=a)
    print(f"[{lang}] EPUB {os.path.getsize(epub)//1024} KB")
    # HTML+PDF (sem bloco-título; capa include-before)
    md = "\n\n".join(strip_yaml(open(f, encoding="utf-8").read()) for f in files)
    render_html_pdf(md, base, title)

def build_combined():
    parts = [strip_yaml(open(f, encoding="utf-8").read()) for f in sorted(glob.glob(os.path.join(HERE,"pt","*.md")))]
    parts.append("\n\n\\newpage\n\n# · · ·  English Edition  · · · {.unnumbered}\n\n"
                 "*The complete study follows in English. The Portuguese edition above and this "
                 "English edition are one and the same work.*\n\n")
    parts += [strip_yaml(open(f, encoding="utf-8").read()) for f in sorted(glob.glob(os.path.join(HERE,"en","*.md")))]
    md = "\n\n".join(parts)
    title = "Liber Loagaeth — Anatomia de uma Língua Selada / Anatomy of a Sealed Language"
    # EPUB
    tmp = os.path.join(OUT, "_combined.md")
    with open(tmp, "w", encoding="utf-8") as f: f.write(md)
    epub = os.path.join(OUT, "Liber_Loagaeth.epub")
    a = ["--toc","--toc-depth=2","--resource-path", f"{HERE}{os.pathsep}{OUT}",
         "--metadata", f"title={title}", "--metadata", "author=Astaron Eremita", "--metadata", "lang=pt-BR"]
    cov = os.path.join(FIG, "cover.png")
    if os.path.exists(cov): a += ["--epub-cover-image", cov]
    pypandoc.convert_file(tmp, "epub", format="markdown", outputfile=epub, extra_args=a)
    print(f"[combo] EPUB {os.path.getsize(epub)//1024} KB")
    render_html_pdf(md, "Liber_Loagaeth", title)

if __name__ == "__main__":
    args = sys.argv[1:] or ["pt"]
    if "combined" in args: build_combined()
    else:
        for l in args: build(l)
