
import os


def get_files(root:str='D:\\',extensions:list=[]) -> list:
    result = []
    for path, directories, files in os.walk(root):
        for file in files:
            for e in extensions:
                if file.endswith(e):
                    result.append({
                        'fullpath': os.path.join(path, file),
                        'file': file
                    })
                continue
    return result



if __name__ == "__main__":
    print(*get_files(root=r'\\Theblackpearl\d\Torrents\Movies'),sep='\n')