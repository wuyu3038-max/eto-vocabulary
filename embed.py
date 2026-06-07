import re, subprocess

result = subprocess.run(["git","show","HEAD~1:index.html"], capture_output=True, text=True)
html = result.stdout

words = []
for m in re.finditer(r"a\('([^']+)','([^']+)','([^']+)','[^']*','([^']*)'\)", html):
    words.append((m.group(1), m.group(2), m.group(3), m.group(4)))

print("Found " + str(len(words)) + " words")

lines = []
for en, zh, cat, ex in words:
    en_s = en.replace("\\", "\\\\").replace("'", "\\'")
    zh_s = zh.replace("\\", "\\\\").replace("'", "\\'")
    cat_s = cat.replace("\\", "\\\\").replace("'", "\\'")
    ex_s = ex.replace("\\", "\\\\").replace("'", "\\'")
    lines.append("a('" + en_s + "','" + zh_s + "','" + cat_s + "','" + ex_s + "')")

words_js = "\n".join(lines)

with open("index.html", "r", encoding="utf-8") as f:
    new_html = f.read()

new_html = new_html.replace(
    "// (825 word entries go here — loaded from embedded data)",
    words_js
)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(new_html)

print("Embedded " + str(len(lines)) + " words")
