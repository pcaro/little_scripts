#!/usr/bin/env python

import time
import sys
import xmlrpclib


def main():
    pypi = xmlrpclib.ServerProxy('http://pypi.python.org/pypi')
    names = set(r[0] for r in pypi.browse(['Framework :: Django']))
    names.update(name for name in pypi.list_packages() if 'django' in name)
    for count, name in enumerate(names):
        total = 0
        releases = pypi.package_releases(name, False)
        for release in releases:
            urls = pypi.release_urls(name, release)
            downloads = sum(int(url['downloads']) for url in urls)
            total += downloads
        print total, name
        sys.stdout.flush()  # So that I can tee to file and watch stdout
        # Be nice and don't hit PyPI too frequently
        time.sleep(0.1)
        # Break early when you are debugging the script
        # For testing
        #if count > 9:
        #    sys.exit()

    print 'Fetched statistics from %d django packages' % count


if __name__ == '__main__':
    main()
