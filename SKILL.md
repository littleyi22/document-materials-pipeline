---
name: document-materials-pipeline
description: Clean, paginate, merge, and prepare ordered student and teacher editions from Word and PDF teaching materials. Use when processing document sets, removing visible page numbers, adding a TOC, rotating pages, or producing student/teacher handouts.
---

# Document Materials Pipeline

Use this workflow to turn mixed Word/PDF source materials into clean, ordered teaching handouts.

## Workflow

1. Identify source files and ask the user to confirm the edition(s) and exact document order. Never infer order from filenames alone when multiple plausible orders exist.
2. Inspect every source: file type, page count, orientation, page size, existing page numbers, headers/footers, and student/teacher status.
3. Keep student and teacher sources separate. Do not include aggregate PDFs when lesson-specific files are available.
4. Build each unit in the confirmed order. A common unit order is: pre-learning sheet, paragraph-comprehension sheet, mind map, then textbook/handout.
5. Apply requested transformations:
   - Remove visible page numbers only when requested; use a bounded mask or content-aware edit and verify body text is not covered.
   - Rotate mind maps or other pages only when requested. Transfer rotation into page content before adding page numbers so the displayed page dimensions and bottom-center position are correct.
   - Add a TOC first when requested. The TOC is unnumbered;正文 pages start at 1 on the next page.
   - Add page numbers at the displayed bottom-center position by default, using the requested font size, accounting for rotated pages and mixed page sizes. Use another position only when the user explicitly requests it.
6. Preserve source files by default. Write outputs to the requested `output` folder, using stable ASCII filenames when cloud-synced paths may corrupt non-ASCII names.
7. Reopen every final PDF, verify page count and readability, verify TOC start pages against actual unit boundaries, and render representative pages: TOC, first content page, rotated page, middle section, and final page.
8. Report created files, missing source types, total pages, and final paths.

## Word and PDF handling

- Use `pypdf` for PDF merging, rotation, overlays, metadata, and structural checks.
- Render PDFs with Ghostscript or Poppler for visual QA; do not rely on file existence or text extraction alone.
- For DOCX sources, preserve the original and render through the document workflow before converting or merging.
- Use a Unicode-capable font for Chinese TOCs and labels, such as Microsoft JhengHei or Noto Sans TC.
- When adding overlays to rotated pages, call `transfer_rotation_to_content()` first, then place the overlay using the resulting displayed page dimensions.

## User interaction

Ask for the order whenever it is not explicitly supplied. Confirm whether the user wants student, teacher, or both editions; whether source files should be overwritten; whether the TOC counts toward page numbering; the requested page-number font size; and whether page-number removal or page rotation is required. Unless the user specifies otherwise, place page numbers at the displayed bottom center because it is the clearest and most balanced default for teaching handouts.

## Bundled resources

Use `scripts/process_materials.py` for deterministic PDF unit merging, optional mind-map rotation, TOC creation, and page numbering. Read its `--help` output before use. Pass a JSON configuration containing the user-confirmed order and edition-specific source selections.
