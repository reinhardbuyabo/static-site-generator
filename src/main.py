import os
import shutil
import sys

from copystatic import copy_files_recursive
from markdown_blocks import markdown_to_blocks, markdown_to_html_node

dir_path_static = "./static"
dir_path_public = "./docs"


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    # generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive("content", "template.html", "docs", basepath)


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    return blocks[0].split()[1]


def generate_page(from_path, template_path, dest_path, basepath):
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

    new_links = result.replace('href="/', f'href="{basepath}')
    new_images = new_links.replace('src="/', f'src="{basepath}')

    with open(dest_path, "w") as f:
        f.write(new_images)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for filename in os.listdir(dir_path_content):
        full_src_path = os.path.join(dir_path_content, filename)
        full_dest_path = (
            os.path.join(dest_dir_path, filename.replace(".md", ".html"))
            if filename.endswith(".md")
            else os.path.join(dest_dir_path, filename)
        )

        if os.path.isfile(full_src_path):
            if os.path.isdir(dest_dir_path):
                generate_page(full_src_path, template_path, full_dest_path, basepath)
            else:
                os.makedirs(dest_dir_path)
                generate_page(full_src_path, template_path, full_dest_path, basepath)
        else:
            generate_pages_recursive(full_src_path, template_path, full_dest_path, basepath)


main()
