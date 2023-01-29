#!/bin/bash

IMAGE1="/home/winter/Projects/SilverstoneV2/R4023-JF008-01_Rev1.20_SilverstoneV2_BMC_Image.ima"
IMAGE2="/home/winter/Projects/SilverstoneV2/R4023-JF008-01_Rev9.99_SilverstoneV2_BMC_Image.ima"

count=0

while true
do
    count=`expr $count + 1`
    echo ""
    echo "###### cycle $count ######"
    echo ""
    rev=`ipmitool -I lanp -H 10.194.78.17 -U admin -P admin raw 0x32 0x8f 8 2 | awk -F " " '{print $1}'`
    if [ "$rev" = "" ];then
        exit
    fi

    if [ "$rev" = "01" ];then
        echo "Update firmware version to v9.99 ..."
        python3 fwupdate.py $IMAGE2
        if [ $? -ne 0 ];then
            echo "Firmware update failed !!!"
            exit 1
        fi
    elif [ "$rev" = "09" ]; then
        echo "Update firmware version to v1.20 ..."
        python3 fwupdate.py $IMAGE1
        if [ $? -ne 0 ];then
            echo "Firmware update failed !!!"
            exit 1
        fi
    else
        echo "Firmware version not correct !!!"
    fi

    sleep 600
done
