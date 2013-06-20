#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Quick and dirty Chrome kwallet password extractor
# From: http://divided-mind.blogspot.com.es/2012/03/extracting-chrome-passwords-from.html

from PyKDE4.kdeui import KWallet
from PyQt4.QtGui import QApplication
from sys import argv, exit

app = QApplication([])
app.setApplicationName("Chrome password extractor")

print "Introduce la contraseña"

wallet = KWallet.Wallet.openWallet(KWallet.Wallet.LocalWallet(), 0)
wallet.setFolder(u'Chrome Form Data (12573476)')  # check your wallet for exact folder name

entries = wallet.entryList()
try:
    entry = entries.filter(argv[1])[0]
except IndexError:
    print "Entrada no encontrada"
    print "Usage: chrome-passwords TEXT"
    exit(1)

entry = wallet.readEntry(entry)[1]

# outputs ugly slice of pickled data, hopefully you can eyeball the passsword from there
print(repr(str(entry[0:-1:2])))
