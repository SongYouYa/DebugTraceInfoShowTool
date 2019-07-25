# -*- coding: utf-8 -*-
# pip install shutil

#using python 3.7

import os
import sys
import shutil
from datetime import datetime
import urllib.request
import zipfile
import subprocess 
import argparse
import time

isServer = 1
# 替换为空
replace_sharepath = "//172.16.100.82/Kipawa/romlib/"

import subprocess 
import sys

pidList = []
errorList =[]
warningList=[]

def keyword_finder_from_line(file,serchParam,listVec,worngParam,worngParam1,warningParam):
    for line in open(file,'rb+'):
        tmpIdString = line[0:8]
    #print tmpIdString
        tmpNumString = line[0:2]
        if tmpIdString == serchParam :
            listVec.append(line)
        #print line
        elif tmpNumString == worngParam:
            listVec.append(line)
        #print line
        elif tmpNumString == worngParam1:
            listVec.append(line)
        #print line
        elif tmpIdString == warningParam:
            listVec.append(line)
        #print line
        else :
            continue


def insert_line_into_file(filepath,insertParam):
    #insert text to  indeed pos
    if insertParam == "waringLabel":
        lis = ''
        for i in range(len(warningList)):
            lis = lis + warningList[i] +"\n"
    elif insertParam == "beginLabel":
        lis = ''
        for i in range(len(pidList)):
            lis = lis + pidList[i] +"\n"
    elif insertParam == "wronglabel":
        lis = ''
        for i in range(len(errorList)):
            lis = lis + errorList[i] +"\n"
        
    with open(filepath, 'r+') as fd:
        contents = fd.readlines()
        if insertParam in contents[-1]:  # Handle last line to prevent IndexError
            contents.append(lis)
        else:
            for index, line in enumerate(contents):
                if insertParam in line and lis not in contents[index + 1]:
                    contents.insert(index + 1, lis)
                    break
        fd.seek(0)
        fd.writelines(contents)	
            
    
def delete_file__header_data(filepath,deleteParam):
    begin_wright_table = 0;
    with open(filepath,'r') as r:
        lines=r.readlines()
    with open(filepath,'w') as w:
        for l in lines: 
            if begin_wright_table == 0 :
                if deleteParam  in l:
                    begin_wright_table = 1;  #find a pos begin to wright
                    w.write(l) 
            else:
                w.write(l) 
    
def gethehtmldoc():
    htmlfilename =  sys.argv[3]+'.html'  
    print ("begin to run main fun")
    keyword_finder_from_line(htmlfilename ,"[New pid",pidList,"Pr","#0","++")
    insert_line_into_file(htmlfilename ,"beginLabel") 
    keyword_finder_from_line(htmlfilename ,"+++++++1",warningList,"++","++","warning:")
    #source.close()
    insert_line_into_file(htmlfilename,"waringLabel")  
    delete_file__header_data(htmlfilename ,"<html>")

def unZip(listzipfiled):
        for file_name in listzipfiled:
            print('was unziping:' + file_name)
            if os.path.splitext(file_name)[1] == '.zip':
                try:
                    print('was unziping:' + file_name)
                    file_zip = zipfile.ZipFile(file_name, 'r')
                    for file in file_zip.namelist():
                        print(file)
                        file_zip.extract(file, r'./')
                    file_zip.close()
                    #os.remove(file_name)
                except:
                    # name = os.path.splitext(file_name)[0]
                    # os.remove(file_name)
                    # zipurl = 'https://github.com/Python3WebSpider/' + name + '/archive/master.zip'
                    # try:
                    #     print('downloading' + name)
                    #     work_path = os.path.join(dir, name + '.zip')
                    #     urllib.request.urlretrieve(zipurl, work_path)
                    # except:
                        continue


# 打开共享文件夹,从服务器下载文件
def files_download(sharefilepath):
    tempZipFile =  getfiledir_download(sharefilepath, "")
    return tempZipFile


# 打开共享文件夹,上传至服务器
def files_upload(locakfiledir,shardir):
    getfiledir_upload(locakfiledir,shardir)


# 下载
def getfiledir_download(sharpath,localdir):   
    childspath = ""
    filelist = os.listdir(sharpath)
    for files in filelist:
        filespath = os.path.join(sharpath, files)
        if os.path.isfile(filespath):   # 为文件
            childspath = localdir           
            # 如果是文件，则复制
            copyfile_download(filespath, childspath)
        elif os.path.isdir(filespath):  # 为文件夹
            # print filespath
            childspath = os.path.join(localdir, files)
            # 如果为文件夹，则继续循环
            getfiledir_download(filespath, childspath)
    return filelist

# 上传服务器
def getfiledir_upload(childpath,sharpath):
    childspath = ""
    filelist = os.listdir(childpath)
    for files in filelist:
        filespath = os.path.join(childpath, files)
        if os.path.isfile(filespath):  # 判断是否为文件 
            childspath = childpath
            # 如果是文件，则复制

            filesharpath = os.path.join(sharpath, files)
            copyfile_upload(filespath, filesharpath)
        elif os.path.isdir(filespath):  # 判断是否为文件夹
            childspath = os.path.join(sharpath, files)
            # 如果为文件夹，则继续循环
            getfiledir_upload(filespath, childpath)


# 复制文件 或 文件夹 至本地存放
def copyfile_download(paths, childpath):
    localpath = os.path.split(os.path.realpath(sys.argv[0]))[0] + "\\romlib"  #must set a value is the same with remte director
    putpath = path(paths, localpath, replace_sharepath)
    shutil.copy(paths, putpath)
   


# 上传至服务器
def copyfile_upload(path, childpath):
    shutil.copy(path,childpath)
   

# 拼接绝对路径
def path(sharpath, localpat, replacepath):
    sharpath_split = str(sharpath).split('/')
    for i in sharpath_split:
        if i == None or i == "":
            continue
        else:
            if i in localpat:
                realpath = localpat.split(i)[0]
                return realpath + sharpath.replace(replacepath, "")

    #----------------------------------------------------------------------------   
    #处理traceScript 导出固定的html文档 文档的名字也可以相应的进行自动化处理
    #结果与处理的文档的结尾编号日期
    #----------------------------------------------------------------------------
def recutsioncopy(srcpath,dstpath):
    if not os.path.exists(srcpath):
        print ('srcpath not exist!')
    if not os.path.exists(dstpath):
        print ('dstpath not exist!')
    for root,dirs,files in os.walk(srcpath,True):
        for eachfile in files:
            shutil.copy(os.path.join(root,eachfile),dstpath)

def findfile(start, name):
	for name2 in os.listdir(os.curdir):
		if name2 == name:
			return 1
		else :
			return 0

def excuteCmd(cmd, passwd, timeout = 1):
        s = subprocess.Popen(cmd,stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell = True) 
        s.stdin.write(passwd+'\n')
        out, err = s.communicate()
        if err is not None:
            return err   
        return out

if __name__ == "__main__":

    # if isServer:
    #     #上传本地的原始文件到共享目录，一般这一步服务者进行选择的选项
    #     sharepath = "//172.16.100.82/Kipawa/romlib/"
    #     #filepath = "D:/TreasureDir/Tempfile"
    #     localfilepath="D:/testdirupdown/" #
    #     files_upload(localfilepath,sharepath)

    # path = "//172.16.100.82/Kipawa/romlib/"
    # zipfileList = files_download(path)
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('string', metavar='->', type=str, nargs='+',
                   help='python3.6  pachong.py  "ROM805" "20190707.cbd49e93" navigation-1286231_241_1SN004I1_1.core')
    parser.add_argument('string', metavar='805', type=str, nargs='+',
                   help='805 is a num of zip  of bench which contains  share library file')
    parser.parse_args()    
    urllist2 = "http://tar1.telenav.com:8080/repository/telenav/client/trunk/Kipawa/Kipawa-qnx-700-1.26r." + sys.argv[2] + "_dev-unstripped.zip"

    #----------------------------------------------------------------------------cbd49e93_dev-unstripped.zip
    #this value expect to get from  parsing html but thare are some problem to do so 
    #从服务端抓取文件
    #----------------------------------------------------------------------------
    htmlZipFile = "Kipawa-qnx-700-1.26r." + sys.argv[2]  + '_dev-unstripped.zip' #------------------------set a params
    print("Kipawa-qnx-700-1.26 is es" )
    isestience = findfile('./',htmlZipFile)
    print(isestience )
    if isestience ==0 :
        urllib.request.urlretrieve(urllist2 ,htmlZipFile)
    else:
            print("the zipfile is existence")

    dirlib = './RomLib'
    dirfilelib = './RomLib/' + sys.argv[1]  +'.zip'
    #download the zip file from git 
    if os.path.exists(dirlib):
        if not os.path.exists(dirfilelib ):
            print('the zip file not  existence\n exec git pull ..........')
            cmdline = "git pull"
            os.system(cmdline)
        else :
             print(' find the rom.zip file!')
    else:
        cmdline1 = "git clone https://bbxyzhangting%40126.com:Number0123@github.com/SongYouYa/RomLib.git"
        print("not find the romlibdir\n begin exec load file from network")
        os.system(cmdline1)
        
    #----------------------------------------------------------------------------   
    #copy file to current dir from  RomLib
    #---------------------------------------------------------------------------
    theCopyZipFileName = sys.argv[1] + '.zip'
    cmdLineCopy = 'cp -a RomLib/' +theCopyZipFileName +  ' ./'
    isestience = findfile('./',theCopyZipFileName )  #if file is existence not cope it again 
    if isestience ==0 : 
        os.system(cmdLineCopy )
    else:
        print("the ROM80*file is existence")
  
    os.system('chmod -R 777 ./')

    #----------------------------------------------------------------------------   
    #upzip file
    #----------------------------------------------------------------------------
    zipfilenamelist = []
    zipfilenamelist.append(htmlZipFile)
    romstr = sys.argv[1] +'.zip'
    zipfilenamelist.append(romstr)#-------------------------------------------------------set param
    unZip(zipfilenamelist)

    recutsioncopy('fs','./') 
    recutsioncopy('proc','./') 
    recutsioncopy('usr','./')
    #----------------------------------------------------------------------------   
    #remove the no use directory
    #----------------------------------------------------------------------------
    shutil.rmtree("fs")
    shutil.rmtree("proc")
    shutil.rmtree("usr")

    cmdline = "/opt/qnx700/host/linux/x86_64/usr/bin/ntoaarch64-gdb -batch -x autoScript.sh navigation " + sys.argv[3]  + " >" + sys.argv[3] + ".html"
    os.system(cmdline)
    #get file which form is html
    gethehtmldoc()


   
