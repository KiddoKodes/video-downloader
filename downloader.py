import os
from socket import gaierror
from pip._vendor import requests
import sys, math, youtube_dl


if not os.path.exists('output'):
    os.makedirs('output')
def KeyBoardInterrupt(revizit):
        confirm = input("[?] Do you want to exit the program [Y/N]: ")
        if(confirm == "y" or confirm == "Y" or confirm == "Yes" or confirm == "yes"):
            sys.exit()
        else:
            revizit
def direct_download(url, filename):
    try:
        with open(os.path.join('output', filename), 'wb') as f:
            try:
                response = requests.get(url, stream=True)
            except Exception:
                print("[-] Invalid Link")
                sys.exit()
            total = response.headers.get('content-length')

            if total is None:
                f.write(response.content)
            else:
                print('[*] Downloading file called {} of size {} MB'.format(filename, math.floor(int(total) / 1000000)))
                downloaded = 0
                total = int(total)
                for data in response.iter_content(chunk_size=max(int(total / 1000), 1024 * 1024)):
                    downloaded += len(data)
                    f.write(data)
                    done = int(50 * downloaded / total)
                    sys.stdout.write('\r[{}{}]'.format('█' * done, '.' * (50 - done)))
                    sys.stdout.flush()
        sys.stdout.write('\n')
        print('[+] Done')
    except KeyboardInterrupt:
        KeyBoardInterrupt(direct_download(url,filename))

def myhooks_for_indirect_download(d):

    if d['status'] == 'downloading':
        done = int(50 * d['downloaded_bytes'] / d['total_bytes'])
        sys.stdout.write('\r[{}{}]'.format('█' * done, '.' * (50 - done)))
        sys.stdout.flush()
    if d['status'] == 'finished':
        print('[+] Done')


def indirect_download(url, filename):
    try:
        ydl_opts = {
            'outtmpl': os.path.join('output', filename),
            'nocheckcertificate': True,
            'no_warnings': True,
            'quiet': True,
            'progress_hooks': [myhooks_for_indirect_download]

        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info=ydl.extract_info(url,download=False)
            formats=info['formats']
            format=formats[0]
            file_size=format['filesize']
            try:
                print('[*] Downloading file called {} of size {} MB'.format(filename, math.floor(int(file_size) / 100000)))
                ydl.download([url])
            except youtube_dl.utils.DownloadError:
                print('[-] Something went wrong.....')
                print('[-] Aborting.....')
                sys.exit()
            except KeyboardInterrupt:
                pass

    except KeyboardInterrupt:
        KeyBoardInterrupt(indirect_download(url,filename))


if __name__ == '__main__':
    direct_download(),
    indirect_download()
