#!/bin/bash
#
# Create my standard yakuake windows.

exit_usage() {
    echo -e "Usage: $0 venv_name [0.0.0.0:9000]"
    exit 1
}

case $# in
    2 ) env=$1
        runserver_args=$2;;
    1)  env=$1
         runserver_args="0.0.0.0:9000";;
    * ) exit_usage;;
esac


sessions=(
    "runserver_$env"  "workon $env; python manage.py runserver $runserver_args"
    "shell_$env"      "workon $env; python manage.py shell_plus"
    "src1_$env"       "sshpro; workon $env; cd $env;"
    "src2_$env"       "workon $env; cd $env;"
    "src2_$env"       "workon $env; cd $env;"
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
