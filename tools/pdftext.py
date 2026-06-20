#!/usr/bin/env python3
"""按 PDF 页码区间抽取纯文本（统一入口，供各 skill 读取教材）。

用法：
    python3 tools/pdftext.py <start_page> <end_page> [pdf_path]

约定：
    - 页码为 0 基（与 pypdf 书签 / get_destination_page_number 一致），含端点。
    - 不依赖 poppler，仅用 pypdf。
    - 不带参数时打印整本书的章节书签（TOC）+ 0 基页码，方便定位。

示例：
    python3 tools/pdftext.py 32 41          # 第 2 章前几页正文
    python3 tools/pdftext.py --toc          # 打印目录与页码
"""
import sys
import os

DEFAULT_PDF = os.path.join(os.path.dirname(__file__), "..", "RM-StatRethink-Bayes.pdf")


def load_reader(pdf_path):
    try:
        import pypdf
    except ImportError:
        sys.exit("缺少 pypdf，请先 `pip install pypdf`")
    return pypdf.PdfReader(pdf_path)


def print_toc(pdf_path):
    reader = load_reader(pdf_path)
    print(f"# {os.path.basename(pdf_path)}  共 {len(reader.pages)} 页（0 基）\n")

    def walk(items, depth=0):
        for it in items:
            if isinstance(it, list):
                walk(it, depth + 1)
            else:
                try:
                    pg = reader.get_destination_page_number(it)
                except Exception:
                    pg = "?"
                print("  " * depth + f"p{pg}: {it.title}")

    try:
        walk(reader.outline)
    except Exception as e:
        print(f"无法读取书签：{e}")


def extract(start, end, pdf_path):
    reader = load_reader(pdf_path)
    n = len(reader.pages)
    start = max(0, start)
    end = min(end, n - 1)
    for i in range(start, end + 1):
        text = reader.pages[i].extract_text() or ""
        print(f"\n===== [PDF page {i}] =====")
        print(text.strip())


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return
    if argv[0] == "--toc":
        pdf = argv[1] if len(argv) > 1 else DEFAULT_PDF
        print_toc(pdf)
        return
    try:
        start = int(argv[0])
        end = int(argv[1])
    except (IndexError, ValueError):
        sys.exit("用法：python3 tools/pdftext.py <start_page> <end_page> [pdf_path]\n     或 python3 tools/pdftext.py --toc")
    pdf = argv[2] if len(argv) > 2 else DEFAULT_PDF
    if not os.path.exists(pdf):
        sys.exit(f"找不到 PDF：{pdf}")
    extract(start, end, pdf)


if __name__ == "__main__":
    main(sys.argv[1:])
