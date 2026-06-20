#!/usr/bin/env python3
"""复习卡通用渲染器 —— 只管样式与组装，内容由 /review 撰写。

把 /review 写好的 HTML 片段（body）套上统一的 <head>/CSS/页眉页脚，
并将其中引用的 materials/figures/*.png（及 --figures 指定的图）全部 base64 内嵌，
产出一个**自包含、可分享、离线可看**的复习卡 HTML。

用法：
    python3 tools/render_card.py --title "第3章复习要点 · Sampling the Imaginary" \
        --body progress/reviews/ch03_card_body.html \
        --out  progress/reviews/ch03_review_notes.html \
        --subtitle "从后验采样做推断" --meta "Ch.3 (p62-83) · 2026-06-21" \
        --figures materials/figures/3.1_samples.png \
        --open

body 片段可用的 CSS 类（撰写时对照）：
  .card                       内容卡片（白底）
  h2 / h3                     小节/子标题
  .flow > .box / .arrow       主轴流程图（横向方框+箭头，非点阵）
  .grid2                      两列网格
  .vocab                      术语卡（蓝）
  .formula  /  .formula .big  公式框（居中、虚线边）
  table / th / td             表格
  .pill.good|.warn|.err|.idea 醒目色块（绿/琥珀/红/紫）—— 学习画像段常用
  .tag.t-blue|t-green|t-amber|t-purple   小圆标签
  .wrong (红粗) / .right (绿粗)          易错点红绿对照
  pre / pre .c                代码块 / 代码注释
  figure > img + figcaption   图（用 <img src="materials/figures/xx.png"> 引用，会自动内嵌）
  .muted / .small / .kbd      次要文字 / 小字 / 键帽
"""
import argparse
import base64
import os
import re
import subprocess
import sys

CSS = r"""
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
"""

PAGE = """<!DOCTYPE html>
<html lang="zh"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>__CSS__</style></head>
<body><div class="wrap">
<header class="top">
  <h1>__TITLE__</h1>
  <div class="sub">__SUBTITLE__</div>
  <div class="meta">__META__</div>
</header>
__BODY__
<p class="muted small" style="text-align:center;margin-top:30px">__FOOTER__</p>
</div></body></html>
"""

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def datauri(path):
    """读图片 -> base64 data URI；找不到返回 None。"""
    full = path if os.path.isabs(path) else os.path.join(ROOT, path)
    if not os.path.exists(full):
        return None
    b = base64.b64encode(open(full, "rb").read()).decode()
    return "data:image/png;base64," + b


def inline_images(html, extra_figures):
    """把 <img src="materials/figures/x.png"> 与 --figures 指定的图 base64 内嵌。
    返回 (html, missing[])。"""
    missing = []

    def repl(m):
        src = m.group(2)
        if src.startswith("data:"):
            return m.group(0)
        uri = datauri(src)
        if uri is None:
            missing.append(src)
            return m.group(0)
        return m.group(1) + uri + m.group(3)

    # 替换 src="..."（单/双引号）
    html = re.sub(r'(<img[^>]*\bsrc=")([^"]+)(")', repl, html)
    # 校验 --figures（仅检查存在性，便于报告）
    for f in extra_figures:
        if datauri(f) is None:
            missing.append(f)
    return html, missing


def main(argv):
    ap = argparse.ArgumentParser(description="复习卡渲染器")
    ap.add_argument("--title", required=True)
    ap.add_argument("--body", required=True, help="HTML 片段文件（/review 撰写）")
    ap.add_argument("--out", required=True)
    ap.add_argument("--subtitle", default="")
    ap.add_argument("--meta", default="")
    ap.add_argument("--footer", default="— 复习卡 · 随时回看，把易错点与待强化读到形成肌肉记忆 —")
    ap.add_argument("--figures", default="", help="逗号分隔的额外图片路径（也会内嵌）")
    ap.add_argument("--open", action="store_true", help="渲染后用 Safari 打开")
    a = ap.parse_args(argv)

    body_path = a.body if os.path.isabs(a.body) else os.path.join(ROOT, a.body)
    if not os.path.exists(body_path):
        sys.exit(f"找不到 body 文件：{a.body}")
    body = open(body_path, encoding="utf-8").read()

    extra = [x.strip() for x in a.figures.split(",") if x.strip()]
    body, missing = inline_images(body, extra)

    html = (PAGE
            .replace("__CSS__", CSS)
            .replace("__BODY__", body)
            .replace("__TITLE__", a.title)
            .replace("__SUBTITLE__", a.subtitle)
            .replace("__META__", a.meta)
            .replace("__FOOTER__", a.footer))

    out_path = a.out if os.path.isabs(a.out) else os.path.join(ROOT, a.out)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    open(out_path, "w", encoding="utf-8").write(html)
    print(f"written: {out_path}  ({len(html)//1024} KB)")
    if missing:
        print("⚠️ 这些图未找到、未内嵌：", ", ".join(sorted(set(missing))))
    if a.open:
        subprocess.run(["open", "-a", "Safari", out_path])
        print("已在 Safari 打开")


if __name__ == "__main__":
    main(sys.argv[1:])
