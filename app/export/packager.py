import os
import json
import shutil
from datetime import datetime
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

from ..config import OUTPUT_ROOT
from ..images.builder import generate_branded_image

def export_batch(posts):
    """Create a batch directory with 30 post sub‑folders, write assets, and zip it.
    Returns the absolute path to the created ZIP file.
    """
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    batch_dir = Path(OUTPUT_ROOT) / f"batch_{timestamp}"
    batch_dir.mkdir(parents=True, exist_ok=True)

    for post in posts:
        post_id = post["id"]
        post_dir = batch_dir / f"post_{post_id}"
        post_dir.mkdir(parents=True, exist_ok=True)

        # Image
        image_path = post_dir / "image.jpg"
        generate_branded_image(post["title"], image_path)
        post["image_source"] = "image.jpg"

        # Caption (title not needed; caption already includes hashtags)
        caption_path = post_dir / "caption.txt"
        with open(caption_path, "w", encoding="utf-8") as f:
            f.write(post["caption"] + "\n" + post["hashtags"])

        # Metadata JSON
        metadata_path = post_dir / "metadata.json"
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(post, f, indent=2, ensure_ascii=False)

    # Create ZIP archive
    zip_name = f"batch_30_instagram_posts_{timestamp}.zip"
    zip_path = batch_dir.parent / zip_name
    with ZipFile(zip_path, "w", compression=ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(batch_dir):
            for file in files:
                file_path = Path(root) / file
                # Archive path should be relative to the batch_dir parent
                arcname = file_path.relative_to(batch_dir.parent)
                zipf.write(file_path, arcname)

    # Optionally clean up the unzipped batch folder (keep only ZIP)
    shutil.rmtree(batch_dir, ignore_errors=True)
    return zip_path
