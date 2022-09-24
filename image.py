import os
from PIL import Image

from .ig import upload

BOOTH_TEXT = Image.open("text.png")


class Booth:
    RESAMPLE = Image.Resampling.LANCZOS

    def __init__(
        self, image_dir, image_size=(750, 500), square_size=1080, top_margin=50
    ):
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
        half = Image.new("RGBA", (self.image_size[0] * 2, self.image_size[1] * 2))
        half.paste(self.resized[0], (0, 0))
        half.paste(self.resized[1], (self.image_size[0], 0))
        half.paste(self.resized[2], (0, self.image_size[1]))
        half.paste(self.resized[3], (self.image_size[0], self.image_size[1]))
        half.paste(
            BOOTH_TEXT,
            (
                (half.size[0] - BOOTH_TEXT.size[0]) // 2,
                (half.size[1] - BOOTH_TEXT.size[1]) // 2,
            ),
            BOOTH_TEXT,
        )
        half.save(os.path.join(self.image_dir, "booth.png"))
        full = Image.new("RGBA", (half.size[0], half.size[1] * 2 + self.top_margin * 2))
        full.paste(half, (0, 0))
        full.paste(half, (0, half.size[1] + self.top_margin))
        self.full_path = os.path.join(self.image_dir, "full.png")
        full.save(self.full_path)

    def print(self, path):
        os.system(f'lpr -o PageSize="5x7.Fullbleed" -o InputSlot=rear {path}')

    def run(self):
        self.resize_images()
        self.assemble()
        self.print(self.full_path)
        self.square_images()
        self.upload_images()
