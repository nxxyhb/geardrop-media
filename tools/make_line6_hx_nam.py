from playwright.sync_api import sync_playwright
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "posts", "2026-11-17-line6-hx-nam-warning")
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

C = {'y':'#E4F75A','w':'#F2F2EE','d':'#2A3037','g':'#8A9097','r':'#B3263A','k':'#151A1F'}
# generic pixel multi-effect floor pedal (screen + knobs + footswitches)
pedal = [
 "dddddddddddd",
 "dkkkkkkkkkkd",
 "dkyyyyyyyykd",
 "dkyddddddykd",
 "dkyyyyyyyykd",
 "dkkkkkkkkkkd",
 "dkwkwkwkwkkd",
 "dkkkkkkkkkkd",
 "dkgkkgkkgkkd",
 "dkrkkykkgkkd",
 "dddddddddddd",
]
warn = ["..y..",".yyy.",".y.y.","yy.yy","yyyyy","yy.yy","yyyyy"]

def page(n, body, extra=""):
    return f"""<html><head><style>{CSS}</style></head><body>
<div class="top"><span>GEAR DROP</span><b>NEWS · {n}/{N}</b></div>
{extra}<div class="wrap">{body}</div>
<div class="foot"><span>@gear.drop.kr</span><span>{'넘겨보기 →' if n<N else '저장 · 공유'}</span></div></body></html>"""

slides = [
 page(1, """
<div class="tag">LINE 6 · HX × NAM</div>
<h1>HX 스톰프에<br>NAM 깔았다면<br><span class="y">잠깐!</span></h1>
<p style="margin-top:50px;font-size:42px">라인6, 비공식 펌웨어에<br><b style="color:#fff">공식 경고</b> 날렸다</p>
<p style="margin-top:20px;font-size:34px;color:#8A9097">2026.11.16 · Guitar World 보도</p>
""", pixels(C, pedal, 640, 700)),
 page(2, """
<h2>무슨 <span class="y">일?</span></h2>
<div class="card"><div class="k">NAM A2</div><div class="v">TONE3000의 <span class="y">오픈소스</span> 앰프 모델링<br>올여름 공개된 2세대 아키텍처</div></div>
<div class="card"><div class="k">비공식 펌웨어</div><div class="v">유저들이 만든 수정 펌웨어로<br><span class="y">HX Stomp · Helix · POD Go</span>에서<br>NAM A2 구동 성공</div></div>
<div class="card"><div class="k">라인6 반응</div><div class="v">모회사 야마하 고객지원 총괄<br>Frank Ritchotte가 SNS로 경고</div></div>
"""),
 page(3, """
<h2>라인6가 꼽은 <span class="y">리스크</span></h2>
<div class="row"><span>01</span><span>향후 공식 업데이트와 충돌</span></div>
<div class="row"><span>02</span><span>고객지원 진단이 복잡해짐</span></div>
<div class="row"><span>03</span><span>공식 개발팀도 못 고치는 문제</span></div>
<div class="row" style="border:0"><span>04</span><span class="y">보증 포기 가능성</span></div>
<p style="margin-top:40px;font-size:34px;color:#8A9097">"아직 출시 안 된 기능과의 상호작용은<br>테스트할 수 없다" — 라인6 측<br>※ 보증 관련은 Guitar World 보도 기준</p>
"""),
 page(4, """
<h2>다른 브랜드는 <span class="y">벌써</span></h2>
<div class="chips"><span>Blackstar</span><span>Zoom</span><span>Fender</span></div>
<div class="card"><div class="k">Blackstar</div><div class="v">Beam Mini로 NAM A2 <span class="y">첫 네이티브 지원</span></div></div>
<div class="card"><div class="k">Zoom · Fender</div><div class="v">줌 지원 합류 · 펜더는<br>Tone Master Pro 통합 작업 중</div></div>
<div class="card"><div class="k">Line 6</div><div class="v">"공식 지원 온다, 기다려 달라"<br><span class="y">일정은 미정</span></div></div>
"""),
 page(5, """
<h2>여러분은?</h2>
<div class="card"><div class="v" style="font-size:44px">내 HX에 NAM,<br><span class="y">지금 깐다 vs 공식 기다린다</span></div></div>
<p style="margin-top:30px">댓글로 알려주세요 👇<br>써본 분은 후기도 환영</p>
<p style="margin-top:80px;font-size:34px">해외 기타 소식, 한국어로 빠르게<br><span class="y" style="font-weight:700">팔로우 @gear.drop.kr</span></p>
""", pixels(C, warn, 798, 880)),
]
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={'width':1080,'height':1350})
    for i, h in enumerate(slides, 1):
        pg.set_content(h); pg.wait_for_timeout(200)
        pg.screenshot(path=f"{OUT}/card{i}.jpg", type="jpeg", quality=92)
    b.close()
