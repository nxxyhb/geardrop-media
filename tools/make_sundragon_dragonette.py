from playwright.sync_api import sync_playwright
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "posts", "2026-11-18-jimmy-page-sundragon-dragonette")
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

C = {'y':'#E4F75A','w':'#F2F2EE','d':'#2A3037','g':'#8A9097','r':'#B3263A','k':'#151A1F','b':'#6B4A2E','t':'#C9A86A'}
# generic pixel 1x10 tube combo (cabinet, grille, control panel, glowing tubes)
amp = [
 "bbbbbbbbbbbb",
 "bkgkgkgkgkkb",
 "bbbbbbbbbbbb",
 "bttttttttttb",
 "bttddddddttb",
 "btdddyydddtb",
 "btddyddyddtb",
 "btddyddyddtb",
 "btdddyydddtb",
 "bttddddddttb",
 "bttttttttttb",
 "bbbbbbbbbbbb",
]
tube = [".w.","wyw","wyw","wyw","ddd"]
q = ["..yyy..",".y...y.","....y..","...y...","...y...",".......","...y..."]

def page(n, body, extra=""):
    return f"""<html><head><style>{CSS}</style></head><body>
<div class="top"><span>GEAR DROP</span><b>NEWS · {n}/{N}</b></div>
{extra}<div class="wrap">{body}</div>
<div class="foot"><span>@gear.drop.kr</span><span>{'넘겨보기 →' if n<N else '저장 · 공유'}</span></div></body></html>"""

slides = [
 page(1, """
<div class="tag">JIMMY PAGE × SUNDRAGON</div>
<h1>레드 제플린 1집<br>그 앰프 소리,<br><span class="y">6와트에 담았다</span></h1>
<p style="margin-top:50px;font-size:42px">지미 페이지 시그니처 콤보<br><b style="color:#fff">'Dragonette'</b> · 단 50대</p>
<p style="margin-top:20px;font-size:34px;color:#8A9097">Guitar World · MusicRadar 보도</p>
""", pixels(C, amp, 640, 760)),
 page(2, """
<h2>어떤 <span class="y">앰프?</span></h2>
<div class="row"><span>출력</span><span>6W 진공관</span></div>
<div class="row"><span>구성</span><span>1×10" 콤보</span></div>
<div class="row"><span>프리앰프</span><span>Sundragon Nymph 계열</span></div>
<div class="row"><span>파워부</span><span>페이지 원본 앰프 기반</span></div>
<div class="row" style="border:0"><span>제작</span><span class="y">뉴욕 핸드와이어드 · NOS 부품</span></div>
<p style="margin-top:36px;font-size:34px;color:#8A9097">"옛것과 새것의 완벽한 조합" — 지미 페이지</p>
"""),
 page(3, """
<h2>원본은 <span class="y">개조 Supro</span></h2>
<div class="card"><div class="k">LED ZEPPELIN I</div><div class="v">펜더 텔레캐스터 + 개조한<br><span class="y">Supro Coronado</span>로 1집 녹음</div></div>
<div class="card"><div class="k">SUNDRAGON</div><div class="v">페이지 · 프로듀서 Perry Margouleff ·<br>전 Park 앰프 오너 Mitch Colby가 함께</div></div>
<div class="card"><div class="k">계보</div><div class="v">Sundragon(2019) → Nymph →<br>Super Dragon → <span class="y">Dragonette</span></div></div>
""", pixels(C, tube, 870, 190)),
 page(4, """
<h2>가격은 <span class="y">약 $9,000</span></h2>
<div class="chips"><span>50대 한정</span><span>페이지 친필 사인</span><span>주문 제작</span></div>
<div class="card"><div class="k">가격</div><div class="v">약 9,000달러<br><span style="color:#8A9097;font-size:30px">(원화 환산 약 1,300만 원 안팎 · 보도 기준, 세금·배송 별도)</span></div></div>
<div class="card"><div class="k">남은 수량</div><div class="v">MusicRadar 보도 시점<br><span class="y">50대 중 8대만 남음</span></div></div>
"""),
 page(5, """
<h2>여러분은?</h2>
<div class="card"><div class="v" style="font-size:44px">6와트 앰프에 약 1,300만 원,<br><span class="y">로망이다 vs 선 넘었다</span></div></div>
<p style="margin-top:30px">댓글로 알려주세요 👇<br>내 최애 지미 페이지 리프도 환영</p>
<p style="margin-top:80px;font-size:34px">해외 기타 소식, 한국어로 빠르게<br><span class="y" style="font-weight:700">팔로우 @gear.drop.kr</span></p>
""", pixels(C, q, 798, 860)),
]
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={'width':1080,'height':1350})
    for i, h in enumerate(slides, 1):
        pg.set_content(h); pg.wait_for_timeout(200)
        pg.screenshot(path=f"{OUT}/card{i}.jpg", type="jpeg", quality=92)
    b.close()
