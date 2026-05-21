import os
import shutil
from os.path import isdir, isfile

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

    # generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive("content", "template.html", "public")


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
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

    with open(dest_path, "w") as f:
        f.write(result)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        full_src_path = os.path.join(dir_path_content, filename)
        full_dest_path = (
            os.path.join(dest_dir_path, filename.replace(".md", ".html"))
            if filename.endswith(".md")
            else os.path.join(dest_dir_path, filename)
        )

        if os.path.isfile(full_src_path):
            if os.path.isdir(dest_dir_path):
                generate_page(full_src_path, template_path, full_dest_path)
            else:
                os.makedirs(dest_dir_path)
                generate_page(full_src_path, template_path, full_dest_path)
        else:
            generate_pages_recursive(full_src_path, template_path, full_dest_path)


main()
