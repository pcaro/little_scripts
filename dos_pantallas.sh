#!/bin/bash
INT="LVDS1"
EXT="VGA1"
xrandr --output $EXT --mode 1280x1024;
xrandr --output $INT --mode 1280x800;
xrandr --output $EXT --above $INT
xrandr --output $INT --primary
