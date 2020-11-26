import configparser
import io
import re
from PIL import Image, ImageDraw, ImageFont


def render(file_name, out):
    s_config = open("digicamvalues2.ini", "r").read().encode().decode("utf-8-sig")

    buf = io.StringIO(s_config)
    config = configparser.ConfigParser()
    config.read_file(buf)

    # Python's ConfigParser takes strings specified with quotes literally.
    # Before any usage, we want to find values matching this criteria
    # and proactively strip quotes.
    for section in config.sections():
        for key, value in config.items(section):
            config[section][key] = value.strip('"')

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
                page_info[f"Layer{page_object}"].replace("Object", "").split(",")[0]
            )

            object_section = config[f"Page{page_num}Object{layer_name}"]
            object_type = int(object_section["ObjectType"])

            # Object is a JPEG.
            if object_type == 1:
                zoom = float(object_section["Zoom"]) * 0.01
                rect_used = object_section["RectUsed"].split(",")
                center_point_x, center_point_y = object_section["CenterPoint"].split(
                    ","
                )

                frame_width = int(object_section["EffectFrameWidth"])
                frame_height = int(object_section["EffectFrameHeight"])

                picture = Image.open(file_name, "r")
                picture_width, picture_height = picture.size

                picture_resized = picture.resize(
                    (int(picture_width * zoom), int(picture_height * zoom))
                )

                mask_im = Image.new(mode="RGB", size=(frame_width, frame_height))
                mask_im.paste(picture_resized, (int(float(rect_used[0]) / 2) * -1, int(float(rect_used[1]) / 2) * -1))

                img.paste(
                    mask_im,
                    (
                        int(center_point_x) - int(frame_width / 2),
                        int(center_point_y) - int(frame_height / 2),
                    ),
                )

            # Object is text.
            elif object_type == 2:
                font_r, font_g, font_b = object_section["FontColor"].split(",")
                start_position_x, start_position_y = object_section[
                    "StartPosition"
                ].split(",")

                character_width = int(float(object_section["Ch_Width_Size"]))
                character_height = int(float(object_section["Ch_Height_Size"]))
                text = " ".join(object_section["Text"].split())

                # When possible, we want to localize.
                if text == "W i i 番 号":
                    text = "Wii Number:"

                try:
                    number = int(text.replace(" ", ""))
                    if len(str(number)) == 16:
                        text = " ".join(re.findall("....", text.replace(" ", "")))
                    if start_position_x == 358:
                        start_position_x = 585
                except ValueError:
                    pass

                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype("FOT-RodinNTLGPro-DB.otf", character_height)

                draw.text(
                    (int(start_position_x), int(start_position_y)),
                    text,
                    (int(font_r), int(font_g), int(font_b)),
                    font,
                )

            # Object is a background.
            elif object_type == 4:
                bg_frame_id = object_section["BGFrameID"].replace(".bmp", ".png")

                background = Image.open(bg_frame_id, "r")
                img.paste(background, (0, 0), background)

            img.save(out.format(page_num.zfill(2)))


# TODO: REMOVE
render("1.jpg", "Page{}.png")
