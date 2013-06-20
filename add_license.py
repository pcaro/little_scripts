#!/usr/bin/python
# -*- coding: utf-8 -*-

AFERO_BLOCK = """#
#--- License block -----------------------------------------------------------
# Copyright 2012-2013 Yaco Sistemas SL
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


EUPL_BLOCK = """#
#--- License block -----------------------------------------------------------
# Copyright 2012-2013 Junta de Andalucía
# All Rights Reserved.
#
# Developed by Yaco Sistemas <info@yaco.es>
#
# Licensed under the European Union Public Licence (EUPL) Version 1.1  or - as
# soon they will be approved by the European Commission - subsequent
# versions of the EUPL (the "Licence");
# You may not use this work except in compliance with the licence.
#
# You should have received a copy of license
# along with this program. If not, please see:
#   http://joinup.ec.europa.eu/software/page/eupl
#
# Unless required by applicable law or agreed to in
# writing, software distributed under the Licence is
# distributed on an "AS IS" basis,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.
#
# See the Licence for the specific language governing
# permissions and limitations under the Licence.
#--- End of License block ----------------------------------------------------

"""

# LICENSE_BLOCK = AFERO_BLOCK
# DEFAULT_LICENSE_CHECK="Affero"

LICENSE_BLOCK = EUPL_BLOCK
DEFAULT_LICENSE_CHECK = "EUPL"

CODING = "# -*- coding: utf-8 -*-\n"

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


def has_license(txt, default="EUPL"):
    txt_lower = txt.lower()
    if default in txt:
        return "has already %s header." % default
    elif "copyright" in txt_lower or "copyleft" in txt_lower:
        return "has copyright."
    for l in ['license', 'licence', 'License']:
        if l in txt:
            return "Has a different license!!!!!! "
    return False


def has_coding(txt):
    if 'coding:' in txt:
        return "has already encoding."
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


def add_coding(filename, txt):
    f = file(filename, 'w')
    counter = 0
    lines = txt.split("\n")
    l = lines[counter]
    if l.startswith("#!"):
        f.write(l + "\n")
        counter += 1
    f.write(CODING)
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


def add_codingline_to_files_in_dir(path):
    for root, dirs, files in os.walk(path):
        for filename in files:
            filename = os.path.join(root, filename)
            if endswith(filename, ('.py', )):
                f = file(filename)
                txt = f.read()
                f.close()

                if not txt:
                    # Don't change empty files
                    continue
                if not has_coding(txt):
                    add_coding(filename, txt)
                else:
                    print "%s : %s" % (filename, has_coding(txt))


def main():
    if len(sys.argv) < 2:
        print "Usage: %s <file/directory> [--coding]"
        exit(1)
    path = sys.argv[1]
    if len(sys.argv) == 3 and sys.argv[2] == "--coding":
        add_codingline_to_files_in_dir(path)
    else:
        add_license_to_files_in_dir(path)

if __name__ == "__main__":
    main()
