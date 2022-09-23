import os
import sys
from datetime import datetime
import gphoto2 as gp


class Camera:
    def strip_filename(self, name):
        return int(name[1:-4])

    def create_filename(self, num):
        return f"P{num}.JPG"

    def get_current_fileno_from_folder(self, folder):
        files = [f[0] for f in self.cam.folder_list_files(folder)]
        return self.strip_filename(max(files))

    def __init__(self):
        print("INIT CAMERA...")
        self.cam = gp.Camera()
        self.cam.init()
        ## cam capture is not working right now
        ## so do this with filesystem
        fp = self.cam.capture(gp.GP_CAPTURE_IMAGE)
        self.folder = fp.folder
        self.current_fileno = self.strip_filename(fp.name)
        print("DONE")
        print(self.folder, self.current_fileno, file=sys.stderr)
        # self.folder = '/store_00010001/DCIM/116_PANA'
        # self.current_fileno = self.get_current_fileno_from_folder(self.folder)

    def trigger_capture(self):
        self.cam.trigger_capture()
        self.current_fileno += 1

    def capture(self):
        print(datetime.now().strftime("%H:%M:%S"), file=sys.stderr)
        fp = self.cam.capture(gp.GP_CAPTURE_IMAGE)
        print(datetime.now().strftime("%H:%M:%S"), file=sys.stderr)
        self.current_fileno = self.strip_filename(fp.name)
        print(f"fileno: {self.current_fileno}")

    def download_image(self, num, target):
        name = self.create_filename(num)
        print("file number:", num, "name:", name, file=sys.stderr)
        file = self.cam.file_get(self.folder, name, gp.GP_FILE_TYPE_NORMAL)
        file.save(target)

    def download_images(self, images, target_dir):
        for i, num in enumerate(images):
            self.download_image(num, os.path.join(target_dir, f"{i}.jpg"))

    def download_n_most_recent_images(self, target_dir, n=4):
        for i in range(n):
            # download oldest first
            j = n - i - 1
            print(target_dir, file=sys.stderr)
            self.download_image(
                self.current_fileno - j, os.path.join(target_dir, f"{i}.jpg")
            )
