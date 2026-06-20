#!/usr/bin/env python3
"""OJ 判题器：用隐藏测试集判定学生对某道练习的实现。

老师为练习定义函数签名（输入/输出规范）+ 一份隐藏测试集（asserts）；
学生只写实现；本工具把"学生实现 + 隐藏测试"拼到一个命名空间里运行并判定。

用法：
    python3 tools/judge.py <学生实现.py> <隐藏测试.py>

约定：
    - 学生文件定义题目要求的函数（如 bayes_update）。
    - 测试文件是若干 assert，直接引用该函数名；可自带 import。
    - 测试全过 → PASS（退出码 0）；任一 assert/报错 → FAIL（退出码 1），并指出失败处。

设计：两文件按 学生→测试 顺序拼接，在独立子进程运行，互不污染当前环境。
"""
import sys
import os
import subprocess
import tempfile


def main(argv):
    if len(argv) < 2:
        sys.exit("用法：python3 tools/judge.py <学生实现.py> <隐藏测试.py>")
    student, tests = argv[0], argv[1]
    for f in (student, tests):
        if not os.path.exists(f):
            sys.exit(f"找不到文件：{f}")
    with open(student, encoding="utf-8") as f:
        scode = f.read()
    with open(tests, encoding="utf-8") as f:
        tcode = f.read()

    harness = (
        scode
        + "\n\n# ===== 隐藏测试 =====\n"
        + tcode
        + "\nprint('JUDGE_OK')\n"
    )
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as tf:
        tf.write(harness)
        tmp = tf.name
    try:
        r = subprocess.run([sys.executable, tmp], capture_output=True, text=True, timeout=120)
    finally:
        os.unlink(tmp)

    out = r.stdout.replace("JUDGE_OK", "").strip()
    if out:
        print(out)
    if r.returncode == 0 and "JUDGE_OK" in r.stdout:
        print("\n=== 判定：PASS ✅ 全部隐藏测试通过 ===")
        sys.exit(0)
    else:
        err = (r.stderr.strip().splitlines() or ["<no stderr>"])
        # 提取最后的报错行（assert 失败/异常）
        tail = "\n".join(err[-6:])
        print("\n--- 报错 ---\n" + tail)
        print("\n=== 判定：FAIL ❌ 修正实现后重交 ===")
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
