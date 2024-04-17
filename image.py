import os
from PIL import Image

from .ig import upload

## To create a dynamic image overlay, modify banner.py
## to your liking, then uncomment this and the make_booth_text
## call in Booth.assemble
# from .banner import make_booth_text

## To use a static image overlay, change this path
BOOTH_TEXT = Image.open("static/jenna_dave_overlay.png")

print_booth = False



def paste_with_alpha(bg, fg):
    """returns new image with fg pasted onto bg in center"""
    # assumes fg is smaller than bg
    fg2 = Image.new("RGBA", bg.size)
    fg2.paste(
        fg,
        (
            (fg2.size[0] - fg.size[0]) // 2,
            (fg2.size[1] - fg.size[1]) // 2,
        ),
        fg,
    )
    return Image.alpha_composite(bg, fg2)


class Booth:
    RESAMPLE = Image.Resampling.LANCZOS

    def __init__(
        self, image_dir, image_size=(750, 500), square_size=1080, top_margin=50
    ):
        """
        image_dir: directory in which to save and load images
        image_size: size in pixels of each of the four images to be printed
        square_size: size in pixels of images to
        top_margin: margin in pixels between half-sheets and at the bottom of the page

        """
        self.image_dir = image_dir
        self.image_size = image_size
        self.square_size = square_size
        self.top_margin = top_margin
        image_paths = [os.path.join(image_dir, "raw", f"{i}.jpg") for i in range(4)]
        self.images = [Image.open(p) for p in image_paths]
        self.square

    def resize_images(self):
        self.resized = [im.resize(self.image_size, self.RESAMPLE) for im in self.images]
        os.makedirs(os.path.join(self.image_dir, "resized"), exist_ok=True)
        for i, im in enumerate(self.resized):
            im.save(os.path.join(self.image_dir, "resized", f"{i}.jpg"))

    def square(self, im, size):
        """
        im: Image
        size: size in pixels of final image.
            Only resizes to this size, does not crop beyond squaring off.
        """
        # assume landscape
        margin = (im.size[0] - im.size[1]) // 2
        box = (margin, 0, im.size[0] - margin, im.size[1])
        im = im.crop(box)
        return im.resize((size, size), self.RESAMPLE)

    def square_images(self):
        self.squared = [self.square(im, self.square_size) for im in self.images]
        os.makedirs(os.path.join(self.image_dir, "square"), exist_ok=True)
        self.square_paths = []
        for i, im in enumerate(self.squared):
            path = os.path.join(self.image_dir, "square", f"{i}.jpg")
            im.save(path)
            self.square_paths.append(path)

    def upload_images(self):
        upload(self.square_paths)

    def assemble(self):
        ## To create a dynamic image overlay, uncomment this and
        ## make your own modifications to banner.py
        # BOOTH_TEXT = make_booth_text()

        # Add all images to half sheet
        half = Image.new("RGBA", (self.image_size[0] * 2, self.image_size[1] * 2))
        half.paste(self.resized[0], (0, 0))
        half.paste(self.resized[1], (self.image_size[0], 0))
        half.paste(self.resized[2], (0, self.image_size[1]))
        half.paste(self.resized[3], (self.image_size[0], self.image_size[1]))
        # add overlay and save
        half = paste_with_alpha(half, BOOTH_TEXT)
        half.save(os.path.join(self.image_dir, "booth.png"))
        # half sheet -> full sheet
        # changing the top margin options and image positioning may
        # result in a better print
        full = Image.new("RGBA", (half.size[0], half.size[1] * 2 + self.top_margin * 2))
        full.paste(half, (0, 0))
        full.paste(half, (0, half.size[1] + self.top_margin))
        self.full_path = os.path.abspath(os.path.join(self.image_dir, "full.png"))
        full.save(self.full_path)

    def print(self, path):
        ## Print {path} on 5x7 paper with full bleed, from rear input slot
        if print_booth:
            print(path)
            os.system(f'lpr -P "HP_ColorLaserJet_M255_M256" -o media=Custom.5x7in {path}')

    def run(self):
        self.resize_images()
        self.assemble()
        self.print(self.full_path)
        self.square_images()
        self.upload_images()
