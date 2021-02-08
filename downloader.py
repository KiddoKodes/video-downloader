import os
import requests
import sys,math,youtube_dl

def direct_download(url, filename):
    with open(filename, 'wb') as f:
        try:
            response = requests.get(url, stream=True)
        except Exception:
            print("[-] Invalid Link")
            sys.exit()
        total = response.headers.get('content-length')

        if total is None:
            f.write(response.content)
        else:
            print('[*] Downloading file called {} of size {} MB'.format(filename,math.floor(int(total)/1000000)))
            downloaded = 0
            total = int(total)
            for data in response.iter_content(chunk_size=max(int(total / 1000), 1024 * 1024)):
                downloaded += len(data)
                f.write(data)
                done = int(50 * downloaded / total)
                sys.stdout.write('\r[{}{}]'.format('█' * done, '.' * (50 - done)))
                sys.stdout.flush()
    sys.stdout.write('\n')
def indirect_download(url,filename):
    try:
        ydl_opts = {
            'outtmpl':os.path.join(filename),
            'nocheckcertificate':True

        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except KeyboardInterrupt:
        confirm = input("[?] Do you want to exit the program [Y/N]: ")
        if confirm == "y" or confirm == "Y" or confirm == "Yes" or confirm == "yes":
            sys.exit()
        else:
            indirect_download(url,filename)


if __name__ == '__main__':
    direct_download(),indirect_download()
