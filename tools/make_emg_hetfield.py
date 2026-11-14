from playwright.sync_api import sync_playwright
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "posts", "2026-11-15-emg-hetfield-het-set")
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

C = {'y':'#E4F75A','w':'#F2F2EE','d':'#2A3037','g':'#8A9097','r':'#E5484D'}
# active humbucker (closed cover, black) + pole hints
hb = ["ddddddddd","dgdgdgdgd","ddddddddd","dyyyyyyyd","ddddddddd","dgdgdgdgd","ddddddddd"]
num50 = ["yyy.yyy","y...y.y","yyy.y.y","..y.y.y","yyy.yyy"]

def page(n, body, extra=""):
    return f"""<html><head><style>{CSS}</style></head><body>
<div class="top"><span>GEAR DROP</span><b>NEWS · {n}/{N}</b></div>
{extra}<div class="wrap">{body}</div>
<div class="foot"><span>@gear.drop.kr</span><span>{'넘겨보기 →' if n<N else '저장 · 공유'}</span></div></body></html>"""

slides = [
 page(1, """
<div class="tag">EMG · 창립 50주년 한정판</div>
<h1>헷필드가 직접<br><span class="y">디자인했다</span></h1>
<p style="margin-top:56px;font-size:42px">메탈리카 James Hetfield<br>시그니처 <b style="color:#fff">'Het Set'</b> 픽업</p>
<p style="margin-top:20px;font-size:34px;color:#8A9097">전 세계 <b class="y">200세트</b> 한정</p>
""", pixels(C, hb, 700, 900)),
 page(2, """
<h2>한정판 정보</h2>
<div class="row"><span>제품</span><span>EMG JH 'Het' 세트</span></div>
<div class="row"><span>수량</span><span class="y">200세트 한정</span></div>
<div class="row"><span>가격</span><span class="y">$299</span></div>
<div class="row"><span>판매</span><span>EMG 공식 직판</span></div>
<div class="row"><span>발매일</span><span>2026.11.13 (미국)</span></div>
<div class="row" style="border:0"><span>구성</span><span>JH-N(넥) + JH-B(브릿지)</span></div>
<p style="margin-top:24px;font-size:30px;color:#8A9097">※ 25k 볼륨·톤 팟, 스테레오 잭, 케이블 포함 (보도 기준)</p>
"""),
 page(3, """
<h2>포인트는 <span class="y">각인</span></h2>
<div class="card"><div class="k">50주년 로고</div><div class="v">헷필드가 <span class="y">메탈리카 폰트</span>로<br>직접 디자인한 로고를 픽업에 각인</div></div>
<div class="card"><div class="k">헷필드 코멘트</div><div class="v">"우리 메탈리카 폰트로<br>50주년 로고를 직접 디자인했다"</div></div>
<div class="card"><div class="k" style="color:#9AA0A6">EMG 50년</div><div class="v">1976년 창립 · 81/60 액티브 픽업으로<br>메탈 사운드의 상징이 된 브랜드</div></div>
"""),
 page(4, """
<h2>81/60과 뭐가 달라?</h2>
<div class="card"><div class="k">JH-N · 넥</div><div class="v">개별 세라믹 폴·보빈, 더 큰 코어<br>→ 어택·출력·저음 <span class="y">더 두툼하게</span></div></div>
<div class="card"><div class="k">JH-B · 브릿지</div><div class="v">81의 바 마그넷 대신 <span class="y">스틸 폴피스</span><br>→ 타이트한 어택 + 더 깔끔한 저음</div></div>
<p style="margin-top:20px;font-size:32px">EMG 측 "지금까지 만든 것 중<br><span class="y" style="font-weight:700">가장 어려운 세트</span>" (보도 기준)</p>
""", pixels(C, num50, 728, 1010)),
 page(5, """
<h2>여러분은?</h2>
<div class="card"><div class="v" style="font-size:44px">메탈 픽업 원픽은<br><span class="y">EMG 81/60 vs 패시브</span></div></div>
<p style="margin-top:30px">댓글로 알려주세요 👇<br>헷필드 리프 최애곡도 OK</p>
<p style="margin-top:80px;font-size:34px">해외 기타 소식, 한국어로 빠르게<br><span class="y" style="font-weight:700">팔로우 @gear.drop.kr</span></p>
"""),
]
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={'width':1080,'height':1350})
    for i, h in enumerate(slides, 1):
        pg.set_content(h); pg.wait_for_timeout(200)
        pg.screenshot(path=f"{OUT}/card{i}.jpg", type="jpeg", quality=92)
    b.close()
