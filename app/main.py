import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse
from starlette.background import BackgroundTask

from app.content.generator import generate_posts
from app.images.builder import generate_branded_image
from app.export.packager import export_batch

app = FastAPI(title="XenoCG v1 - Instagram Content Generator")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Serve a minimal UI with a button to generate the batch."""
    html_path = Path(__file__).parent / "templates" / "index.html"
    if html_path.is_file():
        return HTMLResponse(html_path.read_text())
    # Fallback simple HTML if template missing
    return HTMLResponse("""
    <html><head><title>XenoCG Generator</title></head>
    <body style='font-family:Arial,Helvetica,sans-serif; text-align:center; margin-top:50px;'>
      <h1>XenoCG v1 – Generate 30 Instagram Posts</h1>
      <button onclick='location.href="/generate-30-posts"' style='padding:12px 24px;font-size:1.2rem;'>Generate</button>
    </body></html>
    """)

@app.get("/generate-30-posts")
def generate_30_posts():
    """Create 30 posts, package them into a ZIP, and stream the file back to the client."""
    # 1. Generate content metadata for 30 posts
    posts = generate_posts(30)
    # 2. Export batch to ZIP and get path
    zip_path = export_batch(posts)
    # 3. Return the ZIP as a downloadable file
    filename = os.path.basename(zip_path)
    return FileResponse(path=zip_path, filename=filename, media_type='application/zip')
