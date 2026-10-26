"""Собирает index.html из src/template.html: вшивает фото и логотипы.
Запуск из корня репозитория:  python3 src/build.py
"""
import base64, json, os
SRC = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SRC)
t = open(os.path.join(SRC, "template.html"), encoding="utf-8").read()
def svg(n):
    return open(os.path.join(SRC, "logos", n), encoding="utf-8").read().replace('<svg ', '<svg aria-hidden="true" focusable="false" ')
imgs = {n: "data:image/jpeg;base64," + base64.b64encode(open(os.path.join(SRC, "img", n + ".jpg"), "rb").read()).decode()
        for n in ["taper-single", "flame-pair", "taper-pair", "pillar", "aroma"]}
tex = {}
for f in sorted(os.listdir(os.path.join(SRC, "tex"))):
    k, ext = os.path.splitext(f)
    mime = "image/png" if ext == ".png" else "image/jpeg"
    tex[k] = "data:%s;base64,%s" % (mime, base64.b64encode(open(os.path.join(SRC, "tex", f), "rb").read()).decode())
t = t.replace("{{TEX_JSON}}", json.dumps(tex))
t = (t.replace("{{IMG_JSON}}", json.dumps(imgs)).replace("{{LOGO_WORD}}", svg("wordmark.svg"))
      .replace("{{LOGO_HORIZ}}", svg("horiz.svg")).replace("{{LOGO_STAMP}}", svg("stamp.svg"))
      .replace("{{LOGO_STACK}}", svg("stack2.svg")))
assert "{{" not in t
head = ('<!doctype html>\n<html lang="ru">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        '<meta name="description" content="Потемки — маленький свечной заводик. Свечи ручной работы из оливкового, пчелиного и соевого воска.">\n'
        '<style>:root{padding-top:env(safe-area-inset-top);padding-bottom:env(safe-area-inset-bottom)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n')
i = t.index('<div class="marquee"')
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(head + t[:i] + "</head>\n<body>\n" + t[i:] + "\n</body>\n</html>\n")
# тело без обёртки — для превью-артефакта в Claude
open(os.path.join(ROOT, "src", "artifact.html"), "w", encoding="utf-8").write(t)
print("index.html собран")
