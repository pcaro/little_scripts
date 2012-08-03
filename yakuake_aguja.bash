#!/bin/bash
#
# Create my standard yakuake windows.

sessions=(
    ceic_aguja        'v ceic_aguja; supervisorctl shutdown ; clear ; supervisord; cd django_ezweb'
    ceic_adaptadores  'v ceic_adaptadores; supervisorctl shutdown ; clear ; supervisord'
    ceic_mailproxy    'v ceic_mailproxy; supervisorctl shutdown ; clear ; supervisord'
    ceic_pfirma       'v ceic_pfirma; supervisorctl shutdown ; clear ; supervisord'
    ceic_eco          'v ceic_eco; supervisorctl shutdown ; clear ; supervisord'
    ceic_proxy        'v ceic_proxy; clear; nginxproxy'
    )


function start_sessions()
{
    local session_count=${#sessions[*]}
    local i=0
    while [[ $i -lt $session_count ]]
    do
        local name=${sessions[$i]}
        let i++
        local command=${sessions[$i]}
        let i++

        echo "Creating $name: $command"
        qdbus org.kde.yakuake /yakuake/sessions addSession
        sleep 0.1
        terminalID=$(qdbus org.kde.yakuake | grep Sessions | cut --fields "3" --delim="/" | sort -n | tail -n 1);
        sleep 0.1
        qdbus org.kde.yakuake /yakuake/tabs setTabTitle $((terminalID-1)) $name
        sleep 0.1
        #qdbus org.kde.yakuake /yakuake/sessions runCommand "$command"
        qdbus org.kde.yakuake /yakuake/sessions runCommandInTerminal $((terminalID-1)) "$command"

    done
}

#Is Yakuake running?
if `! qdbus | grep yakuake > /dev/null 2>/dev/null`; then
    #If not, start Yakuake!
    exec yakuake &
    sleep 3
fi

start_sessions
