# inline engine.js + hud.css into scene.src.html -> scene.html (single standalone file)
import sys, re, os
src = sys.argv[1]; out = sys.argv[2]
d = os.path.dirname(os.path.abspath(src))
html = open(src, encoding='utf-8').read()
def rep(m):
    p = os.path.normpath(os.path.join(d, m.group(1)))
    return '<script>\n' + open(p, encoding='utf-8').read() + '\n</script>'
html = re.sub(r'<script src="([^"]+)"></script>', rep, html)
def rep_css(m):
    p = os.path.normpath(os.path.join(d, m.group(1)))
    return '<style>\n' + open(p, encoding='utf-8').read() + '\n</style>'
html = re.sub(r'<link rel="stylesheet" href="([^"]+)">', rep_css, html)
open(out, 'w', encoding='utf-8').write(html)
print('built', out)
