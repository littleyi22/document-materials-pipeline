作者：奕鈞老師 ｜ [https://www.ijun-ai.com/](https://www.ijun-ai.com/)

# 文件教材處理流程

這是一個 Codex Skill 與可重複執行的 Python 工具，用於清洗、整理、加頁碼、製作目錄，以及合併 Word／PDF 教材文件。

## 功能

- 分開處理學生版與教師用版教材。
- 合併前要求使用者確認文件與單元排列順序。
- 支援 PDF 依指定順序合併。
- 支援依需求移除原有可見頁碼。
- 支援旋轉心智圖或其他指定頁面。
- 支援新增不計頁碼的目錄。
- 支援在正文頁面右下角加入指定大小的頁碼。
- 支援混合頁面尺寸與旋轉頁面。
- 提供 JSON 設定檔，方便重複產製教材。

## 使用方式

1. 將 Skill 資料夾安裝到 Codex 的 skills 目錄。
2. 安裝 Python 相依套件：

   `pip install pypdf reportlab`

3. 使用本 Skill 時，先確認以下項目：
   - 學生版、教師用版，或兩者都要。
   - 每個單元的來源文件對應關係。
   - 文件合併的完整順序。
   - 是否移除原有頁碼。
   - 是否旋轉心智圖或其他頁面。
   - 是否新增目錄，以及目錄是否計入頁碼。
   - 頁碼位置與字體大小。
   - 是否允許覆寫原始檔案。

4. 執行處理腳本：

   `python scripts/process_materials.py config.json`

設定檔需要包含標題、輸出路徑、頁碼字體大小、目錄設定，以及依使用者確認順序排列的 `units`。每個單元包含 `name`、`sources`，以及可選的零起始索引 `rotate_indices`。

## 建議流程

1. 先盤點所有 Word／PDF 來源。
2. 確認學生版與教師用版，不要混合使用。
3. 向使用者確認文件排列順序。
4. 先製作各單元，再依學期或指定順序合併。
5. 新增目錄與頁碼。
6. 重新開啟成品，核對頁數與單元起始頁。
7. 渲染目錄、一般頁、旋轉頁、中間頁與最後一頁進行視覺檢查。

## Word 與 PDF 注意事項

- PDF 結構處理使用 `pypdf`。
- PDF 視覺檢查使用 Ghostscript 或 Poppler；不能只依檔案存在判定成功。
- Word 文件應保留原檔，先依文件處理流程轉換並渲染檢查，再進行合併。
- 中文目錄與標籤應使用支援中文的字體，例如 Microsoft JhengHei 或 Noto Sans TC。
- 對旋轉頁面加頁碼前，先將旋轉套用到頁面內容，再依實際顯示尺寸將頁碼放到右下角。

## 授權

MIT License
---
作者：奕鈞老師 ｜ [https://www.ijun-ai.com/](https://www.ijun-ai.com/)

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
