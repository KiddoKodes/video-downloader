from downloader import direct_download,indirect_download
import inquirer,sys
def main():
    try:
        questions = [
          inquirer.List('linkWay',
                        message="What is the type of link you want to download?",
                        choices=['Direct [i.e. https://example.com/download.mp4 || https://google.com/]','Indirect [i.e. https://example.com/watch?v=r5ifjeb00e || https://website.uk/how-to-learn]'],
                    ),
        ]
        answers = inquirer.prompt(questions)
        choice=answers["linkWay"].split(" ")[0]
        url=input("Enter the link: ")
        fname=input("Enter the file name: ")
        if(choice=="Direct"):
            direct_download(url,fname)
        if(choice=="Indirect"):
            indirect_download(url,fname)
    except KeyboardInterrupt and TypeError:
        confirm=input("[?] Do you want to exit the program [Y/N]: ")
        if confirm=="y" or confirm=="Y" or confirm=="Yes" or confirm=="yes":
            sys.exit()
        else:
            main()
main()
