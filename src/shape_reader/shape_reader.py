import os
import re
import shutil

from src.shape_reader.read_exceptions import FileIsNotArchive, FilesAreCorrelating, ThereIsNoShapeFiles


class ShapeReader:
    @staticmethod
    def read(filepath):
        try:
            directory_name = os.path.dirname(filepath)
            shutil.unpack_archive(filepath, directory_name)
        except Exception as e:
            raise FileIsNotArchive()
        os.remove(filepath)
        content = os.listdir(directory_name)
        for file in content:
            ShapeReader.read_directories(os.path.join(directory_name, file), directory_name)
        shape_files = list(filter(
            lambda file_name: re.match(r'.*?\.shp$', file_name, re.IGNORECASE), os.listdir(directory_name)
        ))
        if len(shape_files) == 0:
            raise ThereIsNoShapeFiles()
        return list(map(lambda file_name: os.path.join(directory_name, file_name), shape_files))

    @staticmethod
    def read_directories(filepath, extract_directory):
        if os.path.isdir(filepath):
            content = os.listdir(filepath)
            for file in content:
                ShapeReader.read_directories(os.path.join(filepath, file), extract_directory)
        else:
            if os.path.samefile(os.path.dirname(filepath), extract_directory):
                return
            result_file = os.path.join(extract_directory, os.path.basename(filepath))
            if os.path.exists(result_file):
                raise FilesAreCorrelating()
            shutil.move(filepath, result_file)
