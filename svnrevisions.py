#!/usr/bin/python
# -*- coding: utf8 -*-


import os
from os.path import join
import re
import sys
import pprint 

REGEX = re.compile('^Revisión: (\d+)',re.MULTILINE)

def svnrevisions(dirname=None):
    if dirname == None:
        dirname = os.path.curdir
    revisions = {}
    for root, dirs, files in os.walk(dirname):
        if '.svn' in dirs:
            dirs.remove('.svn')
            path = join(dirname,root)
            r = getRevision(path)
            l = revisions.get(r,[])
            l.append(path)
            revisions[r] = l 
            for file in files:
                path = join(dirname,root,file)
                r = getRevision(path)
                l = revisions.get(r,[])
                l.append(path)
                revisions[r] = l 
    return revisions
                
def getRevision(path):
    pipe = os.popen("svn info %s 2>&1" % path)
    output = pipe.read()
    erno = pipe.close()
    if not erno:
        matches = REGEX.findall(output)
        if matches:
            return matches[0]
    return 'Desconocido'
    

if __name__ == '__main__':
    revisions = svnrevisions()
    if len(sys.argv) > 1:
        r = sys.argv[1]
        if r in revisions:
            print 'Elementos con revisión: %s' % r 
            pprint.pprint(revisions[r])
        else:
            print 'No existen elementos con revisón "%s"' % r
    else:
        print 'Revisiones encontradas.'
        for r in revisions.keys():
            elementos = len(revisions[r])
            print '%-15s  (%s elementos)' % (r,elementos)
        print 'Escriba "svnrevisions REVISION" para ver los elementos'