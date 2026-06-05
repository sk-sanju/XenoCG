import random
import json
from datetime import datetime
from typing import List, Dict

# Predefined pools for diversity
_TITLES = [
    "Unlock the Future of AI",
    "Data-Driven Insights at Scale",
    "Transforming Business with Tech",
    "Innovate with Xenotrix",
    "AI-Powered Solutions",
    "Next‑Gen Analytics",
    "Empowering Digital Transformation",
    "Smart Automation Strategies",
    "Future‑Ready Architecture",
    "Accelerate Your Innovation"
]

_CAPTION_TEMPLATES = [
    "Discover how {topic} can drive growth and efficiency for your organization. #Xenotrix #Innovation",
    "Explore the power of {topic} and stay ahead in the competitive landscape. #TechThoughts",
    "Leverage {topic} to unlock new opportunities. Stay tuned! #AI #DataScience",
    "At Xenotrix, we make {topic} simple and effective. #BusinessTech",
    "Ready to adopt {topic}? Here’s what you need to know. #Automation"
]

_HASHTAG_POOL = [
    "#AI", "#MachineLearning", "#DataAnalytics", "#Tech", "#Innovation", "#Automation",
    "#DigitalTransformation", "#Cloud", "#BigData", "#BusinessIntelligence"
]

_CATEGORIES = ["AI", "Tech", "Business", "Xenotrix", "Data Analytics"]

def _unique_sample(pool: List[str], k: int) -> List[str]:
    """Return k unique items from pool, repeating if k > len(pool)."""
    if k <= len(pool):
        return random.sample(pool, k)
    # If more items needed, repeat with shuffle
    result = []
    while len(result) < k:
        shuffled = random.sample(pool, len(pool))
        result.extend(shuffled)
    return result[:k]

def generate_posts(count: int = 30) -> List[Dict]:
    """Generate a list of post dictionaries with title, caption, hashtags, category and timestamp.
    Each post is guaranteed to have a unique title and caption.
    """
    titles = _unique_sample(_TITLES, count)
    captions = []
    for i in range(count):
        topic = random.choice(["AI", "cloud computing", "data pipelines", "automation", "analytics"])
        template = random.choice(_CAPTION_TEMPLATES)
        captions.append(template.format(topic=topic))
    # Ensure captions are unique – if a duplicate occurs, regenerate that entry
    seen = set()
    for idx, cap in enumerate(captions):
        while cap in seen:
            topic = random.choice(["AI", "cloud computing", "data pipelines", "automation", "analytics"])
            template = random.choice(_CAPTION_TEMPLATES)
            cap = template.format(topic=topic)
        seen.add(cap)
        captions[idx] = cap

    hashtags_list = _unique_sample(_HASHTAG_POOL, count * 3)  # 3 tags per post
    categories = _unique_sample(_CATEGORIES, count)

    posts = []
    for i in range(count):
        post = {
            "id": i + 1,
            "title": titles[i],
            "caption": captions[i],
            "hashtags": " ".join(hashtags_list[i*3:(i+1)*3]),
            "category": categories[i % len(categories)],
            "image_source": "",  # Filled later
            "created_at": datetime.utcnow().isoformat() + "Z"
        }
        posts.append(post)
    return posts

def metadata_to_json(metadata: Dict) -> str:
    """Serialize a single post metadata dict to pretty JSON."""
    return json.dumps(metadata, indent=2, ensure_ascii=False)
