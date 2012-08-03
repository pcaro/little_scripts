#! /usr/bin/env python
import os.path
import re
import sets
import sys

CLASS_CSS_RE = r"\.([a-zA-Z0-9\-\_]+).*{"
CLASS_HTML_RE = r'class=["\'](.*?)["\']'

class ClassOcurrence(object):
    def __init__(self, css_class, places=[]):
        self.css_class = css_class
        self.places = places

    def add_place(self, place):
        if place not in self.places:
            self.places.append(place)

    def __unicode__(self):
        return u'%s@%s' % (self.css_class, u', '.join(self.places))

    def __str__(self):
        return unicode(self)

def find_classes(data, regular_expression):
    classes = re.findall(regular_expression, data)
    # remove duplicates
    return list(sets.ImmutableSet(classes))

def classes_in_css(css_data, regular_expression=CLASS_CSS_RE):
    return find_classes(css_data, regular_expression)

def classes_in_html(html_data, regular_expression=CLASS_HTML_RE):
    return find_classes(html_data, regular_expression)

def classes_collector_walker(classes_bag, dirname, fnames):
    exclude_dirs = [i for i, f in enumerate(fnames) if f in ('.svn', 'tiny_mce')]
    exclude_dirs.reverse()
    for i in exclude_dirs:
        del fnames[i]

    extension_map = {'.html': classes_in_html, '.css': classes_in_css}
    for fname in fnames:
        base, ext = os.path.splitext(fname)
        if ext and ext in extension_map:
            full_path = os.path.join(dirname, fname)
            f = file(full_path)
            data = f.read()
            f.close()

            file_type = ext[1:]
            bag = classes_bag[file_type]

            for css_class in extension_map[ext](data):
                try:
                    ocurrence = bag[css_class]
                    ocurrence.add_place(full_path)
                except KeyError:
                    bag[css_class] = ClassOcurrence(css_class, [full_path])


if __name__ == '__main__':
    top_dir = sys.argv[1]

    classes_bags = {'html': {}, 'css': {}}
    os.path.walk(top_dir, classes_collector_walker, classes_bags)

    html_bag = classes_bags['html']
    css_bag = classes_bags['css']

    counter = 0
    for css_class, ocurrence in css_bag.items():
        if css_class not in html_bag:
            print (u'The class "%s", found at %s, is not used in any html file' %
                   (css_class, u', '.join(ocurrence.places)))
            counter += 1

    if counter > 0:
        print u'%d orphan classes were found' % counter
