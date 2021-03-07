import os

from util.config_extension import ConfigExtension

class FileExtension:  
  base_path = ConfigExtension.get('PATH')['posts_finished_report_path']

  @staticmethod
  def create_file(filename: str, text: str):
    with open(FileExtension.base_path + filename, 'w+') as f:
      return f.write(text)

  @staticmethod
  def append_to_file(filename: str, text: str):
    with open(FileExtension.base_path + filename, 'a+') as f:
      return f.write(text)

  @staticmethod
  def read_lines_all_files_on_folder(folder: str):
    files_lines = []

    for filename in os.listdir(FileExtension.base_path + folder):
      with open(f'{FileExtension.base_path}{folder}\\{filename}') as file:
        for line in file:
          files_lines.append(line.replace('\n', ''))

    return files_lines