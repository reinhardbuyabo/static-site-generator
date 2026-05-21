import os
import shutil

from copystatic import copy_files_recursive
from markdown_blocks import markdown_to_blocks, markdown_to_html_node

dir_path_static = "./static"
dir_path_public = "./public"


def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    generate_page("content/index.md", "template.html", "public/index.html")


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    if len(blocks) > 0:
        print(blocks[0].split()[1])
    return blocks[0].split()[1]


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        md_file = f.read()
    with open(template_path) as f:
        template_file = f.read()

    parent_node = markdown_to_html_node(md_file)
    html_str = parent_node.to_html()

    title = extract_title(md_file)

    replaced = template_file.replace("{{ Title }}", title)
    result = replaced.replace("{{ Content }}", html_str)

    with open(dest_path, 'w') as f:
        f.write(result)


main()
