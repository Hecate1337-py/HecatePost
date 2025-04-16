import os
import requests
import json
from dotenv import load_dotenv, set_key

# === SETUP ===
ENV_FILE = ".env"
load_dotenv()

def save_to_env(key, value):
    if not os.path.exists(ENV_FILE):
        with open(ENV_FILE, 'w') as f:
            f.write('')
    set_key(ENV_FILE, key, value)

def get_long_lived_user_token(app_id, app_secret, short_lived_token):
    print("\n[1] Menukar token pendek ke token panjang...")
    url = 'https://graph.facebook.com/v22.0/oauth/access_token'
    params = {
        'grant_type': 'fb_exchange_token',
        'client_id': app_id,
        'client_secret': app_secret,
        'fb_exchange_token': short_lived_token
    }
    response = requests.get(url, params=params)
    data = response.json()

    if 'access_token' in data:
        token = data['access_token']
        print("✅ Token panjang:\n", token)
        save_to_env("LONG_LIVED_USER_TOKEN", token)
        return token
    else:
        print("❌ Gagal:", data)
        return None

def save_pages_to_json(pages):
    with open("pages.json", "w", encoding="utf-8") as f:
        json.dump(pages, f, indent=2, ensure_ascii=False)
    print("💾 Token halaman disimpan di pages.json")

def get_page_access_tokens(long_lived_user_token):
    print("\n[2] Mengambil token halaman...")
    url = 'https://graph.facebook.com/v22.0/me/accounts'
    params = { 'access_token': long_lived_user_token }
    response = requests.get(url, params=params)
    data = response.json()

    if 'data' in data and data['data']:
        print("\n✅ Token Halaman:")
        for i, page in enumerate(data['data'], 1):
            print(f"{i}. {page['name']} ({page['id']})")
            save_to_env(f"PAGE_NAME_{i}", page['name'])
            save_to_env(f"PAGE_ID_{i}", page['id'])
            save_to_env(f"PAGE_ACCESS_TOKEN_{i}", page['access_token'])
        save_pages_to_json(data['data'])
        return data['data']
    else:
        print("❌ Tidak ada halaman ditemukan.")
        return []

# === POSTING SECTION ===
IMAGES_FOLDER = os.getenv("IMAGES_FOLDER", "images")
VIDEOS_FOLDER = os.getenv("VIDEOS_FOLDER", "vid/shorts")
CAPTIONS_FILE = os.getenv("CAPTIONS_FILE", "link.txt")

HASHTAGS = "#fyp #fypindonesia #facebookreels #memes #aiart #wallpaper #sunset #explorepage"

def load_posted(file_path):
    if not os.path.exists(file_path):
        return set()
    with open(file_path, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f)

def save_posted(file_path, filename):
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"{filename}\n")

def is_already_posted(posted, name): return name in posted

def read_captions():
    try:
        with open(CAPTIONS_FILE, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return []

def post_image(page_id, token, file_path, caption, posted_file):
    print(f"🖼️ Upload gambar: {file_path}")
    url = f"https://graph.facebook.com/{page_id}/photos"
    with open(file_path, 'rb') as img:
        files = {'source': img}
        data = {'caption': caption, 'access_token': token}
        res = requests.post(url, files=files, data=data).json()
    if 'id' in res:
        print("✅ Gambar berhasil:", res['id'])
        save_posted(posted_file, os.path.basename(file_path))
    else:
        print("❌ Gagal:", res)

def post_video(page_id, token, file_path, caption, posted_file):
    print(f"🎥 Upload video: {file_path}")
    url = f"https://graph.facebook.com/{page_id}/videos"
    with open(file_path, 'rb') as vid:
        files = {'source': vid}
        data = {'description': caption, 'access_token': token}
        res = requests.post(url, files=files, data=data).json()
    if 'id' in res:
        print("✅ Video berhasil:", res['id'])
        save_posted(posted_file, os.path.basename(file_path))
        os.remove(file_path)
    else:
        print("❌ Gagal:", res)

def load_page_tokens():
    pages = []
    i = 1
    while True:
        page_id = os.getenv(f"PAGE_ID_{i}")
        token = os.getenv(f"PAGE_ACCESS_TOKEN_{i}")
        if not page_id or not token: break
        pages.append({'index': i, 'page_id': page_id, 'token': token})
        i += 1
    return pages

def select_pages(pages):
    print("\n📃 Pilih halaman:")
    for p in pages:
        print(f"{p['index']}. {p['page_id']}")
    pilihan = input("Pilih (1/2/3 atau 'all'): ").strip().lower()
    if pilihan == 'all': return pages
    idx = [int(x) for x in pilihan.split(",") if x.isdigit()]
    return [p for p in pages if p['index'] in idx]

def select_mode():
    print("\n📁 Pilih konten:")
    print("1. Gambar")
    print("2. Video")
    print("3. Gambar + Video")
    return input("Pilih (1/2/3): ").strip()

def run_posting():
    pages = load_page_tokens()
    if not pages:
        print("❌ Tidak ada halaman ditemukan.")
        return

    selected_pages = select_pages(pages)
    mode = select_mode()
    captions = read_captions()

    for page in selected_pages:
        pid = page['page_id']
        token = page['token']
        posted_img = f"posted_images_{pid}.txt"
        posted_vid = f"posted_videos_{pid}.txt"

        if mode in ["1", "3"]:
            posted = load_posted(posted_img)
            images = sorted([
                os.path.join(IMAGES_FOLDER, f)
                for f in os.listdir(IMAGES_FOLDER)
                if f.lower().endswith(('.jpg', '.jpeg', '.png'))
            ])
            for idx, img in enumerate(images):
                if is_already_posted(posted, os.path.basename(img)): continue
                caption = f"{captions[idx] if idx < len(captions) else ''}\n\n{HASHTAGS}"
                post_image(pid, token, img, caption, posted_img)
                break

        if mode in ["2", "3"]:
            posted = load_posted(posted_vid)
            videos = sorted([
                os.path.join(VIDEOS_FOLDER, f)
                for f in os.listdir(VIDEOS_FOLDER)
                if f.lower().endswith(('.mp4', '.mov', '.avi'))
            ])
            for vid in videos:
                if is_already_posted(posted, os.path.basename(vid)): continue
                title = os.path.splitext(os.path.basename(vid))[0].replace("_", " ")
                caption = f"🎬 {title}\n\n{HASHTAGS}"
                post_video(pid, token, vid, caption, posted_vid)
                break

# === MENU AWAL ===
def main():
    print("=== HECATE FACEBOOK MANAGER ===")
    print("1. Setup APP & Token")
    print("2. Post Gambar/Video")
    pilihan = input("Pilih menu (1/2): ").strip()
    if pilihan == "1":
        app_id = input("APP ID: ").strip()
        app_secret = input("APP SECRET: ").strip()
        short_token = input("Token Pendek: ").strip()
        save_to_env("APP_ID", app_id)
        save_to_env("APP_SECRET", app_secret)
        save_to_env("SHORT_LIVED_USER_TOKEN", short_token)
        user_token = get_long_lived_user_token(app_id, app_secret, short_token)
        if user_token:
            get_page_access_tokens(user_token)
    elif pilihan == "2":
        run_posting()
    else:
        print("❌ Menu tidak valid.")

if __name__ == "__main__":
    main()