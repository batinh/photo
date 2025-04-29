from PIL import Image
from rembg import remove

# Đường dẫn ảnh
overlay_path = "../data/background.jpeg"
background_path = "../data/IMG_6467.jpeg"

# Mở ảnh và xử lý
overlay_img = Image.open(overlay_path).convert("RGBA")
overlay_no_bg = remove(overlay_img)

# Resize overlay (có thể thay đổi tùy ý)
overlay_resized = overlay_no_bg.resize((600, 200))

# Mở ảnh nền
background_img = Image.open(background_path).convert("RGBA")
bg_width, bg_height = background_img.size
ov_width, ov_height = overlay_resized.size

# Vị trí chèn: góc phải trên (có chừa lề 30px)
position = (bg_width - ov_width - 30, 30)

# Chèn ảnh
background_img.paste(overlay_resized, position, overlay_resized)

# Lưu kết quả
background_img.save("../data/result_overlay.png")
print("✅ Đã lưu ảnh kết quả vào result_overlay.png")
