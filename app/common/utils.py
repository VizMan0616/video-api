import os
import os.path as path
from flask import current_app


def create_user_folder(channel_name):
    os.mkdir(f'{current_app.root_path}\\static\\videos\\{channel_name}')
    os.mkdir(f'{current_app.root_path}\\static\\pfp\\{channel_name}')


def save_video(channel_folder, name, file):
    _, f_ext = path.splitext(file.filename)
    resulting_file = name + f_ext
    file.save(
        f'{current_app.root_path}\\static\\videos\\{channel_folder}\\{resulting_file}')


def delete_video(channel_folder, filename):
    os.remove(
        f'{current_app.root_path}\\static\\videos\\{channel_folder}\\{filename}.mp4')


def rename_video(channel_folder, old_name, new_name):
    os.rename(f'{current_app.root_path}\\static\\videos\\{channel_folder}\\{old_name}.mp4',
              f'{current_app.root_path}\\static\\videos\\{channel_folder}\\{new_name}.mp4')
