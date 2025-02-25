#!/bin/bash
echo "Start continuous deployment script"
python3 control.py &
while true
do
    REMOTE_STATUS=$(git remote update && git status)
    if [[ $REMOTE_STATUS == *"behind"* ]];
    then
        git pull
        killall python3
        python3 control.py &
    fi
    sleep 1
done
