import configparser
import enum
import io
import re
from PIL import Image, ImageDraw, ImageFont
from werkzeug.utils import secure_filename

from routes.get_image_id import determine_path


class ObjectTypes(enum.Enum):
    IMAGE = "1"
    TEXT = "2"
    # 3 goes unused.
    BACKGROUND = "4"


def render(order_schema: str, order_id: str, out="todo-remove/"):
    s_config = order_schema.encode().decode("utf-8-sig")

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
    service_type = int(base_info["ServiceType"])

    service_types = {1: "Notebook", 2: "Photo Book", 3: "Business Card"}

    print("Print Type: {}\n".format(service_types[service_type]))

    # We're often given multiple pages.
    # Iterate through all.
    for page_num in range(1, page_count + 1):
        handle_page(page_num, config, order_id)


def handle_page(page_num: int, config: configparser.ConfigParser, order_id: str):
    padded_page_num = f"{page_num:02}"
    page_info = config[f"Page{padded_page_num}Info"]

    page_objects_count = int(page_info["PageObjectsCount"])
    print_size_width = int(page_info["PrintSizeWidth"])
    print_size_height = int(page_info["PrintSizeHeight"])

    # This field can contain "255,255,255" or a filename for a template.
    background_filename = page_info["BackGroundFileName"]
    if "," not in background_filename:
        # Black ("255,255,255,") is the only color sent by the client.
        background_color = (255, 255, 255)
    else:
        # If we're not given a color, default to black.
        background_color = (0, 0, 0)

    # This image represents one for the entire page.
    page_img = Image.new(
        mode="RGB",
        size=(print_size_width, print_size_height),
        color=background_color,
    )

    # If we were given a true filename, paste it over our background.
    if ".bmp" in background_filename:
        bg_frame_id = "assets/templates/{}".format(
            background_filename.replace(".bmp", ".png")
        )

        background = Image.open(bg_frame_id, "r").convert("RGBA")
        page_img.paste(background, (0, 0), background)

    for object_num in range(1, page_objects_count + 1):
        # Pad to two zeros where possible.
        object_num = f"{object_num:02}"

        layer_name = page_info[f"Layer{object_num}"].replace("Object", "").split(",")[0]

        object_section = config[f"Page{padded_page_num}Object{layer_name}"]
        object_type = ObjectTypes(object_section["ObjectType"])

        # Object is a JPEG.
        if object_type == ObjectTypes.IMAGE:
            zoom = float(object_section["Zoom"]) * 0.01
            rect_used = object_section["RectUsed"].split(",")
            center_point_x, center_point_y = object_section["CenterPoint"].split(",")

            frame_width = int(object_section["EffectFrameWidth"])
            frame_height = int(object_section["EffectFrameHeight"])

            object_file_name = secure_filename(object_section["FileName"])
            object_file_path = determine_path(order_id, object_file_name)
            picture = Image.open(object_file_path, "r")
            picture_width, picture_height = picture.size

            picture_resized = picture.resize(
                (int(picture_width * zoom), int(picture_height * zoom))
            )

            mask_im = Image.new(
                mode="RGB",
                size=(int(picture_width * zoom), frame_height),
                color=background_color,
            )
            mask_im.paste(
                picture_resized,
                (
                    int(int(rect_used[0]) * (zoom * -1)),
                    int(int(rect_used[1]) * (zoom * -1)),
                ),
            )

            page_img.paste(
                mask_im,
                (
                    int(center_point_x) - int(int(picture_width * zoom) / 2),
                    int(center_point_y) - int(frame_height / 2),
                ),
            )

        # Object is text.
        elif object_type == ObjectTypes.TEXT:
            font_r, font_g, font_b = object_section["FontColor"].split(",")
            start_position_x, start_position_y = object_section["StartPosition"].split(
                ","
            )

            character_width = int(float(object_section["Ch_Width_Size"]))
            character_height = int(float(object_section["Ch_Height_Size"]))
            text = " ".join(object_section["Text"].split())

            # When possible, we want to localize.
            if text == "W i i 番 号":
                text = "Wii Number:"
            elif text == "電話番号":
                text = "Phone Number:"

            try:
                number = int(text.replace(" ", ""))
                if len(str(number)) == 16:
                    text = " ".join(
                        re.findall("....", text.replace(" ", ""))
                    )  # remove extra spaces
                if start_position_x == "358":
                    start_position_x = "585"
                elif start_position_x == "388":
                    start_position_x = "715"
            except ValueError:
                pass

            draw = ImageDraw.Draw(page_img)
            font = ImageFont.truetype(
                "assets/fonts/FOT-RodinNTLGPro-DB.otf", character_height
            )

            draw.text(
                (int(start_position_x), int(start_position_y)),
                text,
                (int(font_r), int(font_g), int(font_b)),
                font,
            )

        # Object is a background.
        elif object_type == ObjectTypes.BACKGROUND:
            bg_frame_id = "assets/templates/{}".format(
                object_section["BGFrameID"].replace(".bmp", ".png")
            )

            background = Image.open(bg_frame_id, "r").convert("RGBA")
            page_img.paste(background, (0, 0), background)

    page_filename = f"Page {page_num}.png"
    page_save_path = determine_path(order_id, page_filename)

    page_img = page_img.quantize(method=2)
    page_img.save(f"{page_save_path}", optimize=True)
    print(f"Processed {page_filename}")
