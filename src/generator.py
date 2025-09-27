from markdown import markdown_to_html_node
import os


#  HTML page generator functions
def extract_title(markdown):
    # find the h1 header in the markdown, and extract that line
    header = ""
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            header = line
            break
    if header == "":
        raise ValueError("H1 Header not present in markdown")
    #strip the # and any leading or trailing whitespace
    stripped_header = header[2:].strip(' ')
    return stripped_header



# placeholder - a string (e.g. {{Title}} ) to replace
# text to replace it with
def replace_placeholder(text, placeholder, replacement):
    return (text.replace(placeholder,replacement))



# Page generator
# - from_path - path to the markdown file
#  - template_path - path to the template file to read
#  - dest_path - path to write HTML file to
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    #read the markdown file
    with open(from_path) as file:
        md_text = file.read()
    #template file
    with open(template_path) as html_file:
        template_html = html_file.read()
    #convert the markdown to html
    content_node = markdown_to_html_node(md_text)
    content_html = content_node.to_html()
    title = extract_title(md_text)
    print(f"Extracted title: {title}")
    #replace title and content placeholders
    template_html = replace_placeholder(template_html, "{{ Title }}", title)
    #print (f"{template_html}")
    template_html = replace_placeholder(template_html, "{{ Content }}", content_html)

    # save the file to dest. path
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir, exist_ok=True) #will make the subdirectories if they don't exist)
    with open(dest_path, "w") as ofile:
        ofile.write(template_html)

def generate_pages_recursive(dir_path_content, template_path,dest_dir_path):
    content_path = os.path.abspath(dir_path_content)
    if (not os.path.exists(content_path)):
        raise FileNotFoundError(f"Source directory {content_path} not found")
    
    file_list = os.listdir(content_path)

    for file in file_list:
        src_path = os.path.join(content_path, file)
        destname = file.replace("md","html")
        dest_path = os.path.join(dest_dir_path, destname)

        if os.path.isfile(src_path):
            print (f"==> generating {dest_path} from {src_path}")
            generate_page(src_path, template_path, dest_path)
        else:
            #concatinate new directory name to path
            contentdir = os.path.join(dir_path_content, file)
            destdir = os.path.join(dest_dir_path, file)
            print(f"===building dest directory {destdir}")
            os.mkdir(destdir)
            generate_pages_recursive(contentdir,template_path,destdir)
