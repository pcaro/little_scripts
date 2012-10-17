#!/bin/sh
# http://mindref.blogspot.com.es/2011/11/python-egg.html

rm -rf eggs
mkdir eggs
for p in /usr/bin/python?.?
do
    echo -n $p
    rm -rf env/
    virtualenv --no-site-packages --python=$p -q env > /dev/null 2>/dev/null
    echo -n .
    env/bin/easy_install -U -O2 -z distribute > /dev/null 2>/dev/null
    for f in $@
    do
        echo -n .
        env/bin/easy_install -O2 -z $f > /dev/null 2>/dev/null
    done
    cp env/lib/python*.*/site-packages/*.egg eggs/ 2>/dev/null
    echo done
done
rm -rf env/
rm -f eggs/setuptools* eggs/distribute*