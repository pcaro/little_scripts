 #!/usr/bin/python
import os
import re
from os.path import join
from string import Template
import zipfile

import optparse
import sys

project_template_start = """<?xml version="1.0" encoding="UTF-8"?>
<!-- Komodo Project File - DO NOT EDIT -->
<project id="6ff8dfe2-eccd-49c9-b894-40de2bc38b80" kpf_version="4" name="textmate.kpf">
<folder id="b87df6be-832d-4885-bc83-99871e9f56d4" idref="6ff8dfe2-eccd-49c9-b894-40de2bc38b80" name="Abbreviations">
</folder>
"""
snippet_template = Template("""
<snippet id="${id}" idref="b87df6be-832d-4885-bc83-99871e9f56d4" indent_relative="true" keyboard_shortcut="" name="${name}" set_selection="false">
${content}</snippet>""")

project_template_end = """
</project>
"""


def get_content_string(text):
    content_index = text.find("<key>content</key>") + 17
    start = text.find("<string>", content_index) + 8
    end = text.find("</string>", start)
    return text[start:end]


def main(dir='/home/pcaro/tmp/Snippets', output='textmate'):
    tabstop = re.compile(r'(\$\d+)')
    tabstop2 = re.compile(r'(\$\{\d+\})')
    placeholder = re.compile(r'(\$\{\d+:(.*)\})')
    no_nested_placeholder = re.compile(r'(\$\{\d+:([^$\}]+)\})')
    project = project_template_start
    newfile = open("%s.kpf" % output, "w")
    zip = zipfile.ZipFile("%s.kpz" % output, "w")
    i = 0
    for root, dirs, files in os.walk(dir):
        if '.svn' in dirs:
            dirs.remove('.svn')

        for file in files:
            if file.endswith(".tmSnippet"):
                #print file
                i = i + 1
                d = dict(id=i, name=file[:-10])
                f = open(join(root, file))
                source = f.read()
                f.close()
                # Current position
                source.replace("{$TM_SELECTED_TEXT}", "!@#_currentPos!@#_anchor")
                snippet = get_content_string(source)
                snippet = re.sub(no_nested_placeholder, r"[[%tabstop:\2]]", snippet)
                for i in range(3):
                    ## 3 nested levels
                    snippet = re.sub(placeholder, r"\2", snippet)
                snippet = re.sub(tabstop, '[[%tabstop:]]', snippet)
                snippet = re.sub(tabstop2, '[[%tabstop:]]', snippet)
                d['content'] = snippet
                project = project + snippet_template.substitute(d)
    project = project + project_template_end
    print project
    newfile.write(project)
    newfile.close()
    zip.write("%s.kpf" % output)
    zip.close()

if __name__ == '__main__':
    parser = optparse.OptionParser(
        version="0.1",
        usage="%prog -f dest_file snippet_dir")

    parser.add_option("-f",
                  "--file",
                  dest="filename",
                  help="fichero destion.",
                  default="textmate_export"
                  )
    options, args = parser.parse_args()
    if len(args) != 1:
        print 'You must provide a dir to parse with snippets'
        parser.print_help()
        sys.exit(2)

    main(args[0], options.filename)
