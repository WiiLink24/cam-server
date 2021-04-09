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


def parse_coords(coordinates: str) -> (int, int):
    x, y = coordinates.split(",")
    return int(x), int(y)


def parse_rgb(color: str) -> (int, int, int):
    r, g, b = color.split(",")
    return int(r), int(g), int(b)


def render(order_schema: str, order_id: str):
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

    # This field can contain "255,255,255" or a filename for a template.
    background_filename = page_info["BackGroundFileName"]
    if "," not in background_filename:
        # White ("255,255,255") is the only color sent by the client.
        background_color = (255, 255, 255)
    else:
        # If we're not given a color, default to black.
        background_color = (0, 0, 0)

    # This image represents one for the entire page.
    print_size_width = int(page_info["PrintSizeWidth"])
    print_size_height = int(page_info["PrintSizeHeight"])
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

    # Within PageXXInfo, we're given a format similar to 'Layer01="Object01,1"'.
    # This would presumably state a layer order with a respective object and object type.
    # However, item type 1 (a business card) lacks this layer information for seemingly no reason.
    #
    # Historically, we iterated through all of these to determine the order.
    # As the client ensures layers are the same index as objects, we will just loop.
    page_objects_count = int(page_info["PageObjectsCount"])
    for object_num in range(1, page_objects_count + 1):
        # Pad to two zeros where possible.
        object_num = f"{object_num:02}"

        object_section = config[f"Page{padded_page_num}Object{object_num}"]
        object_type = ObjectTypes(object_section["ObjectType"])

        # Object is a JPEG.
        if object_type == ObjectTypes.IMAGE:
            zoom = float(object_section["Zoom"]) * 0.01
            rect_used = object_section["RectUsed"].split(",")
            center_point_x, center_point_y = parse_coords(object_section["CenterPoint"])

            frame_width = int(object_section["EffectFrameWidth"])
            frame_height = int(object_section["EffectFrameHeight"])

            object_file_name = secure_filename(object_section["FileName"])
            object_file_path = determine_path(order_id, object_file_name)
            picture = Image.open(object_file_path, "r")
            picture_width, picture_height = picture.size

            # Resize the image with our specified zoom.
            picture_resized = picture.resize(
                (int(picture_width * zoom), int(picture_height * zoom))
            )

            # Create a mask with the client's specified background color.
            mask_im = Image.new(
                mode="RGB",
                size=(int(picture_width * zoom), frame_height),
                color=background_color,
            )

            # Paste our resized image within the mask.
            rect_x, rect_y = rect_used[0], rect_used[1]
            mask_im.paste(
                picture_resized,
                (
                    int(int(rect_x) * (zoom * -1)),
                    int(int(rect_y) * (zoom * -1)),
                ),
            )

            # Paste centered within our directed frame location.
            page_img.paste(
                mask_im,
                (
                    center_point_x - (frame_width // 2),
                    center_point_y - (frame_height // 2),
                ),
            )

        # Object is text.
        elif object_type == ObjectTypes.TEXT:
            font_r, font_g, font_b = parse_rgb(object_section["FontColor"])
            start_position_x, start_position_y = parse_coords(
                object_section["StartPosition"]
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
                    # Remove extra spaces
                    text = " ".join(re.findall("....", text.replace(" ", "")))
                if start_position_x == 358:
                    start_position_x = 585
                elif start_position_x == 388:
                    start_position_x = 715
            except ValueError:
                pass

            draw = ImageDraw.Draw(page_img)
            font = ImageFont.truetype(
                "assets/fonts/FOT-RodinNTLGPro-DB.otf", character_height
            )

            draw.text(
                (start_position_x, start_position_y),
                text,
                (font_r, font_g, font_b),
                font,
            )

        # Object is a background.
        elif object_type == ObjectTypes.BACKGROUND:
            bg_frame_id = "assets/templates/{}".format(
                object_section["BGFrameID"].replace(".bmp", ".png")
            )

            background = Image.open(bg_frame_id, "r").convert("RGBA")
            page_img.paste(background, (0, 0), background)

    page_filename = f"Page {page_num}.jpg"
    page_save_path = determine_path(order_id, page_filename)

    page_img.convert("RGB")
    page_img.save(f"{page_save_path}", optimize=True)
    print(f"Processed {page_filename}")
