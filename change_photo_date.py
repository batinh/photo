import os
import sys
import piexif
import subprocess
from datetime import datetime

def change_exif_and_creation_date(directory, new_date_str):
    new_date_exif = new_date_str.encode("utf-8")
    new_date_mac = datetime.strptime(new_date_str, "%Y:%m:%d %H:%M:%S").strftime("%m/%d/%Y %H:%M:%S")
    modified_files = 0

    for filename in os.listdir(directory):
        if filename.lower().endswith((".jpg", ".jpeg")):
            file_path = os.path.join(directory, filename)
            try:
                # 1. Update EXIF
                exif_dict = piexif.load(file_path)
                for tag in ['0th', 'Exif']:
                    for exif_tag in piexif.TAGS[tag]:
                        name = piexif.TAGS[tag][exif_tag]["name"]
                        if name in ["DateTimeOriginal", "DateTimeDigitized", "DateTime"]:
                            exif_dict[tag][exif_tag] = new_date_exif
                exif_bytes = piexif.dump(exif_dict)
                piexif.insert(exif_bytes, file_path)

                # 2. Update file creation date using SetFile (macOS only)
                subprocess.run(["SetFile", "-d", new_date_mac, file_path], check=True)

                print(f"[OK] {filename} updated.")
                modified_files += 1
            except Exception as e:
                print(f"[ERR] Failed on {filename}: {e}")

    print(f"\n✅ Done. Modified {modified_files} file(s).")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python change_photo_date_mac.py <directory> <new_date>")
        print("Date format: 'YYYY:MM:DD HH:MM:SS'")
        sys.exit(1)

    dir_path = sys.argv[1]
    new_date = sys.argv[2]

    change_exif_and_creation_date(dir_path, new_date)
