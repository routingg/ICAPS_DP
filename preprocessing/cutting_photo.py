from pathlib import Path
from PIL import Image, ImageOps, ImageColor

# ===== 기본 설정 =====
INPUT_DIR = Path("./our_story")        # 원본 이미지 폴더
OUTPUT_DIR = Path("./fulls_fixed")     # 결과 저장 폴더
SIZE = (1600, 900)                     # 목표 크기 (가로 x 세로)
MODE = "contain"                       # "cover" 또는 "contain"
BG_COLOR = ImageColor.getrgb("#000000")  # contain 모드 배경색
QUALITY = 92                           # JPEG/WebP 퀄리티
OUTPUT_EXT = ".jpg"                    # 저장 확장자 (".jpg", ".png", ".webp" 가능)

def process_image(src_path: Path, dst_path: Path):
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(src_path) as im:
        im = ImageOps.exif_transpose(im)

        if MODE == "cover":
            thumb = ImageOps.fit(im, SIZE, method=Image.LANCZOS, centering=(0.5, 0.5))
        elif MODE == "contain":
            thumb = im.copy()
            thumb.thumbnail(SIZE, Image.LANCZOS)
            canvas = Image.new("RGB", SIZE, BG_COLOR)
            x = (SIZE[0] - thumb.size[0]) // 2
            y = (SIZE[1] - thumb.size[1]) // 2
            canvas.paste(thumb, (x, y))
            thumb = canvas
        else:
            raise ValueError("MODE must be 'cover' or 'contain'")

        # 저장
        if OUTPUT_EXT.lower() in (".jpg", ".jpeg"):
            thumb = thumb.convert("RGB")
            thumb.save(dst_path, format="JPEG", quality=QUALITY, optimize=True, progressive=True)
        elif OUTPUT_EXT.lower() == ".webp":
            thumb.save(dst_path, format="WEBP", quality=QUALITY, method=6)
        else:
            thumb.save(dst_path, format="PNG", optimize=True)

def main():
    if not INPUT_DIR.exists():
        print(f"❌ Input folder not found: {INPUT_DIR}")
        return

    patterns = ["*.jpg", "*.jpeg", "*.png", "*.webp", "*.bmp"]
    files = []
    for pat in patterns:
        files.extend(INPUT_DIR.glob(pat))

    files = sorted(files)  # 정렬 (이름순)

    if not files:
        print("⚠️ No images found in input folder.")
        return

    for idx, src in enumerate(files, start=1):
        filename = f"{idx:03d}{OUTPUT_EXT}"  # 001, 002, 003 …
        dst = OUTPUT_DIR / filename
        try:
            process_image(src, dst)
            print(f"[OK] {src} -> {dst}")
        except Exception as e:
            print(f"[ERR] {src}: {e}")

if __name__ == "__main__":
    main()
