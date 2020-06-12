import os
from os.path import getsize, join
from datetime import datetime
from pathlib import Path

from django.shortcuts import render

DIRECTORY = Path("media")


# Create your views here.
def view_directories(request):
    directories = os.scandir(DIRECTORY)
    folders = []
    files = []

    for dir in directories:
        if dir.is_dir():
            file_info = {"name": dir.name,
                         "path": dir.path,
                         "last_modified": datetime.utcfromtimestamp(dir.stat().st_mtime).strftime('%Y-%m-%d'),
                         "size": bytes_to(os.path.getsize(dir.path), 'm')}
            folders.append(file_info)

        if dir.is_file():
            files.append(dir.name)
    return render(request, 'filesystem/index.html', {'folders': folders, 'files':files})


def bytes_to(bytes, to, bsize=1024):
    a = {'k': 1, 'm': 2, 'g': 3, 't': 4, 'p': 5, 'e': 6}
    r = float(bytes)
    for i in range(a[to]):
        r = r / bsize
    return (r)


def open_directory(request, name):
    directory = name.replace('-', '\\')
    # directory = name

    directories = os.scandir(directory)

    folders = []
    files = []

    for dir in directories:
        if dir.is_dir():
            file_info = {"name": dir.name,
                         "path": dir.path,
                         "last_modified": datetime.utcfromtimestamp(dir.stat().st_mtime).strftime('%Y-%m-%d'),
                         "size": bytes_to(os.path.getsize(dir.path), 'm')}
            folders.append(file_info)

        if dir.is_file():
            file_info = {"name": dir.name,
                         "path": dir.path,
                         "last_modified": datetime.utcfromtimestamp(dir.stat().st_mtime).strftime('%Y-%m-%d'),
                         "size": bytes_to(os.path.getsize(dir.path), 'm')}
            files.append(file_info)

    return render(request, 'filesystem/directory.html', {'folders': folders, 'files': files})
