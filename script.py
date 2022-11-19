import json
import os
import shutil
import sys
from subprocess import PIPE, run
from uuid import UUID

if os.name == "nt":
    import ctypes
    from ctypes import windll, wintypes
    from uuid import UUID

    # ctypes GUID copied from MSDN sample code
    class GUID(ctypes.Structure):
        _fields_ = [
            ("Data1", wintypes.DWORD),
            ("Data2", wintypes.WORD),
            ("Data3", wintypes.WORD),
            ("Data4", wintypes.BYTE * 8),
        ]

        def __init__(self, uuidstr):
            uuid = UUID(uuidstr)
            ctypes.Structure.__init__(self)
            (
                self.Data1,
                self.Data2,
                self.Data3,
                self.Data4[0],
                self.Data4[1],
                rest,
            ) = uuid.fields
            for i in range(2, 8):
                self.Data4[i] = rest >> (8 - i - 1) * 8 & 0xFF

    SHGetKnownFolderPath = windll.shell32.SHGetKnownFolderPath
    SHGetKnownFolderPath.argtypes = [
        ctypes.POINTER(GUID),
        wintypes.DWORD,
        wintypes.HANDLE,
        ctypes.POINTER(ctypes.c_wchar_p),
    ]

    def _get_known_folder_path(uuidstr):
        pathptr = ctypes.c_wchar_p()
        guid = GUID(uuidstr)
        if SHGetKnownFolderPath(ctypes.byref(guid), 0, 0, ctypes.byref(pathptr)):
            raise ctypes.WinError()
        return pathptr.value

    FOLDERID_Download = "{374DE290-123F-4565-9164-39C4925E467B}"

    def get_download_folder():
        return _get_known_folder_path(FOLDERID_Download)

else:

    def get_download_folder():
        home = os.path.expanduser("~")
        return os.path.join(home, "Downloads")


def find_all_files(source):
    paths = []
    dir_paths = []
    for (root, dirs, files) in os.walk(source):
        for file in files:
            path = os.path.join(root, file)

        for directory in dirs:
            dir_path = os.path.join(root, directory)
            dir_paths.append(dir_paths)
    return dir_paths


def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def get_directory_from_directory_path(source, paths):
    source_list = source.split(os.sep)
    for path in paths:
        path_list = path.split(os.sep)
        path_list = path_list[len(source_list)]
        path = os.path.join(path_list)
        print(path)


def main(source):
    pass


if __name__ == "__main__":
    source = get_download_folder()
    dir_paths = find_all_files(source)
    get_directory_from_directory_path(source, dir_paths)
