import pathlib
HTML = r'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>MotiveAR | Parkinson's Dashboard</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    :root {
      --sidebar-bg: #0f1117;
      --sidebar-w: 220px;
      --bg: #f0f2f8;
      --card: #ffffff;
      --accent: #5b6ef5;
      --accent2: #eef0ff;
      --green: #22c55e;
      --red: #ef4444;
      --orange: #f97316;
      --purple: #a855f7;
      --text: #1a1d2e;
      --muted: #8b92a5;
      --border: #e4e7f0;
      --radius: 14px;
    }
    body { font-family:'Inter',sans-serif; background:var(--bg); color:var(--text); display:flex; height:100vh; overflow:hidden; }

    /* SIDEBAR */
    .sidebar { width:var(--sidebar-w); background:var(--sidebar-bg); display:flex; flex-direction:column; padding:24px 0; flex-shrink:0; }
    .sidebar-logo { display:flex; align-items:center; gap:10px; padding:0 20px 24px; font-weight:700; font-size:16px; color:#fff; }
    .sidebar-logo .dot { width:30px;height:30px;background:var(--accent);border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:15px;font-weight:800;color:#fff; }
    .sidebar-search { margin:0 14px 18px; position:relative; }
    .sidebar-search input { width:100%;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.08);border-radius:8px;padding:8px 12px 8px 30px;color:#fff;font-size:12px;outline:none;font-family:inherit; }
    .sidebar-search input::placeholder { color:rgba(255,255,255,0.28); }
    .sidebar-search .si { position:absolute;left:10px;top:50%;transform:translateY(-50%);opacity:0.38;font-size:12px; }
    .nav-section { padding:0 10px; flex:1; }
    .nav-item { display:flex;align-items:center;gap:10px;padding:10px 12px;border-radius:8px;font-size:13px;color:rgba(255,255,255,0.5);cursor:pointer;transition:all .15s;margin-bottom:2px; }
    .nav-item:hover { background:rgba(255,255,255,0.06);color:#fff; }
    .nav-item.active { background:var(--accent);color:#fff; }
    .nav-item .badge { margin-left:auto;background:var(--red);color:#fff;font-size:10px;font-weight:700;border-radius:10px;padding:1px 7px; }
    .nav-divider { height:1px;background:rgba(255,255,255,0.07);margin:10px 10px; }
    .sidebar-footer { padding:14px 14px 0;border-top:1px solid rgba(255,255,255,0.07);display:flex;align-items:center;gap:10px; }
    .avatar-sm { width:34px;height:34px;border-radius:50%;background:linear-gradient(135deg,#5b6ef5,#a855f7);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:12px;color:#fff;flex-shrink:0; }
    .sidebar-footer .sname { font-size:12px;font-weight:600;color:#fff; }
    .sidebar-footer .srole { font-size:10px;color:rgba(255,255,255,0.38); }

    /* MAIN */
    .main { flex:1;display:flex;flex-direction:column;overflow:hidden; }
    .topbar { background:var(--card);border-bottom:1px solid var(--border);padding:16px 28px;display:flex;align-items:center;justify-content:space-between;flex-shrink:0; }
    .topbar h1 { font-size:18px;font-weight:700; }
    .topbar p  { font-size:12px;color:var(--muted);margin-top:2px; }
    .topbar-right { display:flex;align-items:center;gap:12px; }
    .icon-btn { width:36px;height:36px;border-radius:8px;border:1px solid var(--border);background:var(--card);display:flex;align-items:center;justify-content:center;cursor:pointer;position:relative;color:var(--muted); }
    .notif-dot { position:absolute;top:7px;right:7px;width:7px;height:7px;background:var(--red);border-radius:50%;border:2px solid #fff; }
    .topbar-avatar { width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,#5b6ef5,#a855f7);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:12px;color:#fff;cursor:pointer; }
    .live-indicator { display:flex;align-items:center;gap:6px;font-size:11px;color:var(--green);font-weight:600; }
    .live-dot { width:7px;height:7px;border-radius:50%;background:var(--green);animation:pulse 1.4s ease infinite; }
    @keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.45;transform:scale(1.5)} }

    .content { flex:1;overflow-y:auto;padding:20px 28px;display:flex;flex-direction:column;gap:18px; }
    .content::-webkit-scrollbar { width:4px; }
    .content::-webkit-scrollbar-thumb { background:var(--border);border-radius:4px; }

    /* STAT CARDS */
    .stat-row { display:grid;grid-template-columns:repeat(4,1fr);gap:14px; }
    .stat-card { background:var(--card);border-radius:var(--radius);padding:18px 20px;border:1px solid var(--border); }
    .stat-card-top { display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:8px; }
    .stat-icon { width:38px;height:38px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:17px;flex-shrink:0; }
    .stat-label { font-size:11px;color:var(--muted);font-weight:500;text-transform:uppercase;letter-spacing:0.4px; }
    .stat-val { font-size:26px;font-weight:700;letter-spacing:-1px;margin-top:2px; }
    .stat-delta { font-size:11px;font-weight:600;margin-top:3px; }
    .du { color:var(--green); } .dd { color:var(--red); }
    .stat-mini { height:38px;width:100%;margin-top:10px;display:block; }

    /* MID ROW */
    .mid-row { display:grid;grid-template-columns:1fr 315px;gap:14px; }
    .card { background:var(--card);border-radius:var(--radius);border:1px solid var(--border);padding:20px; }
    .card-hdr { display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:12px; }
    .card-hdr h3 { font-size:14px;font-weight:700; }
    .card-hdr .sub { font-size:11px;color:var(--muted);margin-top:2px; }
    .pill-sel { background:var(--bg);border:1px solid var(--border);border-radius:7px;padding:5px 10px;font-size:11px;color:var(--muted);font-family:inherit;cursor:pointer;outline:none; }
    .chart-kpis { display:flex;gap:22px;margin-bottom:12px; }
    .kpi-val { font-size:19px;font-weight:700; }
    .kpi-label { font-size:11px;color:var(--muted);margin-top:1px; }
    .kpi-delta { font-size:11px;font-weight:600;margin-left:5px; }

    /* SIDE CARDS */
    .side-cards { display:flex;flex-direction:column;gap:14px; }
    .side-card { background:var(--card);border-radius:var(--radius);border:1px solid var(--border);padding:18px; }
    .side-card.dark { background:#1a1d2e;border-color:#1a1d2e;color:#fff; }
    .sc-top { display:flex;align-items:center;justify-content:space-between;margin-bottom:12px; }
    .sc-top h4 { font-size:13px;font-weight:600;display:flex;align-items:center;gap:8px; }
    .sc-icon { width:26px;height:26px;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:13px; }
    .sc-big { font-size:26px;font-weight:700; }
    .sc-sub { font-size:11px;color:var(--muted);margin-top:2px; }
    .side-card.dark .sc-sub { color:rgba(255,255,255,0.38); }
    .dot-matrix { display:flex;align-items:center;justify-content:flex-end;gap:4px; }
    .dot-col { display:flex;flex-direction:column;gap:4px; }
    .dot-cell { width:10px;height:10px;border-radius:50%;background:var(--red);opacity:0.14;transition:opacity .3s; }
    .dot-cell.lit { opacity:1; }

    /* TABLE */
    .table-card { background:var(--card);border-radius:var(--radius);border:1px solid var(--border);overflow:hidden; }
    .table-top { padding:16px 22px;display:flex;align-items:center;justify-content:space-between; }
    .table-top h3 { font-size:14px;font-weight:700; }
    .table-top .sub { font-size:11px;color:var(--muted);margin-top:2px; }
    .tsearch { display:flex;align-items:center;gap:8px; }
    .tsearch input { border:1px solid var(--border);border-radius:8px;padding:7px 12px;font-size:12px;outline:none;font-family:inherit;background:var(--bg);color:var(--text); }
    .filter-btn { border:1px solid var(--border);border-radius:8px;padding:7px 14px;background:var(--card);font-size:12px;cursor:pointer;font-family:inherit;display:flex;align-items:center;gap:5px;color:var(--muted); }
    table { width:100%;border-collapse:collapse; }
    thead tr { border-bottom:1px solid var(--border); }
    thead th { padding:9px 20px;font-size:10px;font-weight:600;color:var(--muted);text-align:left;text-transform:uppercase;letter-spacing:0.5px; }
    tbody tr { border-bottom:1px solid var(--border);transition:background .12s; }
    tbody tr:last-child { border-bottom:none; }
    tbody tr:hover { background:var(--bg); }
    tbody td { padding:11px 20px;font-size:13px; }
    .pcell { display:flex;align-items:center;gap:10px; }
    .pavatar { width:30px;height:30px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:11px;color:#fff;flex-shrink:0; }
    .spill { padding:3px 10px;border-radius:20px;font-size:11px;font-weight:600; }
    .spill.stable   { background:#dcfce7;color:#15803d; }
    .spill.elevated { background:#fef9c3;color:#a16207; }
    .spill.critical { background:#fee2e2;color:#b91c1c; }
    .abtn { background:var(--accent2);color:var(--accent);border:none;border-radius:6px;padding:5px 12px;font-size:11px;font-weight:600;cursor:pointer;font-family:inherit; }
    canvas { display:block; }
  </style>
</head>
<body>

<!-- SIDEBAR -->
<nav class="sidebar">
  <div class="sidebar-logo">
    <div class="dot">M</div>MotiveAR
  </div>
  <div class="sidebar-search">
    <span class="si">&#128269;</span>
    <input type="text" placeholder="Search here..." />
  </div>
  <div class="nav-section">
    <div class="nav-item active">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>
      Overview
    </div>
    <div class="nav-item">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>
      Sessions
    </div>
    <div class="nav-item">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/></svg>
      Doctors
    </div>
    <div class="nav-item">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
      Patients
    </div>
    <div class="nav-divider"></div>
    <div class="nav-item">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/></svg>
      Reports
    </div>
    <div class="nav-item">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
      Messages <span class="badge">3</span>
    </div>
    <div class="nav-item">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2"/><rect x="9" y="3" width="6" height="4" rx="1"/></svg>
      Prescriptions
    </div>
  </div>
  <div class="sidebar-footer">
    <div class="avatar-sm">DR</div>
    <div>
      <div class="sname">Dr. Rivera</div>
      <div class="srole">Neurologist &middot; PD Unit</div>
    </div>
  </div>
</nav>

<!-- MAIN -->
<div class="main">
  <div class="topbar">
    <div>
      <h1>Welcome back, Dr. Rivera</h1>
      <p>Track and manage your Parkinson's patient motor data in real time.</p>
    </div>
    <div class="topbar-right">
      <div class="live-indicator"><div class="live-dot"></div>Live Data</div>
      <div class="icon-btn">
        <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>
      </div>
      <div class="icon-btn">
        <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
        <div class="notif-dot"></div>
      </div>
      <div class="topbar-avatar">DR</div>
    </div>
  </div>

  <div class="content">

    <!-- STAT CARDS -->
    <div class="stat-row">
      <div class="stat-card">
        <div class="stat-card-top">
          <div>
            <div class="stat-label">Active Patients</div>
            <div class="stat-val" id="stat-patients">142</div>
            <div class="stat-delta du">&#9650; 12% from last week</div>
          </div>
          <div class="stat-icon" style="background:#eef0ff;">&#129504;</div>
        </div>
        <canvas class="stat-mini" id="chart-patients" height="38"></canvas>
      </div>
      <div class="stat-card">
        <div class="stat-card-top">
          <div>
            <div class="stat-label">Avg Tremor Freq</div>
            <div class="stat-val" id="stat-tremor">4.2 <span style="font-size:13px;font-weight:500;color:var(--muted)">Hz</span></div>
            <div class="stat-delta dd" id="delta-tremor">&#9660; 0.3 Hz vs yesterday</div>
          </div>
          <div class="stat-icon" style="background:#fff0f0;">&#9889;</div>
        </div>
        <canvas class="stat-mini" id="chart-tremor" height="38"></canvas>
      </div>
      <div class="stat-card">
        <div class="stat-card-top">
          <div>
            <div class="stat-label">Motor Stability</div>
            <div class="stat-val" id="stat-stability">87 <span style="font-size:13px;font-weight:500;color:var(--muted)">%</span></div>
            <div class="stat-delta du" id="delta-stability">&#9650; 5% this session</div>
          </div>
          <div class="stat-icon" style="background:#f0fff4;">&#127919;</div>
        </div>
        <canvas class="stat-mini" id="chart-stability" height="38"></canvas>
      </div>
      <div class="stat-card">
        <div class="stat-card-top">
          <div>
            <div class="stat-label">Drills Completed</div>
            <div class="stat-val" id="stat-drills">38</div>
            <div class="stat-delta du" id="delta-drills">&#9650; 8 new today</div>
          </div>
          <div class="stat-icon" style="background:#fdf4ff;">&#10003;</div>
        </div>
        <canvas class="stat-mini" id="chart-drills" height="38"></canvas>
      </div>
    </div>

    <!-- MID ROW -->
    <div class="mid-row">
      <div class="card">
        <div class="card-hdr">
          <div>
            <h3>Motor Signal Overview</h3>
            <div class="sub">Live tremor frequency &amp; stability &mdash; all patients</div>
          </div>
          <select class="pill-sel"><option>Last 60s</option><option>Last 2m</option></select>
        </div>
        <div class="chart-kpis">
          <div>
            <span class="kpi-val" id="live-trem">4.2</span>
            <span style="font-size:12px;color:var(--muted)"> Hz</span>
            <span class="kpi-delta dd" id="kpi-td">&#9660; 0.3</span>
            <div class="kpi-label">Avg Tremor</div>
          </div>
          <div>
            <span class="kpi-val" id="live-stab">87</span>
            <span style="font-size:12px;color:var(--muted)"> %</span>
            <span class="kpi-delta du" id="kpi-sd">&#9650; 5%</span>
            <div class="kpi-label">Stability</div>
          </div>
          <div>
            <span class="kpi-val" id="live-rms">0.18</span>
            <span style="font-size:12px;color:var(--muted)"> g</span>
            <span class="kpi-delta dd" id="kpi-rd">&#9660; 0.02</span>
            <div class="kpi-label">RMS Accel</div>
          </div>
          <div>
            <span class="kpi-val" id="live-spikes">24</span>
            <span style="font-size:12px;color:var(--muted)"> events</span>
            <div class="kpi-label">Spike Events</div>
          </div>
        </div>
        <canvas id="main-chart" height="148" style="width:100%;"></canvas>
      </div>
      <div class="side-cards">
        <div class="side-card">
          <div class="sc-top">
            <h4><div class="sc-icon" style="background:#fee2e2;">&#128308;</div>Tremor Spikes</h4>
            <span style="font-size:18px;color:var(--muted)">&#8943;</span>
          </div>
          <div style="display:flex;align-items:flex-end;justify-content:space-between;">
            <div>
              <div class="sc-big" id="spike-count">24</div>
              <div class="sc-sub">Detected today</div>
              <div style="font-size:11px;color:var(--red);font-weight:600;margin-top:4px;" id="spike-delta">&#9650; 6% vs yesterday</div>
            </div>
            <div class="dot-matrix" id="dot-matrix"></div>
          </div>
        </div>
        <div class="side-card dark">
          <div class="sc-top">
            <h4 style="color:#fff;"><div class="sc-icon" style="background:rgba(91,110,245,0.28);">&#128202;</div>Stability Score</h4>
            <span style="font-size:18px;color:rgba(255,255,255,0.25)">&#8943;</span>
          </div>
          <div style="display:flex;align-items:flex-end;gap:12px;">
            <div>
              <div style="display:flex;align-items:center;gap:8px;">
                <div class="sc-big" id="stability-big">87</div>
                <span id="stability-delta" style="font-size:11px;font-weight:700;color:#22c55e;">&#9650; 5%</span>
              </div>
              <div class="sc-sub">Avg across patients</div>
            </div>
            <canvas id="stab-bar" height="52" style="flex:1;min-width:80px;"></canvas>
          </div>
        </div>
      </div>
    </div>

    <!-- TABLE -->
    <div class="table-card">
      <div class="table-top">
        <div>
          <h3>Recent Patient Sessions</h3>
          <div class="sub">Live motor data &mdash; refreshes every second</div>
        </div>
        <div class="tsearch">
          <input type="text" placeholder="Search patient..." id="patient-search" />
          <button class="filter-btn">&#9776; Filters</button>
        </div>
      </div>
      <table>
        <thead>
          <tr>
            <th>Patient</th><th>Last Session</th><th>Tremor Hz</th>
            <th>Stability</th><th>Drills</th><th>Status</th><th>Action</th>
          </tr>
        </thead>
        <tbody id="patient-tbody"></tbody>
      </table>
    </div>

  </div>
</div>

<script>
// DATA
const PATIENTS = [
  {id:1,name:'James Whitfield', init:'JW',color:'#5b6ef5',age:67,side:'Right', bT:4.8,bS:72},
  {id:2,name:'Margaret Chen',   init:'MC',color:'#a855f7',age:72,side:'Left',  bT:3.2,bS:88},
  {id:3,name:'Robert Okafor',   init:'RO',color:'#f97316',age:58,side:'Both',  bT:6.1,bS:61},
  {id:4,name:'Susan Nakamura',  init:'SN',color:'#22c55e',age:74,side:'Right', bT:2.9,bS:91},
  {id:5,name:'Harold Petrov',   init:'HP',color:'#ef4444',age:63,side:'Left',  bT:5.5,bS:68},
  {id:6,name:'Dorothy Ellis',   init:'DE',color:'#0ea5e9',age:69,side:'Right', bT:3.8,bS:83},
  {id:7,name:'Thomas Reyes',    init:'TR',color:'#d946ef',age:61,side:'Both',  bT:7.2,bS:54},
];
const ST = PATIENTS.map(p=>({...p,tremor:p.bT,stability:p.bS,drills:Math.floor(Math.random()*8)+2,lastSession:rT(),spikes:Math.floor(p.bT*3+Math.random()*4)}));
function rT(){const m=Math.floor(Math.random()*55)+2;return m<60?m+'m ago':Math.floor(m/60)+'h '+m%60+'m ago';}

const SL=60;
const tS=Array.from({length:SL},(_,i)=>3+Math.sin(i*.3)*1.5+Math.random()*.5);
const sS=Array.from({length:SL},(_,i)=>85-Math.sin(i*.25)*10+Math.random()*4);
const rS=Array.from({length:SL},(_,i)=>0.1+Math.sin(i*.2)*.08+Math.random()*.05);
const mH={
  patients:Array.from({length:24},()=>130+Math.random()*20),
  tremor:  Array.from({length:24},()=>3.5+Math.random()*2),
  stability:Array.from({length:24},()=>80+Math.random()*15),
  drills:  Array.from({length:24},()=>25+Math.random()*20),
};
const sbD=Array.from({length:14},()=>50+Math.random()*50);
const DR=4,DC=5;

// CANVAS REFS
const mainC=document.getElementById('main-chart'),mainCtx=mainC.getContext('2d');
const sbC=document.getElementById('stab-bar'),sbCtx=sbC.getContext('2d');
const mC={patients:document.getElementById('chart-patients'),tremor:document.getElementById('chart-tremor'),stability:document.getElementById('chart-stability'),drills:document.getElementById('chart-drills')};

function dprSize(c){
  const dpr=window.devicePixelRatio||1;
  const h=parseInt(c.getAttribute('height')||40);
  c.width=c.parentElement.clientWidth*dpr;
  c.height=h*dpr;
  c.style.width='100%';c.style.height=h+'px';
  c.getContext('2d').setTransform(dpr,0,0,dpr,0,0);
}
function initAll(){[mainC,sbC,...Object.values(mC)].forEach(dprSize);}
window.addEventListener('resize',initAll);
initAll();

// DOT MATRIX
const dmEl=document.getElementById('dot-matrix');
for(let c=0;c<DC;c++){const col=document.createElement('div');col.className='dot-col';for(let r=0;r<DR;r++){const d=document.createElement('div');d.className='dot-cell';d.id='d'+c+'x'+r;col.appendChild(d);}dmEl.appendChild(col);}

function hRgba(h,a){const r=parseInt(h.slice(1,3),16),g=parseInt(h.slice(3,5),16),b=parseInt(h.slice(5,7),16);return `rgba(${r},${g},${b},${a})`;}

function drawLine(ctx,data,w,h,color,fill,mn,mx){
  if(data.length<2)return;
  const pad=3,rng=mx-mn||1,step=(w-pad*2)/(data.length-1);
  const pts=data.map((v,i)=>({x:pad+i*step,y:pad+(1-(v-mn)/rng)*(h-pad*2)}));
  if(fill){
    ctx.beginPath();pts.forEach((p,i)=>i===0?ctx.moveTo(p.x,p.y):ctx.lineTo(p.x,p.y));
    ctx.lineTo(pts[pts.length-1].x,h);ctx.lineTo(pts[0].x,h);ctx.closePath();
    ctx.fillStyle=hRgba(color,0.12);ctx.fill();
  }
  ctx.beginPath();pts.forEach((p,i)=>i===0?ctx.moveTo(p.x,p.y):ctx.lineTo(p.x,p.y));
  ctx.strokeStyle=color;ctx.lineWidth=2;ctx.lineJoin='round';ctx.lineCap='round';ctx.stroke();
}

function drawMini(id,data,color){
  const c=mC[id];if(!c)return;
  const ctx=c.getContext('2d'),w=c.clientWidth,h=c.clientHeight;
  ctx.clearRect(0,0,w,h);
  drawLine(ctx,data,w,h,color,true,Math.min(...data)*.97,Math.max(...data)*1.03);
}

function drawMain(){
  const ctx=mainCtx,w=mainC.clientWidth,h=parseInt(mainC.getAttribute('height')||148);
  ctx.clearRect(0,0,w,h);
  for(let i=0;i<=4;i++){const y=(h/4)*i;ctx.strokeStyle='#e8eaf0';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(w,y);ctx.stroke();}
  const mn=0.5,mx=10.5;
  const sMin=35,sMax=105;
  const sMapped=sS.map(v=>mn+(v-sMin)/(sMax-sMin)*(mx-mn));
  drawLine(ctx,rS.map(v=>mn+v*(mx-mn)/1.5),w,h,'#f97316',true,mn,mx);
  drawLine(ctx,sMapped,w,h,'#a855f7',true,mn,mx);
  drawLine(ctx,tS,w,h,'#5b6ef5',true,mn,mx);
  // y labels
  ctx.fillStyle='#aab0be';ctx.font='9px Inter';ctx.textAlign='left';
  [[9,'9Hz'],[6,'6Hz'],[3,'3Hz']].forEach(([v,l])=>{ctx.fillText(l,2,3+(1-(v-mn)/(mx-mn))*(h-6));});
  // x labels
  ctx.textAlign='center';
  for(let i=0;i<SL;i+=15){const x=(i/(SL-1))*w;ctx.fillText('-'+(SL-1-i)+'s',x,h-1);}
  // legend
  const ld=[['#5b6ef5','Tremor Hz'],['#a855f7','Stability'],['#f97316','RMS Accel']];
  ld.forEach(([c,l],i)=>{
    const lx=w-160+i*52;
    ctx.fillStyle=c;ctx.beginPath();ctx.arc(lx,h-7,4,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='#6b7280';ctx.textAlign='left';ctx.fillText(l,lx+7,h-4);
  });
}

function drawStabBar(){
  const c=sbC,ctx=sbCtx,w=c.clientWidth,h=parseInt(c.getAttribute('height')||52);
  ctx.clearRect(0,0,w,h);
  const n=sbD.length,gap=2,bw=(w-gap*(n-1))/n;
  sbD.forEach((v,i)=>{
    const bh=(v/100)*(h-6),x=i*(bw+gap),y=h-6-bh;
    ctx.fillStyle=i===n-1?'#2dff99':'rgba(255,255,255,0.2)';
    ctx.beginPath();if(ctx.roundRect)ctx.roundRect(x,y,bw,bh,2);else ctx.rect(x,y,bw,bh);ctx.fill();
  });
}

function statusFor(t,s){
  if(t>6||s<65)return{label:'Critical',cls:'critical'};
  if(t>4.5||s<80)return{label:'Elevated',cls:'elevated'};
  return{label:'Stable',cls:'stable'};
}

function renderTable(){
  const q=(document.getElementById('patient-search').value||'').toLowerCase();
  const tb=document.getElementById('patient-tbody');tb.innerHTML='';
  ST.filter(p=>p.name.toLowerCase().includes(q)).forEach(p=>{
    const s=statusFor(p.tremor,p.stability);
    const tc=p.tremor>5?'var(--red)':p.tremor>3.5?'var(--orange)':'var(--green)';
    const sc=p.stability>80?'var(--green)':p.stability>65?'var(--orange)':'var(--red)';
    const tr=document.createElement('tr');
    tr.innerHTML=`
      <td><div class="pcell">
        <div class="pavatar" style="background:${p.color}">${p.init}</div>
        <div><div style="font-weight:600;">${p.name}</div><div style="font-size:11px;color:var(--muted)">Age ${p.age} &middot; ${p.side} hand</div></div>
      </div></td>
      <td style="color:var(--muted);font-size:12px;">${p.lastSession}</td>
      <td><span style="font-weight:600;color:${tc}">${p.tremor.toFixed(1)} Hz</span></td>
      <td><div style="display:flex;align-items:center;gap:8px;">
        <div style="flex:1;height:5px;background:#e4e7f0;border-radius:3px;overflow:hidden;">
          <div style="height:100%;width:${Math.round(p.stability)}%;background:${sc};border-radius:3px;"></div>
        </div>
        <span style="font-size:12px;font-weight:600;">${Math.round(p.stability)}%</span>
      </div></td>
      <td style="font-weight:600;">${p.drills}</td>
      <td><span class="spill ${s.cls}">${s.label}</span></td>
      <td><button class="abtn">View Session</button></td>
    `;
    tb.appendChild(tr);
  });
}
document.getElementById('patient-search').addEventListener('input',renderTable);

function updateDots(n){
  const total=DR*DC,lit=Math.min(total,Math.round((n/60)*total));
  for(let c=0;c<DC;c++)for(let r=0;r<DR;r++){const d=document.getElementById('d'+c+'x'+r);if(d)d.classList.toggle('lit',c*DR+r<lit);}
}

let tick=0;
function updateAll(){
  tick++;
  tS.shift();tS.push(parseFloat((3+Math.sin(tick*.18)*1.8+Math.random()*.7+(Math.random()>.95?2.2:0)).toFixed(2)));
  sS.shift();sS.push(parseFloat((85-Math.sin(tick*.13)*12+Math.random()*5).toFixed(2)));
  rS.shift();rS.push(parseFloat((0.1+Math.sin(tick*.15)*.08+Math.random()*.05).toFixed(3)));

  ST.forEach(p=>{
    p.tremor   =Math.max(1,Math.min(9.9,parseFloat((p.bT+Math.sin(tick*.11+p.id)*.9+(Math.random()-.5)*.6).toFixed(1))));
    p.stability=Math.max(30,Math.min(99,parseFloat((p.bS+Math.sin(tick*.09+p.id)*5+(Math.random()-.5)*3).toFixed(1))));
    if(tick%18===p.id%18){p.drills++;p.lastSession=rT();}
    p.spikes=Math.round(p.tremor*3+Math.random()*2);
  });

  const avgT=ST.reduce((s,p)=>s+p.tremor,0)/ST.length;
  const avgS=ST.reduce((s,p)=>s+p.stability,0)/ST.length;
  const totD=ST.reduce((s,p)=>s+p.drills,0);
  const totSp=ST.reduce((s,p)=>s+p.spikes,0);
  const avgR=rS.reduce((a,b)=>a+b,0)/rS.length;

  document.getElementById('stat-tremor').innerHTML=avgT.toFixed(1)+' <span style="font-size:13px;font-weight:500;color:var(--muted)">Hz</span>';
  document.getElementById('stat-stability').innerHTML=Math.round(avgS)+' <span style="font-size:13px;font-weight:500;color:var(--muted)">%</span>';
  document.getElementById('stat-drills').innerText=totD;

  document.getElementById('live-trem').innerText=avgT.toFixed(1);
  document.getElementById('live-stab').innerText=Math.round(avgS);
  document.getElementById('live-rms').innerText=avgR.toFixed(2);
  document.getElementById('live-spikes').innerText=totSp;

  document.getElementById('spike-count').innerText=totSp;
  document.getElementById('stability-big').innerText=Math.round(avgS);
  const dEl=document.getElementById('stability-delta');
  const diff=avgS-82;
  dEl.innerText=(diff>=0?'\u25b2 ':'\u25bc ')+Math.abs(diff).toFixed(1)+'%';
  dEl.style.color=diff>=0?'#22c55e':'#ef4444';

  mH.tremor.push(avgT);mH.tremor.shift();
  mH.stability.push(avgS);mH.stability.shift();
  mH.drills.push(totD);mH.drills.shift();
  sbD.shift();sbD.push(Math.round(avgS));

  updateDots(totSp);
  drawMain();
  drawMini('patients',mH.patients,'#5b6ef5');
  drawMini('tremor',mH.tremor,'#ef4444');
  drawMini('stability',mH.stability,'#22c55e');
  drawMini('drills',mH.drills,'#a855f7');
  drawStabBar();
  if(tick%2===0)renderTable();
}

renderTable();
updateAll();
setInterval(updateAll,1000);
</script>
</body>
</html>'''
pathlib.Path('/Users/ekans/motive ai/index.html').write_text(HTML)
print('DONE', pathlib.Path('/Users/ekans/motive ai/index.html').stat().st_size, 'bytes')
