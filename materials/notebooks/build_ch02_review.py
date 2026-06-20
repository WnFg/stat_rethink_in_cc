"""生成第 2 章复习要点 HTML（自包含：图片 base64 内嵌）。"""
import base64, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 项目根


def datauri(relpath):
    p = os.path.join(ROOT, relpath)
    if not os.path.exists(p):
        return ""
    b = base64.b64encode(open(p, "rb").read()).decode()
    return f"data:image/png;base64,{b}"


IMG_UPDATING = datauri("materials/figures/2.2_updating.png")
IMG_QUAP = datauri("materials/figures/2.4_quap.png")

HTML = r"""<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>第 2 章复习要点 · Small Worlds and Large Worlds</title>
<style>
  :root{
    --bg:#f6f7f9; --card:#ffffff; --ink:#1f2430; --muted:#5b6472;
    --blue:#2563eb; --blue-soft:#eaf1ff; --green:#16a34a; --green-soft:#e9f9ef;
    --amber:#d97706; --amber-soft:#fef3e2; --red:#dc2626; --red-soft:#fde8e8;
    --purple:#7c3aed; --purple-soft:#f1ebfe; --line:#e6e9ef;
  }
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;
    line-height:1.7;font-size:16px}
  .wrap{max-width:920px;margin:0 auto;padding:32px 22px 80px}
  header.top{background:linear-gradient(120deg,#2563eb,#7c3aed);color:#fff;border-radius:18px;
    padding:30px 32px;box-shadow:0 10px 30px rgba(37,99,235,.18)}
  header.top h1{margin:0 0 6px;font-size:27px;letter-spacing:.3px}
  header.top .sub{opacity:.92;font-size:15px}
  header.top .meta{margin-top:14px;font-size:13px;opacity:.85}
  h2{font-size:21px;margin:38px 0 14px;padding-left:12px;border-left:5px solid var(--blue)}
  h3{font-size:17px;margin:20px 0 8px}
  .card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:20px 22px;margin:14px 0;
    box-shadow:0 2px 10px rgba(20,30,50,.04)}
  .muted{color:var(--muted)}
  code,.mono{font-family:"SF Mono",ui-monospace,Menlo,Consolas,monospace;font-size:13.5px}
  code{background:#f1f3f7;padding:1.5px 6px;border-radius:6px}
  pre{background:#0f1320;color:#e6e9f2;border-radius:10px;padding:14px 16px;overflow:auto;font-size:13px;line-height:1.55}
  pre .c{color:#7d8aa5}
  .flow{display:flex;flex-wrap:wrap;align-items:stretch;gap:10px;margin:6px 0}
  .flow .box{flex:1;min-width:150px;background:var(--blue-soft);border:1px solid #cfe0ff;border-radius:12px;
    padding:14px;text-align:center}
  .flow .box b{display:block;color:var(--blue);font-size:15px;margin-bottom:4px}
  .flow .box span{font-size:12.5px;color:var(--muted)}
  .flow .arrow{display:flex;align-items:center;color:var(--blue);font-size:24px;font-weight:700}
  table{width:100%;border-collapse:collapse;margin:8px 0;font-size:14.5px}
  th,td{border:1px solid var(--line);padding:9px 11px;text-align:left;vertical-align:top}
  th{background:#f0f3f8;font-weight:600}
  .grid2{display:grid;grid-template-columns:1fr 1fr;gap:12px}
  @media(max-width:680px){.grid2{grid-template-columns:1fr}}
  .vocab{background:var(--blue-soft);border:1px solid #cfe0ff;border-radius:12px;padding:13px 15px}
  .vocab b{color:var(--blue)}
  .formula{background:#fbfcff;border:1px dashed #c9d6ef;border-radius:10px;padding:12px 16px;margin:10px 0;
    font-size:16px;text-align:center}
  .formula .big{font-size:18px}
  .tag{display:inline-block;font-size:12px;font-weight:600;padding:2px 9px;border-radius:999px;margin-right:6px}
  .t-blue{background:var(--blue-soft);color:var(--blue)}
  .t-green{background:var(--green-soft);color:var(--green)}
  .t-amber{background:var(--amber-soft);color:var(--amber)}
  .t-purple{background:var(--purple-soft);color:var(--purple)}
  .pill{border-radius:14px;padding:16px 18px;margin:12px 0;border:1px solid}
  .pill.good{background:var(--green-soft);border-color:#bce9cd}
  .pill.warn{background:var(--amber-soft);border-color:#f6d9a8}
  .pill.err{background:var(--red-soft);border-color:#f6c4c4}
  .pill.idea{background:var(--purple-soft);border-color:#dcccfb}
  .pill h3{margin:0 0 8px}
  .wrong{color:var(--red);font-weight:600}
  .right{color:var(--green);font-weight:600}
  figure{margin:10px 0}
  figure img{width:100%;border:1px solid var(--line);border-radius:12px;background:#fff}
  figcaption{font-size:13px;color:var(--muted);margin-top:6px;text-align:center}
  ul{margin:8px 0 8px 2px;padding-left:20px}
  li{margin:5px 0}
  .kbd{font-family:monospace;background:#eef1f6;border:1px solid #d7dce5;border-bottom-width:2px;border-radius:6px;padding:1px 7px;font-size:13px}
  .small{font-size:13.5px}
</style>
</head>
<body>
<div class="wrap">

<header class="top">
  <h1>第 2 章 复习要点 · Small Worlds and Large Worlds</h1>
  <div class="sub">贝叶斯推断的地基：数路径 → 后验 → 三种引擎</div>
  <div class="meta">Statistical Rethinking (1st ed) · Ch.2 (p32–61) &nbsp;|&nbsp; 个性化复习卡 · 2026-06-20</div>
</header>

<h2>① 一张图看懂整章</h2>
<div class="card">
  <div class="flow">
    <div class="box"><b>数路径</b><span>§2.1 · 数"有多少种方式产生数据"，标准化成概率</span></div>
    <div class="arrow">→</div>
    <div class="box"><b>后验公式</b><span>§2.3 · 后验 =(似然×先验)/平均似然</span></div>
    <div class="arrow">→</div>
    <div class="box"><b>三种引擎</b><span>§2.4 · grid / quadratic / MCMC 把后验算出来</span></div>
  </div>
  <p class="muted small" style="margin:10px 0 0">一句话主轴：<b>贝叶斯推断 = 在所有可能的参数里，按"它们产生观测数据的相对方式数"重新分配可信度。</b>没有玄学，全是数数（p33）。</p>
</div>

<h2>② 四个核心词汇（§2.1, p40）</h2>
<div class="card">
  <div class="grid2">
    <div class="vocab"><b>parameter 参数</b> — 要推断的未知量。globe tossing 里就是水的比例 <code>p</code>；代码里是 <code>grid</code> 上每个候选值。</div>
    <div class="vocab"><b>likelihood 似然</b> — 给定某个 p，产生观测数据的相对可能性。<code>binom.pmf(W,N,p)</code>。</div>
    <div class="vocab"><b>prior 先验</b> — 看数据<i>前</i>对 p 的初始权重。本章多用均匀先验 <code>np.ones_like(grid)</code>。</div>
    <div class="vocab"><b>posterior 后验</b> — 看完数据<i>后</i>的权重，<code>Pr(p|W)</code>。这才是贝叶斯的最终产物（一整条分布）。</div>
  </div>
</div>

<h2>③ 核心公式：Bayes 定理（§2.3, p49–50）</h2>
<div class="card">
  <div class="formula"><span class="big">后验 = (似然 × 先验) / 平均似然</span><br>
    <span class="mono">Pr(p|W) = Pr(W|p)·Pr(p) / Pr(W)</span></div>
  <ul>
    <li><b>分母"平均似然" Pr(W)</b> 只是<b>归一化常数</b>——作用就是让后验加起来等于 1。</li>
    <li>它的定义：<code>Pr(W) = ∫ Pr(W|p)·Pr(p) dp</code>（连续）= <code>(likelihood × prior).sum()</code>（网格）。</li>
    <li class="small muted">💡 你早就在算它了：之前写的 <code>post / post.sum()</code> 里那个 <code>.sum()</code> 就是平均似然 Pr(W)。</li>
  </ul>
</div>

<h2>④ 贝叶斯更新：后验如何随数据变化（§2.2, p43）</h2>
<div class="card">
  <p>从均匀先验出发，每喂入一个观测就更新一次：<b>见 W 峰右移、见 L 峰左移；数据越多曲线越高越窄（越确定）</b>。而且更新<b>与数据顺序无关</b>——6W3L 不管什么顺序，终点后验相同。</p>
  __FIG_UPDATING__
  <p class="small muted">关键代码：<code>post = post * binom.pmf(w,1,grid); post /= post.sum()</code> —— 当前后验 × 这次观测的似然，再归一化。</p>
</div>

<h2>⑤ 三种引擎（§2.4, p52）</h2>
<div class="card">
  <table>
    <tr><th>引擎</th><th>怎么做</th><th>特点</th></tr>
    <tr><td><b>① Grid 网格近似</b></td><td>把 p 切成网格，逐点算 <code>先验×似然</code> 归一化</td><td>直观、教学用；<span class="wrong">随参数增多急剧变慢</span>（10 参数→几十亿点）</td></tr>
    <tr><td><b>② Quadratic 二次近似</b></td><td>用一个高斯逼近后验峰附近（MAP + SD）</td><td>便宜、后半本书主力；小样本/偏态会失真</td></tr>
    <tr><td><b>③ MCMC</b></td><td>不直接算，而是<b>从后验抽样</b></td><td>复杂/多层模型的主力（第 8 章细讲）</td></tr>
  </table>
</div>

<h2>⑥ 二次近似 深入（你重点追问的部分）</h2>
<div class="card">
  <h3>理论链（务必记住"哪一步是近似"）</h3>
  <div class="formula mono">对数后验 &nbsp;—(二阶泰勒，<span class="wrong">近似</span>)→&nbsp; 抛物线 &nbsp;—(exp，<span class="right">精确</span>)→&nbsp; 高斯</div>
  <ul>
    <li><b>核心假设</b>：后验在峰附近 ≈ 高斯（§2.4.2, p54）。</li>
    <li>等价说法：<b>对数后验在峰附近 ≈ 一条抛物线</b>（因为"任何高斯的对数 = 抛物线"，这是<span class="right">精确</span>事实）。</li>
    <li>方法：对<b>对数后验</b>在峰处做二阶泰勒展开，一阶项为 0（峰），剩下常数 + 二次项 = 抛物线。</li>
  </ul>
  <h3>两个产出 + 那条让你卡住的关系</h3>
  <div class="formula">中心 <b>μ = MAP</b>（峰）&nbsp;&nbsp;|&nbsp;&nbsp; 宽度 <b>σ² = 1 / |f″(p̂)|</b> &nbsp;→&nbsp; <b>SD = 1/√(曲率)</b></div>
  <p class="small"><b>σ² = 1/|f″| 从哪来？</b> 把"近似后验"和"高斯密度"并排，两者都是 <code>exp(−½ · 系数 · (p−中心)²)</code>。比较 (p−中心)² 前的系数：近似后验是 <code>|f″|</code>，高斯是 <code>1/σ²</code> → 相等取倒数即得。<b>直觉</b>：峰越尖（曲率 |f″| 越大）→ σ² 越小 → 越确定。曲率 = 精度 = 1/方差。</p>
  __FIG_QUAP__
  <p class="small muted">上图（复现书 Fig 2.8）：n=9 后验偏态、高斯近似偏差明显（甚至给 p≈1 不可能区正概率）；n=36 几乎重合。<b>大样本下 quap 才可靠</b>（Bernstein–von Mises）。</p>
</div>

<h2>⑦ MLE 与 MAP（频率派 ↔ 贝叶斯的桥）</h2>
<div class="card">
  <table>
    <tr><th></th><th>定义</th><th>关系</th></tr>
    <tr><td><b>MLE</b></td><td><code>argmax 似然</code> = 似然曲线的峰 = 观测频率 W/N</td><td rowspan="2" class="small">
      <b>均匀先验时 MAP = MLE</b>（先验是常数不动峰）；<br>先验有倾向时 MAP 被拉偏（demo：偏 0.5 的先验把 MAP 从 0.667 拉到 0.53）；<br>数据越多 MAP → MLE。<br><br>⚠️ 两者都只是"<b>一个点</b>"，都丢掉了整条分布——贝叶斯真正的答案是<b>整条后验</b>。</td></tr>
    <tr><td><b>MAP</b></td><td><code>argmax (似然×先验)</code> = 后验的峰</td></tr>
  </table>
</div>

<h2>⑧ ★ 你的学习画像（个性化）</h2>

<div class="pill idea">
  <h3>🌟 你的高光与兴趣点</h3>
  <ul>
    <li><b>喜欢刨根问底的理论</b>：主动追问"二次近似的数学基础"，一路问到 σ²=1/|f″| 的来历——这种深度很难得。</li>
    <li><b>强直觉</b>：自己发现<code>binom.pmf(w,1,grid)</code> 喂单个观测时其实就是 <code>p</code> 或 <code>1−p</code>，binom 是多余的——一眼看穿了"伯努利似然"的本质。</li>
    <li><b>会自己推导</b>：把数值二阶导自推成"(前向一阶导 − 后向一阶导)/eps"，等价于标准三点公式——是理解而非套公式。</li>
    <li><b>关注 API 机制</b>：主动问 <code>binom.pmf</code>/<code>minimize</code>/<code>np.clip</code> 到底在做什么——建议继续保持，下一章会用到更多。</li>
  </ul>
</div>

<div class="pill warn">
  <h3>⚠️ 你的易错点（已澄清，建议反复看）</h3>
  <table>
    <tr><th>易错</th><th><span class="wrong">❌ 当时</span></th><th><span class="right">✅ 正确</span></th></tr>
    <tr><td>归一化分母</td><td>分母 = Σ(似然 × <span class="wrong">p</span>)</td><td>Σ(似然 × <span class="right">prior(p) 先验权重</span>)，乘的是先验不是参数值</td></tr>
    <tr><td>二次近似"谁近似谁"</td><td>把<span class="wrong">后验</span>用抛物线近似，再<span class="wrong">取对数</span>得高斯</td><td>把<span class="right">对数后验</span>用抛物线近似，再<span class="right">exp</span>得高斯；高斯↔抛物线是精确</td></tr>
    <tr><td>数值导数括号</td><td><code>f(x+h) - f(x) <span class="wrong">/ h</span></code></td><td><code><span class="right">(</span>f(x+h) - f(x)<span class="right">)</span> / h</code>（<code>/</code> 优先级高于 <code>−</code>）</td></tr>
  </table>
</div>

<div class="pill warn">
  <h3>🎯 待强化：可信区间 ≠ 置信区间（请练到脱口而出）</h3>
  <div class="grid2">
    <div><span class="tag t-blue">贝叶斯 · 可信区间</span><br>"给定数据，p 落在 [a,b] 的<b>概率是 95%</b>。" 概率属于<b>参数</b>。可直接说 <code>P(a≤p≤b | 数据)=0.95</code>。</div>
    <div><span class="tag t-amber">频率派 · 置信区间</span><br>参数是<b>固定</b>值；95% 说的是<b>程序</b>——重复实验很多次，95% 的此类区间会盖住真值。<b>不能</b>对单个区间说"有 95% 概率含真值"。</div>
  </div>
</div>

<div class="pill good">
  <h3>✅ 你已攻克（4 节 OJ 全部通过 + 复习 fix-this 全对）</h3>
  <p class="small" style="margin:0">数路径计数 · <code>bayes_update</code> · <code>posterior_bayes</code>(显式分母) · <code>quap_globe</code>(MAP+SD自推曲率) · A/B 业务建模(MAP=0.65, 95%区间[0.43,0.82])，并能用贝叶斯语气向 PM 解读。</p>
</div>

<h2>⑨ 速查卡（随手抄）</h2>
<div class="card">
<pre><span class="c"># 网格近似：算后验（均匀先验）</span>
grid = np.linspace(0, 1, 1000)
like = binom.pmf(W, N, grid)        <span class="c"># 似然（grid=一排候选 p）</span>
post = like / like.sum()            <span class="c"># .sum() 就是平均似然 Pr(W)=分母</span>
map_p = grid[np.argmax(post)]       <span class="c"># MAP（均匀先验下 = MLE = W/N）</span>

<span class="c"># 95% 可信区间（百分位）</span>
cum = np.cumsum(post)
lo = grid[np.searchsorted(cum, 0.025)]
hi = grid[np.searchsorted(cum, 0.975)]

<span class="c"># 二次近似：找峰 + 量曲率</span>
neg = lambda p: -binom.logpmf(W, N, np.clip(p, 1e-9, 1-1e-9))  <span class="c"># 负对数后验</span>
m   = minimize(neg, 0.5, method="L-BFGS-B", bounds=[(1e-6,1-1e-6)]).x[0]
second = (neg(m+eps) - 2*neg(m) + neg(m-eps)) / eps**2          <span class="c"># 曲率|f″|</span>
sd  = 1/np.sqrt(second)             <span class="c"># σ = 1/√曲率</span></pre>
  <p class="small muted" style="margin:8px 0 0">配套图与脚本：<code>materials/figures/</code>（贝叶斯更新、quap vs 真实后验）、<code>materials/notebooks/viz_2.2_updating.py</code>、<code>viz_2.4_quap.py</code>，可改参数重跑。</p>
</div>

<h2>⑩ 下一步</h2>
<div class="card">
  <p><b>第 3 章 Sampling the Imaginary</b>：不再死磕公式，而是<b>从后验里采样</b>来做推断——算区间、做后验预测、检查模型。会直接用上你这章写的后验。命令：<span class="kbd">/chapter 3</span>。</p>
  <p class="small muted" style="margin:6px 0 0">挂账 homework（可在开新章前收掉）：avg_like 均匀 vs step 先验 · <code>bayes_update_seq</code> 验证逐步≡一次性 · quap 95% 区间 vs 真实区间。</p>
</div>

<p class="muted small" style="text-align:center;margin-top:30px">— 第 2 章复习卡 · 随时回看，把"易错点"和"待强化"读到形成肌肉记忆 —</p>

</div>
</body>
</html>
"""

upd = f'<figure><img src="{IMG_UPDATING}" alt="贝叶斯更新"><figcaption>逐次贝叶斯更新：每喂一个观测后验如何变化（复现书 Fig 2.5）</figcaption></figure>' if IMG_UPDATING else '<p class="muted small">[图缺失：运行 viz_2.2_updating.py 生成]</p>'
qua = f'<figure><img src="{IMG_QUAP}" alt="quap vs 真实后验"><figcaption>二次近似(黑虚线) vs 真实后验(蓝实线)：n=9 偏差明显，n=36 几乎重合</figcaption></figure>' if IMG_QUAP else '<p class="muted small">[图缺失：运行 viz_2.4_quap.py 生成]</p>'

HTML = HTML.replace("__FIG_UPDATING__", upd).replace("__FIG_QUAP__", qua)

out = os.path.join(ROOT, "progress/reviews/ch02_review_notes.html")
open(out, "w", encoding="utf-8").write(HTML)
print("written:", out, f"({len(HTML)//1024} KB)")
