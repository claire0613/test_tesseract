import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import pytesseract
from googletrans import Translator, LANGUAGES
import time

font_path = "NotoSansTC-Regular.ttf"  # 請確保這個路徑是正確的


def get_target_language():
    print("可用的目標語言:")
    for code, name in LANGUAGES.items():
        print(f"{code}: {name}")

    while True:
        target_lang = (
            input("請輸入目標語言代碼（例如：'zh-tw' 表示繁體中文）: ").strip().lower()
        )
        if target_lang in LANGUAGES:
            print(f"您選擇的目標語言是：{LANGUAGES[target_lang]}")
            return target_lang
        else:
            print("無效的語言代碼，請重新輸入。")


def preprocess_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return img, binary


def detect_text_regions(binary):
    # 使用形態學操作來合併相鄰的文本區域
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 3))
    dilated = cv2.dilate(binary, kernel, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 過濾和合併文本區域
    regions = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w > 20 and h > 8:  # 過濾掉太小的區域
            regions.append((x, y, w, h))

    return merge_nearby_regions(regions)


def merge_nearby_regions(regions, distance_threshold=10):
    merged = []
    for region in regions:
        if not merged:
            merged.append(region)
        else:
            merged_region = merge_if_close(region, merged[-1], distance_threshold)
            if merged_region:
                merged[-1] = merged_region
            else:
                merged.append(region)
    return merged


def merge_if_close(region1, region2, distance_threshold):
    x1, y1, w1, h1 = region1
    x2, y2, w2, h2 = region2
    if abs(y1 - y2) < distance_threshold and (x1 <= x2 + w2 and x2 <= x1 + w1):
        return (
            min(x1, x2),
            min(y1, y2),
            max(x1 + w1, x2 + w2) - min(x1, x2),
            max(y1 + h1, y2 + h2) - min(y1, y2),
        )
    return None


def extract_text(img, region):
    x, y, w, h = region
    roi = img[y : y + h, x : x + w]
    start_time = time.time()
    text = pytesseract.image_to_data(roi, lang="eng+chi_sim")
    end_time = time.time()
    print("total time:", end_time - start_time)
    return text.strip()


def translate_text(text, target_lang):
    translator = Translator()
    return translator.translate(text, dest=target_lang).text


def draw_translated_text(image, region, original_text, translated_text, font_path):
    draw = ImageDraw.Draw(image)
    x, y, w, h = region
    font_size = 20
    font = ImageFont.truetype(font_path, size=font_size)

    while True:
        text_bbox = draw.textbbox((0, 0), translated_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        if text_width <= w * 0.9 and text_height <= h * 0.9:
            break
        font_size -= 1
        font = ImageFont.truetype(font_path, size=font_size)

    overlay = Image.new("RGBA", (w, h), (255, 255, 255, 180))
    image.paste(overlay, (x, y), overlay)

    text_x = x + (w - text_width) / 2
    text_y = y + (h - text_height) / 2
    draw.text((text_x, text_y), translated_text, font=font, fill=(0, 0, 0, 255))


def process_image(image_path, target_lang, output_path):
    img, binary = preprocess_image(image_path)
    regions = detect_text_regions(binary)
    image = Image.open(image_path)

    for region in regions:
        original_text = extract_text(img, region)
        if original_text:
            translated_text = translate_text(original_text, target_lang)
            draw_translated_text(
                image, region, original_text, translated_text, font_path
            )

    image.save(output_path)
    print(f"翻譯後的圖片已保存為 {output_path}")


def main():
    asset_path = "asset/origin"
    translated_path = "asset/translated_file"

    if not os.path.exists(translated_path):
        os.makedirs(translated_path)

    target_lang = get_target_language()

    for filename in os.listdir(asset_path):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
            input_path = os.path.join(asset_path, filename)
            output_filename = f"{os.path.splitext(filename)[0]}_translated_{target_lang}{os.path.splitext(filename)[1]}"
            output_path = os.path.join(translated_path, output_filename)

            try:
                process_image(input_path, target_lang, output_path)
                if os.path.exists(output_path):
                    print(
                        f"輸出文件成功創建，大小：{os.path.getsize(output_path)} 字節"
                    )
                else:
                    print(f"警告：{output_path} 未能成功創建")
            except Exception as e:
                print(f"處理 {filename} 時發生錯誤：{str(e)}")


if __name__ == "__main__":
    main()
