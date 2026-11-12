from playwright.sync_api import sync_playwright
import os
OUT = os.path.dirname(os.path.abspath(__file__))

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
.row{display:flex;justify-content:space-between;padding:30px 0;border-bottom:2px solid #22272D;font-size:38px}
.row span:first-child{color:#8A9097}
.row span:last-child{font-weight:700;text-align:right}
.tag{display:inline-block;font-size:30px;font-weight:700;border:3px solid #E4F75A;color:#E4F75A;padding:10px 24px;border-radius:50px;margin-bottom:40px}
.card{background:#151A1F;border-radius:28px;padding:44px;margin-bottom:28px}
.card .k{font-size:30px;color:#E4F75A;font-weight:700;margin-bottom:10px}
.card .v{font-size:38px;line-height:1.5}
"""

def pixels(colors, pattern, x, y):
    cells = "".join(f'<i style="background:{colors[c]}"></i>' if c != '.' else '<i></i>' for row in pattern for c in row)
    cols = len(pattern[0])
    return f'<div class="px" style="left:{x}px;top:{y}px;grid-template-columns:repeat({cols},34px)">{cells}</div>'

C = {'r':'#E5484D','g':'#3FB66B','y':'#E4F75A','w':'#F2F2EE','d':'#2A3037'}
heart = ["..rr.rr..",".rrrrrrr.",".rrrrrrr.","..rrrrr..","...rrr...","....r...."]
blocks = ["rr..gg","rr..gg","..yy..","..yy..","gg..rr","gg..rr"]

def page(n, body, extra=""):
    return f"""<html><head><style>{CSS}</style></head><body>
<div class="top"><span>GEAR DROP</span><b>NEWS · {n}/5</b></div>
{extra}<div class="wrap">{body}</div>
<div class="foot"><span>@gear.drop.kr</span><span>{'넘겨보기 →' if n<5 else '저장 · 공유'}</span></div></body></html>"""

slides = [
 page(1, """
<div class="tag">FENDER × POKÉMON 30주년</div>
<h1>펜더가<br><span class="y">8비트 소리 나는</span><br>기타를 만들었다</h1>
<p style="margin-top:56px;font-size:42px">레드 스트랫 · 그린 텔레<br>메이드 인 재팬 한정판</p>
""", pixels(C, blocks, 760, 860)),
 page(2, """
<h2>두 모델, 두 버전</h2>
<div class="card"><div class="k" style="color:#E5484D">RED VERSION</div><div class="v">스트라토캐스터<br>로즈우드 지판 · 하이 아웃풋 싱글</div></div>
<div class="card"><div class="k" style="color:#3FB66B">GREEN VERSION</div><div class="v">텔레캐스터<br>메이플 지판 · 밸런스형 싱글</div></div>
<p style="margin-top:20px">초창기 게임 속 <span class="y">레드·그린 버전</span>에서<br>따온 컬러와 픽셀 아트 그래픽</p>
"""),
 page(3, """
<h2>진짜 포인트는<br><span class="y">8-Bit Sound System</span></h2>
<p>볼륨 노브를 조작하면<br>기타 소리에 <b style="color:#fff">8비트 신스 톤</b>이 더해짐</p>
<div class="card" style="margin-top:56px"><div class="k">그 외 디테일</div><div class="v">· 각도 따라 색 변하는 픽셀 픽가드<br>· 30주년 각인 넥 플레이트<br>· 전용 하드케이스 + 피크 틴(11장)</div></div>
""", pixels(C, heart, 700, 1010)),
 page(4, """
<h2>살 수 있나?</h2>
<div class="row"><span>판매 방식</span><span>추첨 판매</span></div>
<div class="row"><span>응모처</span><span>포켓몬센터 온라인</span></div>
<div class="row"><span>응모 기간</span><span>11.19 12:00 ~<br>11.24 16:59 (한국·일본 시간)</span></div>
<div class="row"><span>가격(보도 기준)</span><span class="y">39만 6천 엔</span></div>
<div class="row" style="border:0"><span>배송</span><span>일본 내 배송만</span></div>
<p style="margin-top:30px;font-size:30px;color:#8A9097">※ 해외 판매는 각 지역 공식 채널 공지 확인</p>
"""),
 page(5, """
<h2>여러분이라면?</h2>
<div class="card"><div class="v" style="font-size:46px">🔴 레드 스트랫 vs 🟢 그린 텔레</div></div>
<p style="margin-top:30px">댓글로 골라주세요 👇<br>40만 엔이면 산다 / 안 산다도 OK</p>
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
