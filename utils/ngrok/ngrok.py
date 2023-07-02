import os,time,re
import subprocess


DIR = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.append(DIR)


def run_cmd(cmd):
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

def main():
    try:
        os.remove('ngrok_log')
    except:
        pass

    # try:
    #     os.remove(r'C:\Users\JGarza\Google Drive\TBP_link.txt')
    #     os.remove(r'C:\Users\JGarza\Google Drive\TBP_link.md')
    # except:
    #     pass
    
    x = run_cmd(r'.\utils\ngrok\ngrok http 8800 --log=ngrok_log')
    time.sleep(5)

    nlog = ''
    with open('ngrok_log','r') as file:
        nlog = file.read()
    
    link = ''
    link = re.findall('https:.*\.app\n',nlog)[0]
    link = link.replace('\n','')
    
    with open(r'C:\Users\JGarza\Google Drive\temp\TBP_link.txt','w') as file:
        file.write(
            f'''{link}
user: guest@nothing.com
password: JustAGuest
            ''')
        # file.write(f'{link}')


if __name__ == "__main__":
    main()
