#!/usr/bin/env bash

max=100
string="--args"

if [ $# -gt 1 ]
then
    if [ $1 == $string ]
    then
        if [ $max -ge $2 ] 
        then
            var=`echo $2\*0.01 | bc`
            #Here instead of display name, write the name of your display device
            #To get the display device, enter command xrandr -q | grep "connected"
            xrandr --output display_name --brightness $var 
        else
            echo "Error: Argument should be between 0 to 100"
        fi
    else
        echo "Error: Invalid argument. The list of arguments:"
        echo "--args value"
        echo "--help"
    fi
elif [ $# -eq 1 ] && [ $1 == "--help" ]
then
    echo "Control the brightness of your pc"
    echo "Warning: Prefferably keep the brightness atleast at 20. To use, enter command:"
    echo "  brightness -args 100"
elif [ $# -eq 0 ]
then
    echo "Error: No arguments given"
else
        echo "Error: Invalid argument. The list of arguments:"
        echo "--args value"
        echo "--help"
fi

#To run it from any directory, export the path of the folder to PATH variable
