from PIL import Image
from PIL.ImageFile import ImageFile
from googletrans import Translator, LANGUAGES
import os
import pytesseract
import cv2
import pandas as pd
import time
from datetime import datetime

img = Image.open("asset/origin/how_are_you.png")
img.save("t.png")


def record_time(file_name, total_time):
    with open("total.txt", "a") as f:
        f.write(f"Use {file_name} by tesseract: {total_time} \n")


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


def draw_rectangle(data, image_path, filename, output_path="asset/detection"):
    df = pd.DataFrame(data)

    # 打开图像
    img = cv2.imread(image_path)

    # 过滤置信度低的识别结果
    df = df[df["conf"] > 70]  # 只绘制置信度高于80的结果
    # 在图像上画出每个词的矩形框
    for index, row in df.iterrows():

        left, top, width, height = row["left"], row["top"], row["width"], row["height"]
        cv2.rectangle(img, (left, top), (left + width, top + height), (0, 255, 0), 2)

    output_path = os.path.join(output_path, filename)
    # 保存图像到磁盘
    cv2.imwrite(output_path, img)

    print(f"Image saved to {output_path}")


def translate_text(text, target_lang):
    translator = Translator()
    return translator.translate(text, dest=target_lang).text


def image_to_data(image_path, filename, output_path="asset/tsv"):

    image: ImageFile = Image.open(image_path)
    start_time = time.time()
    tsv_output = pytesseract.image_to_data(
        image,
        output_type=pytesseract.Output.DATAFRAME,
        lang="eng+chi_sim+fra",
        config="--psm 6",
    )
    end_time = time.time()

    record_time(filename, end_time - start_time)

    output_path = os.path.join(output_path, filename[:-4])

    tsv_output.to_csv(f"{output_path}.tsv", sep="\t", index=False)
    return tsv_output


def process_image(image_path, target_lang, output_path, filename):
    tsv_output = image_to_data(image_path, filename)
    translate_text(tsv_output, target_lang)
    draw_rectangle(tsv_output, image_path, filename)

    print(f"翻譯後的圖片已保存為 {output_path}")


def main():
    with open("total.txt", "a") as f:
        now = datetime.now()
        f.write(f"{now} =============== \n")

    asset_path = "asset/origin"
    translated_path = "asset/translated_file"
    asset_blur = "asset/origin/blur"

    if not os.path.exists(translated_path):
        os.makedirs(translated_path)

    # target_lang = get_target_language()

    for filename in os.listdir(asset_path):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
            target_lang = "zh-tw"
            input_path = os.path.join(asset_path, filename)
            output_filename = f"{os.path.splitext(filename)[0]}_translated_{target_lang}{os.path.splitext(filename)[1]}"
            output_path = os.path.join(translated_path, output_filename)

            try:
                process_image(input_path, target_lang, output_path, filename)

            except Exception as e:
                print(f"處理 {filename} 時發生錯誤：{str(e)}")

    for filename in os.listdir(asset_blur):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
            target_lang = "zh-tw"

            input_path = os.path.join(asset_blur, filename)
            output_filename = f"{os.path.splitext(filename)[0]}_translated_{target_lang}{os.path.splitext(filename)[1]}"
            output_path = os.path.join(translated_path, output_filename)

            try:
                process_image(input_path, target_lang, output_path, filename)

            except Exception as e:
                print(f"處理 {filename} 時發生錯誤：{str(e)}")

    with open("total.txt", "a") as f:
        f.write("==============================")


if __name__ == "__main__":

    main()
