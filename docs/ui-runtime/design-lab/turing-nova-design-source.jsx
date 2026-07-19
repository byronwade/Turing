import React, { useState, useCallback, useMemo, useRef, useEffect, useLayoutEffect, memo } from "react";
import {
  ArrowLeft, ArrowRight, ArrowUp, RotateCw, Home, Lock, Star, Shield, ShieldCheck, FileText,
  Puzzle, Settings, History as HistoryIcon, Download, Search, Plus, X,
  MoreVertical, ChevronRight, Globe, Cookie, Zap, Gauge, Palette, Trash2,
  Check, Command, CornerDownLeft, Eye, Key, CircleUser, Blocks, Wifi, Bell,
  Camera, Mic, MapPin, ExternalLink, Sun, Moon, Monitor, ChevronDown, Circle, WifiOff, PanelLeft, PanelRight,
  Sparkles, SlidersHorizontal, LayoutGrid, Bookmark, RefreshCw, Ban, Fingerprint, Terminal, Pin,
  Volume2, VolumeX, Link, Copy, Columns2, BookOpen, ChevronUp, Code, FileCode, Database, Activity, Type,
  EyeOff, KeyRound, ShieldAlert, Dices, LogIn, Layers, ScrollText, Gavel, Radio, Plug,
} from "lucide-react";

/* ============================================================================
   Turing — the open project browser (concept shell). Attio-calibrated light-first UI; dark + community themes via tokens.
   Performance notes (real, not decorative):
   - All styling lives in one injected <style> tag → zero per-render style objects
     for the structural chrome, and the browser's own CSS engine does the work.
   - Long lists (history) are windowed by a tiny useVirtual hook: 400 rows exist,
     ~20 are ever in the DOM.
   - Row/card components are memo()'d; handlers passed down are useCallback'd;
     derived lists are useMemo'd. Re-renders stay local to the panel in view.
   - Animations are transform/opacity only (compositor-friendly), and honor
     prefers-reduced-motion.
   ========================================================================== */

const DESIGN_W = 1440, DESIGN_H = 900;
// mirrors --ease-out: the Web Animations API cannot resolve CSS custom properties
const EASE_OUT = "cubic-bezier(.2,.8,.2,1)";
let __lastId = 0;
const uid = () => { const t = Date.now(); __lastId = t > __lastId ? t : __lastId + 1; return __lastId; };

const CSS = `
:root{
  --ink:#0a0a0a; --c1:#101012; --c2:#141416; --c3:#1b1b1e; --c4:#212125;
  --line:rgba(255,255,255,.08); --line2:rgba(255,255,255,.14);
  --tx:#ededed; --tx2:#9a9a9f; --tx3:#616166;
  --ac:#2e8dff; --ac-soft:rgba(46,141,255,.14); --ac-line:rgba(46,141,255,.4);
  --good:#34d399; --bad:#f87171; --warn:#fbbf24;
  --r:10px; --r-sm:7px; --r-lg:14px;
  /* motion: three intents, one scale — everything below composes from these */
  --ease-out:cubic-bezier(.2,.8,.2,1);      /* settle: things arriving or resizing */
  --ease-inout:cubic-bezier(.4,0,.2,1);     /* travel: things moving across the screen */
  --ease-spring:cubic-bezier(.3,1.3,.5,1);  /* overshoot: things that should feel physical */
  --dur-1:.08s;   /* press feedback */
  --dur-2:.12s;   /* standard UI transition */
  --dur-3:.18s;   /* panels and larger surfaces */
  --dur-4:.4s;    /* entrances */
  --mono:"Geist Mono",ui-monospace,"SF Mono",Menlo,monospace;
  --sans:"Geist","Inter",-apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif;
}
*{box-sizing:border-box;margin:0;padding:0}
.nova,.nova *{font-family:var(--sans)}
.stage{
  position:fixed;inset:0;display:flex;flex-direction:column;overflow:hidden;
  background:#121216;font-family:var(--sans);
}
.zbar{
  flex:none;height:44px;display:flex;align-items:center;gap:10px;padding:0 14px;
  background:#17171b;border-bottom:1px solid rgba(255,255,255,.09);color:#9a9a9f;
}
.zbar .zt{font-size:12px;font-weight:500;color:#ededed;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.zbar .zd{font-family:var(--mono);font-size:11px;color:#616166;white-space:nowrap}
.zseg{display:flex;background:#101013;border:1px solid rgba(255,255,255,.1);border-radius:var(--r);padding:2px;margin-left:auto}
.zseg button{height:28px;padding:0 12px;border-radius:var(--r);color:#9a9a9f;font-size:12px;font-weight:500;font-family:var(--mono);transition:background var(--dur-2),color var(--dur-2)}
.zseg button.on{background:#26262b;color:#ededed}
.zpres{height:28px;padding:0 12px;margin-left:10px;border-radius:var(--r);border:1px solid rgba(255,255,255,.14);color:#c9c9d2;font-size:12px;font-weight:500}
.zpres:hover{background:#26262b;color:#fff}
.canvas.present{background:#0a0a0f;background-image:radial-gradient(760px 460px at 50% 36%,rgba(88,96,180,.22),transparent 70%);background-size:auto}
.zexit{position:fixed;right:18px;bottom:16px;z-index:99;font-size:11px;color:#9a9aa6;background:rgba(20,20,28,.85);border:1px solid rgba(255,255,255,.12);border-radius:7px;padding:6px 11px;opacity:.18;transition:opacity var(--dur-3)}
.zexit:hover{opacity:1}
.canvas{
  flex:1;overflow:auto;-webkit-overflow-scrolling:touch;display:grid;
  background-image:radial-gradient(rgba(255,255,255,.055) 1px,transparent 1px);
  background-size:22px 22px;
}
.holder{margin:auto;padding:28px;flex:none}
.nova{
  width:1440px;height:900px;position:relative;transform-origin:top left;
  background:var(--ink);color:var(--tx);display:flex;flex-direction:column;overflow:hidden;
  border-radius:var(--r-lg);box-shadow:0 30px 90px -18px color-mix(in srgb,var(--tx) 46%,transparent),0 0 0 1px rgba(255,255,255,.14);
  font-size:13px;line-height:1.45;letter-spacing:-.01em;
  -webkit-font-smoothing:antialiased;user-select:none;
}
button{font:inherit;color:inherit;background:none;border:none;cursor:pointer}
/* ---- light theme ---- */
.nova.light{
  --ink:#fbfbfc; --c1:#ffffff; --c2:#f7f8f9; --c3:#eef0f2; --c4:#e2e5e8;
  --line:#e9ebee; --line2:#d9dde2;
  --tx:#17181a; --tx2:#4b5057; --tx3:#8f959d;
  --ac-soft:rgba(46,141,255,.11); --ac-line:rgba(46,141,255,.38);
  --good:#0f9955; --bad:#dc3535; --warn:#c07c1d;
  box-shadow:0 30px 90px -18px rgba(30,30,60,.28),0 0 0 1px rgba(0,0,0,.09);
}
.nova.light ::-webkit-scrollbar-thumb:hover{background:#b9b9c2}
.nova.light .bar.float{box-shadow:0 12px 32px -12px rgba(30,30,60,.28)}
.nova.light .pop,.nova.light .toast,.nova.light .banner,.nova.light .findbar,.nova.light .modal{box-shadow:0 18px 48px -14px rgba(30,30,60,.3)}
/* light DevTools accents that need more contrast */
.nova.light .el-v{color:#15803d}
.nova.light .el-a{color:#7c3aed}
.nova.light .con-row.warn .con-m{color:#b45309}
.nova.light .con-row.error .con-m{color:#dc2626}
.nova.light .fps i{opacity:.75}
.mono{font-family:var(--mono);letter-spacing:0}
::selection{background:var(--ac-soft)}

/* ---- single bar: window controls, nav, tabs-as-text, actions ---- */
.bar{display:flex;align-items:center;gap:10px;height:44px;padding:0 12px;background:var(--c2);border-bottom:1px solid var(--line);-webkit-app-region:drag;position:relative}
.bar.float{position:absolute;top:0;left:0;right:0;z-index:66;animation:barin var(--dur-3) var(--ease-out) both;box-shadow:0 12px 32px -12px color-mix(in srgb,var(--tx) 37%,transparent)}
@keyframes barin{from{transform:translateY(-100%)}to{transform:none}}
.peek{position:absolute;top:0;left:0;right:0;height:16px;z-index:65}
.lsweep{position:absolute;left:0;bottom:-1px;height:2px;width:26%;border-radius:2px;pointer-events:none;
  background:linear-gradient(90deg,transparent,var(--ac),transparent);animation:lsweep .9s var(--ease-inout) forwards}
@keyframes lsweep{from{transform:translateX(-110%)}to{transform:translateX(500%)}}
.ttab.s1{opacity:.72}
.ttab.s2{opacity:.42}
.ttab.s1:hover,.ttab.s2:hover{opacity:1}
.ttab.pinned{min-width:auto;max-width:120px;background:var(--c1)}
.ttab.pinned.on{min-width:150px;background:var(--c3)}
.ttab:active{cursor:grabbing}
.traffic{display:flex;gap:8px;flex:none}
.dot{width:11px;height:11px;border-radius:50%;background:var(--c4);transition:background var(--dur-3)}
.traffic:hover .dot.r{background:#ff5f57}.traffic:hover .dot.y{background:#febc2e}.traffic:hover .dot.g{background:#28c840}
.nova.light .dot.r{background:#ff5f57}.nova.light .dot.y{background:#febc2e}.nova.light .dot.g{background:#28c840}
.nova.light .dot{box-shadow:inset 0 0 0 .5px rgba(0,0,0,.12)}
.nav{display:flex;gap:1px;flex:none;opacity:.35;transition:opacity var(--dur-3)}
.bar:hover .nav{opacity:1}
.numhint{font-family:var(--mono);font-size:9px;color:var(--tx2);border:1px solid var(--line2);border-radius:4px;padding:0 4px;flex:none;animation:fade var(--dur-3) both}
.ttab .rn{background:none;border:none;outline:none;color:var(--tx);font-size:12.5px;width:120px;font-family:var(--sans)}
.ttab.peeking{box-shadow:inset 0 0 0 1px var(--ac-line)}
.ttabs{position:relative;flex:1;align-self:stretch;display:flex;align-items:center;gap:2px;min-width:0;overflow-x:auto;overflow-y:hidden;scrollbar-width:none}
.ttabs::-webkit-scrollbar{display:none}
.ttab:hover{background:var(--c3);color:var(--tx2)}
.ttab:hover .xc{opacity:.6}
.ttab .xc:hover{background:var(--c4);opacity:1}
.site{flex:1;display:flex;align-items:center;justify-content:center;gap:8px;height:30px;min-width:0;border-radius:var(--r);color:var(--tx2);font-family:var(--mono);font-size:12px;transition:background var(--dur-2)}
.site:hover{background:var(--c3)}
.site .kbd{font-size:9px;color:var(--tx3);border:1px solid var(--line);border-radius:4px;padding:1px 4px}
.lockb{width:26px;height:26px;border-radius:var(--r);display:grid;place-items:center;color:var(--good);flex:none;transition:background var(--dur-2)}
.lockb:hover{background:var(--c3)}
.acts{display:flex;align-items:center;gap:2px;flex:none;margin-left:auto}
.newtab{width:28px;height:28px;border-radius:var(--r);display:grid;place-items:center;color:var(--tx3);flex:none;transition:background var(--dur-2),color var(--dur-2)}
.newtab:hover{background:var(--c3);color:var(--tx)}
.mid{flex:1;display:flex;min-height:0}
.main{flex:1;display:flex;flex-direction:column;min-width:0}
.bar.bottom{border-bottom:none;border-top:1px solid var(--line);height:42px}
.vwrap{width:224px;flex:none;overflow:hidden;transition:width .24s var(--ease-out);display:flex}
.vwrap.closed{width:0}
.vwrap.right{justify-content:flex-end}
.siderail{position:absolute;left:0;top:50%;transform:translateY(-50%);z-index:40;width:22px;height:64px;border-radius:0 var(--r) var(--r) 0;background:var(--c2);border:1px solid var(--line);border-left:none;display:grid;place-items:center;color:var(--tx3);opacity:.55;transition:opacity var(--dur-3),color var(--dur-3)}
.siderail:hover{opacity:1;color:var(--tx)}
.siderail.right{left:auto;right:0;border-radius:var(--r) 0 0 var(--r);border:1px solid var(--line);border-right:none}
.vtabs{width:224px;flex:none;background:var(--c2);border-right:1px solid var(--line);display:flex;flex-direction:column;gap:2px;padding:8px;overflow-y:auto}
.vnew-top{display:flex;align-items:center;gap:8px;height:30px;padding:0 9px;margin-bottom:6px;border-radius:var(--r);border:1px dashed var(--line2);font-size:12px;color:var(--tx3);width:100%;text-align:left;transition:color var(--dur-2),border-color var(--dur-2),background var(--dur-2)}
.vnew-top:hover{color:var(--tx);border-color:var(--line2);border-style:solid;background:var(--c3)}
.vnew-top .kbd{opacity:.7}
.vzone{display:flex;flex-direction:column;gap:1px}
.vsep{height:1px;background:var(--line);margin:8px 4px}
.vsec{display:flex;flex-direction:column;gap:1px;margin:2px 0}
.vsec-h{display:flex;align-items:center;gap:7px;height:24px;padding:0 7px;border-radius:var(--r-sm);font-size:11px;font-weight:550;color:var(--tx2);background:transparent;border:none;width:100%;text-align:left;transition:background var(--dur-2)}
.vsec-h:hover{background:var(--c3)}
.vsec-h svg{color:var(--tx3)}
.vsec-n{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.vsec-c{margin-left:auto;font-size:9.5px;color:var(--tx3)}
.vsec-w{display:grid;grid-template-rows:1fr;transition:grid-template-rows .24s var(--ease-out)}
.vsec-w.closed{grid-template-rows:0fr}
.vsec-w>.vsec-b{overflow:hidden;min-height:0}
.vsec-b{display:flex;flex-direction:column;gap:1px;padding-left:9px}
.vtabs.right{border-right:none;border-left:1px solid var(--line)}
.vtab:hover{background:var(--c3);color:var(--tx2)}
.vtab .ttl{flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.vtab:hover .xc{opacity:.6}
.vtab .xc:hover{background:var(--c4);opacity:1}
.vnew{display:flex;align-items:center;gap:8px;height:30px;padding:0 10px;border-radius:var(--r);color:var(--tx3);font-size:12.5px;margin-top:2px;transition:background var(--dur-2),color var(--dur-2)}
.vnew:hover{background:var(--c3);color:var(--tx)}

/* ===== mock web pages — designed sites, light-first, per-domain brand ===== */
.wp{min-height:100%;display:flex;flex-direction:column;background:#fff;color:#191a1f;position:relative;font-family:var(--sans)}
.wp,.wp *{letter-spacing:-.005em}
.sm-nav{display:flex;align-items:center;gap:26px;height:58px;padding:0 36px;border-bottom:1px solid #ececf0;flex:none;background:#fff;position:sticky;top:0;z-index:3}
.sm-mark{display:flex;align-items:center;gap:9px;font-weight:650;font-size:14.5px;color:#141419}
.sm-dot{width:20px;height:20px;border-radius:7px;background:var(--bc,#111);display:grid;place-items:center;color:#fff;font-size:10px;font-weight:700}
.sm-link{font-size:13px;color:#5a5e6a;cursor:pointer}
.sm-link:hover{color:#141419}
.sm-cta{margin-left:auto;height:32px;padding:0 14px;border-radius:7px;background:var(--bc,#111);color:#fff;font-size:12.5px;font-weight:550;display:inline-flex;align-items:center;gap:7px}
.sm-ghost{height:32px;padding:0 13px;border-radius:7px;border:1px solid #e3e4ea;color:#33343c;font-size:12.5px;font-weight:500;display:inline-flex;align-items:center}
.sm-wrap{width:100%;max-width:1020px;margin:0 auto;padding:0 36px}
.sm-hero{padding:74px 0 44px;text-align:center}
.sm-kick{display:inline-flex;align-items:center;gap:7px;font-size:11.5px;font-weight:550;color:var(--bc,#111);background:color-mix(in srgb,var(--bc,#111) 8%,#fff);border:1px solid color-mix(in srgb,var(--bc,#111) 18%,#fff);border-radius:999px;padding:5px 12px;margin-bottom:20px}
.sm-h1{font-size:44px;line-height:1.08;font-weight:700;letter-spacing:-.03em;color:#121318;max-width:640px;margin:0 auto 16px}
.sm-sub{font-size:16px;line-height:1.6;color:#5c6070;max-width:520px;margin:0 auto 26px}
.sm-art{height:300px;border-radius:14px;margin:8px 0 30px;position:relative;overflow:hidden;background:linear-gradient(135deg,color-mix(in srgb,var(--bc,#111) 12%,#fff),color-mix(in srgb,var(--bc,#111) 4%,#f7f8fb) 55%,#fff);border:1px solid #e8e9ef;box-shadow:inset 0 1px 0 #fff}
.sm-art i{position:absolute;border-radius:10px;background:#fff;border:1px solid #e6e7ee;box-shadow:0 18px 40px -18px rgba(20,22,40,.25)}
.sm-logos{display:flex;align-items:center;justify-content:center;gap:34px;padding:6px 0 46px;color:#a2a6b3;font-size:13px;font-weight:600;letter-spacing:.02em}
.sm-grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;padding-bottom:52px}
.sm-card{border:1px solid #e9eaf0;border-radius:14px;padding:20px;background:#fff;box-shadow:0 1px 2px rgba(20,22,40,.04)}
.sm-ci{width:34px;height:34px;border-radius:7px;background:color-mix(in srgb,var(--bc,#111) 9%,#fff);color:var(--bc,#111);display:grid;place-items:center;margin-bottom:13px}
.sm-ct{font-size:14.5px;font-weight:600;margin-bottom:6px;color:#16171c}
.sm-cd{font-size:12.8px;line-height:1.6;color:#666b78}
.sm-article{max-width:640px;margin:0 auto;padding:8px 0 60px}
.sm-foot{border-top:1px solid #ececf0;padding:26px 0 40px;display:flex;gap:40px;font-size:12px;color:#8a8e9b}
.sm-foot b{display:block;color:#3a3d47;font-weight:600;margin-bottom:8px;font-size:12px}
.sm-foot span{display:block;padding:3px 0;cursor:pointer}
/* app shell (linear/mercury/github/stripe) */
.ap-shell{flex:1;display:flex;min-height:0}
.ap-side{width:222px;flex:none;border-right:1px solid #ececf0;background:#fafafc;padding:14px 10px;font-size:12.8px}
.ap-sec{font-size:10.5px;font-weight:650;letter-spacing:.05em;text-transform:uppercase;color:#9a9eab;padding:14px 10px 6px}
.ap-item{display:flex;align-items:center;gap:9px;height:30px;padding:0 10px;border-radius:7px;color:#4c505c;cursor:pointer}
.ap-item:hover{background:#f0f1f5}
.ap-item.on{background:#ebedf3;color:#17181d;font-weight:550}
.ap-item .n{margin-left:auto;font-size:10.5px;color:#9a9eab;font-family:var(--mono)}
.ap-main{flex:1;min-width:0;display:flex;flex-direction:column}
.ap-head{display:flex;align-items:center;gap:12px;height:52px;padding:0 24px;border-bottom:1px solid #ececf0;flex:none}
.ap-title{font-size:14.5px;font-weight:650;color:#16171c}
.ap-chip{font-size:11px;color:#6a6e7b;border:1px solid #e6e7ee;border-radius:7px;padding:3px 9px;background:#fff;cursor:pointer}
.ap-chip.on{background:#f0f1f6;color:#22232a;border-color:#dcdee8}
/* rows */
.iss-row{display:flex;align-items:center;gap:12px;height:44px;padding:0 24px;border-bottom:1px solid #f1f2f6;font-size:13px;cursor:default}
.iss-row:hover{background:#fafbfd}
.iss-pri{width:14px;text-align:center;font-size:11px;flex:none}
.iss-id{font-family:var(--mono);font-size:11px;color:#8b8fa0;width:62px;flex:none}
.iss-t{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:#1c1d24}
.lb{font-size:10px;font-weight:600;border-radius:7px;padding:2px 7px;flex:none}
.stdot{width:9px;height:9px;border-radius:50%;flex:none;border:2px solid transparent}
.ava{width:20px;height:20px;border-radius:50%;display:grid;place-items:center;font-size:8.5px;font-weight:700;color:#fff;flex:none}
.iss-tm{font-size:11px;color:#a0a4b1;width:26px;text-align:right;flex:none;font-family:var(--mono)}
/* mercury */
.me-hero{padding:30px 0 6px}
.me-lbl{font-size:12px;color:#7a7e8b;margin-bottom:6px}
.me-bal{font-size:40px;font-weight:650;letter-spacing:-.02em;font-family:var(--mono);color:#141519;display:flex;align-items:baseline;gap:14px}
.me-up{font-size:13px;color:#0f9955;font-weight:600;font-family:var(--sans)}
.me-cards{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;padding:20px 0}
.me-card{border:1px solid #e9eaf0;border-radius:14px;padding:16px 18px;background:#fff}
.me-cn{font-size:12px;color:#7a7e8b;display:flex;align-items:center;gap:8px}
.me-cv{font-size:20px;font-weight:650;font-family:var(--mono);margin-top:8px;color:#16171c}
.me-apy{font-size:10px;font-weight:650;color:#0f9955;background:#e9f8f0;border-radius:7px;padding:2px 7px;margin-left:auto}
.tx-row{display:flex;align-items:center;gap:14px;height:46px;padding:0 18px;border-bottom:1px solid #f1f2f6;font-size:13px}
.tx-row:hover{background:#fafbfd}
.tx-ic{width:30px;height:30px;border-radius:7px;display:grid;place-items:center;font-size:11px;font-weight:700;color:#fff;flex:none}
.tx-n{flex:1;min-width:0;color:#1c1d24}
.tx-c{font-size:10.5px;color:#8b8fa0;border:1px solid #ececf2;border-radius:7px;padding:2px 8px;flex:none}
.tx-d{font-size:11px;color:#a0a4b1;width:52px;flex:none;font-family:var(--mono)}
.tx-a{font-family:var(--mono);font-size:12.5px;width:96px;text-align:right;flex:none;color:#1c1d24}
.tx-a.pos{color:#0f9955}
/* github */
.gh-head{padding:22px 0 0}
.gh-name{display:flex;align-items:center;gap:9px;font-size:18px;font-weight:600}
.gh-name .mono{color:#0969da}
.gh-pub{font-size:10.5px;color:#6a6e7b;border:1px solid #d9dbe3;border-radius:999px;padding:2px 8px;font-weight:500}
.gh-stats{display:flex;gap:8px;padding:14px 0}
.gh-file{display:flex;align-items:center;gap:12px;height:38px;padding:0 16px;border-bottom:1px solid #eef0f4;font-size:12.8px}
.gh-file:hover{background:#f6f8fa}
.gh-file .f{width:170px;flex:none;color:#0969da;display:flex;align-items:center;gap:9px}
.gh-file .m{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:#59606d}
.gh-file .t{font-size:11px;color:#8b909c;flex:none}
.gh-md{border:1px solid #e6e8ee;border-radius:10px;margin:18px 0 40px;overflow:hidden}
.gh-md-h{display:flex;align-items:center;gap:8px;padding:10px 16px;border-bottom:1px solid #eef0f4;font-size:12px;color:#59606d;background:#f8f9fb}
.gh-md-b{padding:22px 26px;font-size:13.5px;line-height:1.7;color:#2a2c34}
.gh-md-b h1{font-size:22px;margin:0 0 10px;font-weight:650}
.gh-code{background:#f6f8fa;border:1px solid #e8eaef;border-radius:7px;padding:12px 14px;font-family:var(--mono);font-size:11.5px;color:#24292f;margin-top:14px;line-height:1.7}
/* stripe */
.st-tbl{border:1px solid #e9eaf0;border-radius:10px;overflow:hidden;margin:18px 0 40px;background:#fff}
.st-hd,.st-r{display:grid;grid-template-columns:110px 1.5fr 110px 96px 90px;gap:12px;align-items:center;padding:0 18px}
.st-hd{height:38px;font-size:10.5px;font-weight:650;letter-spacing:.05em;text-transform:uppercase;color:#8b8fa0;border-bottom:1px solid #eef0f4;background:#fafbfd}
.st-r{height:44px;font-size:12.8px;border-bottom:1px solid #f1f2f6}
.st-r:hover{background:#fafbfd}
.st-b{font-size:10.5px;font-weight:650;border-radius:7px;padding:3px 8px;width:fit-content}
/* video grid */
.yt-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px 14px;padding:24px 0 48px}
.yt-th{position:relative;aspect-ratio:16/9;border-radius:10px;overflow:hidden}
.yt-dur{position:absolute;right:7px;bottom:7px;background:rgba(10,10,14,.85);color:#fff;font-size:10px;font-family:var(--mono);border-radius:4px;padding:2px 6px}
.yt-t{font-size:13px;font-weight:550;color:#17181d;margin:9px 0 3px;line-height:1.4;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.yt-m{font-size:11.5px;color:#7a7e8b}
/* search results */
.se-r{padding:14px 0;max-width:600px}
.se-u{font-size:12px;color:#1a6b2f;display:flex;align-items:center;gap:7px}
.se-t{font-size:17px;color:#1a0dab;padding:3px 0 4px;cursor:pointer}
.se-t:hover{text-decoration:underline}
.se-d{font-size:12.8px;color:#4d5156;line-height:1.55}
/* prose */
.sm-pq{border-left:3px solid var(--bc,#111);padding:6px 0 6px 18px;margin:26px 0;font-size:17px;line-height:1.6;color:#1e2027;font-weight:500}
/* reader */
.rd h1{font-size:30px;line-height:1.2;font-weight:700;letter-spacing:-.02em;margin:0 0 10px;color:#1c1a15}
.rd .by{font-size:12.5px;color:#8b8678;margin-bottom:30px}
.rd p{font-size:15.5px;line-height:1.85;margin:0 0 20px;color:#33302a}
/* live snapshots — real pixels of the real web */
.shot-img{width:100%;display:block;background:#fff;min-height:200px;transition:opacity .3s;mask-image:linear-gradient(180deg,#000 calc(100% - 56px),transparent);-webkit-mask-image:linear-gradient(180deg,#000 calc(100% - 56px),transparent)}
.shot-load{position:absolute;top:0;left:0;right:0;min-height:720px;background:#fff;z-index:1}
.sk-nav{height:58px;border-bottom:1px solid #eef0f4;display:flex;align-items:center;gap:18px;padding:0 36px}
.sk-b{border-radius:7px;background:linear-gradient(90deg,#f2f3f7 25%,#e8eaf0 37%,#f2f3f7 63%);background-size:400% 100%;animation:shm 1.3s ease infinite}
@keyframes shm{0%{background-position:100% 0}100%{background-position:-100% 0}}
.sk-cap{position:absolute;top:14px;right:16px;font-size:9.5px;color:#b6bac4;letter-spacing:.05em}
/* live pages */
.live-wrap{flex:1;position:relative;min-height:0;background:#fff}
.live-fr{position:absolute;inset:0;width:100%;height:100%;border:0;background:#fff}
.live-load{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;gap:10px;font-size:12.5px;color:#8b8fa0;background:#fff;z-index:1}
.live-tag{position:absolute;top:10px;right:14px;z-index:2;font-size:9px;font-weight:700;letter-spacing:.1em;color:#fff;background:var(--bc,#e5484d);border-radius:7px;padding:3px 8px;box-shadow:0 6px 16px -6px rgba(0,0,0,.3);pointer-events:none}
/* boost tint rides the brand var */
.wp.boost{--bc:var(--boost)}
/* split view */
.splitwrap{display:flex;height:100%;min-height:0}
.pane{flex:1;min-width:0;position:relative;display:flex;flex-direction:column;overflow:hidden}
.pane.dropover{box-shadow:inset 0 0 0 2px var(--ac);z-index:2}
.pane.dropover::after{content:"Drop tab here";position:absolute;left:0;right:0;top:32px;bottom:0;display:grid;place-items:center;font-size:12px;font-weight:600;letter-spacing:-.01em;color:var(--ac);background:var(--ac-soft);pointer-events:none;z-index:5}
.splitwrap.dragging .pane-body{pointer-events:none}
.pane-h{display:flex;align-items:center;justify-content:space-between;height:32px;padding:0 6px 0 12px;border-bottom:1px solid var(--line);background:var(--c2);font-size:11px;color:var(--tx2);flex:none}
.pane-body{flex:1;position:relative;min-height:0}
.pane-dom{display:flex;align-items:center;gap:7px;min-width:0}
.pane-h .mono{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.pane-divider{flex:none;width:9px;margin:0 -4px;position:relative;z-index:6;cursor:col-resize;display:flex;align-items:center;justify-content:center}
.pane-divider::before{content:"";position:absolute;top:0;bottom:0;left:4px;width:1px;background:var(--line2);transition:background var(--dur-2)}
.pane-divider::after{content:"";width:3px;height:36px;border-radius:2px;background:var(--line2);opacity:0;transition:opacity var(--dur-2),background var(--dur-2)}
.pane-divider:hover::before,.pane-divider.drag::before{background:var(--ac-line)}
.pane-divider:hover::after,.pane-divider.drag::after{opacity:1;background:var(--tx3)}
.col-resizing,.col-resizing *{cursor:col-resize!important;user-select:none!important}
/* find in page */
/* confirm modal */
.modalveil{position:absolute;inset:0;z-index:85;background:rgba(5,5,7,.5);backdrop-filter:blur(8px);display:grid;place-items:center;animation:fade var(--dur-2) both}
.modal{width:340px;background:var(--c2);border:1px solid var(--line2);border-radius:var(--r-lg);padding:22px;box-shadow:0 32px 90px -20px color-mix(in srgb,var(--tx) 43%,transparent);animation:pop var(--dur-3) both}
.modal .mt{font-size:15px;font-weight:600;letter-spacing:-.01em;margin-bottom:7px}
.modal .md{font-size:12.5px;color:var(--tx3);line-height:1.55;margin-bottom:18px}
.modal .mrow{display:flex;gap:8px;justify-content:flex-end}
/* restore banner */
.banner{position:absolute;top:16px;left:50%;transform:translateX(-50%);display:flex;align-items:center;gap:10px;background:var(--c2);border:1px solid var(--line2);border-radius:var(--r);padding:8px 14px;font-size:12px;color:var(--tx2);box-shadow:0 16px 40px -12px color-mix(in srgb,var(--tx) 31%,transparent);animation:pop var(--dur-3) var(--dur-2) both;white-space:nowrap;z-index:5}
.banner .dm{color:var(--tx3);font-size:12px;padding:2px 6px;border-radius:var(--r-sm)}
.banner .dm:hover{background:var(--c3);color:var(--tx)}
/* audio chip glyph */
.aud{width:16px;height:16px;margin:-2px;border-radius:var(--r-sm);display:grid;place-items:center;color:var(--tx3);flex:none;position:relative}
.aud:hover{background:var(--c4);color:var(--tx)}
/* link preview */
.linkpill{position:sticky;bottom:10px;left:12px;display:inline-block;background:var(--c2);border:1px solid var(--line);border-radius:var(--r);padding:4px 9px;font-size:10.5px;color:var(--tx2);animation:fade var(--dur-2) both;z-index:4;margin:0 0 10px 12px}
.nova.light .linkpill{background:#fff;border-color:rgba(0,0,0,.1);color:#555}
/* reader */
.wp.reader{background:#0d0d10;color:#d8d6d1}
.nova.light .wp.reader{background:#fbfaf7;color:#26241f}
.rd{max-width:620px;margin:0 auto;width:100%;padding:64px 32px}
.rd-k{font-size:11px;color:var(--tx3);margin-bottom:22px;letter-spacing:.04em;text-transform:uppercase;font-family:var(--mono)}
.toast{position:absolute;top:14px;left:50%;transform:translateX(-50%);z-index:70;background:var(--c2);border:1px solid var(--line2);border-radius:var(--r);padding:8px 14px;font-size:12px;color:var(--tx2);box-shadow:0 16px 40px -12px color-mix(in srgb,var(--tx) 30%,transparent);animation:pop var(--dur-3) var(--ease-out) both;pointer-events:none;white-space:nowrap;display:flex;align-items:center;gap:12px}
.toast.act{pointer-events:auto}
.toast .undo{color:var(--ac);font-size:12px;font-weight:500;padding:2px 6px;border-radius:var(--r-sm)}
.toast .undo:hover{background:var(--ac-soft)}
.wctl{display:flex;gap:2px;-webkit-app-region:no-drag}
.wbtn{width:30px;height:24px;display:grid;place-items:center;border-radius:var(--r-sm);color:var(--tx3);transition:background var(--dur-2),color var(--dur-2)}
.wbtn:hover{background:var(--c2);color:var(--tx)}

/* ---- shared icon button ---- */
.ib{width:32px;height:32px;border-radius:var(--r);display:grid;place-items:center;color:var(--tx2);transition:background var(--dur-2),color var(--dur-2),transform .06s;-webkit-app-region:no-drag}
.ib:hover{background:var(--c3);color:var(--tx)}
.ib:active{transform:scale(.94)}
.ib.off{color:var(--tx3);cursor:default}
.ib.off:hover{background:none;color:var(--tx3)}
.ib.on{background:var(--ac-soft);color:var(--ac)}

/* ---- bookmarks bar ---- */
.bkbar{display:flex;align-items:center;gap:2px;height:34px;padding:0 10px;background:var(--c2);border-bottom:1px solid var(--line);overflow:hidden}
.bk{display:flex;align-items:center;gap:7px;height:26px;padding:0 9px;border-radius:var(--r);color:var(--tx2);font-size:12px;white-space:nowrap;transition:background var(--dur-2),color var(--dur-2)}
.bk:hover{background:var(--c3);color:var(--tx)}
.bk .fav{width:14px;height:14px;border-radius:4px;display:grid;place-items:center;font-size:8px;font-weight:700;flex:none}

/* ---- viewport ---- */
.view{flex:1;overflow:hidden;position:relative;background:var(--ink)}
.scroll{position:absolute;inset:0;overflow-y:auto;overflow-x:hidden}

/* ---- new tab ---- */
.nt{min-height:100%;display:flex;flex-direction:column;align-items:center;padding:0 24px}
.nt-hero::before{content:"";position:absolute;top:-140px;left:50%;transform:translateX(-50%);width:720px;height:420px;background:radial-gradient(closest-side,color-mix(in srgb,var(--ac) 9%,transparent),transparent 70%);pointer-events:none;filter:blur(2px)}
.nt-hero{position:relative;flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;width:100%;max-width:640px;padding:80px 0 40px}
.glyph{width:30px;height:30px;border-radius:var(--r);background:var(--ac);display:grid;place-items:center}
.bigsearch{
  width:100%;display:flex;align-items:center;gap:12px;height:52px;padding:0 18px;
  background:var(--c2);border:1px solid var(--line);border-radius:var(--r-lg);
  transition:border-color var(--dur-3),box-shadow var(--dur-3);cursor:text;
  animation:rise .6s .06s var(--ease-out) both;
}
.bigsearch:hover{border-color:var(--line2)}
.bigsearch.focus{border-color:var(--ac-line);box-shadow:0 0 0 4px var(--ac-soft)}
.bigsearch input{flex:1;background:none;border:none;outline:none;color:var(--tx);font-size:15px}
.bigsearch input::placeholder{color:var(--tx3)}
.bigsearch .hint{font-size:11px;color:var(--tx3);border:1px solid var(--line);border-radius:var(--r-sm);padding:3px 7px;font-family:var(--mono)}
.ticker{
  display:flex;align-items:center;gap:8px;margin-top:20px;color:var(--tx3);font-size:12px;
  animation:rise .6s var(--dur-2) var(--ease-out) both;
}
.ticker b{font-family:var(--mono);color:var(--tx2);font-weight:500;font-variant-numeric:tabular-nums}
.quick{width:100%;max-width:640px;padding-bottom:64px;animation:rise .6s var(--dur-3) var(--ease-out) both}
.quick .lbl{font-size:11px;font-weight:600;color:var(--tx3);text-transform:uppercase;letter-spacing:.08em;margin-bottom:14px;padding-left:2px}
.qgrid{display:grid;grid-template-columns:repeat(6,1fr);gap:10px}
.q{display:flex;flex-direction:column;align-items:center;gap:9px;padding:14px 6px;border-radius:var(--r-lg);border:1px solid transparent;transition:background var(--dur-2),border-color var(--dur-2),transform var(--dur-2)}
.q:hover{background:var(--c2);border-color:var(--line);transform:translateY(-2px)}
.q .fav{width:34px;height:34px;border-radius:var(--r);display:grid;place-items:center;font-size:14px;font-weight:600}
.q span{font-size:11px;color:var(--tx2);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%}

/* ---- generic page (settings/history/etc) ---- */
.pnav{width:230px;flex:none;border-right:1px solid var(--line);padding:22px 12px;position:sticky;top:0;height:100%;overflow-y:auto}
.pnav-search{display:flex;align-items:center;gap:8px;height:30px;padding:0 9px;margin:0 2px 10px;border:1px solid var(--line);border-radius:var(--r);background:var(--c1)}
.pnav-search input{flex:1;background:none;border:none;outline:none;font-size:12px;color:var(--tx);min-width:0}
.pnav-search input::placeholder{color:var(--tx3)}
.pnav-none{padding:14px 10px;font-size:11.5px;color:var(--tx3)}
.pnav h2{font-size:15px;font-weight:600;padding:0 10px 16px;display:flex;align-items:center;gap:9px}
.pnav .grp{font-size:10px;font-weight:600;color:var(--tx3);text-transform:uppercase;letter-spacing:.08em;padding:14px 10px 6px}
.pnav a{display:flex;align-items:center;gap:10px;height:34px;padding:0 10px;border-radius:var(--r);color:var(--tx2);font-size:13px;transition:background var(--dur-2),color var(--dur-2)}
.pnav a:hover{background:var(--c2);color:var(--tx)}
.pnav a.on{background:var(--c3);color:var(--tx);font-weight:500}
.pnav a.on svg{color:var(--ac)}
.pbody{flex:1;overflow-y:auto;padding:40px 40px 80px}

.psub{color:var(--tx2);font-size:13px;margin-bottom:30px}

.sect{margin-bottom:32px}
.sect-h{font-size:12.5px;font-weight:550;color:var(--tx3);margin-bottom:10px}
.card{background:var(--c2);border:1px solid var(--line);border-radius:var(--r-lg);overflow:hidden}
.row{display:flex;align-items:center;gap:14px;padding:14px 18px;border-bottom:1px solid var(--line)}
.row:last-child{border-bottom:none}
.row .ico{width:16px;display:grid;place-items:center;color:var(--tx3);flex:none}
.row .meta{flex:1;min-width:0}
.row .meta .t{font-size:13px;font-weight:500}
.row .meta .d{font-size:12px;color:var(--tx3);margin-top:2px}
.row .val{color:var(--tx2);font-size:12px;font-family:var(--mono)}

/* switch */
.sw{width:38px;height:22px;border-radius:var(--r-lg);background:var(--c4);position:relative;flex:none;transition:background var(--dur-3);cursor:pointer}
.sw::after{content:"";position:absolute;top:2px;left:2px;width:18px;height:18px;border-radius:50%;background:#fff;transition:transform var(--dur-3) var(--ease-spring)}
.sw.on{background:var(--ac)}
.sw.on::after{transform:translateX(16px)}

/* segmented */
.seg{display:flex;background:var(--c1);border:1px solid var(--line);border-radius:var(--r);padding:2px}
.seg button{padding:5px 12px;border-radius:var(--r);color:var(--tx2);font-size:12px;font-weight:500;transition:background var(--dur-2),color var(--dur-2);display:flex;align-items:center;gap:6px}
.seg button.on{background:var(--c4);color:var(--tx)}

/* select pill */
.pill{display:flex;align-items:center;gap:7px;height:32px;padding:0 12px;background:var(--c1);border:1px solid var(--line);border-radius:var(--r);color:var(--tx);font-size:12px;transition:border-color var(--dur-2)}
.pill:hover{border-color:var(--line2)}

/* stats */

/* history */
.htop{display:flex;align-items:center;gap:12px;margin-bottom:22px}
.hsearch.focus{border-color:var(--ac-line);box-shadow:0 0 0 3px var(--ac-soft)}
.hsearch input::placeholder{color:var(--tx3)}
.chips{display:flex;gap:6px;flex-wrap:wrap}
.hlist{position:relative;background:var(--c2);border:1px solid var(--line);border-radius:var(--r-lg);overflow:hidden}
.hwin{position:relative;height:520px;overflow-y:auto}
.hrow{display:flex;align-items:center;gap:14px;height:52px;padding:0 18px;position:absolute;left:0;right:0;border-bottom:1px solid var(--line);transition:background var(--dur-2)}
.hrow:hover{background:var(--c3)}
.hrow .fav{width:22px;height:22px;border-radius:var(--r-sm);display:grid;place-items:center;font-size:10px;font-weight:700;flex:none}
.hrow .t{flex:1;min-width:0;font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.hrow .u{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:240px}
.hrow .u .vchip{max-width:100%;overflow:hidden;text-overflow:ellipsis;display:inline-block;white-space:nowrap}
.hrow .tm{color:var(--tx3);font-size:11px;font-family:var(--mono);width:78px;text-align:right;flex:none}
.hrow .del{width:26px;height:26px;border-radius:var(--r);display:grid;place-items:center;color:var(--tx3);opacity:0;transition:opacity var(--dur-2),background var(--dur-2),color var(--dur-2);flex:none}
.hrow:hover .del{opacity:1}
.hrow .del:hover{background:var(--c4);color:var(--bad)}

/* extensions grid */
.exgrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}
.ex{background:var(--c2);border:1px solid var(--line);border-radius:var(--r-lg);padding:18px;transition:border-color var(--dur-2)}
.ex:hover{border-color:var(--line2)}
.ex-h{display:flex;align-items:flex-start;gap:13px;margin-bottom:12px}
.ex .logo{width:38px;height:38px;border-radius:var(--r);background:var(--c3);color:var(--tx2);display:grid;place-items:center;flex:none}
.ex .nm{font-size:14px;font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;min-width:0}
.ex-meta{font-size:10px;color:var(--tx3);margin-top:7px}
.ex-h > div{min-width:0}
.ex .by{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-size:11px;color:var(--tx3);margin-top:1px}
.ex .desc{display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;font-size:12px;color:var(--tx2);line-height:1.5;margin-bottom:14px;min-height:36px}
.ex-f{display:flex;align-items:center;justify-content:space-between;padding-top:13px;border-top:1px solid var(--line)}
.ex .perm{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;min-width:0;max-width:60%;font-size:11px;color:var(--tx3);display:flex;align-items:center;gap:5px}

/* popover */
.pop{position:absolute;z-index:60;background:var(--c2);border:1px solid var(--line2);border-radius:var(--r-lg);box-shadow:0 24px 60px -10px color-mix(in srgb,var(--tx) 43%,transparent),0 0 0 1px rgba(0,0,0,.4);animation:pop var(--dur-3) var(--ease-out) both;overflow:hidden}
.pop-h{padding:14px 16px;border-bottom:1px solid var(--line);display:flex;align-items:center;gap:10px}
.pop-h .ico{width:30px;height:30px;border-radius:var(--r);display:grid;place-items:center;flex:none}
.pop-h .t{font-size:13px;font-weight:600}
.pop-h .s{font-size:11px;color:var(--tx3);margin-top:1px}
.mitem{display:flex;align-items:center;gap:12px;height:36px;padding:0 12px;color:var(--tx);font-size:13px;border-radius:var(--r);transition:background var(--dur-2);margin:2px 6px}
.mitem:hover{background:var(--c3)}
.mitem .r{margin-left:auto;color:var(--tx3);font-size:11px;font-family:var(--mono)}
.mitem svg{color:var(--tx2)}
.msep{height:1px;background:var(--line);margin:6px 0}
.backdrop{position:fixed;inset:0;z-index:55}

/* command palette */
.cmdveil{position:absolute;inset:0;z-index:80;background:color-mix(in srgb,var(--tx) 24%,transparent);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);display:flex;justify-content:center;padding-top:84px;animation:fade var(--dur-2) both}
.cmd.warm{width:min(900px,94%);height:min(590px,74vh);background:var(--c1);border:1px solid var(--line2);border-radius:14px;
  box-shadow:0 32px 90px -20px rgba(23,24,26,.35),0 4px 16px rgba(23,24,26,.08);display:flex;flex-direction:column;overflow:hidden;animation:pop .17s var(--ease-out) both;position:relative}
.cmd-in{display:flex;align-items:center;gap:12px;padding:16px 20px 12px;flex:none}
.cmd-in input{flex:1;background:none;border:none;outline:none;color:var(--tx);font-size:17.5px;font-family:var(--sans);letter-spacing:-.01em}
.cmd-in input::placeholder{color:var(--tx3)}
.cin-ic{width:34px;height:34px;border-radius:var(--r);background:var(--c3);display:grid;place-items:center;color:var(--tx2);flex:none}
.cin-esc{font-size:10px;color:var(--tx3);border:1px solid var(--line);border-radius:var(--r-sm);padding:2px 6px}
.cmd-quick{display:flex;gap:6px;padding:0 20px 13px;border-bottom:1px solid var(--line);flex:none}
.qa{display:flex;align-items:center;gap:6px;font-size:11.5px;color:var(--tx2);background:var(--c2);border:1px solid var(--line);border-radius:var(--r);padding:5px 10px;transition:background var(--dur-2),border-color var(--dur-2),color var(--dur-2)}
.qa:hover{background:var(--c3);border-color:var(--line2);color:var(--tx)}
.cmd-body{flex:1;display:flex;min-height:0}
.cmd-list{flex:1.45;overflow-y:auto;padding:8px 10px;min-width:0}
.cmd-detail{flex:1;border-left:1px solid var(--line);padding:26px 24px;display:flex;flex-direction:column;min-width:0;background:var(--c2);position:relative}
.cmd-grp{padding:12px 10px 5px;font-size:10px;font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:var(--tx3);display:flex;align-items:center;gap:7px}
.cmd-grp .gc{font-family:var(--mono);font-weight:500;background:var(--c3);border-radius:var(--r-sm);padding:1px 5px;letter-spacing:0;color:var(--tx3)}
.cmd-it{display:flex;align-items:center;gap:12px;padding:9px 11px;border-radius:var(--r);cursor:default;min-height:46px}
.cmd-it.sel{background:var(--ac-soft);box-shadow:inset 0 0 0 1px var(--ac-line)}
.cmd-it .ci{width:32px;height:32px;border-radius:var(--r);background:var(--c3);display:grid;place-items:center;color:var(--tx2);flex:none}
.cmd-it.sel .ci{background:color-mix(in srgb,var(--ac) 18%,transparent);color:var(--ac)}
.cmd-it .ct{flex:1;font-size:13.5px;color:var(--tx);min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.cmd-it .cs{font-size:11.5px;color:var(--tx3);margin-top:1px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.cmd-it .hl{color:var(--ac);font-weight:600}
.cmd-it .tag2{font-size:10px;color:var(--tx3);font-family:var(--mono);flex:none}
.cmd-it .tag2.kb{border:1px solid var(--line);border-radius:var(--r-sm);padding:2px 6px;color:var(--tx3)}
.cmd-it.ans .ct{font-family:var(--mono);font-size:19px;font-weight:600;letter-spacing:-.01em}
.cmd-it.ans .ct .cs{font-family:var(--sans);font-size:11px;font-weight:400;color:var(--tx3);letter-spacing:0}
.cd-ic{width:52px;height:52px;border-radius:var(--r-lg);background:var(--c3);display:grid;place-items:center;color:var(--tx2);margin-bottom:16px}
.cd-t{font-size:16px;font-weight:600;letter-spacing:-.01em}
.cd-s{font-size:12px;color:var(--tx3);margin-top:5px;line-height:1.6}
.cd-prev{margin-top:18px;border:1px solid var(--line);border-radius:var(--r);background:var(--c1);padding:12px;display:flex;flex-direction:column;gap:7px}
.cd-pl{height:7px;border-radius:4px;background:var(--c3)}
.cd-meta{margin-top:auto;border-top:1px solid var(--line);padding-top:12px;display:flex;flex-direction:column;gap:7px}
.cd-row{display:flex;justify-content:space-between;font-size:11.5px;color:var(--tx3)}
.cd-row b{font-weight:500;color:var(--tx2)}
.cf-brand{display:flex;align-items:center;gap:7px;font-weight:600;color:var(--tx2)}
.cf-dot{width:7px;height:7px;border-radius:2px;background:var(--ac)}
.actpanel{position:absolute;right:16px;bottom:16px;width:200px;background:var(--c1);border:1px solid var(--line2);border-radius:var(--r-lg);padding:6px;box-shadow:0 20px 60px -16px rgba(23,24,26,.3);animation:pop var(--dur-2) both;z-index:5}
.ap-t{font-size:10px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--tx3);padding:7px 10px 4px}
.ap-i{display:block;width:100%;text-align:left;padding:8px 10px;border-radius:var(--r);font-size:12.5px;color:var(--tx)}
.ap-i:hover{background:var(--c2)}
.cmd-foot{display:flex;align-items:center;gap:18px;padding:11px 20px;border-top:1px solid var(--line);color:var(--tx3);font-size:11px;flex:none;background:var(--c2)}
.cf-sp{flex:1}
.cf-act{display:flex;align-items:center;gap:6px;color:var(--tx3);font-size:11px;padding:4px 9px;border-radius:var(--r)}
.cf-act:hover{background:var(--c3);color:var(--tx)}

.typinghint{margin-top:12px;font-size:11px;color:var(--tx3);animation:rise .6s var(--dur-3) var(--ease-out) both}
.typinghint .mono{border:1px solid var(--line);border-radius:var(--r-sm);padding:1px 5px;font-size:10px}
.nova button:focus-visible,.nova a:focus-visible,.nova [role="switch"]:focus-visible{outline:2px solid var(--ac-line);outline-offset:1px;border-radius:var(--r)}
.nova input:focus-visible,.nova textarea:focus-visible{outline:none;border-color:var(--ac-line);box-shadow:0 0 0 3px var(--ac-soft)}
.findbar:focus-within,.sidep-s:focus-within,.tabsrch .ts-in:focus-within{border-color:var(--ac-line);box-shadow:0 0 0 3px var(--ac-soft)}
.tabsrch .ts-in:focus-within{border-radius:var(--r-lg) var(--r-lg) 0 0}

/* misc */
.btn{height:34px;padding:0 15px;border-radius:var(--r);font-size:13px;font-weight:500;display:inline-flex;align-items:center;gap:8px;transition:all var(--dur-2)}
.btn.pri{background:var(--ac);color:#fff}
.btn.pri:hover{filter:brightness(1.08)}
.btn.gho{background:var(--c2);border:1px solid var(--line);color:var(--tx)}
.btn.gho:hover{border-color:var(--line2);background:var(--c3)}
.btn.dgr{color:var(--bad)}
.btn.dgr:hover{background:rgba(248,113,113,.1)}
.tag{font-size:10px;font-weight:600;padding:2px 8px;border-radius:var(--r-sm);font-family:var(--mono)}
.tag.on{background:rgba(52,211,153,.14);color:var(--good)}
.tag.off{background:var(--c3);color:var(--tx3)}
.meter{height:6px;border-radius:4px;background:var(--c1);overflow:hidden}
.meter i{display:block;height:100%;border-radius:4px;background:linear-gradient(90deg,var(--ac),#7b5cff)}

@keyframes rise{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
@keyframes pop{from{opacity:0;transform:scale(.97) translateY(-4px)}to{opacity:1;transform:none}}
@keyframes fade{from{opacity:0}to{opacity:1}}

/* ---- restored: perf pill, localhost strip, shield lines ---- */
.perfpill{display:flex;align-items:center;gap:5px;height:28px;padding:0 10px;border-radius:var(--r);font-family:var(--mono);font-size:11px;color:var(--tx3);transition:background var(--dur-2),color var(--dur-2);white-space:nowrap}
.perfpill:hover{background:var(--c3);color:var(--tx2)}
.perfpill b{color:var(--tx2);font-weight:500;font-variant-numeric:tabular-nums}
.lhost{display:flex;align-items:center;gap:12px;padding:12px 16px;background:var(--c2);font-family:var(--mono);font-size:12px;color:var(--tx);transition:background var(--dur-2)}
.lhost:hover{background:var(--c3)}
.lhost .lv{width:6px;height:6px;border-radius:50%;background:var(--good);flex:none}
.lhost.off .lv{background:var(--c4)}
.lhost .ln{color:var(--tx3)}
.lhost .lt{margin-left:auto;font-size:11px;color:var(--tx3)}
.lhost.off .lt{color:var(--tx3)}
.local{display:flex;flex-direction:column;gap:1px;background:var(--line);border:1px solid var(--line);border-radius:var(--r-lg);overflow:hidden}
.sline{display:flex;align-items:center;gap:10px;padding:8px 14px;font-size:12px;border-bottom:1px solid var(--line)}
.sline:last-child{border-bottom:none}
.sline .sl-k{color:var(--tx2);flex:1}
.sline .sl-v{font-family:var(--mono);color:var(--tx);font-size:11px}
.vmini{font-family:var(--mono);font-size:12px;color:var(--tx3)}
.vmini b{color:var(--tx);font-weight:600;font-variant-numeric:tabular-nums}
.beta{font-family:var(--mono);font-size:9px;letter-spacing:.1em;color:var(--ac);border:1px solid var(--ac-line);border-radius:var(--r-sm);padding:2px 6px;vertical-align:middle}
/* pip mini player */
.pip{position:absolute;bottom:16px;right:16px;z-index:56;display:flex;align-items:center;gap:10px;background:var(--c2);border:1px solid var(--line2);border-radius:var(--r-lg);padding:8px 10px 8px 12px;box-shadow:0 18px 48px -14px color-mix(in srgb,var(--tx) 34%,transparent);animation:pop var(--dur-3) both}
.pip .pt{font-size:11.5px;color:var(--tx2);max-width:180px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.eq{display:flex;align-items:flex-end;gap:2px;height:12px}
.eq i{width:3px;border-radius:2px;background:var(--ac);animation:eqb 1s infinite ease-in-out}
.eq i:nth-child(1){height:60%;animation-delay:0s}
.eq i:nth-child(2){height:100%;animation-delay:var(--dur-3)}
.eq i:nth-child(3){height:45%;animation-delay:var(--dur-4)}
@keyframes eqb{0%,100%{transform:scaleY(.5)}50%{transform:scaleY(1)}}
/* history toolbar */
.htools{display:flex;align-items:center;gap:10px;margin-bottom:14px}
.hsearch{flex:1;display:flex;align-items:center;gap:9px;height:34px;padding:0 12px;background:var(--c1);border:1px solid var(--line);border-radius:var(--r);transition:border-color var(--dur-3),box-shadow var(--dur-3)}
.hsearch input{flex:1;background:none;border:none;outline:none;color:var(--tx);font-size:12.5px}
.hclear{height:34px;padding:0 14px;border-radius:var(--r);border:1px solid var(--line2);color:var(--tx2);font-size:12px;flex:none}
.hclear:hover{background:var(--c3);color:var(--bad)}
.hempty{padding:60px 0;text-align:center;color:var(--tx3);font-size:13px}
.spsq{width:18px;height:18px;border-radius:4px;display:grid;place-items:center;font-size:10px;font-weight:700;color:#fff;flex:none;text-transform:uppercase;box-shadow:inset 0 -1px 0 rgba(0,0,0,.15)}
.spn{max-width:110px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.spch{color:var(--tx3);flex:none}
.avmenu{position:relative}
.av-sp{position:absolute;right:-2px;bottom:-2px;width:9px;height:9px;border-radius:4px;border:2px solid var(--c1);box-sizing:content-box}
.pop.acct{width:248px !important}
.pop.acct .mitem{height:27px;font-size:12px;gap:8px}
.pop.acct .mitem svg{width:14px;height:14px}
.pop.acct .msep{margin:3px 6px}
.pop.acct .mitem .r{font-size:10px}
.acct-id{display:flex;align-items:center;gap:9px;padding:10px 12px;border-bottom:1px solid var(--line)}
.acct-prof{display:flex;align-items:center;padding:4px 10px 5px}
.pf{width:20px;height:20px;border-radius:7px;color:#fff;font-size:9.5px;font-weight:700;display:grid;place-items:center;opacity:.45;transition:opacity var(--dur-2),box-shadow var(--dur-2)}
.pf:hover{opacity:.8}
.pf.on{opacity:1;box-shadow:0 0 0 2px var(--c1),0 0 0 3.5px var(--ac-line)}
.acct-id .t{font-size:12.5px;font-weight:600}
.acct-id .s{font-size:10.5px;color:var(--tx3);margin-top:1px}
.acct-l{font-size:9.5px;font-weight:600;color:var(--tx3);padding:5px 10px 3px;letter-spacing:.03em}
.bar-sep{width:1px;height:16px;background:var(--line2);flex:none;margin:0 4px;opacity:.7}
.zoomchip{height:22px;padding:0 8px;border-radius:var(--r-sm);border:1px solid var(--ac-line);background:var(--ac-soft);color:var(--ac);font-size:10.5px;flex:none;margin-left:auto;transition:filter var(--dur-2);-webkit-app-region:no-drag}
.zoomchip:hover{filter:brightness(1.08)}
.spdot{width:9px;height:9px;border-radius:4px;flex:none}
.avatar{width:24px;height:24px;border-radius:50%;display:grid;place-items:center;font-size:10px;font-weight:600;font-family:var(--mono);color:var(--tx2);background:var(--c3);border:1px solid var(--line2);flex:none;transition:border-color var(--dur-2),color var(--dur-2);text-transform:uppercase}
.avatar:hover{border-color:var(--ac-line);color:var(--tx)}
.little{position:absolute;right:48px;bottom:48px;width:560px;height:380px;z-index:58;background:var(--c1);border:1px solid var(--line2);border-radius:var(--r-lg);overflow:hidden;display:flex;flex-direction:column;box-shadow:0 40px 100px -20px color-mix(in srgb,var(--tx) 40%,transparent);animation:pop var(--dur-3) both}
.little-h{display:flex;align-items:center;gap:9px;height:34px;padding:0 8px 0 12px;border-bottom:1px solid var(--line);background:var(--c2);flex:none;font-size:11px}
.little-h .u{font-family:var(--mono);color:var(--tx3);flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.little-h .lb{font-size:10px;color:var(--ac);border:1px solid var(--ac-line);border-radius:var(--r-sm);padding:2px 7px}
.little .scroll{flex:1}
/* ===== Turing: project inspector ===== */
.si{position:absolute;top:44px;right:0;bottom:0;width:340px;z-index:60;background:var(--c1);border-left:1px solid var(--line2);display:flex;flex-direction:column;animation:slidein var(--dur-3) var(--ease-out) both;box-shadow:-24px 0 60px -30px color-mix(in srgb,var(--tx) 31%,transparent)}
.si-h{display:flex;align-items:center;gap:9px;height:44px;padding:0 14px;border-bottom:1px solid var(--line);flex:none}
.si-t{font-size:13px;font-weight:600}
.si-badge{font-size:9px;letter-spacing:.08em;color:var(--ac);border:1px solid var(--ac-line);border-radius:var(--r-sm);padding:2px 6px}
.si-body{flex:1;overflow-y:auto;padding:12px 14px;display:flex;flex-direction:column;gap:16px}
.si-sec{display:flex;flex-direction:column;gap:1px}
.si-kv{display:flex;justify-content:space-between;gap:12px;padding:4px 0;font-size:11.5px;color:var(--tx3);border-bottom:1px solid var(--line)}
.si-kv b{color:var(--tx2);font-weight:500;text-align:right}
.si-note{font-size:11px;color:var(--tx3);line-height:1.6;padding:6px 0}
.si-note b{color:var(--tx2);font-weight:500}
.si-add{color:var(--ac);font-size:11px;margin-left:4px}
.si-dot{display:inline-block;width:6px;height:6px;border-radius:50%;background:var(--tx3);margin:0 2px}
.si-dot.on{background:var(--good)}
.si-bud{display:flex;align-items:center;gap:9px;padding:5px 0;font-size:11px;color:var(--tx3)}
.si-bud>span:first-child{width:104px;flex:none}
.si-bar{flex:1;height:5px;border-radius:4px;background:var(--c3);overflow:hidden}
.si-bar i{display:block;height:100%;background:var(--ac);border-radius:4px}
.si-bud b{font-weight:400;color:var(--tx2);flex:none}
.si-foot{display:flex;flex-wrap:wrap;gap:6px;padding:11px 14px;border-top:1px solid var(--line);flex:none}
.si-foot .hclear{height:26px;padding:0 10px;font-size:11.5px}
/* share sheet */
.sh-row{display:flex;align-items:center;gap:9px;padding:6px 0;font-size:12.5px;color:var(--tx2);border-bottom:1px solid var(--line)}
.sh-row input{accent-color:var(--ac)}
.sh-row.lock{color:var(--tx3)}
.sh-link{font-size:11.5px;color:var(--ac);background:var(--ac-soft);border:1px solid var(--ac-line);border-radius:var(--r);padding:8px 11px}
.sh-link.dead{color:var(--tx3);background:var(--c2);border-color:var(--line);text-decoration:line-through}
/* ===== time machine ===== */
.tm-wrap{display:flex;gap:18px;align-items:flex-start}
.tm-line{width:300px;flex:none;display:flex;flex-direction:column;gap:2px}
.tm-snap{display:grid;grid-template-columns:14px 1fr auto;grid-template-areas:"d e t" ". x x";align-items:center;gap:2px 8px;text-align:left;padding:9px 11px;border-radius:var(--r);border:1px solid transparent}
.tm-snap:hover{background:var(--c2)}
.tm-snap.on{background:var(--c2);border-color:var(--ac-line)}
.tm-dot{grid-area:d;width:8px;height:8px;border-radius:50%;background:var(--c4)}
.tm-snap.on .tm-dot{background:var(--ac)}
.tm-ev{grid-area:e;font-size:12.5px;color:var(--tx)}
.tm-t{grid-area:t;font-size:10px;color:var(--tx3)}
.tm-d{grid-area:x;font-size:11px;color:var(--tx3)}
.tm-view{flex:1;border:1px solid var(--line);border-radius:var(--r-lg);padding:16px 18px;background:var(--c2)}
.tm-prev{display:flex;flex-direction:column;gap:2px;padding:6px 0 10px}
.tm-topo{display:flex;align-items:center;gap:4px;padding-bottom:12px}
.tm-topo i{width:26px;height:12px;border-radius:4px;background:var(--c3);display:block}
.tm-topo i.pin{width:12px;background:var(--ac-soft);border:1px solid var(--ac-line)}
.tm-topo .mono{margin-left:8px;font-size:10.5px;color:var(--tx3)}
.tm-diff{display:flex;flex-direction:column;gap:7px;padding:10px 0;font-size:12px}
.tm-diff .add{color:var(--good)}
.tm-diff .rem{color:var(--bad)}
.tm-diff .mov{color:var(--warn)}
.tm-acts{display:flex;gap:7px;flex-wrap:wrap;padding-top:8px;border-top:1px solid var(--line)}
/* ===== resource truth center ===== */
.rt-sum{font-size:11.5px;color:var(--tx3);margin-bottom:14px}
.rt-hd{display:grid;grid-template-columns:2.2fr .8fr .55fr .55fr .8fr 1.1fr;gap:8px;padding:6px 12px;--num:1;font-size:10px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--tx3);border-bottom:1px solid var(--line)}
.rt-row{display:grid;grid-template-columns:2.2fr .8fr .55fr .55fr .8fr 1.1fr;gap:8px;padding:8px 12px;font-size:12px;border-bottom:1px solid var(--line);align-items:center;cursor:default}
.rt-row:hover{background:var(--c2)}
.rt-row.on{background:var(--c2)}
.rt-hd span:nth-child(n+2):nth-child(-n+5),.rt-row>.mono{text-align:right;font-variant-numeric:tabular-nums}
.rt-row .o{color:var(--tx);display:flex;align-items:center;gap:8px;overflow:hidden;white-space:nowrap;text-overflow:ellipsis}
.rt-kind{font-size:9px;color:var(--tx3);border:1px solid var(--line);border-radius:4px;padding:1px 5px;font-style:normal}
.rt-st{font-size:11px;display:flex;align-items:center;gap:6px}
.rt-st.active{color:var(--good)}
.rt-st.frozen{color:var(--tx3)}
.rt-st.protected{color:var(--warn)}
.rt-prot{font-size:9px;color:var(--warn);border:1px solid color-mix(in srgb,var(--warn) 40%,transparent);border-radius:4px;padding:1px 5px;font-style:normal}
.rt-detail{padding:4px 12px 12px;border-bottom:1px solid var(--line);background:var(--c2)}
/* ===== agent mode ===== */
.ag-grid{display:flex;gap:16px;align-items:stretch}
.ag-task{width:100%;background:var(--c1);border:1px solid var(--line);border-radius:var(--r);padding:10px 12px;color:var(--tx);font:inherit;font-size:12.5px;line-height:1.6;outline:none;resize:vertical}
.ag-task:focus{border-color:var(--ac-line)}
.ag-step{display:flex;align-items:center;gap:10px;padding:8px 10px;border:1px solid var(--line);border-radius:var(--r);font-size:12px;color:var(--tx2)}
.ag-step.running{border-color:var(--ac-line);background:var(--ac-soft)}
.ag-step.done{opacity:.7}
.ag-n{width:14px;color:var(--tx3);flex:none}
.ag-txt{flex:1}
.ag-cap.risk{color:var(--warn);border-color:color-mix(in srgb,var(--warn) 40%,transparent)}
.ag-st{width:14px;color:var(--good)}
.ag-post{display:flex;align-items:center;gap:8px;font-size:11.5px;color:var(--tx2);padding-top:8px}
/* ===== research canvas ===== */
.cv{display:flex;flex-direction:column;height:100%;min-height:0}
.cv-bar{display:flex;align-items:center;gap:10px;height:42px;padding:0 14px;border-bottom:1px solid var(--line);flex:none}
.cv-ground{display:flex;align-items:center;gap:6px;font-size:10px;color:var(--ac);border:1px solid var(--ac-line);border-radius:var(--r-sm);padding:3px 8px}
.cv-body{flex:1;display:flex;min-height:0}
.cv-grid{flex:1;display:grid;gap:1px;background:var(--line);min-height:0;min-width:0}
.cv-grid.n2{grid-template-columns:1fr 1fr}
.cv-grid.n3{grid-template-columns:1fr 1fr 1fr}
.cv-grid.n4{grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr}
.cv-pane{display:flex;flex-direction:column;min-width:0;min-height:0;background:var(--ink)}
.cv-ph{display:flex;align-items:center;height:30px;padding:0 10px;font-size:10.5px;color:var(--tx3);border-bottom:1px solid var(--line);flex:none;background:var(--c1)}
.cv-pb{flex:1;overflow-y:auto;min-height:0}
.cv-rail{width:272px;flex:none;background:var(--c1);border-left:1px solid var(--line);padding:12px 14px;display:flex;flex-direction:column;gap:10px;overflow-y:auto}
.cv-cap{border:1px solid var(--line);border-radius:var(--r);padding:9px 11px}
.cv-cap .q{font-size:11.5px;color:var(--tx);line-height:1.55}
.cv-cap .m{font-size:9.5px;color:var(--tx3);margin-top:5px}
.cv-conflict{display:flex;gap:8px;font-size:11px;color:var(--tx2);line-height:1.5;border:1px solid color-mix(in srgb,var(--warn) 35%,transparent);border-radius:var(--r);padding:9px 11px;background:color-mix(in srgb,var(--warn) 6%,transparent)}
/* ===== migration ===== */
.mg-pick{display:flex;gap:8px;align-items:center;flex-wrap:wrap;padding:6px 0 4px}
.mg-src{height:34px;padding:0 16px;border:1px solid var(--line);border-radius:var(--r);font-size:12.5px;color:var(--tx2)}
.mg-src:hover{background:var(--c2)}
.mg-src.on{border-color:var(--ac-line);background:var(--ac-soft);color:var(--tx)}
.mg-row{display:flex;align-items:center;gap:11px;padding:9px 2px;font-size:12px;border-bottom:1px solid var(--line)}
.card .mg-row:last-child{border-bottom:none}
.mg-row .k{color:var(--tx);flex:none;min-width:220px}
.mg-row .st{font-size:10px;color:var(--tx3);flex:none;width:86px}
.mg-row .w{color:var(--tx3);font-size:11px}
/* ===== causal ===== */
.cz{border-bottom:1px solid var(--line)}
.cz-q{display:block;width:100%;text-align:left;padding:8px 4px;font-size:12px;color:var(--tx2)}
.cz-q:hover{color:var(--tx)}
.cz-q.on{color:var(--ac)}
.cz-chain{padding:2px 4px 10px;font-size:11px;color:var(--tx3);line-height:1.7}
.cz-l:first-child{color:var(--tx2)}
/* ===== a11y reading order ===== */
.a11y-order{position:absolute;left:16px;top:60px;z-index:56;display:flex;flex-direction:column;gap:5px;background:var(--c2);border:1px solid var(--line2);border-radius:var(--r);padding:10px 12px;font-size:10.5px;color:var(--tx2);box-shadow:0 18px 48px -14px color-mix(in srgb,var(--tx) 31%,transparent)}
.a11y-order span{display:flex;align-items:center;gap:7px}
.a11y-order span::before{content:"";width:6px;height:6px;border-radius:2px;background:var(--ac)}
.a11y-order i{font-style:normal;color:var(--tx3);font-size:9.5px;padding-top:4px;border-top:1px solid var(--line);margin-top:3px}
/* ===== theme studio ===== */
.th-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.th-card{display:flex;flex-direction:column;align-items:flex-start;gap:8px;border:1px solid var(--line);border-radius:var(--r-lg);padding:13px 14px;background:var(--c2);transition:border-color var(--dur-2),transform var(--dur-2)}
.th-card:hover{border-color:var(--line2);transform:translateY(-1px)}
.th-card.on{border-color:var(--ac-line);box-shadow:0 0 0 3px var(--ac-soft)}
.th-sw{display:flex;gap:4px}
.th-sw i{width:16px;height:16px;border-radius:var(--r-sm);border:1px solid rgba(128,128,128,.25)}
.th-n{font-size:12.5px;color:var(--tx);font-weight:500}
.th-by{font-size:9px;color:var(--tx3);letter-spacing:.06em}
.th-json{border:1px solid var(--line);border-radius:var(--r-lg);overflow:hidden;background:var(--c1)}
.th-json.err{border-color:color-mix(in srgb,var(--bad) 50%,transparent)}
.th-json textarea{width:100%;background:none;border:none;outline:none;resize:vertical;color:var(--tx);font-family:var(--mono);font-size:12px;line-height:1.7;padding:12px 14px;display:block}
.th-json-bar{display:flex;align-items:center;gap:8px;padding:8px 12px;border-top:1px solid var(--line);background:var(--c2)}
.hp-in{width:210px;background:var(--c1);border:1px solid var(--line);border-radius:var(--r);padding:7px 10px;outline:none;color:var(--tx);font-size:11.5px}
.hp-in:focus{border-color:var(--ac-line)}
.hp-note{height:26px;display:flex;align-items:center;justify-content:center;font-size:10px;color:var(--tx3);border-bottom:1px solid var(--line);background:var(--c1);flex:none}
.dashhead{width:100%;max-width:640px;padding:60px 0 8px}
.dh-t{font-size:26px;font-weight:600;letter-spacing:-.02em}
.dh-s{font-size:11px;color:var(--tx3);margin-top:6px}
/* ===== compact density ===== */
.nova.compact .bar{height:38px}
.nova.compact .ttab{height:21px;font-size:11px}
.nova.compact .ib{width:26px;height:26px}
.nova.compact .mitem{padding:6px 10px;font-size:12px}
.nova.compact .row{padding:10px 14px}
/* ===== agent presence in the tab strip ===== */
.ttab.agenton{box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--ac) 55%,transparent)}
.gpill.agenton{box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--ac) 60%,transparent)}
.ttab.agentwait{box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--warn) 70%,transparent)}
.agdot{width:5px;height:5px;border-radius:50%;background:var(--ac);flex:none;margin-left:1px;animation:agpulse 1.5s ease-in-out infinite}
.ttab.agentwait .agdot{background:var(--warn);animation-duration:.7s}
@keyframes agpulse{0%,100%{opacity:.35;transform:scale(.8)}50%{opacity:1;transform:scale(1.15)}}
.nova.compact .pane-h{height:26px;font-size:10.5px;padding:0 4px 0 10px}
.nova.compact .pane-divider{width:7px;margin:0 -3px}
.nova.compact .pane-divider::after{height:28px}
@keyframes chipin{from{opacity:0;transform:scale(.96)}to{opacity:1;transform:none}}
.ttab.dragging{z-index:20;transform:scale(1.045);box-shadow:0 10px 26px -8px color-mix(in srgb,var(--tx) 34%,transparent);cursor:grabbing;opacity:.97}
.nova.light .ttab.dragging{box-shadow:0 10px 26px -8px rgba(30,30,60,.35)}
.ttab.closing{max-width:0!important;min-width:0!important;padding-left:0!important;padding-right:0!important;opacity:0;border-color:transparent!important;pointer-events:none;transition:max-width var(--dur-3) var(--ease-inout),padding var(--dur-3),opacity var(--dur-2)}
body.tdrag{user-select:none;cursor:grabbing}
body.tdrag .ttab{cursor:grabbing}
.dropspaces{position:absolute;top:48px;left:50%;transform:translateX(-50%);z-index:70;display:flex;align-items:center;gap:8px;background:var(--c2);border:1px solid var(--line2);border-radius:var(--r-lg);padding:8px 12px;box-shadow:0 20px 50px -14px color-mix(in srgb,var(--tx) 34%,transparent);animation:pop var(--dur-3) both}
.ds-l{font-size:10.5px;color:var(--tx3)}
.dropsp{display:flex;align-items:center;gap:7px;height:28px;padding:0 12px;border-radius:var(--r);border:1px dashed var(--line2);font-size:11.5px;color:var(--tx2);transition:border-color var(--dur-2),background var(--dur-2),transform var(--dur-2)}
.dropsp.hot{border-color:var(--ac);border-style:solid;background:var(--ac-soft);color:var(--tx);transform:scale(1.05)}
/* ---- no-shift chip geometry ---- */
.ttab{display:flex;align-items:center;gap:6px;height:24px;padding:0 10px;border-radius:var(--r);color:var(--tx2);font-size:12px;transition:background var(--dur-2),color var(--dur-2);cursor:default;animation:chipin var(--dur-3) var(--ease-out);position:relative;flex:1 1 118px;min-width:54px;max-width:190px;overflow:hidden;padding-right:26px}
.ttab.on .ttl{cursor:text}
.ttab.on .tst{position:relative}
.tsearch{position:absolute;inset:-2px;z-index:1;display:grid;place-items:center;background:var(--c1);color:var(--ac);opacity:0;transition:opacity var(--dur-2);border-radius:4px}
.ttab.on:hover .tsearch{opacity:1}
.ttab.on:hover{box-shadow:inset 0 0 0 1.5px var(--ac-line)}
.ttab .ttl{flex:1;white-space:nowrap;overflow:hidden;text-overflow:clip;min-width:0;mask-image:linear-gradient(90deg,#000 calc(100% - 16px),transparent);-webkit-mask-image:linear-gradient(90deg,#000 calc(100% - 16px),transparent)}
.ttab .xc::after,.aud::after{content:"";position:absolute;inset:-5px;border-radius:inherit}
.ttab .xc{width:16px;height:16px;border-radius:4px;display:grid;place-items:center;flex:none;opacity:0;transition:opacity var(--dur-2),background var(--dur-2);position:absolute;right:5px;top:50%;transform:translateY(-50%)}
.ttab:hover .xc,.ttab.on .xc{opacity:.75}
.ttab .kbd{font-size:9px;color:var(--tx3);border:1px solid var(--line);border-radius:4px;padding:1px 4px;font-family:var(--mono);flex:none;display:none}
.ttab.on{background:var(--c3);color:var(--tx);box-shadow:inset 0 0 0 1px var(--line2)}
.ttab.on::before{content:"";position:absolute;inset:-7px -10px;border-radius:inherit;background:radial-gradient(60% 90% at 50% 100%,color-mix(in srgb,var(--ac) 16%,transparent),transparent 72%);pointer-events:none;z-index:-1}
.nova.light .ttab.on{background:var(--c1);box-shadow:inset 0 0 0 1px var(--line2),0 1px 3px rgba(23,24,26,.08),0 1px 1px rgba(23,24,26,.04)}
.nova.light .ttab:not(.on):hover .ttl{color:var(--tx)}
.ttab:not(.on):hover{background:var(--c2)}
.tst{width:12px;height:12px;flex:none;display:grid;place-items:center}
.tdot{width:5px;height:5px;border-radius:50%;background:transparent}
.tfav{border-radius:4px;display:block;object-fit:cover}
.tspin{width:9px;height:9px;border-radius:50%;border:1.5px solid var(--ac-soft);border-top-color:var(--ac);animation:tsp .7s linear infinite}
@keyframes tsp{to{transform:rotate(360deg)}}
.terr{width:6px;height:6px;border-radius:50%;background:var(--bad)}
.ttab.err .ttl{color:var(--tx2);text-decoration:line-through;text-decoration-color:color-mix(in srgb,var(--bad) 45%,transparent);text-decoration-thickness:1px}
.ttab.err:hover .ttl{text-decoration:none}
/* ---- overflow ---- */
.ovf{display:flex;align-items:center;gap:4px;height:26px;padding:0 8px;border-radius:var(--r);color:var(--tx3);flex:none;border:1px solid var(--line)}
.ovf:hover{background:var(--c2);color:var(--tx2)}
.ovf.on{background:var(--c3);color:var(--tx)}
.ovf .mono{font-size:10px}
.mitem.ovf-in{padding-left:22px}
/* ---- frozen-neighbor drag ---- */
.ttab.ghost{opacity:.3}
.dragproxy{position:absolute;top:0;left:0;z-index:90;pointer-events:none;display:flex;align-items:center;gap:8px;height:28px;padding:0 12px;border-radius:var(--r);background:var(--c3);border:1px solid var(--line2);color:var(--tx);font-size:12.5px;box-shadow:0 14px 34px -10px color-mix(in srgb,var(--tx) 37%,transparent);white-space:nowrap;will-change:transform}
.nova.light .dragproxy{box-shadow:0 14px 34px -10px rgba(30,30,60,.4)}
.dropcue{position:absolute;top:7px;bottom:7px;left:0;width:2px;border-radius:2px;background:var(--ac);opacity:0;pointer-events:none;transition:transform .09s linear,opacity var(--dur-2);will-change:transform}
body.tdrag .ttab:hover{background:transparent}
body.tdrag .ttab.on:hover{background:var(--c3)}
body.tdrag .ttab .xc{opacity:0!important}
body.tdrag .tseg:hover{border-color:var(--line)}
body.tdrag .newtab:hover,body.tdrag .ovf:hover{background:transparent;color:var(--tx3)}
.ttab.kin{background:var(--c2)}
.ttab.kin.on{background:var(--c3)}
/* ---- hero submit ---- */
.go{width:32px;height:32px;border-radius:var(--r);display:grid;place-items:center;background:var(--c3);color:var(--tx3);border:none;flex:none;transition:background var(--dur-3),color var(--dur-3),transform var(--dur-2)}
.go.live{background:var(--ac);color:#fff}
.go.live:hover{transform:scale(1.05)}
.go.live:active{transform:scale(.97)}
/* ---- vtabs parity ---- */
.vtab{display:flex;align-items:center;gap:8px;height:27px;padding:0 26px 0 7px;border-radius:var(--r-sm);color:var(--tx3);font-size:12.5px;cursor:default;transition:background var(--dur-2),color var(--dur-2);position:relative}
.vtab .tst{flex:none}
.vtab .xc{width:16px;height:16px;border-radius:4px;display:grid;place-items:center;flex:none;opacity:0;transition:opacity var(--dur-2);position:absolute;right:5px;top:50%;transform:translateY(-50%)}
.vtab:hover .xc,.vtab.on .xc{opacity:.75}
.vtab.on{background:var(--c3);color:var(--tx);box-shadow:inset 0 0 0 1px var(--line2)}
.vtab.err .ttl{color:var(--tx2);text-decoration:line-through;text-decoration-color:color-mix(in srgb,var(--bad) 45%,transparent);text-decoration-thickness:1px}
/* ---- groups v4: one element type ---- */
.ttab.kin .gdot,.vtab:hover .gdot{transform:scale(1.35)}
.gdot{width:6px;height:6px;border-radius:50%;flex:none;transition:transform var(--dur-2)}
.ttab.fold.droptarget{box-shadow:inset 0 0 0 1.5px var(--ac);background:var(--ac-soft)}
.ttab.fold{cursor:default}
.ttab.fold .ttl{color:var(--tx2)}
.fold-n{font-size:9.5px;color:var(--tx2);flex:none}
.fold-x{position:absolute;right:7px;top:50%;transform:translateY(-50%);color:var(--tx3);opacity:.45;transition:opacity var(--dur-2)}
.ttab.fold:hover .fold-x,.vtab.fold:hover .fold-x{opacity:.8}
.vtab.fold .ttl{color:var(--tx2)}
/* ---- groups v6: inline pill, tinted run — the label lives in the flow ---- */
.trun .ttab{animation:chipin var(--dur-3) var(--ease-out) both}
@keyframes chipin{from{opacity:0;transform:scale(.94)}to{opacity:1;transform:none}}
.trun{display:flex;align-items:center;gap:2px;min-width:0;flex:0 1 auto;padding:2px 3px;border-radius:calc(var(--r) + 2px);background:color-mix(in srgb,var(--gc) 7%,transparent);box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--gc) 16%,transparent)}
.gpill{display:flex;align-items:center;height:20px;padding:0 9px;border-radius:var(--r-sm);flex:none;background:color-mix(in srgb,var(--gc) 15%,transparent);color:var(--gc);font-size:10.5px;font-weight:650;letter-spacing:.01em;white-space:nowrap;cursor:pointer;transition:background var(--dur-2)}
.gpill:hover{background:color-mix(in srgb,var(--gc) 26%,transparent)}
.gpill .gp-c{width:0;opacity:0;margin-left:0;transition:width var(--dur-2),opacity var(--dur-2),margin-left var(--dur-2);transform:rotate(180deg)}
.gpill:hover .gp-c{width:10px;opacity:.9;margin-left:4px}
body.tdrag .gpill{cursor:grabbing}
.nova.light .gpill{color:color-mix(in srgb,var(--gc) 78%,#000)}
.vrun-l{display:flex;align-items:center;gap:6px;width:100%;text-align:left;padding:9px 10px 4px;margin:0;border:none;background:none;font-size:8.5px;font-weight:650;letter-spacing:.09em;text-transform:uppercase;color:var(--gc);opacity:.65;transition:opacity var(--dur-2)}
.vrun-l:hover{opacity:1}
.vrun-l::after{content:"";flex:1;height:1px;background:linear-gradient(90deg,color-mix(in srgb,var(--gc) 55%,transparent),color-mix(in srgb,var(--gc) 12%,transparent))}
/* ---- base-page polish ---- */
.ptitle{font-size:22px;font-weight:600;letter-spacing:-.02em;margin-bottom:6px;display:flex;align-items:center;gap:10px}
.ab-hero{padding:26px;display:flex;gap:20px;align-items:center}
.ab-name{font-size:19px;font-weight:600;letter-spacing:-.01em;display:flex;align-items:center;gap:8px}
.ab-tag{color:var(--tx2);font-size:13px;margin-top:5px;line-height:1.55}
.ab-chips{display:flex;gap:6px;margin-top:12px;flex-wrap:wrap}
.ab-chip{display:inline-flex;align-items:center;gap:5px;font-size:10px;color:var(--tx3);border:1px solid var(--line);border-radius:var(--r-sm);padding:3px 8px}
.ab-chip.up{color:var(--good);border-color:color-mix(in srgb,var(--good) 30%,transparent)}
.ab-grid{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--line);border:1px solid var(--line);border-radius:var(--r-lg);overflow:hidden}
.ab-cell{background:var(--c2);padding:16px 18px}
.ab-cell .t{font-size:13px;font-weight:550;margin-bottom:5px}
.ab-cell .d{font-size:12px;color:var(--tx3);line-height:1.6}
.hday{width:74px;flex:none;font-size:10px;color:var(--tx3);text-align:left}
.dl-head{display:flex;align-items:center;margin-bottom:10px;font-size:11px;color:var(--tx3)}
.dl-row.blocked .dl-mid{opacity:.7}
/* ---- agent page v2 ---- */
.ag-card{flex:1;min-width:0;background:var(--c2);border:1px solid var(--line);border-radius:var(--r-lg);padding:16px 18px;display:flex;flex-direction:column}
.ag-ch{font-size:12.5px;font-weight:550;color:var(--tx3);margin-bottom:12px}
.ag-foot{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:auto;padding-top:14px;border-top:1px solid var(--line)}
.hclear.pri{color:var(--ac);border-color:var(--ac-line)}
.hclear.pri:disabled{opacity:.45}
.ag-empty{border:1px dashed var(--line2);border-radius:var(--r);padding:18px 16px;font-size:12px;color:var(--tx3);line-height:1.65;margin-bottom:14px}
.ag-empty .mono{font-size:9.5px;letter-spacing:.08em;text-transform:uppercase;margin-bottom:6px;color:var(--tx3)}
.ag-steps{display:flex;flex-direction:column;gap:5px;margin-bottom:12px}
.ag-cap{font-size:9.5px;color:var(--good);border:1px solid color-mix(in srgb,var(--good) 35%,transparent);border-radius:var(--r-sm);padding:1px 0;width:64px;text-align:center;flex:none}
/* ---- attio-grade buttons & focus ---- */
.btn-pri{display:inline-flex;align-items:center;gap:7px;height:32px;padding:0 13px;border-radius:var(--r);background:var(--ac);color:#fff;font-size:12.5px;font-weight:550;transition:filter var(--dur-2),transform var(--dur-2);border:1px solid color-mix(in srgb,var(--ac) 85%,#000)}
.btn-pri:hover{filter:brightness(1.06)}
.btn-pri:active{transform:scale(.985)}
.btn-pri:disabled{opacity:.5}
.btn-pri .kbd,.hclear .kbd{border-color:transparent;background:rgba(255,255,255,.2);color:inherit;font-size:9.5px;padding:1px 5px}
.hclear .kbd{background:var(--c3);color:var(--tx3)}
.nova.light .pop,.nova.light .modal,.nova.light .cmd{box-shadow:0 18px 48px -12px rgba(23,24,26,.18),0 2px 8px rgba(23,24,26,.06)}
.nova.light .card{background:var(--c1)}
.nova.light .bar{background:var(--c1)}
.nova.light .vtabs{background:var(--c2)}
.ag-task:focus,.hp-in:focus,.th-json textarea:focus,.hsearch.focus,.ag-task:focus-visible{border-color:var(--ac-line);box-shadow:0 0 0 3px var(--ac-soft)}
.vchip{display:inline-flex;align-items:center;border-radius:var(--r-sm);padding:1px 7px;background:var(--ac-soft);color:var(--ac);font-size:11.5px;font-family:var(--mono)}
/* ---- page header system ---- */
.phead{position:sticky;top:0;z-index:6;background:color-mix(in srgb,var(--ink) 92%,transparent);backdrop-filter:blur(10px);border-bottom:1px solid var(--line);flex:none}
.pcol{width:100%;max-width:var(--colw,880px);margin:0 auto;min-width:0}
.phead-in{display:flex;align-items:center;gap:10px;height:54px}
.ph-acts .hclear,.ph-acts .btn-pri,.ph-acts button{height:28px}
.ph-t{font-size:15px;font-weight:600;letter-spacing:-.01em}
.ph-chip{font-size:10px;color:var(--tx3);border:1px solid var(--line);border-radius:var(--r-sm);padding:2px 7px;background:var(--c2)}
.ph-acts{margin-left:auto;display:flex;align-items:center;gap:8px}
.page .phead{margin:0 -40px}
/* ---- table footers ---- */
.tfoot{display:flex;align-items:center;gap:14px;padding:10px 16px;font-size:11px;color:var(--tx3);border-top:1px solid var(--line);background:var(--c2)}
.tfoot .mono{font-variant-numeric:tabular-nums}
/* ---- floating selection toolbar ---- */
.selbar{position:absolute;left:50%;bottom:22px;transform:translateX(-50%);z-index:80;display:flex;align-items:center;gap:4px;background:var(--c1);border:1px solid var(--line2);border-radius:var(--r-lg);padding:6px 8px;box-shadow:0 20px 50px -12px rgba(23,24,26,.28),0 3px 10px rgba(23,24,26,.08);animation:pop var(--dur-3) both}
.selbar .n{display:flex;align-items:center;gap:6px;background:var(--ac);color:#fff;font-size:11.5px;font-weight:600;border-radius:var(--r);padding:5px 10px;margin-right:4px}
.selbar .hclear{height:28px}
.selbar .x{width:26px;height:26px;border-radius:var(--r-sm);display:grid;place-items:center;color:var(--tx3)}
.selbar .x:hover{background:var(--c3);color:var(--tx)}
/* ---- row selection circles (history) ---- */
.hrow .sel{width:16px;height:16px;border-radius:50%;border:1.5px solid var(--line2);flex:none;display:grid;place-items:center;opacity:0;transition:opacity var(--dur-2),background var(--dur-2),border-color var(--dur-2);background:var(--c1)}
.hrow:hover .sel,.hrow .sel.on{opacity:1}
.hrow .sel.on{background:var(--ac);border-color:var(--ac);color:#fff}
.hrow.selected{background:var(--ac-soft)}
.vdragproxy{position:absolute;z-index:120;pointer-events:none;background:var(--c1);border:1px solid var(--line2);box-shadow:0 14px 34px -10px color-mix(in srgb,var(--tx) 35%,transparent);opacity:.95}
.vsec.vdrop{outline:1.5px solid var(--ac);outline-offset:2px;border-radius:var(--r);background:var(--ac-soft)}
.vtab.vbefore{box-shadow:inset 0 2px 0 var(--ac)}
.vtab.ghost{opacity:.35}
.urlpeek{position:absolute;left:10px;bottom:10px;z-index:60;max-width:46%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;background:var(--c1);border:1px solid var(--line2);border-radius:var(--r-sm);padding:4px 9px;font-size:10.5px;color:var(--tx2);box-shadow:0 6px 18px -6px color-mix(in srgb,var(--tx) 25%,transparent);animation:fade var(--dur-2) both;pointer-events:none}
/* ---- error page ---- */
.errwrap{max-width:460px;margin:11vh auto 0;display:flex;flex-direction:column;align-items:flex-start;gap:0}
.err-ic{width:56px;height:56px;border-radius:var(--r-lg);background:var(--c2);border:1px solid var(--line);display:grid;place-items:center;color:var(--tx3);margin-bottom:20px}
.err-t{font-size:20px;font-weight:600;letter-spacing:-.01em}
.err-s{font-size:13px;color:var(--tx2);line-height:1.65;margin-top:9px}
.err-acts{display:flex;gap:8px;margin-top:22px;flex-wrap:wrap}
.err-note{display:flex;align-items:center;gap:7px;font-size:12px;color:var(--tx3);margin-top:22px}
.err-more{margin-top:16px;font-size:10.5px;color:var(--tx3);text-decoration:underline;text-underline-offset:3px}
.err-more:hover{color:var(--tx)}
.err-det{margin-top:10px;font-size:10.5px;color:var(--tx3);border:1px solid var(--line);border-radius:var(--r);padding:9px 11px;background:var(--c2);line-height:1.7}
/* ================= premium feel pass ================= */
.nova::after{content:"";position:absolute;inset:0;pointer-events:none;z-index:1;background-image:url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2'/%3E%3C/filter%3E%3Crect width='160' height='160' filter='url(%23n)' opacity='0.55'/%3E%3C/svg%3E\");opacity:.022;mix-blend-mode:overlay}
.nova.light::after{opacity:.028}
/* text selection carries the brand (and the space tint) */
.nova ::selection{background:color-mix(in srgb,var(--ac) 25%,transparent);color:var(--tx)}
/* themed scrollbars — thin, quiet, alive on hover */
.nova *{scrollbar-width:thin;scrollbar-color:var(--c4) transparent}
.nova ::-webkit-scrollbar{width:9px;height:9px}
.nova ::-webkit-scrollbar-track{background:transparent}
.nova ::-webkit-scrollbar-thumb{background:var(--c4);border-radius:7px;border:2.5px solid transparent;background-clip:content-box}
.nova ::-webkit-scrollbar-thumb:hover{background:var(--line2);border:2px solid transparent;background-clip:content-box}
/* cards lit from above — the single strongest "expensive" cue */
.card,.ag-card,.hlist,.tm-view,.ab-hero{box-shadow:inset 0 1px 0 rgba(255,255,255,.04)}
.nova.light .card,.nova.light .ag-card,.nova.light .hlist,.nova.light .tm-view,.nova.light .ab-hero{box-shadow:inset 0 1px 0 #fff,0 1px 2px rgba(23,24,26,.04)}
/* physical press — everything interactive gives 2% */
.hclear:active,.btn-pri:active,.chip:active,.ib:active,.mitem:active,.qa:active,.th-card:active,.q:active,.spacepill:active,.vnew-top:active{transform:scale(.975)}
.hclear,.chip,.ib,.mitem,.qa,.th-card,.spacepill,.vnew-top{transition:background var(--dur-2),border-color var(--dur-2),color var(--dur-2),transform var(--dur-1)}
/* page entrances — content rises into place, children stagger */
.page{min-height:100%;display:flex;padding-top:0;animation:pagein .28s var(--ease-out) both}
@keyframes pagein{from{opacity:0;transform:translateY(7px)}to{opacity:1;transform:none}}
.pbody>*{animation:rowin .32s var(--ease-out) both}
.pbody>*:nth-child(1){animation-delay:.02s}.pbody>*:nth-child(2){animation-delay:.05s}
.pbody>*:nth-child(3){animation-delay:var(--dur-1)}.pbody>*:nth-child(4){animation-delay:.11s}
.pbody>*:nth-child(5){animation-delay:var(--dur-2)}.pbody>*:nth-child(6){animation-delay:.17s}
.pbody>*:nth-child(n+7){animation-delay:.19s}
@keyframes rowin{from{opacity:0;transform:translateY(5px)}to{opacity:1;transform:none}}
/* interactive rows announce themselves */
.mitem,.hrow,.dl-row,.vtab,.cmd-it,.rt-row{cursor:default}
.hclear,.btn-pri,.chip,.ib,.qa,.q,.th-card,.spacepill,.vnew-top,.pnav a,.vsec-h{cursor:pointer}
/* the professional tell: motion respects the person */
@media (prefers-reduced-motion:reduce){
  .nova *,.nova *::before,.nova *::after{animation-duration:.001s !important;animation-delay:0s !important;transition-duration:.001s !important}
}
/* ===== inspector dock ===== */
/* ---- spaces ---- */
.spaces{display:flex;gap:3px;flex:none;align-items:center}
.sp{display:flex;align-items:center;gap:6px;height:24px;padding:0 7px;border-radius:var(--r);transition:background var(--dur-2)}
.sp:hover{background:var(--c3)}
.sp .spd{width:9px;height:9px;border-radius:4px;background:var(--st);opacity:.5;transition:opacity var(--dur-2)}
.sp.on .spd{opacity:1}
.sp .spn{font-size:11px;color:var(--tx2);font-weight:500}
/* ---- reading list on new tab ---- */
.rlist{width:min(560px,86%);margin:18px auto 0;border:1px solid var(--line);border-radius:var(--r-lg);padding:10px 12px;background:var(--c1)}
.rl-cap{display:flex;align-items:center;gap:7px;font-size:10px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--tx3);margin-bottom:6px}
.rl-row{display:flex;align-items:center;gap:10px;padding:5px 0;border-top:1px solid var(--line)}
.rl-t{font-size:12.5px;color:var(--tx);text-align:left;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;flex:1}
.rl-t:hover{color:var(--ac)}
.rl-u{font-size:10.5px;color:var(--tx3);flex:none}
/* ---- downloads ---- */
.dl-row{display:flex;align-items:center;gap:12px;padding:11px 14px;border-bottom:1px solid var(--line)}
.dl-ic{min-width:36px;height:24px;padding:0 7px;border-radius:var(--r-sm);border:1px solid var(--line);background:var(--c1);display:grid;place-items:center;color:var(--tx3);flex:none;font-size:9px;font-weight:650;letter-spacing:.06em;text-transform:uppercase}
.dl-mid{flex:1;min-width:0}
.dl-n{font-size:12.5px;color:var(--tx);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.dl-row > div{min-width:0}
.dl-n.blk{color:var(--bad);text-decoration:line-through}
.dl-s{font-size:10.5px;color:var(--tx3);margin-top:2px}
.dl-bar{height:4px;border-radius:4px;background:var(--c3);margin-top:7px;overflow:hidden}
.dl-bar i{display:block;height:100%;background:var(--ac);border-radius:4px}
.dl-blk{display:flex;align-items:center;gap:6px;font-size:11px;color:var(--bad);flex:none}
/* ---- nova mini ---- */
/* ---- ask nova extras ---- */
.ai-prev{display:flex;align-items:center;gap:10px;border:1px solid var(--line);border-radius:var(--r);padding:9px 11px;background:var(--c1);font-size:10.5px;color:var(--tx3)}
.ai-pv{flex:1;display:flex;flex-direction:column;gap:5px}
.ai-maker{padding:10px 12px;border-top:1px solid var(--line);display:flex;flex-direction:column;gap:7px;flex:none}
.ai-maker input{background:var(--c2);border:1px solid var(--line);border-radius:var(--r);padding:7px 10px;outline:none;color:var(--tx);font-size:12px}
.ai-maker input:focus{border-color:var(--ac-line)}
/* ---- boost + translate ---- */
.trbar{position:sticky;top:10px;z-index:4;margin:10px auto 0;width:fit-content;display:flex;align-items:center;gap:8px;background:var(--ac-soft);border:1px solid var(--line2);border-radius:var(--r);padding:0 14px;font-size:11.5px;color:var(--tx2);box-shadow:0 10px 30px -10px color-mix(in srgb,var(--tx) 25%,transparent);height:32px;border-bottom:1px solid var(--ac-line);flex:none}
.trbar button{color:var(--ac);font-size:11.5px;margin-left:auto}
/* ---- per-site permissions ---- */
.permrow{display:flex;align-items:center;gap:9px;padding:5px 0;font-size:12px;color:var(--tx2)}
.permrow .seg button{font-size:10px;padding:3px 7px}
/* ---- tab groups · quiet segments ---- */
.tseg-d{width:6px;height:6px;border-radius:2px;background:var(--gc);flex:none}
/* ---- Ask Turing panel ---- */
.aiwrap{position:absolute;right:18px;bottom:18px;z-index:59;width:404px;max-width:calc(100% - 36px);height:min(628px,calc(100% - 96px));background:var(--c1);border:1px solid var(--line2);border-radius:14px;display:flex;flex-direction:column;overflow:hidden;box-shadow:0 36px 88px -28px color-mix(in srgb,var(--tx) 50%,transparent),0 6px 20px -8px color-mix(in srgb,var(--tx) 24%,transparent),0 0 0 1px rgba(0,0,0,.04);animation:aipop .22s var(--ease-out) both;transform-origin:bottom right}
@keyframes aipop{from{opacity:0;transform:translateY(18px) scale(.965)}to{opacity:1;transform:none}}
@keyframes slidein{from{transform:translateX(24px);opacity:0}to{transform:none;opacity:1}}
.ai-h{display:flex;align-items:center;gap:10px;height:54px;padding:0 10px 0 14px;border-bottom:1px solid var(--line);flex:none}
.ai-hemblem{width:27px;height:27px;border-radius:7px;display:grid;place-items:center;background:var(--ac-soft);border:1px solid var(--ac-line);flex:none}
.ai-htext{display:flex;flex-direction:column;line-height:1.18;min-width:0;margin-right:auto}
.ai-htitle{font-size:13px;font-weight:600;letter-spacing:-.01em}
.ai-hsub{font-size:10.5px;color:var(--tx3);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ai-hbtn{width:28px;height:28px;border-radius:7px;display:grid;place-items:center;color:var(--tx3);flex:none;transition:background var(--dur-2),color var(--dur-2)}
.ai-hbtn:hover{background:var(--c2);color:var(--tx2)}
.ai-menu{position:absolute;bottom:60px;left:12px;right:12px;background:var(--c2);border:1px solid var(--line2);border-radius:10px;padding:5px;box-shadow:0 18px 48px -14px color-mix(in srgb,var(--tx) 31%,transparent);animation:pop var(--dur-2) both;z-index:5;max-height:280px;overflow-y:auto}
/* ---- Ask Turing: threads, streaming, rich messages ---- */
.aiwrap.wide{width:648px;height:min(760px,calc(100% - 96px))}
.ai-hbtn.on{background:var(--ac-soft);color:var(--ac)}
.ai-gap{height:7px}
.ai-li{padding-left:14px;position:relative}
.ai-li::before{content:"·";position:absolute;left:4px;color:var(--tx3)}
.ai-code{font-family:var(--mono);font-size:11px;background:var(--c4);border:1px solid var(--line);border-radius:4px;padding:1px 5px}
.ai-pre{margin:8px 0;border:1px solid var(--line);border-radius:10px;overflow:hidden;background:var(--c1)}
.ai-pre-h{display:flex;align-items:center;justify-content:space-between;padding:5px 8px 5px 10px;background:var(--c3);border-bottom:1px solid var(--line);font-size:10px;color:var(--tx3)}
.ai-pre-h button{display:flex;align-items:center;gap:4px;font-size:10px;color:var(--tx3);padding:2px 6px;border-radius:4px}
.ai-pre-h button:hover{background:var(--c4);color:var(--tx2)}
.ai-pre pre{margin:0;padding:10px;font-size:11px;line-height:1.6;overflow-x:auto;color:var(--tx2);white-space:pre}
.ai-caret{display:inline-block;width:6px;height:12px;background:var(--ac);vertical-align:-1px;margin-left:2px;animation:aicaret .9s steps(2) infinite}
@keyframes aicaret{0%,100%{opacity:1}50%{opacity:0}}
.ai-drawer{position:absolute;inset:54px 0 0;z-index:4;background:var(--c1);display:flex;flex-direction:column;animation:slidein var(--dur-3) var(--ease-out) both}
.ai-dh{display:flex;align-items:center;gap:7px;padding:10px 12px;border-bottom:1px solid var(--line);flex:none}
.ai-dh input{flex:1;background:none;border:none;outline:none;color:var(--tx);font-size:12.5px}
.ai-dh button{width:24px;height:24px;border-radius:7px;display:grid;place-items:center;color:var(--tx3);flex:none}
.ai-dh button:hover{background:var(--c2)}
.ai-dlist{flex:1;overflow-y:auto;padding:8px}
.ai-dempty{padding:22px 12px;text-align:center;font-size:12px;color:var(--tx3);line-height:1.6}
.ai-th{display:flex;align-items:center;gap:2px;border-radius:7px;padding:2px 4px 2px 2px}
.ai-th:hover{background:var(--c2)}
.ai-th.on{background:var(--ac-soft)}
.ai-tht{flex:1;display:flex;align-items:center;gap:8px;text-align:left;padding:8px;min-width:0}
.ai-thn{flex:1;font-size:12.5px;color:var(--tx2);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.ai-th.on .ai-thn{color:var(--tx)}
.ai-thm{font-size:9.5px;color:var(--tx3);flex:none}
.ai-thb{width:22px;height:22px;border-radius:7px;display:grid;place-items:center;color:var(--tx3);opacity:0;flex:none}
.ai-th:hover .ai-thb{opacity:1}
.ai-thb:hover{background:var(--c3);color:var(--tx2)}
.ai-thr{flex:1;background:var(--c1);border:1px solid var(--ac-line);border-radius:7px;padding:6px 8px;color:var(--tx);font-size:12.5px;outline:none;min-width:0}
/* ---- shadcn chat primitives: scroller, message, bubble, attachment, marker ---- */
.msc-wrap{flex:1;position:relative;min-height:0}
.msc{height:100%;overflow-y:auto;padding:16px 14px 10px}
.scroll-fade{-webkit-mask-image:linear-gradient(to bottom,transparent 0,#000 16px,#000 calc(100% - 22px),transparent 100%);mask-image:linear-gradient(to bottom,transparent 0,#000 16px,#000 calc(100% - 22px),transparent 100%)}
.scroll-fade.at-end{-webkit-mask-image:linear-gradient(to bottom,transparent 0,#000 16px,#000 100%);mask-image:linear-gradient(to bottom,transparent 0,#000 16px,#000 100%)}
.att-row.scroll-fade,.sugs.scroll-fade,.pi-atts.scroll-fade{-webkit-mask-image:linear-gradient(to right,#000 0,#000 calc(100% - 16px),transparent 100%);mask-image:linear-gradient(to right,#000 0,#000 calc(100% - 16px),transparent 100%)}
.msc-jump{position:absolute;left:50%;bottom:12px;transform:translateX(-50%);width:28px;height:28px;border-radius:50%;display:grid;place-items:center;background:var(--c3);border:1px solid var(--line2);color:var(--tx2);z-index:3;box-shadow:0 8px 20px -8px color-mix(in srgb,var(--tx) 40%,transparent);animation:pop var(--dur-2) both}
.msc-jump:hover{background:var(--c4);color:var(--tx)}
.shimmer{background:linear-gradient(90deg,var(--tx3) 0%,var(--tx) 45%,var(--tx3) 90%);background-size:220% 100%;-webkit-background-clip:text;background-clip:text;color:transparent;animation:shim 1.9s linear infinite}
@keyframes shim{from{background-position:190% 0}to{background-position:-50% 0}}
.msg{display:flex;gap:9px;align-items:flex-start;margin-bottom:15px}
.msg.grouped{margin-top:-9px}
.msg.is-user{flex-direction:row-reverse}
.msg-av{width:24px;height:24px;border-radius:7px;display:grid;place-items:center;flex:none;font-size:9.5px;font-weight:700;color:var(--tx3);background:var(--c3);border:1px solid var(--line);margin-top:1px}
.msg-av.is-assistant{color:var(--ac);background:var(--ac-soft);border-color:var(--ac-line)}
/* accent-on-tint needs a darker accent in light to clear 3:1 for non-text UI */
.nova.light .msg-av.is-assistant,.nova.light .msg-src-i .mono,.nova.light .cv-emblem{color:color-mix(in srgb,var(--ac) 76%,#000)}
.msg-av-sp{width:24px;flex:none}
.msg-body{min-width:0;max-width:87%;display:flex;flex-direction:column;gap:5px}
.msg.is-user .msg-body{align-items:flex-end}
.msg-h{display:flex;align-items:center;gap:6px;font-size:10.5px;color:var(--tx3);padding:0 2px}
.msg-who{font-weight:650;color:var(--tx2);letter-spacing:-.01em}
.msg-model{font-size:9px;padding:1px 5px;border-radius:4px;background:var(--c3);color:var(--tx3);border:1px solid var(--line)}
.msg-f{min-height:20px;padding:0 2px}
.bub{font-size:12.5px;line-height:1.62;padding:10px 13px;border-radius:14px;min-width:0;overflow-wrap:anywhere}
.bub.is-assistant{background:var(--c2);border:1px solid var(--line);color:var(--tx2);border-top-left-radius:5px}
.bub.is-user{background:var(--ac-soft);border:1px solid var(--ac-line);color:var(--tx);border-top-right-radius:5px}
.att-row{display:flex;gap:6px;overflow-x:auto;padding-bottom:1px}
.att{display:inline-flex;align-items:center;gap:7px;flex:none;max-width:190px;background:var(--c2);border:1px solid var(--line);border-radius:10px;padding:5px 7px}
.att-m{width:20px;height:20px;border-radius:7px;display:grid;place-items:center;background:var(--c4);color:var(--tx3);flex:none}
.att-t{display:flex;flex-direction:column;min-width:0;line-height:1.25}
.att-n{font-size:11px;color:var(--tx2);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.att-meta{font-size:8.5px;color:var(--tx3)}
.att-x{width:16px;height:16px;border-radius:4px;display:grid;place-items:center;color:var(--tx3);flex:none}
.att-x:hover{background:var(--c4);color:var(--tx2)}
.mk{display:flex;align-items:center;gap:6px}
.mk.is-note{font-size:10px;color:var(--tx3)}
.mk.is-live{font-size:12.5px;font-weight:500;padding:2px 0}
.msg-acts{display:flex;align-items:center;gap:2px;opacity:0;transition:opacity var(--dur-2)}
.msg:hover .msg-acts,.msg:focus-within .msg-acts{opacity:1}
.msg-act{width:22px;height:22px;border-radius:7px;display:grid;place-items:center;color:var(--tx3)}
.msg-act:hover{background:var(--c3);color:var(--tx2)}
.msg-act.good{color:var(--good)}
.msg-act.bad{color:var(--bad)}
.msg-src{display:flex;flex-direction:column;gap:5px;align-items:flex-start}
.msg-src-t{display:inline-flex;align-items:center;gap:5px;font-size:10.5px;color:var(--tx2);background:var(--c2);border:1px solid var(--line);border-radius:999px;padding:3px 9px}
.msg-src-t:hover{border-color:var(--line2);color:var(--tx)}
.msg-src-t .rot{transform:rotate(180deg)}
.msg-src-c{display:flex;flex-wrap:wrap;gap:5px}
.msg-src-i{display:inline-flex;align-items:center;gap:5px;font-size:10.5px;color:var(--tx2);background:var(--c2);border:1px solid var(--line);border-radius:var(--r-sm);padding:3px 7px}
.msg-src-i:hover{border-color:var(--ac-line);color:var(--ac)}
.msg-src-i .mono{width:13px;height:13px;border-radius:4px;background:var(--ac-soft);color:var(--ac);display:grid;place-items:center;font-size:8.5px}
.sugs{display:flex;gap:6px;overflow-x:auto;padding:0 0 8px 33px}
.sug-chip{flex:none;font-size:11.5px;color:var(--tx2);background:var(--c2);border:1px solid var(--line);border-radius:999px;padding:5px 12px;white-space:nowrap}
.sug-chip:hover{border-color:var(--ac-line);color:var(--ac)}
.cv-empty{margin:auto 0;display:flex;flex-direction:column;align-items:center;text-align:center;gap:9px;padding:18px 6px}
.cv-emblem{width:44px;height:44px;border-radius:14px;display:grid;place-items:center;background:var(--ac-soft);border:1px solid var(--ac-line)}
.cv-et{font-size:15px;font-weight:600;letter-spacing:-.02em}
.cv-es{font-size:12px;color:var(--tx3);line-height:1.6;max-width:284px}
.cv-esugs{display:flex;flex-direction:column;gap:7px;width:100%;margin-top:6px}
.cv-esug{display:flex;align-items:center;gap:9px;text-align:left;font-size:12px;color:var(--tx2);background:var(--c2);border:1px solid var(--line);border-radius:10px;padding:9px 11px}
.cv-esug:hover{background:var(--c3);border-color:var(--line2)}
.cv-esug .mono{color:var(--ac);flex:none}
.cv-esug span:last-child{color:var(--tx3);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
/* ---- AI Elements: prompt input ---- */
.pi-wrap{position:relative;padding:10px 12px 12px;flex:none}
.pi{background:var(--c2);border:1px solid var(--line2);border-radius:14px;transition:border-color var(--dur-2),box-shadow var(--dur-2)}
.pi:focus-within{border-color:var(--ac-line);box-shadow:0 0 0 3px var(--ac-soft)}
.pi-body{padding:10px 12px 2px}
.pi-atts{display:flex;gap:6px;overflow-x:auto;padding-bottom:9px}
.pi-ta{width:100%;background:none;border:none;outline:none;color:var(--tx);font:inherit;font-size:13px;line-height:1.5;resize:none;max-height:132px;display:block;padding:0}
.pi-ta::placeholder{color:var(--tx3)}
.pi-bar{display:flex;align-items:center;gap:6px;padding:4px 8px 8px 9px}
.pi-tools{display:flex;align-items:center;gap:3px;min-width:0}
.pi-btn{display:inline-flex;align-items:center;gap:4px;height:26px;padding:0 8px;border-radius:999px;font-size:11px;color:var(--tx2);border:1px solid transparent;white-space:nowrap}
.pi-btn:hover{background:var(--c3);color:var(--tx)}
.pi-btn.on{color:var(--ac);background:var(--ac-soft);border-color:var(--ac-line)}
.pi-right{margin-left:auto;display:flex;align-items:center;gap:6px;flex:none}
.pi-meter{font-size:9.5px;color:var(--tx3);white-space:nowrap}
.pi-model{display:inline-flex;align-items:center;gap:4px;height:26px;padding:0 8px;border-radius:999px;font-size:11px;color:var(--tx2);border:1px solid var(--line);white-space:nowrap}
.pi-model:hover{color:var(--tx);border-color:var(--line2)}
.pi-send{width:30px;height:30px;border-radius:50%;display:grid;place-items:center;background:var(--ac);color:#fff;flex:none;transition:background var(--dur-2),opacity var(--dur-2)}
.pi-send:active{transform:scale(.93)}
.pi-send[disabled]{background:var(--c4);color:var(--tx3);cursor:default}
.pi-send.is-streaming{background:var(--c4);color:var(--tx)}
.pi-spin{width:13px;height:13px;border-radius:50%;border:2px solid color-mix(in srgb,#fff 35%,transparent);border-top-color:#fff;animation:pispin .7s linear infinite}
@keyframes pispin{to{transform:rotate(360deg)}}
.pi-wrap .ai-menu{bottom:calc(100% - 2px);left:12px;right:12px}
/* ---- Turing Shield panel ---- */
.pop.shp{padding-bottom:0;overflow:hidden}
.shp-hero{display:flex;align-items:center;gap:12px;padding:14px 16px 12px}
.shp-big{font-size:34px;font-weight:600;line-height:1;color:var(--ac);letter-spacing:-.03em}
.shp-blurb{font-size:11.5px;color:var(--tx3);line-height:1.5}
.shp-blurb b{color:var(--tx2);font-weight:600}
.shp-seg{display:flex;gap:3px;margin:0 14px;padding:3px;background:var(--c1);border:1px solid var(--line);border-radius:10px}
.shp-segb{flex:1;height:26px;border-radius:7px;font-size:11px;font-weight:550;color:var(--tx3)}
.shp-segb:hover{color:var(--tx2)}
.shp-segb.on{background:var(--c3);color:var(--tx);box-shadow:0 1px 2px color-mix(in srgb,var(--ink) 22%,transparent)}
.shp-desc{font-size:10.5px;color:var(--tx3);line-height:1.5;padding:8px 16px 10px}
.shp-tabs{display:flex;gap:14px;padding:0 16px;border-bottom:1px solid var(--line)}
.shp-tabs button{padding:7px 0 8px;font-size:11.5px;color:var(--tx3);border-bottom:1.5px solid transparent;margin-bottom:-1px;display:flex;align-items:center;gap:5px}
.shp-tabs button .mono{font-size:9.5px;background:var(--c3);border-radius:4px;padding:1px 4px}
.shp-tabs button:hover{color:var(--tx2)}
.shp-tabs button.on{color:var(--tx);border-bottom-color:var(--ac)}
.shp-list{max-height:196px;overflow-y:auto;padding:6px 8px}
.shp-row{display:flex;align-items:center;gap:8px;padding:6px 8px;border-radius:7px}
.shp-row:hover{background:var(--c2)}
.shp-row.muted .shp-nm{color:var(--tx3)}
.shp-dot{width:6px;height:6px;border-radius:50%;flex:none;background:var(--tx3)}
.shp-dot[data-cat="ads"]{background:#f87171}
.shp-dot[data-cat="analytics"]{background:#fbbf24}
.shp-dot[data-cat="social"]{background:#60a5fa}
.shp-dot[data-cat="session"]{background:#c084fc}
.shp-dot[data-cat="tag"]{background:#34d399}
.shp-dot[data-cat="widget"]{background:#94a3b8}
.shp-nm{font-size:12px;color:var(--tx2);flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.shp-cat{font-size:9.5px;color:var(--tx3);flex:none}
.shp-c{font-size:10.5px;color:var(--tx3);min-width:16px;text-align:right;flex:none}
.shp-conn{display:flex;align-items:flex-start;gap:9px;padding:8px}
.shp-conn > div{display:flex;flex-direction:column;gap:2px;min-width:0}
.shp-conn b{font-size:12px;color:var(--tx2);font-weight:550}
.shp-conn span{font-size:10.5px;color:var(--tx3);line-height:1.45}
.shp-foot{display:flex;align-items:center;justify-content:space-between;padding:9px 14px;border-top:1px solid var(--line);background:var(--c1);font-size:10.5px;color:var(--tx3)}
.shp-foot b{color:var(--tx2)}
.shp-foot button{display:inline-flex;align-items:center;gap:5px;font-size:11px;color:var(--tx2);padding:4px 8px;border-radius:7px}
.shp-foot button:hover{background:var(--c3);color:var(--tx)}
.shbadge{position:absolute;top:2px;right:1px;min-width:13px;height:13px;padding:0 3px;border-radius:7px;background:color-mix(in srgb,var(--ac) 74%,#000);color:#fff;font-size:8.5px;font-weight:700;display:grid;place-items:center;font-family:var(--mono);pointer-events:none}
/* ---- password vault ---- */
.kdot{position:absolute;top:5px;right:5px;width:6px;height:6px;border-radius:50%;background:var(--good);pointer-events:none}
.vlock{display:flex;flex-direction:column;align-items:center;gap:9px;text-align:center;padding:44px 20px;background:var(--c2);border:1px solid var(--line);border-radius:var(--r-lg)}
.vlock-i{width:46px;height:46px;border-radius:14px;display:grid;place-items:center;background:var(--ac-soft);border:1px solid var(--ac-line)}
.vlock-t{font-size:15px;font-weight:600;letter-spacing:-.02em}
.vlock-s{font-size:12px;color:var(--tx3);margin-bottom:6px}
.vhealth{background:var(--c2);border:1px solid var(--line);border-radius:var(--r-lg);padding:13px 15px;margin-bottom:14px}
.vh-h{display:flex;align-items:center;gap:7px;font-size:12.5px;color:var(--tx2)}
.vh-h b{font-weight:600}
.vh-h button{margin-left:auto;font-size:11px;color:var(--ac);padding:3px 9px;border-radius:7px;border:1px solid var(--ac-line)}
.vh-h button:hover{background:var(--ac-soft)}
.vh-stats{display:flex;gap:20px;margin-top:11px}
.vh-stats div{display:flex;align-items:baseline;gap:6px;font-size:11px;color:var(--tx3)}
.vh-stats .mono{font-size:19px;font-weight:600}
.vbar{display:flex;align-items:center;gap:7px;margin-bottom:12px}
.vsearch{flex:1;display:flex;align-items:center;gap:7px;height:32px;padding:0 11px;background:var(--c2);border:1px solid var(--line);border-radius:7px}
.vsearch input{flex:1;background:none;border:none;outline:none;color:var(--tx);font-size:12.5px}
.vgen{background:var(--c2);border:1px solid var(--line);border-radius:var(--r-lg);padding:13px;margin-bottom:13px;display:flex;flex-direction:column;gap:11px}
.vgen-out{background:var(--c1);border:1px solid var(--line);border-radius:7px;padding:11px 13px;font-size:13.5px;color:var(--tx);word-break:break-all;letter-spacing:.02em}
.vgen-ctl{display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.vgen-ctl label{display:flex;align-items:center;gap:8px;font-size:11.5px;color:var(--tx3);flex:1;min-width:180px}
.vgen-ctl input[type=range]{flex:1;accent-color:var(--ac)}
.vgen-opts{display:flex;gap:5px}
.vgen-opts button{font-size:11px;font-family:var(--mono);color:var(--tx3);border:1px solid var(--line);border-radius:7px;padding:4px 9px}
.vgen-opts button.on{color:var(--ac);border-color:var(--ac-line);background:var(--ac-soft)}
.vgen-act{display:flex;gap:7px;justify-content:flex-end}
.pwm{display:flex;align-items:center;gap:9px;font-size:11px}
.pwm-bars{display:flex;gap:3px}
.pwm-bars i{width:26px;height:4px;border-radius:2px;background:var(--c4)}
.vlist{display:flex;flex-direction:column;gap:5px;margin-bottom:20px}
.vempty{padding:26px;text-align:center;font-size:12px;color:var(--tx3)}
.vrow-w{border:1px solid var(--line);border-radius:10px;background:var(--c2);overflow:hidden}
.vrow-w.open{border-color:var(--ac-line)}
.vrow{display:flex;align-items:center;gap:9px;width:100%;padding:10px 12px;text-align:left}
.vrow:hover{background:var(--c3)}
.v-site{display:flex;flex-direction:column;gap:1px;min-width:0;flex:1;font-size:12.5px;color:var(--tx2)}
.v-user{font-size:10.5px;color:var(--tx3);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.vtag{display:inline-flex;align-items:center;gap:3px;font-size:9px;padding:2px 6px;border-radius:4px;background:var(--c4);color:var(--tx3);flex:none}
.vtag.pk{color:var(--ac);background:var(--ac-soft)}
.vtag.bad{color:var(--bad);background:color-mix(in srgb,var(--bad) 14%,transparent)}
.vtag.warn{color:var(--warn);background:color-mix(in srgb,var(--warn) 15%,transparent)}
.v-used{font-size:9.5px;color:var(--tx3);flex:none}
.v-chev{color:var(--tx3);flex:none;transition:transform var(--dur-2)}
.v-chev.rot{transform:rotate(180deg)}
.vdet{padding:4px 12px 12px;display:flex;flex-direction:column;gap:9px;border-top:1px solid var(--line)}
.vf{display:flex;align-items:center;gap:7px;padding-top:9px}
.vf span{font-size:11px;color:var(--tx3);width:74px;flex:none}
.vf input{flex:1;background:var(--c1);border:1px solid var(--line);border-radius:7px;padding:7px 10px;color:var(--tx);font-size:12.5px;outline:none;min-width:0}
.vf input:focus{border-color:var(--ac-line)}
.vf button{width:26px;height:26px;border-radius:7px;display:grid;place-items:center;color:var(--tx3);flex:none}
.vf button:hover{background:var(--c4);color:var(--tx2)}
.vwarn{display:flex;gap:9px;align-items:flex-start;background:color-mix(in srgb,var(--bad) 10%,transparent);border:1px solid color-mix(in srgb,var(--bad) 30%,transparent);border-radius:7px;padding:9px 11px;color:var(--bad)}
.vwarn div{display:flex;flex-direction:column;gap:2px}
.vwarn b{font-size:11.5px}
.vwarn span{font-size:10.5px;color:var(--tx3)}
.vdet-f{display:flex;align-items:center;gap:9px}
.v-totp{font-size:11px;color:var(--tx3);display:inline-flex;align-items:center;gap:6px}
.v-totp i{width:22px;height:3px;border-radius:2px;background:linear-gradient(90deg,var(--ac) 60%,var(--c4) 60%)}
.vdel{margin-left:auto;display:inline-flex;align-items:center;gap:5px;font-size:11px;color:var(--tx3);padding:4px 9px;border-radius:7px}
.vdel:hover{color:var(--bad);background:color-mix(in srgb,var(--bad) 12%,transparent)}
.vpop-lock{display:flex;flex-direction:column;align-items:center;gap:9px;padding:22px 16px;font-size:12px;color:var(--tx3)}
.vpop-none{padding:16px;text-align:center;font-size:11.5px;color:var(--tx3)}
.vpop-row{display:flex;align-items:center;gap:9px;padding:8px 10px;border-radius:7px}
.vpop-row:hover{background:var(--c2)}
.vpop-u{display:flex;flex-direction:column;gap:1px;flex:1;min-width:0;font-size:12px;color:var(--tx2)}
.vpop-u span{font-size:10px;color:var(--tx3)}
.vpop-fill{display:inline-flex;align-items:center;gap:5px;font-size:11px;color:var(--ac);border:1px solid var(--ac-line);border-radius:7px;padding:4px 9px;flex:none}
.vpop-fill:hover{background:var(--ac-soft)}
.agt-tabs{display:flex;gap:4px;padding:0 0 14px;flex-wrap:wrap}
.agt-tab{display:flex;align-items:center;gap:7px;height:32px;padding:0 13px;border:1px solid var(--line);border-radius:var(--r-sm);font-size:12.5px;color:var(--tx3);background:var(--c2)}
.agt-tab:hover{color:var(--tx2);border-color:var(--line2)}
.agt-tab.on{background:var(--ac-soft);border-color:var(--ac-line);color:var(--ac)}
.agt-body{padding-bottom:40px}
/* ---- agent activity log ---- */
.agl-fil{display:flex;gap:6px;margin-bottom:12px}
.agl-f{display:flex;align-items:center;gap:6px;height:28px;padding:0 11px;border:1px solid var(--line);border-radius:7px;font-size:11.5px;color:var(--tx3)}
.agl-f:hover{color:var(--tx2);border-color:var(--line2)}
.agl-f.on{background:var(--ac-soft);border-color:var(--ac-line);color:var(--ac)}
.agl-f b{font-size:9.5px;background:var(--c3);border-radius:4px;padding:1px 5px;color:var(--tx2)}
.agl-f.on b{background:var(--ac);color:#fff}
.agl-list{display:flex;flex-direction:column;gap:6px}
.agl-row{border:1px solid var(--line);border-radius:10px;background:var(--c2);overflow:hidden}
.agl-row.open{border-color:var(--line2)}
.agl-head{display:flex;align-items:center;gap:10px;width:100%;padding:11px 13px;text-align:left}
.agl-head:hover{background:var(--c1)}
.agl-dot{width:7px;height:7px;border-radius:50%;flex:none}
.agl-main{flex:1;min-width:0;display:flex;flex-direction:column;gap:2px}
.agl-main b{font-size:12.5px;font-weight:550;color:var(--tx)}
.agl-main .mono{font-size:10px;color:var(--tx3)}
.agl-st{font-size:10.5px;font-weight:550;flex:none}
.agl-t{font-size:10px;color:var(--tx3);flex:none;min-width:56px;text-align:right}
.agl-body{padding:0 13px 13px 30px;border-top:1px solid var(--line);padding-top:11px}
.agl-body p{font-size:12px;color:var(--tx2);line-height:1.6;margin:0 0 9px}
.agl-diff{display:flex;flex-direction:column;gap:5px;margin-bottom:10px}
.agl-d{display:flex;align-items:center;gap:8px;padding:7px 10px;background:var(--c1);border:1px solid var(--line);border-radius:7px}
.agl-dk{flex:1;font-size:11.5px;color:var(--tx2)}
.agl-da{font-size:10.5px;color:var(--tx3);text-decoration:line-through}
.agl-db{font-size:10.5px;color:var(--good)}
.agl-empty{padding:26px;text-align:center;font-size:12px;color:var(--tx3);border:1px dashed var(--line);border-radius:10px}
/* ---- agent capabilities ---- */
.acap-post{display:flex;gap:11px;align-items:flex-start;padding:13px 15px;background:var(--c2);border:1px solid var(--line);border-radius:10px;margin-bottom:14px}
.acap-post > div{display:flex;flex-direction:column;gap:3px}
.acap-post b{font-size:12.5px;font-weight:600;color:var(--tx)}
.acap-post span{font-size:11.5px;color:var(--tx3);line-height:1.5}
.acap-list{display:flex;flex-direction:column;gap:2px}
.acap-row{display:flex;align-items:center;gap:12px;padding:10px 13px;background:var(--c2);border:1px solid var(--line);border-radius:10px}
.acap-t{flex:1;min-width:0;display:flex;flex-direction:column;gap:2px}
.acap-t b{font-size:12.5px;font-weight:550;color:var(--tx)}
.acap-t span{font-size:11px;color:var(--tx3)}
.acap-seg{display:flex;gap:2px;padding:2px;background:var(--c1);border:1px solid var(--line);border-radius:7px;flex:none}
.acap-seg button{font-size:10.5px;padding:4px 10px;border-radius:7px;color:var(--tx3)}
.acap-seg button:hover{color:var(--tx2)}
.acap-seg button.on{background:var(--c3);color:var(--tx)}
.acap-seg button.on.allow{background:var(--good);color:#06210f}
.acap-seg button.on.never{background:var(--bad);color:#fff}
/* ---- watched pages ---- */
.wch-list{display:flex;flex-direction:column;gap:6px}
.wch{display:flex;align-items:center;gap:11px;padding:11px 13px;background:var(--c2);border:1px solid var(--line);border-radius:10px}
.wch.hit{border-color:var(--ac-line)}
.wch-t{flex:1;min-width:0;display:flex;flex-direction:column;gap:2px}
.wch-t b{font-size:12.5px;font-weight:550;display:flex;align-items:center;gap:7px}
.wch-badge{font-size:9px;background:var(--ac);color:#fff;border-radius:4px;padding:1px 6px;font-weight:600}
.wch-t .mono{font-size:10px;color:var(--tx3);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.wch-m{display:flex;flex-direction:column;gap:1px;text-align:right;font-size:10px;color:var(--tx2);flex:none}
.wch-m i{font-style:normal;color:var(--tx3);font-size:9.5px}
.wch-x{width:22px;height:22px;border-radius:7px;display:grid;place-items:center;color:var(--tx3);flex:none}
.wch-x:hover{background:var(--c4);color:var(--bad)}
/* ---- approval queue ---- */
.apqbadge{position:absolute;top:2px;right:1px;min-width:13px;height:13px;padding:0 3px;border-radius:7px;background:var(--warn);color:#1a1206;font-size:8.5px;font-weight:700;display:grid;place-items:center}
.apq-list{max-height:330px;overflow-y:auto;padding:6px}
.apq-it{padding:11px 12px;border:1px solid var(--line);border-radius:10px;background:var(--c1);margin-bottom:6px}
.apq-top{display:flex;align-items:center;gap:8px}
.apq-top b{flex:1;font-size:12.5px;font-weight:600;color:var(--tx)}
.apq-cap{font-size:9.5px;color:var(--warn);background:var(--c3);border-radius:4px;padding:2px 6px;flex:none}
.apq-meta{font-size:10px;color:var(--tx3);margin-top:2px}
.apq-d{font-size:11.5px;color:var(--tx2);line-height:1.55;margin:7px 0 8px}
.apq-diff{display:flex;align-items:center;gap:7px;font-size:10.5px;padding:6px 9px;background:var(--c2);border-radius:7px;margin-bottom:8px}
.apq-diff span{flex:1;color:var(--tx3)}
.apq-diff i{font-style:normal;color:var(--tx3);text-decoration:line-through}
.apq-diff b{color:var(--good)}
.apq-act{display:flex;gap:7px;justify-content:flex-end}
.apq-no,.apq-yes{display:flex;align-items:center;gap:5px;height:28px;padding:0 12px;border-radius:7px;font-size:11.5px;font-weight:550}
.apq-no{border:1px solid var(--line2);color:var(--tx2)}
.apq-no:hover{border-color:var(--bad);color:var(--bad)}
.apq-yes{background:var(--ac);color:#fff}
.apq-yes:hover{filter:brightness(1.08)}
.apq-empty{padding:24px 16px;text-align:center;font-size:11.5px;color:var(--tx3);line-height:1.6}
.apq-foot{padding:6px;border-top:1px solid var(--line)}
/* ---- find in page ---- */
.findbar{position:absolute;top:10px;right:14px;z-index:36;display:flex;align-items:center;gap:7px;height:34px;padding:0 8px 0 11px;background:var(--c2);border:1px solid var(--line2);border-radius:10px;box-shadow:var(--sh-2);animation:pop var(--dur-2) var(--ease-out) both}
.findbar input{width:190px;background:none;border:none;outline:none;color:var(--tx);font-size:12.5px}
.fb-n{font-size:10.5px;color:var(--tx3);min-width:34px;text-align:right}
.findbar button{width:24px;height:24px;border-radius:7px;display:grid;place-items:center;color:var(--tx3)}
.findbar button:hover{background:var(--c3);color:var(--tx2)}
mark.fx{background:color-mix(in srgb,var(--warn) 42%,transparent);color:inherit;border-radius:2px}
mark.fx.on{background:var(--ac);color:#fff}
/* ---- link hints ---- */
.hintlayer{position:absolute;inset:0;z-index:38;pointer-events:none}
.hint{position:absolute;transform:translate(-3px,-9px);background:var(--warn);color:#1a1206;font-size:10px;font-weight:700;border-radius:4px;padding:1px 4px;box-shadow:0 2px 6px rgba(0,0,0,.4);letter-spacing:.04em}
.hint b.done{opacity:.4}
/* ---- tab search ---- */
.tabsrch{width:min(620px,84vw);background:var(--c2);border:1px solid var(--line2);border-radius:var(--r-lg);box-shadow:var(--sh-3);overflow:hidden;animation:pop var(--dur-2) var(--ease-out) both}
.ts-in{display:flex;align-items:center;gap:10px;padding:13px 15px;border-bottom:1px solid var(--line)}
.ts-in input{flex:1;background:none;border:none;outline:none;color:var(--tx);font-size:14px}
.ts-c{font-size:10.5px;color:var(--tx3)}
.ts-list{max-height:330px;overflow-y:auto;padding:6px}
.ts-row{display:flex;align-items:center;gap:10px;width:100%;padding:8px 10px;border-radius:7px;text-align:left}
.ts-row.sel{background:var(--c3)}
.ts-t{flex:1;min-width:0;display:flex;flex-direction:column;gap:1px;font-size:12.5px;color:var(--tx2)}
.ts-t .mono{font-size:10px;color:var(--tx3);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.ts-sp{font-size:9.5px;color:var(--ac);background:var(--ac-soft);border:1px solid var(--ac-line);border-radius:4px;padding:2px 6px;flex:none}
.ts-empty{padding:26px;text-align:center;font-size:12px;color:var(--tx3)}
.ts-foot{padding:8px 14px;border-top:1px solid var(--line);font-size:10.5px;color:var(--tx3);background:var(--c1)}
.ts-foot b{font-size:9.5px;background:var(--c3);border-radius:4px;padding:1px 4px;color:var(--tx2)}
/* ---- side panel: reading list + notes ---- */
.sidep{position:absolute;top:0;right:0;bottom:0;width:296px;z-index:30;background:var(--c1);border-left:1px solid var(--line);display:flex;flex-direction:column;animation:slidein var(--dur-2) var(--ease-out) both}
@keyframes slidein{from{transform:translateX(14px);opacity:0}to{transform:none;opacity:1}}
.sidep-h{display:flex;align-items:center;gap:9px;padding:12px 13px;border-bottom:1px solid var(--line)}
.sidep-t{flex:1;min-width:0;display:flex;flex-direction:column;gap:1px;font-size:12.5px;font-weight:550;color:var(--tx)}
.sidep-t span{font-size:10px;color:var(--tx3);font-weight:400}
.sidep-h button{width:24px;height:24px;border-radius:7px;display:grid;place-items:center;color:var(--tx3)}
.sidep-h button:hover{background:var(--c3);color:var(--tx2)}
.sidep-s{display:flex;align-items:center;gap:7px;margin:10px 12px 6px;padding:0 9px;height:28px;background:var(--c2);border:1px solid var(--line);border-radius:7px}
.sidep-s input{flex:1;background:none;border:none;outline:none;color:var(--tx);font-size:11.5px}
.sidep-b{flex:1;overflow-y:auto;padding:4px 8px 12px}
.sidep-e{padding:24px 14px;text-align:center;font-size:11.5px;color:var(--tx3);line-height:1.6}
.sidep-f{padding:8px 13px;border-top:1px solid var(--line);font-size:10px;color:var(--tx3)}
.rdl-row{display:flex;align-items:flex-start;gap:7px;padding:7px 6px;border-radius:7px}
.rdl-row:hover{background:var(--c2)}
.rdl-row.read .rdl-t{color:var(--tx3);text-decoration:line-through}
.rdl-chk{width:19px;height:19px;border-radius:7px;display:grid;place-items:center;color:var(--tx3);flex:none;margin-top:1px}
.rdl-chk:hover{background:var(--c3);color:var(--ac)}
.rdl-main{flex:1;min-width:0;display:flex;flex-direction:column;gap:2px;text-align:left}
.rdl-t{font-size:12px;color:var(--tx2);line-height:1.35}
.rdl-m{font-size:9.5px;color:var(--tx3)}
.rdl-x{width:19px;height:19px;border-radius:7px;display:grid;place-items:center;color:var(--tx3);flex:none;opacity:0}
.rdl-row:hover .rdl-x{opacity:1}
.rdl-x:hover{background:var(--c4);color:var(--bad)}
.npad{flex:1;margin:10px 12px;background:var(--c2);border:1px solid var(--line);border-radius:10px;padding:11px 12px;color:var(--tx);font-size:12.5px;line-height:1.65;outline:none;resize:none;font-family:inherit}
.npad:focus{border-color:var(--ac-line)}
/* ---- task manager ---- */
.taskm{width:min(600px,86vw);background:var(--c2);border:1px solid var(--line2);border-radius:var(--r-lg);box-shadow:var(--sh-3);overflow:hidden;animation:pop var(--dur-2) var(--ease-out) both}
.tk-h,.cap-h,.fo-h{display:flex;align-items:center;gap:9px;padding:13px 15px;border-bottom:1px solid var(--line);font-size:13px;font-weight:600}
.tk-h > div,.cap-h > div,.fo-h > div{flex:1;display:flex;flex-direction:column;gap:1px}
.tk-h span,.cap-h span,.fo-h span{font-size:10px;color:var(--tx3);font-weight:400}
.tk-h button,.cap-h button,.fo-h button{width:24px;height:24px;border-radius:7px;display:grid;place-items:center;color:var(--tx3)}
.tk-h button:hover,.cap-h button:hover,.fo-h button:hover{background:var(--c3);color:var(--tx2)}
.tk-dup{display:flex;align-items:center;gap:8px;margin:10px 12px 0;padding:8px 11px;background:var(--ac-soft);border:1px solid var(--ac-line);border-radius:7px;font-size:11.5px;color:var(--tx2)}
.tk-dup span{flex:1}
.tk-dup button{font-size:11px;color:var(--ac);border:1px solid var(--ac-line);border-radius:7px;padding:3px 10px}
.tk-dup button:hover{background:var(--ac-soft)}
.tk-rows{max-height:320px;overflow-y:auto;padding:8px}
.tk-r{display:flex;align-items:center;gap:9px;padding:7px 9px;border-radius:7px}
.tk-r:hover{background:var(--c1)}
.tk-r.zzz{opacity:.55}
.tk-t{flex:1;min-width:0;font-size:12px;color:var(--tx2);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.tk-bar{width:76px;height:4px;border-radius:2px;background:var(--c4);overflow:hidden;flex:none}
.tk-bar i{display:block;height:100%;background:var(--ac);border-radius:2px}
.tk-v{font-size:10.5px;color:var(--tx2);min-width:52px;text-align:right;flex:none}
.tk-v.dim{color:var(--tx3);min-width:38px}
.tk-a{width:22px;height:22px;border-radius:7px;display:grid;place-items:center;color:var(--tx3);flex:none}
.tk-a:hover{background:var(--c4);color:var(--tx)}
.tk-f{padding:9px 15px;border-top:1px solid var(--line);font-size:10.5px;color:var(--tx3);background:var(--c1)}
/* ---- capture ---- */
.capt,.focus{width:min(460px,88vw);background:var(--c2);border:1px solid var(--line2);border-radius:var(--r-lg);box-shadow:var(--sh-3);overflow:hidden;animation:pop var(--dur-2) var(--ease-out) both}
.cap-modes{display:flex;gap:7px;padding:13px 14px 10px}
.cap-m{flex:1;display:flex;flex-direction:column;gap:3px;align-items:flex-start;text-align:left;padding:9px 10px;border:1px solid var(--line);border-radius:10px;background:var(--c1)}
.cap-m b{font-size:11.5px;color:var(--tx2)}
.cap-m span{font-size:9.5px;color:var(--tx3);line-height:1.4}
.cap-m.on{border-color:var(--ac-line);background:var(--ac-soft)}
.cap-m.on b{color:var(--ac)}
.cap-prev{padding:0 14px 12px}
.cap-frame{height:104px;border:1px dashed var(--line2);border-radius:10px;display:grid;place-items:center;background:var(--c1);color:var(--tx3);font-size:10.5px}
.cap-act{display:flex;gap:7px;justify-content:flex-end;padding:11px 14px;border-top:1px solid var(--line);background:var(--c1)}
/* ---- focus ---- */
.fo-time{font-size:44px;font-weight:600;text-align:center;padding:20px 0 4px;letter-spacing:-.03em}
.fo-goal{text-align:center;font-size:12.5px;color:var(--tx2);padding-bottom:14px}
.fo-ring{height:4px;margin:0 16px;border-radius:2px;background:var(--c4);overflow:hidden}
.fo-ring i{display:block;height:100%;background:var(--ac);transition:width 1s linear}
.fo-blocked{text-align:center;font-size:10.5px;color:var(--tx3);padding:12px 0 4px}
.fo-in{width:calc(100% - 28px);margin:14px;background:var(--c1);border:1px solid var(--line);border-radius:7px;padding:9px 11px;color:var(--tx);font-size:12.5px;outline:none}
.fo-in:focus{border-color:var(--ac-line)}
.fo-mins{display:flex;gap:7px;padding:0 14px 12px}
.fo-mins button{flex:1;height:30px;border:1px solid var(--line);border-radius:7px;font-size:11.5px;color:var(--tx3);font-family:var(--mono)}
.fo-mins button.on{border-color:var(--ac-line);background:var(--ac-soft);color:var(--ac)}
.fo-list{padding:0 14px 6px}
.fo-lt{font-size:10px;color:var(--tx3);margin-bottom:6px}
.fo-chip{display:inline-block;font-size:10px;color:var(--tx3);background:var(--c1);border:1px solid var(--line);border-radius:7px;padding:3px 7px;margin:0 5px 5px 0}
/* ---- site controls ---- */
.sc-zoom{display:flex;align-items:center;gap:8px;padding:11px 15px;border-bottom:1px solid var(--line);font-size:12px;color:var(--tx2)}
.sc-zoom > span{flex:1}
.sc-zoom button{width:24px;height:24px;border-radius:7px;background:var(--c3);color:var(--tx2);display:grid;place-items:center;font-size:14px}
.sc-zoom button:hover{background:var(--c4)}
.sc-zoom b{min-width:40px;text-align:center;font-size:11.5px}
.sc-reset{width:auto!important;padding:0 9px;font-size:10.5px!important}
.sc-list{padding:8px 10px}
.sc-row{display:flex;align-items:center;gap:8px;padding:6px 5px;font-size:12px;color:var(--tx2)}
.sc-row > span{flex:1}
.sc-seg{display:flex;gap:2px;padding:2px;background:var(--c1);border:1px solid var(--line);border-radius:7px}
.sc-seg button{font-size:10px;padding:3px 7px;border-radius:7px;color:var(--tx3)}
.sc-seg button.on{background:var(--c3);color:var(--tx)}
/* ---- workspace export + schedules ---- */
.wsjson{background:var(--c1);border:1px solid var(--line);border-radius:10px;padding:13px 15px;font-size:11px;line-height:1.6;color:var(--tx2);max-height:300px;overflow:auto;white-space:pre-wrap;word-break:break-word}
.ws-act{display:flex;align-items:center;gap:8px;justify-content:flex-end;margin-top:10px}
.ws-act .mono{margin-right:auto;font-size:10.5px;color:var(--tx3)}
.wsdrop{display:flex;flex-direction:column;align-items:center;gap:5px;text-align:center;padding:26px 20px;border:1px dashed var(--line2);border-radius:10px;background:var(--c2);width:100%}
.wsdrop:hover{border-color:var(--ac-line);background:var(--ac-soft)}
.wsdrop b{font-size:12.5px;color:var(--tx2)}
.wsdrop span{font-size:11px;color:var(--tx3);max-width:380px;line-height:1.5}
.wsdrop.small{flex-direction:row;padding:12px;gap:8px;margin-top:9px}
.schl{display:flex;flex-direction:column;gap:8px}
.sch{background:var(--c2);border:1px solid var(--line);border-radius:10px;padding:12px 14px}
.sch.off{opacity:.6}
.sch-top{display:flex;align-items:center;gap:9px}
.sch-top b{font-size:12.5px;font-weight:600}
.sch-when{flex:1;font-size:10.5px;color:var(--ac)}
.sch-task{font-size:11.5px;color:var(--tx3);margin:5px 0 8px;line-height:1.5}
.sch-foot{display:flex;align-items:center;gap:6px;font-size:10px;color:var(--tx3)}
.sch-foot button{margin-left:auto;font-size:10.5px;color:var(--tx2);border:1px solid var(--line);border-radius:7px;padding:3px 9px;font-family:var(--sans)}
.sch-foot button:hover{border-color:var(--ac-line);color:var(--ac)}
/* ---- highlight to ask ---- */
.wp-real{font-size:14.5px;line-height:1.75;color:var(--tx2);margin:0 0 22px;user-select:text;cursor:text;margin-bottom:26px}
.wp.light .wp-real{color:#3c3c44}
.askpill{position:absolute;z-index:62;transform:translateX(-50%);display:flex;align-items:center;gap:6px;background:var(--c2);border:1px solid var(--ac-line);border-radius:var(--r);padding:5px 11px;font-size:11.5px;color:var(--ac);box-shadow:0 14px 36px -10px color-mix(in srgb,var(--tx) 31%,transparent);animation:pop var(--dur-2) both}
.askpill:hover{background:var(--ac-soft)}
.dock{height:340px;flex:none;background:var(--c1);border-top:1px solid var(--line2);display:flex;flex-direction:column;animation:rise var(--dur-3) var(--ease-out) both;transition:height var(--dur-3) var(--ease-out)}
.dock.tall{height:500px}
.dock-h{display:flex;align-items:center;gap:1px;padding:5px 10px;border-bottom:1px solid var(--line);flex:none}
.dtab{display:flex;align-items:center;gap:6px;height:26px;padding:0 10px;border-radius:var(--r);font-size:11.5px;color:var(--tx3);font-family:var(--sans)}
.dtab:hover{background:var(--c2);color:var(--tx2)}
.dtab.on{background:var(--c3);color:var(--tx)}
.dt-split{flex:1;display:flex;min-height:0}
.dt-3col{flex:1;display:flex;min-height:0}
.dt-main{flex:1.6;min-width:0;display:flex;flex-direction:column;overflow-y:auto}
.dt-side{flex:1;max-width:290px;border-left:1px solid var(--line);padding:10px 14px;overflow-y:auto;font-size:11.5px}
.dt-col{flex:1;display:flex;flex-direction:column;min-height:0}
.dt-cap{font-size:10px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--tx3);padding:6px 0}
.dt-dim{color:var(--tx3);font-size:11px}
.dt-sel{margin-left:auto;background:var(--c2);border:1px solid var(--line);border-radius:var(--r);color:var(--tx2);font-size:11px;padding:3px 7px;outline:none}
.kvrow{display:flex;justify-content:space-between;padding:4px 0;color:var(--tx3);font-size:11.5px;border-bottom:1px solid var(--line)}
.kvrow b{color:var(--tx2);font-weight:500;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:60%}
/* elements */
.el-tree{padding:8px 4px;font-family:var(--mono);font-size:11.5px;line-height:1.9}
.el-row{white-space:nowrap;border-radius:var(--r-sm);padding-right:8px;cursor:default}
.el-row:hover{background:var(--c2)}
.el-row.on{background:var(--ac-soft)}
.el-t{color:var(--ac)}
.el-b{color:var(--tx3)}
.el-a{color:#c792ea}
.el-v{color:#7ee2a8}
.el-x{color:var(--tx2)}
.st-blk{font-family:var(--mono);font-size:11px;border:1px solid var(--line);border-radius:var(--r);padding:9px 11px;margin-bottom:8px;position:relative}
.st-sel{color:#c792ea}
.st-p{padding:2px 0 2px 14px;color:var(--tx2);display:flex;gap:6px;align-items:center}
.st-p b{color:#7ee2a8;font-weight:400}
.st-p input{accent-color:var(--ac);width:11px;height:11px}
.st-src{position:absolute;top:9px;right:11px;color:var(--tx3);font-size:10px}
.bm{border:1px dashed var(--line2);border-radius:var(--r-sm);padding:14px;position:relative;text-align:center;font-family:var(--mono);font-size:10px;color:var(--tx3)}
.bm .bm-l{position:absolute;top:2px;left:50%;transform:translateX(-50%)}
.bm.m{background:rgba(255,184,107,.05)}
.bm.b{background:rgba(122,167,255,.06);margin-top:8px}
.bm.p{background:rgba(126,226,168,.05);margin-top:8px}
.bm.c{background:var(--c3);margin-top:8px;padding:10px;color:var(--tx);border-radius:var(--r-sm);border:none}
/* console */
.con-bar{display:flex;gap:5px;align-items:center;padding:7px 12px;border-bottom:1px solid var(--line);flex:none}
.chip{height:22px;padding:0 10px;border-radius:var(--r);background:var(--c2);border:1px solid var(--line);color:var(--tx3);font-size:11px;font-weight:500;transition:all var(--dur-2);display:flex;align-items:center}
.chip:hover{color:var(--tx);background:var(--c2)}
.chip.on{background:var(--c3);border-color:var(--ac-line);color:var(--tx)}
.con-list{flex:1;overflow-y:auto;padding:4px 0;font-family:var(--mono);font-size:11.5px}
.con-row{display:flex;justify-content:space-between;gap:14px;padding:4px 14px;border-bottom:1px solid var(--line)}
.con-row.warn .con-m{color:#ffb86b}
.con-row.error .con-m{color:#ff6b6b}
.con-row.info .con-m{color:var(--tx2)}
.con-row.log .con-m{color:var(--tx2)}
.con-row.echo .con-m{color:var(--tx3)}
.con-row.result .con-m{color:var(--ac)}
.con-s{color:var(--tx3);font-size:10.5px;flex:none}
.con-in{display:flex;gap:9px;align-items:center;padding:8px 14px;border-top:1px solid var(--line);flex:none}
.con-in input{flex:1;background:none;border:none;outline:none;color:var(--tx);font-size:12px;font-family:var(--mono)}
/* network */
.net-hd{display:grid;grid-template-columns:1.4fr 60px 70px 60px 1.4fr;gap:8px;padding:6px 14px;font-size:10px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--tx3);border-bottom:1px solid var(--line)}
.net-list{flex:1;overflow-y:auto}
.net-row{display:grid;grid-template-columns:1.4fr 60px 70px 60px 1.4fr;gap:8px;padding:5px 14px;font-size:11px;border-bottom:1px solid var(--line);align-items:center;cursor:default}
.net-row:hover{background:var(--c2)}
.net-row.on{background:var(--ac-soft)}
.net-row.blk .n{color:#ff6b6b;text-decoration:line-through}
.net-row .n{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:var(--tx2)}
.net-row .s.bad{color:#ff6b6b}
.net-row .s.dim,.net-row .z,.net-row .t{color:var(--tx3)}
.wf{position:relative;height:8px;background:var(--c2);border-radius:4px;overflow:hidden}
.wf i{position:absolute;top:1px;bottom:1px;border-radius:4px}
.net-sum{padding:7px 14px;border-top:1px solid var(--line);flex:none}
.tmrow{display:flex;align-items:center;gap:8px;padding:3px 0;color:var(--tx3);font-size:11px}
.tmrow i{height:6px;border-radius:4px;background:var(--ac);opacity:.7}
.tmrow b{margin-left:auto;color:var(--tx2);font-weight:400}
/* sources */
.src-tree{width:150px;flex:none;border-right:1px solid var(--line);padding:8px 10px;overflow-y:auto}
.src-f{padding:3px 7px;border-radius:var(--r-sm);font-size:11px;color:var(--tx3);white-space:pre;cursor:default}
.src-f:hover{background:var(--c2)}
.src-f.on{background:var(--c3);color:var(--tx)}
.src-code{flex:1.7;min-width:0;overflow:auto;font-size:11.5px;line-height:1.8;padding:8px 0}
.src-ln{display:flex;gap:12px;padding:0 12px;white-space:pre}
.src-ln.cur{background:var(--ac-soft)}
.src-n{width:30px;flex:none;text-align:right;color:var(--tx3);position:relative}
.bp{position:absolute;left:-2px;top:5px;width:8px;height:8px;border-radius:50%;background:#ff6b6b;display:block}
.src-t{color:var(--tx2)}
.src-paused{margin-left:auto;font-size:10px;color:var(--ac);border:1px solid var(--ac-line);border-radius:var(--r-sm);padding:0 6px;align-self:center}
.stk{padding:3px 7px;border-radius:var(--r-sm);font-size:10.5px;color:var(--tx3)}
.stk.on{background:var(--ac-soft);color:var(--tx)}
/* performance */
.fps{display:flex;align-items:flex-end;gap:2px;height:44px}
.fps i{flex:1;background:var(--good);opacity:.55;border-radius:2px 2px 0 0}
.flame{display:flex;flex-direction:column;gap:3px}
.fl-row{position:relative;height:20px}
.fl-row i{position:absolute;top:0;bottom:0;border-radius:4px;font-size:9px;font-family:var(--mono);color:rgba(0,0,20,.75);padding:3px 6px;overflow:hidden;white-space:nowrap}
.perf-leg{display:flex;gap:16px;font-size:11px;color:var(--tx3)}
.perf-leg i{display:inline-block;width:8px;height:8px;border-radius:2px;margin-right:5px}
.perf-leg b{color:var(--tx2);font-weight:500}
.vitrow{display:flex;gap:8px}
.vit{display:flex;align-items:center;gap:7px;border:1px solid var(--line);border-radius:var(--r);padding:6px 10px;font-size:11px}
.vit .k{color:var(--tx3)}
.vit .v{color:var(--tx)}
/* storage */
.st-row{display:grid;grid-template-columns:1fr 1.6fr;gap:8px;padding:6px 14px;font-size:11px;border-bottom:1px solid var(--line);color:var(--tx2)}
/* lighthouse */
.lh-rings{display:flex;gap:26px;padding:6px 0 12px}
.lh{display:flex;flex-direction:column;align-items:center;gap:6px;font-size:11px;color:var(--tx2)}
.lh-row{display:flex;align-items:center;gap:9px;padding:6px 0;font-size:12px;color:var(--tx2);border-bottom:1px solid var(--line)}
.sec-big{display:flex;align-items:center;gap:9px;font-size:13px;padding-bottom:10px}



.scveil{position:fixed;inset:0;z-index:85;background:color-mix(in srgb,var(--tx) 32%,transparent);backdrop-filter:blur(6px);display:grid;place-items:center;padding:24px;animation:fade var(--dur-2) both}
.sc{width:min(720px,94vw);max-height:82vh;overflow-y:auto;background:var(--c2);border:1px solid var(--line2);border-radius:var(--r-lg);box-shadow:0 40px 100px -20px color-mix(in srgb,var(--tx) 45%,transparent);animation:pop var(--dur-3) var(--ease-out) both}
.sc-h{display:flex;align-items:center;gap:11px;padding:19px 24px;border-bottom:1px solid var(--line)}
.sc-h .t{font-size:16px;font-weight:600}
.sc-grid{display:grid;grid-template-columns:1fr 1fr;gap:2px 44px;padding:16px 24px 24px}
.sc-grp{margin-top:14px}
.sc-grp .g{font-size:10px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--tx3);margin-bottom:6px}
.scrow{display:flex;align-items:center;justify-content:space-between;gap:16px;height:33px;font-size:13px;color:var(--tx2)}
.keys{display:flex;gap:4px;flex:none}
.keys span{font-family:var(--mono);font-size:11px;color:var(--tx);background:var(--c1);border:1px solid var(--line2);border-radius:var(--r-sm);min-width:22px;height:22px;padding:0 6px;display:grid;place-items:center}

/* Asteria 05: reduced motion keeps causality — it drops vestibular movement, not the cross-fade that explains what changed */
@media (prefers-reduced-motion:reduce){
.nova.nova *{animation-duration:.01ms!important;animation-iteration-count:1!important;scroll-behavior:auto!important;transition-property:opacity,background-color,border-color,color,box-shadow!important;transition-duration:80ms!important}
.nova [class*="pop"],.nova .ovl>*,.nova .taskm,.nova .capt,.nova .focus,.nova .tabsrch,.nova .findbar,.nova .sidep{animation:none!important;transform:none!important}
}

`;

/* ---------- mock data ---------- */
const FAV = (bg, fg) => ({ background: bg, color: fg || "#fff" });
const site = (letter) => ({ letter, style: { background: "rgba(255,255,255,.06)", color: "#c6c6cd" } });

const TABS0 = [
  { id: 1, title: "Turing — New Tab", url: "nova://newtab", secure: true, heat: 1 },
  { id: 2, title: "Linear – The issue tracker built for speed", url: "linear.app/nova/team", secure: true, heat: 0, group: "sg1" },
  { id: 3, title: "Vercel — v0.app", url: "v0.app/chat", secure: true, heat: 0, group: "sg1" },
  { id: 5, title: "GitHub · nova-project", url: "github.com/nova/shell", secure: true, heat: 1, group: "sg1" },
  { id: 4, title: "Mercury – Banking for startups", url: "mercury.com/dashboard", secure: true, heat: 2, group: "sg2" },
  { id: 7, title: "Stripe – Invoices", url: "stripe.com/invoices", secure: true, heat: 0, group: "sg2" },
  { id: 6, title: "lofi beats to dispatch to — YouTube", url: "youtube.com/watch?v=jfKfPfyJRdk", secure: true, heat: 0, audio: "muted" },
  { id: 8, title: "intranet.wades.local", url: "intranet.wades.local", secure: false, heat: 0, status: "error" },
];
const GROUPS0 = {
  sg1: { name: "Build", color: "#2e8dff", collapsed: false },
  sg2: { name: "Money", color: "#7ee2a8", collapsed: true },
};

const QUICKS = [
  site("▲", "#000", "#fff"), site("L", "#5e6ad2"), site("M", "#5b3df5"),
  site("G", "#24292f"), site("F", "#0055ff"), site("N", "#000"),
  site("S", "#635bff"), site("R", "#ff4f00"), site("W", "#202122"),
  site("D", "#5865f2"), site("Y", "#ff0000"), site("+", "#1b1b1e", "#616166"),
].map((s, i) => ({ ...s, name: ["Vercel", "Linear", "Mercury", "GitHub", "Figma", "Notion", "Stripe", "Raycast", "Wikipedia", "Discord", "YouTube", "Add shortcut"][i] }));
QUICKS[8].u = "en.wikipedia.org/wiki/Web_browser";

const BOOKMARKS = [
  site("L", "#5e6ad2"), site("▲", "#000", "#fff"), site("M", "#5b3df5"),
  site("G", "#24292f"), site("F", "#0055ff"), site("S", "#635bff"), site("N", "#000"),
].map((s, i) => ({ ...s, name: ["Linear", "Vercel", "Mercury", "GitHub", "Figma", "Stripe", "Notion"][i] }));

const EXTENSIONS = [
  { icon: ShieldCheck, nm: "Turing Shield", by: "Nova Labs", desc: "Blocks ads, trackers, and fingerprinting across every site. Built in — always on.", on: true, perms: "All sites", built: true },
  { icon: Key, nm: "Vault Password Manager", by: "vault.io", desc: "Autofill logins and generate strong passwords, secured with end-to-end encryption.", on: true, perms: "All sites" },
  { icon: Palette, nm: "ColorPeek", by: "Studio Eleven", desc: "Eyedropper and palette extractor for any page. Grab hex, HSL, and Tailwind tokens.", on: true, perms: "On click" },
  { icon: Eye, nm: "Reader Mode+", by: "Quiet Software", desc: "Strips clutter for a clean, typographic reading view with adjustable width.", on: false, perms: "On click" },
  { icon: Bookmark, nm: "Raindrop", by: "Raindrop.io", desc: "Save pages, articles, and links to collections that sync across your devices.", on: true, perms: "All sites" },
  { icon: Blocks, nm: "React DevTools", by: "Meta", desc: "Inspect component trees, props, and hooks for React apps you build.", on: true, perms: "localhost" },
  { icon: Type, nm: "Comprehensive Writing Suite — Grammar, Style & Tone for Email, Docs, and Long-Form Publishing (Professional Edition)", by: "quietwrite.software", desc: "Real-time grammar, clarity, and tone suggestions across every site you write on. Understands context, matches your voice, and keeps everything on device — even store descriptions this long clamp cleanly after three lines.", on: false, perms: "All sites · Clipboard · Downloads · Notifications" },
];
EXTENSIONS.forEach((e, i) => { e.ver = ["4.2.1", "1.18.0", "0.9.3", "2.0.0", "6.4.12", "5.3.1", "1.0.0-beta.7"][i]; e.sz = ["2.1", "8.4", "0.6", "1.2", "5.7", "3.3", "48.9"][i] + " MB"; });

const COOKIES = [
  { name: "linear.app", count: 8, size: "142 KB", type: "First-party", secure: true },
  { name: "v0.app", count: 12, size: "310 KB", type: "First-party", secure: true },
  { name: "vercel.com", count: 6, size: "88 KB", type: "First-party", secure: true },
  { name: "google-analytics.com", count: 4, size: "12 KB", type: "Third-party", secure: false },
  { name: "doubleclick.net", count: 9, size: "24 KB", type: "Third-party", secure: false },
  { name: "mercury.com", count: 5, size: "64 KB", type: "First-party", secure: true },
  { name: "github.com", count: 11, size: "201 KB", type: "First-party", secure: true },
  { name: "stripe.com", count: 7, size: "96 KB", type: "First-party", secure: true },
];

const HSITES = [
  { t: "Linear — The issue tracker built for speed", u: "linear.app/nova/team/active", f: site("L", "#5e6ad2") },
  { t: "v0.app — Generative UI", u: "v0.app/chat/browser-concept", f: site("▲", "#000", "#fff") },
  { t: "Mercury Dashboard", u: "mercury.com/dashboard", f: site("M", "#5b3df5") },
  { t: "GitHub · nova/shell — Pull Requests", u: "github.com/nova/shell/pulls", f: site("G", "#24292f") },
  { t: "Figma — Nova Design System", u: "figma.com/file/nova-ds", f: site("F", "#0055ff") },
  { t: "Ramp — Spend management", u: "ramp.com/expenses", f: site("R", "#e5ff44", "#000") },
  { t: "Framer Motion — Documentation", u: "motion.dev/docs/react-animation", f: site("◈", "#0099ff") },
  { t: "Stripe Docs — Payment Intents", u: "stripe.com/docs/payments", f: site("S", "#635bff") },
  { t: "Tailwind CSS v4 — Upgrade guide", u: "tailwindcss.com/docs/v4", f: site("T", "#38bdf8", "#000") },
  { t: "MDN — content-visibility", u: "developer.mozilla.org/CSS/content-visibility", f: site("M", "#000", "#fff") },
  { t: "Supabase — Row Level Security", u: "supabase.com/docs/auth/rls", f: site("S", "#3ecf8e", "#000") },
  { t: "Hacker News", u: "news.ycombinator.com", f: site("Y", "#ff6600") },
];
const DAYS = ["Today", "Today", "Today", "Yesterday", "Yesterday", "Mon, Jul 13", "Sun, Jul 12", "Sat, Jul 11"];
const HISTORY = Array.from({ length: 400 }, (_, i) => {
  const s = HSITES[i % HSITES.length];
  const day = DAYS[Math.min(DAYS.length - 1, Math.floor(i / 52))];
  const h = 23 - (i % 14); const m = (i * 7) % 60;
  const hh = ((h + 11) % 12) + 1; const ap = h < 12 ? "AM" : "PM";
  const stress = i % 40 === 27;
  const stress2 = i % 40 === 39;
  const t = stress ? "RFC 9110 — HTTP Semantics: a very long specification title that keeps going to prove truncation never breaks the row layout even at absurd lengths — Section 8.4.1 Content-Negotiation Weighting and Quality Values in Multi-Range Byte-Serving Responses" : stress2 ? "日本語のタイトル · emoji stress 🚀🔧🧪 · مرحبا · very-long-unbroken-token-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" : s.t;
  const u = stress ? "www.rfc-editor.org/rfc/rfc9110.html#name-content-negotiation-weighting-and-quality-values-extremely-long-anchor" : s.u;
  return { id: i, t, u, f: s.f, day, tm: `${hh}:${String(m).padStart(2, "0")} ${ap}` };
});

/* ---------- tiny virtual-list hook ---------- */
function useVirtual(ref, rowH, count, over = 6) {
  const [top, setTop] = useState(0);
  const [h, setH] = useState(520);
  useEffect(() => {
    const el = ref.current; if (!el) return;
    setH(el.clientHeight);
    const on = () => setTop(el.scrollTop);
    el.addEventListener("scroll", on, { passive: true });
    return () => el.removeEventListener("scroll", on);
  }, [ref]);
  const start = Math.max(0, Math.floor(top / rowH) - over);
  const end = Math.min(count, Math.ceil((top + h) / rowH) + over);
  return { start, end, pad: count * rowH };
}

/* ---------- primitives ---------- */
const Toggle = memo(function Toggle({ on, onClick }) {
  return <div className={"sw" + (on ? " on" : "")} role="switch" aria-checked={on} onClick={onClick} />;
});

const Row = memo(function Row({ icon, title, desc, children }) {
  return (
    <div className="row">
      {icon && <div className="ico">{icon}</div>}
      <div className="meta"><div className="t">{title}</div>{desc && <div className="d">{desc}</div>}</div>
      {children}
    </div>
  );
});

const FavImg = memo(function FavImg({ d, size = 12 }) {
  const [err, setErr] = useState(false);
  if (err || !d || !d.includes(".")) return <i className="tdot" style={{ background: "var(--c4)" }} />;
  if (!REMOTE_FAVICONS) return <i className="tdot" style={{ background: "var(--c4)" }} />;
  return <img className="tfav" width={size} height={size} loading="lazy" decoding="async"
    src={"https://www.google.com/s2/favicons?domain=" + d + "&sz=32"} alt="" onError={() => setErr(true)} />;
});

function Fav({ f, size }) {
  const s = size || 15;
  const ff = f || {};
  return <div className="fav" style={{ ...(ff.style || { background: "var(--c4)" }), width: s, height: s }}>{ff.letter || ""}</div>;
}

function UrlText({ url }) {
  const i = url.indexOf("/");
  const dom = i === -1 ? url : url.slice(0, i);
  const path = i === -1 ? "" : url.slice(i);
  return <span className="ttl mono" style={{ overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{dom}<span style={{ color: "var(--tx2)" }}>{path}</span></span>;
}

const VTabs = memo(function VTabs({ tabs, active, onSelect, onClose, onAdd, right, groups = {}, onToggleGroup, onCtx, onDropRow }) {
  const dragRow = (t) => (e) => {
    if (!onDropRow) return;
    const rowEl = e.currentTarget;
    let proxy = null;
    const host = rowEl.closest(".vtabs");
    startPointerDrag(e, {
      onStart: () => {
        const r = rowEl.getBoundingClientRect();
        proxy = rowEl.cloneNode(true);
        proxy.className = "vtab vdragproxy";
        proxy.style.width = r.width + "px";
        rowEl.closest(".nova").appendChild(proxy);
        rowEl.classList.add("ghost");
      },
      onMove: (ev) => {
        const nr = rowEl.closest(".nova").getBoundingClientRect(); const s = nr.width / DESIGN_W;
        proxy.style.left = (ev.clientX - nr.left) / s - 20 + "px";
        proxy.style.top = (ev.clientY - nr.top) / s - 13 + "px";
        document.querySelectorAll(".vsec.vdrop, .vtab.vbefore").forEach((x) => x.classList.remove("vdrop", "vbefore"));
        const el = document.elementFromPoint(ev.clientX, ev.clientY);
        const sec = el && el.closest && el.closest(".vsec");
        if (sec && sec.closest(".vtabs") === host) { sec.classList.add("vdrop"); return; }
        const row = el && el.closest && el.closest(".vtab");
        if (row && row !== rowEl && !row.classList.contains("vdragproxy") && row.closest(".vtabs") === host) row.classList.add("vbefore");
      },
      onEnd: (ev, started) => {
        rowEl.classList.remove("ghost");
        if (proxy) proxy.remove();
        const marked = { sec: document.querySelector(".vsec.vdrop"), row: document.querySelector(".vtab.vbefore") };
        document.querySelectorAll(".vsec.vdrop, .vtab.vbefore").forEach((x) => x.classList.remove("vdrop", "vbefore"));
        if (!started) return;
        rowEl.dataset.dragged = "1"; setTimeout(() => { delete rowEl.dataset.dragged; }, 0);
        if (marked.row) onDropRow(t.id, { before: +marked.row.dataset.id });
        else if (marked.sec) onDropRow(t.id, { join: marked.sec.dataset.gid });
        else onDropRow(t.id, { loose: true });
      },
    });
  };
  // Dia-style zones: new tab · pinned · group sections · divider · loose tabs
  const pinned = tabs.filter((t) => t.pin);
  const order = [];
  const seen = new Set();
  tabs.forEach((t) => { if (t.group && groups[t.group] && !seen.has(t.group)) { seen.add(t.group); order.push(t.group); } });
  const loose = tabs.filter((t) => !t.pin && !(t.group && groups[t.group]));

  const Row = (t) => (
    <div key={t.id} className={"vtab" + (t.id === active ? " on" : "") + (t.status === "error" ? " err" : "")} data-id={t.id} title={t.title}
      onClick={(e) => { if (e.currentTarget.dataset.dragged) return; onSelect(t); }}
      onPointerDown={dragRow(t)}
      onContextMenu={onCtx ? (e) => onCtx(e, t) : undefined}>
      <span className="tst">
        {t.status === "loading" ? <i className="tspin" />
        : t.status === "error" ? <i className="terr" />
        : t.pin ? <Pin size={10} color="var(--tx3)" />
        : t.audio === "muted" ? <VolumeX size={11} color="var(--tx3)" />
        : t.audio ? <Volume2 size={11} color="var(--ac)" />
        : <FavImg d={t.url.split("/")[0]} size={14} />}
      </span>
      <span className="ttl">{t.label || t.title}</span>
      <button className="xc" onClick={(e) => onClose(t.id, e)} aria-label="Close tab"><X size={12} /></button>
    </div>
  );

  return (
    <div className={"vtabs" + (right ? " right" : "")}>
      <button className="vnew-top" onClick={onAdd}><Plus size={13} /> New Tab <span className="kbd" style={{ marginLeft: "auto" }}>⌘T</span></button>
      {pinned.length > 0 && (<>
        <div className="vzone">{pinned.map(Row)}</div>
        <div className="vsep" />
      </>)}
      {order.map((gid) => {
        const g = groups[gid];
        const members = tabs.filter((t) => t.group === gid);
        return (
          <div key={gid} className="vsec" data-gid={gid}>
            <button className="vsec-h" onClick={() => onToggleGroup && onToggleGroup(gid)}>
              <ChevronDown size={11} style={{ transform: g.collapsed ? "rotate(-90deg)" : "none", transition: "transform var(--dur-3)", flex: "none" }} />
              <i className="gdot" style={{ background: g.color }} />
              <span className="vsec-n">{g.name}</span>
              <span className="vsec-c mono">{members.length}</span>
            </button>
            <div className={"vsec-w" + (g.collapsed ? " closed" : "")}><div className="vsec-b">{members.map(Row)}</div></div>
          </div>
        );
      })}
      {order.length > 0 && loose.length > 0 && <div className="vsep" />}
      <div className="vzone">{loose.map(Row)}</div>
    </div>
  );
});

/* ---------- history row (memoized, absolutely positioned) ---------- */
const HRow = memo(function HRow({ item, y, onDel, dayTag, selected, onSel }) {
  return (
    <div className={"hrow" + (selected ? " selected" : "")} data-url={item.u} style={{ transform: `translateY(${y}px)` }}>
      <span className="hday mono">{dayTag || ""}</span>
      <button className={"sel" + (selected ? " on" : "")} onClick={() => onSel(item.id)} aria-label="Select">{selected && <Check size={10} />}</button>
      <Fav f={item.f} size={22} />
      <span className="t">{item.t}</span>
      <span className="u"><i className="vchip">{item.u}</i></span>
      <span className="tm">{item.tm}</span>
      <button className="del" onClick={() => onDel(item.id)} aria-label="Remove"><X size={14} /></button>
    </div>
  );
});

/* ============================================================================ */
export default function Nova() {
  const [tabs, setTabs] = useState(TABS0);
  const [active, setActive] = useState(2);
  const [view, setView] = useState("newtab"); // newtab|settings|history|extensions|downloads
  const [setSec, setSetSec] = useState("privacy");
  const [heroFocus, setHeroFocus] = useState(false);
  const [pop, setPop] = useState(null); // menu|security|shield|ext|downloads|vault
  const [shieldSites, setShieldSites] = useState({});   // domain -> standard | strict | off
  const [vault, setVault] = useState(VAULT0);
  const [vaultLocked, setVaultLocked] = useState(true);
  const [findOpen, setFindOpen] = useState(false);
  const [hints, setHints] = useState(false);
  const [tabSearch, setTabSearch] = useState(false);
  const [reading, setReading] = useState(READ0);
  const [notesBySpace, setNotesBySpace] = useState({});
  const [side, setSide] = useState(null);          // reading | notes
  const [taskm, setTaskm] = useState(false);
  const [sitePerms, setSitePerms] = useState({});
  const [capture, setCapture] = useState(false);
  const [focusOpen, setFocusOpen] = useState(false);
  const [foMins, setFoMins] = useState(25);
  const [foRun, setFoRun] = useState(false);
  const [foLeft, setFoLeft] = useState(25 * 60);
  const [foGoal, setFoGoal] = useState("");
  const [sched, setSched] = useState(SCHED0);
  const [agentLog, setAgentLog] = useState(AGENTLOG0);
  const [agentCaps, setAgentCaps] = useState({});
  const [watches, setWatches] = useState(WATCH0);
  const [conns, setConns] = useState(CONNS0);
  const [approvals, setApprovals] = useState(APPROVE0);
  const [agentSec, setAgentSec] = useState("activity");
  const [cmd, setCmd] = useState(false);
  const [cmdQ, setCmdQ] = useState("");
  const [cmdSel, setCmdSel] = useState(0);
  const [dock, setDock] = useState(false);
  const [dockTab, setDockTab] = useState("elements");
  const [shortcuts, setShortcuts] = useState(false);
  const [bkbar, setBkbar] = useState(false);
  const [tabPos, setTabPos] = useState("top");
  const [zen, setZen] = useState(false);
  const [peek, setPeek] = useState(false);
  const [loading, setLoading] = useState(false);
  const loadRef = useRef(null);
  const [flags, setFlags] = useState({
    adblock: true, https: true, dnt: true, block3p: true, fingerprint: true,
    safeBrowse: true, memSaver: true, energy: false, preload: true, hwaccel: true,
    prefetch: true, quic: true, autofill: true, passwords: true, sync: true, sugg: true,
    devmode: false, fade: true, autozen: true,
  });
  const toggle = useCallback((k) => setFlags((f) => ({ ...f, [k]: !f[k] })), []);

  const sweep = useCallback((clr = "ac") => {
    setSweepClr(clr);
    setLoading(false);
    cancelAnimationFrame(loadRef.current);
    loadRef.current = requestAnimationFrame(() => {
      setLoading(true);
      clearTimeout(loadRef.timeout);
      loadRef.timeout = setTimeout(() => setLoading(false), 900);
    });
  }, []);

  // real back/forward: a history stack of full (tab, view, url, title) snapshots
  const tabsRef = useRef(TABS0);
  const [hist, setHist] = useState({ stack: [{ t: 2, v: "newtab", url: TABS0[1].url, title: TABS0[1].title }], i: 0 });
  const record = useCallback((t, v, url, title) => {
    setHist((h) => {
      const stack = h.stack.slice(0, h.i + 1);
      const last = stack[stack.length - 1];
      if (last && last.t === t && last.v === v && last.url === url) return h;
      stack.push({ t, v, url, title });
      return { stack, i: stack.length - 1 };
    });
  }, []);
  const canBack = hist.i > 0, canFwd = hist.i < hist.stack.length - 1;
  const goHist = useCallback((dir) => {
    setHist((h) => {
      const i = Math.min(Math.max(h.i + dir, 0), h.stack.length - 1);
      if (i === h.i) return h;
      const e = h.stack[i];
      setActive(e.t); setView(e.v);
      if (e.url) setTabs((ts) => ts.map((x) => (x.id === e.t ? { ...x, url: e.url, title: e.title } : x)));
      return { ...h, i };
    });
    sweep();
  }, [sweep]);

  // zen onboarding hint
  const [zenHint, setZenHint] = useState(false);
  useEffect(() => {
    if (zen) { setZenHint(true); const t = setTimeout(() => setZenHint(false), 2800); return () => clearTimeout(t); }
    setZenHint(false);
  }, [zen]);

  // cool-factor state
  const [modHeld, setModHeld] = useState(false);        // ⌘ held → tab number hints
  const [glance, setGlance] = useState(null);           // hold a chip → peek that page
  const glanceT = useRef(null); const heldRef = useRef(false);
  const [renameId, setRenameId] = useState(null);       // double-click chip → name it
  const [sweepClr, setSweepClr] = useState("ac");       // semantic loading sweep
  const [autoHide, setAutoHide] = useState(false);      // auto-zen on scroll
  const zenTimerRef = useRef(null);
  useEffect(() => { if (!zen) clearTimeout(zenTimerRef.current); }, [zen]);
  const hideBar = zen || autoHide;

  // Design-canvas viewing: the browser always renders at its true 1440×900
  // desktop viewport; zoom chooses how you view it (Fit or fixed %, pan by scroll).
  const canvasRef = useRef(null);
  const [zoom, setZoom] = useState("fit");
  const [present, setPresent] = useState(false);
  const [fitScale, setFitScale] = useState(0.5);
  useEffect(() => {
    const measure = () => {
      const el = canvasRef.current;
      const w = (el && el.clientWidth) || window.innerWidth || 1440;
      const h = (el && el.clientHeight) || window.innerHeight || 900;
      const s = Math.min((w - 56) / DESIGN_W, (h - 56) / DESIGN_H);
      if (s > 0 && isFinite(s)) setFitScale(Math.min(1, s));
    };
    measure();
    const raf = requestAnimationFrame(measure);
    let ro;
    if (typeof ResizeObserver !== "undefined" && canvasRef.current) {
      ro = new ResizeObserver(measure);
      ro.observe(canvasRef.current);
    }
    window.addEventListener("resize", measure);
    window.addEventListener("orientationchange", measure);
    return () => {
      cancelAnimationFrame(raf);
      if (ro) ro.disconnect();
      window.removeEventListener("resize", measure);
      window.removeEventListener("orientationchange", measure);
    };
  }, []);
  const eff = zoom === "fit" ? fitScale : zoom;

  const tab = tabs.find((t) => t.id === active) || tabs[0];
  tabsRef.current = tabs;
  const isNT = tab.url === "nova://newtab" && view === "newtab";

  // keyboard — developer shortcuts only fire in Developer mode
  const devRef = useRef(false);
  devRef.current = flags.devmode;
  const zenRef = useRef(false);
  zenRef.current = zen;
  const cmdRef = useRef(false);
  cmdRef.current = cmd;
  const selectRef = useRef(null);
  useEffect(() => {
    const on = (e) => {
      const k = e.key.toLowerCase();
      const mod = e.metaKey || e.ctrlKey;
      const typing = /^(input|textarea)$/i.test(e.target.tagName || "");
      if (e.key === "Meta" || e.key === "Control") { setModHeld(true); return; }
      if (e.ctrlKey && !e.metaKey && /^[1-9]$/.test(e.key)) {
        e.preventDefault();
        const s = spaceRef.current.spaces[+e.key - 1];
        if (s) spaceRef.current.switchSpace(s.id);
        return;
      }
      if (e.ctrlKey && e.key === "Tab") {
        e.preventDefault();
        const ts = tabsRef.current;
        const i = ts.findIndex((t) => t.id === activeRef.current);
        const n = ts[(i + (e.shiftKey ? -1 : 1) + ts.length) % ts.length];
        if (n && selectRef.current) selectRef.current(n);
        return;
      }
      if (mod && e.shiftKey && !e.altKey && e.code === "KeyS") { e.preventDefault(); sideRef.current && sideRef.current(); return; }
      if (mod && e.shiftKey && e.code === "KeyA") { e.preventDefault(); setTabSearch(true); return; }
      if (mod && e.shiftKey && (e.code === "BracketRight" || e.code === "BracketLeft")) {
        e.preventDefault();
        const ts = tabsRef.current;
        const i = ts.findIndex((t) => t.id === activeRef.current);
        const n = ts[(i + (e.code === "BracketRight" ? 1 : -1) + ts.length) % ts.length];
        if (n && selectRef.current) selectRef.current(n);
        return;
      }
      if (mod && !e.altKey && (k === "k" || k === "l")) {
        if (cmdRef.current && k === "k") return; // palette handles ⌘K as its Actions toggle
        e.preventDefault(); setCmd((v) => !v); setCmdQ(""); setCmdSel(0);
      }
      else if (mod && k === "t") { e.preventDefault(); (e.shiftKey ? reopenRef.current : addRef.current)(); }
      else if (mod && k === "w") { e.preventDefault(); closeRef.current(activeRef.current); }
      else if (mod && /^[1-9]$/.test(e.key)) {
        e.preventDefault();
        const t = tabsRef.current[+e.key - 1];
        if (t && selectRef.current) selectRef.current(t);
      }
      else if (mod && e.key === "Enter") { e.preventDefault(); setZen((v) => !v); setPeek(false); }
      else if (devRef.current && mod && e.altKey && e.code === "KeyI") { e.preventDefault(); setDock((v) => !v); setDockTab("elements"); }
      else if (devRef.current && mod && e.altKey && e.code === "KeyN") { e.preventDefault(); setDock(true); setDockTab("network"); }
      else if (devRef.current && mod && e.altKey && e.code === "KeyJ") { e.preventDefault(); setDock(true); setDockTab("console"); }
      else if (devRef.current && mod && e.altKey && e.code === "KeyS") { e.preventDefault(); setDock(true); setDockTab("sources"); }
      else if (mod && e.key === ".") { e.preventDefault(); setPresent((v) => !v); return; }
      else if (mod && e.code === "Slash") { e.preventDefault(); setShortcuts((v) => !v); }
      else if (mod && e.shiftKey && e.code === "KeyB") { e.preventDefault(); setBkbar((v) => !v); }
      else if (mod && e.key === ",") { e.preventDefault(); goRef.current("settings"); }
      else if (mod && k === "e") { e.preventDefault(); aiRef.current(); }
      else if (mod && !e.shiftKey && k === "d") { e.preventDefault(); markRef.current(); }
      else if (mod && e.shiftKey && e.code === "KeyC") { e.preventDefault(); copyRef.current(); }
      else if (mod && e.shiftKey && e.code === "KeyR") { e.preventDefault(); readerRef.current(); }
      else if (mod && e.shiftKey && e.code === "KeyD") {
        e.preventDefault();
        const t = tabsRef.current.find((x) => x.id === activeRef.current);
        if (t && t.url !== "nova://newtab") {
          setReading((v) => v.some((r) => r.url === t.url) ? v
            : [{ id: Date.now(), title: t.label || t.title || t.url, url: t.url, mins: 3 + (hashStr(t.url) % 12), read: false }, ...v]);
          note("Saved to reading list", [{ label: "Open list", fn: () => setSide("reading") }]);
        }
      }
      else if (mod && e.shiftKey && e.code === "KeyN") { e.preventDefault(); setSide((v) => (v === "notes" ? null : "notes")); }
      else if (mod && e.altKey && e.code === "KeyR") { e.preventDefault(); setSide((v) => (v === "reading" ? null : "reading")); }
      else if (mod && e.shiftKey && e.code === "KeyM") { e.preventDefault(); setTaskm(true); }
      else if (mod && e.shiftKey && e.code === "Digit4") { e.preventDefault(); setCapture(true); }
      else if (mod && e.altKey && e.code === "KeyF") { e.preventDefault(); setFocusOpen(true); }
      else if (mod && e.code === "KeyF" && !e.shiftKey && !e.altKey) { e.preventDefault(); setFindOpen(true); }
      else if (mod && e.altKey && e.code === "KeyL") { e.preventDefault(); setHints(true); }
      else if (mod && e.altKey && e.code === "KeyA") { e.preventDefault(); setTabSearch(true); }
      else if (mod && e.shiftKey && e.code === "Backslash") { e.preventDefault(); swapRef.current(); }
      else if (mod && e.altKey && e.code === "ArrowLeft") { e.preventDefault(); nudgeRef.current(-0.04); }
      else if (mod && e.altKey && e.code === "ArrowRight") { e.preventDefault(); nudgeRef.current(0.04); }
      else if (mod && e.code === "Backslash") { e.preventDefault(); splitRef.current(); }
      else if (mod && (e.key === "=" || e.key === "+")) { e.preventDefault(); zoomRef.current(0.1); }
      else if (mod && e.key === "-") { e.preventDefault(); zoomRef.current(-0.1); }
      else if (mod && e.key === "0") { e.preventDefault(); zoomRef.current(0); }
      else if (e.code === "Slash" && e.shiftKey && !typing) { e.preventDefault(); setShortcuts((v) => !v); }
      else if (k === "escape") {
        if (zenRef.current) setZen(false);
        setCmd(false); setPop(null); setShortcuts(false); setPeek(false); setGlance(null); setRenameId(null); setCtx(null); setPageCtx(null); setFindOpen(false); setHints(false); setTabSearch(false); setTaskm(false); setCapture(false); setFocusOpen(false); setSide(null); setSplitId(null); setConfirmClose(false); setSelPill(null); setAi(false); setLittle(null); setInspector(false); setShare(false);
      }
      // just start typing — any printable key summons the command bar, pre-filled
      else if (!mod && !e.altKey && !typing && !cmdRef.current && e.key.length === 1 && e.key !== " ") {
        e.preventDefault();
        setCmd(true); setCmdQ(e.key); setCmdSel(0);
      }
    };
    const up = (e) => { if (e.key === "Meta" || e.key === "Control") setModHeld(false); };
    const blur = () => setModHeld(false);
    window.addEventListener("keydown", on);
    window.addEventListener("keyup", up);
    window.addEventListener("blur", blur);
    return () => { window.removeEventListener("keydown", on); window.removeEventListener("keyup", up); window.removeEventListener("blur", blur); };
  }, []);

  useEffect(() => {
    if (!foRun) { setFoLeft(foMins * 60); return; }
    const t = setInterval(() => setFoLeft((v) => {
      if (v <= 1) { setFoRun(false); return foMins * 60; }
      return v - 1;
    }), 1000);
    return () => clearInterval(t);
  }, [foRun, foMins]);

  // keep the active chip scrolled into view
  useEffect(() => {
    const raf = requestAnimationFrame(() => {
      document.querySelector(".ttab.on")?.scrollIntoView({ inline: "nearest", block: "nearest" });
    });
    return () => cancelAnimationFrame(raf);
  }, [active, tabs.length]);

  // leaving Developer mode closes the inspector
  useEffect(() => { if (!flags.devmode) setDock(false); }, [flags.devmode]);

  const go = useCallback((v, sec) => {
    setView(v);
    if (sec) { if (v === "agents") setAgentSec(sec); else setSetSec(sec); }
    setPop(null); setCmd(false);
    const t = tabsRef.current.find((x) => x.id === active) || tabsRef.current[0];
    record(active, v, t.url, t.title);
  }, [record, active]);

  // lightweight feedback toasts
  const [notice, setNotice] = useState(null);
  const noteT = useRef(null);
  const note = useCallback((m, actions) => { setNotice({ msg: m, actions }); clearTimeout(noteT.current); noteT.current = setTimeout(() => setNotice(null), actions ? 5000 : 2200); }, []);

  const runSchedule = useCallback((x) => {
    setAgentLog((v) => [{ id: Date.now(), t: "just now", agent: x.name, verb: "Dry ran",
      target: x.task.toLowerCase(), site: "turing://agent", status: "dryrun", diff: [],
      detail: "Ran without touching anything so you can see what it would do. Approve it to let it act." }, ...v]);
    setApprovals((v) => v.some((a) => a.agent === x.name) ? v
      : [{ id: Date.now() + 1, agent: x.name, verb: "Apply", target: "the result of " + x.name.toLowerCase(),
          site: "turing://agent", cap: "post", detail: x.task + " — the dry run finished cleanly.",
          diff: [["Pending changes", "0", "1"]] }, ...v]);
    note("Dry run finished · " + x.name, [{ label: "Review", fn: () => setPop("approve") }]);
  }, [note]);


  const activeRef = useRef(active);
  activeRef.current = active;
  const popRef = useRef(null);
  popRef.current = pop;
  const closedRef = useRef([]);
  const scrollMem = useRef({});   // per-tab scroll position
  const [ctx, setCtx] = useState(null);   // chip context menu {id,x,y}
  const [pageCtx, setPageCtx] = useState(null); // page-area context menu {x,y}
  const [peekUrl, setPeekUrl] = useState(null);
  const [sideOpen, setSideOpen] = useState(true);
  const sideRef = useRef(null);
  const noteRef2 = useRef(null);
  noteRef2.current = note;
  sideRef.current = () => setSideOpen((v) => { note(v ? "Sidebar hidden" : "Sidebar shown"); return !v; });
  // drag an entire collapsed group by its folder chip
  const startGroupDrag = (gid) => (e) => {
    e.stopPropagation();
    const chipEl = e.currentTarget;
    let proxy = null, anchorId = null, atEnd = false;
    const nova = chipEl.closest(".nova");
    const ok = startPointerDrag(e, {
      onStart: () => {
        const r = chipEl.getBoundingClientRect();
        proxy = chipEl.cloneNode(true);
        proxy.className = "ttab fold dragproxy";
        proxy.style.width = r.width + "px";
        nova.appendChild(proxy);
        chipEl.classList.add("ghost");
      },
      onMove: (ev) => {
        const nr = nova.getBoundingClientRect(); const s = nr.width / DESIGN_W;
        proxy.style.left = (ev.clientX - nr.left) / s - 60 + "px";
        proxy.style.top = (ev.clientY - nr.top) / s - 12 + "px";
        anchorId = null; atEnd = true;
        const units = [...document.querySelectorAll(".ttabs .ttab")].filter((c) => c !== chipEl && !c.classList.contains("dragproxy"));
        for (const c of units) {
          const cr = c.getBoundingClientRect();
          if (ev.clientX < cr.left + cr.width / 2) {
            anchorId = c.dataset.id ? +c.dataset.id : ("g:" + c.dataset.gid);
            atEnd = false;
            if (cueRef.current) { const sr = document.querySelector(".ttabs").getBoundingClientRect(); cueRef.current.style.opacity = "1"; cueRef.current.style.transform = `translateX(${(cr.left - sr.left) / s - 2}px)`; cueRef.current.style.background = groupsRef.current[gid]?.color || "var(--ac)"; }
            break;
          }
        }
        if (atEnd && cueRef.current) cueRef.current.style.opacity = "0";
      },
      onEnd: (ev, started) => {
        chipEl.classList.remove("ghost");
        if (proxy) proxy.remove();
        if (cueRef.current) cueRef.current.style.opacity = "0";
        if (!started) return;
        chipEl.dataset.dragged = "1";
        setTimeout(() => { delete chipEl.dataset.dragged; }, 0);
        setTabs((ts) => {
          const block = ts.filter((x) => x.group === gid);
          if (!block.length) return ts;
          let arr = ts.filter((x) => x.group !== gid);
          let at = arr.length;
          if (!atEnd && anchorId != null) {
            if (typeof anchorId === "number") { const i = arr.findIndex((x) => x.id === anchorId); if (i > -1) at = i; }
            else { const g2 = String(anchorId).slice(2); const i = arr.findIndex((x) => x.group === g2); if (i > -1) at = i; }
          }
          const pinnedCount = arr.filter((x) => x.pin).length;
          if (at < pinnedCount) at = pinnedCount;
          arr.splice(at, 0, ...block);
          return arr;
        });
        noteRef2.current && noteRef2.current("Moved “" + (groupsRef.current[gid]?.name || "group") + "”");
      },
    });
    if (ok) e.preventDefault();
  };

  const dropRow = (id, act) => {
    setTabs((ts) => {
      const me = ts.find((x) => x.id === id); if (!me) return ts;
      let arr = ts.filter((x) => x.id !== id);
      if (act.join) {
        const gid = act.join;
        const last = arr.map((x) => x.group).lastIndexOf(gid);
        arr.splice(last + 1, 0, { ...me, group: gid });
        noteRef2.current && noteRef2.current("Filed into “" + (groupsRef.current[gid]?.name || "group") + "”");
      } else if (act.before != null) {
        const i = arr.findIndex((x) => x.id === act.before);
        const tg = i > -1 ? arr[i].group : undefined;
        arr.splice(i < 0 ? arr.length : i, 0, { ...me, group: tg });
      } else {
        arr.push({ ...me, group: undefined });
      }
      return arr;
    });
  };
  // a11y: any visible .pop containing .mitem becomes a keyboard menu
  useEffect(() => {
    const menuOpen = ctx || pageCtx || pop;
    if (!menuOpen) return;
    const t = setTimeout(() => {
      const m = [...document.querySelectorAll(".pop")].pop();
      if (!m) return;
      const items = [...m.querySelectorAll(".mitem")];
      if (!items.length) return;
      m.setAttribute("role", "menu");
      items.forEach((it) => it.setAttribute("role", "menuitem"));
      if (!m.hasAttribute("data-nofocus")) items[0].focus();
    }, 40);
    const key = (e) => {
      const m = [...document.querySelectorAll(".pop")].pop();
      if (!m) return;
      const items = [...m.querySelectorAll(".mitem")];
      if (!items.length) return;
      const i = items.indexOf(document.activeElement);
      if (e.key === "ArrowDown") { e.preventDefault(); e.stopPropagation(); items[(i + 1) % items.length].focus(); }
      else if (e.key === "ArrowUp") { e.preventDefault(); e.stopPropagation(); items[(i - 1 + items.length) % items.length].focus(); }
      else if (e.key === "Home") { e.preventDefault(); items[0].focus(); }
      else if (e.key === "End") { e.preventDefault(); items[items.length - 1].focus(); }
      else if (e.key === "Enter" && i > -1) { e.preventDefault(); e.stopPropagation(); items[i].click(); }
    };
    window.addEventListener("keydown", key, true);
    return () => { clearTimeout(t); window.removeEventListener("keydown", key, true); };
  }, [ctx, pageCtx, pop]);

  const openTabCtx = (e, t) => {
    e.preventDefault(); e.stopPropagation();
    const nr = e.currentTarget.closest(".nova").getBoundingClientRect();
    const s = nr.width / DESIGN_W;
    setCtx({ id: t.id, x: (e.clientX - nr.left) / s, y: (e.clientY - nr.top) / s });
  };
  const [splitId, setSplitId] = useState(null);  // secondary pane tab id
  const [splitRatio, setSplitRatio] = useState(0.5);  // left pane width fraction
  const splitIdRef = useRef(null); splitIdRef.current = splitId;
  const splitRatioRef = useRef(0.5); splitRatioRef.current = splitRatio;
  const [agentOn, setAgentOn] = useState({ ids: [], wait: false });  // tabs an agent is touching right now
  const [layouts, setLayouts] = useState({});  // {spaceId: [{name,left,right,ratio,ld,rd}]}
  const layoutsRef = useRef({}); layoutsRef.current = layouts;
  useEffect(() => { if (splitId != null && (splitId === active || !tabs.some((t) => t.id === splitId))) setSplitId(null); }, [tabs, active, splitId]);
  const [readerIds, setReaderIds] = useState({});// per-tab reader mode
  const [zoomMap, setZoomMap] = useState({});    // per-domain zoom
  const dirtyRef = useRef({});                   // per-tab unsaved typing
  const [confirmClose, setConfirmClose] = useState(false);
  const [lastSession, setLastSession] = useState(null); // for recovery banner
  const [textScale, setTextScale] = useState(1);
  const [theme, setTheme] = useState("light");
  const [themeId, setThemeId] = useState("turing-light");
  const [customVars, setCustomVars] = useState({});
  const [fontSans, setFontSans] = useState(FONTS_SANS[0][1]);
  const [fontMono, setFontMono] = useState(FONTS_MONO[0][1]);
  const [density, setDensity] = useState("cozy");
  const [radius, setRadius] = useState("soft");
  const applyPreset = useCallback((id) => {
    const t = THEMES.find((x) => x.id === id); if (!t) return;
    setThemeId(id); setTheme(t.mode); setCustomVars({});
    note("Theme · " + t.name);
  }, [note]);
  const themeVars = useMemo(() => {
    const t = THEMES.find((x) => x.id === themeId) || THEMES[0];
    const rad = radius === "sharp" ? { "--r": "4px", "--r-sm": "3px", "--r-lg": "6px" } : radius === "round" ? { "--r": "14px", "--r-sm": "10px", "--r-lg": "20px" } : {};
    return { ...t.vars, ...rad, "--sans": fontSans, "--mono": fontMono, ...customVars };
  }, [themeId, customVars, fontSans, fontMono, radius]);
  const toggleTheme = useCallback(() => {
    setTheme((t) => { const n = t === "dark" ? "light" : "dark"; note(n === "light" ? "Light theme" : "Dark theme"); return n; });
    setCmd(false);
  }, [note]);
  const [marks, setMarks] = useState(BOOKMARKS);
  const [groups, setGroups] = useState(GROUPS0);      // id → {name,color,collapsed}

  // reading list
  const saveForLater = useCallback((tabId) => {
    const t = tabsRef.current.find((x) => x.id === (tabId || activeRef.current));
    if (!t || t.url === "nova://newtab") { note("Nothing to save here"); return; }
    setReading((v) => v.some((r) => r.url === t.url) ? v
      : [{ id: Date.now(), title: t.label || t.title || t.url, url: t.url, mins: 3 + (hashStr(t.url) % 12), read: false }, ...v]);
    note("Saved to reading list", [{ label: "Open list", fn: () => setSide("reading") }]);
    setCtx(null); setCmd(false);
  }, [note]);
  const [ai, setAi] = useState(false);                 // Ask Turing panel
  const [aiMsgs, setAiMsgs] = useState([]);
  const [aiThreads, setAiThreads] = useState([]);      // saved Ask Turing conversations
  const [selPill, setSelPill] = useState(null);        // highlight-to-ask {x,y,text}
  const [boosts, setBoosts] = useState({});              // domain → true
  const boostSite = useCallback(() => {
    const t = tabsRef.current.find((x) => x.id === activeRef.current);
    if (!t || t.url === "nova://newtab") { note("Open a site to boost it"); return; }
    const d = t.url.split("/")[0];
    setBoosts((b) => { const on = !b[d]; note(on ? "Boost on — " + d + " wears your accent" : "Boost off"); return { ...b, [d]: on }; });
    setCmd(false);
  }, [note]);
  const GCOLORS = ["#2e8dff", "#c792ea", "#7ee2a8", "#ffb86b", "#f472b6"];

  // ---- Spaces (Arc): each space owns its tabs, groups, and tint ----
  const [spaces, setSpaces] = useState([
    { id: "work", name: "Work", tint: "#2e8dff" },
    { id: "personal", name: "Personal", tint: "#f472b6" },
  ]);
  const [spaceId, setSpaceId] = useState("work");
  const spaceStore = useRef({
    personal: {
      tabs: [
        { id: 71, title: "Turing — New Tab", url: "nova://newtab", secure: true, heat: 0 },
        { id: 72, title: "lofi beats to relax to — YouTube", url: "youtube.com/watch?v=jfKfPfyJRdk", secure: true, heat: 0, audio: "muted", group: "wg1" },
        { id: 73, title: "Trail maps — North Georgia", url: "alltrails.com/georgia", secure: true, heat: 1, group: "wg1" },
      ], active: 72, groups: { wg1: { name: "Weekend", color: "#f472b6", collapsed: false } },
    },
  });
  const switchSpace = useCallback((id) => {
    if (id === spaceId) return;
    spaceStore.current[spaceId] = { tabs: tabsRef.current, active: activeRef.current, groups, split: splitIdRef.current, ratio: splitRatioRef.current };
    const s = spaceStore.current[id] || { tabs: [{ id: Date.now(), title: "Turing — New Tab", url: "nova://newtab", secure: true, heat: 0 }], active: null, groups: {} };
    setTabs(s.tabs); setActive(s.active || s.tabs[0].id); setGroups(s.groups || {});
    setSpaceId(id); setView("newtab"); setSplitId(s.split ?? null); setSplitRatio(s.ratio ?? 0.5); setPop(null); sweep();
    note("Space · " + (spaces.find((x) => x.id === id)?.name || id));
  }, [spaceId, groups, spaces, note, sweep]);
  const addSpace = useCallback(() => {
    const tints = ["#7ee2a8", "#ffb86b", "#c792ea", "#22d3ee"];
    const id = "s" + Date.now();
    setSpaces((sp) => [...sp, { id, name: "Space " + (sp.length + 1), tint: tints[sp.length % tints.length] }]);
    switchSpace(id); setPop(null);
  }, [switchSpace]);
  const spaceRef = useRef(null); spaceRef.current = { spaces, switchSpace };
  const tint = spaces.find((s) => s.id === spaceId)?.tint || "#2e8dff";
  const space = spaces.find((s) => s.id === spaceId) || spaces[0];
  const rgba = (hex, a) => { const n = parseInt(hex.slice(1), 16); return `rgba(${(n >> 16) & 255},${(n >> 8) & 255},${n & 255},${a})`; };
  const [landings, setLandings] = useState({});   // spaceId → {mode,url}
  const landing = landings[spaceId] || { mode: "search", url: "" };
  const setLanding = useCallback((fn) => setLandings((ls) => ({ ...ls, [spaceId]: typeof fn === "function" ? fn(ls[spaceId] || { mode: "search", url: "" }) : fn })), [spaceId]);


  // ---- Profiles (Chrome): cosmetic separation, honest copy ----
  const [profile, setProfile] = useState("Byron");

  // ---- Translate (Chrome): per-tab mock state ----
  const [translated, setTranslated] = useState({});
  const translatePage = useCallback(() => {
    const id = activeRef.current;
    setTranslated((m) => { const on = !m[id]; note(on ? "Translated to English" : "Showing original"); return { ...m, [id]: on }; });
    setCmd(false); setPop(null);
  }, [note]);

  // ---- Per-site permissions (Chrome) ----
  const [perms, setPerms] = useState({});
  const setPerm = useCallback((dom, kind, v) => setPerms((p) => ({ ...p, [dom]: { ...(p[dom] || {}), [kind]: v } })), []);
  const [little, setLittle] = useState(null);
  const [inspector, setInspector] = useState(false);
  const [share, setShare] = useState(false);

  const groupTab = useCallback((tabId) => {
    const t = tabsRef.current.find((x) => x.id === tabId);
    if (!t) return;
    const gid = "g" + Date.now();
    const name = t.url.split(".")[0].split("/")[0].replace("www", "") || "Group";
    setGroups((g) => ({ ...g, [gid]: { name: name[0].toUpperCase() + name.slice(1), color: GCOLORS[Object.keys(g).length % GCOLORS.length], collapsed: false } }));
    setTabs((ts) => ts.map((x) => (x.id === tabId ? { ...x, group: gid } : x)));
    setCtx(null); note("Grouped — right-click others to add");
  }, [note]);

  const organizeTabs = useCallback(() => {
    const prev = { tabs: tabsRef.current, groups };
    const RULES = [
      ["Build", "#2e8dff", /(linear|github|v0|vercel|localhost)/],
      ["Money", "#7ee2a8", /(mercury|stripe|quickbooks)/],
      ["Media", "#ffb86b", /(youtube|spotify|vimeo)/],
    ];
    const g = {}; let made = 0;
    const ids = {};
    RULES.forEach(([name, color, re], i) => { ids[i] = "org" + i; });
    const nt = tabsRef.current.map((t) => {
      const ri = RULES.findIndex(([, , re]) => re.test(t.url));
      if (ri === -1) return { ...t, group: undefined };
      if (!g[ids[ri]]) { g[ids[ri]] = { name: RULES[ri][0], color: RULES[ri][1], collapsed: false }; made++; }
      return { ...t, group: ids[ri] };
    });
    // groups need ≥2 members to be worth it
    Object.keys(g).forEach((gid) => { if (nt.filter((t) => t.group === gid).length < 2) { delete g[gid]; nt.forEach((t) => { if (t.group === gid) t.group = undefined; }); made--; } });
    // pinned-first + group-adjacent ordering
    const order = [...nt.filter((t) => t.pin), ...Object.keys(g).flatMap((gid) => nt.filter((t) => !t.pin && t.group === gid)), ...nt.filter((t) => !t.pin && !t.group)];
    setTabs(order); setGroups(g); setCmd(false);
    note(made > 0 ? `Organized into ${made} group${made === 1 ? "" : "s"}` : "Nothing to organize yet",
      made > 0 ? [{ label: "Undo", fn: () => { setTabs(prev.tabs); setGroups(prev.groups); setNotice(null); } }] : undefined);
  }, [groups, note]);

  const askTuring = useCallback((seedText) => {
    setAi(true); setCmd(false); setSelPill(null);
    if (seedText) {
      setAiMsgs((m) => [...m,
        { role: "user", txt: `“${seedText.slice(0, 90)}” — what does this mean?`, ctx: [] },
        { role: "nova", txt: "That line is arguing that chrome should recede while you read — the same thesis Nova is built on. In context, the author is saying the browser earns trust by disappearing, not by adding surface.", ctx: [] },
      ]);
    }
  }, []);
  const toggleBookmark = useCallback(() => {
    const t = tabsRef.current.find((x) => x.id === activeRef.current);
    if (!t || t.url === "nova://newtab") { note("Nothing to bookmark here"); return; }
    setMarks((ms) => {
      if (ms.some((m) => m.u === t.url)) { note("Bookmark removed"); return ms.filter((m) => m.u !== t.url); }
      note("Bookmarked — ⌘⇧B shows the bar");
      const s = site((t.label || t.title)[0].toUpperCase());
      return [...ms, { ...s, name: (t.label || t.title).split(/[–—·|]/)[0].trim().slice(0, 18), u: t.url }];
    });
  }, [note]);
  const pinOrder = (ts) => [...ts.filter((t) => t.pin), ...ts.filter((t) => !t.pin)];
  const togglePin = (id) => setTabs((ts) => pinOrder(ts.map((t) => (t.id === id ? { ...t, pin: !t.pin } : t))));

  // ---- tab drag engine: pointer-based, FLIP-animated, group-aware, space-droppable ----
  const [dragId, setDragId] = useState(null);
  const stripRef = useRef(null);
  const [visBudget, setVisBudget] = useState(99);
  const [kinG, setKinG] = useState(null);
  const groupsRef = useRef(groups); groupsRef.current = groups;
  useEffect(() => {
    const el = stripRef.current; if (!el) return;
    const calc = () => setVisBudget(Math.max(3, Math.floor((el.clientWidth - 84) / 56)));
    calc();
    const ro = new ResizeObserver(calc); ro.observe(el);
    return () => ro.disconnect();
  }, [tabPos]);
  // visible set: cost-aware walk (collapsed group ≈ one small segment), active always visible
  const { visTabs, hidTabs } = useMemo(() => {
    let cost = 0; const vis = [];
    let i = 0;
    while (i < tabs.length) {
      const t = tabs[i];
      const g = t.group && groups[t.group];
      if (g && g.collapsed) {
        const run = [];
        while (i < tabs.length && tabs[i].group === t.group) { run.push(tabs[i]); i++; }
        if (cost + 1 <= visBudget) { vis.push(...run); cost += 1; }
        continue;
      }
      if (cost + 1 <= visBudget) { vis.push(t); cost += 1; }
      i++;
    }
    if (vis.length === tabs.length) return { visTabs: tabs, hidTabs: [] };
    if (!vis.some((t) => t.id === active)) {
      const at = tabs.find((t) => t.id === active);
      if (at) { const drop = [...vis].reverse().find((v) => !(v.group && groups[v.group]?.collapsed)); if (drop) vis.splice(vis.indexOf(drop), 1); vis.push(at); }
    }
    const visIds = new Set(vis.map((t) => t.id));
    return { visTabs: vis, hidTabs: tabs.filter((t) => !visIds.has(t.id)) };
  }, [tabs, visBudget, active, groups]);
  const dragS = useRef(null);
  const flipPrev = useRef({});
  const proxyRef = useRef(null);
  const cueRef = useRef(null);
  const startTabDrag = useCallback((t) => (e) => {
    if (e.button !== 0 || renameId) return;
    if (e.target.closest(".xc,.aud,.rn")) return;
    const sx = e.clientX, sy = e.clientY, id = t.id;
    const commitDrop = () => {
      const st = dragS.current; if (!st) return;
      if (st.foldGid && groupsRef.current[st.foldGid]) {
        const gid = st.foldGid;
        setTabs((ts) => {
          const me = ts.find((x) => x.id === id); if (!me) return ts;
          let arr = ts.filter((x) => x.id !== id);
          const lastIdx = arr.map((x) => x.group).lastIndexOf(gid);
          arr.splice(lastIdx + 1, 0, { ...me, group: gid });
          return arr;
        });
        noteRef2.current && noteRef2.current("Filed into “" + (groupsRef.current[gid].name) + "”");
        return;
      }
      const { anchorId, lastVisId } = st;
      if (anchorId === undefined && lastVisId === undefined) return;
      setTabs((ts) => {
        const me = ts.find((x) => x.id === id); if (!me) return ts;
        const curIdx = ts.indexOf(me);
        let arr = ts.filter((x) => x.id !== id);
        let insertAt = anchorId != null ? arr.findIndex((x) => x.id === anchorId)
                      : lastVisId != null ? arr.findIndex((x) => x.id === lastVisId) + 1
                      : arr.length;
        if (insertAt < 0) insertAt = arr.length;
        // pinned zone clamp against the full array
        const pinnedCount = arr.filter((x) => x.pin).length;
        if (!me.pin && insertAt < pinnedCount) insertAt = pinnedCount;
        if (me.pin && insertAt > pinnedCount) insertAt = pinnedCount;
        if (insertAt === curIdx && ts[curIdx]?.id === id) return ts;
        arr.splice(insertAt, 0, me);
        if (arr.map((x) => x.id).join() === ts.map((x) => x.id).join()) return ts;
        // group adoption: both full-array neighbors share a group → join; else ungrouped
        const gL = arr[insertAt - 1]?.group, gR = arr[insertAt + 1]?.group;
        const newG = gL && gL === gR ? gL : undefined;
        if (me.group !== newG) arr = arr.map((x) => x.id === id ? { ...x, group: newG } : x);
        return arr;
      });
    };
    startPointerDrag(e, {
      threshold: 6,
      onStart: (ev) => {
        heldRef.current = true;
        clearTimeout(glanceT.current); setGlance(null);
        const chipEl = stripRef.current?.querySelector(`.ttab[data-id="${id}"]`);
        const nova = stripRef.current?.closest(".nova");
        let grabX = 60;
        if (chipEl && nova) {
          const s = nova.getBoundingClientRect().width / DESIGN_W;
          grabX = (sx - chipEl.getBoundingClientRect().left) / s;
        }
        setDragId(id); dragS.current = { id, overSpace: null, grabX,
          label: (t.label || t.title).slice(0, 24), gcol: t.group && groups[t.group]?.color, noPane: t.url === "nova://newtab" };
      },
      onMove: (ev) => {
      // space-drop hit test
      const el = document.elementFromPoint(ev.clientX, ev.clientY);
      dragS.current.overSpace = el?.closest?.(".dropsp")?.dataset?.sp || null;
      document.querySelectorAll(".dropsp").forEach((d) => d.classList.toggle("hot", d.dataset.sp === dragS.current.overSpace));
      // position the floating proxy (screen → design coords) — always follows
      const nova = stripRef.current?.closest(".nova");
      if (nova && proxyRef.current) {
        const nr = nova.getBoundingClientRect();
        const s = nr.width / DESIGN_W;
        proxyRef.current.style.transform = `translate(${(ev.clientX - nr.left) / s - dragS.current.grabX}px, ${(ev.clientY - nr.top) / s - 14}px)`;
      }
      if (dragS.current.overSpace) { if (cueRef.current) cueRef.current.style.opacity = "0"; return; }
      if (!dragS.current.noPane) { const panesEls = [...document.querySelectorAll(".pane[data-pane]")]; let ovp = null;
        for (const pn of panesEls) { const pr = pn.getBoundingClientRect(); if (ev.clientX >= pr.left && ev.clientX <= pr.right && ev.clientY >= pr.top && ev.clientY <= pr.bottom) { ovp = +pn.dataset.pane; break; } }
        dragS.current.overPane = ovp;
        panesEls.forEach((pn) => pn.classList.toggle("dropover", ovp != null && pn.dataset.pane === String(ovp)));
        if (ovp != null) { if (cueRef.current) cueRef.current.style.opacity = "0"; return; } }
      // compute anchor for the drop cue — neighbors stay frozen
      const strip = stripRef.current; if (!strip) return;
      const others = [...strip.querySelectorAll(".ttab[data-id]")].filter((c) => +c.dataset.id !== id);
      let anchorId = null, cueX = null;
      const sr = strip.getBoundingClientRect();
      const nr2 = nova ? nova.getBoundingClientRect() : sr;
      const sc = nr2.width / DESIGN_W;
      for (const c of others) {
        const r = c.getBoundingClientRect();
        if (ev.clientX < r.left + r.width / 2) { anchorId = +c.dataset.id; cueX = (r.left - sr.left) / sc - 2; break; }
      }
      if (cueX == null && others.length) {
        const last = others[others.length - 1].getBoundingClientRect();
        cueX = (last.right - sr.left) / sc + 1;
      }
      dragS.current.anchorId = anchorId;
      dragS.current.lastVisId = others.length ? +others[others.length - 1].dataset.id : null;
      if (cueRef.current) {
        cueRef.current.style.opacity = dragS.current.overSpace ? "0" : "1";
        cueRef.current.style.transform = `translateX(${cueX}px)`;
        const ts2 = tabsRef.current;
        const anchorT = ts2.find((x) => x.id === anchorId);
        const ai = anchorT ? ts2.indexOf(anchorT) : -1;
        const gJoin = anchorT?.group && ai > 0 && ts2[ai - 1]?.group === anchorT.group && ts2[ai - 1].id !== id ? anchorT.group : null;
        cueRef.current.style.background = gJoin ? (groupsRef.current[gJoin]?.color || "var(--ac)") : "var(--ac)";
        // dropping ONTO a collapsed folder chip files the tab into that group
        const foldEl = el && el.closest ? el.closest(".ttab.fold") : null;
        const foldGid = foldEl ? foldEl.dataset.gid : null;
        document.querySelectorAll(".ttab.fold.droptarget").forEach((f) => f.classList.remove("droptarget"));
        if (foldGid) { foldEl.classList.add("droptarget"); if (cueRef.current) cueRef.current.style.opacity = "0"; }
        dragS.current.foldGid = foldGid || null;
      }
      },
      onEnd: (ev, started) => {
      document.querySelectorAll(".dropsp").forEach((d) => d.classList.remove("hot"));
      document.querySelectorAll(".ttab.fold.droptarget").forEach((f) => f.classList.remove("droptarget"));
      document.querySelectorAll(".pane[data-pane].dropover").forEach((p) => p.classList.remove("dropover"));
      const target = dragS.current?.overSpace;
      const overPane = dragS.current?.overPane;
      if (started && overPane != null && assignPaneRef.current) assignPaneRef.current(overPane, id);
      else if (started && target) moveTabToSpaceRef.current(id, target);
      else if (started) commitDrop();
      setDragId(null);
      if (started) setTimeout(() => { heldRef.current = false; }, 0);
      dragS.current = null;
      },
    });
  }, [renameId]);

  const moveTabToSpaceRef = useRef(null);
  moveTabToSpaceRef.current = (id, targetId) => {
    const t = tabsRef.current.find((x) => x.id === id); if (!t) return;
    if (t.pin) { note("Pinned tabs stay in their project"); return; }
    const store = spaceStore.current;
    if (!store[targetId]) store[targetId] = { tabs: [{ id: Date.now() + 1, title: "Turing — New Tab", url: "nova://newtab", secure: true, heat: 0 }], groups: {}, active: null };
    store[targetId].tabs = [...store[targetId].tabs, { ...t, group: undefined }];
    setTabs((ts) => {
      const n = ts.filter((x) => x.id !== id);
      if (n.length === 0) {
        const fresh = { id: Date.now(), title: "Turing — New Tab", url: "nova://newtab", secure: true, heat: 0 };
        setActive(fresh.id); setView("newtab"); return [fresh];
      }
      if (id === activeRef.current) { setActive(n[0].id); setView("newtab"); }
      return n;
    });
    const nm = spaces.find((s) => s.id === targetId)?.name || targetId;
    note(`Moved to ${nm}`, [{ label: "Go there", fn: () => { setNotice(null); switchSpace(targetId); } }]);
  };

  // FLIP: animate only when the strip's structure actually changes — never on hover renders
  const orderSig = useMemo(() =>
    visTabs.map((t) => t.id + ":" + (t.group || "")).join("|") + "§" +
    Object.entries(groups).map(([k, v]) => k + (v.collapsed ? 1 : 0)).join(","),
  [visTabs, groups]);
  useLayoutEffect(() => {
    const strip = stripRef.current; if (!strip) return;
    const els = [...strip.querySelectorAll("[data-flip]")];
    const next = {};
    els.forEach((el) => {
      const k = el.dataset.flip;
      const r = el.getBoundingClientRect();
      next[k] = r.left;
      const prev = flipPrev.current[k];
      if (prev != null && Math.abs(prev - r.left) > 1 && k !== "t" + dragId) {
        el.getAnimations().forEach((a) => a.cancel());
        el.animate([{ transform: `translateX(${prev - r.left}px)` }, { transform: "translateX(0)" }], { duration: 170, easing: EASE_OUT });
      }
    });
    flipPrev.current = next;
  }, [orderSig, dragId]); // eslint-disable-line

  // ---- animated close: guards first, then collapse, then remove ----
  const [closingIds, setClosingIds] = useState(() => new Set());
  const performClose = useCallback((id) => {
    setTabs((ts) => {
      const idx = ts.findIndex((t) => t.id === id);
      if (idx === -1) return ts;
      closedRef.current.push(ts[idx]);
      if (closedRef.current.length > 20) closedRef.current.shift();
      delete scrollMem.current[id];
      // eslint-disable-next-line no-empty

      const n = ts.filter((t) => t.id !== id);
      if (n.length === 0) {
        const fresh = { id: Date.now(), title: "Turing — New Tab", url: "nova://newtab", secure: true, heat: 0 };
        setActive(fresh.id); setView("newtab");
        return [fresh];
      }
      if (id === activeRef.current) {
        const nb = n[Math.min(idx, n.length - 1)];
        setActive(nb.id); setView("newtab");
      }
      return n;
    });
  }, [note]);

  const closeTab = useCallback((id, e) => {
    if (e) e.stopPropagation();
    const t = tabsRef.current.find((x) => x.id === id);
    if (!t) return;
    if (t.pin) { note("Pinned — unpin to close"); return; }
    if (dirtyRef.current[id]) {
      note("You have unsaved typing here", [
        { label: "Close anyway", fn: () => { dirtyRef.current[id] = false; setNotice(null); closeRef.current(id); } },
        { label: "Keep", fn: () => setNotice(null) },
      ]);
      return;
    }
    setClosingIds((s) => new Set(s).add(id));
    setTimeout(() => {
      performClose(id);
      setClosingIds((s) => { const n = new Set(s); n.delete(id); return n; });
    }, 150);
  }, [note, performClose]);

  const reopenTab = useCallback(() => {
    const t = closedRef.current.pop();
    if (!t) { note("Nothing to reopen"); return; }
    const id = Date.now();
    const nt = { ...t, id };
    setTabs((ts) => [...ts, nt]);
    setActive(id); setView("newtab");
    record(id, "newtab", nt.url, nt.title);
    note(`Reopened “${(nt.label || nt.title).slice(0, 32)}”`);
    sweep();
  }, [record, sweep, note]);

  const addTab = useCallback(() => {
    const id = uid();
    setTabs((ts) => [...ts, { id, title: "Turing — New Tab", url: "nova://newtab", secure: true, heat: 0 }]);
    setActive(id); setView("newtab");
    record(id, "newtab", "nova://newtab", "Turing — New Tab");
  }, [record]);

  const TRACKY = /(google\.com\/search|youtube|news\.|doubleclick)/;

  const selectTab = useCallback((t) => {
    if (t.group) setGroups((gs) => gs[t.group]?.collapsed ? { ...gs, [t.group]: { ...gs[t.group], collapsed: false } } : gs);
    setActive(t.id); setView("newtab"); setAutoHide(false); setGlance(null);
    setTabs((ts) => ts.map((x) => (x.id === t.id ? { ...x, heat: 0 } : x)));
    record(t.id, "newtab", t.url, t.title);
    sweep(flags.adblock && TRACKY.test(t.url) ? "good" : "ac");
  }, [sweep, record, flags.adblock]);
  selectRef.current = selectTab;

  const loadT = useRef({});
  const markLoading = useCallback((id) => {
    setTabs((ts) => ts.map((x) => x.id === id ? { ...x, status: "loading" } : x));
    clearTimeout(loadT.current[id]);
    loadT.current[id] = setTimeout(() => setTabs((ts) => ts.map((x) => x.id === id ? { ...x, status: undefined } : x)), 750);
  }, []);
  const navigate = useCallback((q) => {
    const bang = applyBang(q);
    if (bang) {
      markLoading(active);
      setTabs((ts) => ts.map((x) => (x.id === active ? { ...x, url: bang.url, title: bang.term + " — " + bang.name, heat: 0, status: "loading" } : x)));
      setView("newtab"); setCmd(false); setAutoHide(false);
      note("Searched " + bang.name + " directly");
      return;
    }
    let url = q.trim().replace(/^https?:\/\//, "");
    let title = url;
    if (!url.includes(".") || url.includes(" ")) { title = q.trim() + " — Search"; url = "google.com/search?q=" + encodeURIComponent(q.trim()); }
    markLoading(active);
    setTabs((ts) => ts.map((x) => (x.id === active ? { ...x, url, title, heat: 0, status: "loading" } : x)));
    setView("newtab"); setCmd(false); setAutoHide(false); record(active, "newtab", url, title);
    sweep(flags.adblock && TRACKY.test(url) ? "good" : "ac");
  }, [active, sweep, record, flags.adblock, markLoading]);

  const SESSION = [
    { id: 9101, title: "Linear – Sprint board", url: "linear.app/nova/sprint", secure: true, heat: 0 },
    { id: 9102, title: "Figma — Nova Design System", url: "figma.com/file/nova-ds", secure: true, heat: 0 },
    { id: 9103, title: "Mercury – Banking for startups", url: "mercury.com/dashboard", secure: true, heat: 1 },
    { id: 9104, title: "Stripe Docs — Payment Intents", url: "stripe.com/docs/payments", secure: true, heat: 1 },
  ];
  const resumeSession = useCallback(() => {
    setTabs(SESSION); setActive(SESSION[0].id); setView("newtab"); setCmd(false);
    record(SESSION[0].id, "newtab", SESSION[0].url, SESSION[0].title); sweep();
    note("Restored yesterday — 4 tabs");
  }, [record, sweep, note]);

  const copyUrl = useCallback(() => {
    const t = tabsRef.current.find((x) => x.id === activeRef.current);
    try { navigator.clipboard && navigator.clipboard.writeText("https://" + t.url); } catch { }
    note("Address copied");
    setCmd(false);
  }, [note]);

  const toggleReader = useCallback(() => {
    setReaderIds((r) => ({ ...r, [activeRef.current]: !r[activeRef.current] }));
    setCmd(false); sweep();
  }, [sweep]);

  const toggleSplit = useCallback((id) => {
    setSplitId((s) => {
      if (s) { note("Split view closed"); return null; }
      const pick = tabsRef.current.find((t) => t.id !== activeRef.current && t.url !== "nova://newtab") || tabsRef.current.find((t) => t.id !== activeRef.current);
      const other = id != null ? id : (pick || {}).id;
      if (other == null) { note("Open another tab to split"); return null; }
      note("Split view — drag a tab into either side · drag the middle to resize");
      return other;
    });
    setCmd(false); setCtx(null);
  }, [note]);

  const assignPane = useCallback((side, id) => {
    const a = activeRef.current, s = splitIdRef.current;
    if (id === a && id === s) return;
    if (side === 1) { if (id === s) return; if (id === a) { setActive(s); setSplitId(id); } else setSplitId(id); }
    else { if (id === a) return; if (id === s) { setSplitId(a); setActive(id); } else setActive(id); }
  }, []);
  const assignPaneRef = useRef(null); assignPaneRef.current = assignPane;
  const closeSplit = useCallback((keep) => {
    if (keep === "right") { const s = splitIdRef.current; if (s != null) setActive(s); }
    setSplitId(null); note("Split view closed");
  }, [note]);
  const nudgeSplit = useCallback((d) => {
    if (splitIdRef.current == null) { note("No split view — ⌘\\ opens one"); return; }
    setSplitRatio((r) => { const n = Math.max(0.22, Math.min(0.78, r + d)); note("Split " + Math.round(n * 100) + " / " + Math.round((1 - n) * 100)); return n; });
  }, [note]);
  const nudgeRef = useRef(null); nudgeRef.current = nudgeSplit;
  const swapPanes = useCallback(() => {
    const a = activeRef.current, sp = splitIdRef.current;
    if (sp == null) { note("No split view — ⌘\\ opens one"); return; }
    setActive(sp); setSplitId(a); setSplitRatio((r) => 1 - r); note("Panes swapped");
  }, [note]);
  const swapRef = useRef(null); swapRef.current = swapPanes;
  const resetSplit = useCallback(() => { setSplitRatio(0.5); note("Panes reset to 50 / 50"); }, [note]);
  const saveLayout = useCallback(() => {
    const a = activeRef.current, sp = splitIdRef.current, ts = tabsRef.current;
    if (sp == null) { note("Open a split view first — ⌘\\"); return; }
    const L = ts.find((t) => t.id === a), R = ts.find((t) => t.id === sp);
    if (!L || !R) return;
    const dom = (t) => t.url.split("/")[0];
    const gname = L.group && L.group === R.group ? groupsRef.current?.[L.group]?.name : null;
    const name = gname || (dom(L) + " ｜ " + dom(R));
    const had = (layoutsRef.current[spaceId] || []).some((x) => x.name === name);
    const entry = { name, left: a, right: sp, ratio: splitRatioRef.current, ld: dom(L), rd: dom(R) };
    setLayouts((m) => ({ ...m, [spaceId]: [entry, ...(m[spaceId] || []).filter((x) => x.name !== name)].slice(0, 8) }));
    note((had ? "Layout updated · " : "Layout saved · ") + name);
  }, [spaceId, note]);
  const applyLayout = useCallback((i) => {
    const l = (layoutsRef.current[spaceId] || [])[i];
    if (!l) return;
    const ts = tabsRef.current, has = (id) => ts.some((t) => t.id === id);
    if (!has(l.left) || !has(l.right)) { note("Layout unavailable — those tabs are closed"); return; }
    setActive(l.left); setSplitId(l.right); setSplitRatio(l.ratio); setView("newtab"); note("Layout · " + l.name);
  }, [spaceId, note]);
  const forgetLayout = useCallback((i) => {
    setLayouts((m) => ({ ...m, [spaceId]: (m[spaceId] || []).filter((_, j) => j !== i) }));
    note("Layout forgotten");
  }, [spaceId, note]);
  const dblRef = useRef(0);
  const startDivider = useCallback((e) => {
    e.preventDefault();
    const now = Date.now();
    if (now - dblRef.current < 340) { dblRef.current = 0; resetSplit(); return; }
    dblRef.current = now;
    const wrap = e.currentTarget.closest(".splitwrap"); if (!wrap) return;
    const div = e.currentTarget; div.classList.add("drag");
    const move = (ev) => { const r = wrap.getBoundingClientRect(); const ratio = (ev.clientX - r.left) / r.width; setSplitRatio(Math.max(0.22, Math.min(0.78, ratio))); };
    const up = () => { window.removeEventListener("pointermove", move); window.removeEventListener("pointerup", up); document.body.classList.remove("col-resizing"); div.classList.remove("drag"); };
    window.addEventListener("pointermove", move); window.addEventListener("pointerup", up); document.body.classList.add("col-resizing");
  }, [note, resetSplit]);

  const zoomBy = useCallback((delta) => {
    const t = tabsRef.current.find((x) => x.id === activeRef.current);
    if (!t || t.url === "nova://newtab") return;
    const dom = t.url.split("/")[0];
    setZoomMap((m) => {
      const z = delta === 0 ? 1 : Math.min(1.6, Math.max(0.6, +(((m[dom] || 1) + delta)).toFixed(2)));
      note(Math.round(z * 100) + "% · " + dom);
      const next = { ...m, [dom]: z };
      const ks = Object.keys(next);
      if (ks.length > 40) delete next[ks[0]];
      return next;
    });
  }, [note]);

  const duplicateTab = useCallback((id) => {
    setTabs((ts) => {
      const i = ts.findIndex((t) => t.id === id);
      if (i === -1) return ts;
      const copy = { ...ts[i], id: Date.now(), pin: false };
      const n = [...ts]; n.splice(i + 1, 0, copy);
      setActive(copy.id); setView("newtab");
      record(copy.id, "newtab", copy.url, copy.title);
      return n;
    });
    setCtx(null); sweep();
  }, [record, sweep]);

  const reopenAt = useCallback((idx) => {
    const t = closedRef.current.splice(idx, 1)[0];
    if (!t) return;
    const nt = { ...t, id: Date.now() };
    setTabs((ts) => [...ts, nt]);
    setActive(nt.id); setView("newtab");
    record(nt.id, "newtab", nt.url, nt.title);
    setCmd(false); sweep();
  }, [record, sweep]);

  const closeAllTabs = useCallback(() => {
    setLastSession(tabsRef.current);
    const fresh = { id: Date.now(), title: "Turing — New Tab", url: "nova://newtab", secure: true, heat: 0 };
    setTabs([fresh]); setActive(fresh.id); setView("newtab");
    setConfirmClose(false); setSplitId(null);
  }, []);

  const restoreSession = useCallback(() => {
    if (!lastSession) return;
    setTabs(lastSession); setActive(lastSession[0].id); setView("newtab");
    setLastSession(null); note(`Restored ${lastSession.length} tabs`); sweep();
  }, [lastSession, note, sweep]);

  const openInNew = useCallback((url) => {
    const id = Date.now();
    const clean = url.replace(/^https?:\/\//, "");
    setTabs((ts) => [...ts, { id, title: clean, url: clean, secure: true, heat: 0 }]);
    setActive(id); setView("newtab"); setCmd(false);
    record(id, "newtab", clean, clean); sweep();
  }, [record, sweep]);

  const agentOpen = useCallback((url) => {
    const clean = url.replace(/^https?:\/\//, "");
    const dom = clean.split("/")[0];
    if (tabsRef.current.some((t) => t.url.split("/")[0] === dom)) return;
    const id = Date.now() + Math.floor(Math.random() * 100);
    setTabs((ts) => [...ts, { id, title: clean, url: clean, secure: true, heat: 0 }]);
    note("Agent opened " + dom + " — background tab, scoped");
  }, [note]);

  const zenTimer = useCallback((mins) => {
    setZen(true); setCmd(false);
    clearTimeout(zenTimerRef.current);
    zenTimerRef.current = setTimeout(() => setZen(false), mins * 60000);
  }, []);

  const addRef = useRef(null), closeRef = useRef(null), reopenRef = useRef(null);
  addRef.current = addTab; closeRef.current = closeTab; reopenRef.current = reopenTab;
  const copyRef = useRef(null), readerRef = useRef(null), splitRef = useRef(null), zoomRef = useRef(null);
  copyRef.current = copyUrl; readerRef.current = toggleReader; splitRef.current = () => toggleSplit(); zoomRef.current = zoomBy;
  const goRef = useRef(null), markRef = useRef(null), aiRef = useRef(null);
  goRef.current = go; markRef.current = toggleBookmark; aiRef.current = () => setAi((v) => !v);

  const tidyTabs = useCallback(() => {
    setTabs((ts) => {
      const n = ts.filter((t) => t.pin || t.heat < 2 || t.id === active);
      const removed = ts.length - n.length;
      if (removed) {
        const prev = ts;
        note(`Closed ${removed} faded tab${removed === 1 ? "" : "s"}`, [{ label: "Undo", fn: () => { setTabs(prev); setNotice(null); } }]);
      } else note("Nothing to tidy yet");
      return n.length ? n : ts;
    });
  }, [active, note]);

  const delHistory = useCallback((id) => { /* concept: no-op removal animation slot */ }, []);

  return (
    <div className="stage">
      <style>{CSS}</style>
      {!present && (
      <div className="zbar">
        <span className="zt">Turing</span>
        <span className="zd">desktop · 1440×900 · {Math.round(eff * 100)}%</span>
        <div className="zseg">
          {[["fit", "Fit"], [0.5, "50"], [0.75, "75"], [1, "100"]].map(([z, l]) => (
            <button key={l} className={zoom === z ? "on" : ""} onClick={() => setZoom(z)}>{l}</button>
          ))}
        </div>
        <button className="zpres" onClick={() => setPresent(true)}>Present <span style={{ opacity: .55 }}>⌘.</span></button>
      </div>
      )}
      <div className={"canvas" + (present ? " present" : "")} ref={canvasRef}>
        <div className="holder" style={{ width: 1440 * eff + 56, height: 900 * eff + 56 }}>
          <div className={"nova" + (theme === "light" ? " light" : "") + (density === "compact" ? " compact" : "")}
            style={{ transform: `scale(${eff || 0.5})`, ...themeVars, "--ac": customVars["--ac"] || tint, "--ac-soft": rgba(customVars["--ac"] || tint, theme === "light" ? 0.11 : 0.12), "--ac-line": rgba(customVars["--ac"] || tint, 0.4) }}>
          {hideBar && !peek && <div className="peek" onMouseEnter={() => setPeek(true)} />}

      {/* ===== the bar — window, navigation, tabs, and address in one ===== */}
      {(!hideBar || peek) && (
      <div className={"bar" + (hideBar ? " float" : "")} onMouseLeave={hideBar ? () => { if (!popRef.current) setPeek(false); } : undefined}>
        {loading && <span className="lsweep" style={{ background: `linear-gradient(90deg,transparent,var(--${sweepClr}),transparent)` }} />}
        <div className="traffic"><span className="dot r" onClick={() => (tabsRef.current.length > 3 ? setConfirmClose(true) : closeAllTabs())} style={{ cursor: "pointer" }} /><span className="dot y" /><span className="dot g" /></div>
        {(tabPos === "left" || tabPos === "right") && (
          <button className="ib" style={{ width: 28, height: 28 }} title={(sideOpen ? "Hide" : "Show") + " sidebar (⇧⌘S)"} onClick={() => sideRef.current()}>
            {tabPos === "right" ? <PanelRight size={15} /> : <PanelLeft size={15} />}
          </button>
        )}
        <div className="nav">
          <button className={"ib" + (canBack ? "" : " off")}
            onClick={() => { if (heldRef.current) { heldRef.current = false; return; } canBack && goHist(-1); }}
            onMouseDown={() => { glanceT.current = setTimeout(() => { heldRef.current = true; setPop("trail"); }, 400); }}
            onMouseUp={() => clearTimeout(glanceT.current)} onMouseLeave={() => clearTimeout(glanceT.current)}
            title="Back · hold for trail"><ArrowLeft size={16} /></button>
          <button className={"ib" + (canFwd ? "" : " off")} onClick={() => canFwd && goHist(1)}><ArrowRight size={16} /></button>
          <button className="ib" title="Reload page" onClick={() => sweep()}><RotateCw size={15} /></button>
        </div>

        {tabPos === "top" ? (
          tabs.length === 1 ? (
            <div className="ttabs" style={{ justifyContent: "center" }}>
              <button className="site" style={{ flex: "0 1 auto", maxWidth: 420, padding: "0 14px" }} onClick={() => setCmd(true)} title="Search or enter address · ⌘K">
                {!isNT && <Lock size={11} color="var(--good)" />}
                {isNT ? <span style={{ overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap", color: "var(--tx3)" }}>Search or enter address</span> : <UrlText url={tab.url} />}
                <span className="kbd">⌘K</span>
              </button>
              <div className="dropcue" ref={cueRef} aria-hidden />
            {hidTabs.length > 0 && (
              <button className="ovf" onClick={() => setTabSearch(true)} title={hidTabs.length + " more tabs · ⇧⌘A"}>
                <ChevronDown size={13} /><span className="mono">{hidTabs.length}</span>
              </button>
            )}
            <button className="newtab" onClick={addTab} aria-label="New tab"><Plus size={15} /></button>
            </div>
          ) : (
          <div className="ttabs" ref={stripRef} onDoubleClick={(e) => { if (e.target.classList && e.target.classList.contains("ttabs")) addTab(); }}>
            {(() => {
              const chip = (t, ti) => {
              const on = t.id === active;
              const fadeCls = !on && !t.pin && flags.fade && t.heat > 0 ? " s" + t.heat : "";
              const peeking = glance && glance.id === t.id ? " peeking" : "";
              if (renameId === t.id) return (
                <div key={t.id} className="ttab on" style={{ minWidth: 140 }}>
                  <input autoFocus className="rn" defaultValue={t.label || t.title}
                    onKeyDown={(e) => { if (e.key === "Enter") { const v = e.target.value.trim(); setTabs((ts) => ts.map((x) => x.id === t.id ? { ...x, label: v || undefined } : x)); setRenameId(null); } if (e.key === "Escape") setRenameId(null); }}
                    onBlur={(e) => { const v = e.target.value.trim(); setTabs((ts) => ts.map((x) => x.id === t.id ? { ...x, label: v || undefined } : x)); setRenameId(null); }} />
                </div>
              );
              return (
                <div key={t.id} className={"ttab" + (on ? " on" : "") + (t.pin ? " pinned" : "") + (t.status === "error" ? " err" : "") + (t.group ? " gm" : "") + (kinG && t.group === kinG ? " kin" : "") + fadeCls + peeking + (dragId === t.id ? " ghost" : "") + (closingIds.has(t.id) ? " closing" : "") + (agentOn.ids.includes(t.id) ? (agentOn.wait ? " agentwait" : " agenton") : "")}
                  data-id={t.id} data-flip={"t" + t.id}
                  onPointerDown={(e) => { if (e.button === 1) { e.preventDefault(); e.stopPropagation(); closeTab(t.id, e); return; } startTabDrag(t)(e); }}
                  onContextMenu={(e) => {
                    e.preventDefault();
                    const nr = e.currentTarget.closest(".nova").getBoundingClientRect();
                    const s = nr.width / DESIGN_W;
                    setCtx({ id: t.id, x: (e.clientX - nr.left) / s, y: (e.clientY - nr.top) / s });
                  }}
                  onClick={(e) => {
                    if (e.detail > 1) return;
                    if (heldRef.current) { heldRef.current = false; return; }
                    if (t.status === "error") { markLoading(t.id); note("Retrying " + t.url.split("/")[0] + "…"); selectTab(t); return; }
                    if (on) { setCmd(true); return; }
                    selectTab(t);
                  }}
                  onMouseDown={(e) => { if (e.button === 1) { e.preventDefault(); closeTab(t.id, e); return; } if (e.button === 0 && !on) glanceT.current = setTimeout(() => { heldRef.current = true; setGlance(t); }, 320); }}
                  onMouseUp={() => { clearTimeout(glanceT.current); setGlance(null); }}
                  onMouseLeave={() => { clearTimeout(glanceT.current); setGlance(null); }}
                  title={on ? "Search or enter address · ⌘K" : t.title + " · hold to glance · right-click for options"}>
                  <span className="tst" aria-hidden>
                    {on && t.status !== "loading" && <span className="tsearch"><Search size={10.5} /></span>}
                    {t.status === "loading" ? <i className="tspin" />
                    : t.status === "error" ? <i className="terr" title="Couldn’t load — click to retry" />
                    : t.pin ? <Pin size={10} color="var(--tx3)" />
                    : t.audio ? (
                      <button className="aud" title={t.audio === "muted" ? "Auto-muted — tap to unmute" : "Playing — tap to mute"}
                        onClick={(e) => { e.stopPropagation(); note(t.audio === "muted" ? "Unmuted" : "Muted"); setTabs((ts) => ts.map((x) => x.id === t.id ? { ...x, audio: x.audio === "muted" ? "on" : "muted" } : x)); }}>
                        {t.audio === "muted" ? <VolumeX size={11} /> : <Volume2 size={11} color="var(--ac)" />}
                      </button>
                    ) : <FavImg d={t.url.split("/")[0]} />}
                  </span>
                  {agentOn.ids.includes(t.id) && (
                    <span className="agdot" title={agentOn.wait ? "Agent is waiting for you to approve a step" : "An agent is working on this tab"} aria-hidden />
                  )}
                  {modHeld && ti < 9 && <span className="numhint">{ti + 1}</span>}
                  {on && !isNT && <Lock size={11} color="var(--good)" onClick={(e) => { e.stopPropagation(); setPop(pop === "security" ? null : "security"); }} />}
                  {on ? (isNT ? <span className="ttl" style={{color:"var(--tx3)"}}>Search or enter address</span> : <UrlText url={tab.url} />) : <span className="ttl">{t.label || t.title}</span>}
                  {on && <span className="kbd">⌘K</span>}
                  {!t.pin && <button className="xc" onClick={(e) => closeTab(t.id, e)} aria-label="Close tab"><X size={12} /></button>}
                </div>
              );
              };
              // one element type: chips. members carry a colored dot; a collapsed group IS a chip.
              const items = [];
              let i = 0;
              const src2 = visTabs;
              while (i < src2.length) {
                const t = src2[i];
                const g = t.group && groups[t.group];
                if (!g) { items.push(chip(t, tabs.indexOf(t))); i++; continue; }
                const gid = t.group, members = [];
                while (i < src2.length && src2[i].group === gid) { members.push(src2[i]); i++; }
                if (g.collapsed) {
                  items.push(
                    <div key={"g" + gid} className={"ttab fold" + (members.some((m) => agentOn.ids.includes(m.id)) ? (agentOn.wait ? " agentwait" : " agenton") : "")}
                      data-gid={gid} data-flip={"g" + gid}
                      title={g.name + " — " + members.length + " tabs · click to expand" + (members.some((m) => agentOn.ids.includes(m.id)) ? (agentOn.wait ? " · agent needs your approval inside" : " · an agent is working in here") : "")}
                      onPointerDown={startGroupDrag(gid)}
                      onClick={(e) => { if (e.currentTarget.dataset.dragged) return; setGroups((gs) => ({ ...gs, [gid]: { ...g, collapsed: false } })); }}>
                      <span className="tst"><i className="gdot" style={{ background: g.color }} /></span>
                      <span className="ttl">{g.name}</span>
                      {members.some((m) => agentOn.ids.includes(m.id)) && <span className="agdot" aria-hidden />}
                      <span className="fold-n mono">{members.length}</span>
                      <span className="fold-x"><ChevronDown size={11} /></span>
                    </div>
                  );
                } else {
                  items.push(
                    <div key={"g" + gid} className="trun" data-flip={"g" + gid} style={{ "--gc": g.color }}>
                      <button className={"gpill" + (members.some((m) => agentOn.ids.includes(m.id)) ? " agenton" : "")}
                        title={g.name + " — click to collapse · drag to move the group"}
                        onPointerDown={startGroupDrag(gid)}
                        onMouseEnter={() => setKinG(gid)} onMouseLeave={() => setKinG(null)}
                        onClick={(e) => { if (e.currentTarget.dataset.dragged) return; setGroups((gs) => ({ ...gs, [gid]: { ...g, collapsed: true } })); }}>{g.name}<ChevronDown size={9} className="gp-c" /></button>
                      {members.map((m) => chip(m, tabs.indexOf(m)))}
                    </div>
                  );
                }
              }
              return items;
            })()}
            <div className="dropcue" ref={cueRef} aria-hidden />
            {hidTabs.length > 0 && (
              <button className="ovf" onClick={() => setTabSearch(true)} title={hidTabs.length + " more tabs · ⇧⌘A"}>
                <ChevronDown size={13} /><span className="mono">{hidTabs.length}</span>
              </button>
            )}
            <button className="newtab" onClick={addTab} aria-label="New tab"><Plus size={15} /></button>
          </div>
          )
        ) : (
          <button className="site" onClick={() => setCmd(true)} title="Search or enter address · ⌘K">
            {!isNT && <Lock size={11} color="var(--good)" />}
            {isNT ? <span style={{ overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap", color: "var(--tx3)" }}>Search or enter address</span> : <UrlText url={tab.url} />}
            <span className="kbd">⌘K</span>
          </button>
        )}

        {(() => { const z = zoomMap[tab.url.split("/")[0]]; return z && Math.abs(z - 1) > 0.01 ? (
          <button className="zoomchip mono" title="Reset zoom (⌘0)" onClick={() => setZoomMap((m) => ({ ...m, [tab.url.split("/")[0]]: 1 }))}>{Math.round(z * 100)}%</button>
        ) : null; })()}
        <span className="bar-sep" style={{ marginLeft: "auto" }} />
        <div className="acts" style={{ marginLeft: 0 }}>
          {flags.devmode && <PerfPill onClick={() => { setDock(true); setDockTab("elements"); }} />}
          {flags.devmode && (
            <button className={"ib" + (dock ? " on" : "")} onClick={() => setDock((v) => !v)} title="Inspector · ⌥⌘I"><Terminal size={15} /></button>
          )}
          <button className={"ib" + (ai ? " on" : "")} onClick={() => setAi((v) => !v)} title="Ask Turing · ⌘E"><Sparkles size={15} /></button>
          {(() => {
            const dm = tab.url.split("/")[0];
            const has = vault.some((e) => e.site === dm || dm.endsWith("." + e.site));
            return (
              <button className={"ib" + (pop === "vault" ? " on" : "")} onClick={() => setPop(pop === "vault" ? null : "vault")}
                title={has ? "Saved login for " + dm : "Passwords"} style={{ position: "relative" }}>
                <KeyRound size={16} />
                {has && !vaultLocked && <span className="kdot" />}
              </button>
            );
          })()}
          <button className={"ib" + (pop === "approve" ? " on" : "")} style={{ position: "relative" }}
            onClick={() => setPop(pop === "approve" ? null : "approve")}
            title={approvals.length ? approvals.length + " action waiting on you" : "Nothing waiting on you"}>
            <Gavel size={16} />
            {approvals.length > 0 && <span className="apqbadge">{approvals.length}</span>}
          </button>
          {(() => {
            const dm = tab.url.split("/")[0];
            const lv = shieldSites[dm] || "standard";
            const rep = shieldFor(dm);
            const n = (lv === "off" || !flags.adblock) ? 0 : rep.trackers + rep.ads + rep.banners;
            return (
              <button className={"ib" + (pop === "shield" ? " on" : "")} style={{ position: "relative" }}
                onClick={() => setPop(pop === "shield" ? null : "shield")}
                title={"Turing Shield — " + (n ? n + " blocked on this page" : "off for this site")}>
                <ShieldCheck size={16} />
                {n > 0 && <span className="shbadge">{n > 99 ? "99+" : n}</span>}
              </button>
            );
          })()}
          <button className="avatar avmenu" onClick={() => setPop(pop === "profile" ? null : "profile")} title={profile + " · spaces, settings & more"}>
            {profile[0]}<span className="av-sp" style={{ background: tint }} />
          </button>
        </div>
      </div>
      )}

      <div className="mid">
        {tabPos === "left" && !hideBar && <div className={"vwrap" + (sideOpen ? "" : " closed")}><VTabs onCtx={openTabCtx} onDropRow={dropRow} tabs={tabs} active={active} onSelect={selectTab} onClose={closeTab} onAdd={addTab} groups={groups} onToggleGroup={(gid) => setGroups((gs) => ({ ...gs, [gid]: { ...gs[gid], collapsed: !gs[gid].collapsed } }))} /></div>}
        {(tabPos === "left" || tabPos === "right") && !hideBar && !sideOpen && (
          <button className={"siderail" + (tabPos === "right" ? " right" : "")} title="Show sidebar (⇧⌘S)" onClick={() => sideRef.current()}>
            {tabPos === "right" ? <PanelRight size={13} /> : <PanelLeft size={13} />}
          </button>
        )}
        <div className="main">

      {/* ===== bookmarks bar (off by default) ===== */}
      {bkbar && !hideBar && (
        <div className="bkbar">
          {marks.map((b, i) => (
            <button key={i} className="bk" onClick={() => navigate(b.u || b.name.toLowerCase().replace(/ /g, "") + ".com")}><Fav f={b} size={14} />{b.name}</button>
          ))}
        </div>
      )}

      {/* ===== viewport ===== */}
      <div className="view"
        onMouseOver={(e) => { const l = e.target.closest && e.target.closest("a[href], [data-url]"); setPeekUrl(l ? (l.dataset.url || l.getAttribute("href")) : null); }}
        onMouseLeave={() => setPeekUrl(null)}
        onContextMenu={(e) => {
        if (e.target.closest(".pop") || e.target.closest(".modal") || e.target.closest("input, textarea")) return;
        e.preventDefault();
        const nr = e.currentTarget.closest(".nova").getBoundingClientRect();
        const s = nr.width / DESIGN_W;
        setPageCtx({ x: (e.clientX - nr.left) / s, y: (e.clientY - nr.top) / s });
      }}>
        {view === "newtab" && (glance ? <SitePage key={"g" + glance.id} tab={glance} /> :
          isNT ? <NewTab heroFocus={heroFocus} setHeroFocus={setHeroFocus} dev={flags.devmode} onNavigate={navigate}
                   restore={lastSession && { n: lastSession.length, go: restoreSession, dismiss: () => setLastSession(null) }}
                   readList={reading.filter((r) => !r.read).map((r) => ({ t: r.title, u: r.url }))}
                   onOpenRead={(u) => { navigate(u); setReading((v) => v.map((r) => (r.url === u ? { ...r, read: true } : r))); }}
                   onDropRead={(u) => setReading((v) => v.filter((r) => r.url !== u))}
                   landing={landing} spaceName={space.name} onNote={note}
                   onDirty={(d) => { dirtyRef.current[active] = d; }} /> :
          splitId && tabs.find((x) => x.id === splitId) ? (
            <div className={"splitwrap" + (dragId ? " dragging" : "")}>
              <div className="pane" data-pane="0" style={{ flex: splitRatio }}>
                <div className="pane-h"><span className="pane-dom"><FavImg d={tab.url.split("/")[0]} size={13} /><span className="mono">{tab.url.split("/")[0]}</span></span>
                  <button className="ib" title="Close this pane" style={{ width: 22, height: 22 }} onClick={() => closeSplit("right")}><X size={12} /></button></div>
                <div className="pane-body">
                  <SitePage key={tab.id + tab.url} tab={tab} mem={scrollMem} reader={readerIds[tab.id]} zoom={(zoomMap[tab.url.split("/")[0]] || 1) * textScale} onDir={(h) => flags.autozen && !zen && setAutoHide(h)} />
                </div>
              </div>
              <div className="pane-divider" onPointerDown={startDivider}
                title="Drag to resize · double-click for 50/50 · ⌥⌘← ⌥⌘→" />
              <div className="pane side" data-pane="1" style={{ flex: 1 - splitRatio }}>
                <div className="pane-h"><span className="pane-dom"><FavImg d={tabs.find((x) => x.id === splitId).url.split("/")[0]} size={13} /><span className="mono">{tabs.find((x) => x.id === splitId).url.split("/")[0]}</span></span>
                  <button className="ib" title="Close this pane" style={{ width: 22, height: 22 }} onClick={() => closeSplit("left")}><X size={12} /></button></div>
                <div className="pane-body">
                  <SitePage key={"s" + splitId} tab={tabs.find((x) => x.id === splitId)} mem={scrollMem} zoom={textScale} />
                </div>
              </div>
            </div>
          ) :
          tab.status === "error" ? <ErrorPage key={"err" + tab.id} tab={tab} note={note} onRetry={() => { markLoading(tab.id); note("Retrying " + tab.url.split("/")[0] + "…"); }} onResources={() => goRef.current("resources")} /> :
          <SitePage key={tab.id + tab.url} tab={tab} mem={scrollMem} reader={readerIds[tab.id]} zoom={(zoomMap[tab.url.split("/")[0]] || 1) * textScale} onDir={(h) => flags.autozen && !zen && setAutoHide(h)} onAsk={setSelPill}
            boost={boosts[tab.url.split("/")[0]]} translated={translated[tab.id]} onShowOriginal={() => setTranslated((m) => ({ ...m, [tab.id]: false }))}
            onLittle={(u) => setLittle({ url: u })} />)}
        {view === "settings" && <SettingsPage sec={setSec} setSec={setSetSec} flags={flags} toggle={toggle} tabPos={tabPos} setTabPos={setTabPos} textScale={textScale} setTextScale={setTextScale} theme={theme} setTheme={setTheme}
          studio={{ themeId, applyPreset, customVars, setCustomVars, fontSans, setFontSans, fontMono, setFontMono, density, setDensity, radius, setRadius, note }} landing={landing} setLanding={setLanding}
          vault={vault} setVault={setVault} vaultLocked={vaultLocked} setVaultLocked={setVaultLocked} note={note} go={go}
          tabs={tabs} spaces={spaces} spaceId={spaceId} reading={reading} notesBySpace={notesBySpace} layouts={layouts} sched={sched} setSched={setSched}
          agentLog={agentLog} setAgentLog={setAgentLog} agentCaps={agentCaps} setAgentCaps={setAgentCaps}
          watches={watches} setWatches={setWatches} conns={conns} setConns={setConns} />}
        {view === "history" && <HistoryPage onDel={delHistory} note={note} />}
        {view === "agents" && (
          <AgentsPage sec={agentSec} setSec={setAgentSec} log={agentLog} setLog={setAgentLog}
            caps={agentCaps} setCaps={setAgentCaps} sched={sched} setSched={setSched}
            onRunSchedule={runSchedule} watches={watches} setWatches={setWatches}
            conns={conns} setConns={setConns} pending={approvals.length}
            onOpenQueue={() => setPop("approve")} note={note} />
        )}
        {view === "timemachine" && <TimeMachinePage note={note}
          onRestore={(s) => { note("Restored “" + s.ev + "” · " + s.tabs + " tabs — nothing replayed"); }}
          onFork={(s) => { addSpace(); note("Forked into a new project from " + s.t); }} />}
        {view === "resources" && <ResourcesPage note={note} />}
        {view === "agent" && <AgentPage tabs={tabs} note={note} onAgentTabs={setAgentOn} onOpenTab={agentOpen} />}
        {view === "canvas" && <CanvasPage tabs={tabs} note={note} />}
        {view === "migrate" && <MigrationPage note={note} />}
        {view === "extensions" && <ExtensionsPage note={note} />}
        {view === "downloads" && <DownloadsPage />}

        {/* popovers */}
        {pop && <div className="backdrop" onClick={() => setPop(null)} />}
        {pop === "boost" && (
          <div className="pop" style={{ top: 4, right: 10, width: 230 }}>
            <div className="pop-h"><div className="t">Boost · {tab.url.split("/")[0]}</div></div>
            <div style={{ padding: 12, display: "flex", gap: 9, alignItems: "center" }}>
              {[null, "#7b5cff", "#0ea5e9", "#f97316", "#16a34a", "#e11d48"].map((c) => (
                <button key={c || "none"} onClick={() => { setBoosts((b) => ({ ...b, [tab.url.split("/")[0]]: c })); setPop(null); }}
                  style={{ width: 26, height: 26, borderRadius: "var(--r)", background: c || "var(--c3)", display: "grid", placeItems: "center",
                    outline: (boosts[tab.url.split("/")[0]] || null) === c ? "2px solid var(--tx)" : "1px solid var(--line2)", outlineOffset: 2 }}>
                  {!c && <Ban size={12} color="var(--tx3)" />}
                </button>
              ))}
            </div>
            <div style={{ padding: "0 12px 12px", fontSize: 11, color: "var(--tx3)" }}>Tints every page on this site. Just for you.</div>
          </div>
        )}
        {pop === "profile" && (
          <div className="pop acct" style={{ top: 4, right: 10, maxHeight: 720, overflowY: "auto" }}>
            <div className="acct-id">
              <span className="avatar" style={{ width: 26, height: 26, fontSize: 11.5 }}>{profile[0]}</span>
              <div><div className="t">{profile}</div><div className="s">Turing account</div></div>
              <span style={{ marginLeft: "auto", display: "flex", gap: 5 }}>
                {["Byron", "Wade’s Plumbing", "Guest"].map((n) => (
                  <button key={n} className={"pf" + (profile === n ? " on" : "")} title={n} onClick={() => setProfile(n)}
                    style={{ background: n === "Guest" ? "var(--c4)" : "var(--ac)" }}>{n[0]}</button>
                ))}
              </span>
            </div>
            <div style={{ padding: 6 }}>
              {spaces.map((s) => (
                <button key={s.id} className="mitem" onClick={() => switchSpace(s.id)}>
                  <span className="spsq" style={{ background: s.tint, width: 15, height: 15, fontSize: 8.5 }}>{s.name[0]}</span>
                  {s.name}{s.id === spaceId && <Check size={13} color="var(--good)" style={{ marginLeft: "auto" }} />}
                </button>
              ))}
              <button className="mitem" onClick={addSpace}><Plus size={15} /> New space</button>
              <div className="msep" />
              <button className="mitem" onClick={() => go("history")}><HistoryIcon size={15} /> History <span className="r">⌘Y</span></button>
              <button className="mitem" onClick={() => go("downloads")}><Download size={15} /> Downloads <span className="r">⌘J</span></button>
              <button className="mitem" onClick={() => go("extensions")}><Puzzle size={15} /> Extensions</button>
              <div className="msep" />
              <button className="mitem" onClick={() => { setZen(true); setPop(null); }}><Eye size={15} /> Zen mode <span className="r">⌘⏎</span></button>
              <button className="mitem" onClick={() => { setBkbar((v) => !v); setPop(null); }}><Star size={15} /> Bookmarks bar <span className="r">⇧⌘B</span></button>
              <div className="msep" />
              <button className="mitem" onClick={() => { setPop(null); setInspector(true); }}><SlidersHorizontal size={15} /> Project details…</button>
              <button className="mitem" onClick={() => go("settings", "general")}><Settings size={15} /> Settings <span className="r">⌘,</span></button>
              <button className="mitem" onClick={() => { setPop(null); setShortcuts(true); }}><Command size={15} /> Keyboard shortcuts <span className="r">⌘/</span></button>
            </div>
          </div>
        )}
        {pop === "security" && <SecurityPop flags={flags} go={go} domain={tab.url.split("/")[0]} perms={perms} setPerm={setPerm}
          onReceipt={() => setPop("receipt")} />}
        {pop === "receipt" && <ReceiptPop domain={tab.url.split("/")[0]} close={() => setPop(null)} />}
        {inspector && <SpaceInspector space={{ name: space.name, tint }} tabsN={tabs.length} close={() => setInspector(false)}
          onShare={() => { setInspector(false); setShare(true); }}
          onTimeMachine={() => { setInspector(false); go("timemachine"); }}
          onExport={() => note("Project exported — open .turing bundle")} />}
        {share && <ShareSheet space={{ name: space.name }} close={() => setShare(false)} note={note} />}
        {findOpen && <FindBar onClose={() => setFindOpen(false)} note={note} />}
        {side && (
          <SidePanel kind={side} onClose={() => setSide(null)} reading={reading} setReading={setReading}
            notes={notesBySpace[spaceId] || ""} setNotes={(v) => setNotesBySpace((m) => ({ ...m, [spaceId]: v }))}
            spaceName={(spaces.find((x) => x.id === spaceId) || {}).name || spaceId}
            onOpen={(u) => { openInNew(u); setSide(null); }} note={note} />
        )}
        {capture && <CapturePop dom={tab.url.split("/")[0]} onClose={() => setCapture(false)} note={note} />}
        {focusOpen && <FocusPanel mins={foMins} setMins={setFoMins} running={foRun} setRunning={setFoRun}
          left={foLeft} goal={foGoal} setGoal={setFoGoal} onClose={() => setFocusOpen(false)} note={note} />}
        {pop === "approve" && (
          <ApprovalPop items={approvals} onClose={() => setPop(null)} go={go}
            onDecide={(a, ok) => {
              setApprovals((v) => v.filter((x) => x.id !== a.id));
              setAgentLog((v) => [{
                id: Date.now(), t: "just now", agent: a.agent, verb: ok ? a.verb + "ed" : "Blocked",
                target: a.target, site: a.site, status: ok ? "applied" : "blocked",
                detail: ok ? "You approved this once. It ran immediately and can still be undone."
                           : "You denied this. The agent stopped and will not retry without asking.",
                diff: ok ? a.diff : [],
              }, ...v]);
              note(ok ? "Approved — " + a.verb.toLowerCase() + " " + a.target : "Denied — nothing happened",
                [{ label: "See log", fn: () => go("agents", "activity") }]);
            }} />
        )}
        {pop === "site" && (() => {
          const dm = tab.url.split("/")[0];
          return <SiteControls dom={dm} zoom={zoomMap[dm] || 1} setZoom={(z) => setZoomMap((m) => ({ ...m, [dm]: z }))}
            perms={sitePerms} setPerms={setSitePerms} level={shieldSites[dm] || "standard"}
            setLevel={(v) => { setShieldSites((m) => ({ ...m, [dm]: v })); setPop(null); note("Shield " + v + " on " + dm); }}
            onClose={() => setPop(null)} note={note} go={go} />;
        })()}
        {taskm && <TaskManager tabs={tabs} onClose={() => setTaskm(false)} note={note}
          onMergeDup={(urls) => {
            const seen = {};
            const keep = tabs.filter((t) => {
              if (!urls.includes(t.url)) return true;
              if (seen[t.url]) return false;
              seen[t.url] = t.id; return true;
            });
            const removed = tabs.length - keep.length;
            if (!keep.some((t) => t.id === active)) {
              const dead = tabs.find((t) => t.id === active);
              if (dead && seen[dead.url]) setActive(seen[dead.url]);
            }
            setTabs(keep);
            note("Merged duplicates — " + removed + " tab" + (removed === 1 ? "" : "s") + " closed");
          }}
          onSleep={(id) => { setTabs((ts) => ts.map((t) => (t.id === id ? { ...t, asleep: !t.asleep } : t))); note("Tab slept — memory released"); }}
          onClose1={(id) => { closeTab(id); }} />}
        {hints && <HintLayer onDone={() => setHints(false)} note={note} />}
        {tabSearch && (
          <TabSearch tabs={tabs} spaceId={spaceId} spaces={spaces} spaceStore={spaceStore}
            onClose={() => setTabSearch(false)}
            onPick={(r) => {
              setTabSearch(false);
              if (r.space !== spaceId) { switchSpace(r.space); setTimeout(() => setActive(r.t.id), 60); note("Jumped to " + (r.t.label || r.t.url) + " in another space"); }
              else { setActive(r.t.id); setView("newtab"); }
            }} />
        )}
        {pop === "vault" && (() => {
          const dm = tab.url.split("/")[0];
          return <VaultPop vault={vault} locked={vaultLocked} setLocked={setVaultLocked} dom={dm} note={note} go={go}
            onFill={(e) => { setPop(null); note("Filled " + e.user + " on " + dm, [{ label: "Undo", fn: () => note("Cleared") }]); }} />;
        })()}
        {pop === "shield" && (() => {
          const dm = tab.url.split("/")[0];
          return <ShieldPop flags={flags} toggle={toggle} go={go} dom={dm}
            level={shieldSites[dm] || "standard"}
            setLevel={(v) => { setShieldSites((m) => ({ ...m, [dm]: v })); note("Shield · " + v + " on " + dm); }}
            weekTotal={12480 + (hashStr(spaceId) % 900)} />;
        })()}

        {pop === "trail" && <TrailPop hist={hist} jump={(i) => { setHist((h) => { const e = h.stack[i]; setActive(e.t); setView(e.v); if (e.url) setTabs((ts) => ts.map((x) => x.id === e.t ? { ...x, url: e.url, title: e.title } : x)); return { ...h, i }; }); setPop(null); sweep(); }} />}

        {/* command palette */}
        {cmd && <CommandPalette q={cmdQ} setQ={setCmdQ} sel={cmdSel} setSel={setCmdSel} close={() => setCmd(false)} go={go} dev={flags.devmode}
          tabs={tabs} activeId={active} onSwitchTab={(id) => { const t = tabs.find((x) => x.id === id); if (t) selectTab(t); setCmd(false); }}
          closed={closedRef.current} onReopenAt={reopenAt}
          onHints={() => setHints(true)} onTabSearch={() => setTabSearch(true)} onSide={(k) => setSide(k)}
          onTaskm={() => setTaskm(true)} onCapture={() => setCapture(true)} onFocus={() => setFocusOpen(true)}
          onSiteCtl={() => setPop("site")} onApprovals={() => setPop("approve")}
          onCopy={copyUrl} onReader={toggleReader} onFind={() => setFindOpen(true)} onSplit={() => toggleSplit()}
          onOpenNew={openInNew} onCloseTab={(id) => closeTab(id)} onNewTab={() => { addTab(); setCmd(false); }} shieldOn={flags.adblock}
          onTheme={toggleTheme} onMark={toggleBookmark} onAI={() => askTuring()} onOrganize={organizeTabs} onTranslate={translatePage} onSpace={() => { const i = spaces.findIndex((s) => s.id === spaceId); switchSpace(spaces[(i + 1) % spaces.length].id); }} onLater={() => saveForLater()} onBoost={boostSite} onLittleWin={() => setLittle({ url: "thorbis.com/notes/scratch" })} onInspector={() => setInspector(true)}
          onNavigate={navigate} onSession={resumeSession} onZenTimer={zenTimer}
          onZen={() => { setZen((v) => !v); setCmd(false); }} onTidy={() => { tidyTabs(); setCmd(false); }}
          layouts={layouts[spaceId] || []} splitOpen={splitId != null} onSaveLayout={saveLayout} onApplyLayout={applyLayout} onForgetLayout={forgetLayout}
          openDock={(t) => { setDock(true); setDockTab(t); setCmd(false); }} openShortcuts={() => { setShortcuts(true); setCmd(false); }} />}
      </div>

      {confirmClose && (
        <div className="modalveil" onClick={() => setConfirmClose(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="mt">Close {tabs.length} tabs?</div>
            <div className="md">Turing will remember them — you can restore this session from the new tab page.</div>
            <div className="mrow" style={{ justifyContent: "flex-end", gap: 8 }}>
              <button className="hclear" onClick={() => setConfirmClose(false)}>Cancel <span className="kbd">ESC</span></button>
              <button className="btn-pri" onClick={closeAllTabs}>Close all <span className="kbd">↵</span></button>
            </div>
          </div>
        </div>
      )}
      {zen && zenHint && <div className="toast">Zen — move to the top edge for the bar · Esc to exit</div>}
      {flags.readOrder && view === "newtab" && !isNT && (
        <div className="a11y-order mono">
          {["1 nav", "2 heading", "3 article", "4 aside", "5 actions"].map((t) => <span key={t}>{t}</span>)}
          <i>reading order — as assistive tech will speak it</i>
        </div>
      )}
      {dragId && (
        <div className="dragproxy" ref={proxyRef} aria-hidden>
          <i className="tseg-d" style={{ background: dragS.current?.gcol || "var(--c4)" }} />
          <span>{dragS.current?.label}</span>
        </div>
      )}
      {dragId && spaces.length > 1 && (
        <div className="dropspaces">
          <span className="ds-l">Move to</span>
          {spaces.filter((s) => s.id !== spaceId).map((s) => (
            <span key={s.id} className="dropsp" data-sp={s.id}><span className="spdot" style={{ background: s.tint }} />{s.name}</span>
          ))}
        </div>
      )}
      {little && (
        <div className="little">
          <div className="little-h">
            <span className="spdot" style={{ background: "var(--ac)" }} />
            <span className="u">{little.url}</span>
            <button className="lb" onClick={() => { openInNew(little.url); setLittle(null); }}>Move to tabs</button>
            <button className="ib" title="Dismiss" style={{ width: 24, height: 24 }} onClick={() => setLittle(null)}><X size={13} /></button>
          </div>
          <SitePage key={"lil" + little.url} tab={{ id: "lil", url: little.url, title: little.url }} zoom={0.85} />
        </div>
      )}
      {selPill && (
        <button className="askpill" style={{ left: selPill.x, top: selPill.y }}
          onMouseDown={(e) => e.preventDefault()}
          onClick={() => askTuring(selPill.text)}>
          <Sparkles size={11} /> Ask Turing
        </button>
      )}
      {(() => { const at = tabs.find((t) => t.audio === "on"); return at && (
        <div className="pip">
          <span className="eq"><i /><i /><i /></span>
          <span className="pt">{(at.label || at.title).slice(0, 26)}</span>
          <button className="ib" style={{ width: 22, height: 22 }} title="Mute"
            onClick={() => setTabs((ts) => ts.map((x) => x.id === at.id ? { ...x, audio: "muted" } : x))}><VolumeX size={12} /></button>
        </div>
      ); })()}
      {notice && <div className="toast act">{notice.msg}{(notice.actions || []).map((a) => <button key={a.label} className="undo" onClick={a.fn}>{a.label}</button>)}</div>}
      {ctx && (() => { const t = tabs.find((x) => x.id === ctx.id); if (!t) return null;
        const W = 236, H = 12 + 34 * 2 + 30 * (10 + Object.keys(groups).length);
        const mx = Math.min(ctx.x, DESIGN_W - W - 10), my = Math.min(ctx.y, DESIGN_H - Math.min(H, 520) - 10);
        return (
        <>
          <div className="backdrop" style={{ position: "absolute", zIndex: 74 }} onClick={() => setCtx(null)} onContextMenu={(e) => { e.preventDefault(); setCtx(null); }} />
          <div className="pop dense" style={{ top: my, left: mx, width: W, zIndex: 75, maxHeight: 520, overflowY: "auto" }}>
            <div style={{ padding: 5 }}>
              <button className="mitem" onClick={() => { markLoading(t.id); note("Reloading " + (t.label || t.title) + "…"); setCtx(null); }}><RotateCw size={14} /> Reload <span className="r">⌘R</span></button>
              <button className="mitem" onClick={() => duplicateTab(t.id)}><Copy size={14} /> Duplicate</button>
              <button className="mitem" onClick={() => { togglePin(t.id); setCtx(null); }}><Pin size={14} /> {t.pin ? "Unpin tab" : "Pin tab"}</button>
              <button className="mitem" onClick={() => { setTabs((ts) => ts.map((x) => x.id === t.id ? { ...x, audio: x.audio === "muted" ? "on" : "muted" } : x)); note(t.audio === "muted" ? "Unmuted" : "Muted"); setCtx(null); }}><Volume2 size={14} /> {t.audio === "muted" ? "Unmute tab" : t.audio ? "Mute tab" : "Mute tab"}</button>
              <div className="msep" />
              <button className="mitem" onClick={() => { setRenameId(t.id); setCtx(null); }}><Sparkles size={14} /> Rename…</button>
              <button className="mitem" onClick={() => saveForLater(t.id)}><BookOpen size={14} /> Save for later</button>
              {t.id !== active && <button className="mitem" onClick={() => { setLittle({ url: t.url }); setCtx(null); }}><Columns2 size={14} /> Peek in Mini</button>}
              {t.id !== active && <button className="mitem" onClick={() => toggleSplit(t.id)}><Columns2 size={14} /> Split with this tab</button>}
              <div className="msep" />
              {!t.group ? (
                <button className="mitem" onClick={() => groupTab(t.id)}><LayoutGrid size={14} /> New group with this tab</button>
              ) : (
                <button className="mitem" onClick={() => { setTabs((ts) => ts.map((x) => x.id === t.id ? { ...x, group: undefined } : x)); setCtx(null); }}><LayoutGrid size={14} /> Remove from group</button>
              )}
              {!t.group && Object.entries(groups).slice(0, 3).map(([gid, g]) => (
                <button key={gid} className="mitem" onClick={() => { setTabs((ts) => ts.map((x) => x.id === t.id ? { ...x, group: gid } : x)); setCtx(null); }}>
                  <span style={{ width: 14, display: "grid", placeItems: "center" }}><span style={{ width: 8, height: 8, borderRadius: 4, background: g.color }} /></span> Add to “{g.name}”
                </button>
              ))}
              {spaces.filter((s) => s.id !== spaceId).map((s) => (
                <button key={s.id} className="mitem" onClick={() => { moveTabToSpaceRef.current(t.id, s.id); setCtx(null); }}>
                  <span style={{ width: 14, display: "grid", placeItems: "center" }}><span style={{ width: 8, height: 8, borderRadius: 4, background: s.tint }} /></span> Move to {s.name}
                </button>
              ))}
              <div className="msep" />
              <button className="mitem" onClick={(e) => { closeTab(t.id, e); setCtx(null); }} style={t.pin ? { opacity: .45 } : null}><X size={14} /> Close tab {!t.pin && <span className="r">⌘W</span>}</button>
              <button className="mitem" onClick={() => {
                const keep = t.id; const prev = tabs;
                const victims = tabs.filter((x) => x.id !== keep && !x.pin);
                setTabs((ts) => ts.filter((x) => x.id === keep || x.pin));
                if (active !== keep) selectTab(t);
                note("Closed " + victims.length + " tabs", [{ label: "Undo", fn: () => { setTabs(prev); setNotice(null); } }]);
                setCtx(null);
              }}><X size={14} /> Close other tabs</button>
            </div>
          </div>
        </>
      ); })()}

      {pageCtx && (() => {
        const W = 232, H = 380;
        const mx = Math.min(pageCtx.x, DESIGN_W - W - 10), my = Math.min(pageCtx.y, DESIGN_H - H - 10);
        return (
        <>
          <div className="backdrop" style={{ position: "absolute", zIndex: 74 }} onClick={() => setPageCtx(null)} onContextMenu={(e) => { e.preventDefault(); setPageCtx(null); }} />
          <div className="pop dense" style={{ top: my, left: mx, width: W, zIndex: 75 }}>
            <div style={{ padding: 5 }}>
              <button className="mitem" disabled={!canBack} style={!canBack ? { opacity: .4 } : null} onClick={() => { canBack && goHist(-1); setPageCtx(null); }}><ArrowLeft size={14} /> Back <span className="r">⌘[</span></button>
              <button className="mitem" disabled={!canFwd} style={!canFwd ? { opacity: .4 } : null} onClick={() => { canFwd && goHist(1); setPageCtx(null); }}><ArrowRight size={14} /> Forward <span className="r">⌘]</span></button>
              <button className="mitem" onClick={() => { markLoading(active); note("Reloading…"); setPageCtx(null); }}><RotateCw size={14} /> Reload <span className="r">⌘R</span></button>
              <div className="msep" />
              <button className="mitem" onClick={() => { note("Saved page to Downloads"); setPageCtx(null); }}><Download size={14} /> Save page as…</button>
              <button className="mitem" onClick={() => { note("Print dialog — concept"); setPageCtx(null); }}><FileText size={14} /> Print…</button>
              <button className="mitem" onClick={() => { note("URL copied"); setPageCtx(null); }}><Copy size={14} /> Copy page URL <span className="r">⇧⌘C</span></button>
              <div className="msep" />
              <button className="mitem" onClick={() => { setAi(true); setPageCtx(null); }}><Sparkles size={14} /> Ask Turing about this page <span className="r">⌘E</span></button>
              <button className="mitem" onClick={() => { translatePage(); setPageCtx(null); }}><Globe size={14} /> Translate page</button>
              <button className="mitem" onClick={() => { setPageCtx(null); setPop("boost"); }}><Palette size={14} /> Boost this site…</button>
              {flags.devmode && <><div className="msep" />
              <button className="mitem" onClick={() => { setDock(true); setDockTab("sources"); setPageCtx(null); }}><FileText size={14} /> View page source</button>
              <button className="mitem" onClick={() => { setDock(true); setDockTab("elements"); setPageCtx(null); }}><Search size={14} /> Inspect <span className="r">⌥⌘I</span></button></>}
            </div>
          </div>
        </>
      ); })()}
      {peekUrl && <div className="urlpeek mono">{peekUrl}</div>}
      {dock && flags.devmode && <InspectorDock tab={dockTab} setTab={setDockTab} close={() => setDock(false)} />}
        </div>
        {tabPos === "right" && !hideBar && <div className={"vwrap right" + (sideOpen ? "" : " closed")}><VTabs right onCtx={openTabCtx} onDropRow={dropRow} tabs={tabs} active={active} onSelect={selectTab} onClose={closeTab} onAdd={addTab} groups={groups} onToggleGroup={(gid) => setGroups((gs) => ({ ...gs, [gid]: { ...gs[gid], collapsed: !gs[gid].collapsed } }))} /></div>}
        {ai && <AskNova tabs={tabs} activeTab={tab} msgs={aiMsgs} setMsgs={setAiMsgs} close={() => setAi(false)} onOpen={(u) => navigate(u)}
          onOpenNew={openInNew} threads={aiThreads} setThreads={setAiThreads} note={note}
          onAgent={() => { setAi(false); go("agent"); note("Handed to Agent Mode — dry-run first"); }} />}
      </div>

      {tabPos === "bottom" && !hideBar && (
        <div className="bar bottom">
          <div className="ttabs">
            {tabs.map((t) => (
              <div key={t.id} className={"ttab" + (t.id === active ? " on" : "") + (t.pin ? " pinned" : "") + (t.status === "error" ? " err" : "")} onClick={() => selectTab(t)} title={t.title}>
                <span className="tst" aria-hidden>
                  {t.status === "loading" ? <i className="tspin" />
                  : t.status === "error" ? <i className="terr" />
                  : t.pin ? <Pin size={10} color="var(--tx3)" />
                  : t.audio === "muted" ? <VolumeX size={11} color="var(--tx3)" />
                  : t.audio ? <Volume2 size={11} color="var(--ac)" />
                  : <FavImg d={t.url.split("/")[0]} />}
                </span>
                <span className="ttl">{t.title}</span>
                <button className="xc" onClick={(e) => closeTab(t.id, e)} aria-label="Close tab"><X size={12} /></button>
              </div>
            ))}
            <div className="dropcue" ref={cueRef} aria-hidden />
            {hidTabs.length > 0 && (
              <button className="ovf" onClick={() => setTabSearch(true)} title={hidTabs.length + " more tabs · ⇧⌘A"}>
                <ChevronDown size={13} /><span className="mono">{hidTabs.length}</span>
              </button>
            )}
            <button className="newtab" onClick={addTab} aria-label="New tab"><Plus size={15} /></button>
          </div>
        </div>
      )}

      {shortcuts && <ShortcutsOverlay close={() => setShortcuts(false)} />}
          </div>
        </div>
        {present && <button className="zexit" onClick={() => setPresent(false)}>Exit presentation · ⌘.</button>}
      </div>
    </div>
  );
}

/* ---------- mock web pages ---------- */
const Skl = ({ w, h = 8, dim, mb = 0 }) => <div className={"skl" + (dim ? " dim" : "")} style={{ width: w, height: h, marginBottom: mb }} />;

const BRANDS = {
  "vercel.com": { n: "Vercel", c: "#111114", h1: "Develop. Preview. Ship.", sub: "The frontend cloud. Build, scale, and secure the best web experiences with your team." },
  "figma.com": { n: "Figma", c: "#0055ff", h1: "How teams design together", sub: "Design, prototype, and ship products in one shared space — from first idea to final handoff." },
  "notion.com": { n: "Notion", c: "#16161a", h1: "One workspace. Every team.", sub: "Write, plan, and organize in a tool that shapes itself to how your team actually works." },
  "raycast.com": { n: "Raycast", c: "#ff4f00", h1: "Your shortcut to everything", sub: "A blazingly fast launcher — scripts, windows, clipboard, and AI, one keystroke away." },
  "discord.com": { n: "Discord", c: "#5865f2", h1: "Where communities live", sub: "Voice, video, and text for the people who build things together." },
  "alltrails.com": { n: "AllTrails", c: "#2f7d3b", h1: "Find your next trail", sub: "Over 450,000 curated trail maps with reviews, photos, and conditions from hikers like you." },
  "ramp.com": { n: "Ramp", c: "#7a9a01", h1: "Spend less. Close faster.", sub: "Corporate cards, bill pay, and accounting automation that pays for itself." },
  "supabase.com": { n: "Supabase", c: "#2fa572", h1: "Build in a weekend. Scale to millions.", sub: "The open-source Postgres platform — auth, storage, realtime, and vectors included." },
  "tailwindcss.com": { n: "Tailwind CSS", c: "#0ea5e9", h1: "Rapidly build modern websites", sub: "A utility-first CSS framework packed with classes that compose into any design." },
  "motion.dev": { n: "Motion", c: "#0099ff", h1: "A production-grade animation library", sub: "Springs, gestures, and layout animations for React — 120fps by default." },
  "developer.mozilla.org": { n: "MDN", c: "#1b1b1f", h1: "Resources for developers, by developers", sub: "Documenting the web platform — HTML, CSS, JavaScript, and everything between." },
  "news.ycombinator.com": { n: "Hacker News", c: "#ff6600", h1: "News for builders", sub: "Stories that gratify intellectual curiosity — startups, systems, and strange rabbit holes." },
  "stripe.com": { n: "Stripe", c: "#635bff" }, "linear.app": { n: "Linear", c: "#5e6ad2" },
  "mercury.com": { n: "Mercury", c: "#5b3df5" }, "github.com": { n: "GitHub", c: "#1f883d" },
  "v0.app": { n: "v0", c: "#111114" }, "youtube.com": { n: "YouTube", c: "#ff0000" },
};
function siteBrand(d) {
  if (BRANDS[d]) return BRANDS[d];
  let h = 0; for (let i = 0; i < d.length; i++) h = (h * 31 + d.charCodeAt(i)) % 360;
  const raw = d.split(".")[0].replace(/-/g, " ");
  return { n: raw.charAt(0).toUpperCase() + raw.slice(1), c: "hsl(" + h + ",58%,42%)" };
}
const LIVE_HOSTS = { "wikipedia.org": 1, "en.wikipedia.org": 1, "www.wikipedia.org": 1, "example.com": 1 };
function liveSrc(url) {
  const d = url.split("/")[0];
  if (LIVE_HOSTS[d]) {
    const path = url.slice(d.length);
    const host = d === "wikipedia.org" ? "en.wikipedia.org" : d;
    return "https://" + host + (path || (host === "en.wikipedia.org" ? "/wiki/Web_browser" : "/"));
  }
  if (d.includes("youtube.com")) {
    const m = url.match(/[?&]v=([A-Za-z0-9_-]{11})/);
    if (m) return "https://www.youtube-nocookie.com/embed/" + m[1] + "?autoplay=0";
  }
  return null;
}
const FICTIONAL = { "turing.app": 1, "docs.turing.app": 1 };
// Off by default: thum.io renders pages server-side and can take tens of seconds,
// and a sandboxed frame may never resolve the request at all. The designed mocks
// are the better render anyway. Flip to true only for a live-capture shoot.
const LIVE_SNAPSHOTS = false;
// Favicons are small and fail fast, so they stay on. Set to false for a fully
// offline shell (tabs fall back to the lettered brand tiles).
const REMOTE_FAVICONS = true;
function shotSrc(url) {
  if (!LIVE_SNAPSHOTS) return null;
  const d = url.split("/")[0];
  if (!d.includes(".") || FICTIONAL[d] || d.includes("localhost") || d.endsWith(".local")) return null;
  if (LIVE_HOSTS[d] || d.includes("youtube.com")) return null;
  const isSearch = d.includes("google.") && url.includes("/search");
  const target = "https://" + (isSearch ? url : d);
  return "https://image.thum.io/get/fullpage/width/1440/" + target;
}
const ESSAY = "The best interface is the one you stop noticing. Every pixel of chrome is a small tax on attention, and the browsers we love most are the ones that learned to disappear when the page deserves the room.";

const SitePage = memo(function SitePage({ tab, onDir, mem, reader, zoom = 1, onAsk, boost, translated, onShowOriginal, onLittle }) {
  const d = tab.url.split("/")[0];
  const brand = siteBrand(d);
  const live = liveSrc(tab.url);
  const snap = liveSrc(tab.url) ? null : shotSrc(tab.url);
  const [lo, setLo] = useState(false);
  useEffect(() => { setLo(false); }, [live]);
  const [shot, setShot] = useState({ st: "load", n: 0 });
  useEffect(() => { setShot({ st: "load", n: 0 }); }, [snap]);
  const [hoverLink, setHoverLink] = useState(null);
  const lastY = useRef(0);
  const ref = useRef(null);
  useEffect(() => {
    if (ref.current && mem && mem.current[tab.id]) {
      ref.current.scrollTop = mem.current[tab.id];
      lastY.current = mem.current[tab.id];
    }
  }, []);
  const onScroll = (e) => {
    const y = e.target.scrollTop;
    if (mem) mem.current[tab.id] = y;
    if (!onDir) return;
    const dy = y - lastY.current;
    lastY.current = y;
    if (y > 70 && dy > 5) onDir(true);
    else if (dy < -5 || y < 24) onDir(false);
  };
  const hov = (u) => ({
    onMouseEnter: () => setHoverLink("https://" + u),
    onMouseLeave: () => setHoverLink(null),
    onClick: () => onLittle && onLittle(u),
  });
  const Ava = ({ t, c }) => <span className="ava" style={{ background: c }}>{t}</span>;

  if (reader) return (
    <div className="scroll" ref={ref} onScroll={onScroll}>
      <div className="wp reader" style={{ minHeight: "140%", zoom }}>
        <div className="rd">
          <div className="rd-k">{d} · reader</div>
          <h1>The interface you stop noticing</h1>
          <div className="by">Nova Journal · 6 min read</div>
          <p>{ESSAY}</p>
          <p>Attention is the only budget that never refills. Every toolbar, every badge, every persistent panel spends a little of it — and the spend compounds. A browser that respects the reader treats its own chrome as debt: taken on deliberately, paid down constantly.</p>
          <p>The counterargument writes itself: hide the affordances and you hide the power. But the answer is not more surface — it is better timing. Controls that arrive when reached for, and leave when the page deserves the room.</p>
          <p>That is the whole thesis. Not minimalism as aesthetic, but restraint as engineering — measured in frames, in milliseconds, in the moment you forget you are using a browser at all.</p>
        </div>
      </div>
    </div>
  );

  if (live && !reader) return (
    <div className="scroll" style={{ overflow: "hidden" }}>
      <div className={"wp" + (boost ? " boost" : "")} style={{ height: "100%", display: "flex", flexDirection: "column", "--bc": boost || brand.c, boxShadow: boost ? "inset 0 3px 0 " + boost : undefined }}>
        {translated && (
          <div className="trbar"><Globe size={12} /> Translated to English<button onClick={onShowOriginal}>Show original</button></div>
        )}
        <div className="live-wrap">
          {!lo && <div className="live-load"><i className="tspin" /> Loading live page — {d}</div>}
          <iframe className="live-fr" key={live} src={live} title={d} onLoad={() => setLo(true)}
            sandbox="allow-scripts allow-same-origin allow-popups allow-forms" referrerPolicy="no-referrer" />
          <span className="live-tag">LIVE</span>
        </div>
      </div>
    </div>
  );

  if (snap && !reader && shot.st !== "err") return (
    <div className="scroll" ref={ref} onScroll={onScroll}>
      <div className={"wp" + (boost ? " boost" : "")} style={{ minHeight: "100%", display: "block", position: "relative", "--bc": boost || brand.c, boxShadow: boost ? "inset 0 3px 0 " + boost : undefined }}>
        {translated && (
          <div className="trbar"><Globe size={12} /> Translated to English<button onClick={onShowOriginal}>Show original</button></div>
        )}
        {shot.st === "load" && (
          <div className="shot-load">
            <div className="sk-nav"><span className="sk-b" style={{ width: 26, height: 26 }} /><span className="sk-b" style={{ width: 60, height: 10 }} /><span className="sk-b" style={{ width: 48, height: 10 }} /><span className="sk-b" style={{ width: 54, height: 10 }} /><span className="sk-b" style={{ marginLeft: "auto", width: 92, height: 30 }} /></div>
            <div style={{ maxWidth: 880, margin: "64px auto 0", padding: "0 36px" }}>
              <span className="sk-b" style={{ display: "block", width: "58%", height: 38, marginBottom: 16 }} />
              <span className="sk-b" style={{ display: "block", width: "40%", height: 14, marginBottom: 34 }} />
              <span className="sk-b" style={{ display: "block", width: "100%", height: 300, borderRadius: 14 }} />
            </div>
            <div className="sk-cap mono">rendering live snapshot · {d}</div>
          </div>
        )}
        <img className="shot-img" key={snap + shot.n} src={snap} alt={d} style={{ zoom, opacity: shot.st === "ok" ? 1 : 0 }}
          onLoad={(e) => { const w = e.target.naturalWidth; if (w < 600 && shot.n < 2) setTimeout(() => setShot((s) => ({ st: "load", n: s.n + 1 })), 2200); else setShot((s) => ({ ...s, st: "ok" })); }}
          onError={() => setShot((s) => s.n < 2 ? { st: "load", n: s.n + 1 } : { ...s, st: "err" })} />
      </div>
    </div>
  );

  let body;
  if (d.includes("google.") && tab.url.includes("/search")) {
    const q = decodeURIComponent((tab.url.split("q=")[1] || "").split("&")[0]).replace(/\+/g, " ") || "search";
    body = (<>
      <div className="sm-nav"><span className="sm-mark"><span className="sm-dot" style={{ "--bc": "#4285f4" }}>G</span></span>
        <span className="sm-ghost" style={{ flex: "0 1 460px", justifyContent: "flex-start", color: "#33343c", borderRadius: 999 }}><Search size={13} style={{ marginRight: 8, opacity: .5 }} />{q}</span>
      </div>
      <div className="sm-wrap" style={{ maxWidth: 760, margin: 0, paddingTop: 10 }}>
        <div style={{ fontSize: 11.5, color: "#8b8fa0", padding: "8px 0" }}>About 2,140,000 results (0.31 seconds)</div>
        {[["turing.app", "Turing — the open project browser", "Projects instead of tabs, a Time Machine for every workspace state, and agents that carry typed powers only. Import from any browser in one step."],
          ["en.wikipedia.org", q.charAt(0).toUpperCase() + q.slice(1) + " — Wikipedia", "Overview, history, and technical background. Includes references, related concepts, and further reading curated by contributors."],
          ["news.ycombinator.com", q + " | Hacker News", "247 points · 118 comments — practitioners debate trade-offs, share benchmarks, and link three follow-up write-ups worth the click."],
          ["docs.turing.app", q + " — official documentation", "Step-by-step guides with worked examples, an API reference, and migration notes for teams switching mid-project."]].map(([u, t, ds]) => (
          <div key={u} className="se-r" {...hov(u)}>
            <div className="se-u"><span className="sm-dot" style={{ width: 16, height: 16, fontSize: 8, "--bc": "#e8e9ef", color: "#5a5e6a" }}>{u[0].toUpperCase()}</span>{u}</div>
            <div className="se-t">{t}</div><div className="se-d">{ds}</div>
          </div>
        ))}
      </div>
    </>);
  } else if (d.includes("linear")) {
    const ISS = [
      ["!", "NOV-142", "Tab strip drops frames during group drag", "Bug", "#e5484d", "#f5a623", "EK", "#5e6ad2", "2d"],
      ["▲", "NOV-139", "Shield: allowlist import silently skips comments", "Bug", "#e5484d", "#c9cdd6", "BW", "#0f9955", "2d"],
      ["▲", "NOV-137", "Palette ranks recent tabs below fuzzy matches", "UX", "#5e6ad2", "#f5a623", "MR", "#f45d48", "3d"],
      ["–", "NOV-134", "Reader mode: widow lines on pull quotes", "Polish", "#8f95a3", "#c9cdd6", "EK", "#5e6ad2", "4d"],
      ["▲", "NOV-131", "Freeze explainer shows stale memory savings", "Perf", "#f5a623", "#5e6ad2", "BW", "#0f9955", "5d"],
      ["–", "NOV-129", "Migration report: Arc split layouts approximate", "Import", "#0f9955", "#0f9955", "MR", "#f45d48", "6d"],
      ["!", "NOV-127", "Agent dry-run misses credential-handle step", "Agent", "#7c5cff", "#f5a623", "EK", "#5e6ad2", "1w"],
      ["–", "NOV-124", "Time Machine diff misorders folder moves", "Bug", "#e5484d", "#c9cdd6", "AS", "#7c5cff", "1w"],
      ["▲", "NOV-121", "New tab ticker jumps under reduced motion", "A11y", "#0f9955", "#0f9955", "BW", "#0f9955", "1w"],
      ["–", "NOV-118", "Split view: divider hit area too narrow", "UX", "#5e6ad2", "#5e6ad2", "AS", "#7c5cff", "2w"],
    ];
    body = (
      <div className="ap-shell">
        <div className="ap-side">
          <div className="ap-item" style={{ fontWeight: 600, color: "#17181d" }}><span className="sm-dot" style={{ width: 16, height: 16, fontSize: 8, "--bc": brand.c }}>N</span> Nova</div>
          <div className="ap-sec">Workspace</div>
          <div className="ap-item">Inbox <span className="n">3</span></div>
          <div className="ap-item">My Issues <span className="n">12</span></div>
          <div className="ap-item">Views</div>
          <div className="ap-sec">Projects</div>
          <div className="ap-item on"><i className="gdot" style={{ background: "#5e6ad2" }} /> Nova Shell</div>
          <div className="ap-item"><i className="gdot" style={{ background: "#f5a623" }} /> Telemetry</div>
          <div className="ap-item"><i className="gdot" style={{ background: "#0f9955" }} /> Q3 Invoicing</div>
        </div>
        <div className="ap-main">
          <div className="ap-head"><span className="ap-title">Nova Shell — Active issues</span>
            <span className="ap-chip on">All</span><span className="ap-chip">Assigned</span><span className="ap-chip">Board</span>
            <span className="ap-chip" style={{ marginLeft: "auto" }}>Filter</span>
          </div>
          <div>
            {ISS.map(([pr, id, t, lb, lc, sc, av, ac, tm]) => (
              <div key={id} className="iss-row" {...hov(d + "/issue/" + id.toLowerCase())}>
                <span className="iss-pri" style={{ color: pr === "!" ? "#e5484d" : "#8f95a3" }}>{pr}</span>
                <span className="iss-id">{id}</span>
                <span className="iss-t">{t}</span>
                <span className="lb" style={{ color: lc, background: "color-mix(in srgb," + lc + " 10%,#fff)" }}>{lb}</span>
                <span className="stdot" style={{ background: sc }} />
                <Ava t={av} c={ac} /><span className="iss-tm">{tm}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  } else if (d.includes("mercury")) {
    const TX = [
      ["S", "#635bff", "Stripe payout", "Revenue", "Jul 15", "+$4,820.00", 1],
      ["G", "#f45d48", "Gusto — payroll", "Payroll", "Jul 15", "−$12,304.18", 0],
      ["A", "#e88b00", "Amazon Web Services", "Infra", "Jul 14", "−$1,284.09", 0],
      ["W", "#0f9955", "Wade’s Plumbing — INV-1042", "Invoice", "Jul 14", "+$2,150.00", 1],
      ["L", "#5e6ad2", "Linear", "Software", "Jul 13", "−$96.00", 0],
      ["F", "#0055ff", "Figma", "Software", "Jul 12", "−$45.00", 0],
      ["R", "#7a9a01", "Ramp — card payment", "Card", "Jul 11", "−$3,412.77", 0],
    ];
    body = (<>
      <div className="sm-nav"><span className="sm-mark"><span className="sm-dot" style={{ "--bc": brand.c }}>M</span>Mercury</span>
        {["Accounts", "Payments", "Cards", "Capital"].map((l) => <span key={l} className="sm-link">{l}</span>)}
        <span className="sm-cta" style={{ "--bc": brand.c }}>Move money</span>
      </div>
      <div className="sm-wrap">
        <div className="me-hero">
          <div className="me-lbl">Total balance · Wade’s Plumbing &amp; Septic LLC</div>
          <div className="me-bal">$128,420.18 <span className="me-up">▲ 2.4% this month</span>
            <svg width="120" height="30" viewBox="0 0 120 30" style={{ marginLeft: "auto" }}><polyline points="0,24 18,22 34,25 50,17 66,19 84,10 102,12 120,4" fill="none" stroke="#0f9955" strokeWidth="2" strokeLinecap="round" /></svg>
          </div>
        </div>
        <div className="me-cards">
          <div className="me-card"><div className="me-cn">Checking ··4821</div><div className="me-cv">$84,210.55</div></div>
          <div className="me-card"><div className="me-cn">Savings</div><div className="me-cv">$32,400.00</div></div>
          <div className="me-card"><div className="me-cn">Treasury <span className="me-apy">4.10% APY</span></div><div className="me-cv">$11,809.63</div></div>
        </div>
        <div style={{ fontSize: 13, fontWeight: 650, padding: "6px 0 10px" }}>Recent transactions</div>
        <div className="st-tbl" style={{ margin: "0 0 44px" }}>
          {TX.map(([l, c, n, cat, dt, amt, pos]) => (
            <div key={n} className="tx-row" {...hov(d + "/tx/" + n.toLowerCase().replace(/[^a-z0-9]+/g, "-"))}>
              <span className="tx-ic" style={{ background: c }}>{l}</span>
              <span className="tx-n">{n}</span><span className="tx-c">{cat}</span>
              <span className="tx-d">{dt}</span><span className={"tx-a" + (pos ? " pos" : "")}>{amt}</span>
            </div>
          ))}
        </div>
      </div>
    </>);
  } else if (d.includes("github")) {
    const FILES = [
      [1, "src", "tab strip: FLIP under drag, no hover-jitter", "2d"],
      [1, "components", "group pill v6 — label joins the flow", "3d"],
      [1, "skills", "agent dry-run manifests", "5d"],
      [0, "shell.tsx", "fix: monotonic tab ids under held ⌘T", "2d"],
      [0, "theme.json", "paper + rosé pine presets", "6d"],
      [0, "package.json", "chore: esbuild 0.21", "1w"],
      [0, "README.md", "docs: the open .turing format", "1w"],
    ];
    body = (<>
      <div className="sm-nav"><span className="sm-mark"><span className="sm-dot" style={{ "--bc": "#24292f", borderRadius: "50%" }}>◍</span>GitHub</span>
        <span className="sm-ghost" style={{ width: 280, justifyContent: "flex-start", color: "#8b909c" }}><Search size={13} style={{ marginRight: 8 }} />Search or jump to…</span>
        {["Pulls", "Issues", "Explore"].map((l) => <span key={l} className="sm-link">{l}</span>)}
        <span style={{ marginLeft: "auto" }}><Ava t="B" c="#5b3df5" /></span>
      </div>
      <div className="sm-wrap">
        <div className="gh-head">
          <div className="gh-name"><BookOpen size={17} color="#59606d" /><span className="mono">nova</span><span style={{ color: "#8b909c" }}>/</span><span className="mono" style={{ fontWeight: 650 }}>shell</span><span className="gh-pub">Public</span></div>
          <div className="gh-stats">
            <span className="sm-ghost" style={{ height: 28, fontSize: 12 }}><Star size={13} style={{ marginRight: 6 }} /> Star · 2.4k</span>
            <span className="sm-ghost" style={{ height: 28, fontSize: 12 }}>Fork · 184</span>
            <span className="sm-ghost" style={{ height: 28, fontSize: 12 }}>Watch · 96</span>
            <span className="sm-cta" style={{ marginLeft: "auto", height: 28, fontSize: 12, "--bc": "#1f883d" }}>Code ▾</span>
          </div>
        </div>
        <div className="st-tbl" style={{ margin: "4px 0 0" }}>
          {FILES.map(([dir, f, m, t]) => (
            <div key={f} className="gh-file" {...hov(d + "/nova/shell/" + f)}>
              <span className="f">{dir ? <span className="sm-dot" style={{ width: 14, height: 14, "--bc": "#79b8ff", borderRadius: 4 }} /> : <FileCode size={14} color="#8b909c" />}{f}</span>
              <span className="m">{m}</span><span className="t">{t}</span>
            </div>
          ))}
        </div>
        <div className="gh-md">
          <div className="gh-md-h"><BookOpen size={13} /> README.md</div>
          <div className="gh-md-b">
            <h1>Nova Shell</h1>
            The open project browser — concept shell. Attio-calibrated chrome, one injected stylesheet, windowed lists, and agents that carry typed powers only. Everything exports to the documented <span className="mono" style={{ fontSize: 12 }}>.turing</span> format, so leaving never costs your work.
            <div className="gh-code">npm install<br />npm run dev &nbsp;<span style={{ color: "#8b909c" }}># localhost:5173 — HMR in 84ms</span></div>
          </div>
        </div>
      </div>
    </>);
  } else if (d.includes("stripe")) {
    const INV = [
      ["INV-1042", "Wade’s Plumbing & Septic", "$2,150.00", "Paid", "#0f9955", "#e9f8f0"],
      ["INV-1041", "Hearth & Home Services", "$840.00", "Open", "#4f5be5", "#eef2ff"],
      ["INV-1040", "BlueRidge HVAC", "$12,400.00", "Paid", "#0f9955", "#e9f8f0"],
      ["INV-1039", "Marietta Property Group", "$3,260.00", "Overdue", "#d64545", "#fdecec"],
      ["INV-1038", "Northside Builders", "$1,175.50", "Open", "#4f5be5", "#eef2ff"],
      ["INV-1037", "Canton Dental Partners", "$96.00", "Paid", "#0f9955", "#e9f8f0"],
    ];
    body = (<>
      <div className="sm-nav"><span className="sm-mark"><span className="sm-dot" style={{ "--bc": brand.c }}>S</span>Stripe</span>
        {["Payments", "Billing", "Customers", "Reports"].map((l) => <span key={l} className="sm-link">{l}</span>)}
        <span className="sm-cta" style={{ "--bc": brand.c }}>+ New invoice</span>
      </div>
      <div className="sm-wrap">
        <div style={{ display: "flex", alignItems: "center", gap: 10, padding: "26px 0 4px" }}>
          <span style={{ fontSize: 20, fontWeight: 650 }}>Invoices</span>
          <span className="tx-c">Last 30 days</span>
          <span className="sm-ghost" style={{ marginLeft: "auto", height: 30 }}>Export</span>
        </div>
        <div className="st-tbl">
          <div className="st-hd"><span>Invoice</span><span>Customer</span><span style={{ textAlign: "right" }}>Amount</span><span>Status</span><span>Due</span></div>
          {INV.map(([id, cu, amt, st, c, bg]) => (
            <div key={id} className="st-r" {...hov(d + "/invoices/" + id.toLowerCase())}>
              <span className="mono" style={{ fontSize: 11.5, color: "#59606d" }}>{id}</span>
              <span style={{ overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{cu}</span>
              <span className="mono" style={{ fontSize: 12, textAlign: "right" }}>{amt}</span>
              <span className="st-b" style={{ color: c, background: bg }}>{st}</span>
              <span style={{ fontSize: 11.5, color: "#8b8fa0" }}>Jul 30</span>
            </div>
          ))}
        </div>
      </div>
    </>);
  } else if (d.includes("v0")) {
    body = (<>
      <div className="sm-nav"><span className="sm-mark"><span className="sm-dot" style={{ "--bc": "#111114" }}>▲</span>v0</span>
        {["Projects", "Community", "Docs"].map((l) => <span key={l} className="sm-link">{l}</span>)}
        <span className="sm-cta" style={{ "--bc": "#111114" }}>New chat</span>
      </div>
      <div className="sm-wrap" style={{ maxWidth: 720 }}>
        <div className="sm-hero" style={{ padding: "64px 0 20px" }}>
          <div className="sm-kick" style={{ "--bc": "#111114" }}><Sparkles size={12} /> Generative UI</div>
          <div className="sm-h1" style={{ fontSize: 36 }}>What can I help you ship?</div>
        </div>
        <div className="sm-ghost" style={{ width: "100%", height: 54, justifyContent: "flex-start", color: "#8b909c", fontSize: 14, borderRadius: 14, padding: "0 18px", marginBottom: 12 }}>Describe a component, a page, or a whole app…</div>
        <div style={{ display: "flex", gap: 8, justifyContent: "center", paddingBottom: 34 }}>
          {["Pricing section", "Dashboard shell", "Onboarding flow", "Invoice table"].map((s) => <span key={s} className="ap-chip">{s}</span>)}
        </div>
        <div className="sm-grid3" style={{ gridTemplateColumns: "1fr 1fr" }}>
          {[["browser-concept", "14 iterations · yesterday", "135deg,#dbe4ff,#f4f0ff"], ["invoice-table", "shipped to prod · 3d", "135deg,#dff7ea,#f2fff8"]].map(([n, m, g]) => (
            <div key={n} className="sm-card" {...hov(d + "/chat/" + n)} style={{ cursor: "pointer" }}>
              <div style={{ height: 110, borderRadius: 10, background: "linear-gradient(" + g + ")", border: "1px solid #e9eaf0", marginBottom: 12 }} />
              <div className="sm-ct mono" style={{ fontSize: 13 }}>{n}</div><div className="sm-cd">{m}</div>
            </div>
          ))}
        </div>
      </div>
    </>);
  } else if (d.includes("youtube")) {
    const VIDS = [
      ["lofi beats to dispatch to — 24/7 radio", "Lofi Field", "LIVE · 2.1K watching", "160deg,#2b2350,#6a5cff", "◉ LIVE"],
      ["Designing calm interfaces", "Quiet Software", "318K views · 2 weeks ago", "160deg,#123a2e,#2fae7d", "24:12"],
      ["The browser that disappears — concept teardown", "Interface Review", "96K views · 5 days ago", "160deg,#3a1220,#c2455e", "16:04"],
      ["North Georgia trail cams — spring melt", "BlueRidge Wild", "1.2M views · 1 month ago", "160deg,#0e3a4a,#2f9dae", "12:47"],
      ["How invoices actually get paid", "Field Ops HQ", "42K views · 3 weeks ago", "160deg,#3a2a0e,#c98f2f", "9:58"],
      ["Attio-style tables from scratch", "Build Log", "210K views · 2 months ago", "160deg,#1c1c22,#5a5a68", "31:26"],
    ];
    body = (<>
      <div className="sm-nav"><span className="sm-mark"><span className="sm-dot" style={{ "--bc": "#ff0000", borderRadius: 7 }}>▶</span>YouTube</span>
        <span className="sm-ghost" style={{ flex: "0 1 400px", justifyContent: "flex-start", color: "#8b909c", borderRadius: 999 }}><Search size={13} style={{ marginRight: 8 }} />Search</span>
        <span style={{ marginLeft: "auto" }}><Ava t="B" c="#5b3df5" /></span>
      </div>
      <div className="sm-wrap">
        <div style={{ display: "flex", gap: 8, padding: "16px 0 0" }}>
          {["All", "Live", "Design", "Trades", "Music", "Recently uploaded"].map((c, i) => <span key={c} className={"ap-chip" + (i === 0 ? " on" : "")}>{c}</span>)}
        </div>
        <div className="yt-grid">
          {VIDS.map(([t, ch, m, g, dur]) => (
            <div key={t} {...hov(d + "/watch?v=" + t.slice(0, 8).replace(/\W/g, ""))} style={{ cursor: "pointer" }}>
              <div className="yt-th" style={{ background: "linear-gradient(" + g + ")" }}><span className="yt-dur">{dur}</span></div>
              <div className="yt-t">{t}</div><div className="yt-m">{ch} · {m}</div>
            </div>
          ))}
        </div>
      </div>
    </>);
  } else {
    body = (<>
      <div className="sm-nav"><span className="sm-mark"><span className="sm-dot">{brand.n[0]}</span>{brand.n}</span>
        {["Product", "Docs", "Pricing", "Changelog"].map((l) => <span key={l} className="sm-link">{l}</span>)}
        <span className="sm-ghost" style={{ marginLeft: "auto" }}>Sign in</span>
        <span className="sm-cta">Get started</span>
      </div>
      <div className="sm-wrap">
        <div className="sm-hero">
          <div className="sm-kick"><Sparkles size={12} /> New · {brand.n} 2.0 is here</div>
          <div className="sm-h1">{brand.h1 || "Everything your team ships, in one place"}</div>
          <div className="sm-sub">{brand.sub || "Plan, build, and launch together — without the busywork. Trusted by 40,000+ teams who care how their tools feel."}</div>
          <div style={{ display: "flex", gap: 10, justifyContent: "center" }}>
            <span className="sm-cta" style={{ height: 40, padding: "0 20px", fontSize: 13.5 }}>Start for free</span>
            <span className="sm-ghost" style={{ height: 40, padding: "0 18px", fontSize: 13.5 }}>Talk to sales</span>
          </div>
        </div>
        <div className="sm-art">
          <i style={{ left: "8%", top: "18%", width: "34%", height: "58%" }} />
          <i style={{ left: "46%", top: "30%", width: "28%", height: "52%" }} />
          <i style={{ left: "78%", top: "14%", width: "16%", height: "40%" }} />
        </div>
        <div className="sm-logos">{["ACME CORP", "NORTHWIND", "GLOBEX", "INITECH", "STARK"].map((l) => <span key={l}>{l}</span>)}</div>
        <div className="sm-grid3">
          {[[Zap, "Instant by default", "Every interaction lands in under 50ms — the entire product is engineered around that promise."],
            [ShieldCheck, "Private by design", "Your data stays yours. SOC 2, SSO, and audit logs on every plan, not just enterprise."],
            [Blocks, "Plays well with others", "A real API, webhooks, and 200+ integrations that never feel bolted on."]].map(([Ic, t, ds]) => (
            <div key={t} className="sm-card"><div className="sm-ci"><Ic size={16} /></div><div className="sm-ct">{t}</div><div className="sm-cd">{ds}</div></div>
          ))}
        </div>
        <div className="sm-article">
          <p className="wp-real" onMouseUp={(e) => {
            const s = window.getSelection(); const txt = s ? s.toString().trim() : "";
            if (txt.length > 8 && onAsk) {
              const r = s.getRangeAt(0).getBoundingClientRect();
              const nr = e.target.closest(".nova").getBoundingClientRect();
              const sc = nr.width / DESIGN_W;
              onAsk({ x: (r.x + r.width / 2 - nr.left) / sc, y: (r.y - nr.top) / sc - 34, text: txt });
            }
          }}>{ESSAY}</p>
          <div className="sm-pq">“Restraint is not an aesthetic. It is engineering — measured in frames, in milliseconds, in the moment you forget the tool is there.”</div>
          <p className="wp-real">That is why the teams who switch rarely switch back: the product earns trust by disappearing, and disappearing is the hardest feature to build.</p>
        </div>
        <div className="sm-foot">
          <div><b>Product</b><span>Overview</span><span>Pricing</span><span>Changelog</span></div>
          <div><b>Company</b><span>About</span><span>Careers</span><span>Blog</span></div>
          <div><b>Resources</b><span>Docs</span><span>API</span><span>Status</span></div>
          <div style={{ marginLeft: "auto", alignSelf: "flex-end" }}>© 2026 {brand.n}</div>
        </div>
      </div>
    </>);
  }

  return (
    <div className="scroll" ref={ref} onScroll={onScroll}>
      <div className={"wp" + (boost ? " boost" : "")} style={{ minHeight: "140%", zoom, "--bc": boost || brand.c, "--boost": boost || undefined, boxShadow: boost ? "inset 0 3px 0 " + boost : undefined }}>
        {translated && (
          <div className="trbar"><Globe size={12} /> Translated to English<button onClick={onShowOriginal}>Show original</button></div>
        )}
        {body}
        {hoverLink && <span className="linkpill mono">{hoverLink}</span>}
      </div>
    </div>
  );
});

/* ---------- New Tab ---------- */
function NewTab({ heroFocus, setHeroFocus, dev, onNavigate, restore, onDirty, readList = [], onOpenRead, onDropRead, landing = { mode: "search" }, spaceName, onNote }) {
  const inRef = useRef(null);
  const [tick, setTick] = useState(0);
  useEffect(() => {
    const target = 18204;
    if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) { setTick(target); return; }
    const t0 = performance.now(); let raf;
    const step = (t) => { const k = Math.min(1, (t - t0) / 1100); setTick(Math.round(target * (1 - Math.pow(1 - k, 3)))); if (k < 1) raf = requestAnimationFrame(step); };
    raf = requestAnimationFrame(step);
    return () => cancelAnimationFrame(raf);
  }, []);
  const [ntq, setNtq] = useState(false);
  if (landing.mode === "url" && landing.url) {
    return (
      <div style={{ height: "100%", display: "flex", flexDirection: "column" }}>
        <div className="hp-note mono">project homepage · {landing.url} · change in Settings → Appearance</div>
        <div style={{ flex: 1, minHeight: 0 }}><SitePage tab={{ id: "hp", url: landing.url, title: landing.url }} /></div>
      </div>
    );
  }
  return (
    <div className="scroll">
      <div className="nt">
        {restore && (
          <div className="banner">
            <RefreshCw size={13} />
            <span>Restore {restore.n} tabs from last time?</span>
            <button className="undo" onClick={restore.go}>Restore</button>
            <button className="dm" onClick={restore.dismiss}>Dismiss</button>
          </div>
        )}
        {landing.mode === "dashboard" && (
          <div className="dashhead">
            <div className="dh-t">{spaceName || "Work"}</div>
            <div className="dh-s mono">{new Date().toLocaleDateString("en-US", { weekday: "long", month: "short", day: "numeric" })} · everything where you left it</div>
          </div>
        )}
        <div className="nt-hero" style={landing.mode === "dashboard" ? { display: "none" } : undefined}>
          <div className={"bigsearch" + (heroFocus ? " focus" : "")} onClick={() => setHeroFocus(true)}>
            <Search size={19} color="var(--tx3)" />
            <input ref={inRef} placeholder="Search the web or ask anything"
              onFocus={() => setHeroFocus(true)} onBlur={() => setHeroFocus(false)}
              onKeyDown={(e) => { if (e.key === "Enter" && e.target.value.trim()) { onDirty && onDirty(false); onNavigate(e.target.value); } }}
              onChange={(e) => { onDirty && onDirty(e.target.value.trim().length > 0); setNtq(e.target.value.trim().length > 0); }} />
            <button className={"go" + (ntq ? " live" : "")} aria-label="Go"
              onClick={() => { const v = inRef.current?.value?.trim(); if (v) { onDirty && onDirty(false); onNavigate(v); } }}>
              <ArrowRight size={15} />
            </button>
          </div>
          <div className="ticker">
            <ShieldCheck size={13} />
            <span><b>{tick.toLocaleString()}</b> trackers blocked today</span>
          </div>
          <div className="typinghint">Type anywhere to begin · <span className="mono">⌘K</span></div>
        </div>
        {readList.length > 0 && (
          <div className="rlist">
            <div className="rl-cap"><BookOpen size={12} /> Read later</div>
            {readList.slice(0, 4).map((r) => (
              <div key={r.u} className="rl-row">
                <button className="rl-t" onClick={() => onOpenRead(r.u)}>{r.t}</button>
                <span className="rl-u mono">{r.u.split("/")[0]}</span>
                <button className="xc" style={{ opacity: .6 }} onClick={() => onDropRead(r.u)}><X size={11} /></button>
              </div>
            ))}
          </div>
        )}
        <div className="quick">
          <div className="qgrid">
            {QUICKS.map((q, i) => (
              <button key={i} className="q" data-url={q.u || q.url || (q.name ? q.name.toLowerCase().replace(/ /g,"")+".com" : undefined)}
                onClick={() => { if (q.name === "Add shortcut") { onNote && onNote("Pin any site here — drag a tab onto the grid"); return; } onNavigate(q.u || q.url || q.name.toLowerCase().replace(/ /g, "") + ".com"); }}>
                <div className="fav" style={q.style}>{q.letter}</div>
                <span>{q.name}</span>
              </button>
            ))}
          </div>
          {dev && (
            <>
              <div className="lbl" style={{ marginTop: 30 }}>Localhost</div>
              <div className="local">
                <a className="lhost"><span className="lv" />localhost:3000<span className="ln">Next.js · thorbis</span><span className="lt">HMR</span></a>
                <a className="lhost"><span className="lv" />localhost:5173<span className="ln">Vite · nova-shell</span><span className="lt">ready</span></a>
                <a className="lhost off"><span className="lv" />localhost:8080<span className="ln">API · not running</span><span className="lt">idle</span></a>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

/* ---------- Settings ---------- */
function A11ySec({ flags, toggle }) {
  return (
    <>
      <div className="ptitle">Accessibility & Focus</div>
      <div className="psub">A visible advantage, not a checkbox. Focus modes never hide security indicators.</div>
      <div className="sect">
        <div className="sect-h">Operate</div>
        <div className="card">
        <Row icon={<Command size={16} />} title="Complete keyboard operation" desc="Every surface reachable without a pointer. ⌘/ shows the map."><span className="pill">Always on</span></Row>
        <Row icon={<Eye size={16} />} title="Reading-order inspector" desc="Number every region in the order assistive tech will read it."><SW k="readOrder" flags={flags} toggle={toggle} /></Row>
        <Row icon={<ChevronRight size={16} />} title="Focus-navigation history" desc="Walk back through where your focus has been, like tab history for the keyboard."><span className="pill mono">⌥⇧←</span></Row>
        </div>
      </div>
      <div className="sect">
        <div className="sect-h">Comfort</div>
        <div className="card">
        <Row icon={<Type size={16} />} title="Typography & contrast policy" desc="Minimum sizes and contrast enforced per project — pages comply, not you."><SW k="a11yType" flags={flags} toggle={toggle} /></Row>
        <Row icon={<Zap size={16} />} title="Motion & distraction policy" desc="Honor reduced motion, mute autoplay, pin down sticky banners."><SW k="a11yCalm" flags={flags} toggle={toggle} /></Row>
        </div>
      </div>
    </>
  );
}

const SET_NAV = [
  { g: "" , items: [["general", "General", Settings], ["appearance", "Appearance", Palette]] },
  { g: "Protection", items: [["privacy", "Privacy & security", Shield], ["shields", "Ad blocker & shields", Ban], ["cookies", "Cookies & site data", Cookie]] },
  { g: "System", items: [["workspace", "Workspace & export", FileText], ["performance", "Performance", Gauge], ["a11y", "Accessibility", Eye], ["migrate", "Import from another browser", Download], ["downloads", "Downloads", Download], ["developer", "Developer", Terminal]] },
  { g: "You", items: [["passwords", "Passwords", KeyRound], ["autofill", "Autofill & cards", Key], ["extensions", "Extensions", Puzzle], ["search", "Search engine", Search]] },
  { g: "", items: [["about", "About Turing", Circle]] },
];

function SettingsPage({ sec, setSec, flags, toggle, tabPos, setTabPos, textScale, setTextScale, theme, setTheme, studio, landing, setLanding, vault, setVault, vaultLocked, setVaultLocked, note, go, tabs, spaces, spaceId, reading, notesBySpace, layouts, sched, setSched, onRunSchedule, agentLog, setAgentLog, agentCaps, setAgentCaps, watches, setWatches, conns, setConns }) {
  const [navQ, setNavQ] = useState("");
  return (
    <div className="scroll">
      <div className="page">
        <nav className="pnav">
          <h2><Settings size={17} color="var(--ac)" /> Settings</h2>
          <div className="pnav-search">
            <Search size={13} color="var(--tx3)" />
            <input placeholder="Search settings" value={navQ} onChange={(e) => setNavQ(e.target.value)} />
          </div>
          {SET_NAV.map((grp, gi) => {
            const items = grp.items.filter(([, label]) => !navQ || label.toLowerCase().includes(navQ.toLowerCase()));
            if (!items.length) return null;
            return (
            <div key={gi}>
              {grp.g && <div className="grp">{grp.g}</div>}
              {items.map(([id, label, Ic]) => (
                <a key={id} className={sec === id ? "on" : ""} onClick={() => { setSec(id); setNavQ(""); }}><Ic size={16} />{label}</a>
              ))}
            </div>
          ); })}
          {navQ && SET_NAV.every((g) => g.items.every(([, l]) => !l.toLowerCase().includes(navQ.toLowerCase()))) &&
            <div className="pnav-none">No settings match “{navQ}”</div>}
        </nav>
        <div className="pbody">
          {sec === "privacy" && <PrivacySec flags={flags} toggle={toggle} />}
          {sec === "shields" && <ShieldsSec flags={flags} toggle={toggle} />}
          {sec === "cookies" && <CookiesSec flags={flags} toggle={toggle} />}
          {sec === "performance" && <PerformanceSec flags={flags} toggle={toggle} />}
          {sec === "appearance" && <AppearanceSec tabPos={tabPos} setTabPos={setTabPos} flags={flags} toggle={toggle} textScale={textScale} setTextScale={setTextScale} theme={theme} setTheme={setTheme} studio={studio} landing={landing} setLanding={setLanding} />}
          {sec === "general" && <GeneralSec flags={flags} toggle={toggle} />}
          {sec === "workspace" && <WorkspaceSec tabs={tabs} spaces={spaces} spaceId={spaceId} reading={reading} notesBySpace={notesBySpace} layouts={layouts}
            agentCaps={agentCaps} watches={watches} agentLog={agentLog} note={note} />}
          {sec === "passwords" && <PasswordsSec vault={vault} setVault={setVault} locked={vaultLocked} setLocked={setVaultLocked} note={note} go={go} />}
          {sec === "autofill" && <AutofillSec flags={flags} toggle={toggle} />}
          {sec === "search" && <SearchSec flags={flags} toggle={toggle} />}
          {sec === "about" && <AboutSec />}
          {sec === "downloads" && <DownloadsSettings />}
          {sec === "a11y" && <A11ySec flags={flags} toggle={toggle} />}
          {sec === "migrate" && <MigrationPage note={() => {}} />}
          {sec === "developer" && <DeveloperSec flags={flags} toggle={toggle} />}
          {sec === "extensions" && <ExtensionsInline />}
        </div>
      </div>
    </div>
  );
}

function DeveloperSec({ flags, toggle }) {
  return (
    <>
      <div className="ptitle">Developer</div>
      <div className="psub">Tools for people building websites and apps. These stay out of the way unless you turn them on.</div>
      <div className="sect">
        <div className="card">
          <Row icon={<Terminal size={15} />} title="Developer mode" desc="Adds the inspector, a live performance readout, and localhost shortcuts on the new tab page.">
            <SW k="devmode" flags={flags} toggle={toggle} />
          </Row>
          <Row icon={<Gauge size={15} />} title="Open the inspector" desc="Web vitals, network requests, security report, and console.">
            <span className="val">{flags.devmode ? "⌥⌘I" : "Turn on Developer mode"}</span>
          </Row>
        </div>
      </div>
    </>
  );
}

function SW({ k, flags, toggle }) { return <Toggle on={flags[k]} onClick={() => toggle(k)} />; }

function PrivacySec({ flags, toggle }) {
  return (
    <>
      <div className="ptitle">Privacy & security</div>
      <div className="psub">Turing hardens every connection and keeps your browsing yours. These are the defaults for a concept — tuned aggressive.</div>
      <div className="sect">
        <div className="sect-h">Connection</div>
        <div className="card">
          <Row icon={<Lock size={16} />} title="Always use secure connections" desc="Upgrade every request to HTTPS and warn before loading insecure pages."><SW k="https" flags={flags} toggle={toggle} /></Row>
          <Row icon={<Wifi size={16} />} title="Secure DNS" desc="Resolve domains over encrypted DNS-over-HTTPS."><span className="pill">Cloudflare (1.1.1.1) <ChevronDown size={14} color="var(--tx3)" /></span></Row>
          <Row icon={<ShieldCheck size={16} />} title="Safe Browsing" desc="Block known phishing and malware sites in real time."><SW k="safeBrowse" flags={flags} toggle={toggle} /></Row>
        </div>
      </div>
      <div className="sect">
        <div className="sect-h">Tracking</div>
        <div className="card">
          <Row icon={<Ban size={16} />} title="Send “Do Not Track” request" desc="Ask sites not to track you. Turing also enforces this on its own."><SW k="dnt" flags={flags} toggle={toggle} /></Row>
          <Row icon={<Fingerprint size={16} />} title="Fingerprint protection" desc="Randomize the signals sites use to identify your device."><SW k="fingerprint" flags={flags} toggle={toggle} /></Row>
          <Row icon={<Cookie size={16} />} title="Block third-party cookies" desc="Stop cross-site cookies from following you around the web."><SW k="block3p" flags={flags} toggle={toggle} /></Row>
        </div>
      </div>
      <div className="sect">
        <div className="sect-h">Permissions</div>
        <div className="card">
          <Row icon={<MapPin size={16} />} title="Location" desc="2 sites allowed"><span className="pill">Ask first <ChevronDown size={14} color="var(--tx3)" /></span></Row>
          <Row icon={<Camera size={16} />} title="Camera" desc="1 site allowed"><span className="pill">Ask first <ChevronDown size={14} color="var(--tx3)" /></span></Row>
          <Row icon={<Mic size={16} />} title="Microphone" desc="No sites allowed"><span className="pill">Ask first <ChevronDown size={14} color="var(--tx3)" /></span></Row>
          <Row icon={<Bell size={16} />} title="Notifications" desc="Blocked by default"><span className="pill">Block <ChevronDown size={14} color="var(--tx3)" /></span></Row>
        </div>
      </div>
    </>
  );
}

function ShieldsSec({ flags, toggle }) {
  const lists = [
    ["EasyList", "78,204 rules", true], ["EasyPrivacy", "51,880 rules", true],
    ["Peter Lowe’s List", "3,120 rules", true], ["uBlock filters — Badware", "9,441 rules", true],
    ["Fanboy’s Annoyances", "44,010 rules", false], ["Regional — Nova Community", "6,502 rules", false],
  ];
  return (
    <>
      <div className="ptitle">Ad blocker & shields</div>
      <div className="psub">A built-in engine blocks ads, trackers, and page annoyances before they ever load — no extension required.</div>
      <div className="sect">
        <div className="sect-h">Shields</div>
        <div className="card">
          <Row icon={<Ban size={16} />} title="Block ads & trackers" desc="Cosmetic + network filtering on every site."><SW k="adblock" flags={flags} toggle={toggle} /></Row>
          <Row icon={<Zap size={16} />} title="Block annoyances" desc="Cookie banners, newsletter popups, chat widgets."><SW k="prefetch" flags={flags} toggle={toggle} /></Row>
          <Row icon={<Fingerprint size={16} />} title="Anti-fingerprinting" desc="Spoof canvas, audio, and font enumeration."><SW k="fingerprint" flags={flags} toggle={toggle} /></Row>
        </div>
      </div>
      <div className="sect">
        <div className="sect-h">Filter lists</div>
        <div className="card">
          {lists.map(([n, c, on]) => (
            <Row key={n} icon={<LayoutGrid size={15} />} title={n} desc={c}><Toggle on={on} onClick={() => { }} /></Row>
          ))}
          <div className="row"><button className="btn gho"><Plus size={14} /> Add custom filter list</button><span className="val" style={{ marginLeft: "auto" }}>Updated 2h ago</span></div>
        </div>
      </div>
    </>
  );
}

function CookiesSec({ flags, toggle }) {
  return (
    <>
      <div className="ptitle">Cookies & site data</div>
      <div className="psub">See exactly what each site stores, and clear it in a tap. Third-party cookies are blocked by default.</div>
      <div className="sect">
        <div className="sect-h">Default behavior</div>
        <div className="card">
          <Row icon={<Cookie size={16} />} title="Block third-party cookies" desc="Recommended. First-party cookies still work so you stay logged in."><SW k="block3p" flags={flags} toggle={toggle} /></Row>
          <Row icon={<Trash2 size={16} />} title="Clear cookies when Turing closes" desc="Keep exceptions for sites you choose."><Toggle on={false} onClick={() => { }} /></Row>
        </div>
      </div>
      <div className="sect">
        <div className="sect-h" style={{ display: "flex", justifyContent: "space-between" }}>
          <span>Stored data — {COOKIES.length} sites</span>
          <button className="btn dgr" style={{ height: 24, padding: "0 8px", fontSize: 12 }}><Trash2 size={13} /> Clear all</button>
        </div>
        <div className="card">
          {COOKIES.map((c) => (
            <div className="row" key={c.name}>
              <div className="ico" style={{ color: c.secure ? "var(--good)" : "var(--tx3)" }}>
                {c.secure ? <Lock size={14} /> : <Globe size={14} />}
              </div>
              <div className="meta"><div className="t mono">{c.name}</div><div className="d">{c.count} cookies · {c.size}</div></div>
              <span className={"tag " + (c.type === "First-party" ? "on" : "off")}>{c.type}</span>
              <button className="ib" style={{ width: 28, height: 28 }}><Trash2 size={14} /></button>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}

function PerformanceSec({ flags, toggle }) {
  return (
    <>
      <div className="ptitle">Performance</div>
      <div className="psub">Nova is built to feel instant. Tune how aggressively it trades memory for speed.</div>
      <div className="sect">
        <div className="sect-h">Speed</div>
        <div className="card">
          <Row icon={<Gauge size={16} />} title="Memory Saver" desc="Sleep inactive tabs and free their memory. Wakes instantly on click."><SW k="memSaver" flags={flags} toggle={toggle} /></Row>
          <Row icon={<Zap size={16} />} title="Preload pages" desc="Speculatively load links you’re likely to click for instant navigation."><SW k="preload" flags={flags} toggle={toggle} /></Row>
          <Row icon={<Monitor size={16} />} title="Hardware acceleration" desc="Use the GPU for compositing, video, and animation."><SW k="hwaccel" flags={flags} toggle={toggle} /></Row>
          <Row icon={<Wifi size={16} />} title="HTTP/3 (QUIC)" desc="Faster, multiplexed connections with zero head-of-line blocking."><SW k="quic" flags={flags} toggle={toggle} /></Row>
          <Row icon={<Sun size={16} />} title="Energy Saver" desc="Cap background frame rate and pause animations on battery."><SW k="energy" flags={flags} toggle={toggle} /></Row>
        </div>
      </div>
      <div className="sect">
        <div className="sect-h">Memory by tab</div>
        <div className="card">
          {[["v0.app", 92, "148 MB"], ["Figma — Nova DS", 78, "121 MB"], ["GitHub · nova/shell", 34, "54 MB"], ["Linear", 22, "34 MB"]].map(([n, p, mb]) => (
            <div className="row" key={n}>
              <div className="meta"><div className="t">{n}</div><div style={{ marginTop: 8 }} className="meter"><i style={{ width: p + "%" }} /></div></div>
              <span className="val">{mb}</span>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}

function ThemeStudio({ themeId, applyPreset, customVars, setCustomVars, fontSans, setFontSans, fontMono, setFontMono, density, setDensity, radius, setRadius, note }) {
  const [json, setJson] = useState("");
  const [err, setErr] = useState(false);
  const effective = { "--ac": customVars["--ac"] || "#2e8dff", ...THEMES.find((t) => t.id === themeId)?.vars, ...customVars };
  useEffect(() => { setJson(JSON.stringify({ accent: effective["--ac"], surface: effective["--c1"] || "#101012", text: effective["--tx"] || "#f2f2f3", line: effective["--line"] || "rgba(255,255,255,.06)" }, null, 2)); }, [themeId]); // eslint-disable-line
  const apply = () => {
    try {
      const j = JSON.parse(json);
      const map = { accent: "--ac", surface: "--c1", text: "--tx", line: "--line" };
      const next = {};
      Object.entries(j).forEach(([k, v]) => { if (map[k]) next[map[k]] = v; });
      setCustomVars((c) => ({ ...c, ...next })); setErr(false); note("theme.json applied — live");
    } catch { setErr(true); }
  };
  return (
    <>
      <div className="sect">
        <div className="sect-h">Theme · like your terminal, but a browser</div>
        <div className="th-grid">
          {THEMES.map((t) => (
            <button key={t.id} className={"th-card" + (themeId === t.id ? " on" : "")} onClick={() => applyPreset(t.id)}>
              <span className="th-sw">
                {[t.vars["--ink"] || (t.mode === "light" ? "#f2f2f5" : "#0a0a0a"), t.vars["--c2"] || (t.mode === "light" ? "#f3f3f6" : "#141416"), t.vars["--tx"] || (t.mode === "light" ? "#16161a" : "#f2f2f3"), "#2e8dff"].map((c, i) => <i key={i} style={{ background: c }} />)}
              </span>
              <span className="th-n">{t.name}</span>
              <span className="th-by mono">{t.by}</span>
            </button>
          ))}
        </div>
      </div>
      <div className="sect">
        <div className="sect-h">Type</div>
        <div className="card">
          <Row icon={<Type size={16} />} title="Interface font" desc="The voice of the chrome.">
            <div className="seg">{FONTS_SANS.map(([n, stack]) => <button key={n} className={fontSans === stack ? "on" : ""} onClick={() => setFontSans(stack)}>{n}</button>)}</div>
          </Row>
          <Row icon={<Terminal size={16} />} title="Mono font" desc="URLs, numbers, and anything that must line up.">
            <div className="seg">{FONTS_MONO.map(([n, stack]) => <button key={n} className={fontMono === stack ? "on" : ""} onClick={() => setFontMono(stack)}>{n}</button>)}</div>
          </Row>
          <Row icon={<LayoutGrid size={16} />} title="Density" desc="Compact tightens the bar and chips for small screens or maximal tabs.">
            <div className="seg">{["cozy", "compact"].map((d) => <button key={d} className={density === d ? "on" : ""} onClick={() => setDensity(d)}>{d[0].toUpperCase() + d.slice(1)}</button>)}</div>
          </Row>
          <Row icon={<Circle size={16} />} title="Corners" desc="Sharp for the terminal crowd, round for the soft-launch crowd.">
            <div className="seg">{["sharp", "soft", "round"].map((r) => <button key={r} className={radius === r ? "on" : ""} onClick={() => setRadius(r)}>{r[0].toUpperCase() + r.slice(1)}</button>)}</div>
          </Row>
        </div>
      </div>
      <div className="sect">
        <div className="sect-h">theme.json — edit the tokens directly</div>
        <div className={"th-json" + (err ? " err" : "")}>
          <textarea value={json} spellCheck={false} rows={7} onChange={(e) => { setJson(e.target.value); setErr(false); }} />
          <div className="th-json-bar">
            {err ? <span className="mono" style={{ color: "var(--bad)", fontSize: 11 }}>invalid JSON — nothing applied</span>
                 : <span className="mono" style={{ fontSize: 10.5, color: "var(--tx3)" }}>changes apply live · exportable · shareable</span>}
            <button className="hclear" style={{ marginLeft: "auto", height: 26 }} onClick={() => { navigator.clipboard?.writeText(json); note("theme.json copied — share it"); }}>Export</button>
            <button className="hclear" style={{ height: 26, color: "var(--ac)" }} onClick={apply}>Apply</button>
          </div>
        </div>
      </div>
    </>
  );
}

function AppearanceSec({ tabPos, setTabPos, flags, toggle, textScale, setTextScale, theme, setTheme, studio, landing, setLanding }) {
  const [accent, setAccent] = useState("#2e8dff");
  const accents = ["#2e8dff", "#7b5cff", "#34d399", "#f97316", "#f472b6", "#eab308"];
  return (
    <>
      <div className="ptitle">Appearance</div>
      <div className="psub">Yours down to the tokens — themes, type, density, and the page every tab lands on.</div>
      <ThemeStudio {...studio} />
      <div className="sect">
        <div className="sect-h">New tabs land on</div>
        <div className="card">
          <Row icon={<Plus size={16} />} title="Landing" desc="Per project. Search for speed, Dashboard for context, or any page you choose.">
            <div className="seg">{["search", "dashboard", "url"].map((m) => <button key={m} className={landing.mode === m ? "on" : ""} onClick={() => setLanding((l) => ({ ...l, mode: m }))}>{m === "url" ? "Custom URL" : m[0].toUpperCase() + m.slice(1)}</button>)}</div>
          </Row>
          {landing.mode === "url" && (
            <Row icon={<Globe size={16} />} title="Homepage" desc="Every new tab in this project opens here.">
              <input className="hp-in mono" value={landing.url} onChange={(e) => setLanding((l) => ({ ...l, url: e.target.value }))} placeholder="linear.app/team" />
            </Row>
          )}
        </div>
      </div>
      <div className="sect">
        <div className="sect-h">Theme</div>
        <div className="card">
          <Row icon={<Moon size={16} />} title="Color mode" desc="Nova’s chrome in dark or light. Pages keep their own colors. ⌘K → “Toggle theme” works too.">
            <div className="seg">
              {[["dark", Moon], ["light", Sun]].map(([m, Ic]) => (
                <button key={m} className={theme === m ? "on" : ""} onClick={() => setTheme(m)}><Ic size={13} />{m[0].toUpperCase() + m.slice(1)}</button>
              ))}
            </div>
          </Row>
          <Row icon={<Palette size={16} />} title="Accent color" desc="Used for focus, links, and active state.">
            <div style={{ display: "flex", gap: 8 }}>
              {accents.map((c) => (
                <button key={c} onClick={() => setAccent(c)} style={{ width: 24, height: 24, borderRadius: "var(--r)", background: c, outline: accent === c ? "2px solid var(--tx)" : "none", outlineOffset: 2 }} />
              ))}
            </div>
          </Row>
        </div>
      </div>
      <div className="sect">
        <div className="sect-h">Layout</div>
        <div className="card">
          <Row icon={<LayoutGrid size={16} />} title="Tab position" desc="Where your open tabs live. Changes apply right away.">
            <div className="seg">
              {["top", "left", "right", "bottom"].map((p) => (
                <button key={p} className={tabPos === p ? "on" : ""} onClick={() => setTabPos(p)}>{p[0].toUpperCase() + p.slice(1)}</button>
              ))}
            </div>
          </Row>
          <Row icon={<Sparkles size={16} />} title="Fade unused tabs" desc="Tabs you haven’t touched gently dim, so what matters stands out. “Tidy tabs” closes the faded ones.">
            <SW k="fade" flags={flags} toggle={toggle} />
          </Row>
          <Row icon={<Eye size={16} />} title="Hide the bar while you scroll" desc="Reading a page tucks the bar away; scrolling up brings it right back.">
            <SW k="autozen" flags={flags} toggle={toggle} />
          </Row>
          <Row icon={<BookOpen size={16} />} title="Make text bigger" desc={<span style={{ fontSize: 12 * textScale + "px" }}>Pages will look like this sentence.</span>}>
            <div className="seg">
              {[[0.9, "A−"], [1, "Normal"], [1.15, "A+"]].map(([v, l]) => (
                <button key={l} className={textScale === v ? "on" : ""} onClick={() => setTextScale(v)}>{l}</button>
              ))}
            </div>
          </Row>
          <Row icon={<Bookmark size={16} />} title="Show bookmarks bar" desc="Always visible under the toolbar."><Toggle on={false} onClick={() => { }} /></Row>
        </div>
      </div>
    </>
  );
}

function GeneralSec({ flags, toggle }) {
  return (
    <>
      <div className="ptitle">General</div>
      <div className="psub">Startup, downloads, and the basics.</div>
      <div className="sect"><div className="sect-h">On startup</div>
        <div className="card">
          <Row icon={<Home size={16} />} title="Open the New Tab page" desc="What Nova shows when it launches."><span className="pill">New Tab <ChevronDown size={14} color="var(--tx3)" /></span></Row>
          <Row icon={<RefreshCw size={16} />} title="Continue where you left off" desc="Restore tabs from your last session."><Toggle on onClick={() => { }} /></Row>
          <Row icon={<Sparkles size={16} />} title="Show suggestions in address bar" desc="Search and history suggestions as you type."><SW k="sugg" flags={flags} toggle={toggle} /></Row>
        </div>
      </div>
      <div className="sect"><div className="sect-h">Sync</div>
        <div className="card">
          <Row icon={<RefreshCw size={16} />} title="Sync across devices" desc="Tabs, bookmarks, and history, end-to-end encrypted."><SW k="sync" flags={flags} toggle={toggle} /></Row>
        </div>
      </div>
    </>
  );
}

function AutofillSec({ flags, toggle }) {
  return (
    <>
      <div className="ptitle">Autofill & passwords</div>
      <div className="psub">Nova can fill logins, addresses, and cards — stored encrypted on your device.</div>
      <div className="sect"><div className="sect-h">Passwords</div>
        <div className="card">
          <Row icon={<Key size={16} />} title="Offer to save passwords" desc="Prompt to store new logins securely."><SW k="passwords" flags={flags} toggle={toggle} /></Row>
          <Row icon={<ShieldCheck size={16} />} title="Password health check" desc="3 reused · 1 weak · 0 leaked"><button className="btn gho" style={{ height: 28 }}>Review</button></Row>
          <Row icon={<Fingerprint size={16} />} title="Require device unlock" desc="Face or fingerprint before autofilling."><Toggle on onClick={() => { }} /></Row>
        </div>
      </div>
      <div className="sect"><div className="sect-h">Autofill</div>
        <div className="card">
          <Row icon={<CircleUser size={16} />} title="Addresses & more" desc="2 saved profiles"><SW k="autofill" flags={flags} toggle={toggle} /></Row>
          <Row icon={<Key size={16} />} title="Payment methods" desc="Cards are tokenized; full numbers never stored."><Toggle on onClick={() => { }} /></Row>
        </div>
      </div>
    </>
  );
}

function SearchSec({ flags, toggle }) {
  const engines = [["Google", "G", "#4285f4", true], ["DuckDuckGo", "D", "#de5833", false], ["Brave", "B", "#fb542b", false], ["Perplexity", "P", "#20808d", false]];
  return (
    <>
      <div className="ptitle">Search engine</div>
      <div className="psub">The engine used from the address bar and New Tab.</div>
      <div className="sect"><div className="sect-h">Default</div>
        <div className="card">
          {engines.map(([n, l, c, on]) => (
            <div className="row" key={n}>
              <div className="fav" style={{ ...FAV(c), width: 30, height: 30, borderRadius: "var(--r)", fontSize: 13, fontWeight: 700 }}>{l}</div>
              <div className="meta"><div className="t">{n}</div></div>
              {on ? <span className="tag on">Default</span> : <button className="btn gho" style={{ height: 28 }}>Make default</button>}
            </div>
          ))}
        </div>
      </div>
      <div className="sect"><div className="sect-h">Address bar</div>
        <div className="card">
          <Row icon={<Search size={16} />} title="Search suggestions" desc="Show completions from your engine."><SW k="sugg" flags={flags} toggle={toggle} /></Row>
        </div>
      </div>
    </>
  );
}

function AboutSec() {
  const PILLARS = [
    ["Projects, not tabs", "A Space keeps its identity, history, notes, and budgets — pause it, share it, take it anywhere."],
    ["Time Machine", "Every state versioned. Restores structure, never repeats actions."],
    ["Resource truth", "Every megabyte owned, every freeze explained before it happens."],
    ["Trustworthy agents", "Typed powers, dry-runs, and your hand on every consequential step."],
    ["Research canvas", "Linked panes and cited evidence — reproduce why you concluded."],
    ["Open by design", "High-fidelity import, documented export. Leaving never costs your work."],
  ];
  return (
    <>
      <div className="ptitle">About Turing</div>
      <div className="psub">The open project browser — for people and agents.</div>
      <div className="card ab-hero">
        <div className="glyph" style={{ width: 54, height: 54, borderRadius: "var(--r-lg)", flex: "none" }}><Sparkles size={26} color="#fff" /></div>
        <div style={{ minWidth: 0 }}>
          <div className="ab-name">Turing <span className="beta">CONCEPT</span></div>
          <div className="ab-tag">It remembers the work, explains the cost, and keeps you in control.</div>
          <div className="ab-chips">
            {["v0.1.0", "Chromium 126", "React shell", "open .turing format"].map((c) => <span key={c} className="ab-chip mono">{c}</span>)}
            <span className="ab-chip mono up"><Check size={11} /> up to date</span>
          </div>
        </div>
      </div>
      <div className="sect" style={{ marginTop: 24 }}>
        <div className="sect-h">What makes it Turing</div>
        <div className="ab-grid">
          {PILLARS.map(([t, d]) => (
            <div key={t} className="ab-cell"><div className="t">{t}</div><div className="d">{d}</div></div>
          ))}
        </div>
      </div>
    </>
  );
}

function DownloadsSettings() {
  return (
    <>
      <div className="ptitle">Downloads</div>
      <div className="psub">Where files land and how they’re handled.</div>
      <div className="card">
        <Row icon={<Download size={16} />} title="Location" desc="/Users/nova/Downloads"><button className="btn gho" style={{ height: 28 }}>Change</button></Row>
        <Row icon={<ChevronRight size={16} />} title="Ask where to save each file" desc="Prompt for a location every time."><Toggle on={false} onClick={() => { }} /></Row>
      </div>
    </>
  );
}
function ExtensionsInline() { return <ExtensionsPage embedded />; }

/* ---------- History page (virtualized) ---------- */
function HistoryPage({ onDel, note }) {
  const [q, setQ] = useState("");
  const [range, setRange] = useState("all");
  const [focus, setFocus] = useState(false);
  const [cleared, setCleared] = useState(false);
  const [confirm, setConfirm] = useState(false);
  const [sel, setSel] = useState(() => new Set());
  const toggleSel = (id) => setSel((s) => { const n = new Set(s); n.has(id) ? n.delete(id) : n.add(id); return n; });
  const ref = useRef(null);
  const ROW = 52;

  const list = useMemo(() => {
    const ql = q.trim().toLowerCase();
    if (cleared) return [];
    return HISTORY.filter((h) => {
      if (range === "today" && h.day !== "Today") return false;
      if (range === "week" && !["Today", "Yesterday", "Mon, Jul 13", "Sun, Jul 12", "Sat, Jul 11"].includes(h.day)) return false;
      if (!ql) return true;
      return h.t.toLowerCase().includes(ql) || h.u.toLowerCase().includes(ql);
    });
  }, [q, range, cleared]);

  const { start, end, pad } = useVirtual(ref, ROW, list.length);
  const slice = list.slice(start, end);
  const empty = list.length === 0;

  return (
    <div className="scroll" style={{ position: "relative" }}>
      <PageHeader icon={HistoryIcon} title="History" chip={list.length.toLocaleString() + " entries"} maxW={940}>
        {!cleared && (confirm ? (
          <span style={{ display: "flex", gap: 6, alignItems: "center" }}>
            <span style={{ fontSize: 12, color: "var(--tx3)" }}>Really clear?</span>
            <button className="hclear" style={{ color: "var(--bad)" }} onClick={() => { setCleared(true); setConfirm(false); }}>Yes, clear</button>
            <button className="hclear" onClick={() => setConfirm(false)}>Keep</button>
          </span>
        ) : (
          <button className="hclear" onClick={() => setConfirm(true)}>Clear browsing data</button>
        ))}
      </PageHeader>
      <div className="page">
        <div className="pbody wide pcol" style={{ "--colw": "940px" }}>
          <div className="htop" style={{ marginTop: 18 }}>
            <div className={"hsearch" + (focus ? " focus" : "")}>
              <Search size={16} color="var(--tx3)" />
              <input placeholder="Search history" value={q} onChange={(e) => setQ(e.target.value)}
                onFocus={() => setFocus(true)} onBlur={() => setFocus(false)} />
            </div>
            <div className="chips">
              {[["all", "All"], ["today", "Today"], ["week", "This week"]].map(([id, l]) => (
                <button key={id} className={"chip" + (range === id ? " on" : "")} onClick={() => setRange(id)}>{l}</button>
              ))}
            </div>
          </div>
          <div className="hlist">
            {empty && <div className="hempty">{cleared ? "History cleared. Fresh start." : "Nothing matches that search."}</div>}
            <div className="hwin" ref={ref}>
              {list.length === 0 ? (
                <div className="hempty">No results for “{q}”.</div>
              ) : (
                <div style={{ height: pad, position: "relative" }}>
                  {slice.map((item, i) => (
                    <HRow key={item.id} item={item} y={(start + i) * ROW} onDel={onDel}
                      selected={sel.has(item.id)} onSel={toggleSel}
                      dayTag={(start + i) === 0 || list[start + i - 1].day !== item.day ? item.day.replace(/^\w+, /, "") : ""} />
                  ))}
                </div>
              )}
            </div>
            {!empty && <div className="tfoot"><span className="mono">{list.length.toLocaleString()} entries</span><span>grouped by day</span><span style={{ marginLeft: "auto" }}>windowed rendering — only what's on screen exists</span></div>}
          </div>
        </div>
      </div>
      {sel.size > 0 && (
        <div className="selbar">
          <span className="n">{sel.size} selected</span>
          <button className="hclear" onClick={() => { note && note("Opened " + sel.size + " pages in new tabs"); setSel(new Set()); }}>Open all</button>
          <button className="hclear" onClick={() => { note && note(sel.size + " links copied"); setSel(new Set()); }}>Copy links</button>
          <button className="hclear" style={{ color: "var(--bad)" }} onClick={() => { const ids = [...sel]; ids.forEach(onDel); note && note("Removed " + ids.length + " entries"); setSel(new Set()); }}>Remove</button>
          <button className="x" onClick={() => setSel(new Set())}><X size={13} /></button>
        </div>
      )}
    </div>
  );
}

/* ---------- Extensions page ---------- */
function ExtensionsPage({ embedded, note }) {
  const [ext, setExt] = useState(EXTENSIONS);
  const flip = (i) => setExt((e) => e.map((x, j) => (j === i ? { ...x, on: !x.on } : x)));
  const body = (
    <>
      <div className="psub" style={{ marginTop: 4 }}>{ext.filter((e) => e.on).length} of {ext.length} enabled · each runs in an isolated sandbox.</div>
      <div className="exgrid">
        {ext.map((e, i) => (
          <div className="ex" key={e.nm}>
            <div className="ex-h">
              <div className="logo"><e.icon size={18} /></div>
              <div style={{ flex: 1 }}>
                <div className="nm">{e.nm} {e.built && <span className="tag on" style={{ marginLeft: 4 }}>BUILT-IN</span>}</div>
                <div className="by">by {e.by}</div>
              </div>
              <Toggle on={e.on} onClick={() => flip(i)} />
            </div>
            <div className="desc">{e.desc}</div>
            <div className="ex-meta mono">v{e.ver} · {e.sz}</div>
            <div className="ex-f">
              <span className="perm"><Eye size={13} /> {e.perms}</span>
              <div style={{ display: "flex", gap: 4 }}>
                <button className="ib" style={{ width: 28, height: 28 }}><Settings size={14} /></button>
                {!e.built && <button className="ib" style={{ width: 28, height: 28 }}><Trash2 size={14} /></button>}
              </div>
            </div>
          </div>
        ))}
      </div>
    </>
  );
  if (embedded) return body;
  return (
    <div className="scroll">
      <PageHeader icon={Puzzle} title="Extensions" chip={ext.filter((e) => e.on).length + " of " + ext.length + " on"} maxW={900}>
        <button className="hclear" onClick={() => note && note("The extension store opens here — concept")}><Blocks size={13} style={{ marginRight: 6, verticalAlign: -2 }} />Browse store</button>
        <button className="btn-pri" style={{ height: 28 }} onClick={() => note && note("Drop a .crx or pick from the store — concept")}><Plus size={14} /> Add extension</button>
      </PageHeader>
      <div className="page"><div className="pbody pcol" style={{ "--colw": "900px" }}>{body}</div></div>
    </div>
  );
}

/* ---------- Downloads page ---------- */

/* ---------- popovers ---------- */

function TrailPop({ hist, jump }) {
  const entries = [];
  for (let i = hist.i - 1; i >= 0 && entries.length < 5; i--) entries.push({ ...hist.stack[i], idx: i });
  return (
    <div className="pop" style={{ top: 4, left: 52, width: 280 }}>
      <div className="pop-h"><div className="t">Trail</div><div className="s" style={{ marginLeft: "auto" }}>hold ← anytime</div></div>
      <div style={{ padding: 6 }}>
        {entries.length === 0 && <div style={{ padding: "10px 12px", color: "var(--tx3)", fontSize: 12 }}>Nothing behind you yet.</div>}
        {entries.map((e) => (
          <button key={e.idx} className="mitem" onClick={() => jump(e.idx)}>
            <ArrowLeft size={14} /><span style={{ flex: 1, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap", textAlign: "left" }}>{e.v === "newtab" ? (e.title || e.url) : e.v[0].toUpperCase() + e.v.slice(1)}</span>
          </button>
        ))}
      </div>
    </div>
  );
}

function SecurityPop({ flags, go, domain, perms, setPerm, onReceipt }) {
  return (
    <div className="pop" style={{ top: 4, left: 170, width: 300 }}>
      <div className="pop-h">
        <div className="ico" style={{ background: "rgba(52,211,153,.12)", color: "var(--good)" }}><Lock size={16} /></div>
        <div><div className="t">Connection is secure</div><div className="s">Your data is encrypted (TLS 1.3)</div></div>
      </div>
      <div style={{ padding: 6 }}>
        <button className="mitem"><ShieldCheck size={16} /> Certificate is valid <Check size={14} color="var(--good)" style={{ marginLeft: "auto" }} /></button>
        <button className="mitem" onClick={() => go("settings", "cookies")}><Cookie size={16} /> Cookies in use <span className="r">8</span></button>
        <button className="mitem" onClick={() => go("settings", "privacy")}><SlidersHorizontal size={16} /> Site permissions</button>
        <button className="mitem" onClick={onReceipt}><FileCode size={16} /> Privacy receipt — what this page did</button>
        <div className="msep" />
        <div style={{ padding: "6px 12px 10px", display: "flex", alignItems: "center", gap: 8, color: "var(--tx2)", fontSize: 12 }}>
          <ShieldCheck size={14} color="var(--good)" /> <b className="mono" style={{ color: "var(--good)" }}>17</b> trackers blocked here
        </div>
      </div>
      <div style={{ padding: "4px 12px 10px" }}>
        <div className="dt-cap" style={{ padding: "6px 0" }}>Permissions · {domain}</div>
        {[["cam", "Camera", Camera], ["mic", "Microphone", Mic], ["loc", "Location", MapPin]].map(([k, l, I]) => (
          <div key={k} className="permrow">
            <I size={14} /><span>{l}</span>
            <div className="seg" style={{ marginLeft: "auto" }}>
              {["ask", "allow", "block"].map((v) => (
                <button key={v} className={((perms[domain] || {})[k] || "ask") === v ? "on" : ""} onClick={() => setPerm(domain, k, v)}>{v[0].toUpperCase() + v.slice(1)}</button>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

/* ---------- Turing Shield ---------- */
const TRACKER_POOL = [
  ["Google Analytics", "analytics"], ["Google Tag Manager", "tag"], ["DoubleClick", "ads"],
  ["Meta Pixel", "social"], ["TikTok Pixel", "social"], ["LinkedIn Insight", "social"],
  ["Segment", "analytics"], ["Hotjar", "session"], ["Mixpanel", "analytics"],
  ["Amplitude", "analytics"], ["Intercom", "widget"], ["Criteo", "ads"],
  ["Taboola", "ads"], ["FullStory", "session"], ["Optimizely", "analytics"],
];
const SHIELD_CATS = { ads: "Advertising", analytics: "Analytics", social: "Social", session: "Session replay", tag: "Tag manager", widget: "Chat widget" };
function hashStr(str) { let h = 2166136261; for (let i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; }
// deterministic per-domain report: the same site always shows the same numbers
function shieldFor(dom) {
  const h = hashStr(dom || "x");
  const seen = new Map();
  const n = 3 + (h % 5);
  for (let i = 0; i < n; i++) {
    const [name, cat] = TRACKER_POOL[(h >>> (i * 3)) % TRACKER_POOL.length];
    const c = 1 + ((h >>> (i * 5)) % 4);
    if (!seen.has(name)) seen.set(name, { name, cat, c });
  }
  const items = [...seen.values()].sort((a, b) => b.c - a.c);
  const trackers = items.reduce((a, b) => a + b.c, 0);
  return {
    items, trackers,
    ads: 4 + (h % 14),
    fp: h % 3,
    banners: h % 2,
    kb: (40 + (h % 380)),
    ms: 120 + (h % 620),
    upgraded: (h % 5) !== 0,
  };
}
const SH_LEVELS = [["standard", "Standard", "Blocks ads and cross-site trackers. Sites keep working."],
                   ["strict", "Strict", "Adds fingerprint randomising and first-party isolation. May break a few sites."],
                   ["off", "Off", "No filtering on this site."]];

function ShieldPop({ flags, toggle, go, dom, level, setLevel, weekTotal }) {
  const [tab, setTab] = useState("blocked");
  const r = shieldFor(dom);
  const off = level === "off" || !flags.adblock;
  const total = off ? 0 : r.trackers + r.ads + r.banners;
  return (
    <div className="pop shp" style={{ top: 4, right: 46, width: 344 }}>
      <div className="pop-h">
        <div className="ico" style={{ background: off ? "var(--c3)" : "var(--ac-soft)", color: off ? "var(--tx3)" : "var(--ac)" }}><ShieldCheck size={16} /></div>
        <div style={{ minWidth: 0 }}>
          <div className="t">Turing Shield</div>
          <div className="s mono" style={{ overflow: "hidden", textOverflow: "ellipsis" }}>{dom}</div>
        </div>
        <div style={{ marginLeft: "auto" }}><Toggle on={!off} onClick={() => setLevel(off ? "standard" : "off")} /></div>
      </div>

      <div className="shp-hero">
        <div className="shp-big mono">{total}</div>
        <div className="shp-blurb">
          {off ? <>Shield is <b>off</b> for this site. Nothing is being filtered.</>
               : <>things blocked on this page · <b>{r.kb} KB</b> and about <b>{(r.ms / 1000).toFixed(1)}s</b> saved</>}
        </div>
      </div>

      <div className="shp-seg">
        {SH_LEVELS.map(([id, label, desc]) => (
          <button key={id} className={"shp-segb" + (level === id ? " on" : "")} title={desc} onClick={() => setLevel(id)}>{label}</button>
        ))}
      </div>
      <div className="shp-desc">{(SH_LEVELS.find((x) => x[0] === level) || SH_LEVELS[0])[2]}</div>

      {!off && (
        <>
          <div className="shp-tabs">
            <button className={tab === "blocked" ? "on" : ""} onClick={() => setTab("blocked")}>Blocked <span className="mono">{r.items.length}</span></button>
            <button className={tab === "conn" ? "on" : ""} onClick={() => setTab("conn")}>Connection</button>
          </div>
          {tab === "blocked" ? (
            <div className="shp-list">
              {r.items.map((it) => (
                <div key={it.name} className="shp-row">
                  <span className="shp-dot" data-cat={it.cat} />
                  <span className="shp-nm">{it.name}</span>
                  <span className="shp-cat">{SHIELD_CATS[it.cat]}</span>
                  <span className="shp-c mono">{it.c}</span>
                </div>
              ))}
              <div className="shp-row muted">
                <span className="shp-dot" data-cat="ads" />
                <span className="shp-nm">Ad slots removed</span>
                <span className="shp-cat">Cosmetic</span>
                <span className="shp-c mono">{r.ads}</span>
              </div>
              {r.banners > 0 && (
                <div className="shp-row muted">
                  <span className="shp-dot" data-cat="widget" />
                  <span className="shp-nm">Cookie banner dismissed</span>
                  <span className="shp-cat">Annoyance</span>
                  <span className="shp-c mono">1</span>
                </div>
              )}
            </div>
          ) : (
            <div className="shp-list">
              <div className="shp-conn"><Lock size={13} color="var(--good)" /><div><b>Encrypted connection</b><span>TLS 1.3 · certificate valid</span></div></div>
              <div className="shp-conn"><ArrowUp size={13} color={r.upgraded ? "var(--good)" : "var(--tx3)"} /><div><b>{r.upgraded ? "Upgraded to HTTPS" : "Already secure"}</b><span>{r.upgraded ? "This site was requested over http" : "No downgrade attempted"}</span></div></div>
              <div className="shp-conn"><Fingerprint size={13} color={level === "strict" ? "var(--good)" : "var(--warn)"} /><div>
                <b>{level === "strict" ? "Fingerprint randomised" : "Fingerprint readable"}</b>
                <span>{level === "strict" ? "Canvas, audio and font probes get noise" : r.fp + " probe" + (r.fp === 1 ? "" : "s") + " seen — Strict randomises them"}</span></div></div>
              <div className="shp-conn"><Cookie size={13} color="var(--tx2)" /><div><b>Cookies isolated</b><span>Third-party cookies are partitioned per site</span></div></div>
            </div>
          )}
        </>
      )}

      <div className="shp-foot">
        <span><b className="mono">{weekTotal.toLocaleString()}</b> blocked this week</span>
        <button onClick={() => go("settings", "shields")}><SlidersHorizontal size={13} />Settings</button>
      </div>
    </div>
  );
}

/* ---------- password manager ---------- */
const VAULT0 = [
  { id: 1, site: "linear.app", user: "byron@thorbis.com", pw: "kR7#mve2Qp!Lz9", used: "2 hours ago", totp: true },
  { id: 2, site: "github.com", user: "byronwade", pw: "Xy4$np8Wq!vB3d", used: "yesterday", passkey: true },
  { id: 3, site: "mercury.com", user: "byron@thorbis.com", pw: "7Hn!qZ4tv#Rm2s", used: "3 days ago", totp: true },
  { id: 4, site: "stripe.com", user: "byron@thorbis.com", pw: "Thorbis2024!", used: "6 days ago" },
  { id: 5, site: "vercel.com", user: "byron@thorbis.com", pw: "Thorbis2024!", used: "1 week ago" },
  { id: 6, site: "figma.com", user: "byron@thorbis.com", pw: "wades123", used: "3 weeks ago" },
  { id: 7, site: "notion.com", user: "byron@thorbis.com", pw: "bQ9%zk3Hs!Wd7x", used: "1 month ago" },
  { id: 8, site: "intranet.wades.local", user: "bwade", pw: "PlumbCo!2019", used: "2 months ago" },
];
const BREACHED = { "wades123": "LinkedIn, 2021 · 6.5M accounts", "PlumbCo!2019": "Dropbox, 2022 · 68M accounts" };
const PW_LABEL = ["Very weak", "Weak", "Fair", "Strong", "Excellent"];
function pwScore(pw) {
  if (!pw) return 0;
  let n = 0;
  if (pw.length >= 8) n++; if (pw.length >= 12) n++; if (pw.length >= 16) n++;
  if (/[a-z]/.test(pw) && /[A-Z]/.test(pw)) n++;
  if (/\d/.test(pw)) n++;
  if (/[^A-Za-z0-9]/.test(pw)) n++;
  if (/^[A-Za-z]+[0-9]{0,4}[!@#]?$/.test(pw)) n -= 3;   // a word with a number stuck on the end
  return Math.max(0, Math.min(4, n - 1));
}
function vaultHealth(v) {
  const seen = {};
  v.forEach((e) => { seen[e.pw] = (seen[e.pw] || 0) + 1; });
  return {
    reused: v.filter((e) => seen[e.pw] > 1),
    weak: v.filter((e) => pwScore(e.pw) <= 1),
    breached: v.filter((e) => BREACHED[e.pw]),
  };
}
function genPw(len, up, num, sym) {
  const lo = "abcdefghijkmnopqrstuvwxyz", UP = "ABCDEFGHJKLMNPQRSTUVWXYZ", NU = "23456789", SY = "!@#$%^&*?-_=+";
  let pool = lo + (up ? UP : "") + (num ? NU : "") + (sym ? SY : "");
  let out = "";
  for (let i = 0; i < len; i++) out += pool[Math.floor(Math.random() * pool.length)];
  return out;
}
function PwMeter({ pw }) {
  const sc = pwScore(pw);
  const tone = ["var(--bad)", "var(--bad)", "var(--warn)", "var(--good)", "var(--good)"][sc];
  return (
    <div className="pwm">
      <div className="pwm-bars">{[0, 1, 2, 3].map((i) => <i key={i} style={{ background: i <= sc - 1 || (sc === 0 && i === 0) ? tone : "var(--c4)" }} />)}</div>
      <span style={{ color: tone }}>{PW_LABEL[sc]}</span>
    </div>
  );
}
function VaultRow({ e, open, onOpen, onCopy, onDelete, onUpdate }) {
  const [show, setShow] = useState(false);
  const bad = BREACHED[e.pw];
  const sc = pwScore(e.pw);
  return (
    <div className={"vrow-w" + (open ? " open" : "")}>
      <button className="vrow" onClick={onOpen}>
        <Fav f={{ f: site(e.site[0].toUpperCase(), "#7c8798") }} size={16} />
        <span className="v-site">{e.site}<span className="v-user">{e.user}</span></span>
        {e.passkey && <span className="vtag pk"><KeyRound size={9} />Passkey</span>}
        {e.totp && <span className="vtag">2FA</span>}
        {bad && <span className="vtag bad"><ShieldAlert size={9} />Breached</span>}
        {!bad && sc <= 1 && <span className="vtag warn">Weak</span>}
        <span className="v-used mono">{e.used}</span>
        <ChevronDown size={13} className={"v-chev" + (open ? " rot" : "")} />
      </button>
      {open && (
        <div className="vdet">
          <label className="vf"><span>Username</span>
            <input value={e.user} onChange={(ev) => onUpdate({ user: ev.target.value })} />
            <button title="Copy username" onClick={() => onCopy(e.user, "Username copied")}><Copy size={12} /></button>
          </label>
          <label className="vf"><span>Password</span>
            <input type={show ? "text" : "password"} value={e.pw} onChange={(ev) => onUpdate({ pw: ev.target.value })} className="mono" />
            <button title={show ? "Hide" : "Reveal"} onClick={() => setShow((v) => !v)}>{show ? <EyeOff size={12} /> : <Eye size={12} />}</button>
            <button title="Copy password" onClick={() => onCopy(e.pw, "Password copied · clears in 30s")}><Copy size={12} /></button>
            <button title="Generate a new one" onClick={() => onUpdate({ pw: genPw(18, true, true, true) })}><Dices size={12} /></button>
          </label>
          <PwMeter pw={e.pw} />
          {bad && <div className="vwarn"><ShieldAlert size={13} /><div><b>Seen in a breach</b><span>{bad} — change it and stop reusing it.</span></div></div>}
          <div className="vdet-f">
            {e.totp && <span className="v-totp mono">2FA · 481 209 <i /></span>}
            <button className="vdel" onClick={onDelete}><Trash2 size={12} />Delete</button>
          </div>
        </div>
      )}
    </div>
  );
}
function PasswordsSec({ vault, setVault, locked, setLocked, note, go }) {
  const [q, setQ] = useState("");
  const [open, setOpen] = useState(null);
  const [gen, setGen] = useState(false);
  const [gl, setGl] = useState(20); const [gu, setGu] = useState(true); const [gn, setGn] = useState(true); const [gs, setGs] = useState(true);
  const [gpw, setGpw] = useState(() => genPw(20, true, true, true));
  const h = vaultHealth(vault);
  const copy = (t, msg) => { try { navigator.clipboard && navigator.clipboard.writeText(t); } catch (e) {} note(msg); };
  const shown = vault.filter((e) => !q.trim() || (e.site + " " + e.user).toLowerCase().includes(q.trim().toLowerCase()));

  if (locked) {
    return (
      <>
        <div className="ptitle">Passwords</div>
        <div className="psub">Your vault is encrypted on this device. Nothing syncs unless you turn it on.</div>
        <div className="vlock">
          <div className="vlock-i"><Lock size={22} color="var(--ac)" /></div>
          <div className="vlock-t">Vault locked</div>
          <div className="vlock-s">{vault.length} logins · unlock with your device to view or fill them.</div>
          <button className="btn-pri" onClick={() => { setLocked(false); note("Vault unlocked · re-locks after 5 minutes idle"); }}>
            <Fingerprint size={14} />Unlock with Touch ID
          </button>
        </div>
      </>
    );
  }
  return (
    <>
      <div className="ptitle">Passwords</div>
      <div className="psub">{vault.length} logins, encrypted on this device. Turing fills them; it never uploads them.</div>

      {(h.breached.length + h.reused.length + h.weak.length) > 0 && (
        <div className="vhealth">
          <div className="vh-h"><ShieldAlert size={15} color="var(--warn)" /><b>Password health</b>
            <button onClick={() => { setQ(""); setOpen(h.breached[0]?.id || h.weak[0]?.id || h.reused[0]?.id); }}>Review</button></div>
          <div className="vh-stats">
            <div><span className="mono" style={{ color: "var(--bad)" }}>{h.breached.length}</span>in a known breach</div>
            <div><span className="mono" style={{ color: "var(--warn)" }}>{h.reused.length}</span>reused elsewhere</div>
            <div><span className="mono" style={{ color: "var(--warn)" }}>{h.weak.length}</span>too weak</div>
          </div>
        </div>
      )}

      <div className="vbar">
        <div className="vsearch"><Search size={13} color="var(--tx3)" /><input placeholder="Search logins" value={q} onChange={(e) => setQ(e.target.value)} /></div>
        <button className="btn gho" onClick={() => setGen((v) => !v)}><Dices size={13} />Generator</button>
        <button className="btn gho" onClick={() => {
          const id = Date.now();
          setVault((v) => [{ id, site: "new-site.com", user: "", pw: genPw(20, true, true, true), used: "just now" }, ...v]);
          setOpen(id); note("New login added");
        }}><Plus size={13} />Add</button>
        <button className="btn gho" title="Lock the vault" onClick={() => { setLocked(true); note("Vault locked"); }}><Lock size={13} /></button>
      </div>

      {gen && (
        <div className="vgen">
          <div className="vgen-out mono">{gpw}</div>
          <div className="vgen-ctl">
            <label>Length <b className="mono">{gl}</b>
              <input type="range" min="8" max="40" value={gl} onChange={(e) => { const n = +e.target.value; setGl(n); setGpw(genPw(n, gu, gn, gs)); }} />
            </label>
            <div className="vgen-opts">
              {[["A-Z", gu, setGu], ["0-9", gn, setGn], ["!@#", gs, setGs]].map(([lb, val, set]) => (
                <button key={lb} className={val ? "on" : ""} onClick={() => { set(!val); setGpw(genPw(gl, lb === "A-Z" ? !val : gu, lb === "0-9" ? !val : gn, lb === "!@#" ? !val : gs)); }}>{lb}</button>
              ))}
            </div>
          </div>
          <PwMeter pw={gpw} />
          <div className="vgen-act">
            <button className="btn gho" onClick={() => setGpw(genPw(gl, gu, gn, gs))}><RefreshCw size={12} />New</button>
            <button className="btn-pri" onClick={() => copy(gpw, "Generated password copied")}><Copy size={12} />Copy</button>
          </div>
        </div>
      )}

      <div className="vlist">
        {shown.length === 0 && <div className="vempty">No logins match “{q}”.</div>}
        {shown.map((e) => (
          <VaultRow key={e.id} e={e} open={open === e.id} onOpen={() => setOpen(open === e.id ? null : e.id)}
            onCopy={copy}
            onUpdate={(patch) => setVault((v) => v.map((x) => (x.id === e.id ? { ...x, ...patch } : x)))}
            onDelete={() => { setVault((v) => v.filter((x) => x.id !== e.id)); setOpen(null); note("Login deleted"); }} />
        ))}
      </div>

      <div className="sect"><div className="sect-h">Passkeys</div>
        <div className="card">
          {vault.filter((e) => e.passkey).map((e) => (
            <Row key={e.id} icon={<KeyRound size={16} />} title={e.site} desc={"Synced · created " + e.used + " · this device + iPhone"}>
              <button className="btn gho" style={{ height: 26 }} onClick={() => note("Passkey for " + e.site + " is on 2 devices")}>Manage</button>
            </Row>
          ))}
          <Row icon={<Plus size={16} />} title="Add a passkey" desc="Replace a password with a device-bound key. Nothing to type, nothing to leak.">
            <button className="btn gho" style={{ height: 26 }} onClick={() => note("Ready — visit a site that supports passkeys")}>Set up</button>
          </Row>
        </div>
      </div>
      <div className="sect"><div className="sect-h">How filling works</div>
        <div className="card">
          <Row icon={<Fingerprint size={16} />} title="Require unlock before filling" desc="Touch ID each time a password leaves the vault."><Toggle on onClick={() => { }} /></Row>
          <Row icon={<KeyRound size={16} />} title="Prefer passkeys" desc="Use a passkey instead of a password where the site supports it."><Toggle on onClick={() => { }} /></Row>
          <Row icon={<Ban size={16} />} title="Never fill on http:// pages" desc="Refuse to autofill over an unencrypted connection."><Toggle on onClick={() => { }} /></Row>
        </div>
      </div>
    </>
  );
}
function VaultPop({ vault, locked, setLocked, dom, note, go, onFill }) {
  const matches = vault.filter((e) => e.site === dom || dom.endsWith("." + e.site));
  const copy = (t, m) => { try { navigator.clipboard && navigator.clipboard.writeText(t); } catch (e) {} note(m); };
  return (
    <div className="pop" style={{ top: 4, right: 46, width: 300 }}>
      <div className="pop-h">
        <div className="ico" style={{ background: "var(--ac-soft)", color: "var(--ac)" }}><KeyRound size={16} /></div>
        <div style={{ minWidth: 0 }}><div className="t">Passwords</div><div className="s mono">{dom}</div></div>
      </div>
      {locked ? (
        <div className="vpop-lock">
          <Lock size={18} color="var(--tx3)" />
          <span>Vault is locked</span>
          <button className="btn-pri" onClick={() => { setLocked(false); note("Vault unlocked"); }}><Fingerprint size={13} />Unlock</button>
        </div>
      ) : (
        <div style={{ padding: 6 }}>
          {matches.length === 0 && <div className="vpop-none">No saved login for this site.</div>}
          {matches.map((e) => (
            <div key={e.id} className="vpop-row">
              <Fav f={{ f: site(e.site[0].toUpperCase(), "#7c8798") }} size={15} />
              <span className="vpop-u">{e.user}<span>{e.passkey ? "Passkey" : "Password · " + e.used}</span></span>
              <button className="vpop-fill" onClick={() => { onFill(e); }}><LogIn size={12} />Fill</button>
            </div>
          ))}
          <button className="mitem" onClick={() => copy(genPw(20, true, true, true), "Generated password copied")}><Dices size={15} />Generate a password</button>
          <button className="mitem" onClick={() => go("settings", "passwords")}><KeyRound size={15} />Open vault</button>
        </div>
      )}
    </div>
  );
}

/* ---------- modal focus containment (Asteria 05: focus is trapped while modal, restored on close) ---------- */
function useFocusTrap(ref) {
  useEffect(() => {
    const node = ref.current;
    if (!node) return;
    const opener = document.activeElement;
    const SEL = 'button,a[href],input,textarea,select,[tabindex]:not([tabindex="-1"])';
    const list = () => [...node.querySelectorAll(SEL)].filter((e) => e.getBoundingClientRect().width > 0);
    const first = list()[0];
    (first || node).focus();
    const onKey = (e) => {
      if (e.key !== "Tab") return;
      const f = list();
      if (!f.length) { e.preventDefault(); node.focus(); return; }
      const i = f.indexOf(document.activeElement);
      if (e.shiftKey) { if (i <= 0) { e.preventDefault(); f[f.length - 1].focus(); } }
      else if (i === f.length - 1 || i === -1) { e.preventDefault(); f[0].focus(); }
    };
    node.addEventListener("keydown", onKey);
    return () => {
      node.removeEventListener("keydown", onKey);
      if (opener && opener.focus && document.contains(opener)) opener.focus();
    };
  }, [ref]);
}

/* ---------- find in page ---------- */
const findRoot = () => document.querySelector(".nova .view");
function clearMarks() {
  const r = findRoot(); if (!r) return;
  r.querySelectorAll("mark.fx").forEach((m) => { const t = document.createTextNode(m.textContent); m.replaceWith(t); });
  r.normalize();
}
function runFind(q) {
  clearMarks();
  const r = findRoot(); if (!r || !q) return 0;
  const walk = document.createTreeWalker(r, NodeFilter.SHOW_TEXT, {
    acceptNode(n) {
      if (!n.nodeValue || !n.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
      const p = n.parentElement;
      if (!p || p.closest("script,style,input,textarea,.findbar,.hintlayer")) return NodeFilter.FILTER_REJECT;
      return NodeFilter.FILTER_ACCEPT;
    },
  });
  const nodes = []; let n;
  while ((n = walk.nextNode())) nodes.push(n);
  const rx = new RegExp(q.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "gi");
  let count = 0;
  nodes.forEach((node) => {
    const text = node.nodeValue;
    rx.lastIndex = 0;
    if (!rx.test(text)) return;
    rx.lastIndex = 0;
    const frag = document.createDocumentFragment();
    let last = 0, m;
    while ((m = rx.exec(text))) {
      if (m.index > last) frag.appendChild(document.createTextNode(text.slice(last, m.index)));
      const mk = document.createElement("mark");
      mk.className = "fx"; mk.textContent = m[0];
      frag.appendChild(mk); last = m.index + m[0].length; count++;
      if (m[0].length === 0) break;
    }
    frag.appendChild(document.createTextNode(text.slice(last)));
    node.parentNode.replaceChild(frag, node);
  });
  return count;
}
function FindBar({ onClose, note }) {
  const [q, setQ] = useState("");
  const [n, setN] = useState(0);
  const [i, setI] = useState(0);
  const inp = useRef(null);
  useEffect(() => { inp.current && inp.current.focus(); return () => clearMarks(); }, []);
  useEffect(() => {
    const c = runFind(q); setN(c); setI(c ? 1 : 0);
    if (c) { const m = findRoot().querySelectorAll("mark.fx")[0]; if (m) { m.classList.add("on"); m.scrollIntoView({ block: "center" }); } }
  }, [q]);
  const step = (d) => {
    const marks = findRoot() ? findRoot().querySelectorAll("mark.fx") : [];
    if (!marks.length) return;
    const next = ((i - 1 + d) + marks.length) % marks.length;
    marks.forEach((m) => m.classList.remove("on"));
    marks[next].classList.add("on"); marks[next].scrollIntoView({ block: "center" });
    setI(next + 1);
  };
  return (
    <div className="findbar">
      <Search size={13} color="var(--tx3)" />
      <input ref={inp} placeholder="Find on page" value={q} onChange={(e) => setQ(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") { e.preventDefault(); step(e.shiftKey ? -1 : 1); }
          if (e.key === "Escape") { e.preventDefault(); onClose(); }
        }} />
      <span className="fb-n mono">{q ? i + "/" + n : ""}</span>
      <button onClick={() => step(-1)} title="Previous · ⇧↵"><ChevronUp size={13} /></button>
      <button onClick={() => step(1)} title="Next · ↵"><ChevronDown size={13} /></button>
      <button onClick={onClose} title="Close · esc"><X size={13} /></button>
    </div>
  );
}

/* ---------- keyboard link hints ---------- */
const HINT_KEYS = "asdfghjkl";
function HintLayer({ onDone, note }) {
  const [typed, setTyped] = useState("");
  const [hints, setHints] = useState([]);
  useEffect(() => {
    const r = document.querySelector(".nova"); if (!r) { onDone(); return; }
    const vh = window.innerHeight, vw = window.innerWidth;
    const els = [...r.querySelectorAll('a[href],button,[data-url],[role="button"],.ttab,.bm')].filter((e) => {
      if (e.closest(".hintlayer")) return false;
      const b = e.getBoundingClientRect();
      return b.width > 8 && b.height > 8 && b.top > -4 && b.top < vh && b.left < vw && getComputedStyle(e).visibility !== "hidden";
    }).slice(0, 81);
    const lab = (i) => els.length <= HINT_KEYS.length ? HINT_KEYS[i]
      : HINT_KEYS[Math.floor(i / HINT_KEYS.length)] + HINT_KEYS[i % HINT_KEYS.length];
    setHints(els.map((el, i) => { const b = el.getBoundingClientRect(); return { el, k: lab(i), x: b.left, y: b.top }; }));
  }, [onDone]);
  useEffect(() => {
    const on = (e) => {
      if (e.key === "Escape") { onDone(); return; }
      if (e.key === "Backspace") { setTyped((t) => t.slice(0, -1)); return; }
      if (e.key.length !== 1) return;
      e.preventDefault(); e.stopPropagation();
      const t = (typed + e.key.toLowerCase());
      const hit = hints.find((h) => h.k === t);
      if (hit) { hit.el.click(); note("Followed hint " + t.toUpperCase()); onDone(); return; }
      if (hints.some((h) => h.k.startsWith(t))) setTyped(t); else onDone();
    };
    window.addEventListener("keydown", on, true);
    return () => window.removeEventListener("keydown", on, true);
  }, [typed, hints, onDone, note]);
  return (
    <div className="hintlayer">
      {hints.filter((h) => !typed || h.k.startsWith(typed)).map((h, i) => (
        <span key={i} className="hint mono" style={{ left: h.x, top: h.y }}>
          {h.k.split("").map((c, j) => <b key={j} className={j < typed.length ? "done" : ""}>{c}</b>)}
        </span>
      ))}
    </div>
  );
}

/* ---------- tab search across every space ---------- */
function TabSearch({ tabs, spaceId, spaces, spaceStore, onPick, onClose }) {
  const box = useRef(null); useFocusTrap(box);
  const [q, setQ] = useState("");
  const [sel, setSel] = useState(0);
  const all = useMemo(() => {
    const rows = tabs.map((t) => ({ t, space: spaceId, here: true }));
    Object.keys(spaceStore.current || {}).forEach((sp) => {
      if (sp === spaceId) return;
      (spaceStore.current[sp].tabs || []).forEach((t) => rows.push({ t, space: sp, here: false }));
    });
    return rows;
  }, [tabs, spaceId, spaceStore]);
  const ql = q.trim().toLowerCase();
  const list = all
    .filter((r) => (ql ? r.t.url !== "nova://newtab" : true))
    .filter((r) => !ql || ((r.t.label || r.t.title || "") + " " + r.t.url).toLowerCase().includes(ql))
    .slice(0, 60);
  useEffect(() => { setSel(0); }, [q]);
  const spName = (id) => (spaces.find((x) => x.id === id) || {}).name || id;
  return (
    <div className="ovl" onClick={onClose}>
      <div className="tabsrch" ref={box} role="dialog" aria-modal="true" aria-label="Search all tabs" tabIndex={-1} onClick={(e) => e.stopPropagation()}>
        <div className="ts-in">
          <Search size={15} color="var(--tx3)" />
          <input autoFocus placeholder="Search every open tab, in every space · ⌥⌘A" value={q}
            onChange={(e) => setQ(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "ArrowDown") { e.preventDefault(); setSel((v) => Math.min(list.length - 1, v + 1)); }
              if (e.key === "ArrowUp") { e.preventDefault(); setSel((v) => Math.max(0, v - 1)); }
              if (e.key === "Enter") { e.preventDefault(); const r = list[sel]; if (r) onPick(r); }
              if (e.key === "Escape") onClose();
            }} />
          <span className="mono ts-c">{list.length}</span>
        </div>
        <div className="ts-list">
          {list.length === 0 && <div className="ts-empty">Nothing open matches “{q}”.</div>}
          {list.map((r, i) => (
            <button key={r.space + "-" + r.t.id} className={"ts-row" + (i === sel ? " sel" : "")}
              onMouseEnter={() => setSel(i)} onClick={() => onPick(r)}>
              <Fav f={r.t.f} size={15} />
              <span className="ts-t">{(r.t.label || r.t.title || r.t.url).slice(0, 54)}<span className="mono">{r.t.url}</span></span>
              {!r.here && <span className="ts-sp">{spName(r.space)}</span>}
            </button>
          ))}
        </div>
        <div className="ts-foot"><span><b className="mono">↑↓</b> move · <b className="mono">↵</b> switch · <b className="mono">esc</b> close</span></div>
      </div>
    </div>
  );
}

/* ---------- reading list ---------- */
const READ0 = [
  { id: 1, title: "The cost of context switching", url: "linear.app/blog/context", mins: 6, read: false },
  { id: 2, title: "Designing for keyboard-first users", url: "vercel.com/blog/keyboard", mins: 9, read: false },
  { id: 3, title: "What we learned shipping agents", url: "notion.com/blog/agents", mins: 12, read: true },
];
/* ---------- search bangs ---------- */
const BANGS = [
  ["!gh", "github.com/search?q=", "GitHub"],
  ["!mdn", "developer.mozilla.org/search?q=", "MDN"],
  ["!yt", "youtube.com/results?search_query=", "YouTube"],
  ["!npm", "npmjs.com/search?q=", "npm"],
  ["!w", "en.wikipedia.org/w/index.php?search=", "Wikipedia"],
  ["!so", "stackoverflow.com/search?q=", "Stack Overflow"],
];
function applyBang(q) {
  const m = q.trim().match(/^(![a-z]+)\s+(.*)$/i);
  if (!m) return null;
  const b = BANGS.find((x) => x[0] === m[1].toLowerCase());
  if (!b) return null;
  return { url: b[1] + encodeURIComponent(m[2]), name: b[2], term: m[2] };
}

function SidePanel({ kind, onClose, reading, setReading, notes, setNotes, spaceName, onOpen, note }) {
  const [q, setQ] = useState("");
  const unread = reading.filter((r) => !r.read).length;
  return (
    <div className="sidep">
      <div className="sidep-h">
        {kind === "reading" ? <BookOpen size={15} color="var(--ac)" /> : <FileText size={15} color="var(--ac)" />}
        <div className="sidep-t">{kind === "reading" ? "Reading list" : "Project notes"}
          <span>{kind === "reading" ? unread + " unread" : spaceName}</span></div>
        <button onClick={onClose} title="Close"><X size={14} /></button>
      </div>
      {kind === "reading" ? (
        <>
          <div className="sidep-s"><Search size={12} color="var(--tx3)" />
            <input placeholder="Filter" value={q} onChange={(e) => setQ(e.target.value)} /></div>
          <div className="sidep-b">
            {reading.filter((r) => !q || r.title.toLowerCase().includes(q.toLowerCase())).map((r) => (
              <div key={r.id} className={"rdl-row" + (r.read ? " read" : "")}>
                <button className="rdl-chk" title={r.read ? "Mark unread" : "Mark read"}
                  onClick={() => setReading((v) => v.map((x) => (x.id === r.id ? { ...x, read: !x.read } : x)))}>
                  {r.read ? <Check size={11} /> : <Circle size={11} />}
                </button>
                <button className="rdl-main" onClick={() => onOpen(r.url)}>
                  <span className="rdl-t">{r.title}</span>
                  <span className="rdl-m mono">{r.url.split("/")[0]} · {r.mins} min</span>
                </button>
                <button className="rdl-x" title="Remove" onClick={() => setReading((v) => v.filter((x) => x.id !== r.id))}><X size={11} /></button>
              </div>
            ))}
            {reading.length === 0 && <div className="sidep-e">Nothing saved yet. Press ⇧⌘D on any page.</div>}
          </div>
        </>
      ) : (
        <>
          <textarea className="npad" value={notes} placeholder={"Notes for " + spaceName + " — they stay with this project."}
            onChange={(e) => setNotes(e.target.value)} />
          <div className="sidep-f mono">{notes.trim() ? notes.trim().split(/\s+/).length + " words" : "empty"} · saved to this space</div>
        </>
      )}
    </div>
  );
}

/* ---------- task manager ---------- */
function TaskManager({ tabs, onClose, onSleep, onClose1, onMergeDup, note }) {
  const box = useRef(null); useFocusTrap(box);
  const rows = tabs.filter((t) => t.url !== "nova://newtab").map((t) => {
    const h = hashStr(t.url);
    return { t, mem: 40 + (h % 380), cpu: (h % 47) / 10, sleeping: !!t.asleep };
  }).sort((a, b) => b.mem - a.mem);
  const total = rows.reduce((n, r) => n + r.mem, 0);
  return (
    <div className="ovl" onClick={onClose}>
      <div className="taskm" ref={box} role="dialog" aria-modal="true" aria-label="Task manager" tabIndex={-1} onClick={(e) => e.stopPropagation()}>
        <div className="tk-h"><Activity size={15} color="var(--ac)" />
          <div>Task manager<span className="mono">{rows.length} tabs · {(total / 1024).toFixed(2)} GB</span></div>
          <button onClick={onClose}><X size={14} /></button></div>
        {(() => {
          const by = {};
          rows.forEach((r) => { by[r.t.url] = (by[r.t.url] || 0) + 1; });
          const dup = Object.keys(by).filter((u) => by[u] > 1);
          if (!dup.length) return null;
          const extra = dup.reduce((n, u) => n + by[u] - 1, 0);
          return (
            <div className="tk-dup">
              <Layers size={13} />
              <span>{extra} duplicate tab{extra === 1 ? "" : "s"} across {dup.length} address{dup.length === 1 ? "" : "es"}</span>
              <button onClick={() => { onMergeDup(dup); }}>Merge</button>
            </div>
          );
        })()}
        <div className="tk-rows">
          {rows.map((r) => (
            <div key={r.t.id} className={"tk-r" + (r.sleeping ? " zzz" : "")}>
              <Fav f={r.t.f} size={14} />
              <span className="tk-t">{(r.t.label || r.t.title || r.t.url).slice(0, 40)}</span>
              <span className="tk-bar"><i style={{ width: Math.min(100, r.mem / 4.2) + "%" }} /></span>
              <span className="tk-v mono">{r.mem} MB</span>
              <span className="tk-v mono dim">{r.sleeping ? "—" : r.cpu.toFixed(1) + "%"}</span>
              <button className="tk-a" title={r.sleeping ? "Wake" : "Sleep this tab"} onClick={() => onSleep(r.t.id)}>
                {r.sleeping ? <RotateCw size={11} /> : <Moon size={11} />}
              </button>
              <button className="tk-a" title="Close tab" onClick={() => onClose1(r.t.id)}><X size={11} /></button>
            </div>
          ))}
        </div>
        <div className="tk-f">Sleeping a tab frees its memory and keeps the chip in place. It wakes when you click it.</div>
      </div>
    </div>
  );
}

/* ---------- per-site controls ---------- */
const SITE_PERMS = [["Camera", "ask"], ["Microphone", "ask"], ["Location", "block"], ["Notifications", "block"], ["Motion sensors", "ask"]];
function SiteControls({ dom, zoom, setZoom, perms, setPerms, level, setLevel, onClose, note, go }) {
  const p = perms[dom] || {};
  const set = (k, v) => { setPerms((m) => ({ ...m, [dom]: { ...(m[dom] || {}), [k]: v } })); note(k + " · " + v + " on " + dom); };
  return (
    <div className="pop" style={{ top: 4, left: 132, width: 312 }}>
      <div className="pop-h">
        <div className="ico" style={{ background: "var(--ac-soft)", color: "var(--ac)" }}><SlidersHorizontal size={15} /></div>
        <div style={{ minWidth: 0 }}><div className="t">Site controls</div><div className="s mono">{dom}</div></div>
      </div>
      <div className="sc-zoom">
        <span>Zoom</span>
        <button onClick={() => setZoom(Math.max(0.5, +(zoom - 0.1).toFixed(2)))}>−</button>
        <b className="mono">{Math.round(zoom * 100)}%</b>
        <button onClick={() => setZoom(Math.min(2, +(zoom + 0.1).toFixed(2)))}>+</button>
        <button className="sc-reset" onClick={() => setZoom(1)}>Reset</button>
      </div>
      <div className="sc-list">
        {SITE_PERMS.map(([k, dflt]) => {
          const v = p[k] || dflt;
          return (
            <div key={k} className="sc-row">
              <span>{k}</span>
              <div className="sc-seg">
                {["allow", "ask", "block"].map((o) => (
                  <button key={o} className={v === o ? "on" : ""} onClick={() => set(k, o)}>{o}</button>
                ))}
              </div>
            </div>
          );
        })}
      </div>
      <div style={{ padding: 6, borderTop: "1px solid var(--line)" }}>
        <button className="mitem" onClick={() => { setLevel(level === "off" ? "standard" : "off"); }}>
          <ShieldCheck size={15} />{level === "off" ? "Turn Shield on for this site" : "Turn Shield off for this site"}
        </button>
        <button className="mitem" onClick={() => go("settings", "cookies")}><Cookie size={15} />Clear cookies & site data</button>
      </div>
    </div>
  );
}

/* ---------- capture ---------- */
function CapturePop({ dom, onClose, note }) {
  const [mode, setMode] = useState("visible");
  const box = useRef(null); useFocusTrap(box);
  const shots = [["visible", "Visible area", "What you can see right now"], ["full", "Full page", "Scrolls and stitches the whole document"], ["region", "Selection", "Drag a box over the part you want"]];
  return (
    <div className="ovl" onClick={onClose}>
      <div className="capt" ref={box} role="dialog" aria-modal="true" aria-label="Capture" tabIndex={-1} onClick={(e) => e.stopPropagation()}>
        <div className="cap-h"><Camera size={15} color="var(--ac)" /><div>Capture<span className="mono">{dom}</span></div>
          <button onClick={onClose}><X size={14} /></button></div>
        <div className="cap-modes">
          {shots.map(([id, t, d]) => (
            <button key={id} className={"cap-m" + (mode === id ? " on" : "")} onClick={() => setMode(id)}>
              <b>{t}</b><span>{d}</span>
            </button>
          ))}
        </div>
        <div className="cap-prev"><div className="cap-frame"><span className="mono">{mode === "full" ? "1440 × 4200" : mode === "region" ? "drag to select" : "1440 × 780"}</span></div></div>
        <div className="cap-act">
          <button className="btn gho" onClick={() => { note("Copied to clipboard"); onClose(); }}><Copy size={13} />Copy</button>
          <button className="btn gho" onClick={() => { note("Saved to Downloads"); onClose(); }}><Download size={13} />Save</button>
          <button className="btn-pri" onClick={() => { note("Opened in annotator — draw, arrow, blur"); onClose(); }}><Sparkles size={13} />Annotate</button>
        </div>
      </div>
    </div>
  );
}

/* ---------- focus session ---------- */
const FOCUS_BLOCK = ["news.ycombinator.com", "x.com", "reddit.com", "youtube.com"];
function FocusPanel({ mins, setMins, running, setRunning, left, goal, setGoal, onClose, note }) {
  const box = useRef(null); useFocusTrap(box);
  return (
    <div className="ovl" onClick={onClose}>
      <div className="focus" ref={box} role="dialog" aria-modal="true" aria-label="Focus session" tabIndex={-1} onClick={(e) => e.stopPropagation()}>
        <div className="fo-h"><Circle size={15} color="var(--ac)" /><div>Focus session<span className="mono">{running ? "running" : "not started"}</span></div>
          <button onClick={onClose}><X size={14} /></button></div>
        {running ? (
          <>
            <div className="fo-time mono">{String(Math.floor(left / 60)).padStart(2, "0")}:{String(left % 60).padStart(2, "0")}</div>
            <div className="fo-goal">{goal || "No goal set"}</div>
            <div className="fo-ring"><i style={{ width: (100 - (left / (mins * 60)) * 100) + "%" }} /></div>
            <div className="fo-blocked">{FOCUS_BLOCK.length} sites held back until you finish</div>
            <div className="cap-act"><button className="btn gho" onClick={() => { setRunning(false); note("Session ended early"); }}>Stop</button></div>
          </>
        ) : (
          <>
            <input className="fo-in" placeholder="What are you working on?" value={goal} onChange={(e) => setGoal(e.target.value)} />
            <div className="fo-mins">
              {[15, 25, 45, 90].map((m) => (
                <button key={m} className={mins === m ? "on" : ""} onClick={() => setMins(m)}>{m}m</button>
              ))}
            </div>
            <div className="fo-list">
              <div className="fo-lt">Held back while you focus</div>
              {FOCUS_BLOCK.map((d) => <span key={d} className="fo-chip mono">{d}</span>)}
            </div>
            <div className="cap-act">
              <button className="btn-pri" onClick={() => { setRunning(true); note("Focus session started · " + mins + " minutes"); }}>
                <Circle size={13} />Start {mins} minutes
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

/* ---------- workspace export (.turing) ---------- */
function WorkspaceSec({ tabs, spaces, spaceId, reading, notesBySpace, layouts, agentCaps, watches, agentLog, note }) {
  const [inc, setInc] = useState({ tabs: true, spaces: true, reading: true, notes: true, layouts: true, agents: true, vault: false });
  const doc = useMemo(() => {
    const o = { format: "turing/1.0", exported: new Date().toISOString().slice(0, 19) + "Z", space: spaceId };
    if (inc.tabs) o.tabs = tabs.filter((t) => t.url !== "nova://newtab").map((t) => ({ url: t.url, title: t.label || t.title, group: t.group || null }));
    if (inc.spaces) o.spaces = spaces.map((x) => ({ id: x.id, name: x.name }));
    if (inc.reading) o.reading = reading.map((r) => ({ url: r.url, title: r.title, read: r.read }));
    if (inc.notes) o.notes = notesBySpace;
    if (inc.layouts) o.layouts = layouts || {};
    if (inc.agents) o.agents = {
      capabilities: AGENT_CAPS.reduce((m, c) => { m[c[0]] = (agentCaps || {})[c[0]] || c[3]; return m; }, {}),
      watching: (watches || []).map((w) => ({ url: w.url, every: w.every })),
      log: (agentLog || []).slice(0, 20).map((e) => ({ t: e.t, agent: e.agent, action: e.verb + " " + e.target, status: e.status })),
    };
    if (inc.vault) o.vault = "<encrypted blob omitted>";
    return o;
  }, [inc, tabs, spaces, spaceId, reading, notesBySpace, layouts, agentCaps, watches, agentLog]);
  const json = JSON.stringify(doc, null, 2);
  return (
    <>
      <div className="ptitle">Workspace & export</div>
      <div className="psub">Everything Turing knows about this project, in a documented plain-text format. No lock-in: read it, diff it, hand it to an agent.</div>
      <div className="sect"><div className="sect-h">What to include</div>
        <div className="card">
          {[["tabs", "Open tabs", "URLs, titles and group membership"],
            ["spaces", "Spaces", "Names and ids"],
            ["reading", "Reading list", "Saved pages and read state"],
            ["notes", "Project notes", "Per-space scratchpads"],
            ["layouts", "Saved layouts", "Named split arrangements"],
            ["agents", "Agent activity & rules", "The log, capabilities and watches"],
            ["vault", "Passwords", "Exported encrypted — never in the clear"]].map(([k, t, d]) => (
            <Row key={k} icon={<FileText size={16} />} title={t} desc={d}>
              <Toggle on={inc[k]} onClick={() => setInc((m) => ({ ...m, [k]: !m[k] }))} />
            </Row>
          ))}
        </div>
      </div>
      <div className="sect"><div className="sect-h">Preview · workspace.turing</div>
        <pre className="wsjson mono">{json.length > 1800 ? json.slice(0, 1800) + "\n  …" : json}</pre>
        <div className="ws-act">
          <span className="mono">{(json.length / 1024).toFixed(1)} KB</span>
          <button className="btn gho" onClick={() => { try { navigator.clipboard && navigator.clipboard.writeText(json); } catch (e) {} note("Copied workspace.turing"); }}><Copy size={13} />Copy</button>
          <button className="btn-pri" onClick={() => note("Saved workspace.turing to Downloads")}><Download size={13} />Export</button>
        </div>
      </div>
      <div className="sect"><div className="sect-h">Import</div>
        <div className="wsdrop" onClick={() => note("Pick a .turing file — tabs, spaces and notes are restored, nothing is replayed")}>
          <Download size={18} color="var(--tx3)" />
          <b>Drop a .turing file</b>
          <span>Restores tabs, spaces, notes and layouts. Existing work is kept — imports land in a new space.</span>
        </div>
      </div>
    </>
  );
}

/* ---------- agent schedules ---------- */
const SCHED0 = [
  { id: 1, name: "Morning triage", when: "Weekdays · 8:00", task: "Summarise new Linear issues assigned to me", on: true, last: "today 8:00", runs: 34 },
  { id: 2, name: "Deploy watch", when: "Every 30 min", task: "Check Vercel for failed builds, notify on failure", on: true, last: "22 min ago", runs: 612 },
  { id: 3, name: "Friday digest", when: "Fridays · 16:30", task: "Write a week-in-review from my open tabs and notes", on: false, last: "3 weeks ago", runs: 9 },
];
function SchedulesSec({ sched, setSched, onRun, note }) {
  return (
    <>
      <div className="ptitle">Agent schedules</div>
      <div className="psub">Recurring work the agent runs on its own. Every run is dry-run first and writes to the log — nothing consequential happens without your say-so.</div>
      <div className="sect"><div className="sect-h">Schedules</div>
        <div className="schl">
          {sched.map((x) => (
            <div key={x.id} className={"sch" + (x.on ? "" : " off")}>
              <div className="sch-top">
                <b>{x.name}</b>
                <span className="sch-when mono">{x.when}</span>
                <Toggle on={x.on} onClick={() => { setSched((v) => v.map((y) => (y.id === x.id ? { ...y, on: !y.on } : y))); note(x.name + (x.on ? " paused" : " resumed")); }} />
              </div>
              <div className="sch-task">{x.task}</div>
              <div className="sch-foot mono">
                <span>{x.runs} runs</span><span>·</span><span>last {x.last}</span>
                <button onClick={() => onRun(x)}>Run now</button>
              </div>
            </div>
          ))}
        </div>
        <button className="wsdrop small" onClick={() => {
          setSched((v) => [...v, { id: Date.now(), name: "New schedule", when: "Daily · 9:00", task: "Describe what the agent should do", on: false, last: "never", runs: 0 }]);
          note("Schedule added — set it up below");
        }}><Plus size={15} /><b>New schedule</b></button>
      </div>
    </>
  );
}

/* ---------- agent accountability: data ---------- */
const AGENT_CAPS = [
  ["read", "Read page content", "See what is on a page you have open", "allow"],
  ["nav", "Open and close tabs", "Move around on its own", "allow"],
  ["fill", "Fill forms", "Type into fields — you still press send", "ask"],
  ["creds", "Use saved passwords", "Unlock a site with your vault", "ask"],
  ["download", "Download files", "Save things to your machine", "ask"],
  ["post", "Submit and post", "Anything another person would see", "ask"],
  ["spend", "Spend money", "Checkouts, invoices, transfers", "never"],
];
const CAP_ORDER = ["allow", "ask", "never"];
const AGENTLOG0 = [
  { id: 9, t: "08:02", agent: "Morning triage", verb: "Summarised", target: "7 new Linear issues", site: "linear.app", status: "applied", detail: "Read the issue list, grouped by project, wrote a digest into Project notes.", diff: [["Project notes", "412 words", "596 words"]] },
  { id: 8, t: "07:41", agent: "Deploy watch", verb: "Checked", target: "12 recent builds", site: "vercel.com", status: "applied", detail: "All builds green. Nothing to report, so nothing was sent.", diff: [] },
  { id: 7, t: "yesterday", agent: "Ask Turing", verb: "Blocked", target: "payment form submit", site: "stripe.com", status: "blocked", detail: "The agent tried to submit a payment form. Spend money is set to never, so it stopped and asked.", diff: [] },
  { id: 6, t: "yesterday", agent: "Friday digest", verb: "Drafted", target: "week-in-review", site: "notion.com", status: "dryrun", detail: "Dry run only — the draft was written to a scratch page, not published.", diff: [["notion.com/week-47", "(empty)", "1,240 word draft"]] },
  { id: 5, t: "2 days ago", agent: "Morning triage", verb: "Filled", target: "standup form", site: "intranet.wades.local", status: "undone", detail: "Filled the standup form from yesterday's notes. You undid this.", diff: [["Standup field", "(empty)", "3 bullet points"]] },
];
const AGL_STATUS = {
  applied: ["Applied", "var(--good)"],
  dryrun: ["Dry run", "var(--ac)"],
  blocked: ["Blocked", "var(--bad)"],
  pending: ["Waiting on you", "var(--warn)"],
  undone: ["Undone", "var(--tx3)"],
};
const WATCH0 = [
  { id: 1, url: "vercel.com/nova/deployments", label: "Deploys", every: "5 min", last: "3 min ago", changed: true },
  { id: 2, url: "linear.app/nova/team", label: "Team board", every: "30 min", last: "12 min ago", changed: false },
  { id: 3, url: "intranet.wades.local/oncall", label: "On-call rota", every: "1 hour", last: "41 min ago", changed: false },
];
const CONNS0 = [
  { id: 1, name: "Linear", scopes: ["read issues", "comment"], on: true, last: "8 min ago" },
  { id: 2, name: "GitHub", scopes: ["read repos", "open PRs"], on: true, last: "1 hour ago" },
  { id: 3, name: "Vercel", scopes: ["read deployments"], on: true, last: "3 min ago" },
  { id: 4, name: "Mercury", scopes: ["read balance"], on: false, last: "never" },
  { id: 5, name: "Local filesystem", scopes: ["read ~/projects"], on: false, last: "never" },
];

/* ---------- agent activity log ---------- */
function AgentLogSec({ log, setLog, note }) {
  const [f, setF] = useState("all");
  const [open, setOpen] = useState(null);
  const rows = log.filter((e) => f === "all" || e.status === f);
  const counts = { applied: 0, dryrun: 0, blocked: 0, pending: 0 };
  log.forEach((e) => { if (counts[e.status] !== undefined) counts[e.status]++; });
  return (
    <>
      <div className="ptitle">Agent activity</div>
      <div className="psub">Everything an agent did on your behalf, in order, with what changed. Nothing here is a summary written after the fact — it is the receipt.</div>
      <div className="agl-fil">
        {[["all", "Everything"], ["applied", "Applied"], ["dryrun", "Dry run"], ["blocked", "Blocked"]].map(([k, l]) => (
          <button key={k} className={"agl-f" + (f === k ? " on" : "")} onClick={() => setF(k)}>
            {l}{k !== "all" && counts[k] ? <b className="mono">{counts[k]}</b> : null}
          </button>
        ))}
      </div>
      <div className="agl-list">
        {rows.length === 0 && <div className="agl-empty">Nothing {f === "all" ? "logged yet" : "with that status"}.</div>}
        {rows.map((e) => {
          const [label, col] = AGL_STATUS[e.status] || ["", "var(--tx3)"];
          const isOpen = open === e.id;
          return (
            <div key={e.id} className={"agl-row" + (isOpen ? " open" : "")}>
              <button className="agl-head" onClick={() => setOpen(isOpen ? null : e.id)}>
                <i className="agl-dot" style={{ background: col }} />
                <span className="agl-main">
                  <b>{e.verb} {e.target}</b>
                  <span className="mono">{e.agent} · {e.site}</span>
                </span>
                <span className="agl-st" style={{ color: col }}>{label}</span>
                <span className="agl-t mono">{e.t}</span>
                {isOpen ? <ChevronUp size={13} color="var(--tx3)" /> : <ChevronDown size={13} color="var(--tx3)" />}
              </button>
              {isOpen && (
                <div className="agl-body">
                  <p>{e.detail}</p>
                  {e.diff.length > 0 && (
                    <div className="agl-diff">
                      {e.diff.map(([k, a, b2], i) => (
                        <div key={i} className="agl-d">
                          <span className="agl-dk">{k}</span>
                          <span className="agl-da mono">{a}</span>
                          <ArrowUp size={11} color="var(--tx3)" style={{ transform: "rotate(90deg)" }} />
                          <span className="agl-db mono">{b2}</span>
                        </div>
                      ))}
                    </div>
                  )}
                  {e.status === "applied" && (
                    <button className="btn gho" style={{ height: 26 }}
                      onClick={() => { setLog((v) => v.map((x) => (x.id === e.id ? { ...x, status: "undone" } : x))); note("Undone — " + e.verb.toLowerCase() + " " + e.target); }}>
                      <RotateCw size={12} />Undo this
                    </button>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </>
  );
}

/* ---------- agent permissions ---------- */
function AgentPermsSec({ caps, setCaps, note }) {
  const level = (k) => caps[k] || (AGENT_CAPS.find((c) => c[0] === k) || [])[3] || "ask";
  const acting = AGENT_CAPS.filter((c) => c[0] !== "read" && c[0] !== "nav");
  const freeToAct = acting.filter((c) => level(c[0]) === "allow").length;
  return (
    <>
      <div className="ptitle">What agents may do</div>
      <div className="psub">One switch per capability, not one switch per agent. An agent inherits these no matter who started it.</div>
      <div className="acap-post">
        <ShieldCheck size={16} color={freeToAct ? "var(--warn)" : "var(--good)"} />
        <div>
          <b>{freeToAct === 0 ? "Agents can look, but must ask before they act" : freeToAct + " action" + (freeToAct === 1 ? "" : "s") + " can happen without asking"}</b>
          <span>{freeToAct === 0 ? "The safe default. Reading and moving around is free; anything with a consequence stops for you." : "Review these — they will not stop to ask."}</span>
        </div>
      </div>
      <div className="sect"><div className="sect-h">Capabilities</div>
        <div className="acap-list">
          {AGENT_CAPS.map(([k, label, desc]) => {
            const v = level(k);
            return (
              <div key={k} className="acap-row">
                <div className="acap-t"><b>{label}</b><span>{desc}</span></div>
                <div className="acap-seg">
                  {CAP_ORDER.map((o) => (
                    <button key={o} className={v === o ? "on " + o : ""}
                      onClick={() => { setCaps((m) => ({ ...m, [k]: o })); note(label + " · " + o); }}>{o}</button>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </>
  );
}

/* ---------- watched pages ---------- */
function WatchesSec({ watches, setWatches, note }) {
  return (
    <>
      <div className="ptitle">Watched pages</div>
      <div className="psub">Turing re-reads these on a timer and tells you what moved. A watch never clicks anything — it only looks.</div>
      <div className="sect"><div className="sect-h">Watching {watches.length}</div>
        <div className="wch-list">
          {watches.map((w) => (
            <div key={w.id} className={"wch" + (w.changed ? " hit" : "")}>
              <Radio size={14} color={w.changed ? "var(--ac)" : "var(--tx3)"} />
              <div className="wch-t">
                <b>{w.label}{w.changed && <span className="wch-badge">changed</span>}</b>
                <span className="mono">{w.url}</span>
              </div>
              <span className="wch-m mono">every {w.every}<i>checked {w.last}</i></span>
              <button className="wch-x" title="Stop watching"
                onClick={() => { setWatches((v) => v.filter((x) => x.id !== w.id)); note("Stopped watching " + w.label); }}><X size={12} /></button>
            </div>
          ))}
          {watches.length === 0 && <div className="agl-empty">Nothing is being watched.</div>}
        </div>
      </div>
    </>
  );
}

/* ---------- agent connections ---------- */
function ConnectionsSec({ conns, setConns, note }) {
  const on = conns.filter((c) => c.on).length;
  return (
    <>
      <div className="ptitle">Connections</div>
      <div className="psub">The tools an agent can reach beyond the page itself. {on} of {conns.length} are live. Each one lists exactly what it may touch.</div>
      <div className="sect"><div className="sect-h">Connected tools</div>
        <div className="card">
          {conns.map((c) => (
            <Row key={c.id} icon={<Plug size={16} />} title={c.name}
              desc={c.scopes.join(" · ") + " — last used " + c.last}>
              <Toggle on={c.on} onClick={() => { setConns((v) => v.map((x) => (x.id === c.id ? { ...x, on: !x.on } : x))); note(c.name + (c.on ? " disconnected" : " connected")); }} />
            </Row>
          ))}
        </div>
      </div>
    </>
  );
}

/* ---------- agents: a first-class surface, not a preferences group ---------- */
const AGT_TABS = [
  ["activity", "Activity", ScrollText],
  ["rules", "What agents may do", Gavel],
  ["schedules", "Schedules", Sparkles],
  ["watches", "Watched pages", Radio],
  ["connections", "Connections", Plug],
];
function AgentsPage({ sec, setSec, log, setLog, caps, setCaps, sched, setSched, onRunSchedule,
                      watches, setWatches, conns, setConns, pending, onOpenQueue, note }) {
  const applied = log.filter((e) => e.status === "applied").length;
  return (
    <div className="scroll">
      <PageHeader icon={Gavel} title="Agents" chip={applied + " applied · " + log.length + " logged"} maxW={880}>
        {pending > 0 && (
          <button className="btn-pri" style={{ height: 28 }} onClick={onOpenQueue}>
            {pending} waiting on you
          </button>
        )}
      </PageHeader>
      <div className="pcol" style={{ "--colw": "880px" }}>
        <div className="agt-tabs">
          {AGT_TABS.map(([k, label, Ic]) => (
            <button key={k} className={"agt-tab" + (sec === k ? " on" : "")} onClick={() => setSec(k)}>
              <Ic size={14} />{label}
            </button>
          ))}
        </div>
        <div className="agt-body">
          {sec === "activity" && <AgentLogSec log={log} setLog={setLog} note={note} />}
          {sec === "rules" && <AgentPermsSec caps={caps} setCaps={setCaps} note={note} />}
          {sec === "schedules" && <SchedulesSec sched={sched} setSched={setSched} onRun={onRunSchedule} note={note} />}
          {sec === "watches" && <WatchesSec watches={watches} setWatches={setWatches} note={note} />}
          {sec === "connections" && <ConnectionsSec conns={conns} setConns={setConns} note={note} />}
        </div>
      </div>
    </div>
  );
}

/* ---------- approval queue ---------- */
const APPROVE0 = [
  { id: 1, agent: "Deploy watch", verb: "Post", target: "a comment on PR #482", site: "github.com", cap: "post",
    detail: "Build 4c1f failed on main. The agent wants to comment with the failing step and a link to the log.",
    diff: [["PR #482 comments", "14", "15"]] },
  { id: 2, agent: "Morning triage", verb: "Fill", target: "the standup form", site: "intranet.wades.local", cap: "fill",
    detail: "Fills today's standup from your Linear activity and Project notes. It will not press submit.",
    diff: [["Standup draft", "(empty)", "3 bullet points"]] },
];
function ApprovalPop({ items, onDecide, onClose, go }) {
  return (
    <div className="pop apq" style={{ top: 4, right: 8, width: 350 }}>
      <div className="pop-h">
        <div className="ico" style={{ background: "var(--warn-soft,var(--ac-soft))", color: "var(--warn)" }}><Gavel size={15} /></div>
        <div style={{ minWidth: 0 }}>
          <div className="t">Waiting on you</div>
          <div className="s">{items.length ? items.length + " action" + (items.length === 1 ? "" : "s") + " an agent cannot take alone" : "Nothing pending"}</div>
        </div>
      </div>
      <div className="apq-list">
        {items.length === 0 && <div className="apq-empty">You are all caught up. Agents will queue anything they cannot do on their own.</div>}
        {items.map((a) => (
          <div key={a.id} className="apq-it">
            <div className="apq-top">
              <b>{a.verb} {a.target}</b>
              <span className="apq-cap mono">{a.cap}</span>
            </div>
            <div className="apq-meta mono">{a.agent} · {a.site}</div>
            <p className="apq-d">{a.detail}</p>
            {a.diff.map(([k, x, y], i) => (
              <div key={i} className="apq-diff mono"><span>{k}</span><i>{x}</i><ArrowUp size={10} style={{ transform: "rotate(90deg)" }} /><b>{y}</b></div>
            ))}
            <div className="apq-act">
              <button className="apq-no" onClick={() => onDecide(a, false)}><Ban size={12} />Deny</button>
              <button className="apq-yes" onClick={() => onDecide(a, true)}><Check size={12} />Approve once</button>
            </div>
          </div>
        ))}
      </div>
      <div className="apq-foot">
        <button className="mitem" onClick={() => { onClose(); go("agents", "rules"); }}><Gavel size={15} />Change what agents may do</button>
        <button className="mitem" onClick={() => { onClose(); go("agents", "activity"); }}><ScrollText size={15} />See the full activity log</button>
      </div>
    </div>
  );
}

/* ---------- command palette ---------- */
const CMDS = [
  ["nav", "New Tab", "Open a fresh tab", Plus, "newtab"],
  ["nav", "History", "Browse everywhere you’ve been", HistoryIcon, "history"],
  ["nav", "Downloads", "Your recent files", Download, "downloads"],
  ["view", "Little Turing", "A throwaway mini window — browse without committing a tab", Columns2, "littlewin"],
  ["view", "Agent Mode", "Typed powers, dry-run first, you confirm every consequential step", Sparkles, "agent"],
  ["view", "Research Canvas", "2–4 linked panes with cited evidence", Columns2, "canvas"],
  ["view", "Time Machine", "Every state of this project, versioned", RotateCw, "timemachine"],
  ["view", "Resource Truth Center", "Every megabyte owned, every freeze explained", Activity, "resources"],
  ["view", "Project details", "Identity, budgets, AI authority, sharing", SlidersHorizontal, "inspector"],
  ["nav", "Import from another browser", "High-fidelity migration with a full report", Download, "migrate"],
  ["nav", "Extensions", "Manage installed extensions", Puzzle, "extensions"],
  ["set", "Settings", "All preferences", Settings, "settings:general"],
  ["set", "Privacy & security", "Trackers, cookies, connection", Shield, "settings:privacy"],
  ["set", "Ad blocker & shields", "Filter lists and blocking", Ban, "settings:shields"],
  ["set", "Cookies & site data", "See and clear stored data", Cookie, "settings:cookies"],
  ["set", "Passwords", "Your vault — logins, passkeys, health check", KeyRound, "settings:passwords"],
  ["set", "Workspace & export", "Everything as plain .turing text", FileText, "settings:workspace"],
  ["view", "Agents", "Activity, rules, schedules and connections", Gavel, "agents:activity"],
  ["view", "Agent activity", "Every action an agent took, with receipts", ScrollText, "agents:activity"],
  ["view", "What agents may do", "Capabilities: look, act, spend", Gavel, "agents:rules"],
  ["view", "Agent schedules", "Recurring work the agent runs on its own", Sparkles, "agents:schedules"],
  ["view", "Watched pages", "Pages Turing re-reads on a timer", Radio, "agents:watches"],
  ["view", "Connections", "Tools an agent can reach", Plug, "agents:connections"],
  ["view", "Waiting on you", "Approve or deny what agents queued", Gavel, "approvals"],
  ["view", "Find on page", "Highlight every match · ⌘F", Search, "find"],
  ["view", "Link hints", "Reach any control from the keyboard · ⌥⌘L", Command, "hints"],
  ["view", "Search all tabs", "Every tab in every space · ⌥⌘A", Layers, "tabsearch"],
  ["view", "Reading list", "What you saved for later · ⌥⌘R", BookOpen, "reading"],
  ["view", "Project notes", "A scratchpad per space · ⇧⌘N", FileText, "notes"],
  ["view", "Task manager", "Memory and CPU per tab · ⇧⌘M", Activity, "taskm"],
  ["view", "Capture", "Screenshot the page · ⇧⌘4", Camera, "capture"],
  ["view", "Focus session", "A timer that holds back the noise · ⌥⌘F", Circle, "focus"],
  ["view", "Site controls", "Permissions and zoom for this site", SlidersHorizontal, "sitectl"],
  ["set", "Password generator", "Make a strong one and copy it", Dices, "settings:passwords"],
  ["set", "Performance", "Memory saver, preload, GPU", Gauge, "settings:performance"],
  ["set", "Appearance", "Theme, accent, and tab position", Palette, "settings:appearance"],
  ["set", "Developer", "Turn developer tools on or off", Terminal, "settings:developer"],
  ["view", "Zen mode", "Hide everything but the page", Eye, "zen"],
  ["view", "Reader mode", "Strip the page down to just the words", BookOpen, "reader"],
  ["view", "Split view", "See this page beside another", Columns2, "split"],
  ["nav", "Copy current address", "Put this page’s link on your clipboard", Link, "copy"],
  ["set", "Toggle theme", "Switch between dark and light", Palette, "theme"],
  ["nav", "Bookmark this page", "Save it to your bookmarks bar", Bookmark, "mark"],
  ["view", "Ask Turing", "Chat with your tabs — @ to add context", Sparkles, "ai"],
  ["nav", "Switch space", "Flip between Work and Personal", RefreshCw, "space"],
  ["nav", "Save to reading list", "Keep this page for later · ⇧⌘D", BookOpen, "later"],
  ["view", "Boost this site", "Give it your accent — Nova remembers per site", Palette, "boost"],
  ["view", "Translate this page", "To English, with one-tap original", Globe, "translate"],
  ["nav", "Organize tabs", "Nova groups similar tabs, names included", LayoutGrid, "organize"],
  ["view", "Translate page", "Into English — instantly", Globe, "translate"],
  ["view", "Tidy tabs", "Close tabs you haven’t touched in a while", Sparkles, "tidy"],
  ["dev", "DevTools", "Elements, console, network, sources & more", Terminal, "dock:elements"],
  ["dev", "Elements", "Inspect structure & styles", Code, "dock:elements"],
  ["dev", "Sources", "Debug with breakpoints", FileCode, "dock:sources"],
  ["dev", "Performance", "Flame chart & web vitals", Activity, "dock:performance"],
  ["dev", "Lighthouse", "Audit scores & opportunities", Gauge, "dock:lighthouse"],
  ["dev", "Network", "Requests, sizes, waterfall", Wifi, "dock:network"],
  ["dev", "Console", "Logs for this page", Terminal, "dock:console"],
  ["dev", "Hard reload", "Bypass the cache", RotateCw, "noop"],
  ["dev", "Copy as cURL", "Reproduce the request", CornerDownLeft, "noop"],
  ["sec", "Security report", "Connection posture & connections", ShieldCheck, "dock:security"],
  ["sec", "Clear cookies & site data", "For the current site", Trash2, "noop"],
  ["sec", "Open private tab", "Ephemeral · no history", Eye, "noop"],
  ["view", "Keyboard shortcuts", "Every binding", Command, "shortcuts"],
];

const UNIT = { mi: ["km", 1.60934], km: ["mi", 0.621371], kg: ["lb", 2.20462], lb: ["kg", 0.453592], lbs: ["kg", 0.453592], ft: ["m", 0.3048], m: ["ft", 3.28084] };
function instantAnswer(q) {
  const zen = q.match(/^zen\s+(\d{1,3})$/i);
  if (zen) return { type: "zentimer", n: +zen[1] };
  const u = q.match(/^([\d.]+)\s*(mi|km|kg|lbs?|ft|m)\s+to\s+(mi|km|kg|lbs?|ft|m)$/i);
  if (u) {
    const [, n, from] = u; const conv = UNIT[from.toLowerCase()];
    if (conv) return { type: "answer", text: `${(+n * conv[1]).toFixed(2)} ${conv[0]}`, sub: q };
  }
  const c = q.match(/^([\d.]+)\s*(c|f)\s+to\s+(c|f)$/i);
  if (c) { const n = +c[1]; const f = c[2].toLowerCase() === "c" ? n * 9 / 5 + 32 + " °F" : ((n - 32) * 5 / 9).toFixed(1) + " °C"; return { type: "answer", text: String(f), sub: q }; }
  if (/^[\d\s+\-*/().%]+$/.test(q) && /\d/.test(q) && /[+\-*/]/.test(q)) {
    try { const v = Function('"use strict";return (' + q + ")")(); if (isFinite(v)) return { type: "answer", text: String(Math.round(v * 1e6) / 1e6), sub: q }; } catch { }
  }
  return null;
}

const SHORTKEYS = { ai: "⌘E", zen: "⌘⏎", reader: "⌘⇧R", find: "⌘F", split: "⌘\\", copy: "⌘⇧C", newtab: "⌘T", shortcuts: "⌘/" };
function hiText(t, ql) {
  if (!ql) return t;
  const i = t.toLowerCase().indexOf(ql);
  if (i === -1) return t;
  return <>{t.slice(0, i)}<b className="hl">{t.slice(i, i + ql.length)}</b>{t.slice(i + ql.length)}</>;
}
function CommandPalette({ q, setQ, sel, setSel, close, go, openDock, openShortcuts, dev, onHints, onTabSearch, onSide, onTaskm, onCapture, onFocus, onSiteCtl, onApprovals, onZen, onTidy, onNavigate, onSession, onZenTimer, tabs, activeId, onSwitchTab, closed, onReopenAt, onCopy, onReader, onFind, onSplit, onOpenNew, onCloseTab, onNewTab, shieldOn, onTheme, onMark, onAI, onOrganize, onSpace, onLater, onBoost, onTranslate, onLittleWin, onInspector, layouts, splitOpen, onSaveLayout, onApplyLayout, onForgetLayout }) {
  const [acts, setActs] = useState(false);
  const list = useMemo(() => {
    const ql = q.trim().toLowerCase();
    const others = (tabs || []).filter((t) => t.id !== activeId);
    const tabItems = others
      .filter((t) => !ql || (t.label || t.title).toLowerCase().includes(ql) || t.url.toLowerCase().includes(ql))
      .slice(0, ql ? 4 : 3)
      .map((t) => ["tab", t.label || t.title, t.url, LayoutGrid, "tab:" + t.id]);
    const closedItems = (closed || [])
      .map((t, i) => [t, i]).reverse().slice(0, 3)
      .filter(([t]) => !ql || t.title.toLowerCase().includes(ql))
      .map(([t, i]) => ["closed", t.label || t.title, t.url, HistoryIcon, "reopenat:" + i]);
    const layoutItems = (layouts || [])
      .map((l, i) => [l, i])
      .filter(([l]) => !ql || l.name.toLowerCase().includes(ql) || "layout".includes(ql))
      .slice(0, 4)
      .map(([l, i]) => ["layout", l.name, l.ld + " · " + l.rd + " — " + Math.round(l.ratio * 100) + "/" + Math.round((1 - l.ratio) * 100), Columns2, "layout:" + i]);
    const saveItem = splitOpen && (!ql || "save this layout".includes(ql)) ? [["layout", "Save this layout", "Remember both panes and their size for this space", Columns2, "savelayout"]] : [];
    const base = CMDS.filter(([g, t, s, , dest]) => {
      if (!dev && (g === "dev" || String(dest).startsWith("dock:"))) return false;
      return !ql || t.toLowerCase().includes(ql) || s.toLowerCase().includes(ql);
    });
    if (ql) {
      const ia = instantAnswer(q.trim());
      const head = [];
      if (ia && ia.type === "answer") head.push(["answer", "= " + ia.text, ia.sub, Sparkles, "noop"]);
      if (ia && ia.type === "zentimer") head.push(["answer", `Focus for ${ia.n} minute${ia.n === 1 ? "" : "s"}`, "Zen until the timer ends · Esc to leave early", Eye, "zentimer:" + ia.n]);
      head.push(["nav", `Go to “${q.trim()}”`, "Open address or search the web", Globe, "go:" + q.trim()]);
      return [...head, ...layoutItems, ...saveItem, ...tabItems, ...closedItems, ...base];
    }
    // zero-typing: most navigation should need no keystrokes at all
    const recents = HISTORY.slice(0, 3).map((h) => ["recent", h.t, h.u, HistoryIcon, "go:" + h.u]);
    const tops = QUICKS.slice(0, 4).map((s) => ["top", s.name, "Open", Globe, "go:" + s.name.toLowerCase().replace(/\s/g, "") + ".com"]);
    const session = [["session", "Resume yesterday", "Reopen your last session — 4 tabs", RefreshCw, "session"]];
    const closedZ = closedItems.length ? closedItems : [];
    return [...layoutItems, ...saveItem, ...tabItems, ...recents, ...tops, ...closedZ, ...session, ...base];
  }, [q, dev, tabs, activeId, closed, layouts, splitOpen]);

  useEffect(() => { if (sel >= list.length) setSel(Math.max(0, list.length - 1)); }, [list.length, sel, setSel]);

  useEffect(() => {
    const on = (e) => {
      if (e.key === "ArrowDown") { e.preventDefault(); setSel((s) => Math.min(list.length - 1, s + 1)); }
      if (e.key === "ArrowUp") { e.preventDefault(); setSel((s) => Math.max(0, s - 1)); }
      if (e.key === "Enter") { e.preventDefault(); run(list[sel]); }
    };
    window.addEventListener("keydown", on);
    return () => window.removeEventListener("keydown", on);
  }, [list, sel]);

  const run = (c) => {
    if (!c) return;
    const dest = c[4];
    if (dest.startsWith("go:")) onNavigate(dest.slice(3));
    else if (dest.startsWith("tab:")) onSwitchTab(+dest.slice(4));
    else if (dest.startsWith("reopenat:")) onReopenAt(+dest.split(":")[1]);
    else if (dest === "copy") onCopy();
    else if (dest === "reader") onReader();
    else if (dest === "find") { close(); onFind(); }
    else if (dest === "hints") { close(); onHints(); }
    else if (dest === "tabsearch") { close(); onTabSearch(); }
    else if (dest === "reading") { close(); onSide("reading"); }
    else if (dest === "notes") { close(); onSide("notes"); }
    else if (dest === "taskm") { close(); onTaskm(); }
    else if (dest === "capture") { close(); onCapture(); }
    else if (dest === "focus") { close(); onFocus(); }
    else if (dest === "sitectl") { close(); onSiteCtl(); }
    else if (dest === "approvals") { close(); onApprovals(); }
    else if (dest === "split") onSplit();
    else if (dest === "theme") onTheme();
    else if (dest === "mark") { onMark(); close(); }
    else if (dest === "ai") onAI();
    else if (dest === "organize") onOrganize();
    else if (dest === "translate") onTranslate();
    else if (dest === "space") onSpace();
    else if (dest === "later") onLater();
    else if (dest === "littlewin") onLittleWin();
    else if (dest === "inspector") { onInspector(); close(); }
    else if (dest === "boost") onBoost();
    else if (dest.startsWith("zentimer:")) onZenTimer(+dest.split(":")[1]);
    else if (dest === "session") onSession();
    else if (dest.startsWith("agents:")) go("agents", dest.split(":")[1]);
    else if (dest.startsWith("settings:")) go("settings", dest.split(":")[1]);
    else if (dest.startsWith("dock:")) openDock(dest.split(":")[1]);
    else if (dest === "shortcuts") openShortcuts();
    else if (dest === "zen") onZen();
    else if (dest === "tidy") onTidy();
    else if (dest.startsWith("layout:")) { onApplyLayout(+dest.split(":")[1]); close(); }
    else if (dest === "savelayout") { onSaveLayout(); close(); }
    else if (dest === "noop") close();
    else go(dest);
    close();   // a command has run — the dialog should never linger behind it
  };

  const GNAMES = { nav: "Navigate", set: "Settings", dev: "Developer", sec: "Security", view: "View", recent: "Recents", top: "Top sites", session: "Sessions", answer: "Answer", tab: "Switch to", closed: "Recently closed", layout: "Layouts" };
  const TAGS = { nav: "Command", set: "Setting", dev: "Developer", sec: "Security", view: "Command", recent: "History", top: "Site", session: "Session", answer: "Answer", tab: "Open tab", closed: "Closed tab", layout: "Layout" };
  const selItem = list[sel];
  const ql2 = q.trim().toLowerCase();

  // ⌘K toggles the Actions panel while the dialog is open
  useEffect(() => {
    const on = (e) => { if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") { e.preventDefault(); setActs((v) => !v); } };
    window.addEventListener("keydown", on);
    return () => window.removeEventListener("keydown", on);
  }, []);
  useEffect(() => { setActs(false); }, [sel, q]);

  const itemActions = (c) => {
    if (!c) return [];
    const [g, t, s, , dest] = c;
    if (g === "tab") return [
      { l: "Switch to tab", f: () => run(c) },
      { l: "Split with this tab", f: () => { onSplit(+dest.slice(4)); } },
      { l: "Close tab", f: () => { onCloseTab(+dest.slice(4)); setActs(false); } },
    ];
    if (String(dest).startsWith("go:")) return [
      { l: "Open here", f: () => run(c) },
      { l: "Open in new tab", f: () => onOpenNew(dest.slice(3)) },
    ];
    if (g === "layout" && String(dest).startsWith("layout:")) return [
      { l: "Open layout", f: () => run(c) },
      { l: "Forget layout", f: () => { onForgetLayout(+dest.split(":")[1]); setActs(false); } },
    ];
    if (g === "closed") return [{ l: "Reopen tab", f: () => run(c) }];
    return [{ l: "Run", f: () => run(c) }];
  };

  const counts = {};
  list.forEach(([g]) => { counts[g] = (counts[g] || 0) + 1; });

  const QUICKA = [
    { l: "New tab", I: Plus, f: onNewTab },
    { l: "Copy link", I: Link, f: onCopy },
    { l: "Reader", I: BookOpen, f: onReader },
    { l: "Split", I: Columns2, f: () => onSplit() },
    { l: "Zen", I: Eye, f: onZen },
  ];

  let lastG = null;
  return (
    <div className="cmdveil" onClick={close}>
      <div className="cmd warm" onClick={(e) => e.stopPropagation()}>
        <div className="cmd-in">
          <div className="cin-ic"><Search size={18} /></div>
          <input autoFocus placeholder="Search, type an address, do anything…" value={q}
            onChange={(e) => { setQ(e.target.value); setSel(0); }} />
          <span className="cin-esc mono">esc</span>
        </div>
        <div className="cmd-quick">
          {QUICKA.map(({ l, I, f }) => (
            <button key={l} className="qa" onClick={f}><I size={13} /> {l}</button>
          ))}
        </div>
        <div className="cmd-body">
          <div className="cmd-list">
            {list.length === 0 && <div style={{ padding: 24, textAlign: "center", color: "var(--wtx3)" }}>No matches — press ↵ to search the web.</div>}
            {list.map((c, i) => {
              const [g, t, s, Ic, dest] = c;
              const head = g !== lastG ? (lastG = g, GNAMES[g] || g) : null;
              const sk = SHORTKEYS[dest];
              return (
                <div key={g + t + i}>
                  {head && <div className="cmd-grp">{head}{counts[g] > 1 && <span className="gc">{counts[g]}</span>}</div>}
                  <div className={"cmd-it" + (i === sel ? " sel" : "") + (g === "answer" ? " ans" : "")} onMouseEnter={() => setSel(i)} onClick={() => run(c)}>
                    <div className="ci"><Ic size={16} /></div>
                    <div className="ct">{hiText(t, ql2)}<div className="cs">{hiText(s, ql2)}</div></div>
                    {sk ? <span className="tag2 kb">{sk}</span> : <span className="tag2">{TAGS[g] || ""}</span>}
                  </div>
                </div>
              );
            })}
          </div>
          <div className="cmd-detail">
            {selItem ? (() => {
              const [g, t, s, Ic, dest] = selItem;
              const preview = g === "tab" || g === "top" || g === "recent" || g === "closed" || String(dest).startsWith("go:");
              return (
                <>
                  <div className="cd-ic"><Ic size={26} /></div>
                  <div className="cd-t">{t}</div>
                  <div className="cd-s">{s}</div>
                  {preview && (
                    <div className="cd-prev">
                      <div className="cd-pl" style={{ width: "62%" }} /><div className="cd-pl" style={{ width: "88%" }} />
                      <div className="cd-pl" style={{ width: "74%" }} /><div className="cd-pl" style={{ width: "40%" }} />
                    </div>
                  )}
                  <div className="cd-meta">
                    <div className="cd-row"><span>Type</span><b>{TAGS[g] || "Command"}</b></div>
                    {String(dest).startsWith("go:") && <div className="cd-row"><span>Opens</span><b className="mono">{dest.slice(3).slice(0, 24)}</b></div>}
                    {g === "recent" && <div className="cd-row"><span>Visited</span><b>Today</b></div>}
                    {g === "top" && <div className="cd-row"><span>Why</span><b>You go here often</b></div>}
                    {g === "tab" && <div className="cd-row"><span>Action</span><b>Switch instantly</b></div>}
                    {g === "closed" && <div className="cd-row"><span>Closed</span><b>This session</b></div>}
                    {g === "answer" && <div className="cd-row"><span>Source</span><b>Calculated locally</b></div>}
                    <div className="cd-row"><span>Press</span><b className="mono">{SHORTKEYS[dest] || "↵"}</b></div>
                  </div>
                </>
              );
            })() : <div className="cd-s">Nothing selected</div>}
            {acts && selItem && (
              <div className="actpanel">
                <div className="ap-t">Actions</div>
                {itemActions(selItem).map((a) => <button key={a.l} className="ap-i" onClick={a.f}>{a.l}</button>)}
              </div>
            )}
          </div>
        </div>
        <div className="cmd-foot">
          <span className="cf-brand"><span className="cf-dot" /> Turing</span>
          <span>{(tabs || []).length} tabs · Shield {shieldOn ? "on" : "off"}</span>
          <span style={{ marginLeft: "auto" }}>Open <b>↵</b></span>
          <button className="cf-act" onClick={() => setActs((v) => !v)}>Actions <b>⌘K</b></button>
        </div>
      </div>
    </div>
  );
}

/* ============================================================================
   Developer / security / performance surface
   ========================================================================== */

/* live toolbar readout — isolated interval so only this leaf re-renders */
const PerfPill = memo(function PerfPill({ onClick }) {
  const [m, setM] = useState({ mem: 312, fps: 120 });
  useEffect(() => {
    const id = setInterval(() => setM({ mem: 298 + Math.round(Math.random() * 32), fps: 118 + Math.round(Math.random() * 4) }), 1400);
    return () => clearInterval(id);
  }, []);
  return (
    <button className="perfpill" onClick={onClick} title="Performance · ⌥⌘I">
      <b>{m.mem}</b> MB · <b>{m.fps}</b> fps
    </button>
  );
});

const VITALS = [
  { k: "LCP", v: "0.9s", d: "Largest paint", g: "good" },
  { k: "INP", v: "42ms", d: "Interaction", g: "good" },
  { k: "CLS", v: "0.01", d: "Layout shift", g: "good" },
  { k: "TTFB", v: "120ms", d: "First byte", g: "good" },
  { k: "FCP", v: "0.6s", d: "First paint", g: "good" },
];
const NET = [
  { n: "document", m: "GET", s: 200, t: "doc", sz: "14.2 KB", off: 0, w: 15 },
  { n: "entry.client.tsx", m: "GET", s: 200, t: "script", sz: "88.1 KB", off: 12, w: 24 },
  { n: "chunk-vendor.js", m: "GET", s: 200, t: "script", sz: "142 KB", off: 14, w: 30 },
  { n: "app.css", m: "GET", s: 200, t: "css", sz: "24.6 KB", off: 12, w: 11 },
  { n: "GeistVF.woff2", m: "GET", s: 200, t: "font", sz: "41.0 KB", off: 26, w: 9 },
  { n: "api/session", m: "GET", s: 200, t: "fetch", sz: "1.2 KB", off: 44, w: 7 },
  { n: "api/metrics", m: "POST", s: 204, t: "fetch", sz: "312 B", off: 52, w: 6 },
  { n: "hero.avif", m: "GET", s: 200, t: "img", sz: "62.4 KB", off: 34, w: 21 },
  { n: "analytics.js", m: "GET", s: 0, t: "tracker", sz: "—", blk: true },
  { n: "collect?v=2", m: "GET", s: 0, t: "tracker", sz: "—", blk: true },
  { n: "fbevents.js", m: "GET", s: 0, t: "tracker", sz: "—", blk: true },
  { n: "px.gif", m: "GET", s: 0, t: "tracker", sz: "—", blk: true },
];
const SECCHECKS = [
  ["Protocol", "TLS 1.3"], ["Cipher", "AES-256-GCM"], ["HSTS", "Enabled · preloaded"],
  ["Certificate", "Let’s Encrypt · valid 89d"], ["CSP", "strict-dynamic"],
  ["Mixed content", "None"], ["Referrer-Policy", "strict-origin"], ["Permissions", "camera=(), geolocation=()"],
];
const CONNS = [
  { d: "v0.app", t: "1st", ok: true }, { d: "vercel.com", t: "1st", ok: true },
  { d: "fonts.gstatic.com", t: "3rd", ok: true }, { d: "google-analytics.com", t: "3rd", ok: false },
  { d: "doubleclick.net", t: "3rd", ok: false }, { d: "connect.facebook.net", t: "3rd", ok: false },
];
const LOGS = [
  { lv: "info", ts: "10:02:14", m: "[vite] connecting…" },
  { lv: "info", ts: "10:02:14", m: "[vite] connected." },
  { lv: "log", ts: "10:02:15", m: "↳ Nova shell mounted in 84ms" },
  { lv: "warn", ts: "10:02:15", m: "React DevTools: install the standalone build for a better dev experience" },
  { lv: "log", ts: "10:02:16", m: "[shield] blocked 4 trackers on this page" },
  { lv: "err", ts: "10:02:18", m: "GET https://google-analytics.com/collect  net::ERR_BLOCKED_BY_CLIENT" },
  { lv: "info", ts: "10:02:22", m: "[vite] hot updated: /src/App.tsx" },
];

const LiveVitals = memo(function LiveVitals() {
  const [t, setT] = useState({ fps: 120, heap: 48.2, dom: 1284, evt: 6 });
  useEffect(() => {
    const id = setInterval(() => setT({
      fps: 118 + Math.round(Math.random() * 4),
      heap: +(46 + Math.random() * 6).toFixed(1),
      dom: 1240 + Math.round(Math.random() * 90),
      evt: 4 + Math.round(Math.random() * 5),
    }), 1200);
    return () => clearInterval(id);
  }, []);
  return (
    <>
      <span className="vmini">FPS <b>{t.fps}</b></span>
      <span className="vmini">JS heap <b>{t.heap} MB</b></span>
      <span className="vmini">DOM nodes <b>{t.dom.toLocaleString()}</b></span>
      <span className="vmini">Listeners <b>{t.evt}</b></span>
      <span className="vmini">Main thread <b style={{ color: "var(--good)" }}>idle</b></span>
    </>
  );
});





/* ================= Turing: theme engine ================= */
const THEMES = [
  { id: "turing-light", name: "Turing Light", mode: "light", by: "built-in", vars: {} },
  { id: "turing-dark", name: "Turing Dark", mode: "dark", by: "built-in", vars: {} },
  { id: "nord", name: "Nord", mode: "dark", by: "community", vars: { "--ink": "#2e3440", "--c1": "#3b4252", "--c2": "#434c5e", "--c3": "#4c566a", "--c4": "#576076", "--line": "rgba(216,222,233,.08)", "--line2": "rgba(216,222,233,.15)", "--tx": "#eceff4", "--tx2": "#d8dee9", "--tx3": "#8a93a6" } },
  { id: "gruvbox", name: "Gruvbox", mode: "dark", by: "community", vars: { "--ink": "#1d2021", "--c1": "#282828", "--c2": "#32302f", "--c3": "#3c3836", "--c4": "#504945", "--line": "rgba(235,219,178,.08)", "--line2": "rgba(235,219,178,.16)", "--tx": "#ebdbb2", "--tx2": "#d5c4a1", "--tx3": "#928374", "--good": "#b8bb26", "--warn": "#fabd2f", "--bad": "#fb4934" } },
  { id: "rose-pine", name: "Rosé Pine", mode: "dark", by: "community", vars: { "--ink": "#191724", "--c1": "#1f1d2e", "--c2": "#26233a", "--c3": "#2f2b46", "--c4": "#3b3654", "--line": "rgba(224,222,244,.07)", "--line2": "rgba(224,222,244,.14)", "--tx": "#e0def4", "--tx2": "#c5c3dd", "--tx3": "#6e6a86", "--good": "#9ccfd8", "--warn": "#f6c177", "--bad": "#eb6f92" } },
  { id: "paper", name: "Paper", mode: "light", by: "community", vars: { "--ink": "#f2efe9", "--c1": "#faf8f4", "--c2": "#f1ede6", "--c3": "#e6e0d6", "--c4": "#d6cec1", "--line": "rgba(60,50,30,.09)", "--line2": "rgba(60,50,30,.16)", "--tx": "#2a2418", "--tx2": "#5a5244", "--tx3": "#96907f" } },
];
const FONTS_SANS = [["Geist", '"Geist","Inter",-apple-system,system-ui,sans-serif'], ["Inter", '"Inter",-apple-system,system-ui,sans-serif'], ["System", '-apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif'], ["Atkinson", '"Atkinson Hyperlegible","Inter",system-ui,sans-serif']];
const FONTS_MONO = [["Geist Mono", '"Geist Mono",ui-monospace,"SF Mono",Menlo,monospace'], ["JetBrains", '"JetBrains Mono",ui-monospace,Menlo,monospace'], ["IBM Plex", '"IBM Plex Mono",ui-monospace,Menlo,monospace'], ["Fira Code", '"Fira Code",ui-monospace,Menlo,monospace']];

/* ================= Turing: Research Canvas ================= */
function CanvasPage({ tabs, note }) {
  const [n, setN] = useState(2);
  const [linked, setLinked] = useState(true);
  const [caps, setCaps] = useState([{ q: "Plan pricing starts at $29/user with annual billing.", src: "linear.app/pricing", t: "14:02", v: "v2026-07-14" }]);
  const panes = tabs.filter((t) => t.url !== "nova://newtab").slice(0, n);
  const gridRef = useRef(null);
  const syncing = useRef(false);
  const onScrollCap = (i) => (e) => {
    if (!linked || syncing.current) return;
    if (!e.target.classList || !e.target.classList.contains("scroll")) return;
    const top = e.target.scrollTop;
    syncing.current = true;
    const els = gridRef.current ? [...gridRef.current.querySelectorAll(".cv-pb .scroll")] : [];
    els.forEach((el, x) => { if (x !== i) el.scrollTop = top; });
    requestAnimationFrame(() => { syncing.current = false; });
  };
  const capture = (p) => setCaps((c) => [{ q: "Enterprise tier requires a sales conversation — no listed price.", src: p.url, t: "now", v: "v2026-07-16" }, ...c]);
  return (
    <div className="cv">
      <div className="cv-bar">
        <span className="dt-cap" style={{ padding: 0 }}>Research Canvas</span>
        <span className="seg" style={{ height: 24 }}>{[2, 3, 4].map((k) => <button key={k} className={n === k ? "on" : ""} onClick={() => setN(k)} style={{ fontSize: 11, padding: "0 9px" }}>{k}</button>)}</span>
        <button className={"chip" + (linked ? " on" : "")} onClick={() => setLinked((v) => !v)}>Linked scroll</button>
        <span className="cv-ground mono"><Sparkles size={11} /> AI grounded to these {panes.length} sources only</span>
        <button className="hclear" style={{ marginLeft: "auto", height: 26 }} onClick={() => note("Exported — Markdown with full provenance")}>Export ▾</button>
      </div>
      {panes.length === 0 && <div className="hempty" style={{ flex: 1 }}>Open a couple of pages in this project, then bring them here to compare.</div>}
      <div className="cv-body">
      <div className={"cv-grid n" + n} ref={gridRef}>
        {panes.map((p, i) => (
          <div key={p.id} className="cv-pane">
            <div className="cv-ph mono">{p.url.split("/")[0]}
              <button className="hclear" style={{ height: 20, fontSize: 10, marginLeft: "auto" }} onClick={() => capture(p)}>Capture quote</button>
            </div>
            <div className="cv-pb" onScrollCapture={onScrollCap(i)}>
              <SitePage key={"cv" + p.id} tab={p} zoom={0.7} />
            </div>
          </div>
        ))}
      </div>
      <div className="cv-rail">
        <div className="dt-cap">Evidence · {caps.length}</div>
        {caps.map((c, i) => (
          <div key={i} className="cv-cap">
            <div className="q">“{c.q}”</div>
            <div className="m mono">{c.src} · {c.t} · {c.v}</div>
          </div>
        ))}
        <div className="cv-conflict"><Ban size={12} color="var(--warn)" /> Sources disagree: $29/user vs “contact sales” for the same tier. Both kept, both cited.</div>
        <div className="si-note" style={{ marginTop: "auto" }}>Every claim keeps its source. The test: can you reproduce why you reached this conclusion?</div>
      </div>
      </div>
    </div>
  );
}

/* ================= Turing: Migration & open export ================= */
function MigrationPage({ note }) {
  const [src2, setSrc2] = useState(null);
  const [done, setDone] = useState(false);
  const REPORT = [
    ["Bookmarks (1,204)", "exact", "byte-for-byte, folders kept"],
    ["History (90 days)", "exact", "timestamps preserved"],
    ["Passwords & passkeys", "exact", "via system keychain"],
    ["Tab groups (7)", "transformed", "became Turing folders — colors kept"],
    ["Arc Spaces (3)", "transformed", "became Projects with containers"],
    ["Pinned tabs (5)", "exact", ""],
    ["Split layouts", "transformed", "2-pane maps 1:1 · 3-pane approximated"],
    ["Extension settings", "partial", "4 of 6 had compatible plug-ins"],
    ["uBlock custom filters", "skipped", "Shield covers this — verify your allowlist"],
  ];
  const ICO = { exact: ["✓", "var(--good)"], transformed: ["~", "var(--warn)"], partial: ["◐", "var(--warn)"], skipped: ["✗", "var(--bad)"] };
  return (
    <div className="scroll">
      <PageHeader icon={Download} title="Move in · move out" chip="open format" maxW={780}>
        <button className="hclear" onClick={() => note("Exported .turing bundle — versioned, documented, yours")}>Export .turing</button>
      </PageHeader>
      <div className="page"><div className="pbody pcol" style={{ "--colw": "780px" }}>
      <div className="psub" style={{ marginTop: 18 }}>Migration is a feature, not plumbing.</div>
      <div className="ab-chips" style={{ marginBottom: 20 }}>
        {["high-fidelity import", "nothing silently dropped", "open, documented export", "leaving never costs your work"].map((c) => <span key={c} className="ab-chip mono">{c}</span>)}
      </div>
      {!done ? (
        <div className="mg-pick">
          {["Chrome", "Arc", "Zen", "Edge", "Firefox", "Safari"].map((b) => (
            <button key={b} className={"mg-src" + (src2 === b ? " on" : "")} onClick={() => setSrc2(b)}>{b}</button>
          ))}
          <button className="btn-pri" disabled={!src2} onClick={() => { setDone(true); note("Imported from " + src2 + " — report below"); }}>Import from {src2 || "…"}</button>
        </div>
      ) : (
        <>
          <div className="dt-cap">Migration report · {src2} → Turing</div>
          <div className="card" style={{ padding: "2px 16px", marginTop: 6 }}>
          {REPORT.map(([k, st, why]) => (
            <div key={k} className="mg-row">
              <b style={{ color: ICO[st][1] }} className="mono">{ICO[st][0]}</b><span className="k">{k}</span>
              <span className="st mono">{st}</span><span className="w">{why}</span>
            </div>
          ))}
          </div>
          <div className="si-note" style={{ marginTop: 10 }}>Nothing was silently dropped. Two items ask for your eyes — they’re marked.</div>
        </>
      )}
      <div className="dt-cap" style={{ marginTop: 22 }}>Open export</div>
      <div className="mg-row"><b className="mono" style={{ color: "var(--good)" }}>⇪</b><span className="k">Everything — projects, folders, notes, evidence, settings</span>
        <button className="hclear" style={{ marginLeft: "auto", height: 26 }} onClick={() => note("Exported .turing bundle — versioned, documented, yours")}>Export .turing</button></div>
    </div></div></div>
  );
}

/* ================= Turing: Privacy Receipt ================= */
function ReceiptPop({ domain, close }) {
  return (
    <div className="pop" style={{ top: 4, left: 170, width: 330, maxHeight: 480, overflowY: "auto" }}>
      <div className="pop-h"><div className="ico" style={{ background: "var(--ac-soft)", color: "var(--ac)" }}><FileCode size={15} /></div>
        <div><div className="t">Privacy receipt · {domain}</div><div className="s">Everything this page did — inspectable, provider-neutral</div></div>
        <button className="ib" style={{ width: 24, height: 24, marginLeft: "auto" }} onClick={close}><X size={13} /></button>
      </div>
      <div style={{ padding: "6px 12px 12px" }}>
        {[["Network", "9 destinations · 2 countries · 2 blocked by Shield"],
          ["Cookies & storage", "3 first-party · 0 third-party · 1.1 MB"],
          ["Permissions", "none used this visit"],
          ["Plug-in observations", "Shield read the request list — nothing else"],
          ["AI data", "none sent — no agent touched this page"],
          ["Credentials", "1 used via handle · secret never left the vault"],
          ["Retention", "cleared when this project closes"],
          ["Provenance", "C2PA — publisher-signed images ✓"]].map(([k, v]) => (
          <div key={k} className="si-kv"><span>{k}</span><b>{v}</b></div>
        ))}
      </div>
    </div>
  );
}

/* ================= Turing: Resource Truth Center ================= */
function ResourcesPage({ note }) {
  const [rows, setRows] = useState([
    { own: "Work · linear.app", kind: "tab", mem: 312, cpu: 4.1, gpu: 18, net: "2.1 KB/s", st: "active", why: null, prot: ["unsaved form"] },
    { own: "Work · mercury.com", kind: "tab", mem: 188, cpu: 0.4, gpu: 0, net: "—", st: "active", why: null, prot: [] },
    { own: "Work · github.com", kind: "tab", mem: 96, cpu: 0, gpu: 0, net: "—", st: "frozen", why: "inactive 22 min · saves 210 MB · restore: exact scroll, ~instant", prot: [] },
    { own: "Work · agent task #12", kind: "agent", mem: 74, cpu: 1.2, gpu: 0, net: "0.3 KB/s", st: "active", why: null, prot: [], ai: "8.2k tokens · $0.03 · claude · 240 ms p50" },
    { own: "Shield (plug-in)", kind: "plugin", mem: 22, cpu: 0.1, gpu: 0, net: "—", st: "active", why: null, prot: [] },
    { own: "Personal · youtube.com", kind: "tab", mem: 401, cpu: 2.0, gpu: 34, net: "1.4 MB/s", st: "protected", why: null, prot: ["audio playing"] },
    { own: "Browser UI", kind: "ui", mem: 138, cpu: 0.8, gpu: 12, net: "—", st: "active", why: null, prot: [] },
    { own: "Shared GPU service", kind: "svc", mem: 89, cpu: 0.2, gpu: 22, net: "—", st: "active", why: null, prot: [] },
  ]);
  const [sel, setSel] = useState(2);
  const toggleFreeze = (i) => {
    setRows((rs) => rs.map((r, x) => x !== i ? r : r.st === "frozen"
      ? { ...r, st: "active", why: null }
      : r.prot.length ? (note("Protected: " + r.prot[0] + " — will not freeze"), r)
      : { ...r, st: "frozen", why: "frozen by you · saves " + Math.round(r.mem * 0.7) + " MB · restore: exact scroll, ~instant" }));
  };
  const tot = rows.reduce((a, r) => a + r.mem, 0);
  return (
    <div className="scroll">
      <PageHeader icon={Activity} title="Resources" chip={(tot / 1000).toFixed(1) + " GB attributed"} maxW={940}>
        <button className="hclear" onClick={() => note("Idle tabs will explain themselves before freezing")}>Freeze idle…</button>
      </PageHeader>
      <div className="page"><div className="pbody pcol" style={{ "--colw": "940px" }}>
      <div className="psub" style={{ marginTop: 18 }}>Every megabyte has an owner and every freeze has a reason.</div>
      <div className="ab-chips" style={{ marginBottom: 18 }}>
        {["attributed, not estimated", "explained before it acts", "protected work never sleeps", "agent spend visible"].map((c) => <span key={c} className="ab-chip mono">{c}</span>)}
      </div>
      <div className="card" style={{ overflow: "hidden" }}>
      <div className="rt-hd"><span>Owner</span><span>Memory</span><span>CPU</span><span>GPU</span><span>Network</span><span>State</span></div>
      {rows.map((r, i) => (
        <div key={r.own}>
          <div className={"rt-row" + (sel === i ? " on" : "")} onClick={() => setSel(sel === i ? null : i)}>
            <span className="o">{r.own}<i className={"rt-kind mono"}>{r.kind}</i></span>
            <span className="mono">{r.mem} MB</span><span className="mono">{r.cpu}%</span><span className="mono">{r.gpu ? r.gpu + "%" : "—"}</span><span className="mono">{r.net}</span>
            <span className={"rt-st " + r.st}>{r.st}{r.prot.map((p) => <i key={p} className="rt-prot">{p}</i>)}</span>
          </div>
          {sel === i && (
            <div className="rt-detail">
              {r.why && <div className="si-kv"><span>Why</span><b>{r.why}</b></div>}
              {r.ai && <div className="si-kv"><span>Model</span><b className="mono">{r.ai}</b></div>}
              {!r.why && !r.ai && <div className="si-kv"><span>Lifecycle</span><b>active — will only freeze with an explanation first</b></div>}
              {r.kind === "tab" && <button className="hclear" style={{ marginTop: 8 }} onClick={(e) => { e.stopPropagation(); toggleFreeze(i); }}>{r.st === "frozen" ? "Wake — restores exactly" : "Freeze now — shows savings first"}</button>}
            </div>
          )}
        </div>
      ))}
      <div className="tfoot"><span className="mono">{rows.length} owners</span><span className="mono">{(tot / 1000).toFixed(1)} GB attributed</span><span className="mono">{rows.filter((r) => r.st === "frozen").length} frozen · {rows.filter((r) => r.prot.length).length} protected</span><span className="mono" style={{ marginLeft: "auto" }}>agent spend today $0.03</span></div>
      </div>
    </div></div></div>
  );
}

/* ================= Turing: Trustworthy Agent Mode ================= */
function AgentPage({ tabs, note, onAgentTabs, onOpenTab }) {
  const [task, setTask] = useState("Find the two invoices over $500 on Mercury and draft (don’t send) a reminder for each.");
  const [scope, setScope] = useState(["mercury.com"]);
  const [plan, setPlan] = useState(null);   // null | steps[]
  const [running, setRunning] = useState(false);
  const [confirmStep, setConfirmStep] = useState(null);
  const [done, setDone] = useState(false);
  const doms = [...new Set(tabs.filter((t) => t.url !== "nova://newtab").map((t) => t.url.split("/")[0]))].slice(0, 5);
  // surface agent activity in the tab strip: the work is visible where the work is
  useEffect(() => {
    if (!onAgentTabs) return;
    const ids = running || confirmStep !== null
      ? tabs.filter((t) => scope.includes(t.url.split("/")[0])).map((t) => t.id) : [];
    const wait = confirmStep !== null;
    onAgentTabs((prev) => (prev.ids.join(",") === ids.join(",") && prev.wait === wait ? prev : { ids, wait }));
  }, [running, confirmStep, scope, tabs, onAgentTabs]);
  const STEPS = [
    { n: "Open mercury.com/invoices", cap: "navigate", risk: 0 },
    { n: "Read invoice table (page text only)", cap: "read", risk: 0 },
    { n: "Extract invoices where amount > $500", cap: "extract", risk: 0 },
    { n: "Draft reminder for each — saved to Notes", cap: "compose", risk: 1 },
  ];
  const dryRun = () => { setPlan(STEPS.map((s) => ({ ...s, st: "planned" }))); setDone(false); };
  const run = () => {
    if (!plan) return;
    if (onOpenTab) scope.forEach((d) => onOpenTab(d));
    setRunning(true);
    let i = 0;
    const step = () => {
      if (i >= plan.length) { setRunning(false); setDone(true); note("Postconditions verified · 2 drafts in Notes · nothing sent"); return; }
      if (plan[i].risk && confirmStep === null) { setConfirmStep(i); return; }
      setPlan((p) => p.map((s, x) => x === i ? { ...s, st: "done" } : x === i + 1 ? { ...s, st: "running" } : s));
      i++; setTimeout(step, 420);
    };
    setPlan((p) => p.map((s, x) => x === 0 ? { ...s, st: "running" } : s));
    setTimeout(step, 420);
  };
  const allow = () => {
    const i = confirmStep; setConfirmStep(null);
    setPlan((p) => p.map((s, x) => x <= i ? { ...s, st: "done" } : s));
    setRunning(false); setDone(true); note("Postconditions verified · 2 drafts in Notes · nothing sent");
  };
  return (
    <div className="scroll">
      <PageHeader icon={Sparkles} title="Agent Mode" chip={running ? "running" : plan ? "plan ready" : "idle"} maxW={920}>
        <button className="hclear" style={{ color: "var(--bad)" }} onClick={() => { setPlan(null); setRunning(false); setConfirmStep(null); note("Agent stopped · grants revoked"); }}>Stop & revoke</button>
      </PageHeader>
      <div className="page"><div className="pbody pcol" style={{ "--colw": "920px" }}>
      <div className="psub" style={{ marginTop: 18 }}>Delegate the task, keep the authority. Web content can never expand what an agent may do.</div>
      <div className="ab-chips" style={{ marginBottom: 22 }}>
        {["isolated task identity", "typed powers only", "credential handles — never secrets", "budgeted", "fully auditable"].map((c) => <span key={c} className="ab-chip mono">{c}</span>)}
      </div>
      <div className="ag-grid">
        <div className="ag-card">
          <div className="ag-ch">Compose</div>
          <textarea className="ag-task" value={task} onChange={(e) => setTask(e.target.value)} rows={3} placeholder="What should it do?" />
          <div className="dt-cap" style={{ padding: "14px 0 7px" }}>Scope · origins it may observe</div>
          <div className="chips">{doms.map((d) => (
            <button key={d} className={"chip" + (scope.includes(d) ? " on" : "")} onClick={() => setScope((s) => s.includes(d) ? s.filter((x) => x !== d) : [...s, d])}>{d}</button>
          ))}</div>
          <div className="dt-cap" style={{ padding: "16px 0 4px" }}>Data classes</div>
          {[["Page text", "read", true], ["Form fields", "denied", false], ["Credentials", "handles only", true]].map(([k, v, ok]) => (
            <div key={k} className="si-kv"><span>{k}</span><b style={{ color: ok ? "var(--good)" : "var(--bad)" }}>{v}</b></div>
          ))}
          <div className="dt-cap" style={{ padding: "16px 0 4px" }}>Provider & budgets</div>
          <div className="si-kv"><span>Provider</span><b>Claude · remote · disclosed</b></div>
          {[["Time", 30, "1:10 of 4:00"], ["Tokens", 22, "11k of 50k"], ["Network", 8, "scoped origins"]].map(([k, p, l]) => (
            <div key={k} className="si-bud"><span>{k}</span><span className="si-bar"><i style={{ width: p + "%" }} /></span><b className="mono">{l}</b></div>
          ))}
          <div className="ag-foot">
            <button className="hclear" onClick={dryRun}>Dry-run plan</button>
            <button className="btn-pri" disabled={!plan || running} onClick={run}>Run with confirmations</button>
          </div>
        </div>
        <div className="ag-card">
          <div className="ag-ch">Plan · every step typed</div>
          {!plan && (
            <div className="ag-empty">
              <div className="mono">nothing moves yet</div>
              Dry-run first — you’ll see exactly what it intends, each step carrying only the power it needs.
            </div>
          )}
          {plan && <div className="ag-steps">{plan.map((s, i) => (
            <div key={i} className={"ag-step " + (s.st || "")}>
              <span className="ag-n mono">{i + 1}</span><span className="ag-txt">{s.n}</span>
              <span className={"ag-cap mono" + (s.risk ? " risk" : "")}>{s.cap}</span>
              <span className="ag-st mono">{s.st === "done" ? "✓" : s.st === "running" ? "…" : ""}</span>
            </div>
          ))}</div>}
          {done && <div className="ag-post"><Check size={13} color="var(--good)" /> Postconditions verified · nothing sent · complete local audit kept</div>}
          <div className="ag-foot mono" style={{ fontSize: 10, color: "var(--tx3)" }}>observation manifest · 2 pages · 0 forms · 1 credential handle</div>
        </div>
      </div>
      {confirmStep !== null && (
        <div className="modalveil"><div className="modal" style={{ width: 420 }}>
          <div className="t">Turing asks — not the agent</div>
          <div className="s" style={{ padding: "6px 0 14px" }}>Step {confirmStep + 1}: “{STEPS[confirmStep].n}”. This writes to your Notes. Allow once?</div>
          <div style={{ display: "flex", gap: 8, justifyContent: "flex-end" }}>
            <button className="hclear" onClick={() => { setConfirmStep(null); setRunning(false); note("Denied — agent halted before acting"); }}>Deny <span className="kbd">ESC</span></button>
            <button className="btn-pri" onClick={allow}>Allow once <span className="kbd">↵</span></button>
          </div>
        </div></div>
      )}
    </div></div></div>
  );
}

/* ================= shared pointer-drag primitive ================= */
function startPointerDrag(e, { threshold = 5, onStart, onMove, onEnd }) {
  if (e.button !== 0) return false;
  const startX = e.clientX, startY = e.clientY;
  let started = false;
  const move = (ev) => {
    if (!started) {
      if (Math.abs(ev.clientX - startX) < threshold && Math.abs(ev.clientY - startY) < threshold) return;
      started = true;
      document.body.classList.add("tdrag");
      onStart && onStart(ev);
    }
    onMove && onMove(ev);
  };
  const up = (ev) => {
    window.removeEventListener("pointermove", move);
    window.removeEventListener("pointerup", up);
    document.body.classList.remove("tdrag");
    onEnd && onEnd(ev, started);
  };
  window.addEventListener("pointermove", move);
  window.addEventListener("pointerup", up);
  return true;
}

/* ================= error page ================= */
function ErrorPage({ tab, onRetry, onResources, note }) {
  const host = tab.url.split("/")[0];
  const [det, setDet] = useState(false);
  return (
    <div className="scroll"><div className="page"><div className="errwrap">
      <div className="err-ic"><WifiOff size={26} /></div>
      <div className="err-t">Can’t reach {host}</div>
      <div className="err-s">The server isn’t responding. Your Context Firewall allows this domain — the machine on the other end is quiet.</div>
      <div className="err-acts">
        <button className="btn-pri" onClick={onRetry}>Try again <span className="kbd">⌘R</span></button>
        <button className="hclear" onClick={() => note("Address copied")}>Copy address</button>
        <button className="hclear" onClick={onResources}>Open Resources</button>
      </div>
      <div className="err-note"><Check size={12} color="var(--good)" /> This tab’s state is snapshotted — nothing was lost.</div>
      <button className="err-more mono" onClick={() => setDet((v) => !v)}>{det ? "Hide details" : "Details"}</button>
      {det && <div className="err-det mono">ERR_CONNECTION_REFUSED · 3 attempts · last 22:41 · DNS ok · TCP handshake timed out (5 s)</div>}
    </div></div></div>
  );
}


/* ================= page header system ================= */
function PageHeader({ icon: Ic, title, chip, maxW = 880, children }) {
  return (
    <div className="phead">
      <div className="phead-in pcol" style={{ "--colw": maxW + "px" }}>
        {Ic && <Ic size={16} color="var(--ac)" />}
        <span className="ph-t">{title}</span>
        {chip && <span className="ph-chip mono">{chip}</span>}
        <div className="ph-acts">{children}</div>
      </div>
    </div>
  );
}

/* ================= Turing: Project Inspector ================= */
function SpaceInspector({ space, tabsN, close, onShare, onTimeMachine, onExport }) {
  const [fw, setFw] = useState(true);
  const Sec = ({ t, children }) => (<div className="si-sec"><div className="dt-cap" style={{ padding: "0 0 6px" }}>{t}</div>{children}</div>);
  const KV = ({ k, v, good }) => (<div className="si-kv"><span>{k}</span><b style={good ? { color: "var(--good)" } : undefined}>{v}</b></div>);
  return (
    <div className="si">
      <div className="si-h">
        <span className="spdot" style={{ background: space.tint }} />
        <span className="si-t">{space.name}</span>
        <span className="si-badge mono">project</span>
        <button className="ib" style={{ width: 24, height: 24, marginLeft: "auto" }} onClick={close}><X size={13} /></button>
      </div>
      <div className="si-body">
        <Sec t="Identity & container">
          <KV k="Container" v={space.name + " · isolated"} good />
          <KV k="Cookies & logins" v="scoped to this project" />
          <KV k="Context firewall" v={<span className="seg" style={{ height: 20 }}><button className={fw ? "on" : ""} onClick={() => setFw(true)} style={{ fontSize: 10, padding: "0 7px" }}>On</button><button className={!fw ? "on" : ""} onClick={() => setFw(false)} style={{ fontSize: 10, padding: "0 7px" }}>Off</button></span>} />
          <div className="si-note">Personal accounts never load here. Domains bound: <b className="mono">mercury.com · linear.app · stripe.com</b> <button className="si-add">+ bind domain</button></div>
          <KV k="Network policy" v="system DNS · no proxy" />
        </Sec>
        <Sec t="What lives here">
          <KV k="Tabs & folders" v={tabsN + " tabs · 1 folder · 2 pinned"} />
          <KV k="History & bookmarks" v="412 entries · project-only" />
          <KV k="Notes & evidence" v="6 notes · 3 cited captures" />
          <KV k="Downloads" v="2 files · kept 30 days" />
          <KV k="Apps" v={<span>Linear <i className="si-dot on" /> · Gmail <i className="si-dot" /> suspended</span>} />
        </Sec>
        <Sec t="AI authority">
          <KV k="Provider" v="Claude · remote, disclosed" />
          <KV k="Context" v="only tabs in this project" />
          <KV k="Allowed actions" v="read · summarize · draft" />
          <KV k="Never" v="submit · purchase · credentials" good />
        </Sec>
        <Sec t="Budgets">
          {[["Memory", 62, "1.9 GB of 3 GB"], ["CPU (background)", 18, "18% cap 25%"], ["Tokens today", 41, "82k of 200k · $0.31"]].map(([k, pct, l]) => (
            <div key={k} className="si-bud"><span>{k}</span><span className="si-bar"><i style={{ width: pct + "%" }} /></span><b className="mono">{l}</b></div>
          ))}
        </Sec>
        <Sec t="Sync · retention">
          <KV k="Sync" v="this device + laptop · encrypted" />
          <KV k="Retention" v="history 90d · snapshots 30d" />
        </Sec>
      </div>
      <div className="si-foot">
        <button className="hclear" onClick={onTimeMachine}>Time Machine</button>
        <button className="hclear" onClick={onShare}>Share</button>
        <button className="hclear" onClick={onExport}>Export</button>
        <button className="hclear">Pause</button>
      </div>
    </div>
  );
}

function ShareSheet({ space, close, note }) {
  const [revoked, setRevoked] = useState(false);
  const [inc, setInc] = useState({ tabs: true, folders: true, notes: true, cookies: false, creds: false, history: false });
  const Row = ({ k, l, lock }) => (
    <label className={"sh-row" + (lock ? " lock" : "")}>
      <input type="checkbox" checked={inc[k]} disabled={lock} onChange={() => setInc((v) => ({ ...v, [k]: !v[k] }))} />{l}
      {lock && <span className="mono" style={{ marginLeft: "auto", fontSize: 9.5, color: "var(--tx3)" }}>never shared</span>}
    </label>
  );
  return (
    <div className="modalveil" onClick={close}>
      <div className="modal" style={{ width: 400 }} onClick={(e) => e.stopPropagation()}>
        <div className="t">Share “{space.name}” — live & revocable</div>
        <div style={{ padding: "4px 0 10px" }}>
          <Row k="tabs" l="Tabs & layout" /><Row k="folders" l="Folders & pins" /><Row k="notes" l="Notes & citations" />
          <Row k="cookies" l="Cookies" lock /><Row k="creds" l="Credentials" lock /><Row k="history" l="Private history" lock />
        </div>
        <div className={"sh-link mono" + (revoked ? " dead" : "")}>{revoked ? "link revoked — viewers lost access" : "turing.app/s/wade-q3-invoicing"}</div>
        <div style={{ display: "flex", gap: 8, justifyContent: "flex-end", marginTop: 12 }}>
          <button className="hclear" style={{ color: "var(--bad)" }} onClick={() => { setRevoked(true); note("Share link revoked"); }}>Revoke</button>
          <button className="btn-pri" onClick={() => { note("Live link copied — updates follow"); close(); }}>Copy live link <span className="kbd">↵</span></button>
        </div>
      </div>
    </div>
  );
}

/* ================= Turing: Workspace Time Machine ================= */
const SNAPS = [
  { id: 1, t: "2 min ago", ev: "Auto snapshot", d: "+1 tab · scroll saved", tabs: 6, folders: 1, layout: "2-pane" },
  { id: 2, t: "34 min ago", ev: "Before AI organize", d: "you ran Organize tabs", tabs: 6, folders: 0, layout: "single" },
  { id: 3, t: "2 hr ago", ev: "Closed 4 tabs", d: "tidy — recoverable one by one", tabs: 9, folders: 1, layout: "single" },
  { id: 4, t: "Yesterday 17:40", ev: "Crash recovery point", d: "restored cleanly in 1.2 s", tabs: 8, folders: 1, layout: "2-pane" },
  { id: 5, t: "Mon 09:12", ev: "Before update 1.4 → 1.5", d: "automatic pre-update snapshot", tabs: 7, folders: 1, layout: "single" },
];
function TimeMachinePage({ onRestore, onFork, note }) {
  const [sel, setSel] = useState(1);
  const [compare, setCompare] = useState(false);
  const s = SNAPS.find((x) => x.id === sel);
  return (
    <div className="scroll">
      <PageHeader icon={RotateCw} title="Time Machine" chip={SNAPS.length + " snapshots"} maxW={880}>
        <button className="hclear" onClick={() => note("Encrypted recovery bundle exported")}>Export bundle</button>
        <button className="btn-pri" style={{ height: 28 }} onClick={() => onRestore(s)}>Restore project</button>
      </PageHeader>
      <div className="page"><div className="pbody pcol" style={{ "--colw": "880px" }}>
      <div className="psub" style={{ marginTop: 18 }}>Every state of this project, versioned.</div>
      <div className="ab-chips" style={{ marginBottom: 22 }}>
        {["automatic snapshots", "restores structure — never repeats actions", "crash & update recovery", "encrypted export"].map((c) => <span key={c} className="ab-chip mono">{c}</span>)}
      </div>
      <div className="tm-wrap">
        <div className="tm-line">
          {SNAPS.map((sn) => (
            <button key={sn.id} className={"tm-snap" + (sel === sn.id ? " on" : "")} onClick={() => setSel(sn.id)}>
              <span className="tm-dot" /><span className="tm-ev">{sn.ev}</span><span className="tm-t mono">{sn.t}</span><span className="tm-d">{sn.d}</span>
            </button>
          ))}
        </div>
        <div className="tm-view">
          <div className="dt-cap">{compare ? "Compare · now vs " + s.t : "Snapshot · " + s.t}</div>
          {!compare ? (
            <div className="tm-prev">
              <div className="tm-topo">{Array.from({ length: s.tabs }, (_, i) => <i key={i} className={i < 2 ? "pin" : ""} />)}<span className="mono">{s.tabs} tabs · {s.folders} folder · {s.layout}</span></div>
              <div className="si-kv"><span>Scroll & selection</span><b>saved · safe to restore</b></div>
              <div className="si-kv"><span>Unsaved work</span><b style={{ color: "var(--good)" }}>none detected</b></div>
              <div className="si-kv"><span>Plug-in state</span><b>2 compatible · restorable</b></div>
            </div>
          ) : (
            <div className="tm-diff">
              <span className="add">+ 2 tabs opened since</span><span className="rem">− 1 folder collapsed</span><span className="mov">~ split layout changed</span>
            </div>
          )}
          <div className="tm-acts">
            <button className="hclear" onClick={() => note("Restored 1 tab from " + s.t)}>Restore one tab…</button>
            <button className="hclear" onClick={() => setCompare((v) => !v)}>{compare ? "Preview" : "Compare"}</button>
            <button className="hclear" onClick={() => onFork(s)}>Fork from here</button>
          </div>
        </div>
      </div>
    </div></div></div>
  );
}

function DownloadsPage() {
  const [items, setItems] = useState([
    { n: "thorbis-quote-1042.pdf", z: "1.2 MB", d: "mercury.com", t: "2 min ago", st: "done" },
    { n: "site-photos-jul.zip", z: "48.1 MB of 112 MB", d: "linear.app", t: "now", st: "active", pct: 43 },
    { n: "tracker-bundle.exe", z: "—", d: "freebies.example", t: "1 hr ago", st: "blocked" },
    { n: "ubuntu-24.04-desktop-amd64-with-an-impossibly-long-filename-that-must-ellipsize-cleanly-or-the-design-fails.iso", z: "4700.0 MB", d: "releases.ubuntu.com", t: "2 hrs ago", st: "done" },
    { n: "empty-report.pdf", z: "0.0 MB", d: "mercury.com", t: "3 hrs ago", st: "done" },
    { n: "design-tokens.zip", z: "12.4 MB", d: "figma.com", t: "just now", st: "active", pct: 3 },
    { n: "permit-application.docx", z: "220 kB", d: "county.gov", t: "Yesterday", st: "done" },
  ]);
  return (
    <div className="scroll">
      <PageHeader icon={Download} title="Downloads" chip={items.length + " files"} maxW={760}>
        <button className="hclear" onClick={() => setItems([])}>Clear all</button>
      </PageHeader>
      <div className="page">
        <div className="pbody pcol" style={{ "--colw": "760px" }}>
          <div className="psub" style={{ marginTop: 18 }}>Everything lands here. Shield screens files before they touch your disk.</div>
          <div className="hlist">
            {items.length === 0 && <div className="hempty">No downloads yet.</div>}
            {items.map((it) => (
              <div key={it.n} className={"dl-row" + (it.st === "blocked" ? " blocked" : "")}>
                <div className="dl-ic mono">{(it.n.split(".").pop() || "?").slice(0, 4)}</div>
                <div className="dl-mid">
                  <div className={"dl-n" + (it.st === "blocked" ? " blk" : "")}>{it.n}</div>
                  <div className="dl-s mono">{it.d} · {it.z} · {it.t}</div>
                  {it.st === "active" && <div className="dl-bar"><i style={{ width: it.pct + "%" }} /></div>}
                </div>
                {it.st === "done" && <button className="hclear" style={{ height: 28 }}>Show in folder</button>}
                {it.st === "active" && <button className="hclear" style={{ height: 28 }}>Pause</button>}
                {it.st === "blocked" && <span className="dl-blk"><ShieldCheck size={12} /> Blocked by Shield</span>}
                {false && null}
                <button className="xc" style={{ opacity: .6 }} onClick={() => setItems((xs) => xs.filter((x) => x.n !== it.n))}><X size={12} /></button>
              </div>
            ))}
            {items.length > 0 && <div className="tfoot"><span className="mono">{items.length} files</span><span className="mono">{items.reduce((a, x) => a + (parseFloat(x.z) || 0), 0).toFixed(1)} MB</span><span style={{ marginLeft: "auto" }}>{items.filter((x) => x.st === "blocked").length} screened by Shield</span></div>}
          </div>
        </div>
      </div>
    </div>
  );
}

/* ================= Ask Turing — chat with your tabs ================= */
const SKILLS0 = [
  ["summarize", "Summarize", "Boil this page down to its argument"],
  ["compare", "Compare", "Line up the tabs you mention"],
  ["write", "Write", "Draft something from this context"],
  ["devil", "Devil’s advocate", "Argue against the current page"],
];
const GALLERY = [
  ["rewrite", "Rewrite", "Same message, tighter and warmer"],
  ["explain", "Explain code", "Walk through what this snippet does"],
  ["actions", "Action items", "Pull the to-dos out of this page"],
];
function fmtInline(str) {
  const out = []; let k = 0, last = 0, m;
  const rx = /(\*\*[^*]+\*\*|`[^`]+`)/g;
  while ((m = rx.exec(str))) {
    if (m.index > last) out.push(str.slice(last, m.index));
    const tk = m[0];
    if (tk.startsWith("**")) out.push(<b key={"b" + k++}>{tk.slice(2, -2)}</b>);
    else out.push(<code key={"c" + k++} className="ai-code">{tk.slice(1, -1)}</code>);
    last = m.index + tk.length;
  }
  if (last < str.length) out.push(str.slice(last));
  return out;
}
function CodeBlock({ code }) {
  const [ok, setOk] = useState(false);
  const t = code.replace(/^\n/, "");
  const first = t.split("\n")[0].trim();
  const lang = /^[a-z]{1,10}$/.test(first) ? first : "";
  const body = (lang ? t.slice(t.indexOf("\n") + 1) : t).replace(/\n$/, "");
  return (
    <div className="ai-pre">
      <div className="ai-pre-h">
        <span className="mono">{lang || "text"}</span>
        <button onClick={() => { try { navigator.clipboard && navigator.clipboard.writeText(body); } catch (e) {} setOk(true); setTimeout(() => setOk(false), 1200); }}>
          {ok ? <Check size={10} /> : <Copy size={10} />}{ok ? "Copied" : "Copy"}
        </button>
      </div>
      <pre className="mono">{body}</pre>
    </div>
  );
}
function RichText({ text }) {
  const chunks = String(text).split("```");
  return chunks.map((c, i) => {
    if (i % 2) return <CodeBlock key={i} code={c} />;
    return c.split("\n").map((line, j) => {
      const bullet = /^\s*[·\-\*]\s+/.test(line);
      if (!line.trim()) return <div key={i + "-" + j} className="ai-gap" />;
      return <div key={i + "-" + j} className={bullet ? "ai-li" : "ai-p"}>{fmtInline(bullet ? line.replace(/^\s*[·\-\*]\s+/, "") : line)}</div>;
    });
  });
}

const MODELS = [
  ["swift", "Swift", "instant · cheapest", 0.001],
  ["core", "Core", "balanced — default", 0.003],
  ["deep", "Deep", "reasons longer, cites more", 0.015],
];
const ATTACH = [
  ["page", "This page, as text", FileText],
  ["shot", "Screenshot of this page", Camera],
  ["sel", "Your last selection", Type],
];

/* ===== shadcn/ui chat primitives, ported to Turing's tokens =====
   Same abstractions as shadcn/ui's chat set (MessageScroller, Message, Bubble,
   Attachment, Marker) plus AI Elements' PromptInput. Ported, not imported:
   this shell has no Tailwind and no @/ alias, so the behaviour and composition
   are reproduced against the CSS variables the rest of the browser uses. */

function MessageScroller({ children, stickKey }) {
  const ref = useRef(null);
  const [atEnd, setAtEnd] = useState(true);
  const stick = useCallback(() => { const el = ref.current; if (el) el.scrollTop = el.scrollHeight; }, []);
  useEffect(() => { if (atEnd) stick(); });                       // auto-follow streamed replies
  useEffect(() => { stick(); setAtEnd(true); }, [stickKey, stick]); // anchor new turns
  return (
    <div className="msc-wrap">
      <div ref={ref} className={"msc scroll-fade" + (atEnd ? " at-end" : "")}
        onScroll={(e) => { const el = e.currentTarget; setAtEnd(el.scrollHeight - el.scrollTop - el.clientHeight < 44); }}>
        {children}
      </div>
      {!atEnd && (
        <button className="msc-jump" title="Jump to latest" onClick={() => { stick(); setAtEnd(true); }}>
          <ChevronDown size={14} />
        </button>
      )}
    </div>
  );
}
function Message({ from, grouped, children }) {
  return <div className={"msg is-" + from + (grouped ? " grouped" : "")}>{children}</div>;
}
function MessageAvatar({ from }) {
  return <span className={"msg-av is-" + from}>{from === "user" ? "Y" : <Sparkles size={12} />}</span>;
}
function MessageBody({ children }) { return <div className="msg-body">{children}</div>; }
function MessageHeader({ children }) { return <div className="msg-h">{children}</div>; }
function MessageFooter({ children }) { return <div className="msg-f">{children}</div>; }
function Bubble({ variant, children }) { return <div className={"bub is-" + (variant || "assistant")}>{children}</div>; }
function Attachment({ icon: Ic, name, meta, onRemove }) {
  const I = Ic || FileText;
  return (
    <div className="att">
      <span className="att-m"><I size={12} /></span>
      <span className="att-t"><span className="att-n">{name}</span>{meta && <span className="att-meta mono">{meta}</span>}</span>
      {onRemove && <button className="att-x" onClick={onRemove} aria-label="Remove"><X size={10} /></button>}
    </div>
  );
}
function Marker({ variant, children }) { return <div className={"mk is-" + (variant || "note")}>{children}</div>; }
function Actions({ children }) { return <div className="msg-acts">{children}</div>; }
function Action({ label, onClick, tone, children }) {
  return <button className={"msg-act" + (tone ? " " + tone : "")} title={label} aria-label={label} onClick={onClick}>{children}</button>;
}
function Sources({ cites, onOpen }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="msg-src">
      <button className="msg-src-t" onClick={() => setOpen((v) => !v)}>
        <Link size={10} />{cites.length} source{cites.length === 1 ? "" : "s"}
        <ChevronDown size={10} className={open ? "rot" : ""} />
      </button>
      {open && (
        <div className="msg-src-c">
          {cites.map((c, i) => (
            <button key={i} className="msg-src-i" onClick={() => onOpen(c)} title={"Open " + c}>
              <span className="mono">{i + 1}</span>{c.split("/")[0]}<ExternalLink size={9} />
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
function Suggestions({ children }) { return <div className="sugs scroll-fade">{children}</div>; }
function Suggestion({ onClick, children }) { return <button className="sug-chip" onClick={onClick}>{children}</button>; }

/* ---- AI Elements: PromptInput ---- */
function PromptInput({ children }) { return <div className="pi">{children}</div>; }
function PromptInputBody({ children }) { return <div className="pi-body">{children}</div>; }
function PromptInputToolbar({ children }) { return <div className="pi-bar">{children}</div>; }
function PromptInputTools({ children }) { return <div className="pi-tools">{children}</div>; }
function PromptInputButton({ active, label, onClick, children }) {
  return <button className={"pi-btn" + (active ? " on" : "")} title={label} onClick={onClick}>{children}</button>;
}
function PromptInputSubmit({ status, onClick, disabled }) {
  return (
    <button className={"pi-send is-" + status} onClick={onClick} disabled={disabled}
      title={status === "streaming" ? "Stop generating" : "Send · ↵"} aria-label={status === "streaming" ? "Stop" : "Send"}>
      {status === "streaming" ? <Ban size={15} /> : status === "submitted" ? <span className="pi-spin" /> : <ArrowUp size={16} />}
    </button>
  );
}

function AskNova({ tabs, activeTab, msgs, setMsgs, close, onOpen, onOpenNew, onAgent, threads, setThreads, note }) {
  const [q, setQ] = useState("");
  const aiInRef = useRef(null);
  const [ctxTabs, setCtxTabs] = useState([]);
  const [menu, setMenu] = useState(null);
  const [busy, setBusy] = useState(false);
  const [skills, setSkills] = useState(SKILLS0);
  const [maker, setMaker] = useState(false);
  const [mkName, setMkName] = useState(""); const [mkPrompt, setMkPrompt] = useState("");
  const [model, setModel] = useState("core");
  const [web, setWeb] = useState(false);
  const [atts, setAtts] = useState([]);
  const [wide, setWide] = useState(false);
  const [drawer, setDrawer] = useState(false);
  const [thq, setThq] = useState("");
  const [renameId, setRenameId] = useState(null);
  const [curId, setCurId] = useState(null);
  const [copied, setCopied] = useState(null);
  const [streaming, setStreaming] = useState(false);
  const streamRef = useRef(null);

  useEffect(() => () => clearTimeout(streamRef.current), []);
  useEffect(() => {
    if (!curId) return;
    setThreads((ts) => ts.map((t) => (t.id === curId ? { ...t, msgs, at: Date.now() } : t)));
  }, [msgs, curId, setThreads]);

  const tokens = useMemo(() => msgs.reduce((n, m) => n + Math.ceil((m.txt || "").length / 4), 0), [msgs]);
  const rate = (MODELS.find((m) => m[0] === model) || MODELS[1])[3];
  const cost = ((tokens / 1000) * rate).toFixed(3);
  const modelName = (MODELS.find((m) => m[0] === model) || [])[1];

  const onChange = (v) => {
    setQ(v);
    if (v.endsWith("@")) setMenu("at");
    else if (v === "/") setMenu("slash");
    else if (menu === "at" || menu === "slash") setMenu(null);
  };
  const addCtx = (t) => { setCtxTabs((c) => (c.some((x) => x.id === t.id) ? c : [...c, t])); setQ((s2) => s2.replace(/@$/, "")); setMenu(null); };

  const baseReply = (text, ctx) => {
    const ia = instantAnswer(text);
    if (ia && ia.type === "answer") return { txt: "= " + ia.text, follow: ["Show your working", "Convert to another unit"] };
    if (ctx.some((c) => c.id === "hist")) return { txt: "From your last 7 days you kept circling three places — **linear.app** (14 visits, mostly the sprint board), **mercury.com** (invoices, Tue and Thu), and **stripe.com/docs**. The thread connecting them looks like the Q3 invoicing push.", follow: ["Summarize just that trail", "What did I miss?"] };
    const custom = skills.find(([id]) => text.startsWith("/" + id) && !SKILLS0.some(([s0]) => s0 === id) && !GALLERY.some(([g0]) => g0 === id));
    if (custom) return { txt: "Running your **" + custom[1] + "** skill on " + activeTab.url.split("/")[0] + ": " + custom[2] + " — done.\n\nIn the real build this executes your saved prompt against the page." };
    if (text.startsWith("/rewrite")) return { txt: "Tighter version:\n\n“We reviewed both tools. The faster one wins for our crew — let's pilot it two weeks and measure close time.”", follow: ["Make it warmer", "Make it shorter"] };
    if (text.startsWith("/explain")) return {
      txt: "This finds a matching discount rule, applies it, and rounds to cents:\n\n```js\nfunction applyDiscount(cart, rules) {\n  const rule = (rules ?? []).find(r => r.id === cart.code);\n  if (!rule) return cart.subtotal;\n  const off = cart.subtotal * (rule.pct / 100);\n  return Math.round((cart.subtotal - off) * 100) / 100;\n}\n```\n\n**The important bit:** `?? []` means a missing rules list returns the subtotal instead of throwing.",
      follow: ["What could break here?", "Write a test for it"],
    };
    if (text.startsWith("/actions")) return { txt: "Action items on this page:\n\n· Confirm the Q3 invoice batch — **owner: you**\n· Reply to the permit thread by Friday\n· Re-check `tracker.js` — Shield blocked it twice", follow: ["Add these to my reminders", "Who owns the permit thread?"] };
    if (text.startsWith("/summarize")) return { txt: "**" + activeTab.url.split("/")[0] + " in one line:** a dense tool page whose core claim is speed — 11 items above the fold, zero decoration. The rest is supporting detail.", follow: ["What's the strongest claim?", "Compare to the other tab"] };
    if (text.startsWith("/compare") || ctx.length > 1) {
      const pair = ctx.length ? ctx : tabs.slice(1, 3);
      return { txt: "Across " + pair.length + " tabs — **" + pair.map((t) => t.url.split("/")[0]).join("** vs **") + "**: same job, different bets. One optimizes for keyboard speed, the other for visual overview.\n\n· Terminal-first team → the first\n· Plans visually → the second", preview: pair[0].url, follow: ["Which is cheaper to run?", "Draft a recommendation"] };
    }
    if (text.startsWith("/write")) return { txt: "Draft, in your voice:\n\n“Quick note — I looked at the options we had open and the trade-off is speed vs. overview. Recommend we pilot the faster one for two weeks and measure ticket close time.”", follow: ["More direct", "Add the numbers"] };
    if (text.startsWith("/devil")) return { txt: "Counter-position: this page's minimalism is doing **marketing** work, not product work. Density ≠ speed, and hiding chrome hides affordances. If a new dispatcher can't find the button, “zen” is just friction with good typography.", follow: ["Steelman the other side", "What would change your mind?"] };
    if (ctx.length === 1) return { txt: "From **" + ctx[0].url.split("/")[0] + "**: the short answer is yes — the page's own data supports it.\n\nTwo caveats: the numbers are self-reported, and the comparison excludes setup time.", preview: ctx[0].url, follow: ["Find a second source", "How self-reported?"] };
    return { txt: "Looking at **" + activeTab.url.split("/")[0] + "** — it's making one claim and backing it with layout, not copy. Ask me to `/summarize` it, or @-mention another tab and I'll compare them.", follow: ["/summarize this page", "Compare with my other tabs"] };
  };
  const reply = (text, ctx) => {
    const b = baseReply(text, ctx);
    const cites = web ? [activeTab.url, "developer.mozilla.org/en-US/docs/Web", "news.ycombinator.com/item?id=41"].slice(0, 3) : null;
    return { ...b, cites, model, follow: b.follow || ["Go deeper", "What's the counter-argument?"] };
  };

  const stream = (full, meta) => {
    setBusy(false); setStreaming(true);
    setMsgs((m) => [...m, { ...meta, role: "nova", txt: "", streaming: true, follow: null, _follow: meta.follow }]);
    let i = 0;
    const tick = () => {
      i += 2 + Math.round(Math.random() * 5);
      const part = full.slice(0, i);
      setMsgs((m) => { const c = [...m]; c[c.length - 1] = { ...c[c.length - 1], txt: part }; return c; });
      if (i < full.length) streamRef.current = setTimeout(tick, 16);
      else {
        setMsgs((m) => { const c = [...m]; const L = c[c.length - 1]; c[c.length - 1] = { ...L, streaming: false, follow: L._follow }; return c; });
        streamRef.current = null; setStreaming(false);
      }
    };
    streamRef.current = setTimeout(tick, 120);
  };
  const stopGen = () => {
    clearTimeout(streamRef.current); streamRef.current = null; setStreaming(false); setBusy(false);
    setMsgs((m) => { const c = [...m]; if (c.length) c[c.length - 1] = { ...c[c.length - 1], streaming: false, stopped: true }; return c; });
  };
  const send = (override) => {
    const text = (override != null ? override : q).trim();
    if (!text && ctxTabs.length === 0 && atts.length === 0) return;
    if (streaming) stopGen();
    const ctx = ctxTabs;
    if (!curId) {
      const id = "th" + Date.now();
      setCurId(id);
      setThreads((ts) => [{ id, title: (text || "Tab comparison").slice(0, 44), msgs: [], at: Date.now() }, ...ts]);
    }
    setMsgs((m) => [...m, { role: "user", txt: text || "Compare these", ctx, atts }]);
    setQ(""); setCtxTabs([]); setAtts([]); setMenu(null); setBusy(true);
    if (aiInRef.current) aiInRef.current.style.height = "auto";
    setTimeout(() => { const r = reply(text, ctx); stream(r.txt, r); }, 420);
  };
  const regen = (i) => {
    const prev = [...msgs.slice(0, i)].reverse().find((m) => m.role === "user");
    if (!prev) return;
    setMsgs((m) => m.slice(0, i)); setBusy(true);
    setTimeout(() => { const r = reply(prev.txt, prev.ctx || []); stream(r.txt, r); }, 300);
  };
  const copyMsg = (t, i) => { try { navigator.clipboard && navigator.clipboard.writeText(t); } catch (e) {} setCopied(i); setTimeout(() => setCopied(null), 1200); };
  const feedback = (i, v) => setMsgs((m) => m.map((x, j) => (j === i ? { ...x, fb: x.fb === v ? 0 : v } : x)));
  const newChat = () => { clearTimeout(streamRef.current); setStreaming(false); setBusy(false); setMsgs([]); setCurId(null); setCtxTabs([]); setAtts([]); setQ(""); setMenu(null); setDrawer(false); };
  const openThread = (t) => { clearTimeout(streamRef.current); setStreaming(false); setBusy(false); setCurId(t.id); setMsgs(t.msgs || []); setDrawer(false); };
  const delThread = (id) => { setThreads((ts) => ts.filter((t) => t.id !== id)); if (id === curId) newChat(); };
  const shown = (threads || []).filter((t) => !thq.trim() || t.title.toLowerCase().includes(thq.trim().toLowerCase()));

  const onKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); }
    else if (e.key === "Escape") { if (menu) { e.stopPropagation(); setMenu(null); } }
    else if (e.key === "ArrowUp" && !q.trim()) {
      const lastUser = [...msgs].reverse().find((m) => m.role === "user");
      if (lastUser) { e.preventDefault(); setQ(lastUser.txt); }
    }
  };
  const grow = (el) => { el.style.height = "auto"; el.style.height = Math.min(132, el.scrollHeight) + "px"; };
  const last = msgs[msgs.length - 1];
  const status = streaming ? "streaming" : busy ? "submitted" : "ready";

  return (
    <div className={"aiwrap" + (wide ? " wide" : "")}>
      <div className="ai-h">
        <span className="ai-hemblem"><Sparkles size={15} color="var(--ac)" /></span>
        <div className="ai-htext">
          <div className="ai-htitle">Ask Turing</div>
          <div className="ai-hsub">{curId ? ((threads.find((t) => t.id === curId) || {}).title || "New chat") : "Chat with your tabs · or take control"}</div>
        </div>
        <button className={"ai-hbtn" + (drawer ? " on" : "")} title="Chat history" onClick={() => setDrawer((v) => !v)}><HistoryIcon size={15} /></button>
        <button className="ai-hbtn" title={wide ? "Narrow panel" : "Widen panel"} onClick={() => setWide((v) => !v)}><Columns2 size={15} /></button>
        {msgs.length > 0 && <button className="ai-hbtn" title="New chat" onClick={newChat}><Plus size={16} /></button>}
        <button className="ai-hbtn" title="Close · ⌘E" onClick={close}><X size={15} /></button>
      </div>

      {drawer && (
        <div className="ai-drawer">
          <div className="ai-dh">
            <Search size={12} color="var(--tx3)" />
            <input placeholder="Search chats" value={thq} onChange={(e) => setThq(e.target.value)} />
            <button onClick={() => { setDrawer(false); setThq(""); }}><X size={13} /></button>
          </div>
          <div className="ai-dlist">
            {shown.length === 0 && <div className="ai-dempty">{(threads || []).length ? "No chats match." : "No saved chats yet — start one below."}</div>}
            {shown.map((t) => (
              <div key={t.id} className={"ai-th" + (t.id === curId ? " on" : "")}>
                {renameId === t.id ? (
                  <input className="ai-thr" autoFocus defaultValue={t.title}
                    onBlur={(e) => { const v = e.target.value.trim(); if (v) setThreads((ts) => ts.map((x) => (x.id === t.id ? { ...x, title: v } : x))); setRenameId(null); }}
                    onKeyDown={(e) => { if (e.key === "Enter") e.target.blur(); if (e.key === "Escape") setRenameId(null); }} />
                ) : (
                  <button className="ai-tht" onClick={() => openThread(t)}>
                    <span className="ai-thn">{t.title}</span><span className="ai-thm mono">{(t.msgs || []).length}</span>
                  </button>
                )}
                <button className="ai-thb" title="Rename" onClick={() => setRenameId(t.id)}><Type size={11} /></button>
                <button className="ai-thb" title="Delete" onClick={() => delThread(t.id)}><Trash2 size={11} /></button>
              </div>
            ))}
          </div>
        </div>
      )}

      <MessageScroller stickKey={msgs.length}>
        {msgs.length === 0 && (
          <div className="cv-empty">
            <div className="cv-emblem"><Sparkles size={20} color="var(--ac)" /></div>
            <div className="cv-et">{activeTab.url === "nova://newtab" ? "Ask Turing anything" : "Ask about " + activeTab.url.split("/")[0]}</div>
            <div className="cv-es">I can read your open tabs, compare them, or run a skill. Type <b className="mono">@</b> to add a tab, <b className="mono">/</b> for skills.</div>
            <div className="cv-esugs">
              {skills.slice(0, 3).map(([id, n, d]) => (
                <button key={id} className="cv-esug" onClick={() => { setQ("/" + id + " "); requestAnimationFrame(() => aiInRef.current && aiInRef.current.focus()); }}>
                  <span className="mono">/{id}</span><span>{d}</span>
                </button>
              ))}
            </div>
          </div>
        )}
        {msgs.map((m, i) => {
          const from = m.role === "user" ? "user" : "assistant";
          const grouped = i > 0 && (msgs[i - 1].role === m.role);
          return (
            <Message key={i} from={from} grouped={grouped}>
              {grouped ? <span className="msg-av-sp" /> : <MessageAvatar from={from} />}
              <MessageBody>
                {!grouped && (
                  <MessageHeader>
                    <span className="msg-who">{from === "user" ? "You" : "Turing"}</span>
                    {m.model && from === "assistant" && <span className="msg-model mono">{(MODELS.find((x) => x[0] === m.model) || [])[1]}</span>}
                  </MessageHeader>
                )}
                {m.atts && m.atts.length > 0 && (
                  <div className="att-row scroll-fade">{m.atts.map((a, k) => <Attachment key={k} icon={Camera} name={a} meta="context" />)}</div>
                )}
                {m.ctx && m.ctx.length > 0 && (
                  <div className="att-row scroll-fade">{m.ctx.map((t) => <Attachment key={t.id} icon={Globe} name={t.url.split("/")[0]} meta="tab" />)}</div>
                )}
                <Bubble variant={from}>
                  <RichText text={m.txt} />
                  {m.streaming && <i className="ai-caret" />}
                </Bubble>
                {m.stopped && <Marker variant="note">Stopped by you</Marker>}
                {m.cites && m.cites.length > 0 && !m.streaming && <Sources cites={m.cites} onOpen={onOpen} />}
                {m.preview && !m.streaming && (
                  <div className="ai-prev">
                    <div className="ai-pv"><div className="cd-pl" style={{ width: "70%" }} /><div className="cd-pl" style={{ width: "45%" }} /><div className="cd-pl" style={{ width: "58%" }} /></div>
                    <span className="mono">{m.preview.split("/")[0]}</span>
                    <button className="hclear" style={{ height: 24, fontSize: 11 }} onClick={() => onOpen(m.preview)}>Open</button>
                  </div>
                )}
                {!m.streaming && (
                  <MessageFooter>
                    <Actions>
                      {from === "assistant" ? (
                        <>
                          <Action label="Copy" onClick={() => copyMsg(m.txt, i)}>{copied === i ? <Check size={11} /> : <Copy size={11} />}</Action>
                          <Action label="Regenerate" onClick={() => regen(i)}><RefreshCw size={11} /></Action>
                          <Action label="Good answer" tone={m.fb === 1 ? "good" : ""} onClick={() => feedback(i, 1)}><Check size={11} /></Action>
                          <Action label="Not helpful" tone={m.fb === -1 ? "bad" : ""} onClick={() => feedback(i, -1)}><X size={11} /></Action>
                          <Action label="Turn this into an agent task" onClick={() => onAgent && onAgent()}><Sparkles size={11} /></Action>
                        </>
                      ) : (
                        <>
                          <Action label="Edit and resend" onClick={() => { setQ(m.txt); requestAnimationFrame(() => aiInRef.current && (aiInRef.current.focus(), grow(aiInRef.current))); }}><Type size={11} /></Action>
                          <Action label="Copy" onClick={() => copyMsg(m.txt, i)}>{copied === i ? <Check size={11} /> : <Copy size={11} />}</Action>
                        </>
                      )}
                    </Actions>
                  </MessageFooter>
                )}
              </MessageBody>
            </Message>
          );
        })}
        {busy && (
          <Message from="assistant">
            <MessageAvatar from="assistant" />
            <MessageBody><Marker variant="live"><span className="shimmer">Thinking…</span></Marker></MessageBody>
          </Message>
        )}
        {!streaming && !busy && last && last.role === "nova" && last.follow && last.follow.length > 0 && (
          <Suggestions>
            {last.follow.map((f, i) => <Suggestion key={i} onClick={() => send(f)}>{f}</Suggestion>)}
          </Suggestions>
        )}
      </MessageScroller>

      {maker && (
        <div className="ai-maker">
          <div className="ap-t">New skill</div>
          <input placeholder="Name — e.g. quote-check" value={mkName} onChange={(e) => setMkName(e.target.value)} />
          <input placeholder="What should it do?" value={mkPrompt} onChange={(e) => setMkPrompt(e.target.value)} />
          <div style={{ display: "flex", gap: 6, justifyContent: "flex-end" }}>
            <button className="hclear" style={{ height: 26 }} onClick={() => setMaker(false)}>Cancel</button>
            <button className="hclear" style={{ height: 26, color: "var(--ac)" }} onClick={() => {
              const id = mkName.trim().toLowerCase().replace(/\s+/g, "-");
              if (!id) return;
              setSkills((s2) => [...s2, [id, mkName.trim(), mkPrompt.trim() || "Custom skill"]]);
              setMaker(false); setMkName(""); setMkPrompt(""); setQ("/" + id + " ");
            }}>Save skill</button>
          </div>
        </div>
      )}

      <div className="pi-wrap">
        {menu === "at" && (
          <div className="ai-menu">
            <button className="ap-i" style={{ color: "var(--ac)" }} onClick={() => addCtx({ id: "hist", url: "history · 7 days", title: "History" })}><b className="mono" style={{ marginRight: 6 }}>@</b>history — your last 7 days</button>
            {tabs.filter((t) => t.url !== "nova://newtab").slice(0, 5).map((t) => (
              <button key={t.id} className="ap-i" onClick={() => addCtx(t)}>{(t.label || t.title).slice(0, 30)}</button>
            ))}
          </div>
        )}
        {menu === "slash" && (
          <div className="ai-menu">
            {skills.map(([id, n, d]) => <button key={id} className="ap-i" onClick={() => { setQ("/" + id + " "); setMenu(null); }}><b className="mono" style={{ marginRight: 6 }}>/{id}</b>{d}</button>)}
            <div className="ap-t" style={{ marginTop: 4 }}>Gallery</div>
            {GALLERY.filter(([id]) => !skills.some(([sid]) => sid === id)).map(([id, n, d]) => (
              <button key={id} className="ap-i" onClick={() => { setSkills((s2) => [...s2, [id, n, d]]); }}><b className="mono" style={{ marginRight: 6 }}>+</b>{n} — {d}</button>
            ))}
            <button className="ap-i" style={{ color: "var(--ac)" }} onClick={() => { setMaker(true); setMenu(null); }}>＋ New skill…</button>
          </div>
        )}
        {menu === "model" && (
          <div className="ai-menu">
            <div className="ap-t">Model</div>
            {MODELS.map(([id, n, d]) => (
              <button key={id} className="ap-i" onClick={() => { setModel(id); setMenu(null); note && note("Model · Turing " + n); }}>
                <b style={{ marginRight: 6, color: model === id ? "var(--ac)" : "var(--tx2)" }}>{n}</b><span style={{ color: "var(--tx3)" }}>{d}</span>
                {model === id && <Check size={11} style={{ marginLeft: "auto", color: "var(--ac)" }} />}
              </button>
            ))}
          </div>
        )}
        {menu === "attach" && (
          <div className="ai-menu">
            <div className="ap-t">Attach context</div>
            {ATTACH.map(([id, label, Ic]) => (
              <button key={id} className="ap-i" onClick={() => { setAtts((a) => (a.includes(label) ? a : [...a, label])); setMenu(null); }}>
                <Ic size={12} style={{ marginRight: 7 }} />{label}
              </button>
            ))}
          </div>
        )}

        <PromptInput>
          <PromptInputBody>
            {(atts.length > 0 || ctxTabs.length > 0) && (
              <div className="pi-atts scroll-fade">
                {ctxTabs.map((t) => <Attachment key={t.id} icon={Globe} name={t.url.split("/")[0]} meta="tab" onRemove={() => setCtxTabs((c) => c.filter((x) => x.id !== t.id))} />)}
                {atts.map((a, i) => <Attachment key={i} icon={Camera} name={a} meta="context" onRemove={() => setAtts((c) => c.filter((_, j) => j !== i))} />)}
              </div>
            )}
            <textarea ref={aiInRef} className="pi-ta" rows={1} value={q} placeholder="Message Turing…"
              onChange={(e) => { onChange(e.target.value); grow(e.target); }} onKeyDown={onKey} />
          </PromptInputBody>
          <PromptInputToolbar>
            <PromptInputTools>
              <PromptInputButton label="Attach context" onClick={() => setMenu(menu === "attach" ? null : "attach")}><Plus size={13} /></PromptInputButton>
              <PromptInputButton label="Search the web and cite sources" active={web} onClick={() => { setWeb((v) => !v); note && note(web ? "Web search off" : "Web search on — answers will cite sources"); }}><Globe size={12} />Web</PromptInputButton>
              <PromptInputButton label="Skills" onClick={() => setMenu(menu === "slash" ? null : "slash")}><Command size={12} />Skills</PromptInputButton>
              <PromptInputButton label="Voice input" onClick={() => note && note("Listening… (concept shell)")}><Mic size={12} /></PromptInputButton>
            </PromptInputTools>
            <div className="pi-right">
              {tokens > 0 && <span className="pi-meter mono">{tokens >= 1000 ? (tokens / 1000).toFixed(1) + "k" : tokens} tok · ${cost}</span>}
              <button className="pi-model" onClick={() => setMenu(menu === "model" ? null : "model")} title="Choose a model">
                <Zap size={11} />{modelName}<ChevronDown size={9} />
              </button>
              <PromptInputSubmit status={status}
                disabled={status === "ready" && !q.trim() && ctxTabs.length === 0 && atts.length === 0}
                onClick={() => (streaming ? stopGen() : send())} />
            </div>
          </PromptInputToolbar>
        </PromptInput>
      </div>
    </div>
  );
}

/* ================= Nova DevTools ================= */
const DT_TABS = [
  ["elements", "Elements", Code], ["console", "Console", Terminal], ["network", "Network", Wifi],
  ["sources", "Sources", FileCode], ["performance", "Performance", Activity], ["storage", "Storage", Database],
  ["lighthouse", "Lighthouse", Gauge], ["security", "Security", ShieldCheck], ["causal", "Causal", Zap],
];
const CAUSAL_QS = [
  ["Why did github.com sleep?", ["inactive 22 min", "→ policy: freeze after 20 min unless protected", "→ no audio · no unsaved form · no capture", "→ frozen · 210 MB reclaimed · restore: exact"]],
  ["Why was tracker.js blocked?", ["request matched Shield list EasyPrivacy", "→ project policy: Work blocks trackers strictly", "→ blocked before DNS · 0 bytes sent"]],
  ["Who retains this 312 MB?", ["linear.app renderer", "→ 214 MB DOM + 61 MB JS heap + 37 MB images", "→ grows 2 MB/min: detached nodes in board view", "→ suggested: report to site · freeze reclaims 78%"]],
  ["Which task delayed my click?", ["input arrived 14:02:11.220", "→ main thread busy 180 ms: applyDiscount (cart.js:9)", "→ policy hint: long task > 50 ms — split or defer"]],
  ["Where did replay diverge?", ["deterministic replay of session #41", "→ step 14: Date.now() differed (frozen in replay)", "→ diff exported · reduced test generated (12 lines)"]],
];

const DOM_TREE = [
  [0, "html", 'lang="en"'], [1, "head", null], [1, "body", 'class="page dark"'],
  [2, "nav", 'class="topnav"'], [3, "a", 'class="logo" href="/"', "Nova"],
  [2, "main", 'class="hero"', null, true],
  [3, "h1", 'class="title"', "Browse without the browser."],
  [3, "p", 'class="sub"', "One bar. One keystroke. Nothing else."],
  [3, "button", 'class="cta" data-track="hero"', "Get Turing"],
  [2, "footer", 'class="foot"'],
];

const NET_ROWS = [
  ["document", "shell.html", 200, "12.4 kB", 82, 2, 10, "#7aa7ff"],
  ["fetch", "session", 200, "1.2 kB", 34, 8, 22, "#2e8dff"],
  ["script", "app.js", 200, "84.1 kB", 130, 14, 30, "#c792ea"],
  ["css", "tokens.css", 200, "6.3 kB", 48, 18, 12, "#7ee2a8"],
  ["img", "hero.avif", 200, "121 kB", 210, 26, 60, "#ffb86b"],
  ["fetch", "vitals", 200, "0.4 kB", 22, 40, 8, "#2e8dff"],
  ["script", "tracker.js", 0, "0 B", 0, 44, 4, "#ff6b6b"],
  ["font", "geist-mono.woff2", 200, "31 kB", 96, 48, 28, "#e2c08d"],
  ["img", "grid.svg", 200, "2.1 kB", 18, 60, 6, "#ffb86b"],
  ["fetch", "prefs", 304, "0.2 kB", 12, 74, 5, "#2e8dff"],
  ["script", "analytics.js", 0, "0 B", 0, 80, 4, "#ff6b6b"],
  ["doc", "favicon.svg", 200, "0.9 kB", 9, 92, 4, "#7aa7ff"],
];

const SRC_CODE = [
  "import { cart } " + "from " + '"./state";',
  '',
  'export function applyDiscount(code) {',
  '  const rules = cart.rules ?? [];',
  '  const match = rules.find((r) => r.code === code);',
  '  if (!match) return { valid: false };',
  '',
  '  const total = cart.subtotal * (1 - match.pct);',
  '  cart.total = round(total);',
  '  emit("cart:update", cart);',
  '  return { valid: true, total: cart.total };',
  '}',
  '',
  'function round(n) {',
  '  return Math.round(n * 100) / 100;',
  '}',
];

function CausalList() {
  const [open, setOpen] = useState(0);
  return (
    <>
      {CAUSAL_QS.map(([q, chain], i) => (
        <div key={q} className="cz">
          <button className={"cz-q" + (open === i ? " on" : "")} onClick={() => setOpen(open === i ? null : i)}>{q}</button>
          {open === i && <div className="cz-chain mono">{chain.map((c, x) => <div key={x} className="cz-l" style={{ paddingLeft: x * 14 }}>{c}</div>)}</div>}
        </div>
      ))}
    </>
  );
}

function InspectorDock({ tab, setTab, close }) {
  const [tall, setTall] = useState(false);
  const [logs, setLogs] = useState([
    ["info", "Turing shell ready in 212 ms", "boot.js:12"],
    ["log", "session restored · 6 tabs", "session.js:41"],
    ["warn", "prefers-reduced-motion: honoring user setting", "motion.js:8"],
    ["error", "tracker.js blocked by Shield", "shield:1"],
    ["log", "route → /nova/team", "router.js:77"],
  ]);
  const [evalQ, setEvalQ] = useState("");
  const [netSel, setNetSel] = useState(1);
  const [domSel, setDomSel] = useState(5);
  const runEval = () => {
    const q = evalQ.trim(); if (!q) return;
    const ia = instantAnswer(q);
    const res = ia && ia.type === "answer" ? ia.text : "undefined";
    setLogs((l) => [...l, ["echo", q, ""], ["result", res, ""]]);
    setEvalQ("");
  };
  return (
    <div className={"dock" + (tall ? " tall" : "")}>
      <div className="dock-h">
        {DT_TABS.map(([id, l, I]) => (
          <button key={id} className={"dtab" + (tab === id ? " on" : "")} onClick={() => setTab(id)}><I size={13} /> {l}</button>
        ))}
        <div style={{ marginLeft: "auto", display: "flex", gap: 2 }}>
          <button className="ib" style={{ width: 26, height: 26 }} onClick={() => setTall((v) => !v)} title="Resize">{tall ? <ChevronDown size={14} /> : <ChevronUp size={14} />}</button>
          <button className="ib" style={{ width: 26, height: 26 }} onClick={close}><X size={14} /></button>
        </div>
      </div>

      {tab === "elements" && (
        <div className="dt-split">
          <div className="dt-main el-tree">
            {DOM_TREE.map(([d, tag, attrs, text], i) => (
              <div key={i} className={"el-row" + (i === domSel ? " on" : "")} style={{ paddingLeft: 10 + d * 16 }} onClick={() => setDomSel(i)}>
                <span className="el-b">‹</span><span className="el-t">{tag}</span>
                {attrs && <span className="el-a"> {attrs.split("=")[0]}=<span className="el-v">{attrs.split("=").slice(1).join("=")}</span></span>}
                <span className="el-b">›</span>
                {text && <span className="el-x">{text}</span>}
                {text && <><span className="el-b">‹/</span><span className="el-t">{tag}</span><span className="el-b">›</span></>}
              </div>
            ))}
          </div>
          <div className="dt-side">
            <div className="dt-cap">Styles</div>
            <div className="st-blk"><span className="st-sel">.hero</span> <span className="el-b">{'{'}</span>
              <div className="st-p"><input type="checkbox" defaultChecked readOnly />display: <b>flex</b>;</div>
              <div className="st-p"><input type="checkbox" defaultChecked readOnly />gap: <b>24px</b>;</div>
              <div className="st-p"><input type="checkbox" defaultChecked readOnly />padding: <b>96px 32px</b>;</div>
              <span className="el-b">{'}'}</span><span className="st-src">app.css:42</span>
            </div>
            <div className="st-blk"><span className="st-sel">body</span> <span className="el-b">{'{'}</span>
              <div className="st-p"><input type="checkbox" defaultChecked readOnly />font-family: <b>Inter</b>;</div>
              <span className="el-b">{'}'}</span><span className="st-src">tokens.css:3</span>
            </div>
            <div className="dt-cap">Box model</div>
            <div className="bm m"><span className="bm-l">24</span>
              <div className="bm b"><span className="bm-l">1</span>
                <div className="bm p"><span className="bm-l">32</span>
                  <div className="bm c">1187 × 640</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {tab === "console" && (
        <div className="dt-col">
          <div className="con-bar">
            {["All", "Errors", "Warnings", "Info"].map((f, i) => <button key={f} className={"chip" + (i === 0 ? " on" : "")}>{f}</button>)}
            <span style={{ marginLeft: "auto" }} className="dt-dim">{logs.length} messages</span>
          </div>
          <div className="con-list">
            {logs.map(([lv, msg, src2], i) => (
              <div key={i} className={"con-row " + lv}>
                <span className="con-m">{lv === "echo" ? "› " + msg : lv === "result" ? "‹ " + msg : msg}</span>
                <span className="con-s mono">{src2}</span>
              </div>
            ))}
          </div>
          <div className="con-in">
            <span className="mono" style={{ color: "var(--ac)" }}>›</span>
            <input value={evalQ} placeholder="Evaluate — try 128*0.85" onChange={(e) => setEvalQ(e.target.value)} onKeyDown={(e) => e.key === "Enter" && runEval()} />
          </div>
        </div>
      )}

      {tab === "network" && (
        <div className="dt-split">
          <div className="dt-main">
            <div className="con-bar">
              {["All", "Fetch", "JS", "CSS", "Img", "Doc"].map((f, i) => <button key={f} className={"chip" + (i === 0 ? " on" : "")}>{f}</button>)}
              <select className="dt-sel"><option>No throttling</option><option>Fast 4G</option><option>Slow 4G</option><option>Offline</option></select>
            </div>
            <div className="net-hd"><span>Name</span><span>Status</span><span>Size</span><span>Time</span><span style={{ flex: 1 }}>Waterfall</span></div>
            <div className="net-list">
              {NET_ROWS.map(([type, name, st, size, ms, off, w, clr], i) => (
                <div key={i} className={"net-row" + (i === netSel ? " on" : "") + (st === 0 ? " blk" : "")} onClick={() => setNetSel(i)}>
                  <span className="n mono">{name}</span>
                  <span className={"s mono" + (st === 0 ? " bad" : st === 304 ? " dim" : "")}>{st === 0 ? "blocked" : st}</span>
                  <span className="z mono">{size}</span>
                  <span className="t mono">{ms} ms</span>
                  <span className="wf"><i style={{ left: off + "%", width: Math.max(w, 2) + "%", background: clr }} /></span>
                </div>
              ))}
            </div>
            <div className="net-sum dt-dim">12 requests · 259 kB transferred · Finish 412 ms · 2 blocked by Shield</div>
          </div>
          <div className="dt-side">
            <div className="dt-cap">{NET_ROWS[netSel][1]}</div>
            <div className="kvrow"><span>Method</span><b>GET</b></div>
            <div className="kvrow"><span>Status</span><b>{NET_ROWS[netSel][2] || "Blocked"}</b></div>
            <div className="kvrow"><span>Type</span><b>{NET_ROWS[netSel][0]}</b></div>
            <div className="kvrow"><span>Remote</span><b className="mono">104.18.2.1:443 · h3</b></div>
            <div className="dt-cap" style={{ marginTop: 14 }}>Timing</div>
            {[["Queued", 4], ["DNS", 8], ["Connect", 16], ["TLS", 12], ["Waiting", 38], ["Download", 22]].map(([k, v]) => (
              <div className="tmrow" key={k}><span>{k}</span><i style={{ width: v * 2 + "px" }} /><b className="mono">{v} ms</b></div>
            ))}
          </div>
        </div>
      )}

      {tab === "sources" && (
        <div className="dt-3col">
          <div className="src-tree">
            <div className="dt-cap">nova.app</div>
            {["src/", "  state.js", "  cart.js ●", "  router.js", "styles/", "  tokens.css", "index.html"].map((f) => (
              <div key={f} className={"src-f mono" + (f.includes("cart") ? " on" : "")}>{f}</div>
            ))}
          </div>
          <div className="src-code mono">
            {SRC_CODE.map((line, i) => (
              <div key={i} className={"src-ln" + (i === 8 ? " cur" : "")}>
                <span className="src-n">{i === 7 ? <i className="bp" /> : null}{i + 1}</span>
                <span className="src-t">{line || " "}</span>
                {i === 8 && <span className="src-paused">paused</span>}
              </div>
            ))}
          </div>
          <div className="dt-side">
            <div className="dt-cap">Watch</div>
            <div className="kvrow mono"><span>cart.total</span><b>128.40</b></div>
            <div className="kvrow mono"><span>match.pct</span><b>0.15</b></div>
            <div className="dt-cap" style={{ marginTop: 12 }}>Call stack</div>
            {["applyDiscount — cart.js:9", "checkout — cart.js:31", "onClick — app.js:112"].map((s, i) => <div key={s} className={"stk mono" + (i === 0 ? " on" : "")}>{s}</div>)}
            <div className="dt-cap" style={{ marginTop: 12 }}>Scope · Local</div>
            <div className="kvrow mono"><span>code</span><b>"SAVE20"</b></div>
            <div className="kvrow mono"><span>valid</span><b style={{ color: "var(--good)" }}>true</b></div>
          </div>
        </div>
      )}

      {tab === "performance" && (
        <div className="dt-col" style={{ padding: "10px 14px", gap: 12, overflowY: "auto" }}>
          <div className="dt-cap" style={{ padding: 0 }}>Frames · 60 fps steady</div>
          <div className="fps">{Array.from({ length: 48 }, (_, i) => <i key={i} style={{ height: (i % 9 === 7 ? 40 : 85 + (i % 4) * 3) + "%" }} />)}</div>
          <div className="dt-cap" style={{ padding: 0 }}>Main thread</div>
          <div className="flame">
            <div className="fl-row">{[[0, 30, "#2e8dff", "evaluate"], [32, 20, "#7aa7ff", "parse"], [58, 34, "#2e8dff", "applyDiscount"]].map(([l, w, c, n]) => <i key={n} style={{ left: l + "%", width: w + "%", background: c }}>{n}</i>)}</div>
            <div className="fl-row">{[[4, 18, "#c792ea", "layout"], [60, 12, "#c792ea", "layout"], [76, 10, "#7ee2a8", "paint"]].map(([l, w, c, n], i) => <i key={n + i} style={{ left: l + "%", width: w + "%", background: c }}>{n}</i>)}</div>
            <div className="fl-row">{[[8, 8, "#7ee2a8", "paint"], [80, 6, "#e2c08d", "composite"]].map(([l, w, c, n]) => <i key={n} style={{ left: l + "%", width: w + "%", background: c }}>{n}</i>)}</div>
          </div>
          <div className="perf-leg">
            {[["Scripting", "41%", "#2e8dff"], ["Rendering", "22%", "#c792ea"], ["Painting", "9%", "#7ee2a8"], ["Idle", "28%", "#3a3a40"]].map(([k, v, c]) => (
              <span key={k}><i style={{ background: c }} />{k} <b className="mono">{v}</b></span>
            ))}
          </div>
          <div className="vitrow">
            {[["LCP", "0.9 s", true], ["INP", "24 ms", true], ["CLS", "0.00", true], ["TTFB", "80 ms", true], ["FCP", "0.5 s", true]].map(([k, v]) => (
              <div key={k} className="vit"><span className="k mono">{k}</span><span className="v mono">{v}</span><Check size={11} color="var(--good)" /></div>
            ))}
          </div>
        </div>
      )}

      {tab === "storage" && (
        <div className="dt-split">
          <div className="src-tree" style={{ width: 170 }}>
            <div className="dt-cap">Storage</div>
            {["Local storage", "Session storage", "Cookies", "IndexedDB", "Cache storage"].map((f, i) => <div key={f} className={"src-f" + (i === 0 ? " on" : "")}>{f}</div>)}
          </div>
          <div className="dt-main">
            <div className="net-hd" style={{ gridTemplateColumns: "1fr 1.6fr" }}><span>Key</span><span>Value</span></div>
            {[["nova.theme", '"dark"'], ["nova.accent", '"#2e8dff"'], ["session.id", '"9f2c…a1"'], ["cart", '{ items: 3, total: 128.4 }'], ["zen.timer", "null"], ["tabs.pinned", "[2]"]].map(([k, v]) => (
              <div key={k} className="st-row mono"><span>{k}</span><span className="dt-dim">{v}</span></div>
            ))}
            <div className="net-sum dt-dim">6 keys · 1.2 kB · isolated per-site</div>
          </div>
        </div>
      )}

      {tab === "lighthouse" && (
        <div className="dt-col" style={{ padding: 16, overflowY: "auto" }}>
          <div className="lh-rings">
            {[["Performance", 99], ["Accessibility", 100], ["Best practices", 100], ["SEO", 92]].map(([k, v]) => (
              <div key={k} className="lh">
                <svg viewBox="0 0 44 44" width="64" height="64">
                  <circle cx="22" cy="22" r="19" fill="none" stroke="var(--c3)" strokeWidth="3.5" />
                  <circle cx="22" cy="22" r="19" fill="none" stroke={v >= 95 ? "var(--good)" : "#ffb86b"} strokeWidth="3.5"
                    strokeDasharray={`${(v / 100) * 119.4} 119.4`} strokeLinecap="round" transform="rotate(-90 22 22)" />
                  <text x="22" y="26" textAnchor="middle" fontSize="12" fill="var(--tx)" fontFamily="var(--mono)">{v}</text>
                </svg>
                <span>{k}</span>
              </div>
            ))}
          </div>
          <div className="dt-cap" style={{ padding: "8px 0 2px" }}>Opportunities</div>
          {[["Preload hero.avif", "saves 120 ms", true], ["Serve grid.svg from cache", "saves 12 ms", true], ["Reduce unused JS in app.js", "18 kB unused", false]].map(([t, s, ok]) => (
            <div key={t} className="lh-row">{ok ? <Check size={13} color="var(--good)" /> : <Ban size={13} color="#ffb86b" />}<span>{t}</span><span className="dt-dim" style={{ marginLeft: "auto" }}>{s}</span></div>
          ))}
        </div>
      )}

      {tab === "causal" && (
        <div className="dt-col" style={{ padding: "10px 14px", overflowY: "auto", gap: 4 }}>
          <div className="dt-dim" style={{ paddingBottom: 6 }}>DevTools that answer <b style={{ color: "var(--tx)" }}>why</b> — not just show state. Record/replay is deterministic; bundles are safe to share.</div>
          <CausalList />
          <div style={{ display: "flex", gap: 8, paddingTop: 10 }}>
            <button className="hclear" style={{ height: 26 }}>● Record</button>
            <button className="hclear" style={{ height: 26 }}>Replay</button>
            <button className="hclear" style={{ height: 26 }}>Export safe diagnostic bundle</button>
          </div>
        </div>
      )}
      {tab === "security" && (
        <div className="dt-split">
          <div className="dt-main" style={{ padding: 14 }}>
            <div className="sec-big"><ShieldCheck size={18} color="var(--good)" /> This page is secure — grade <b className="mono" style={{ color: "var(--good)" }}>A+</b></div>
            {[["TLS 1.3 · X25519 · AES-128-GCM", true], ["Certificate valid — expires in 71 days", true], ["HSTS enforced · preloaded", true], ["CSP: default-src 'self'", true], ["No mixed content", true]].map(([t]) => (
              <div key={t} className="lh-row"><Check size={13} color="var(--good)" /><span>{t}</span></div>
            ))}
          </div>
          <div className="dt-side">
            <div className="dt-cap">Connections</div>
            {[["linear.app", "A+"], ["fonts.nova.app", "A+"], ["cdn.nova.app", "A"]].map(([d, g]) => (
              <div key={d} className="kvrow mono"><span>{d}</span><b style={{ color: "var(--good)" }}>{g}</b></div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

const SC = [
  ["Navigate", [
    ["Command palette", ["⌘K"]], ["Just start typing", ["a…z"]],
    ["Reload page", ["⌘R"]], ["Find in page", ["⌘F"]],
    ["Ask Turing", ["⌘E"]], ["Copy page URL", ["⇧⌘C"]],
    ["Bookmark page", ["⌘D"]], ["Settings", ["⌘,"]],
    ["Link hints", ["⌥⌘L"]], ["Search all tabs", ["⌥⌘A"]],
  ]],
  ["Tabs", [
    ["New tab", ["⌘T"]], ["Close tab", ["⌘W"]],
    ["Reopen closed tab", ["⇧⌘T"]], ["Next / previous tab", ["⌃Tab", "⌃⇧Tab"]],
    ["Cycle tabs", ["⇧⌘]", "⇧⌘["]], ["Jump to tab", ["⌘1–9"]],
    ["Close (mouse)", ["middle-click"]], ["Rename", ["double-click"]],
    ["All tabs & overflow", ["⇧⌘A"]], ["Task manager", ["⇧⌘M"]],
  ]],
  ["Workspace", [
    ["Toggle sidebar", ["⇧⌘S"]], ["Zen mode", ["⌘↵"]],
    ["Reading list", ["⌥⌘R"]], ["Save to reading list", ["⇧⌘D"]],
    ["Project notes", ["⇧⌘N"]], ["Focus session", ["⌥⌘F"]],
    ["Capture", ["⇧⌘4"]],
    ["Bookmarks bar", ["⇧⌘B"]], ["Split view", ["⌘\\"]],
    ["Swap split panes", ["⇧⌘\\"]], ["Resize split", ["⌥⌘←", "⌥⌘→"]],
    ["Reader", ["⇧⌘R"]], ["Zoom", ["⌘+", "⌘−", "⌘0"]],
  ]],
  ["Menus & dialogs", [
    ["Context menu nav", ["↑", "↓", "↵"]], ["This overlay", ["⌘/"]],
    ["Dismiss anything", ["ESC"]],
  ]],
  ["DevTools · dev mode", [
    ["Elements / Console", ["⌥⌘I", "⌥⌘J"]], ["Network / Sources", ["⌥⌘N", "⌥⌘S"]],
  ]],
];

function ShortcutsOverlay({ close }) {
  return (
    <div className="scveil" onClick={close}>
      <div className="sc" onClick={(e) => e.stopPropagation()}>
        <div className="sc-h">
          <Command size={18} color="var(--ac)" /><span className="t">Keyboard shortcuts</span>
          <span className="mono" style={{ marginLeft: "auto", fontSize: 11, color: "var(--tx3)", border: "1px solid var(--line)", borderRadius: 7, padding: "3px 7px" }}>ESC</span>
        </div>
        <div className="sc-grid">
          {SC.map(([g, rows]) => (
            <div className="sc-grp" key={g}>
              <div className="g">{g}</div>
              {rows.map(([label, keys]) => (
                <div className="scrow" key={label}>{label}<span className="keys">{keys.map((k, i) => <span key={i}>{k}</span>)}</span></div>
              ))}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
