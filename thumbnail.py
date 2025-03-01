import os
from PIL import Image

# 원본 이미지가 있는 폴더
input_folder = "images/"
output_folder = "thumbnails/"
size = (200, 200)

# 출력 폴더가 없으면 생성
os.makedirs(output_folder, exist_ok=True)

# 폴더 내 모든 이미지 처리
for filename in os.listdir(input_folder):
    if filename.endswith((".jpg", ".png", ".jpeg")):
        img_path = os.path.join(input_folder, filename)
        img = Image.open(img_path)
        img.thumbnail(size)
        img.save(os.path.join(output_folder, filename))
        print(f"Thumbnail saved: {filename}")

print("All thumbnails created successfully!")
