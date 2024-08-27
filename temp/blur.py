import cv2
import os

asset_path = "asset/origin"
blur_path = "asset/origin/blur"


def apply_blur_and_save(kernel_size):

    for filename in os.listdir(asset_path):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
            input_path = os.path.join(asset_path, filename)
            output_filename = f"{os.path.splitext(filename)[0]}_blur_{kernel_size}{os.path.splitext(filename)[1]}"
            output_path = os.path.join(blur_path, output_filename)

        img = cv2.imread(input_path)

        blurred_img = cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

        cv2.imwrite(output_path, blurred_img)


apply_blur_and_save(5)
apply_blur_and_save(3)
