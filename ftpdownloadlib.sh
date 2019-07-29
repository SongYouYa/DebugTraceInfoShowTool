#!/bin/shä»¶
echo -e "\e[1;32m begin to download lib from network this will cost about one minutes please waiting......\e[0m"
ftp -n<<! 
open 172.16.60.48 
user shareFile 12TY2167m
passive
binary
cd ./$1/lib
lcd ./$1
prompt
mget *
bye
!
