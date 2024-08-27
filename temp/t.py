from PIL import Image, ImageEnhance, ImageFilter


def preprocess_image(image_path):
    img = Image.open(image_path)

    # 调整亮度和对比度
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2)  # 对比度加强

    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.2)  # 亮度增强

    # 应用滤波去噪
    img = img.filter(ImageFilter.MedianFilter(size=1))

    # 应用锐化
    img = img.filter(ImageFilter.SHARPEN)

    # 转换为灰度图像后二值化
    img = img.convert("L")
    img = img.point(lambda x: 0 if x < 128 else 255, "1")

    img.save("processed_image.png")
    return "processed_image.png"


# # 调用函数处理图像
preprocessed_image_path = preprocess_image("asset/origin/test_table.png")


# import pytesseract
# from PIL import Image
# import pandas as pd

# # 加载图像
# img = Image.open('asset/origin/test_table.png')

# # 使用 pytesseract 获取文本的详细数据
# data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DATAFRAME)

# # 过滤掉识别为空的结果
# data = data[data.conf != -1]

# # 排序和合并文本
# sorted_data = data.sort_values(by=['top', 'left'])
# current_top = sorted_data.iloc[0]['top']
# lines = []
# line = []

# for index, row in sorted_data.iterrows():
#     if abs(row['top'] - current_top) > 10:  # 根据实际情况调整行间距阈值
#         lines.append(' '.join(line))
#         line = []
#         current_top = row['top']
#     line.append(row['text'])

# if line:
#     lines.append(' '.join(line))

# # 翻译每一行
# from googletrans import Translator
# translator = Translator()
# translations = [translator.translate(line, src='en', dest='zh-tw').text for line in lines]

# # 打印原文和翻译
# for original, translation in zip(lines, translations):
#     print(f"原文: {original}\n翻译: {translation}\n" + '-'*50)


# from PIL import Image
# import pytesseract
# from googletrans import Translator

# # 设定Tesseract的路径，如果已经配置好环境变量则无需此步骤
# # pytesseract.pytesseract.tesseract_cmd = r'你的Tesseract路径'

# # 打开图像
# image_path = "processed_image.png"
# image = Image.open(image_path)

# # 使用Tesseract OCR提取文本
# text = pytesseract.image_to_string(image, lang="eng")

# # 打印提取的英文文本
# print("提取的英文文本:")
# print(text)

# # 使用Google翻译API进行翻译
# translator = Translator()
# translated = translator.translate(text, src="en", dest="zh-cn")

# # 打印翻译后的中文文本
# print("翻译后的中文文本:")
# print(translated.text)
