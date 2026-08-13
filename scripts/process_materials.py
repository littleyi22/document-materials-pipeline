"""Merge ordered PDF materials, rotate selected source groups, add a TOC and page numbers."""
import argparse
import json
import os
from io import BytesIO

from pypdf import PdfReader, PdfWriter
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def register_cjk_font():
    for path in (r"C:\Windows\Fonts\msjh.ttc", r"C:\Windows\Fonts\NotoSansTC-VF.ttf", r"/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"):
        if os.path.exists(path):
            pdfmetrics.registerFont(TTFont("MaterialsCJK", path))
            return "MaterialsCJK"
    return "Helvetica"


def make_toc(title, entries, toc_counts, font_name):
    stream = BytesIO()
    c = canvas.Canvas(stream, pagesize=A4)
    width, height = A4
    c.setTitle(title + " - TOC and page numbers")
    c.setFont(font_name, 24)
    c.drawCentredString(width / 2, height - 86, title)
    c.setFont(font_name, 18)
    c.drawCentredString(width / 2, height - 122, "目錄")
    c.setStrokeColor(colors.HexColor("#52708a"))
    c.line(72, height - 142, width - 72, height - 142)
    c.setFont(font_name, 14)
    for i, (name, page_start) in enumerate(entries):
        y = height - 178 - i * 26
        c.drawString(92, y, name)
        c.setDash(1, 3)
        c.line(190, y + 4, width - 132, y + 4)
        c.setDash()
        shown = page_start + 1 if toc_counts else page_start
        c.drawRightString(width - 92, y, f"第 {shown} 頁")
    c.setFont(font_name, 10)
    c.setFillColor(colors.HexColor("#666666"))
    c.drawCentredString(width / 2, 42, "目錄頁計入頁碼" if toc_counts else "本目錄頁不計入正文頁碼")
    c.save()
    stream.seek(0)
    return PdfReader(stream).pages[0]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", help="UTF-8 JSON configuration file")
    args = parser.parse_args()
    with open(args.config, "r", encoding="utf-8-sig") as handle:
        config = json.load(handle)

    font_name = register_cjk_font()
    flat_pages = []
    boundaries = []
    current = 1
    for unit in config["units"]:
        boundaries.append((unit["name"], current))
        rotate_indices = set(unit.get("rotate_indices", []))
        for index, source in enumerate(unit["sources"]):
            reader = PdfReader(source)
            for page in reader.pages:
                if index in rotate_indices:
                    page.rotate(270)
                flat_pages.append(page)
                current += 1

    writer = PdfWriter()
    include_toc = config.get("include_toc", True)
    toc_counts = bool(config.get("toc_counts", False))
    if include_toc:
        writer.add_page(make_toc(config["title"], boundaries, toc_counts, font_name))

    font_size = float(config.get("page_number_font_size", 14))
    for number, page in enumerate(flat_pages, start=1):
        if int(page.get("/Rotate", 0) or 0) % 360 in (90, 270):
            page.transfer_rotation_to_content()
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
        stream = BytesIO()
        overlay = canvas.Canvas(stream, pagesize=(width, height))
        overlay.setFillColor(colors.black)
        overlay.setFont("Helvetica", font_size)
        overlay.drawRightString(width - 24, 24, str(number))
        overlay.save()
        stream.seek(0)
        page.merge_page(PdfReader(stream).pages[0])
        writer.add_page(page)

    writer.add_metadata({"Title": config["title"], "Subject": "Cleaned and paginated teaching materials"})
    output = config["output"]
    os.makedirs(os.path.dirname(os.path.abspath(output)), exist_ok=True)
    with open(output, "wb") as handle:
        writer.write(handle)
    print(f"SOURCES={sum(len(u['sources']) for u in config['units'])}")
    print(f"CONTENT_PAGES={len(flat_pages)}")
    print(f"FINAL_PAGES={len(writer.pages)}")


if __name__ == "__main__":
    main()
