# AI Image Generation for TikTok Carousels — Skill File
**Owner:** Duncan Rogoff
**Last Updated:** 2026-02-13
**Purpose:** gpt-image-1.5 prompt templates for generating photo-realistic, iPhone-style images for TikTok slideshow carousels.

---

## 1. Core Principle

**Every AI-generated image must look like it was taken on an iPhone by a real person.**

Not AI art. Not renders. Not illustrations. Not stock photography.
Photo-realistic. Natural. Imperfect enough to feel authentic.

---

## 2. Model & Settings

### Primary: gpt-image-1.5
- **Quality:** High
- **Style:** Natural (NOT vivid — vivid pushes toward AI-art look)
- **Size:** 1024×1792 (portrait, closest to 9:16 for TikTok)
- **Output:** PNG

### Fallback: DALL-E 3 / Flux via GoAPI
Same prompt structure applies. Adjust for model-specific quirks.

---

## 3. Master Prompt Template

```
[SCENE DESCRIPTION]. Shot on iPhone 16 Pro, [LIGHTING TYPE], [ENVIRONMENT].
[SUBJECT DESCRIPTION — age, appearance, clothing, expression, action].
[COMPOSITION — framing, angle, depth of field].
Natural skin texture, no retouching, no filters. Candid moment.
No text, no watermarks, no logos, no UI elements.
```

### Key Modifiers (Always Include)
- "Shot on iPhone 16 Pro" — triggers photo-realistic rendering
- "Natural lighting" or "soft window light" — avoids studio look
- "Slight depth of field" — background blur like real phone camera
- "Candid moment" — avoids posed/stock feel
- "No text, no watermarks, no logos" — clean for text overlay later
- "Natural skin texture, no retouching" — prevents AI smoothing

---

## 4. Prompt Templates by Slide Type

### 4A. Hook Slides (Slide 1 — Stop the Scroll)

**Template: Person + Tech Setup**
```
A [age]s [gender] business owner sitting at a modern desk with a MacBook Pro and
large monitor showing colorful data dashboards. Shot on iPhone 16 Pro, warm ambient
lighting from desk lamp, modern home office. They're leaning forward with an excited
expression, hand on trackpad. Slight depth of field, shot from slight angle.
Natural skin texture, no retouching. Candid moment.
No text, no watermarks, no logos, no UI elements.
```

**Template: Phone Screen Reveal**
```
Close-up of hands holding an iPhone showing a notification with follower count.
Shot on iPhone 16 Pro, natural daylight from nearby window, café setting.
Shallow depth of field, coffee cup blurred in background. The phone screen
shows a clean analytics interface. Natural hand positioning, candid grip.
No text overlays, no watermarks.
```

**Template: Before/After Contrast**
```
Split composition: left side shows a dimly lit, cluttered desk with papers and
a stressed person. Right side shows a clean, organized desk with a smiling
person and a glowing laptop screen. Shot on iPhone 16 Pro, natural mixed
lighting. Both sides feel authentic, not staged. Candid energy.
No text, no watermarks, no logos.
```

### 4B. Problem Slides (Slide 2 — Pain Point Visualization)

**Template: Frustrated Business Owner**
```
A [age]s professional [gender] sitting alone at a coffee shop, staring at their
laptop with a concerned expression. Empty coffee cups nearby. Shot on iPhone 16 Pro,
overcast natural light through window. They're rubbing their forehead, clearly
struggling with something on screen. Slight depth of field, other patrons blurred.
Natural skin texture, candid moment. No text, no watermarks.
```

**Template: Empty Inbox / No Leads**
```
Over-the-shoulder shot of a person looking at a laptop screen showing an empty
email inbox. Shot on iPhone 16 Pro, home office setting, soft desk lamp light.
The person's posture suggests disappointment — slumped slightly. Shallow depth
of field. Natural, unposed. No text, no watermarks.
```

**Template: Scrolling Social Media (Seeing Others Succeed)**
```
Close-up of a person's face lit by phone screen glow in a dim room, scrolling
through social media. Their expression is a mix of frustration and longing.
Shot on iPhone 16 Pro, phone light is primary illumination. Intimate, candid
moment. Natural skin texture. No text, no watermarks.
```

### 4C. Aspiration Slides (Slide 5-6 — The After State)

**Template: Success Moment**
```
A confident [age]s [gender] business owner standing at a modern standing desk,
smiling while looking at a large monitor showing growth charts trending upward.
Shot on iPhone 16 Pro, bright natural daylight from large windows, modern office
or co-working space. They're holding a coffee, relaxed posture. Plants and
clean decor in background. Depth of field on background. Candid energy.
No text, no watermarks.
```

**Template: Client Call Win**
```
A [age]s professional [gender] on a video call, visible on laptop screen,
leaning back in chair with a genuine smile and subtle fist pump gesture.
Shot on iPhone 16 Pro, home office with good lighting. The laptop screen
shows a video call interface. The mood is celebratory but natural.
No text, no watermarks, no logos.
```

**Template: Building an Audience**
```
A [age]s [gender] content creator filming themselves with a ring light and
camera setup in a clean home studio. They look engaged and confident,
mid-sentence. Shot on iPhone 16 Pro from behind the camera setup, showing
both the creator and their recording equipment. Natural energy, not overly
produced. Slight depth of field. No text, no watermarks.
```

### 4D. Framework/System Slides (Slide 5 — Visual Breakdown)

For framework slides, **generate a clean background** and add text/graphics in Canva:

**Template: Clean Background for Text Overlay**
```
Minimalist dark gradient background, deep navy (#0a0f1e) to charcoal (#1a1a2e),
with subtle geometric light patterns or soft bokeh. Shot as if through textured
glass. No subjects, no objects. Clean space for text overlay.
No text, no watermarks.
```

**Template: Desk Flatlay (For Framework Overlays)**
```
Top-down flatlay of a clean dark desk with a MacBook, iPhone, AirPods, notebook,
and a single plant. Organized, minimal, aesthetic. Shot on iPhone 16 Pro with
flash, creating slight shadows. Space in center for text overlay.
No text, no watermarks.
```

---

## 5. Diversity & Representation

### Subject Specifications
Rotate through diverse representations to reflect Duncan's actual audience:
- **Age range:** 28-55 (core: 32-45)
- **Gender:** Mixed — male, female, non-binary presentations
- **Ethnicity:** Diverse — rotate through each batch
- **Style:** Professional-casual (no suits, no hoodies — think "successful freelancer")
- **Settings:** Home offices, co-working spaces, coffee shops, modern apartments

### Avoid
- All subjects looking the same across posts
- Only one gender or ethnicity
- Unrealistic beauty standards (no model-perfect faces)
- Corporate/stock photo poses

---

## 6. Quality Control Checklist

Before using any AI-generated image in a carousel:

- [ ] **Realism test:** Would someone think this is a real iPhone photo? If not, regenerate.
- [ ] **Hand check:** Fingers look natural? (Common AI failure point — regenerate if weird)
- [ ] **Text artifacts:** No accidental text or symbols generated in the image?
- [ ] **Screen content:** If there's a screen visible, does it look realistic? (Can be blurry/generic)
- [ ] **Skin texture:** Natural, not waxy/smooth/plastic?
- [ ] **Lighting:** Consistent light sources, no impossible shadows?
- [ ] **Composition:** Enough space for text overlay where needed (top or center)?
- [ ] **Background:** No random impossible architecture or objects?
- [ ] **Brand match:** Fits the dark/modern/clean aesthetic?

### Regeneration Triggers
If any of these appear, regenerate immediately:
- Extra fingers or merged hands
- Text or letters appearing in the image
- Waxy/plastic skin (especially faces)
- Impossibly perfect symmetry (stock photo vibes)
- Artifacts or glitches in backgrounds
- Inconsistent lighting/shadows

---

## 7. Batch Generation Workflow

### Weekly Image Batch (Aligned with Content Plan)

1. Review the week's 5-7 carousel briefs
2. Identify which slides need AI images (typically 3-4 per carousel × 5-7 = 15-28 images)
3. Write prompts using templates above
4. Generate 2-3 variations per prompt (pick best)
5. Run through quality checklist
6. Save to `/images/ai-generated/YYYY-MM-DD/` folder
7. Tag with content brief number for easy assembly

### Folder Structure
```
/images/
├── ai-generated/
│   ├── 2026-02-13/
│   │   ├── hook-frustrated-owner-v1.png
│   │   ├── hook-frustrated-owner-v2.png
│   │   ├── aspiration-success-desk-v1.png
│   │   └── ...
│   └── 2026-02-20/
│       └── ...
├── screenshots/     (→ see screenshot-capture.md)
└── assembled/       (final carousel slides with text overlays)
    ├── carousel-001/
    │   ├── slide-1.png
    │   ├── slide-2.png
    │   └── ...
    └── ...
```

---

## 8. Text Overlay Integration

After generating the base image, add text overlays using:

### Option A: Canva (Fastest)
1. Upload AI image as background
2. Add text using Inter Bold / Montserrat Black
3. White text with subtle drop shadow (2px, 40% opacity black)
4. Export at 1080×1920

### Option B: Figma (Most Control)
1. Create 1080×1920 frame
2. Place AI image as fill
3. Add text layers with brand fonts
4. Use auto-layout for consistent spacing
5. Export as PNG 2x

### Option C: Automated (ImageMagick)
```bash
convert base-image.png \
  -gravity North -pointsize 72 -font "Inter-Bold" \
  -fill white -stroke 'rgba(0,0,0,0.5)' -strokewidth 2 \
  -annotate +0+200 "Your Hook Text Here" \
  output-slide.png
```

---

## 9. Prompt Iteration Log

Track which prompts produce the best results:

| Date | Prompt Summary | Quality (1-5) | Issues | Notes |
|------|---------------|----------------|--------|-------|
| _template_ | _"[age]s owner at desk..."_ | _4_ | _Hand slightly off_ | _Added "hands visible on keyboard" — fixed_ |

### Lessons Learned
- Adding "Shot on iPhone 16 Pro" is the single biggest quality lever
- "Candid moment" prevents stock-photo posing
- Specifying exact age (e.g., "38-year-old") beats "middle-aged"
- "No retouching" prevents waxy skin
- For screens in images, say "screen shows blurred interface" — don't try to generate specific UI
- "Slight depth of field" is better than "bokeh" (bokeh sometimes triggers artistic blur)
