# Document Materials Pipeline

A Codex skill and deterministic Python helper for preparing teaching materials from Word and PDF sources.

## Features

- Keeps student and teacher editions separate.
- Lets the user confirm the exact unit order before processing.
- Supports ordered PDF merging, optional page-number removal workflows, page rotation, table-of-contents creation, and page numbering.
- Handles mixed page sizes and rotated pages by transferring rotation into page content before overlays.
- Includes a JSON-driven processing script for repeatable output.

## Use

1. Install the skill folder into your Codex skills directory.
2. Install Python dependencies:

   `pip install pypdf reportlab`

3. Read `SKILL.md` and ask the user to confirm edition, source mapping, document order, TOC behavior, page-number location/size, and overwrite policy.
4. Run:

   `python scripts/process_materials.py config.json`

The configuration contains a title, output path, page-number size, TOC settings, and an ordered `units` list. Each unit has `name`, `sources`, and optional zero-based `rotate_indices`.

## Validation

Reopen the output with `pypdf`, verify page counts and TOC boundaries, then render representative pages using Ghostscript or Poppler.

## License

MIT
