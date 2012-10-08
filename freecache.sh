#!/bin/bash

# http://eduangi.com/2009/04/04/limpiar-memoria-en-linux/

sync; echo 3 > /proc/sys/vm/drop_caches
