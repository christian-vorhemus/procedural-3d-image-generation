import os
import string
import random
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

# 40% will be damaged, 60% okay
damaged_intact_ratio = 0.4
# Specify the number of images you want to create. Depending on your computer, one image pair can take between 2 and 6 minutes to render
num_images = 100
# Specify the absolute path where you want to store the created images
file_base_path = "/path/to/folder"

# ------------- Pipeline start -------------

if not os.path.exists(os.path.join(file_base_path, "damaged")):
    new_dir = os.path.join(file_base_path, "damaged")
    os.makedirs(new_dir)
    print(f"Created directory {new_dir}")

if not os.path.exists(os.path.join(file_base_path, "intact")):
    new_dir = os.path.join(file_base_path, "intact")
    os.makedirs(new_dir)
    print(f"Created directory {new_dir}")

for i in range(0, num_images):
    img = Image.open("./Template.png")
    draw = ImageDraw.Draw(img)

    serial_number = "0" + str(random.randint(100000000000, 999999999999))
    batch_number = ''.join(random.choices(string.ascii_uppercase, k=2)) + str(random.randint(100000, 999999)) + "-" + str(random.randint(0, 9)) + ''.join(random.choices(string.ascii_uppercase, k=1))

    font = ImageFont.truetype("./BellGothicStd-Bold.otf", 28)

    draw.text((1060, 130), f"SN:              {serial_number}", (0,0,0), font=font)
    draw.text((1060, 170), f"Ch.-B.:         {batch_number}", (0,0,0), font=font)
    draw.text((1060, 210), f"Verw.bis:     12.2082", (0,0,0), font=font)

    img.save('./Wrapping.png')

    coinflip = random.uniform(0, 1)

    if coinflip < damaged_intact_ratio:
        os.system(f"blender Package.blend --python blenderBackgroundTask.py -- damaged {serial_number} {file_base_path}")
    else:
        os.system(f"blender Package.blend --python blenderBackgroundTask.py -- intact {serial_number} {file_base_path}")