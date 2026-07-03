#!/usr/bin/env python3
import os
import sys
import math
import random
import asyncio
import argparse
import urllib.parse
import requests
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips

SCRIPTS = {
    "subhas chandra bose": {
        "segments": [
            {
                "text": "Netaji Subhas Chandra Bose, a legendary leader of India's freedom struggle.",
                "image_prompt": "A highly accurate historical portrait painting of Netaji Subhas Chandra Bose in military uniform, round spectacles, round military cap, looking forward, dramatic warm lighting, oil painting style, masterpiece"
            },
            {
                "text": "He founded the Indian National Army, fighting British colonial rule.",
                "image_prompt": "Netaji Subhas Chandra Bose addressing a passionate crowd of soldiers, epic historical painting, warm atmospheric lighting, high detail, masterpiece"
            },
            {
                "text": "His cry, 'Give me blood and I shall give you freedom', echoes forever.",
                "image_prompt": "A majestic monument of Subhas Chandra Bose with the Indian tricolor flag waving proudly in a dramatic sky at sunset, cinematic lens flare, photorealistic"
            }
        ]
    },
    "bhagat singh": {
        "segments": [
            {
                "text": "Bhagat Singh, a legendary symbol of courage in India's independence movement.",
                "image_prompt": "A highly accurate historical portrait painting of Shaheed Bhagat Singh with his iconic mustache, wearing his signature black felt hat and white shirt, looking intensely forward, dramatic lighting, historic sepia oil painting style, masterpiece"
            },
            {
                "text": "His slogan 'Inquilab Zindabad' inspired millions to rise against colonial rule.",
                "image_prompt": "Shaheed Bhagat Singh speaking passionately in a historic courtroom, detailed face, vintage lighting, classic warm colors, oil painting style, masterpiece"
            },
            {
                "text": "At just twenty-three, his ultimate sacrifice immortalized him as a hero.",
                "image_prompt": "A symbolic glowing flame of freedom inside a dark cell, representing the sacrifice of Bhagat Singh, cinematic golden lighting, hyper-detailed"
            }
        ]
    },
    "mahatma gandhi": {
        "segments": [
            {
                "text": "Mahatma Gandhi, the father of the nation, led India with non-violence.",
                "image_prompt": "A warm cinematic portrait of Mahatma Gandhi wearing simple round spectacles and a khadi shawl, walking with a staff, smiling gently, beautiful historic painting style, soft natural morning sunlight"
            },
            {
                "text": "His historic salt march and peaceful protests united millions.",
                "image_prompt": "A massive crowd of diverse Indian citizens marching together on a dusty road at sunrise, leading with peace, cinematic atmospheric dust, oil painting style"
            },
            {
                "text": "His simple message of peace and self-reliance reshaped history.",
                "image_prompt": "A close-up of a traditional Indian spinning wheel (Charkha) in a rustic cottage, warm sunbeams streaming through a window, nostalgic cinematic lighting"
            }
        ]
    },
    "rani lakshmibai": {
        "segments": [
            {
                "text": "Rani Lakshmibai of Jhansi, the warrior queen who stood against colonial rule.",
                "image_prompt": "A heroic cinematic painting of Rani Lakshmibai of Jhansi on a white rearing horse, holding a sword high, armor gleaming, historic battlefield, dramatic lighting"
            },
            {
                "text": "She led Jhansi's troops into battle, defending her land with bravery.",
                "image_prompt": "Rani Lakshmibai in combat, fighting courageously amidst smoke and dust of war, dramatic warm color palette, detailed historical oil painting"
            },
            {
                "text": "Her name remains forever etched as Jhansi's legendary queen.",
                "image_prompt": "A golden statue of Rani Lakshmibai of Jhansi at sunset, silhouette against a brilliant orange sky, majestic, cinematic wide angle, epic perspective"
            }
        ]
    }
}

def query_gemini(fighter_name, api_key=None, creds_path=None, timeout=30):
    system_instruction = (
        "You are an expert scriptwriter and AI prompt engineer for high-production historical documentary shorts. "
        "Your task is to generate a 10-second introduction to a specified Indian freedom fighter. "
        "The script must be split into exactly 3 sequential segments. The total spoken voiceover word count should be around "
        "20 to 25 words in total across all segments (approx 6-8 words per segment), as this ensures the spoken duration "
        "at normal speech rate is around 9-10 seconds. "
        "For each segment, generate: "
        "1. The voiceover text (extremely concise, dramatic, and inspiring). "
        "2. A detailed AI image generation prompt. IMPORTANT: The image prompt must describe the actual historical appearance of the specific freedom fighter in detail (e.g. for Bhagat Singh: mustache, wearing his iconic black felt hat, white shirt; for Subhas Chandra Bose: round spectacles, military uniform, round cap; for Mahatma Gandhi: round spectacles, dhoti, smiling face) to ensure the generated image resembles them historically. Visual style must be a historic oil painting, highly detailed, dramatic lighting, no text in image. "
        "You must respond with a JSON object containing a list of exactly 3 segments under the key 'segments'. "
        "Each segment must have 'text' and 'image_prompt' keys. Do not include any markdown styling or wrapper other than JSON."
    )
    
    prompt = f"Create a 10-second cinematic introduction video script for the Indian freedom fighter: {fighter_name}."
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "systemInstruction": {"parts": [{"text": system_instruction}]},
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.2
        }
    }
    
    if not creds_path:
        creds_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "GOOGLE_APPLICATION_CREDENTIALS.json")
        
    if os.path.exists(creds_path):
        try:
            import google.auth
            from google.auth.transport.requests import Request
            
            credentials, project_id = google.auth.load_credentials_from_file(
                creds_path,
                scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )
            credentials.refresh(Request())
            access_token = credentials.token
            
            region = "us-central1"
            vertex_url = f"https://{region}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{region}/publishers/google/models/gemini-2.5-flash:generateContent"
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            vertex_payload = {}
            if "contents" in payload:
                vertex_contents = []
                for content in payload["contents"]:
                    if isinstance(content, dict):
                        vc = content.copy()
                        if "role" not in vc:
                            vc["role"] = "user"
                        vertex_contents.append(vc)
                    else:
                        vertex_contents.append(content)
                vertex_payload["contents"] = vertex_contents
            
            sys_inst = payload.get("system_instruction") or payload.get("systemInstruction")
            if sys_inst:
                vertex_payload["systemInstruction"] = sys_inst
                
            gen_cfg = payload.get("generationConfig") or payload.get("generation_config")
            if gen_cfg:
                vertex_payload["generationConfig"] = gen_cfg
                
            print("[*] Contacting Vertex AI Gemini API...")
            res = requests.post(vertex_url, headers=headers, json=vertex_payload, timeout=timeout)
            if res.status_code == 200:
                return res.json()
            else:
                print(f"[!] Vertex AI returned status {res.status_code}. Checking AI Studio fallback...")
        except Exception as ve:
            print(f"[!] Vertex AI connection issue: {ve}")
            
    api_key = api_key or os.environ.get("GEMINI_API_KEY")
    if api_key:
        try:
            print("[*] Contacting Google AI Studio API...")
            ai_studio_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
            res = requests.post(ai_studio_url, headers={"Content-Type": "application/json"}, json=payload, timeout=timeout)
            if res.status_code == 200:
                return res.json()
            else:
                print(f"[!] AI Studio returned status {res.status_code}")
        except Exception as ae:
            print(f"[!] AI Studio connection issue: {ae}")
            
    return None

def parse_gemini_response(res_json):
    if not res_json:
        return None
    try:
        text = res_json["candidates"][0]["content"]["parts"][0]["text"].strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
        import json
        parsed = json.loads(text)
        if "segments" in parsed and len(parsed["segments"]) > 0:
            return parsed
    except Exception as e:
        print(f"[!] Failed to parse JSON response: {e}")
    return None

def get_script(fighter_name, api_key=None, creds_path=None):
    res_json = query_gemini(fighter_name, api_key, creds_path)
    parsed = parse_gemini_response(res_json)
    if parsed:
        print(f"[+] Dynamically generated script for {fighter_name} using Gemini.")
        return parsed
        
    key = fighter_name.lower().strip()
    if key in SCRIPTS:
        print(f"[*] Using local fallback script for {fighter_name}.")
        return SCRIPTS[key]
        
    print(f"[!] No match found for '{fighter_name}'. Using generic template.")
    return {
        "segments": [
            {
                "text": f"{fighter_name} was a key leader in India's struggle for independence, inspiring generations.",
                "image_prompt": f"A cinematic historical portrait of {fighter_name}, looking courageous, warm dramatic colors, oil painting style"
            },
            {
                "text": "Through relentless determination and sacrifices, they fought against oppressive colonial rule.",
                "image_prompt": f"A dramatic historical scene depicting {fighter_name} leading patriots, atmospheric smoke, cinematic lighting, masterpiece"
            },
            {
                "text": f"Today, the legacy of {fighter_name} stands as an eternal beacon of freedom and patriotism.",
                "image_prompt": f"A majestic monument dedicated to the freedom struggle of India, tricolor flag waving, golden sunset sky, cinematic wide angle"
            }
        ]
    }

def download_image(prompt, output_path, seed=None, retries=4):
    import time
    if seed is None:
        seed = random.randint(0, 100000)
    full_prompt = f"{prompt}, highly detailed, cinematic style, 8k resolution, oil painting style, dramatic warm lighting"
    url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(full_prompt)}?width=1280&height=720&nologo=true&seed={seed}"
    
    for attempt in range(retries):
        print(f"[*] Fetching image from Pollinations (attempt {attempt+1}/{retries})...")
        try:
            res = requests.get(url, timeout=40)
            if res.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(res.content)
                print(f"[+] Saved image to {output_path}")
                return True
        except Exception as e:
            print(f"[!] Image download error: {e}")
            if attempt < retries - 1:
                sleep_time = 3 + (attempt * 2)
                time.sleep(sleep_time)
    return False

async def generate_voiceover(text, voice, output_path):
    import edge_tts
    print(f"[*] Synthesizing voiceover (+20% speed) for: '{text}'")
    try:
        communicate = edge_tts.Communicate(text, voice, rate="+20%")
        await communicate.save(output_path)
        print(f"[+] Saved voiceover to {output_path}")
        return True
    except Exception as e:
        print(f"[!] Edge-TTS error: {e}")
        return False

def draw_subtitles(frame, text, font_size=28):
    img = Image.fromarray(frame)
    draw = ImageDraw.Draw(img)
    width, height = img.size
    
    font = None
    system_fonts = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Verdana.ttf",
        "/System/Library/Fonts/Supplemental/Georgia.ttf",
        "arial.ttf"
    ]
    for sys_font in system_fonts:
        try:
            font = ImageFont.truetype(sys_font, font_size)
            break
        except:
            continue
    if not font:
        font = ImageFont.load_default()
        
    max_w = int(width * 0.8)
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = " ".join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if (bbox[2] - bbox[0]) <= max_w:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))
        
    line_w_h = []
    total_h = 0
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        line_w_h.append((w, h))
        total_h += h + 6
    total_h -= 6
    
    pad_x, pad_y = 24, 14
    box_w = max(w for w, h in line_w_h) + 2 * pad_x
    box_h = total_h + 2 * pad_y
    
    box_x = (width - box_w) // 2
    box_y = int(height * 0.80) - box_h // 2
    
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rounded_rectangle(
        [box_x, box_y, box_x + box_w, box_y + box_h],
        radius=12,
        fill=(0, 0, 0, 150)
    )
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(img)
    
    curr_y = box_y + pad_y
    for i, line in enumerate(lines):
        w, h = line_w_h[i]
        tx = box_x + pad_x + (max(lw for lw, lh in line_w_h) - w) // 2
        draw.text(
            (tx, curr_y), line, font=font,
            fill=(255, 255, 255, 255),
            stroke_width=2, stroke_fill=(0, 0, 0, 255)
        )
        curr_y += h + 6
        
    return np.array(img.convert("RGB"))

def zoom_and_pan(clip, zoom_ratio=0.08, pan_x=40, pan_y=20):
    def _apply(get_frame, t):
        img = Image.fromarray(get_frame(t))
        w, h = img.size
        
        scale = 1.0 + (zoom_ratio * t)
        new_w, new_h = math.ceil(w * scale), math.ceil(h * scale)
        
        new_w += new_w % 2
        new_h += new_h % 2
        
        img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        duration = clip.duration if clip.duration and clip.duration > 0 else 5.0
        ratio = min(t / duration, 1.0)
        dx = int(pan_x * (ratio - 0.5))
        dy = int(pan_y * (ratio - 0.5))
        
        x_center = (new_w - w) // 2
        y_center = (new_h - h) // 2
        
        x = max(0, min(x_center + dx, new_w - w))
        y = max(0, min(y_center + dy, new_h - h))
        
        return np.array(img.crop((x, y, x + w, y + h)))
        
    return clip.transform(_apply)

def download_music(url, output_path):
    print(f"[*] Downloading background music from: {url}")
    try:
        res = requests.get(url, timeout=30)
        if res.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(res.content)
            return True
    except Exception as e:
        print(f"[!] Music download error: {e}")
    return False

def build_video(segments, voice_paths, image_paths, music_path, output_path, skip_music=False):
    clips = []
    for i, seg in enumerate(segments):
        audio = AudioFileClip(voice_paths[i])
        
        img_clip = ImageClip(image_paths[i]).with_duration(audio.duration)
        animated = zoom_and_pan(img_clip)
        subtitled = animated.transform(lambda gf, t: draw_subtitles(gf(t), seg["text"]))
        
        clips.append(subtitled.with_audio(audio))
        
    print("[*] Assembling video track...")
    video = concatenate_videoclips(clips, method="compose")
    
    if not skip_music and os.path.exists(music_path):
        try:
            print("[*] Mixing background music track...")
            bg = AudioFileClip(music_path).subclipped(0, video.duration).with_volume_scaled(0.15)
            video = video.with_audio(CompositeAudioClip([video.audio, bg]))
        except Exception as e:
            print(f"[!] Music mixing issue: {e}. Defaulting to voiceover only.")
            
    print(f"[*] Encoding final video (Length: {video.duration:.2f}s)...")
    video.write_videofile(
        output_path, fps=24, codec="libx264", audio_codec="aac",
        temp_audiofile="temp-audio.m4a", remove_temp=True
    )

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fighter", type=str, default="Subhas Chandra Bose")
    parser.add_argument("--output", type=str, default="freedom_fighter.mp4")
    parser.add_argument("--voice", type=str, default="en-IN-NeerjaNeural")
    parser.add_argument("--no-music", action="store_true")
    parser.add_argument("--music-url", type=str, default="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
    parser.add_argument("--creds", type=str, default=None)
    parser.add_argument("--api-key", type=str, default=None)
    args = parser.parse_args()
    
    temp_dir = os.path.join(os.getcwd(), "temp_assets")
    os.makedirs(temp_dir, exist_ok=True)
    
    print(f"[+] Target Freedom Fighter: {args.fighter}")
    script_data = get_script(args.fighter, args.api_key, args.creds)
    segments = script_data["segments"]
    
    img_paths, voice_paths = [], []
    for i, seg in enumerate(segments):
        img_path = os.path.join(temp_dir, f"image_{i+1}.png")
        if download_image(seg["image_prompt"], img_path, seed=i*123+45):
            img_paths.append(img_path)
        else:
            print("[!] Critical error downloading image segment. Exiting.")
            sys.exit(1)
            
        voice_path = os.path.join(temp_dir, f"voiceover_{i+1}.mp3")
        if asyncio.run(generate_voiceover(seg["text"], args.voice, voice_path)):
            voice_paths.append(voice_path)
        else:
            print("[!] Critical error synthesizing audio segment. Exiting.")
            sys.exit(1)
            
    music_path = os.path.join(temp_dir, "background_music.mp3")
    skip_music = args.no_music
    if not skip_music and not os.path.exists(music_path):
        if not download_music(args.music_url, music_path):
            print("[!] Background music download failed. Continuing without music.")
            skip_music = True
            
    build_video(segments, voice_paths, img_paths, music_path, args.output, skip_music)
    print(f"\n[+] SUCCESS: Video generated at '{args.output}'\n")

if __name__ == "__main__":
    main()
