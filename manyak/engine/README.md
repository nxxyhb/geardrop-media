# 만약에 3D 미니 엔진

- `engine.js` — 순수 WebGL1 렌더러(UV구·반구·박스·원기둥·원판·삼각기둥·산 메시, Lambert+반구 앰비언트+Blinn 하이라이트+림라이트+거리 안개, 반투명 후처리), 임계감쇠 스프링 카메라(`springCamera`, 결정적), 시리즈 표준 캐릭터(`drawCharacter`: 큰 머리·단발·타원 눈+하이라이트·볼·입·눈썹·팔다리, 놀람/점눈/말하기).
- `render.js` — Playwright(swiftshader)로 `window.renderAt(t)`를 프레임마다 찍어 ffmpeg로 mp4. `node render.js scene.html out.mp4` / 키 프레임: `node render.js scene.html --shots dir 0 3 6`.
- `build_scene.py` — 장면 HTML의 `<script src>`를 인라인해 한 장짜리 scene.html 생성.
- `sound_ep02.py` — numpy 피치카토 BGM·효과음·내레이션 덕킹 믹스(에피소드마다 복사해 타이밍만 바꿔 쓰기).
- 장면 예시: `../posts/2026-11-19-convenience-1plus1/scene.src.html` (HUD: 배지·제목·카운터·팝 텍스트·자막·엔딩 카드).
