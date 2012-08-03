#!/bin/bash
#
# Set current dir as active tab title

function set_title()
{
    local terminalID=$(qdbus org.kde.yakuake  /yakuake/sessions activeTerminalId );
    local name=$(basename `pwd`);
    qdbus org.kde.yakuake /yakuake/tabs setTabTitle $((terminalID)) $name
    sleep 0.1
}

#Is Yakuake running?
if `! qdbus | grep yakuake > /dev/null 2>/dev/null`; then
    #If not, start Yakuake!
    exec yakuake &
    sleep 3
fi

set_title
