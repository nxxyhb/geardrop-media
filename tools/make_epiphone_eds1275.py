from playwright.sync_api import sync_playwright
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "posts", "2026-11-16-epiphone-eds1275-doubleneck")
os.makedirs(OUT, exist_ok=True)
N = 5

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;background:#0C0F12;color:#F2F2EE;font-family:'Noto Sans CJK KR';overflow:hidden;position:relative}
.y{color:#E4F75A}
.top{position:absolute;top:64px;left:72px;right:72px;display:flex;justify-content:space-between;align-items:center;font-size:26px;font-weight:700;letter-spacing:4px;color:#9AA0A6}
.top b{color:#0C0F12;background:#E4F75A;padding:8px 18px;border-radius:40px;letter-spacing:2px}
.wrap{position:absolute;left:72px;right:72px;top:190px}
.foot{position:absolute;bottom:60px;left:72px;right:72px;display:flex;justify-content:space-between;font-size:24px;color:#6B7178;letter-spacing:2px}
.px{position:absolute;display:grid;gap:6px}
.px i{width:34px;height:34px;display:block}
h1{font-size:96px;line-height:1.12;font-weight:900;letter-spacing:-2px}
h2{font-size:64px;line-height:1.2;font-weight:900;letter-spacing:-1px;margin-bottom:48px}
p{font-size:38px;line-height:1.6;color:#C9CDD1}
.row{display:flex;justify-content:space-between;padding:28px 0;border-bottom:2px solid #22272D;font-size:38px}
.row span:first-child{color:#8A9097}
.row span:last-child{font-weight:700;text-align:right}
.tag{display:inline-block;font-size:30px;font-weight:700;border:3px solid #E4F75A;color:#E4F75A;padding:10px 24px;border-radius:50px;margin-bottom:40px}
.card{background:#151A1F;border-radius:28px;padding:40px 44px;margin-bottom:26px}
.card .k{font-size:30px;color:#E4F75A;font-weight:700;margin-bottom:10px}
.card .v{font-size:36px;line-height:1.5}
.chips{display:flex;flex-wrap:wrap;gap:16px;margin-bottom:40px}
.chips span{font-size:32px;font-weight:700;background:#151A1F;border:2px solid #2A3037;border-radius:40px;padding:12px 26px}
"""

def pixels(colors, pattern, x, y):
    cells = "".join(f'<i style="background:{colors[c]}"></i>' if c != '.' else '<i></i>' for row in pattern for c in row)
    cols = len(pattern[0])
    return f'<div class="px" style="left:{x}px;top:{y}px;grid-template-columns:repeat({cols},34px)">{cells}</div>'

C = {'y':'#E4F75A','w':'#F2F2EE','d':'#2A3037','g':'#8A9097','r':'#B3263A'}
# generic pixel double-neck silhouette (two necks + SG-style body)
dn = [
 ".gg.....gg.",
 ".gg.....gg.",
 "..d......d.",
 "..d......d.",
 "..d......d.",
 "..d......d.",
 "..d......d.",
 "rrdrr..rrdr",
 "rrdrrrrrrdr",
 ".rwyrrrrwyr",
 ".rrrrrrrrr.",
 ".rwyrrrrwyr",
 "rrrrrrrrrrr",
 "rrrr...rrrr",
]
num2 = ["yy..yyy",".y....y",".y..yyy",".y..y..","yyy.yyy"]

def page(n, body, extra=""):
    return f"""<html><head><style>{CSS}</style></head><body>
<div class="top"><span>GEAR DROP</span><b>NEWS · {n}/{N}</b></div>
{extra}<div class="wrap">{body}</div>
<div class="foot"><span>@gear.drop.kr</span><span>{'넘겨보기 →' if n<N else '저장 · 공유'}</span></div></body></html>"""

slides = [
 page(1, """
<div class="tag">EPIPHONE · EDS-1275 리프레시</div>
<h1>지미 페이지의<br>그 더블넥,<br><span class="y">$999</span></h1>
<p style="margin-top:50px;font-size:42px">12현 + 6현 한 몸에<br>에피폰 <b style="color:#fff">EDS-1275</b> 새 버전</p>
<p style="margin-top:20px;font-size:34px;color:#8A9097">2026.11.11 공개 · Gibson 공식 발표</p>
""", pixels(C, dn, 580, 640)),
 page(2, """
<h2>뭐가 <span class="y">바뀌었나</span></h2>
<div class="card"><div class="k">지판</div><div class="v">두 넥 모두 <span class="y">리얼 로즈우드</span> 지판<br>바인딩 + 펄로이드 인레이</div></div>
<div class="card"><div class="k">픽업</div><div class="v">에피폰 <span class="y">ProBucker</span> 탑재<br>넥 ProBucker 2 · 브릿지 ProBucker 3</div></div>
<div class="card"><div class="k">하드웨어</div><div class="v">LockTone 튠오매틱 · CTS 팟<br>Graph Tech 너트 · 하드케이스 포함</div></div>
"""),
 page(3, """
<h2>스펙 정리</h2>
<div class="row"><span>바디</span><span>솔리드 마호가니</span></div>
<div class="row"><span>넥</span><span>마호가니 셋넥 × 2</span></div>
<div class="row"><span>구성</span><span class="y">위 12현 · 아래 6현</span></div>
<div class="row"><span>넥 쉐입</span><span>SlimTaper C</span></div>
<div class="row"><span>스케일</span><span>24.75" · 20프렛</span></div>
<div class="row"><span>지판 R</span><span>12"</span></div>
<div class="row" style="border:0"><span>컨트롤</span><span>넥별 볼륨·톤 + 넥 선택 3웨이</span></div>
"""),
 page(4, """
<h2>컬러 3종 · <span class="y">$999</span></h2>
<div class="card"><div class="k" style="color:#E5484D">Vintage Cherry</div><div class="v">니켈 하드웨어 · 기본 컬러</div></div>
<div class="card"><div class="k" style="color:#F2F2EE">Alpine White</div><div class="v"><span class="y">골드</span> 하드웨어 · Gibson 독점</div></div>
<div class="card"><div class="k" style="color:#7FB3D5">Pelham Blue</div><div class="v">니켈 하드웨어 · Gibson 독점</div></div>
<p style="margin-top:16px;font-size:30px;color:#8A9097">※ 미국 Gibson 공식몰 기준 $999 (각 컬러 동일)<br>※ 국내 출시·가격은 아직 미발표</p>
"""),
 page(5, """
<h2>여러분은?</h2>
<div class="card"><div class="v" style="font-size:44px">더블넥 기타,<br><span class="y">로망 vs 어깨 박살</span></div></div>
<p style="margin-top:30px">댓글로 알려주세요 👇<br>더블넥 하면 떠오르는 곡도 OK</p>
<p style="margin-top:80px;font-size:34px">해외 기타 소식, 한국어로 빠르게<br><span class="y" style="font-weight:700">팔로우 @gear.drop.kr</span></p>
""", pixels(C, num2, 728, 1010)),
]
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={'width':1080,'height':1350})
    for i, h in enumerate(slides, 1):
        pg.set_content(h); pg.wait_for_timeout(200)
        pg.screenshot(path=f"{OUT}/card{i}.jpg", type="jpeg", quality=92)
    b.close()
