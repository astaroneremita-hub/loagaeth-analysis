# -*- coding: utf-8 -*-
"""Compila o livro: EPUB (pandoc nativo), HTML standalone (imagens embutidas)
e PDF (Chrome headless imprimindo o HTML). Parametrizado por idioma."""
import os, sys, glob, subprocess, shutil
import pypandoc

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, "figuras")
OUT = os.path.join(HERE, "dist")
os.makedirs(OUT, exist_ok=True)

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

CSS = """
@page { size: A4; margin: 2.2cm 2cm; }
html { font-size: 12pt; }
body { font-family: 'Georgia','Cambria',serif; line-height: 1.5; color: #1b1a17;
       max-width: 42em; margin: 0 auto; text-align: justify; hyphens: auto; }
h1 { font-family: 'Helvetica','Arial',sans-serif; font-size: 1.7em; color: #6b4e13;
     border-bottom: 2px solid #b8912f; padding-bottom: .2em; margin-top: 2.2em;
     page-break-before: always; }
h1:first-of-type { page-break-before: avoid; }
h2 { font-family: 'Helvetica','Arial',sans-serif; font-size: 1.25em; color: #1b1a17;
     margin-top: 1.6em; border-left: 3px solid #b8912f; padding-left: .5em; }
h3 { font-family: 'Helvetica','Arial',sans-serif; font-size: 1.05em; color: #444; }
blockquote { border-left: 3px solid #b8912f; margin: 1em 0; padding: .3em 1em;
             color: #555; font-style: italic; background: #faf7ef; }
code { background: #f2efe6; padding: .05em .3em; border-radius: 3px; font-size: .9em; }
table { border-collapse: collapse; margin: 1.2em auto; font-size: .92em; width: 100%; }
th, td { border: 1px solid #ccc; padding: .35em .6em; }
th { background: #f0e9d6; font-family: 'Helvetica',sans-serif; }
img { max-width: 100%; display: block; margin: 1.2em auto; }
figcaption, p em:only-child { color: #666; font-size: .9em; }
a { color: #6b4e13; }
hr { border: none; border-top: 1px solid #ddd; margin: 2em 0; }
#TOC, nav#TOC { page-break-after: always; }
#TOC ul { list-style: none; }
"""

def build(lang):
    src = os.path.join(HERE, lang)
    files = sorted(glob.glob(os.path.join(src, "*.md")))
    if not files:
        print(f"[{lang}] sem arquivos .md, pulando"); return
    base = f"Liber_Loagaeth_{lang.upper()}"
    css_path = os.path.join(OUT, f"estilo_{lang}.css")
    with open(css_path, "w", encoding="utf-8") as f:
        f.write(CSS)
    cover = os.path.join(FIG, "cover.png")

    common = ["--toc", "--toc-depth=2", "--resource-path", f"{src}{os.pathsep}{HERE}"]

    # EPUB
    epub = os.path.join(OUT, base + ".epub")
    args = common + ["--metadata", f"lang={'pt-BR' if lang=='pt' else 'en-US'}"]
    if os.path.exists(cover):
        args += ["--epub-cover-image", cover]
    pypandoc.convert_file(files, "epub", format="markdown", outputfile=epub, extra_args=args)
    print(f"[{lang}] EPUB -> {epub}  ({os.path.getsize(epub)//1024} KB)")

    # HTML standalone (imagens embutidas)
    html = os.path.join(OUT, base + ".html")
    args = common + ["--standalone", "--embed-resources", "--css", css_path,
                     "--metadata", "title-prefix= "]
    pypandoc.convert_file(files, "html5", format="markdown", outputfile=html, extra_args=args)
    print(f"[{lang}] HTML -> {html}  ({os.path.getsize(html)//1024} KB)")

    # PDF via Chrome/Edge headless
    pdf = os.path.join(OUT, base + ".pdf")
    browser = CHROME if os.path.exists(CHROME) else EDGE
    prof = os.path.join(OUT, f".chrome_{lang}")
    cmd = [browser, "--headless=new", "--disable-gpu", "--no-sandbox",
           f"--user-data-dir={prof}", "--no-pdf-header-footer",
           f"--print-to-pdf={pdf}", "file:///" + html.replace("\\", "/")]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    if os.path.exists(pdf):
        print(f"[{lang}] PDF  -> {pdf}  ({os.path.getsize(pdf)//1024} KB)")
    else:
        print(f"[{lang}] PDF FALHOU rc={r.returncode}\n{r.stderr[:500]}")
    shutil.rmtree(prof, ignore_errors=True)

import re, tempfile
def strip_yaml(t):
    return re.sub(r"^---\n.*?\n---\n", "", t, count=1, flags=re.S)

def build_combined():
    """Volume único: PT inteiro, depois EN inteiro."""
    parts = []
    for f in sorted(glob.glob(os.path.join(HERE, "pt", "*.md"))):
        parts.append(strip_yaml(open(f, encoding="utf-8").read()))
    parts.append("\n\n\\newpage\n\n# · · ·\n\n# English Edition\n\n"
                 "*The complete study follows in English. The Portuguese edition above "
                 "and this English edition are one and the same work.*\n\n\\newpage\n\n")
    for f in sorted(glob.glob(os.path.join(HERE, "en", "*.md"))):
        parts.append(strip_yaml(open(f, encoding="utf-8").read()))
    combined = "\n\n".join(parts)

    tmp = os.path.join(OUT, "_combined.md")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(combined)
    base = "Liber_Loagaeth"
    css_path = os.path.join(OUT, "estilo_combined.css")
    with open(css_path, "w", encoding="utf-8") as f:
        f.write(CSS)
    cover = os.path.join(FIG, "cover.png")
    meta = ["--metadata", "title=Liber Loagaeth — Anatomia de uma Língua Selada / Anatomy of a Sealed Language",
            "--metadata", "author=Astaron Eremita", "--metadata", "lang=pt-BR"]
    common = ["--toc", "--toc-depth=2", "--resource-path", f"{HERE}{os.pathsep}{OUT}"]

    epub = os.path.join(OUT, base + ".epub")
    a = common + meta + (["--epub-cover-image", cover] if os.path.exists(cover) else [])
    pypandoc.convert_file(tmp, "epub", format="markdown", outputfile=epub, extra_args=a)
    print(f"[combо] EPUB -> {epub}  ({os.path.getsize(epub)//1024} KB)")

    html = os.path.join(OUT, base + ".html")
    a = common + meta + ["--standalone", "--embed-resources", "--css", css_path]
    pypandoc.convert_file(tmp, "html5", format="markdown", outputfile=html, extra_args=a)
    print(f"[combо] HTML -> {html}  ({os.path.getsize(html)//1024} KB)")

    pdf = os.path.join(OUT, base + ".pdf")
    browser = CHROME if os.path.exists(CHROME) else EDGE
    prof = os.path.join(OUT, ".chrome_combo")
    cmd = [browser, "--headless=new", "--disable-gpu", "--no-sandbox",
           f"--user-data-dir={prof}", "--no-pdf-header-footer",
           f"--print-to-pdf={pdf}", "file:///" + html.replace("\\", "/")]
    subprocess.run(cmd, capture_output=True, text=True, timeout=240)
    print(f"[combо] PDF  -> {pdf}  ({os.path.getsize(pdf)//1024} KB)" if os.path.exists(pdf) else "[combо] PDF FALHOU")
    shutil.rmtree(prof, ignore_errors=True)

if __name__ == "__main__":
    args = sys.argv[1:] or ["pt"]
    if "combined" in args:
        build_combined()
    else:
        for l in args:
            build(l)
