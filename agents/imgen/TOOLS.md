# TOOLS.md - Imgen Agent Local Notes

## Key References

### n8n Instance
- **URL:** `https://duncanrogoff.app.n8n.cloud/`
- For screenshot slides: use browser tool to capture real workflow screenshots
- Navigate to specific workflow → zoom to fit → screenshot → crop/resize → style

### Duncan's Likeness Reference
- **Imgur:** `https://i.imgur.com/vc7pPOC.jpeg`
- 4-angle reference sheet (front, side, back, three-quarter)
- Orange hoodie is signature outfit

### Text Styling
- **Engine:** `/data/.openclaw/workspace/carousel-system/text_styler.py`
- White Roboto bold, 80px left offset, soft drop shadow
- Scale: 0.82× for 4:5 (headline ~54px, body ~36px)
- Darken backgrounds to 85% brightness
- No background boxes, no emojis, no outlines

### Format Validation
- **Validator:** `/data/.openclaw/workspace/carousel-system/format_validator.py`
- **Resizer:** `/data/.openclaw/workspace/carousel-system/resize_to_format.py`
- Always validate dimensions before upload

### Imgur Upload
- **Client ID:** `546c25a59c58ad7` (anonymous)
- Base64 encode → POST to `https://api.imgur.com/3/image`

### Process Doc
- **File:** `/data/.openclaw/workspace/CAROUSEL_PROCESS.md`
- Single source of truth for the full carousel pipeline

## Non-Negotiable Rules
- **NEVER** use dark placeholder backgrounds for screenshot slides — capture REAL n8n workflows
- **NEVER** skip infographic generation
- **ALWAYS** validate format before uploading
- **ALWAYS** check text isn't clipped at edges before finishing
- Fix all issues yourself — never present broken work

## Reference Materials
- **reference-photos/public_url.txt** - Duncan's reference photo for matching style/persona in generated images
- **image-generation.md** - Master prompt templates for gpt-image-1.5 (photo-realistic iPhone-style images)
