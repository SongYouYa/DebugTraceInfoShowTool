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

import subprocess 
import sys
pidList = []
errorList =[]
warningList=[]

sysargv1=""
sysargv2=""
sysargv3=""
sysargv4=""


parser = argparse.ArgumentParser()
parser.add_argument("--romnum", help="import a rom num for example -r ROM860 ", type=str)
parser.add_argument("--softpkg", help="num of file which contain network  -n 20190707 cbd49e93 is a slice of file name", type=str)
parser.add_argument("--core", help="-c navigation-1286231_241_1SN004I1_1.core", type=str)
parser.add_argument("--cover", help="whether to cach date , if date have been downloaded in you local place you can set the value is n ", type=str)
args = parser.parse_args()
if args.romnum:
    print args.romnum
if args.softpkg:
    print args.softpkg
if args.core:
    print args.core
if args.cover:
    print args.cover

sysargv1= args.romnum
sysargv2=args.softpkg
sysargv3=args.core
sysargv4=args.cover

absoluteRomLibpath = os.getcwd() + "/" +sysargv1
htmlZipFile = "Kipawa-qnx-700-1.26r." + sysargv2  + '_dev-unstripped.zip' #------------------------set a params
navigationpath  = os.getcwd() + "/"+sysargv1+ "/navigation"
absoluteRomLibcopy = os.getcwd() + "/" +sysargv1+"-lib"

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


def file_name_list(file_dir):
    fileterFileList=[]
    for root,firs,files in os.walk(file_dir):
        for file in files:
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
    
def generate_html_doc():
    htmlfilename =  sysargv3+'.html'  
    print ("begin to run main fun")
    keyword_finder_from_line(htmlfilename ,"[New pid",pidList,"Pr","#0","++")
    insert_line_into_file(htmlfilename ,"beginLabel") 
    keyword_finder_from_line(htmlfilename ,"+++++++1",warningList,"++","++","warning:")
    #source.close()
    insert_line_into_file(htmlfilename,"waringLabel")  
    delete_file__header_data(htmlfilename ,"<html>")

def un_Zip_files(listzipfiled):
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
def get_file_dir_upload(childpath,sharpath):
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
    localpath = os.path.split(os.path.realpath(sysargv0))[0] + "\\romlib"  #must set a value is the same with remte director
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
def recurse_copy(srcpath,dstpath):
    if not os.path.exists(srcpath):
        print ('srcpath not exist!')
    if not os.path.exists(dstpath):
        print ('dstpath not exist!')
    for root,dirs,files in os.walk(srcpath,True):
        for eachfile in files:
            shutil.copy(os.path.join(root,eachfile),dstpath)
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
def meterial_prepare():	
	#---------------------------
	#download gazz for window server
	#method using the ftp shell script 
	#----------------------------
	
	findFiles = []
	mkdir(absoluteRomLibpath)
	mkdir(absoluteRomLibcopy)
	findFiles = file_name_filter(absoluteRomLibpath ,'.gzaa')
	if len(findFiles):
		print('find gzaa file path is :',findFiles)
	else:
		print("the gzaa file is not exits download  from windows server........")
		downloadfilecmdline ='sh '+ os.getcwd() +"/ftpdownloadzip.sh" + " " +sysargv1
		print(downloadfilecmdline)
		os.system(downloadfilecmdline)

	isexistfile = []
	isexistfile = file_name_filter(absoluteRomLibpath,'.gzaa')
	if len(isexistfile):
		print("download the zip file sucesss!")
	else:
		print("download the zip file failure,please checkout out!")
		exit()

	#unzip gzaa
	str5 = "".join(isexistfile[0])
	unzipcmdline = "cat " +str5 + " >> " + absoluteRomLibpath + "/Intermediate.tar.gz"
	print("unzip tar.gzaa is:",unzipcmdline)
	
	intermediatarpath = os.getcwd() + "/Intermediate.tar.gz"
	interdiate_fzip_path = absoluteRomLibpath +"/" + "Intermediate.tar.gz"
	interdiate_tar_path = absoluteRomLibpath  +"/"+"Intermediate.tar"
	if os.path.exists(intermediatarpath):
		os.system("tar zvxf " +interdiate_fzip_path + " -C " + absoluteRomLibpath )
	else:
		os.system(unzipcmdline)
		os.system("tar zvxf " +interdiate_fzip_path + " -C " + absoluteRomLibpath )

	#获取必要的html头信息
	handle_html_header()

	#delete the tem lib file
	os.system("rm  -rf " + interdiate_fzip_path)
	os.system("rm  -rf " + unzipcmdline)
	os.system("rm -rf " +str5)
	
	xzfileList = []
	xzfileList = file_name_filter('./','.xz')
	intermediatarpath0 = absoluteRomLibpath + "/TEMP0"
	intermediatarpath1 = absoluteRomLibpath  +"/TEMP1"
	intermediatarpath2 = absoluteRomLibpath  +"/TEMP0/aarch64le/usr/lib/qt"
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
	#delete the middle file
	print("begine to delete strxz  file..............................")
	os.system("rm -rf " +strxz0)
	os.system("rm -rf " +strxz1)
	print("end to delete strxz  file..............................")

	#####################################
	####获取文件夹下的所有.so文件
	####
	########################################################
	lib_file_path_list = []
	for root,dirs,files in os.walk(intermediatarpath0):
		for file in files:
			tempfilepath = os.path.join(root,file)
			isfind = tempfilepath.find('.so')
			if isfind != -1:
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

	libpath = os.getcwd() +"/"+sysargv1
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
	print("begin to delete TEM dir...................")
	#os.system("rm -rf " + intermediatarpath0)
	#os.system("rm -rf " + intermediatarpath1)
	print("begin to delete lib dir..............")
	os.system("rm -rf  " +absoluteRomLibpath)
	#os.system("rm -rf  " +absoluteRomLibpath+"_")
	print("unload lib file sucess>>>>>>>>>>>>>>>>>>>>>>>ok!")


def modified_html_header_info(filepath,platform,os,date):
    data = ''
    with open(filepath, 'r+') as f:
        for line in f.readlines():
            if(line.find('Platform:<') != -1):
                line = r"echo                 <pre style=""><strong>Platform:</strong>" +platform+"</pre>\n"
                #print(line)
            elif(line.find('OS:<') != -1):
                line = r"echo                 <pre style=""><strong>OS:</strong>" +os+"</pre>\n"
                #print(line)
            elif(line.find('Date:<') != -1):
                line = r"echo                 <pre style=""><strong>Date:</strong> "+date+"</pre>\n"
                #print(line)
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


def handle_html_header():
    gzfilelist = []
    gzfilelist = file_name_filter(absoluteRomLibpath,'.gzaa')
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
    modified_html_header_info('./autoScript.sh','SYNC4',ossysystem ,filecreattime) 

def download_lib_file_from_network():
    #ftp upload the files
    mkdir(absoluteRomLibpath)
    print("begin to download lib from network this will cost about one minutes please waiting..............")
    downloadlibcmdline ='sh '+ os.getcwd() +"/ftpdownloadlib.sh" + " " +sysargv1
    #print("downloadlibcmdline is :",downloadlibcmdline)
    os.system(downloadlibcmdline )
    print("finish downloading lib from network..............")

def get_dependence_lib_list():
    mkdir(absoluteRomLibcopy)
    f =open("dependanceLlibList.txt")
    lib_name_lists =list()
    for line in f.readlines():
        line =line.strip()
        lib_name_lists.append(line)
    f.close()
    result_file_lists =list()
    result_file_lists = file_name_list(absoluteRomLibpath)

    for varfile in lib_name_lists:
        tag=0
        for namepath in result_file_lists:
            errorvalue = namepath.rfind(varfile)
            if errorvalue != -1:
                print("the lib file is find :",varfile)
                temfileppath = "cp -a " + namepath + "  " +absoluteRomLibcopy 
                #print(temfileppath)
                tag=1
                os.system(temfileppath)
                break
        if tag ==0 :
            print("no matched lib file is:",varfile ) 
    #ftp upload the files
    uploadfilecmdline ='sh '+ os.getcwd() +"/ftpuploadlib.sh" + " " +sysargv1
    print("uploadfilecmdline is :",uploadfilecmdline )
    os.system(uploadfilecmdline)
    #delete swap dir
    os.system("rm -rf " + absoluteRomLibcopy)

def unzip_zip() :
    absolutehtmlzipfilepath = os.getcwd() + "/" +sysargv1 +"/"+ htmlZipFile
    unzipfileqnxpath = "unzip -o " + absolutehtmlzipfilepath  +  " -d  " +absoluteRomLibpath 
    print("unzipfileqnxpath path is :",unzipfileqnxpath)
    if 1 :
        os.system(unzipfileqnxpath)
        print("was unziping unstripped.zip file...........")
    else :
        print("run the script no overright file before")   
    #os.system("rm -rf " + absolutehtmlzipfilepath)  

def down_load_zip_from_network():
    urllist2 = "http://tar1.telenav.com:8080/repository/telenav/client/trunk/Kipawa/Kipawa-qnx-700-1.26r." + sysargv2 + "_dev-unstripped.zip"      
    absolutehtmlzipfilepath = os.getcwd() + "/" +sysargv1 +"/"+ htmlZipFile
    print(urllist2 )   
    findFiles = file_name_filter(absoluteRomLibpath ,'.zip')
    if len(findFiles):
        print ("the html zip file is existence!unzip directly!")
    else:
        print("begin to download untripzip from network ....................")
        errorreturn = os.system("wget -P " + absoluteRomLibpath +" " + urllist2 )
        #r = requests.get(urllist2 , stream=True,timeout=10)
        if errorreturn !=0:
            print("please checkout the ----softpkg  is right :" ,sysargv2 )
        print(errorreturn )
        #with open(absoluteRomLibpath+ "/"+htmlZipFile ,"wb") as pdf:
            #for chunk in r.iter_content(chunk_size=1024):
               # if chunk:
                    #pdf.write(chunk)
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>-----------]85.00%")   
 
def generate_gdbinfo_into_html():
    cmdline = "/opt/qnx700/host/linux/x86_64/usr/bin/ntoaarch64-gdb -batch -x autoScript.sh " +  navigationpath  +" "  +absoluteRomLibpath +"/"+ sysargv3  + " >" + sysargv3 + ".html"
    os.system("export PATH=$PATH:" +absoluteRomLibpath ) 
    #get file which form is html/
    cpnavigationcore = "cp -a " + sysargv3 +" " + absoluteRomLibpath
    os.system(cpnavigationcore)
    os.system(cmdline)
    print("acpnavigati path is :", cpnavigationcore )
    #copy navigation to romlib
    generate_html_doc()


###################################################################################################################################
###################################################################################################################################	
###################################################################################################################################
		
if __name__ == "__main__":
    os.system("export PATH=$PATH:/home/treasureFolder/traceAutoScript/traceTool/ROM86 ")
    if sysargv4 == "yes" :
        #meterial_prepare() 
        #get_dependence_lib_list() 
        download_lib_file_from_network()
        down_load_zip_from_network()#download the cbd49e93_dev-unstripped.zip from network
        unzip_zip()
    elif sysargv4 !="no":
        print("error : --cover format is not right please checkout !")
        exit()
    generate_gdbinfo_into_html()
    
