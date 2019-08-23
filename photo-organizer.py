import os
import shutil
from datetime import datetime
from PIL import Image

class PhotoOrganizer:
    extensions = ['jpg', 'jpeg', 'JPG', 'JPEG']

    @staticmethod
    def folder_path_from_photo_date(file):
        date = PhotoOrganizer.photo_shooting_date(file)
        return date.strftime('%Y') + '/' + date.strftime('%Y-%m-%d')

    @staticmethod
    def photo_shooting_date(file):
        photo = Image.open(file)
        info = photo._getexif()
        date = datetime.fromtimestamp(os.path.getmtime(file))
        if info:
            if 36867 in info:
                date = info[36867]
                date = datetime.strptime(date, '%Y:%m:%d %H:%M:%S')
        return date

    @staticmethod
    def move_photo(file):
        new_folder = PhotoOrganizer.folder_path_from_photo_date(file)
        if not os.path.exists(new_folder):
            os.makedirs(new_folder)
        shutil.move(file, new_folder + '/' + file)

    @staticmethod
    def organize():
        PhotoOrganizer.create_extensions_to_organize()
        
        photos = [
            filename for filename in os.listdir('.') if any(filename.endswith(ext) for ext in PhotoOrganizer.extensions)
        ]
        for filename in photos:
            PhotoOrganizer.move_photo(filename)

    @staticmethod
    def create_extensions_to_organize():
        if (not os.path.isfile("extensions.txt")):
            f = open("extensions.txt", "w+")
            f.write("jpg\njpeg\nJPG\nJPEG")
            f.close()

        PhotoOrganizer.get_extensions_to_organize()

    @staticmethod
    def get_extensions_to_organize():
        f=open("extensions.txt", "r")
        f1 = f.readlines()

        PhotoOrganizer.extensions.clear()

        for line in f1:
            PhotoOrganizer.extensions.append(line.strip())


if __name__ == "__main__":
    PhotoOrganizer().organize()