#!/bin/shä»¶
ftp -n<<! 
open 172.16.60.48 
user shareFile 12TY2167m
passive
binary
cd ./$1/lib
lcd ./$1"-lib"
prompt
mput *
bye
!
