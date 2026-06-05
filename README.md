# XenoCG v1 – Instagram Content Generator

## Overview
A production‑ready, local‑first FastAPI application that generates **30 Instagram posts** in a single click. Each post includes:
- AI‑styled caption and hashtags
- Branded image (generated with Pillow; optional stock‑image integration)
- Structured metadata JSON
- Packaged as a downloadable ZIP ready for Meta Business Suite.

## Project Structure
```
XenoCG/
├─ app/
│   ├─ __init__.py
│   ├─ main.py            # FastAPI entry point & UI route
│   ├─ config.py          # Settings (paths, colors, API keys)
│   ├─ content/
│   │   ├─ __init__.py
│   │   └─ generator.py    # Title / caption / hashtag generation
│   ├─ images/
│   │   ├─ __init__.py
│   │   └─ builder.py      # Pillow branding overlay
│   ├─ export/
│   │   ├─ __init__.py
│   │   └─ packager.py     # Folder hierarchy & ZIP creation
│   └─ templates/
│       └─ index.html      # Minimal UI with generate button
├─ assets/
│   └─ logo.png            # **Provide your Xenotrix logo here**
├─ output_batches/          # Generated ZIP batches (auto‑created)
├─ requirements.txt
└─ README.md                # This file
```

## Setup & Run
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the development server
uvicorn app.main:app --reload --port 8000
```
Open `http://127.0.0.1:8000/` in a browser and click **Generate Batch**. The UI will download a ZIP named `xenocg_batch_<timestamp>.zip`.

## How It Works
1. **Content generation** (`app/content/generator.py`) creates 30 unique post dictionaries – title, caption, hashtags, category, timestamps.
2. **Image generation** (`app/images/builder.py`) produces a 1080×1080 dark‑navy background, adds the post title and the Xenotrix logo (or a placeholder).
3. **Export** (`app/export/packager.py`) builds the required folder hierarchy, writes `image.jpg`, `caption.txt`, `metadata.json` for each post, zips the whole batch, and returns the ZIP path.
4. **FastAPI endpoint** (`/generate-30-posts`) orchestrates the above steps and streams the ZIP back to the client.
5. **Optional UI** (`app/templates/index.html`) provides a polished single‑page interface with a generate button and automatic download link.

## Customisation
- **Brand colours** – edit `BRAND_PRIMARY_COLOR` and `BRAND_ACCENT_COLOR` in `app/config.py`.
- **Logo** – replace `assets/logo.png` with your official PNG (transparent background). If missing, a placeholder logo is generated automatically.
- **Stock images** – set `UNSPLASH_ACCESS_KEY` or `PEXELS_API_KEY` in the environment and extend `builder.py` to fetch real images. The current implementation falls back to the solid colour placeholder.
- **Output location** – change `OUTPUT_ROOT` in `app/config.py`.

## Testing & Verification
- Run the server and generate a batch.
- Unzip the file; each `post_<n>` folder should contain:
  - `image.jpg` – branded image with title overlay.
  - `caption.txt` – caption + hashtags.
  - `metadata.json` – valid JSON matching the defined schema.
- Verify that the total generation time stays under 5 minutes on a typical workstation.

## Future Enhancements (optional)
- Dockerisation for container deployment.
- Integration with Unsplash/Pexels APIs for real stock images.
- Unit test suite (`pytest`) for content uniqueness and ZIP integrity.
- CI/CD pipeline to run tests and build Docker images.
- More sophisticated UI (React/Vite) if a richer front‑end is required.

---
*All files are located under `d:/Xenotrix/XenoCG/`. The system is ready for production‑grade local execution.*
