from PIL import Image, ImageDraw, ImageFont

# 打開原始圖片
image = Image.open("/Users/claireliang/Desktop/how_are_you.png")

# 準備要繪製的文本
with open("translated_text.txt", "r") as file:
    translated_text = file.read()
    print(translated_text)

# 創建繪圖對象
draw = ImageDraw.Draw(image)

# 設置字體和大小
font = ImageFont.truetype("Arial.ttf", size=20)  # 你可能需要指定一個有效的字體文件

# 在圖片上寫入文本
draw.text(
    (10, 10), translated_text, font=font, fill="black"
)  # (10, 10) 是文本的位置，"black" 是顏色

# 保存圖片
image.save("translated_image.png")
