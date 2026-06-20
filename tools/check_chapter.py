#!/usr/bin/env python3
"""教案质量检查器（L1 结构/引用 lint + L2 代码执行闸门）。

依据 curriculum/QUALITY.md 的 rubric 检查 curriculum/chapters/chNN.md。
L1：每个 `## N.M` 小节字段齐全；非讨论节有代码块；引用页码落在本章页区间；
    每道"练习"配折叠解法或被标记讨论题。
L2：抽出全部 ```python 代码块（含 <details> 内解法），逐块独立子进程运行；
    任何报错 / AssertionError 即失败。

用法：
    python3 tools/check_chapter.py curriculum/chapters/ch02.md --pages 32 61
    python3 tools/check_chapter.py curriculum/chapters/ch02.md          # 跳过页码范围检查

退出码：0 全过；1 有失败项。
"""
import sys
import re
import os
import subprocess
import tempfile
import textwrap

REQUIRED_FIELDS = ["学习目标", "核心概念", "关键直觉", "设计练习", "常见误区"]
WORKED = "Worked example"
# 章级收尾小节（非教学小节），跳过 rubric 字段检查
SKIP_TITLE = ("summary", "practice", "小结", "习题")


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def split_sections(text):
    """按 `## N.M ...` 切分小节，返回 [(title, body), ...]。"""
    parts = re.split(r"(?m)^##\s+(\d+\.\d+\b.*)$", text)
    secs = []
    # parts[0] 是首个小节前的前言，丢弃
    for i in range(1, len(parts), 2):
        secs.append((parts[i].strip(), parts[i + 1]))
    return secs


def code_blocks(text):
    """提取所有 ```python ... ``` 块内容（含 <details> 内），去掉 markdown 列表缩进。"""
    raw = re.findall(r"```python\s*\n(.*?)```", text, re.DOTALL)
    return [textwrap.dedent(b) for b in raw]


def is_discussion(title, body):
    """纯讨论/概念小节：标题或正文显式标注（无需代码）。"""
    return ("讨论" in title) or ("（讨论" in body) or ("[discussion]" in body.lower())


def lint(text, page_range):
    """L1：返回问题列表。"""
    problems = []
    secs = split_sections(text)
    if not secs:
        problems.append("L1: 找不到任何 `## N.M` 小节标题")
    for title, body in secs:
        tag = title.split()[0]
        if any(k in title.lower() for k in SKIP_TITLE):
            continue  # 章级收尾小节（Summary/Practice），非教学小节
        disc = is_discussion(title, body)
        for fld in REQUIRED_FIELDS:
            if disc and fld in ("设计练习", "常见误区"):
                continue
            if fld not in body:
                problems.append(f"L1[{tag}]: 缺字段「{fld}」")
        if not disc:
            if WORKED not in body:
                problems.append(f"L1[{tag}]: 缺「Worked example」")
            if not code_blocks(body):
                problems.append(f"L1[{tag}]: 非讨论小节却没有 python 代码块（A5）")
        # 练习须配折叠解法（B2）：出现"设计练习"且有计算练习时，应有 <details>
        if "设计练习" in body and not disc:
            if "<details>" not in body:
                problems.append(f"L1[{tag}]: 设计练习缺折叠解法块 <details>（B2）；纯讨论题请在题面标注")
    # 引用页码范围（A2）
    if page_range:
        lo, hi = page_range
        for m in re.finditer(r"[pP](\d{1,3})", text):
            pg = int(m.group(1))
            if pg < lo or pg > hi:
                problems.append(f"L1: 引用页码 p{pg} 超出本章范围 {lo}–{hi}")
                break  # 只报一次，避免刷屏
    return problems


def run_blocks(text):
    """L2：逐块独立运行，返回失败列表 [(idx, head, err), ...]。"""
    failures = []
    blocks = code_blocks(text)
    for i, code in enumerate(blocks, 1):
        head = next((ln for ln in code.splitlines() if ln.strip()), "")[:60]
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as tf:
            tf.write(code)
            tmp = tf.name
        try:
            r = subprocess.run([sys.executable, tmp], capture_output=True, text=True, timeout=120)
            if r.returncode != 0:
                err = (r.stderr.strip().splitlines() or ["<no stderr>"])[-1]
                failures.append((i, head, err))
        except subprocess.TimeoutExpired:
            failures.append((i, head, "超时(>120s)"))
        finally:
            os.unlink(tmp)
    return failures, len(blocks)


def main(argv):
    if not argv:
        sys.exit(__doc__)
    path = argv[0]
    page_range = None
    if "--pages" in argv:
        k = argv.index("--pages")
        page_range = (int(argv[k + 1]), int(argv[k + 2]))
    if not os.path.exists(path):
        sys.exit(f"找不到文件：{path}")
    text = read(path)

    print(f"# 检查 {path}")
    l1 = lint(text, page_range)
    fails, n = run_blocks(text)

    print(f"\n## L1 结构/引用 lint：{'PASS ✅' if not l1 else f'FAIL ❌（{len(l1)} 项）'}")
    for p in l1:
        print("  -", p)

    print(f"\n## L2 代码执行（{n} 个代码块）：{'PASS ✅' if not fails else f'FAIL ❌（{len(fails)}/{n} 块失败）'}")
    for i, head, err in fails:
        print(f"  - 第 {i} 块 `{head}` → {err}")

    ok = not l1 and not fails
    print(f"\n=== 总判定：{'PASS ✅（L1+L2 全绿，可进入 L3 独立审阅）' if ok else 'FAIL ❌（修复后重跑）'} ===")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main(sys.argv[1:])
