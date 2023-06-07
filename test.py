
import os
from werkzeug.security import generate_password_hash, check_password_hash

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


# def get_hs_password(password):
#     return generate_password_hash(
#         'default',
#         method='pbkdf2:sha256',
#         salt_length=8
#     )


if __name__ == "__main__":
    # print(*get_files(root=r'\\Theblackpearl\d\Torrents\Movies'),sep='\n')

    password = 'default'
    hspw = generate_password_hash(
        password,
        method='pbkdf2:sha256',
        salt_length=8
        )
    print(password)
    print(hspw)


    check = check_password_hash(hspw, password)
    print(check)

