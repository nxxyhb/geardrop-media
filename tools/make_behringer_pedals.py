from playwright.sync_api import sync_playwright
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "posts", "2026-11-14-behringer-10-dollar-pedals")
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
# simple stompbox: knobs, LED, footswitch
pedal = ["yyyyyyy","ywydywy","yyyyyyy","yyyryyy","yyyyyyy","yyyyyyy","yyywyyy","yyyyyyy"]
coin = [".yyyy.","yy..yy","y.yy.y","y.yy.y","yy..yy",".yyyy."]

def page(n, body, extra=""):
    return f"""<html><head><style>{CSS}</style></head><body>
<div class="top"><span>GEAR DROP</span><b>NEWS · {n}/{N}</b></div>
{extra}<div class="wrap">{body}</div>
<div class="foot"><span>@gear.drop.kr</span><span>{'넘겨보기 →' if n<N else '저장 · 공유'}</span></div></body></html>"""

slides = [
 page(1, """
<div class="tag">BEHRINGER · 페달 대량 예고</div>
<h1>이펙터 하나에<br><span class="y">10~15달러?</span></h1>
<p style="margin-top:56px;font-size:42px">베링거, 올메탈 페달<br><b style="color:#fff">200~300종</b> 출시 예고</p>
<p style="margin-top:20px;font-size:30px;color:#8A9097">개당 약 1.5~2만 원대 (환율 단순 환산)</p>
""", pixels(C, pedal, 760, 840)),
 page(2, """
<h2>뭘 예고했나</h2>
<div class="row"><span>규모</span><span>200~300종</span></div>
<div class="row"><span>가격</span><span class="y">개당 $10~15</span></div>
<div class="row"><span>구성</span><span>아날로그 + 디지털</span></div>
<div class="row"><span>바디</span><span>올메탈</span></div>
<div class="row"><span>발표 채널</span><span>베링거 공식 페이스북</span></div>
<div class="row" style="border:0"><span>출시일</span><span>미정 (비공개)</span></div>
<p style="margin-top:24px;font-size:30px;color:#8A9097">※ 11월 초 SNS 예고 기준, 정식 출시 전</p>
"""),
 page(3, """
<h2>라인업 힌트</h2>
<p style="margin-bottom:30px">예고 사진에 보인 종류</p>
<div class="chips"><span>디스토션</span><span>오버드라이브</span><span>퍼즈</span><span>딜레이</span><span>리버브</span><span>페이저</span><span>코러스</span><span>옥타버</span><span>비브라토</span><span>미니 페달</span></div>
<div class="card"><div class="k">눈에 띄는 포인트</div><div class="v">· 전설적 클래식 페달부터 새 디자인까지<br>· 직접 개조 가능한 <span class="y">오픈소스</span> 페달 언급<br>· 베이스용도 고려 중 (댓글 답변)</div></div>
""", pixels(C, coin, 760, 940)),
 page(4, """
<h2>그리고 <span class="y">논란</span></h2>
<div class="card"><div class="k">베링거 게시물 문구</div><div class="v">"부티크 페달 업체들이<br>좀 언짢아할까? 아마도."</div></div>
<div class="card"><div class="k" style="color:#E5484D">반발</div><div class="v">영국 부티크 제작사 Intensive Care Audio<br>"소규모 제작자를 조롱한다" 공개 비판</div></div>
<div class="card"><div class="k" style="color:#9AA0A6">옹호</div><div class="v">클래식 톤을 누구나 싸게 쓸 수 있다<br>vs 결국 카피 아니냐 (클론 분쟁 전례)</div></div>
"""),
 page(5, """
<h2>여러분은?</h2>
<div class="card"><div class="v" style="font-size:44px">1~2만 원대 베링거 페달<br><span class="y">산다 vs 안 산다</span></div></div>
<p style="margin-top:30px">댓글로 알려주세요 👇<br>제일 먼저 나왔으면 하는 페달도 OK</p>
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
