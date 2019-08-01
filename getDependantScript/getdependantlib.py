# -*- coding: utf-8 -*-
# pip install shutil
#using python
import os
import sys
import shutil
import zipfile
import subprocess 
import argparse

pidList = []
errorList =[]
warningList=[]
sysargv1=""
sysargv3=""
sysargv5=" "


parser = argparse.ArgumentParser()
parser.add_argument("--romnum", help="import a rom num for example --romnum ROM860 ", type=str)
parser.add_argument("--unziptype", help="input the unzip file type such as --gz or --ga n ", type=str)
parser.add_argument("--name", help="imput a file name which you want to unzip  such as --namen ", type=str)
args = parser.parse_args()
if args.romnum:
    print args.romnum
if args.unziptype:
    print args.unziptype
if args.name:
    print args.name

sysargv1 = args.romnum
sysargv5  = args.unziptype
sysargv3 = args.name


absoluteRomLibpath = os.getcwd() + "/" +sysargv1
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
            print("os.path.splitext",os.path.splitext(file)[1])
            if os.path.splitext(file)[1]== filter :
                fileterFileList.append(os.path.join(root,file))
    return fileterFileList


def file_name_list(file_dir):
    fileterFileList=[]
    for root,firs,files in os.walk(file_dir):
        for file in files:
            fileterFileList.append(os.path.join(root,file))
    return fileterFileList





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
	findFiles = file_name_filter(os.getcwd(),'.gzaa')
	isexistfile = []
	isexistfile = file_name_filter(absoluteRomLibpath,'.gzaa')
	zipfilepath = os.getcwd() + "/" +sysargv3
	#unzip gzaa
	print("begin to unzip gz-------------------------------------------------------------------")
	if  sysargv5 =="ga":
		str5 = "".join(isexistfile[0])
		print("str5---------------------",str5)
		unzipcmdline = "cat " +str5 + " >> " + zipfilepath + "/Intermediate.tar.gz"
		print("unzip tar.gzaa is:",unzipcmdline)	
		intermediatarpath = os.getcwd() + "/Intermediate.tar.gz"
		interdiate_fzip_path = absoluteRomLibpath +"/" + "Intermediate.tar.gz"
		interdiate_tar_path = absoluteRomLibpath  +"/"+"Intermediate.tar"
		if os.path.exists(intermediatarpath):
			os.system("tar zvxf " +interdiate_fzip_path + " -C " + absoluteRomLibpath )
		else:
			os.system(unzipcmdline)
			os.system("tar zvxf " +interdiate_fzip_path + " -C " + absoluteRomLibpath )
	if sysargv5 =="gz":
		os.system("tar zvxf " +zipfilepath  + " -C " + absoluteRomLibpath )	
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
	#####################################
	####获取文件夹下的所有.so文件
	########################################################
	lib_file_path_list = []
	for root,dirs,files in os.walk(intermediatarpath0):
		for file in files:
			tempfilepath = os.path.join(root,file)
			isfind = tempfilepath.find('.so')
			if isfind == -1:
				print("no find the lib file :",tempfilepath )

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
				lib_file_path_list1.append(tempfilepath1)

	libpath = os.getcwd() +"/"+sysargv1
	mkdir(libpath)
	print ("[>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>-------------------]60.00%")
	print("......")
	######################################
	#copy  libfile to  romLib path
	#
	##################################
	for filepath in lib_file_path_list :
		print(filepath)
		os.system("cp -a " + filepath + " " + libpath )

	for filepath1 in lib_file_path_list1 :
		print(filepath1)
		os.system("cp -a " + filepath1 + " " + libpath )

	#for filepath2 in lib_file_path_list2 :
		#os.system("cp -a " + filepath2 + " " + libpath )
	print("unload lib file sucess>>>>>>>>>>>>>>>>>>>>>>>ok!")



def  replace_qt_lib_name():
	result_file_lists = file_name_list(absoluteRomLibpath)
	for varfile in result_file_lists:
		portion =os.path.splitext(varfile)
		cutstr = ".".join(varfile.split('.')[:-3])
		cutstr+=".5"		
		findqtstr = cutstr .find("libQt5")
		if findqtstr != -1:
			print("cutstr------------:",cutstr )
			os.rename(varfile,cutstr)
			
		#print("sufix is :",portion)		

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
    #delete swap dir
	#os.system("rm -rf " + absoluteRomLibpath)
    #os.system("rm -rf " + absoluteRomLibcopy)


###################################################################################################################################
###################################################################################################################################	
###################################################################################################################################
		
if __name__ == "__main__":

    meterial_prepare()
    #replace_qt_lib_name() #modified the sufix file name
    get_dependence_lib_list()
    os.system("rm -rf " + absoluteRomLibpath)
    
