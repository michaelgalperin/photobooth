from PIL import Image, ImageDraw, ImageFont
from random import choice
import warnings
warnings.filterwarnings('ignore', message='textsize is deprecated and will be removed in Pillow 10')


colors = [
    (255, 255, 0), # yellow
    (0, 0, 255), # blue
    (255, 127, 17), # orange
    (93, 217, 193), # teal
    (86, 130, 89), # forest green
    # (204, 252, 203), # mint green
    (56, 97, 140), # dark blue
    (200, 29, 37), # red
]

make_color = lambda : choice(colors)

font_header = ImageFont.truetype('static/superscript.ttf', size=110)
font_footer = ImageFont.truetype('static/zx-spectrum.ttf', size=40)

maya = Image.open('static/maya.png').resize((160,160), Image.Resampling.BOX)

def make_header(text="Maya's Party!", font=font_header, image_size=(5000, 500)):
    image = Image.new("RGBA", image_size, (0,0,0,0)) # scrap image
    draw = ImageDraw.Draw(image)
    image2 = Image.new("RGBA", image_size, (0,0,0,0)) # final image

    fill = " o "
    x = 0
    w_fill, y = draw.textsize(fill, font=font)
    x_draw, x_paste = 0, 0

    for c in text:
        w_full = draw.textsize(fill+c, font=font)[0]
        w = w_full - w_fill     # the width of the character on its own
        draw.text((x_draw, 0), fill+c, make_color(), font=font)
        iletter = image.crop((x_draw+w_fill, -30, x_draw+w_full, y+30))
        image2.paste(iletter, (x_paste, 0))
        x_draw += w_full
        x_paste += w
    image_box = image2.getbbox()
    image2 = image2.crop(image_box)
    return image2


def make_footer(text="february 18, 2023", fill=(0,0,0), font=font_footer, image_size=(5000, 200)):
    image = Image.new("RGBA", image_size, (0,0,0,0)) # scrap image
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, fill=fill, font=font)
    image_box = image.getbbox()
    image = image.crop(image_box)
    return image

def make_booth_text(resize=1):
    image = Image.new("RGBA", (1200, 1200))
    header = make_header()
    footer = make_footer()
    image.paste(maya, ((image.size[0] - maya.size[0]) // 2, 0), maya)
    image.paste(footer, ((image.size[0] - footer.size[0]) // 2, maya.size[1] + header.size[1] - 8), footer)
    image.paste(header, ((image.size[0] - header.size[0]) // 2, maya.size[1] - 10), header)
    image_box = image.getbbox()
    image = image.crop(image_box)
    image = image.resize((int(image.size[0] * resize), int(image.size[1] * resize)), Image.Resampling.BOX)
    return image


if __name__ == "__main__":
    make_booth_text().show()