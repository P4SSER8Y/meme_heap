import{c as I,d,h as $,e as X,u as ve,f as fe,g as me,P as Ke,i as Xe,j as P,n as Ue,l as Ye,k as R,p as ne,m as we,s as ie,o as se,q as re,r as Ee,t as Ge,v as Je,w as Ze,x as et,y as le,z as tt,A as E,B as at,C as nt,D as g,E as it,F as ke,G as rt,H as lt,I as qe,J as ut,K as ot,L as st,M as dt,N as ct,O as $e,Q as F,R as H,S as _,T as C,U as vt,V as ft,W as K,X as de,Y as mt,Z as ht,_ as yt,$ as bt,a0 as pt,a1 as gt,a2 as wt,a3 as kt,a4 as qt,a5 as Ct,a6 as Ce,a7 as _t}from"./index.c7127962.js";import{_ as De}from"./plugin-vue_export-helper.21dcd24c.js";var ce=I({name:"QItemLabel",props:{overline:Boolean,caption:Boolean,header:Boolean,lines:[Number,String]},setup(e,{slots:i}){const l=d(()=>parseInt(e.lines,10)),h=d(()=>"q-item__label"+(e.overline===!0?" q-item__label--overline text-overline":"")+(e.caption===!0?" q-item__label--caption text-caption":"")+(e.header===!0?" q-item__label--header":"")+(l.value===1?" ellipsis":"")),t=d(()=>e.lines!==void 0&&l.value>1?{overflow:"hidden",display:"-webkit-box","-webkit-box-orient":"vertical","-webkit-line-clamp":l.value}:null);return()=>$("div",{style:t.value,class:h.value},X(i.default))}}),Bt=I({name:"QList",props:{...ve,bordered:Boolean,dense:Boolean,separator:Boolean,padding:Boolean,tag:{type:String,default:"div"}},setup(e,{slots:i}){const l=me(),h=fe(e,l.proxy.$q),t=d(()=>"q-list"+(e.bordered===!0?" q-list--bordered":"")+(e.dense===!0?" q-list--dense":"")+(e.separator===!0?" q-list--separator":"")+(h.value===!0?" q-list--dark":"")+(e.padding===!0?" q-list--padding":""));return()=>$(e.tag,{class:t.value},X(i.default))}});const he={left:!0,right:!0,up:!0,down:!0,horizontal:!0,vertical:!0},Lt=Object.keys(he);he.all=!0;function _e(e){const i={};for(const l of Lt)e[l]===!0&&(i[l]=!0);return Object.keys(i).length===0?he:(i.horizontal===!0?i.left=i.right=!0:i.left===!0&&i.right===!0&&(i.horizontal=!0),i.vertical===!0?i.up=i.down=!0:i.up===!0&&i.down===!0&&(i.vertical=!0),i.horizontal===!0&&i.vertical===!0&&(i.all=!0),i)}function Be(e,i){return i.event===void 0&&e.target!==void 0&&e.target.draggable!==!0&&typeof i.handler=="function"&&e.target.nodeName.toUpperCase()!=="INPUT"&&(e.qClonedBy===void 0||e.qClonedBy.indexOf(i.uid)===-1)}function St(){if(window.getSelection!==void 0){const e=window.getSelection();e.empty!==void 0?e.empty():e.removeAllRanges!==void 0&&(e.removeAllRanges(),Ke.is.mobile!==!0&&e.addRange(document.createRange()))}else document.selection!==void 0&&document.selection.empty()}function ue(e,i,l){const h=se(e);let t,n=h.left-i.event.x,o=h.top-i.event.y,f=Math.abs(n),c=Math.abs(o);const s=i.direction;s.horizontal===!0&&s.vertical!==!0?t=n<0?"left":"right":s.horizontal!==!0&&s.vertical===!0?t=o<0?"up":"down":s.up===!0&&o<0?(t="up",f>c&&(s.left===!0&&n<0?t="left":s.right===!0&&n>0&&(t="right"))):s.down===!0&&o>0?(t="down",f>c&&(s.left===!0&&n<0?t="left":s.right===!0&&n>0&&(t="right"))):s.left===!0&&n<0?(t="left",f<c&&(s.up===!0&&o<0?t="up":s.down===!0&&o>0&&(t="down"))):s.right===!0&&n>0&&(t="right",f<c&&(s.up===!0&&o<0?t="up":s.down===!0&&o>0&&(t="down")));let r=!1;if(t===void 0&&l===!1){if(i.event.isFirst===!0||i.event.lastDir===void 0)return{};t=i.event.lastDir,r=!0,t==="left"||t==="right"?(h.left-=n,f=0,n=0):(h.top-=o,c=0,o=0)}return{synthetic:r,payload:{evt:e,touch:i.event.mouse!==!0,mouse:i.event.mouse===!0,position:h,direction:t,isFirst:i.event.isFirst,isFinal:l===!0,duration:Date.now()-i.event.time,distance:{x:f,y:c},offset:{x:n,y:o},delta:{x:h.left-i.event.lastX,y:h.top-i.event.lastY}}}}let Et=0;var oe=Xe({name:"touch-pan",beforeMount(e,{value:i,modifiers:l}){if(l.mouse!==!0&&P.has.touch!==!0)return;function h(n,o){l.mouse===!0&&o===!0?Ee(n):(l.stop===!0&&ie(n),l.prevent===!0&&we(n))}const t={uid:"qvtp_"+Et++,handler:i,modifiers:l,direction:_e(l),noop:Ue,mouseStart(n){Be(n,t)&&Ye(n)&&(R(t,"temp",[[document,"mousemove","move","notPassiveCapture"],[document,"mouseup","end","passiveCapture"]]),t.start(n,!0))},touchStart(n){if(Be(n,t)){const o=n.target;R(t,"temp",[[o,"touchmove","move","notPassiveCapture"],[o,"touchcancel","end","passiveCapture"],[o,"touchend","end","passiveCapture"]]),t.start(n)}},start(n,o){if(P.is.firefox===!0&&ne(e,!0),t.lastEvt=n,o===!0||l.stop===!0){if(t.direction.all!==!0&&(o!==!0||t.modifiers.mouseAllDir!==!0&&t.modifiers.mousealldir!==!0)){const s=n.type.indexOf("mouse")>-1?new MouseEvent(n.type,n):new TouchEvent(n.type,n);n.defaultPrevented===!0&&we(s),n.cancelBubble===!0&&ie(s),Object.assign(s,{qKeyEvent:n.qKeyEvent,qClickOutside:n.qClickOutside,qAnchorHandled:n.qAnchorHandled,qClonedBy:n.qClonedBy===void 0?[t.uid]:n.qClonedBy.concat(t.uid)}),t.initialEvent={target:n.target,event:s}}ie(n)}const{left:f,top:c}=se(n);t.event={x:f,y:c,time:Date.now(),mouse:o===!0,detected:!1,isFirst:!0,isFinal:!1,lastX:f,lastY:c}},move(n){if(t.event===void 0)return;const o=se(n),f=o.left-t.event.x,c=o.top-t.event.y;if(f===0&&c===0)return;t.lastEvt=n;const s=t.event.mouse===!0,r=()=>{h(n,s);let y;l.preserveCursor!==!0&&l.preservecursor!==!0&&(y=document.documentElement.style.cursor||"",document.documentElement.style.cursor="grabbing"),s===!0&&document.body.classList.add("no-pointer-events--children"),document.body.classList.add("non-selectable"),St(),t.styleCleanup=v=>{if(t.styleCleanup=void 0,y!==void 0&&(document.documentElement.style.cursor=y),document.body.classList.remove("non-selectable"),s===!0){const L=()=>{document.body.classList.remove("no-pointer-events--children")};v!==void 0?setTimeout(()=>{L(),v()},50):L()}else v!==void 0&&v()}};if(t.event.detected===!0){t.event.isFirst!==!0&&h(n,t.event.mouse);const{payload:y,synthetic:v}=ue(n,t,!1);y!==void 0&&(t.handler(y)===!1?t.end(n):(t.styleCleanup===void 0&&t.event.isFirst===!0&&r(),t.event.lastX=y.position.left,t.event.lastY=y.position.top,t.event.lastDir=v===!0?void 0:y.direction,t.event.isFirst=!1));return}if(t.direction.all===!0||s===!0&&(t.modifiers.mouseAllDir===!0||t.modifiers.mousealldir===!0)){r(),t.event.detected=!0,t.move(n);return}const p=Math.abs(f),w=Math.abs(c);p!==w&&(t.direction.horizontal===!0&&p>w||t.direction.vertical===!0&&p<w||t.direction.up===!0&&p<w&&c<0||t.direction.down===!0&&p<w&&c>0||t.direction.left===!0&&p>w&&f<0||t.direction.right===!0&&p>w&&f>0?(t.event.detected=!0,t.move(n)):t.end(n,!0))},end(n,o){if(t.event!==void 0){if(re(t,"temp"),P.is.firefox===!0&&ne(e,!1),o===!0)t.styleCleanup!==void 0&&t.styleCleanup(),t.event.detected!==!0&&t.initialEvent!==void 0&&t.initialEvent.target.dispatchEvent(t.initialEvent.event);else if(t.event.detected===!0){t.event.isFirst===!0&&t.handler(ue(n===void 0?t.lastEvt:n,t).payload);const{payload:f}=ue(n===void 0?t.lastEvt:n,t,!0),c=()=>{t.handler(f)};t.styleCleanup!==void 0?t.styleCleanup(c):c()}t.event=void 0,t.initialEvent=void 0,t.lastEvt=void 0}}};if(e.__qtouchpan=t,l.mouse===!0){const n=l.mouseCapture===!0||l.mousecapture===!0?"Capture":"";R(t,"main",[[e,"mousedown","mouseStart",`passive${n}`]])}P.has.touch===!0&&R(t,"main",[[e,"touchstart","touchStart",`passive${l.capture===!0?"Capture":""}`],[e,"touchmove","noop","notPassiveCapture"]])},updated(e,i){const l=e.__qtouchpan;l!==void 0&&(i.oldValue!==i.value&&(typeof value!="function"&&l.end(),l.handler=i.value),l.direction=_e(i.modifiers))},beforeUnmount(e){const i=e.__qtouchpan;i!==void 0&&(i.event!==void 0&&i.end(),re(i,"main"),re(i,"temp"),P.is.firefox===!0&&ne(e,!1),i.styleCleanup!==void 0&&i.styleCleanup(),delete e.__qtouchpan)}});function j(e,i,l){return l<=i?i:Math.min(l,Math.max(i,e))}const Le=150;var $t=I({name:"QDrawer",inheritAttrs:!1,props:{...Ge,...ve,side:{type:String,default:"left",validator:e=>["left","right"].includes(e)},width:{type:Number,default:300},mini:Boolean,miniToOverlay:Boolean,miniWidth:{type:Number,default:57},breakpoint:{type:Number,default:1023},showIfAbove:Boolean,behavior:{type:String,validator:e=>["default","desktop","mobile"].includes(e),default:"default"},bordered:Boolean,elevated:Boolean,overlay:Boolean,persistent:Boolean,noSwipeOpen:Boolean,noSwipeClose:Boolean,noSwipeBackdrop:Boolean},emits:[...Je,"onLayout","miniState"],setup(e,{slots:i,emit:l,attrs:h}){const t=me(),{proxy:{$q:n}}=t,o=fe(e,n),{preventBodyScroll:f}=ut(),{registerTimeout:c,removeTimeout:s}=Ze(),r=et(tt,le);if(r===le)return console.error("QDrawer needs to be child of QLayout"),le;let p,w,y;const v=E(e.behavior==="mobile"||e.behavior!=="desktop"&&r.totalWidth.value<=e.breakpoint),L=d(()=>e.mini===!0&&v.value!==!0),k=d(()=>L.value===!0?e.miniWidth:e.width),m=E(e.showIfAbove===!0&&v.value===!1?!0:e.modelValue===!0),W=d(()=>e.persistent!==!0&&(v.value===!0||Me.value===!0));function b(a,u){if(xe(),a!==!1&&r.animate(),B(0),v.value===!0){const q=r.instances[V.value];q!==void 0&&q.belowBreakpoint===!0&&q.hide(!1),D(1),r.isContainer.value!==!0&&f(!0)}else D(0),a!==!1&&ee(!1);c(()=>{a!==!1&&ee(!0),u!==!0&&l("show",a)},Le)}function O(a,u){Te(),a!==!1&&r.animate(),D(0),B(T.value*k.value),te(),u!==!0?c(()=>{l("hide",a)},Le):s()}const{show:U,hide:Q}=at({showing:m,hideOnRouteChange:W,handleShow:b,handleHide:O}),{addToHistory:xe,removeFromHistory:Te}=nt(m,Q,W),z={belowBreakpoint:v,hide:Q},S=d(()=>e.side==="right"),T=d(()=>(n.lang.rtl===!0?-1:1)*(S.value===!0?1:-1)),ye=E(0),M=E(!1),Y=E(!1),be=E(k.value*T.value),V=d(()=>S.value===!0?"left":"right"),G=d(()=>m.value===!0&&v.value===!1&&e.overlay===!1?e.miniToOverlay===!0?e.miniWidth:k.value:0),J=d(()=>e.overlay===!0||e.miniToOverlay===!0||r.view.value.indexOf(S.value?"R":"L")>-1||n.platform.is.ios===!0&&r.isContainer.value===!0),A=d(()=>e.overlay===!1&&m.value===!0&&v.value===!1),Me=d(()=>e.overlay===!0&&m.value===!0&&v.value===!1),Oe=d(()=>"fullscreen q-drawer__backdrop"+(m.value===!1&&M.value===!1?" hidden":"")),Qe=d(()=>({backgroundColor:`rgba(0,0,0,${ye.value*.4})`})),pe=d(()=>S.value===!0?r.rows.value.top[2]==="r":r.rows.value.top[0]==="l"),Ae=d(()=>S.value===!0?r.rows.value.bottom[2]==="r":r.rows.value.bottom[0]==="l"),Pe=d(()=>{const a={};return r.header.space===!0&&pe.value===!1&&(J.value===!0?a.top=`${r.header.offset}px`:r.header.space===!0&&(a.top=`${r.header.size}px`)),r.footer.space===!0&&Ae.value===!1&&(J.value===!0?a.bottom=`${r.footer.offset}px`:r.footer.space===!0&&(a.bottom=`${r.footer.size}px`)),a}),Fe=d(()=>{const a={width:`${k.value}px`,transform:`translateX(${be.value}px)`};return v.value===!0?a:Object.assign(a,Pe.value)}),Ie=d(()=>"q-drawer__content fit "+(r.isContainer.value!==!0?"scroll":"overflow-auto")),We=d(()=>`q-drawer q-drawer--${e.side}`+(Y.value===!0?" q-drawer--mini-animate":"")+(e.bordered===!0?" q-drawer--bordered":"")+(o.value===!0?" q-drawer--dark q-dark":"")+(M.value===!0?" no-transition":m.value===!0?"":" q-layout--prevent-focus")+(v.value===!0?" fixed q-drawer--on-top q-drawer--mobile q-drawer--top-padding":` q-drawer--${L.value===!0?"mini":"standard"}`+(J.value===!0||A.value!==!0?" fixed":"")+(e.overlay===!0||e.miniToOverlay===!0?" q-drawer--on-top":"")+(pe.value===!0?" q-drawer--top-padding":""))),ze=d(()=>{const a=n.lang.rtl===!0?e.side:V.value;return[[oe,je,void 0,{[a]:!0,mouse:!0}]]}),Ve=d(()=>{const a=n.lang.rtl===!0?V.value:e.side;return[[oe,ge,void 0,{[a]:!0,mouse:!0}]]}),Ne=d(()=>{const a=n.lang.rtl===!0?V.value:e.side;return[[oe,ge,void 0,{[a]:!0,mouse:!0,mouseAllDir:!0}]]});function Z(){He(v,e.behavior==="mobile"||e.behavior!=="desktop"&&r.totalWidth.value<=e.breakpoint)}g(v,a=>{a===!0?(p=m.value,m.value===!0&&Q(!1)):e.overlay===!1&&e.behavior!=="mobile"&&p!==!1&&(m.value===!0?(B(0),D(0),te()):U(!1))}),g(()=>e.side,(a,u)=>{r.instances[u]===z&&(r.instances[u]=void 0,r[u].space=!1,r[u].offset=0),r.instances[a]=z,r[a].size=k.value,r[a].space=A.value,r[a].offset=G.value}),g(r.totalWidth,()=>{(r.isContainer.value===!0||document.qScrollPrevented!==!0)&&Z()}),g(()=>e.behavior+e.breakpoint,Z),g(r.isContainer,a=>{m.value===!0&&f(a!==!0),a===!0&&Z()}),g(r.scrollbarWidth,()=>{B(m.value===!0?0:void 0)}),g(G,a=>{x("offset",a)}),g(A,a=>{l("onLayout",a),x("space",a)}),g(S,()=>{B()}),g(k,a=>{B(),ae(e.miniToOverlay,a)}),g(()=>e.miniToOverlay,a=>{ae(a,k.value)}),g(()=>n.lang.rtl,()=>{B()}),g(()=>e.mini,()=>{e.modelValue===!0&&(Re(),r.animate())}),g(L,a=>{l("miniState",a)});function B(a){a===void 0?ke(()=>{a=m.value===!0?0:k.value,B(T.value*a)}):(r.isContainer.value===!0&&S.value===!0&&(v.value===!0||Math.abs(a)===k.value)&&(a+=T.value*r.scrollbarWidth.value),be.value=a)}function D(a){ye.value=a}function ee(a){const u=a===!0?"remove":r.isContainer.value!==!0?"add":"";u!==""&&document.body.classList[u]("q-body--drawer-toggle")}function Re(){clearTimeout(w),t.proxy&&t.proxy.$el&&t.proxy.$el.classList.add("q-drawer--mini-animate"),Y.value=!0,w=setTimeout(()=>{Y.value=!1,t&&t.proxy&&t.proxy.$el&&t.proxy.$el.classList.remove("q-drawer--mini-animate")},150)}function je(a){if(m.value!==!1)return;const u=k.value,q=j(a.distance.x,0,u);if(a.isFinal===!0){q>=Math.min(75,u)===!0?U():(r.animate(),D(0),B(T.value*u)),M.value=!1;return}B((n.lang.rtl===!0?S.value!==!0:S.value)?Math.max(u-q,0):Math.min(0,q-u)),D(j(q/u,0,1)),a.isFirst===!0&&(M.value=!0)}function ge(a){if(m.value!==!0)return;const u=k.value,q=a.direction===e.side,N=(n.lang.rtl===!0?q!==!0:q)?j(a.distance.x,0,u):0;if(a.isFinal===!0){Math.abs(N)<Math.min(75,u)===!0?(r.animate(),D(1),B(0)):Q(),M.value=!1;return}B(T.value*N),D(j(1-N/u,0,1)),a.isFirst===!0&&(M.value=!0)}function te(){f(!1),ee(!0)}function x(a,u){r.update(e.side,a,u)}function He(a,u){a.value!==u&&(a.value=u)}function ae(a,u){x("size",a===!0?e.miniWidth:u)}return r.instances[e.side]=z,ae(e.miniToOverlay,k.value),x("space",A.value),x("offset",G.value),e.showIfAbove===!0&&e.modelValue!==!0&&m.value===!0&&e["onUpdate:modelValue"]!==void 0&&l("update:modelValue",!0),it(()=>{l("onLayout",A.value),l("miniState",L.value),p=e.showIfAbove===!0;const a=()=>{(m.value===!0?b:O)(!1,!0)};if(r.totalWidth.value!==0){ke(a);return}y=g(r.totalWidth,()=>{y(),y=void 0,m.value===!1&&e.showIfAbove===!0&&v.value===!1?U(!1):a()})}),rt(()=>{y!==void 0&&y(),clearTimeout(w),m.value===!0&&te(),r.instances[e.side]===z&&(r.instances[e.side]=void 0,x("size",0),x("offset",0),x("space",!1))}),()=>{const a=[];v.value===!0&&(e.noSwipeOpen===!1&&a.push(lt($("div",{key:"open",class:`q-drawer__opener fixed-${e.side}`,"aria-hidden":"true"}),ze.value)),a.push(qe("div",{ref:"backdrop",class:Oe.value,style:Qe.value,"aria-hidden":"true",onClick:Q},void 0,"backdrop",e.noSwipeBackdrop!==!0&&m.value===!0,()=>Ne.value)));const u=L.value===!0&&i.mini!==void 0,q=[$("div",{...h,key:""+u,class:[Ie.value,h.class]},u===!0?i.mini():X(i.default))];return e.elevated===!0&&m.value===!0&&q.push($("div",{class:"q-layout__shadow absolute-full overflow-hidden no-pointer-events"})),a.push(qe("aside",{ref:"content",class:We.value,style:Fe.value},q,"contentclose",e.noSwipeClose!==!0&&v.value===!0,()=>Ve.value)),$("div",{class:"q-drawer-container"},a)}}}),Se=I({name:"QItemSection",props:{avatar:Boolean,thumbnail:Boolean,side:Boolean,top:Boolean,noWrap:Boolean},setup(e,{slots:i}){const l=d(()=>`q-item__section column q-item__section--${e.avatar===!0||e.side===!0||e.thumbnail===!0?"side":"main"}`+(e.top===!0?" q-item__section--top justify-start":" justify-center")+(e.avatar===!0?" q-item__section--avatar":"")+(e.thumbnail===!0?" q-item__section--thumbnail":"")+(e.noWrap===!0?" q-item__section--nowrap":""));return()=>$("div",{class:l.value},X(i.default))}}),Dt=I({name:"QItem",props:{...ve,...ot,tag:{type:String,default:"div"},active:{type:Boolean,default:null},clickable:Boolean,dense:Boolean,insetLevel:Number,tabindex:[String,Number],focused:Boolean,manualFocus:Boolean},emits:["click","keyup"],setup(e,{slots:i,emit:l}){const{proxy:{$q:h}}=me(),t=fe(e,h),{hasLink:n,linkAttrs:o,linkClass:f,linkTag:c,navigateOnClick:s}=st(),r=E(null),p=E(null),w=d(()=>e.clickable===!0||n.value===!0||e.tag==="label"),y=d(()=>e.disable!==!0&&w.value===!0),v=d(()=>"q-item q-item-type row no-wrap"+(e.dense===!0?" q-item--dense":"")+(t.value===!0?" q-item--dark":"")+(n.value===!0&&e.active===null?f.value:e.active===!0?` q-item--active${e.activeClass!==void 0?` ${e.activeClass}`:""}`:"")+(e.disable===!0?" disabled":"")+(y.value===!0?" q-item--clickable q-link cursor-pointer "+(e.manualFocus===!0?"q-manual-focusable":"q-focusable q-hoverable")+(e.focused===!0?" q-manual-focusable--focused":""):"")),L=d(()=>{if(e.insetLevel===void 0)return null;const b=h.lang.rtl===!0?"Right":"Left";return{["padding"+b]:16+e.insetLevel*56+"px"}});function k(b){y.value===!0&&(p.value!==null&&(b.qKeyEvent!==!0&&document.activeElement===r.value?p.value.focus():document.activeElement===p.value&&r.value.focus()),s(b))}function m(b){if(y.value===!0&&dt(b,13)===!0){Ee(b),b.qKeyEvent=!0;const O=new MouseEvent("click",b);O.qKeyEvent=!0,r.value.dispatchEvent(O)}l("keyup",b)}function W(){const b=ct(i.default,[]);return y.value===!0&&b.unshift($("div",{class:"q-focus-helper",tabindex:-1,ref:p})),b}return()=>{const b={ref:r,class:v.value,style:L.value,role:"listitem",onClick:k,onKeyup:m};return y.value===!0?(b.tabindex=e.tabindex||"0",Object.assign(b,o.value)):w.value===!0&&(b["aria-disabled"]="true"),$(c.value,b,W())}}});const xt=$e({name:"EssentialLink",props:{title:{type:String,required:!0},caption:{type:String,default:""},link:{type:String,default:"#"},icon:{type:String,default:""}}});function Tt(e,i,l,h,t,n){return F(),H(Dt,{clickable:"",tag:"a",target:"_blank",href:e.link},{default:_(()=>[e.icon?(F(),H(Se,{key:0,avatar:""},{default:_(()=>[C(vt,{name:e.icon},null,8,["name"])]),_:1})):ft("",!0),C(Se,null,{default:_(()=>[C(ce,null,{default:_(()=>[K(de(e.title),1)]),_:1}),C(ce,{caption:""},{default:_(()=>[K(de(e.caption),1)]),_:1})]),_:1})]),_:1},8,["href"])}var Mt=De(xt,[["render",Tt]]);const Ot=[{title:"Docs",caption:"quasar.dev",icon:"school",link:"https://quasar.dev"},{title:"Github",caption:"github.com/quasarframework",icon:"code",link:"https://github.com/quasarframework"},{title:"Discord Chat Channel",caption:"chat.quasar.dev",icon:"chat",link:"https://chat.quasar.dev"},{title:"Forum",caption:"forum.quasar.dev",icon:"record_voice_over",link:"https://forum.quasar.dev"},{title:"Twitter",caption:"@quasarframework",icon:"rss_feed",link:"https://twitter.quasar.dev"},{title:"Facebook",caption:"@QuasarFramework",icon:"public",link:"https://facebook.quasar.dev"},{title:"Quasar Awesome",caption:"Community Quasar projects",icon:"favorite",link:"https://awesome.quasar.dev"}],Qt=$e({name:"MainLayout",components:{EssentialLink:Mt},setup(){const e=E(!1);return{essentialLinks:Ot,leftDrawerOpen:e,toggleLeftDrawer(){e.value=!e.value}}}});function At(e,i,l,h,t,n){const o=Ce("EssentialLink"),f=Ce("router-view");return F(),H(Ct,{view:"lHh Lpr lFf"},{default:_(()=>[C(pt,{elevated:""},{default:_(()=>[C(mt,null,{default:_(()=>[C(ht,{flat:"",dense:"",round:"",icon:"menu","aria-label":"Menu",onClick:e.toggleLeftDrawer},null,8,["onClick"]),C(yt,null,{default:_(()=>[K(" Quasar App ")]),_:1}),bt("div",null,"Quasar v"+de(e.$q.version),1)]),_:1})]),_:1}),C($t,{modelValue:e.leftDrawerOpen,"onUpdate:modelValue":i[0]||(i[0]=c=>e.leftDrawerOpen=c),"show-if-above":"",bordered:""},{default:_(()=>[C(Bt,null,{default:_(()=>[C(ce,{header:""},{default:_(()=>[K(" Essential Links ")]),_:1}),(F(!0),gt(kt,null,wt(e.essentialLinks,c=>(F(),H(o,_t({key:c.title},c),null,16))),128))]),_:1})]),_:1},8,["modelValue"]),C(qt,null,{default:_(()=>[C(f)]),_:1})]),_:1})}var Wt=De(Qt,[["render",At]]);export{Wt as default};