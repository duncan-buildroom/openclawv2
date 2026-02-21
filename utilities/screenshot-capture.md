# Screenshot Capture System — Skill File
**Owner:** Duncan Rogoff
**Last Updated:** 2026-02-13
**Purpose:** Browser automation for capturing clean, carousel-ready screenshots of tools, dashboards, and proof metrics.

---

## 1. Tools & Setup

### Primary Method: Playwright (Node.js)
Duncan already uses Playwright for browser automation. This extends it for screenshot capture.

```bash
# Install if not already available
npm install playwright
```

### Alternative: Manual + CleanShot X (macOS)
For one-off captures when automation is overkill.

---

## 2. Screenshot Targets

### What to Capture (Organized by Content Category)

#### Automation Workflows
- **n8n canvas view** — Full workflow zoomed to show node connections
- **n8n node detail** — Individual node config showing logic
- **n8n execution log** — Successful runs with timestamps
- **Make.com scenario** — Full scenario builder view
- **Make.com execution history** — Run count, success rate

#### Proof & Metrics
- **TikTok Analytics** — Follower growth, video views, profile views
- **YouTube Studio** — Subscriber count, view graphs, top videos
- **LinkedIn analytics** — Post impressions, profile views, follower growth
- **Skool dashboard** — Member count, engagement metrics, revenue
- **Stripe/PayPal** — Revenue screenshots (blur sensitive info)
- **Airtable views** — Client lists, project trackers, content calendars

#### Client Work
- **Client dashboards** — Lovable/Notion dashboards built for clients
- **Before/after workflows** — Side-by-side of manual vs automated
- **DM conversations** — Testimonials, results messages (with permission)
- **Proposal documents** — Project scope and pricing (anonymized)

---

## 3. Playwright Automation Script

### Base Screenshot Function

```javascript
const { chromium } = require('playwright');

async function captureScreenshot(options) {
  const {
    url,
    selector = null,       // CSS selector for specific element
    viewport = { width: 1080, height: 1920 },  // TikTok carousel size
    darkMode = true,
    outputPath = './screenshots/capture.png',
    waitFor = 2000,        // ms to wait for page load
    hideElements = [],     // CSS selectors to hide (nav bars, sidebars)
    annotations = []       // { x, y, width, height, color } for highlights
  } = options;

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport,
    colorScheme: darkMode ? 'dark' : 'light',
    deviceScaleFactor: 2   // Retina quality
  });

  const page = await context.newPage();
  await page.goto(url, { waitUntil: 'networkidle' });
  await page.waitForTimeout(waitFor);

  // Hide unwanted elements
  for (const sel of hideElements) {
    await page.evaluate((s) => {
      document.querySelectorAll(s).forEach(el => el.style.display = 'none');
    }, sel);
  }

  // Capture
  if (selector) {
    const element = await page.$(selector);
    await element.screenshot({ path: outputPath });
  } else {
    await page.screenshot({ path: outputPath, fullPage: false });
  }

  await browser.close();
  return outputPath;
}
```

### n8n Workflow Screenshot

```javascript
async function captureN8nWorkflow(workflowUrl, outputPath) {
  return captureScreenshot({
    url: workflowUrl,
    viewport: { width: 1920, height: 1080 }, // Landscape for workflow
    darkMode: true,
    outputPath,
    waitFor: 3000,
    hideElements: [
      '.sidebar',           // Hide sidebar
      '.execution-panel',   // Hide execution panel
      '[data-test-id="header"]'  // Hide header
    ]
  });
}
```

### Analytics Dashboard Screenshot

```javascript
async function captureDashboard(url, outputPath) {
  return captureScreenshot({
    url,
    viewport: { width: 1080, height: 1920 }, // Portrait for carousel
    darkMode: true,
    outputPath,
    waitFor: 5000,  // Dashboards take longer to render
    hideElements: [
      'nav',
      '.cookie-banner',
      '.notifications'
    ]
  });
}
```

---

## 4. Post-Processing Pipeline

### Step 1: Crop to Carousel Dimensions
Target: 1080 × 1920 px (9:16)

```bash
# Using ImageMagick
convert input.png -resize 1080x1920^ -gravity center -extent 1080x1920 output.png
```

### Step 2: Apply Dark Overlay (if needed)
For screenshots that aren't dark-mode:

```bash
# Darken + increase contrast
convert input.png -brightness-contrast -20x20 -fill 'rgba(0,0,0,0.3)' -draw 'rectangle 0,0 1080,1920' output.png
```

### Step 3: Add Rounded Corners + Shadow (Floating Card Look)

```bash
# Round corners (20px radius) and add drop shadow
convert input.png \
  \( +clone -alpha extract -draw 'fill black polygon 0,0 0,20 20,0 fill white circle 20,20 20,0' \
  \( +clone -flip \) -compose Multiply -composite \
  \( +clone -flop \) -compose Multiply -composite \) \
  -alpha off -compose CopyOpacity -composite \
  \( +clone -background '#0D0D0D' -shadow 60x10+0+10 \) \
  +swap -background '#0D0D0D' -layers merge +repage \
  output.png
```

### Step 4: Add Text Overlay
Use `image-generation.md` system or Canva for adding text overlays on top of screenshots.

---

## 5. Sensitive Data Handling

### What to Blur
- Client full names (use first name only or initials)
- Email addresses
- Phone numbers
- API keys / tokens
- Billing details
- Full URLs with auth tokens

### What to Keep Visible
- Revenue numbers (the whole point)
- Follower/subscriber counts
- View counts and engagement metrics
- Workflow node names and structure
- Tool names and integrations
- Timestamps (proves recency)

### Blur Method

```bash
# Blur specific region (x, y, width, height)
convert input.png -region 200x50+400+300 -blur 0x20 output.png
```

---

## 6. Screenshot Library Structure

```
/screenshots/
├── workflows/
│   ├── n8n-content-repurpose.png
│   ├── n8n-lead-gen.png
│   ├── make-tiktok-scraper.png
│   └── ...
├── analytics/
│   ├── tiktok-growth-feb2026.png
│   ├── youtube-studio-feb2026.png
│   ├── skool-dashboard.png
│   └── ...
├── proof/
│   ├── revenue-screenshot.png
│   ├── client-dm-testimonial.png
│   ├── follower-milestone.png
│   └── ...
├── client-work/
│   ├── jason-workflows.png
│   ├── eartha-church-automation.png
│   └── ...
└── templates/
    ├── slide-template-dark.png
    ├── slide-template-proof.png
    └── ...
```

---

## 7. Batch Capture Workflow

For weekly content production, batch-capture all needed screenshots:

### Weekly Capture Checklist
- [ ] TikTok Analytics (follower growth, top video stats)
- [ ] YouTube Studio (subscriber graph, recent video performance)
- [ ] Skool dashboard (member count, engagement)
- [ ] Any new n8n workflows built this week
- [ ] Client results/wins (with permission)
- [ ] Revenue milestones (if applicable)
- [ ] New tool setups or integrations

### Automation via n8n
Build an n8n workflow that:
1. Triggers weekly (Monday morning)
2. Opens Playwright to capture analytics dashboards
3. Saves to Google Drive / local screenshots folder
4. Sends Telegram notification with thumbnails
5. Updates Airtable content calendar with available screenshots

---

## 8. Quality Standards

### Must-Have
- **Retina quality** — 2x device scale factor minimum
- **Dark mode** — Matches Duncan's brand aesthetic
- **Clean viewport** — No browser chrome, no notifications, no cookie banners
- **Readable at mobile size** — If you can't read it on a phone, it's too small
- **Consistent framing** — Same padding/margins across all screenshots

### Nice-to-Have
- Accent color highlights on key metrics (#22D3EE cyan or #F59E0B amber)
- Subtle gradient overlay at edges (focuses attention on center)
- Brand watermark in corner (small, non-distracting)

### Don't
- Don't screenshot at 1x resolution (will look blurry on retina phones)
- Don't include personal bookmarks bar or tabs
- Don't leave error states or loading spinners visible
- Don't use light mode screenshots on dark carousel backgrounds (jarring contrast)
