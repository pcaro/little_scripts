#!/usr/bin/env python
'''
From:
    https://gist.github.com/3555765

'''
import pip
import xmlrpclib


def main():
    pypi = xmlrpclib.ServerProxy('http://pypi.python.org/pypi')
    for dist in pip.get_installed_distributions():
        available = pypi.package_releases(dist.project_name)
        if not available:
            # Try to capitalize pkg name
            available = pypi.package_releases(dist.project_name.capitalize())

        try:
            if available[0] != dist.version:
                print '{dist.project_name} ({dist.version} < {available})'.format(dist=dist, available=available[0])

        except IndexError:
            pass


if __name__ == '__main__':
    main()
