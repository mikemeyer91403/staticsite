from textnode import TextNode
from textnode import TextType
import os
import shutil
from generator import generate_page


def empty_directory(path):
    shutil.rmtree(path)
# get a list of directory items:
# for each item, check to see if directory
# if it is, call clear_directory recursively on that path and then delte
# else delete file



def directory_copier(source_dir, dest_dir):

    from_path = os.path.abspath(source_dir) 
    to_path = os.path.abspath(dest_dir)
    
    if (not os.path.exists(from_path)):
        raise FileExistsError(f"Source Directory {from_path} not found")

    if (os.path.exists(to_path)):
        print(f"removing old files from {to_path}")
        empty_directory(to_path)
    os.mkdir(to_path)

    filelist = os.listdir(from_path)
    print(filelist)

    for file in filelist:
        src_path = os.path.join(from_path, file)
        dest_path = os.path.join(to_path, file)

        if os.path.isfile(src_path):
            print (f"==> Copying {src_path} to {dest_path}")
            shutil.copy (src_path, dest_path)
        else: 
            print(f"Directory {dest_path}:")
            os.mkdir(dest_path)
            directory_copier(src_path, dest_path)


def main():
    print ("static site generator -- starting...")
    print ("moving source files...")

    # Delete public directory and copy static files to public
    # empty_directory("./public")
    directory_copier( "./static", "./public")

    #generate a page from contect/index.md using template.html and write to public/index.html
    generate_page("./content/index.md","./template.html", "public/index.html")
    print ("... Done!")

main()