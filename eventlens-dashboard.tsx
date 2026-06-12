import { useState, useMemo } from "react";
import { ScatterChart, Scatter, XAxis, YAxis, ZAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from "recharts";

const CATS = ["All", "Politics", "Sports", "Macro", "Crypto", "Weather", "Corporate"];
const W = { liq: 30, conc: 25, res: 25, cal: 20 };

const MARKETS = [
  { id: 1, name: "Team A wins NBA Finals", cat: "Sports", price: 0.61, platform: "Kalshi", liq: 92, conc: 88, res: 95, cal: 86, vol: "4.2M", spread: 0.8, whale: 6, brier: 0.041, reg: "Medium",
    warn: null, expl: "Deep order book, tight spread, broad participation. Price closely tracks sportsbook consensus. Sports match-winner markets in this category show strong historical calibration.",
    hist: [0.52,0.55,0.54,0.58,0.6,0.59,0.61],
    rd: { liq: "Spread 0.8¢; depth supports five-figure size", conc: "Largest holder ≈ 6% of open interest", res: "Objective outcome, official league result", cal: "Match-winner category Brier ≈ 0.04" },
    flags: [], resSummary: "Resolution is unambiguous: official NBA Finals result. No source, timing, or definitional risk identified." },
  { id: 2, name: "Candidate X resigns by Dec 31", cat: "Politics", price: 0.34, platform: "Polymarket", liq: 38, conc: 22, res: 31, cal: 48, vol: "180K", spread: 4.1, whale: 47, brier: 0.19, reg: "High",
    warn: "Whale-driven · ambiguous resolution", expl: "Single wallet holds 47% of YES exposure; price moved 9pts on one trade. Resolution text does not define 'resigns' vs. 'announces resignation.' Treat the 34% as a position, not a consensus probability.",
    hist: [0.21,0.22,0.24,0.23,0.31,0.33,0.34],
    rd: { liq: "Spread 4.1¢; ~$500 moves price several points", conc: "Largest wallet holds 47% of YES exposure", res: "'Resigns' undefined; no source hierarchy", cal: "Resignation markets historically overpriced" },
    flags: ["Undefined trigger: 'resigns' vs 'announces resignation'", "No source hierarchy specified", "Time-zone for deadline unstated", "Insider-risk category: subject controls outcome"],
    resSummary: "Resolves cleanly if the person formally leaves office before the deadline. Unclear if they announce resignation before Dec 31 but leave after it — the wording supports both readings." },
  { id: 3, name: "Fed cuts rates at July FOMC", cat: "Macro", price: 0.47, platform: "Kalshi", liq: 85, conc: 79, res: 92, cal: 81, vol: "2.8M", spread: 1.2, whale: 9, brier: 0.062, reg: "Low",
    warn: null, expl: "High liquidity, objective resolution (official FOMC statement), consistent with fed funds futures pricing. Macro categories show mild underconfidence near 50% historically.",
    hist: [0.39,0.41,0.44,0.43,0.45,0.46,0.47],
    rd: { liq: "Spread 1.2¢; deep two-sided book", conc: "Largest holder ≈ 9% of open interest", res: "Resolves on official FOMC statement", cal: "Macro category Brier ≈ 0.06" },
    flags: ["Minor: 'cut' size not specified (any cut counts?)"], resSummary: "Official FOMC statement is an unambiguous source. Only residual question is whether any cut size qualifies — wording implies yes." },
  { id: 4, name: "Company Q announces acquisition by Q3", cat: "Corporate", price: 0.18, platform: "Polymarket", liq: 29, conc: 35, res: 44, cal: 39, vol: "95K", spread: 5.6, whale: 38, brier: 0.21, reg: "High",
    warn: "Insider-risk category · thin book", expl: "Corporate-event contracts carry structural insider-information risk. Liquidity too shallow for the price to absorb informed flow. Two trades in the last 48h preceded news coverage — flagged for timing review.",
    hist: [0.12,0.11,0.13,0.12,0.16,0.17,0.18],
    rd: { liq: "Spread 5.6¢; book too thin to absorb informed flow", conc: "Largest wallet holds 38%; trades preceded news", res: "'Announces' vs 'completes' undefined", cal: "Corporate-event markets show worst category Brier" },
    flags: ["'Announces acquisition' — LOI? definitive agreement? rumor confirmed?", "Subject ambiguity: acquirer or target?", "Insider-risk: material non-public information likely exists", "Suspicious-timing pattern detected in last 48h"],
    resSummary: "High structural ambiguity. An announced letter of intent, a definitive agreement, and a completed deal are different events; the wording does not distinguish them. Combined with insider risk, this price should not be read as a public probability." },
  { id: 5, name: "Rain in NYC on Friday", cat: "Weather", price: 0.72, platform: "Kalshi", liq: 74, conc: 81, res: 97, cal: 90, vol: "410K", spread: 1.8, whale: 11, brier: 0.038, reg: "Low",
    warn: null, expl: "Objective resolution via official weather station data. Price consistent with NWS forecast. Weather markets show the strongest calibration of any category tracked.",
    hist: [0.61,0.66,0.65,0.7,0.69,0.71,0.72],
    rd: { liq: "Spread 1.8¢; adequate depth", conc: "Largest holder ≈ 11% of open interest", res: "Named weather station, defined measurement window", cal: "Weather category Brier ≈ 0.04 (best tracked)" },
    flags: [], resSummary: "Specifies the measuring station, the measurement threshold, and the local-time window. A model example of clean contract design." },
  { id: 6, name: "BTC above $150K by Sep 1", cat: "Crypto", price: 0.29, platform: "Polymarket", liq: 67, conc: 58, res: 89, cal: 62, vol: "1.1M", spread: 2.2, whale: 19, brier: 0.11, reg: "Low",
    warn: "Category overconfidence", expl: "Decent liquidity and clear resolution, but crypto long-shot contracts show persistent favorite–longshot bias in our calibration data: prices in the 20–35% band resolved YES only ~21% of the time.",
    hist: [0.33,0.31,0.3,0.27,0.28,0.3,0.29],
    rd: { liq: "Spread 2.2¢; reasonable depth", conc: "Largest wallet ≈ 19% of open interest", res: "Defined price source and timestamp", cal: "Crypto long-shots historically overpriced in 20–35% band" },
    flags: ["Minor: brief wick above threshold — does it count? Source feed defined but sampling unclear"],
    resSummary: "Price source is named, but whether a momentary spike on one exchange qualifies depends on the feed's sampling. Usually resolves cleanly; edge cases exist." },
  { id: 7, name: "Party Y wins District 12 special election", cat: "Politics", price: 0.58, platform: "Polymarket", liq: 21, conc: 30, res: 78, cal: 44, vol: "42K", spread: 7.3, whale: 41, brier: 0.18, reg: "High",
    warn: "Very thin · local race insider risk", expl: "Local races have scarce public polling, so informed local actors dominate. $500 of volume moves this price ~5pts. The 58% reflects a handful of participants, not aggregated public information.",
    hist: [0.5,0.51,0.49,0.55,0.54,0.57,0.58],
    rd: { liq: "Spread 7.3¢; ~$500 moves price ~5pts", conc: "Largest wallet holds 41% of open interest", res: "Outcome objective, but certification timing unstated", cal: "Local-politics category Brier well above national races" },
    flags: ["Resolution date vs certification date unclear", "Recount scenario unaddressed", "Local insider-information risk: low public data environment"],
    resSummary: "The winner is objectively determinable, but the contract does not say whether it resolves on election-night call, official certification, or after potential recounts." },
  { id: 8, name: "Player Z scores 30+ pts tonight", cat: "Sports", price: 0.42, platform: "Kalshi", liq: 49, conc: 64, res: 93, cal: 57, vol: "260K", spread: 3.4, whale: 16, brier: 0.13, reg: "High",
    warn: "Prop market · news-sensitive", expl: "Player props reprice slowly on injury/rotation news relative to sharp sportsbooks. Last lineup update not yet reflected. Resolution is objective but the displayed price may be ~30 minutes stale.",
    hist: [0.45,0.44,0.46,0.43,0.44,0.43,0.42],
    rd: { liq: "Spread 3.4¢; moderate depth", conc: "Largest holder ≈ 16% of open interest", res: "Official box score; DNP/postponement rules stated", cal: "Prop markets reprice slowly vs sharp books" },
    flags: ["Player props fall in proposed CFTC sensitive-category zone", "Injury/late-scratch information asymmetry"],
    resSummary: "Box-score resolution is objective and DNP rules are stated. The risk is regulatory (props are a contested category) and informational (lineup news), not definitional." },
];

const score = m => Math.round((W.liq*m.liq + W.conc*m.conc + W.res*m.res + W.cal*m.cal)/100);
const tier = s => s >= 75 ? ["High trust","#34d399"] : s >= 55 ? ["Moderate","#fbbf24"] : ["Low trust","#f87171"];
const regColor = r => r === "Low" ? "#34d399" : r === "Medium" ? "#fbbf24" : "#f87171";
const clarityColor = v => v >= 75 ? "#34d399" : v >= 50 ? "#fbbf24" : "#f87171";

const Bar = ({ label, val, hint }) => (
  <div style={{ marginBottom: 10 }}>
    <div style={{ display: "flex", justifyContent: "space-between", fontSize: 12, color: "#94a3b8", marginBottom: 3 }}>
      <span>{label}</span><span style={{ color: "#e2e8f0", fontVariantNumeric: "tabular-nums" }}>{val}/100</span>
    </div>
    <div style={{ height: 6, background: "#1e293b", borderRadius: 3 }}>
      <div style={{ height: 6, width: `${val}%`, borderRadius: 3, background: val >= 75 ? "#34d399" : val >= 55 ? "#fbbf24" : "#f87171", transition: "width .4s" }} />
    </div>
    <div style={{ fontSize: 11, color: "#64748b", marginTop: 2 }}>{hint}</div>
  </div>
);

const Drivers = ({ m }) => {
  const rows = [
    ["Liquidity", "liq", m.rd.liq], ["Concentration", "conc", m.rd.conc],
    ["Resolution clarity", "res", m.rd.res], ["Category calibration", "cal", m.rd.cal],
  ].map(([label, k, reason]) => ({ label, ded: Math.round(W[k]*(100-m[k])/100), max: W[k], reason }));
  return (
    <div style={{ background: "#0b1322", border: "1px solid #1e293b", borderRadius: 10, padding: "12px 14px" }}>
      <div style={{ fontSize: 11, color: "#64748b", textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 8 }}>Why this score? (100 − deductions)</div>
      {rows.map(r => (
        <div key={r.label} style={{ display: "flex", gap: 10, marginBottom: 8, alignItems: "baseline" }}>
          <span style={{ color: r.ded > r.max*0.4 ? "#f87171" : r.ded > r.max*0.15 ? "#fbbf24" : "#34d399", fontWeight: 800, fontVariantNumeric: "tabular-nums", minWidth: 34, fontSize: 13 }}>−{r.ded}</span>
          <div>
            <span style={{ fontSize: 12, fontWeight: 700, color: "#cbd5e1" }}>{r.label}</span>
            <span style={{ fontSize: 11, color: "#64748b" }}> (max −{r.max})</span>
            <div style={{ fontSize: 11.5, color: "#94a3b8" }}>{r.reason}</div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default function EventLens() {
  const [cat, setCat] = useState("All");
  const [sel, setSel] = useState(null);
  const [tab, setTab] = useState("markets");
  const [resSel, setResSel] = useState(2);

  const rows = useMemo(() => MARKETS.filter(m => cat === "All" || m.cat === cat).map(m => ({ ...m, ts: score(m) })).sort((a,b) => b.ts - a.ts), [cat]);
  const scatter = MARKETS.map(m => ({ x: score(m), y: m.brier, name: m.name }));
  const rm = MARKETS.find(x => x.id === resSel);

  return (
    <div style={{ fontFamily: "ui-sans-serif, system-ui", background: "#0b1120", minHeight: "100vh", color: "#e2e8f0", padding: "24px 20px" }}>
      <div style={{ maxWidth: 1000, margin: "0 auto" }}>
        <div style={{ display: "flex", alignItems: "baseline", gap: 12, flexWrap: "wrap" }}>
          <h1 style={{ fontSize: 26, fontWeight: 800, margin: 0, letterSpacing: -0.5 }}>Event<span style={{ color: "#38bdf8" }}>Lens</span></h1>
          <span style={{ fontSize: 13, color: "#64748b" }}>A trust layer for prediction markets — we don't tell you the right price, we tell you when to trust the displayed one.</span>
        </div>

        <div style={{ display: "flex", gap: 14, margin: "18px 0", flexWrap: "wrap" }}>
          {[["Markets tracked","8 (demo)"],["Avg trust score", Math.round(rows.reduce((a,b)=>a+b.ts,0)/rows.length||0)],["Flagged markets", MARKETS.filter(x=>x.warn).length],["High reg. risk", MARKETS.filter(x=>x.reg==="High").length],["Calibration sample","312 resolved"]].map(([k,v]) => (
            <div key={k} style={{ background: "#111a2e", border: "1px solid #1e293b", borderRadius: 10, padding: "10px 16px", minWidth: 120 }}>
              <div style={{ fontSize: 11, color: "#64748b", textTransform: "uppercase", letterSpacing: 0.5 }}>{k}</div>
              <div style={{ fontSize: 20, fontWeight: 700 }}>{v}</div>
            </div>
          ))}
        </div>

        <div style={{ display: "flex", gap: 8, marginBottom: 16, flexWrap: "wrap" }}>
          {[["markets","Market scores"],["resolution","Resolution Risk Analyzer"],["validation","Validation"]].map(([id, label]) => (
            <button key={id} onClick={() => setTab(id)} style={{ background: tab===id ? "#1d4ed8" : "#111a2e", color: tab===id ? "#fff" : "#94a3b8", border: "1px solid #1e293b", borderRadius: 8, padding: "7px 14px", fontSize: 13, cursor: "pointer", fontWeight: 600 }}>{label}</button>
          ))}
        </div>

        {tab === "markets" && (
          <>
            <div style={{ display: "flex", gap: 6, marginBottom: 14, flexWrap: "wrap" }}>
              {CATS.map(c => (
                <button key={c} onClick={() => { setCat(c); setSel(null); }} style={{ background: cat===c ? "#0ea5e9" : "transparent", color: cat===c ? "#0b1120" : "#94a3b8", border: "1px solid " + (cat===c ? "#0ea5e9" : "#1e293b"), borderRadius: 999, padding: "4px 12px", fontSize: 12, cursor: "pointer", fontWeight: 600 }}>{c}</button>
              ))}
            </div>

            <div style={{ background: "#111a2e", border: "1px solid #1e293b", borderRadius: 12, overflow: "hidden" }}>
              <div style={{ display: "grid", gridTemplateColumns: "minmax(170px,2.1fr) 60px 60px 100px 80px 1.2fr", gap: 8, padding: "10px 14px", fontSize: 11, color: "#64748b", textTransform: "uppercase", letterSpacing: 0.5, borderBottom: "1px solid #1e293b" }}>
                <span>Market</span><span>Price</span><span>Trust</span><span>Rating</span><span>Reg. risk</span><span>Main warning</span>
              </div>
              {rows.map(r => {
                const [label, color] = tier(r.ts);
                const open = sel === r.id;
                return (
                  <div key={r.id}>
                    <div onClick={() => setSel(open ? null : r.id)} style={{ display: "grid", gridTemplateColumns: "minmax(170px,2.1fr) 60px 60px 100px 80px 1.2fr", gap: 8, padding: "12px 14px", fontSize: 13, alignItems: "center", cursor: "pointer", background: open ? "#0f1a30" : "transparent", borderBottom: "1px solid #16213a" }}>
                      <div>
                        <div style={{ fontWeight: 600 }}>{r.name}</div>
                        <div style={{ fontSize: 11, color: "#64748b" }}>{r.platform} · {r.cat} · vol ${r.vol}</div>
                      </div>
                      <span style={{ fontVariantNumeric: "tabular-nums", fontWeight: 700 }}>{Math.round(r.price*100)}%</span>
                      <span style={{ fontVariantNumeric: "tabular-nums", fontWeight: 800, color }}>{r.ts}</span>
                      <span style={{ color, fontSize: 12, fontWeight: 700 }}>{label}</span>
                      <span style={{ color: regColor(r.reg), fontSize: 12, fontWeight: 700 }}>{r.reg}</span>
                      <span style={{ fontSize: 12, color: r.warn ? "#fca5a5" : "#475569" }}>{r.warn || "—"}</span>
                    </div>
                    {open && (
                      <div style={{ padding: "16px 18px", background: "#0d1628", borderBottom: "1px solid #16213a", display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 20 }}>
                        <div>
                          <Bar label="Liquidity" val={r.liq} hint={r.rd.liq} />
                          <Bar label="Concentration" val={r.conc} hint={r.rd.conc} />
                          <Bar label="Resolution clarity" val={r.res} hint={r.rd.res} />
                          <Bar label="Category calibration" val={r.cal} hint={r.rd.cal} />
                        </div>
                        <Drivers m={r} />
                        <div>
                          <div style={{ fontSize: 11, color: "#64748b", textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 6 }}>7-day price</div>
                          <div style={{ height: 64 }}>
                            <ResponsiveContainer width="100%" height="100%">
                              <LineChart data={r.hist.map((p,i)=>({i,p:Math.round(p*100)}))}>
                                <Line type="monotone" dataKey="p" stroke="#38bdf8" strokeWidth={2} dot={false} />
                                <YAxis hide domain={["dataMin-3","dataMax+3"]} /><XAxis hide dataKey="i" />
                              </LineChart>
                            </ResponsiveContainer>
                          </div>
                          <div style={{ fontSize: 11, color: "#64748b", textTransform: "uppercase", letterSpacing: 0.5, margin: "10px 0 4px" }}>AI assessment</div>
                          <p style={{ fontSize: 12.5, color: "#cbd5e1", lineHeight: 1.55, margin: 0 }}>{r.expl}</p>
                        </div>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
            <p style={{ fontSize: 11, color: "#475569", marginTop: 10 }}>Demo data. Composite = 100 − weighted deductions (liquidity 30 · concentration 25 · resolution 25 · calibration 20). All scores are computed ex-ante and timestamped before resolution.</p>
          </>
        )}

        {tab === "resolution" && rm && (
          <div style={{ display: "grid", gridTemplateColumns: "240px 1fr", gap: 16 }}>
            <div style={{ background: "#111a2e", border: "1px solid #1e293b", borderRadius: 12, padding: 8, alignSelf: "start" }}>
              {MARKETS.map(x => (
                <div key={x.id} onClick={() => setResSel(x.id)} style={{ padding: "9px 10px", borderRadius: 8, cursor: "pointer", background: resSel===x.id ? "#1d4ed8" : "transparent", marginBottom: 2 }}>
                  <div style={{ fontSize: 12.5, fontWeight: 600, color: resSel===x.id ? "#fff" : "#cbd5e1" }}>{x.name}</div>
                  <div style={{ fontSize: 11, color: resSel===x.id ? "#bfdbfe" : clarityColor(x.res), fontWeight: 700 }}>Clarity {x.res}/100 · {x.flags.length} flag{x.flags.length!==1?"s":""}</div>
                </div>
              ))}
            </div>
            <div style={{ background: "#111a2e", border: "1px solid #1e293b", borderRadius: 12, padding: 20 }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: 10 }}>
                <h3 style={{ margin: 0, fontSize: 16 }}>{rm.name}</h3>
                <div style={{ background: "#0b1322", border: `1px solid ${clarityColor(rm.res)}`, color: clarityColor(rm.res), borderRadius: 8, padding: "4px 12px", fontWeight: 800, fontSize: 14 }}>Clarity {rm.res}/100</div>
              </div>
              <p style={{ fontSize: 12, color: "#64748b", margin: "4px 0 14px" }}>AI contract-wording analysis · {rm.platform} · regulatory risk: <span style={{ color: regColor(rm.reg), fontWeight: 700 }}>{rm.reg}</span></p>

              <div style={{ fontSize: 11, color: "#64748b", textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 6 }}>Flags</div>
              {rm.flags.length === 0 ? (
                <p style={{ fontSize: 13, color: "#34d399", margin: "0 0 14px" }}>✓ No resolution-risk flags identified</p>
              ) : (
                <div style={{ marginBottom: 14 }}>
                  {rm.flags.map((f,i) => (
                    <div key={i} style={{ display: "flex", gap: 8, fontSize: 13, color: "#fca5a5", marginBottom: 5 }}>
                      <span>⚠</span><span style={{ color: "#e2e8f0" }}>{f}</span>
                    </div>
                  ))}
                </div>
              )}

              <div style={{ fontSize: 11, color: "#64748b", textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 6 }}>Human summary</div>
              <p style={{ fontSize: 13.5, color: "#cbd5e1", lineHeight: 1.6, margin: "0 0 14px" }}>{rm.resSummary}</p>

              <div style={{ fontSize: 11, color: "#64748b", textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 6 }}>Structured output</div>
              <pre style={{ background: "#0b1322", border: "1px solid #1e293b", borderRadius: 8, padding: 12, fontSize: 11.5, color: "#7dd3fc", overflow: "auto", margin: 0 }}>{JSON.stringify({ resolution_clarity_score: rm.res, regulatory_risk: rm.reg, flags: rm.flags, human_summary: rm.resSummary.slice(0, 110) + "…" }, null, 2)}</pre>
            </div>
          </div>
        )}

        {tab === "validation" && (
          <div style={{ background: "#111a2e", border: "1px solid #1e293b", borderRadius: 12, padding: 20 }}>
            <h3 style={{ margin: "0 0 4px", fontSize: 16 }}>Does the ex-ante trust score predict ex-post calibration?</h3>
            <p style={{ fontSize: 13, color: "#94a3b8", margin: "0 0 10px", lineHeight: 1.5 }}>Every trust score is computed and timestamped <strong style={{ color: "#e2e8f0" }}>before</strong> resolution; Brier error (p − y)² is observed only <strong style={{ color: "#e2e8f0" }}>after</strong>. Snapshots are append-only — no look-ahead bias. The claim: markets scored low-trust should show materially higher realized error.</p>
            <div style={{ height: 300 }}>
              <ResponsiveContainer width="100%" height="100%">
                <ScatterChart margin={{ top: 10, right: 20, bottom: 30, left: 10 }}>
                  <CartesianGrid stroke="#1e293b" />
                  <XAxis type="number" dataKey="x" name="Trust score" domain={[20, 100]} stroke="#64748b" fontSize={12} label={{ value: "Ex-ante trust score", position: "insideBottom", offset: -18, fill: "#94a3b8", fontSize: 12 }} />
                  <YAxis type="number" dataKey="y" name="Brier" domain={[0, 0.25]} stroke="#64748b" fontSize={12} label={{ value: "Ex-post Brier error", angle: -90, position: "insideLeft", fill: "#94a3b8", fontSize: 12 }} />
                  <ZAxis range={[90, 90]} />
                  <Tooltip cursor={{ strokeDasharray: "3 3" }} contentStyle={{ background: "#0b1120", border: "1px solid #1e293b", borderRadius: 8, fontSize: 12 }} formatter={(v,n)=>[v, n==="x"?"Trust score":"Brier error"]} labelFormatter={()=>""} />
                  <Scatter data={scatter} fill="#38bdf8" />
                </ScatterChart>
              </ResponsiveContainer>
            </div>
            <p style={{ fontSize: 12, color: "#64748b", marginTop: 8 }}>Demo relationship (negative slope = methodology works). Planned extensions: subscore ablation tests, category-level calibration curves, out-of-sample holdout. Microstructure note: trade direction uses on-chain OrderFilled events, not inferred order-book direction.</p>
          </div>
        )}
      </div>
    </div>
  );
}