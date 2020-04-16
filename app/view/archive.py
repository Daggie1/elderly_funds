from django.shortcuts import render


def get_archives(request):
    # show all files
    # search form for a file
    return render(request, 'archive/index.html')

def open_file(request):
    # get a file and its content
    return render(request, 'archive/file.html')