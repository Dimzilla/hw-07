import os
from pathlib import Path
from shutil import move
from zipfile import ZipFile
from sys import argv
from glob import glob


main_path = Path(r"d:\Разобрать")

"""Tansliteration"""


def normalize(transliteration):
    cyrillic_ua = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    latin = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u", "f",
             "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

    latter_dict = {}
    for c, l in zip(cyrillic_ua, latin):
        latter_dict[ord(c)] = l
        latter_dict[ord(c.upper())] = l.upper()

    translated = transliteration.translate(latter_dict)
    word_check = (f"")
    for char in translated:
        if char.isdigit() or char.isalpha():
            word_check += char
        else:
            word_check += "_"

    return word_check


'''Unpacking archives'''


def unarchive(folder_path):
    try:
        for archive in os.listdir(fr"{ folder_path }\\archives_file"):
            os.mkdir(
                fr"{folder_path}\archives_file\{os.path.splitext(archive)[0]}")
            extract_dir = fr"{folder_path}\archives_file\{os.path.splitext(archive)[0]}"
            with ZipFile(fr"{folder_path}\archives_file\{archive}") as arch:
                arch.extractall(extract_dir)

            def renamed(dirpath, names, encoding):
                new_names = [old.encode('cp437').decode(encoding)
                             for old in names]
                for old, new in zip(names, new_names):
                    os.rename(os.path.join(dirpath, old),
                              os.path.join(dirpath, normalize(os.path.splitext(new)[0]) + os.path.splitext(new)[1]))
                return new_names

            encoding = 'cp866'
            os.chdir(extract_dir)
            for dirpath, dirs, files in os.walk(os.curdir, topdown=True):
                renamed(dirpath, files, encoding)
                dirs[:] = renamed(dirpath, dirs, encoding)
    except FileNotFoundError:
        print(f"archives_file[zip,gz,tar] not found")


"""Key for check files"""
extensions = {
    "images_file": [".jpeg", ".png", ".jpg", ".svg"],
    "video_file": [".avi", ".mp4", ".mov", ".mkv"],
    "document_file": [".doc", ".docs", ".txt", ".pdf", ".xlsx", ".pptx"],
    "audio_file": [".mp3", ".ogg", ".wav", ".amr"],
    "archives_file": [".zip", ".gz", ".tar"],
    "unknown_extensions_file": [None]
}

"""Creates folders and sort file"""


def create_folders_from_list(folder_path, folder_names):
    for folder in folder_names:
        if not os.path.exists(f"{folder_path}\\{folder}"):
            os.mkdir(f"{folder_path}\\{folder}")


def get_subfolder_paths(folder_path) -> list:
    subfolder_paths = [f.path for f in os.scandir(folder_path) if f.is_dir()]

    return subfolder_paths


def get_file_paths(folder_path) -> list:
    file_paths = [f.path for f in os.scandir(folder_path) if not f.is_dir()]

    return file_paths


def sort_files(folder_path):
    file_paths = get_file_paths(folder_path)
    ext_list = list(extensions.items())

    for file_path in file_paths:
        extension = os.path.splitext(file_path)[1]
        file_name = file_path.split("\\")[-1].split(".")[0]
        file_name = normalize(file_name)

        for dict_key_int in range(len(ext_list)):

            if extension in ext_list[dict_key_int][1]:

                print(
                    f"Moving {file_name} in {ext_list[dict_key_int][0]} folder\n")
                os.rename(
                    file_path, f"{main_path}\\{ext_list[dict_key_int][0]}\\{file_name}{extension}")


def remove_empty_folders(folder_path):
    subfolder_paths = get_subfolder_paths(folder_path)

    for p in subfolder_paths:
        if not os.listdir(p):
            print("Deleting empty folder:", p.split("\\")[-1], "\n")
            os.rmdir(p)


if __name__ == "__main__":
    create_folders_from_list(main_path, extensions)
    sort_files(main_path)
    remove_empty_folders(main_path)
    unarchive(main_path)
