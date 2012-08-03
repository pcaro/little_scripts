#!/usr/bin/python
# -*- coding: utf-8 -*-
LICENSE_BLOCK = """#
#--- License block -----------------------------------------------------------
# Copyright 2011-2012 Yaco Sistemas SL
# All Rights Reserved.
#
# This file is part of TANGRAM BPM
# Developed by Yaco Sistemas <info@yaco.es>
#
# Licensed under the GNU Affero General Public License Version 3
# You may not use this work except in compliance with the licence.
#
# You should have received a copy of the GNU Affero General Public License Version 3
# along with this program. If not, please see:
#   http://www.gnu.org/licenses/agpl-3.0.en.html
#
# See the Licence for the specific language governing
# permissions and limitations under the Licence.
#--- End of License block ----------------------------------------------------

"""


import os
import sys


def endswith(s, t):
    if isinstance(t, basestring):
        return s.endswith(t)
    if isinstance(t, (list, tuple)):
        for ele in t:
            if s.endswith(ele):
                return True
    return False


def has_license(txt):
    txt_lower = txt.lower()
    if "Affero" in txt:
        return "has already Affero header."
    elif "copyright" in txt_lower or "copyleft" in txt_lower:
        return "has copyright."
    for l in ['license', 'licence', 'License']:
        if l in txt:
            return "Has a different license!!!!!! "
    return False


def add_license(filename, txt):
    f = file(filename, 'w')
    counter = 0
    lines = txt.split("\n")
    l = lines[counter]
    if l.startswith("#"):
        f.write(l + "\n")
        counter += 1
    l = lines[counter]
    if l.startswith("#"):
        if "coding: " in l.lower():
            f.write(l + "\n")
            counter += 1
    f.write(LICENSE_BLOCK)
    for l in lines[counter:-1]:
        f.write(l)
        f.write('\n')
    f.write(lines[-1])
    f.close()


def add_license_to_files_in_dir(path):
    for root, dirs, files in os.walk(path):
        for filename in files:
            filename = os.path.join(root, filename)
            if endswith(filename, ('.py', '.cfg', '.sh')):
                f = file(filename)
                txt = f.read()
                f.close()

                if not txt:
                    # Don't license empty files
                    continue
                if not has_license(txt):
                    # print "adding license."
                    # shutil.copy(filename, filename + '.bak')
                    add_license(filename, txt)
                else:
                    print "%s : %s" % (filename, has_license(txt))


def main():
    if len(sys.argv) < 2:
        print "Usage: %s <file/directory>"
        exit(1)
    path = sys.argv[1]
    add_license_to_files_in_dir(path)

if __name__ == "__main__":
    main()
