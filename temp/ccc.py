import cv2
import pandas as pd

# 加载数据
data = {
    "level": [5, 5, 5, 5],
    "page_num": [1, 1, 1, 1],
    "block_num": [1, 1, 1, 1],
    "par_num": [1, 1, 1, 1],
    "line_num": [1, 1, 1, 1],
    "word_num": [1, 2, 3, 4],
    "left": [25, 171, 300, 402],
    "top": [27, 28, 40, 40],
    "width": [126, 109, 84, 95],
    "height": [45, 43, 31, 44],
    "conf": [95.780014, 95.782608, 95.782608, 96.361763],
    "text": ["hello", "how", "are", "you"],
}

df = pd.DataFrame(data)

# 打开图像
image_path = "asset/origin/how_are_you.png"  # 修改为你的图片路径
img = cv2.imread(image_path)

# 在图像上画出每个词的矩形框
for index, row in df.iterrows():
    left, top, width, height = row["left"], row["top"], row["width"], row["height"]
    cv2.rectangle(img, (left, top), (left + width, top + height), (0, 255, 0), 2)

# 显示图像
cv2.imshow("Text Detection", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 如果需要保存结果图像
# cv2.imwrite('path_to_save_image.jpg', img)
