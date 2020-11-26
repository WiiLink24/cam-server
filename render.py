import configparser
import io
import re
from PIL import Image, ImageDraw, ImageFont


def render(file_name, out):
    s_config = open("digicamvalues.ini", "r").read().encode().decode("utf-8-sig")

    buf = io.StringIO(s_config)
    config = configparser.ConfigParser()
    config.read_file(buf)

    base_info = config["BaseInfo"]
    page_count = int(base_info["PageCount"])

    for page_num in range(1, page_count + 1):
        page_num = f"{page_num:02}"

        page_info = config[f"Page{page_num}Info"]
        page_objects_count = int(page_info["PageObjectsCount"])
        print_size_width = int(page_info["PrintSizeWidth"])
        print_size_height = int(page_info["PrintSizeHeight"])

        img = Image.new(mode="RGB", size=(print_size_width, print_size_height))

        for page_object in range(1, page_objects_count + 1):
            # Pad to two zeros where possible.
            page_object = f"{page_object:02}"

            layer_name = (
                page_info[f"Layer{page_object}"]
                .replace('"', "")
                .replace("Object", "")
                .split(",")[0]
            )
            object_section = config[f"Page{page_num}Object{layer_name}"]
            object_type = int(object_section["ObjectType"])

            zoom = float(object_section["Zoom"]) / 100

            rect_used = object_section["RectUsed"].replace('"', "").split(",")

            frame_width = int(object_section["EffectFrameWidth"])
            frame_height = int(object_section["EffectFrameHeight"])

            picture = Image.open(file_name, "r")
            picture_width, picture_height = picture.size

            picture_resized = picture.resize(
                (frame_width, int(picture_height / (picture_width / frame_width)))
            )

            mask_im = Image.new(mode="RGB", size=(frame_width, frame_height))
            mask_im.paste(picture_resized, (0, 0))

            img.paste(
                mask_im,
                (
                    center_point_x - int(frame_width / 2),
                    center_point_y - int(frame_height / 2),
                ),
            )

            # Object is a JPEG.
            if object_type == 1:
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
                text = object_section["Text"].replace('"', "")

                # When possible, we want to localize.
                if original_wii_number_text(text):
                    text = "Wii Number:"

                try:
                    number = int(text.replace(" ", ""))
                    if len(str(number)) == 16:
                        text = " ".join(re.findall("....", text.replace(" ", "")))
                    if start_position_x == 358:
                        start_position_x = 585
                except ValueError:
                    pass

            # Object is text.
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

            # Object is a background.
            elif object_type == 4:
                bg_frame_id = (
                    object_section["BGFrameID"].replace('"', "").replace(".bmp", ".jpg")
                )

                background = Image.open(bg_frame_id, "r")
                img.paste(background, (0, 0), background)

            img.save(out.format(page_num))


# Best seen as "Wii番号" with odd spacing.
def original_wii_number_text(text) -> bool:
    regex = re.compile("W\s{35}i\s{17}i\s{46}番\s{50}号")
    return regex.match(text) is not None

