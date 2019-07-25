# -*- coding: utf-8 -*-
# pip install shutil

#using python
import os
import sys
import shutil
from datetime import datetime
import zipfile
import subprocess 
import argparse
import time
import requests
from progressbar import *
isServer = 1
# 替换为空
replace_sharepath = "//172.16.100.82/Kipawa/romlib/"

import subprocess 
import sys

pidList = []
errorList =[]
warningList=[]

#-------------------------------------------------
# @param file_dir  file path
# @param filter find the index of files
#其中os.path.splitext()函数将路径拆分为文件名+扩展名
##-------------------------------------------------
def file_name_filter(file_dir,filter):
    fileterFileList=[]
    for root,firs,files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1]== filter :
                fileterFileList.append(os.path.join(root,file))
    return fileterFileList


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
#查找文件是否存在
def findfile(start, name):
	for name2 in os.listdir(start):
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
#创建目录
def mkdir(path):
	folder = os.path.exists(path)
	if not folder:                   
		os.makedirs(path)        
		print ("---  new folder...  ---")
		print ("---  OK  ---")
	else:
		print ("---  There is this folder!  ---")
		
#从服务器下载解压文件并筛选.so文件复制到指定的目录下
def meterialPrepare():	
	#---------------------------
	#download gazz for window server
	#method using the ftp shell script 
	#----------------------------
	findFiles = []
	absoluteRomLIbpath = os.getcwd() + "/" + sys.argv[1]
	
	findFiles = file_name_filter(absoluteRomLIbpath ,'.gzaa')
	if len(findFiles):
		print('find gzaa file path is :',findFiles)
	else:
		print("the gzaa file is not exits download  from windows server........")
		downloadfilecmdline ='sh '+ os.getcwd() +"/ftpdownloadfile.sh" + " " +sys.argv[1]
		print(downloadfilecmdline)
		os.system(downloadfilecmdline)

	isexistfile = []
	isexistfile = file_name_filter(absoluteRomLIbpath,'.gzaa')
	if len(isexistfile):
		print("download the zip file sucesss!")
	else:
		print("download the zip file failure,please checkout out!")
		exit()

	#unzip gzaa
	str5 = "".join(isexistfile[0])
	unzipcmdline = "cat " +str5 + " >> " + absoluteRomLIbpath + "/Intermediate.tar.gz"
	print("unzip tar.gzaa is:",unzipcmdline)
	
	intermediatarpath = os.getcwd() + "/Intermediate.tar.gz"
	interdiate_fzip_path = absoluteRomLIbpath +"/" + "Intermediate.tar.gz"
	interdiate_tar_path = absoluteRomLIbpath  +"/"+"Intermediate.tar"
	if os.path.exists(intermediatarpath):
		os.system("tar zvxf " +interdiate_fzip_path + " -C " + absoluteRomLIbpath )
		#os.system("tar zvxf "+interdiate_tar_path +" -C " + absoluteRomLIbpath )
	else:
		os.system(unzipcmdline)
		os.system("tar zvxf " +interdiate_fzip_path + " -C " + absoluteRomLIbpath )
		#os.system("tar zvxf "+interdiate_tar_path +" -C " + absoluteRomLIbpath )
	#进一步进行解压xz 结尾的文件

	xzfileList = []
	xzfileList = file_name_filter('./','.xz')
	intermediatarpath0 = absoluteRomLIbpath + "/TEMP0"
	intermediatarpath1 = absoluteRomLIbpath  +"/TEMP1"
	intermediatarpath2 = absoluteRomLIbpath  +"/TEMP0/aarch64le/usr/lib/qt"
	mkdir(intermediatarpath0)
	mkdir(intermediatarpath1)
	print ("[>>>>>>>>>>>>>>>>>>>---------------------------------------]30.00%")
	print("......")
	strxz0 = "".join(xzfileList[0])
	strxz1 = "".join(xzfileList[1])
	
	cmdlinexz0 = "tar  -xJf  " +strxz0 + " -C " + intermediatarpath0
	cmdlinexz1 = "tar  -xJf  " +strxz1 + "  -C " + intermediatarpath1
	os.system(cmdlinexz0)
	os.system(cmdlinexz1)

	#####################################
	####获取文件夹下的所有.so文件
	####
	########################################################
	lib_file_path_list = []
	for root,dirs,files in os.walk(intermediatarpath0):
		for file in files:
			tempfilepath = os.path.join(root,file)
			isfind = tempfilepath.find('.so')
			if isfind == -1:
				process_bar.show_process(60)
			else :
				lib_file_path_list.append(tempfilepath)

	lib_file_path_list1 = []
	for root,dirs,files in os.walk(intermediatarpath1):
		for file in files:
			tempfilepath1 = os.path.join(root,file)
			isfind = tempfilepath1.find('.so')
			if isfind == -1:
				print("no find the lib file :",tempfilepath1)
			else :
				lib_file_path_list1.append(tempfilepath)

	libpath = os.getcwd() +"/"+sys.argv[1]
	mkdir(libpath)
	print ("[>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>-------------------]60.00%")
	print("......")
	######################################
	#copy  libfile to  romLib path
	#
	##################################
	for filepath in lib_file_path_list :
		os.system("cp -a " + filepath + " " + libpath )

	for filepath1 in lib_file_path_list1 :
		os.system("cp -a " + filepath1 + " " + libpath )

	#for filepath2 in lib_file_path_list2 :
		#os.system("cp -a " + filepath2 + " " + libpath )


class ShowProcess():
    """
    显示处理进度的类
    调用该类相关函数即可实现处理进度的显示
    """
    i = 0 # 当前的处理进度
    max_steps = 0 # 总共需要处理的次数
    max_arrow = 50 #进度条的长度
    infoDone = 'done'

    # 初始化函数，需要知道总共的处理次数
    def __init__(self, max_steps, infoDone = 'Done'):
        self.max_steps = max_steps
        self.i = 0
        self.infoDone = infoDone

    # 显示函数，根据当前的处理进度i显示进度
    # 效果为[>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>]100.00%
    def show_process(self, i=None):
        if i is not None:
            self.i = i
        else:
            self.i += 1
        num_arrow = int(self.i * self.max_arrow / self.max_steps) #计算显示多少个'>'
        num_line = self.max_arrow - num_arrow #计算显示多少个'-'
        percent = self.i * 100.0 / self.max_steps #计算完成进度，格式为xx.xx%
        process_bar = '[' + '>' * num_arrow + '-' * num_line + ']'\
                      + '%.2f' % percent + '%' + '\r' #带输出的字符串，'\r'表示不换行回到最左边
        sys.stdout.write(process_bar) #这两句打印字符到终端
        #sys.stdout.flush()
        if self.i >= self.max_steps:
            self.close()

    def close(self):
        print('')
        print(self.infoDone)
        self.i = 0

def modifiedHtmlHeaderInfo(filepath,platform,os,date):
    data = ''
    with open(filepath, 'r+') as f:
        for line in f.readlines():
            if(line.find('Platform:<') != -1):
                line = r"echo                 <pre style=""><strong>Platform:</strong>" +platform+"</pre>\n"
                print(line)
            elif(line.find('OS:<') != -1):
                line = r"echo                 <pre style=""><strong>OS:</strong>" +os+"</pre>\n"
                print(line)
            elif(line.find('Date:<') != -1):
                line = r"echo                 <pre style=""><strong>Date:</strong> "+date+"</pre>\n"
                print(line)
            data += line

    with open(filepath, 'r+') as f:
        f.writelines(data)   

def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)

def get_FileCreateTime(filePath):
    filePath = unicode(filePath,'utf8')
    t = os.path.getctime(filePath)
    return TimeStampToTime(t)


if __name__ == "__main__":
    max_steps = 100
    print (">------------------------------------------]1.00%")
    process_bar = ShowProcess(max_steps, 'OK')

    process_bar.show_process(2)
    # if isServer:
    #     #上传本地的原始文件到共享目录，一般这一步服务者进行选择的选项
    #     sharepath = "//172.16.100.82/Kipawa/romlib/"
    #     #filepath = "D:/TreasureDir/Tempfile"
    #     localfilepath="D:/testdirupdown/" #
    #     files_upload(localfilepath,sharepath)
#############################################################
#set the param guild the users how to using the script
#############################################################
    # path = "//172.16.100.82/Kipawa/romlib/"
    # zipfileList = files_download(path)
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('string', metavar='->', type=str, nargs='+',
                   help='python3.6  pachong.py  "ROM805" "20190707.cbd49e93" navigation-1286231_241_1SN004I1_1.core')
    parser.add_argument('string1', metavar='805', type=str, nargs='+',
                   help='860 is a num of zip  of bench which contains  share library file')
    parser.add_argument('string', metavar='1', type=str, nargs='+',
                   help='1 whether  redownload file from server if local have been files  you can set num is 0')

    args = parser.parse_args()
    mkdir(sys.argv[1]) #mkadir a romdir which is used to contain .so and mid file which is generated by run program
    #print (">>>>>>-------------------------------------]5.00%")
    print("......")

#############################################################
#get lib file from windows server
#############################################################
    if sys.argv[4] == '1' :
        meterialPrepare()
        print("was get source file from window server...........")
    else :
        print("run the script no overright file before")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>-------------------------------------]50.00%")

#########################
#
#modified the html head info 
###################################################################
    gzfilelist = []
    absoluteRomLIbpath = os.getcwd() + "/" +sys.argv[1]
    gzfilelist = file_name_filter(absoluteRomLIbpath,'.gzaa')
    if len(gzfilelist ):
        print("gzaa file sucess find!")
    else:
         print("gzzaa file not find ,please checkout out!")
         exit()
    gzzfilename = "".join(gzfilelist[0])
    ossysystem = gzzfilename[-70:-33]
    filecreattime = get_FileCreateTime(gzzfilename)
    print("filecreattime is :",ossysystem)
    print("gzzfilepath  is :",gzzfilename)
    print("gzzfilepath is :",filecreattime)
    modifiedHtmlHeaderInfo('./autoScript.sh','SYNC4',ossysystem ,filecreattime )  

#############################################################
#download the cbd49e93_dev-unstripped.zip from network
#############################################################
    urllist2 = "http://tar1.telenav.com:8080/repository/telenav/client/trunk/Kipawa/Kipawa-qnx-700-1.26r." + sys.argv[2] + "_dev-unstripped.zip"      
    htmlZipFile = "Kipawa-qnx-700-1.26r." + sys.argv[2]  + '_dev-unstripped.zip' #------------------------set a params
    absolutehtmlzipfilepath = os.getcwd() + "/" +sys.argv[1] +"/"+ htmlZipFile  
    
    mkdir(absoluteRomLIbpath)
    navigationpath  = os.getcwd() + "/"+sys.argv[1]+ "/navigation"
    print("absolutehtmlzipfilepath  path is :",absolutehtmlzipfilepath )
    isestience = sys.argv[4]
    print("is existence the zip ifle 1 yes 0 no  value is:",isestience )
    r = requests.get(urllist2 , stream=True)
    if isestience == '1' :
        with open(absoluteRomLIbpath+ "/"+htmlZipFile ,"wb") as pdf:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    pdf.write(chunk)
    else:
        print ("the html zip file is existence!unzip directly!")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>-----------]85.00%")
#############################################################
#unzip html files
#############################################################  
    unzipfileqnxpath = "unzip -o " + absolutehtmlzipfilepath  +  " -d  " +absoluteRomLIbpath 
    print("unzipfileqnxpath path is :",unzipfileqnxpath)
    if sys.argv[4] == '1' :
        os.system(unzipfileqnxpath)
        print("was unziping unstripped.zip file...........")
    else :
        print("run the script no overright file before")
    
    process_bar.show_process(90)

    #----------------------------------------------------------------------------
    #run the gdb out put the gdb.html file
    #
    #---------------------------------------------------------------------------------
    cmdline = "/opt/qnx700/host/linux/x86_64/usr/bin/ntoaarch64-gdb -batch -x autoScript.sh " +  navigationpath  +" "  +absoluteRomLIbpath +"/"+ sys.argv[3]  + " >" + sys.argv[3] + ".html"
    os.system("export PATH=$PATH:" +absoluteRomLIbpath ) 
    #get file which form is html/
    cpnavigationcore = "cp -a " + sys.argv[3] +" " + absoluteRomLIbpath
    os.system(cpnavigationcore)
    os.system(cmdline)
    print("acpnavigati path is :", cpnavigationcore )
    #copy navigation to romlib
    gethehtmldoc()
    process_bar.show_process(100)
    time.sleep(1) 
