import os
from flask import Flask, render_template, request, jsonify
from groq import Groq
import replicate

app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing")

if not REPLICATE_API_TOKEN:
    raise ValueError("REPLICATE_API_TOKEN is missing")

groq_client = Groq(api_key=GROQ_API_KEY)
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN


@app.route("/")
def home():
    return render_template("instagram_auto_post.html")


@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()

        topic = data.get("topic")
        tone = data.get("tone")

        prompt = f"""
Generate an Instagram post.

Topic: {topic}
Tone: {tone}

Return ONLY in this format:

Caption:
<caption>

Hashtags:
<8-10 hashtags>

Image Prompt:
<realistic image prompt>

Best Time:
<best time to post>
"""

        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        text = response.choices[0].message.content

        caption = text.split("Caption:")[1].split("Hashtags:")[0].strip()
        hashtags = text.split("Hashtags:")[1].split("Image Prompt:")[0].strip()
        image_prompt = text.split("Image Prompt:")[1].split("Best Time:")[0].strip()
        best_time = text.split("Best Time:")[1].strip()

        image = replicate.run(
            "black-forest-labs/flux-schnell",
            input={
                "prompt": image_prompt,
                "go_fast": True,
                "megapixels": "1",
                "num_outputs": 1,
                "aspect_ratio": "1:1",
                "output_format": "png",
                "output_quality": 80
            }
        )

        image_url = image[0]

        return jsonify({
            "caption": caption,
            "hashtags": hashtags,
            "bestTime": best_time,
            "image": image_url
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)