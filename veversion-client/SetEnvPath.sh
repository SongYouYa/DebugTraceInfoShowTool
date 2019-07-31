if [ $1 -eq '0' ];then
    unset QNX_HOST
    unset QNX_TARGET
else
    export QNX_HOST=/opt/qnx700/host/linux/x86_64$QNX_HOST
    export QNX_TARGET=/opt/qnx700/target/qnx7$QNX_TARGET
fi
