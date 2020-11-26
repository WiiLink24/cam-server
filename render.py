import configparser
import io
import re
from PIL import Image, ImageDraw, ImageFont


def render(file_name,out):
    s_config = open("digicamvalues.ini", "r").read().encode().decode("utf-8-sig")

    buf = io.StringIO(s_config)
    config = configparser.ConfigParser()
    config.read_file(buf)

    base_info = config["BaseInfo"]
    page_count = int(base_info["PageCount"])

    for i in range(1, page_count + 1):
        i = str(i).zfill(2)

        page_info = config["Page{}Info".format(i)]
        page_objects_count = int(page_info["PageObjectsCount"])
        print_size_width = int(page_info["PrintSizeWidth"])
        print_size_height = int(page_info["PrintSizeHeight"])

        img = Image.new(mode="RGB", size=(print_size_width, print_size_height))

        for j in range(1, page_objects_count + 1):
            j = str(j).zfill(2)

            layer_name = (
                page_info["Layer{}".format(j)]
                .replace('"', "")
                .replace("Object", "")
                .split(",")[0]
            )
            object_section = config[
                "Page{}Object{}".format(str(i).zfill(2), layer_name)
            ]
            object_type = int(object_section["ObjectType"])

            zoom = float(object_section["Zoom"]) / 100

            rect_used = object_section["RectUsed"].replace('"', "").split(",")

            frame_width = int(object_section["EffectFrameWidth"])
            frame_height = int(object_section["EffectFrameHeight"])

            picture = Image.open(file_name, "r")
            picture_width, picture_height = picture.size

            picture_resized = picture.resize((frame_width, int(picture_height / (picture_width / frame_width))))

            mask_im = Image.new(mode="RGB", size=(frame_width, frame_height))
            mask_im.paste(picture_resized, (0, 0))

            img.paste(mask_im, (center_point_x - int(frame_width / 2), center_point_y - int(frame_height / 2)))

        elif object_type == 2:
            font_color = object_section["FontColor"].replace('"', "").split(",")
            start_position = object_section["StartPosition"].replace('"', "").split(",")
            start_position_x = int(start_position[0])
            start_position_y = int(start_position[1])
            character_width = int(float(object_section["Ch_Width_Size"].replace('"', "")))
            character_height = int(float(object_section["Ch_Height_Size"].replace('"', "")))    
            text = object_section["Text"].replace('"', "")

            if text == "W" + (" " * 35) + "i" + (" " * 17) + "i" + (" " * 46) + "番" + (" " * 50) + "号":
                text = "Wii Number:"

            try:
                number = int(text.replace(" ", ""))
                if len(str(number)) == 16:
                    text = " ".join(re.findall('....', text.replace(" ", "")))
                if start_position_x == 358:
                    start_position_x = 585
            except ValueError:
                pass

            elif object_type == 2:
                font_color = object_section["FontColor"].replace('"', "").split(",")
                start_position = (
                    object_section["StartPosition"].replace('"', "").split(",")
                )
                start_position_x = int(start_position[0])
                start_position_y = int(start_position[1])
                character_width = int(
                    float(object_section["Ch_Width_Size"].replace('"', ""))
                )
                character_height = int(
                    float(object_section["Ch_Height_Size"].replace('"', ""))
                )
                text = " ".join(object_section["Text"].replace('"', "").split())

                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype("FOT-RodinNTLGPro-DB.otf", character_height)

                draw.text(
                    (start_position_x, start_position_y),
                    text,
                    (int(font_color[0]), int(font_color[1]), int(font_color[2])),
                    font,
                )

            elif object_type == 4:
                bg_frame_id = (
                    object_section["BGFrameID"].replace('"', "").replace(".bmp", ".jpg")
                )

                background = Image.open(bg_frame_id, "r")
                img.paste(background, (0, 0), background)

            img.save(out.format(i))
