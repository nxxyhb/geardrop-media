(()=>{const c=CUR_CAM;const f=v3.norm(v3.sub(c.look,c.pos));const r=v3.norm([-f[2],0,f[0]]);const out={};
const items=[['hero',window.__head,0.55],['g',window.__gh,0.55],['cap',window.__gcap,0.5]];
for(const [k,H,R] of items){if(!H)continue;const xs=[proj(v3.add(H,v3.mul(r,-R)))[0],proj(v3.add(H,v3.mul(r,R)))[0]];out[k]=[Math.round(Math.min(...xs)),Math.round(Math.max(...xs)),Math.round(proj(v3.add(H,[0,R,0]))[1])]}
const sub=document.querySelector('#counter .sub');if(sub){const b=sub.getBoundingClientRect();out.chipBottom=Math.round(b.bottom);out.chipOp=getComputedStyle(document.getElementById('counterRow')).opacity}
return out})()
