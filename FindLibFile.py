'''
	author:
'''
import os
import  shutil 
import sys

listpathfind = []

def mkdir(path):
	folder = os.path.exists(path)
	if not folder:                   
		os.makedirs(path)        
		print "---  new folder...  ---"
		print "---  OK  ---"
 	else:
		print "---  There is this folder!  ---"

def finddir(startdir, target):
    try:
        os.chdir(startdir) 
    except:
        return
    for new_dir in os.listdir(os.curdir):  
        #print(new_dir)
        if new_dir == target :
            #print("FIND--------------------------------------------------------------------------------------------------")
            tepmstr = os.getcwd() + os.sep + new_dir
	    listpathfind.append(tepmstr )
        if os.path.isdir(new_dir) :  
            finddir(new_dir, target)
            os.chdir(os.pardir)   

mkdir('./ROM860') 
# startdir = str(input('Please input startdir: '))
# target = str(input('Please input target: '))
lisdir = '/home/treasureFolder/ZU5T-14G682-AB00041-sym/aarch64le'
lisdir3 = '/home/treasureFolder/ZU5T-14G682-AB00041-sym/aarch64le/usr/lib'
lisdir1 = '/home/treasureFolder/ZU5T-14G682-AB00041-sym/themes'
lisdir2 = '/home/treasureFolder/ZU5T-14G682-AB00041-sym/aarch64le/usr'
list = ['libstringsa64.so','libQt5Quick.so.5.12.2','libcurl.so.2','libQt5Xml.so.5.12.2','libQt5Svg.so.5.12.2','libHMIControls.so','libHMIThemeBundle.so.1','libAudioSoundInterfaceLibrary.so.1','libhmiservices.so.1','libwindowmanager.so.1','libtelemetryidl.so','libftcpidl.so','libtelemetry.so','libNS_Logger.so.1','libfnv_notifications.so.1','libNS_MessageCenter.so.1','libNS_SharedMemIf.so.1','libNS_MessageQueue.so.1','libmosquittopp.so.1','libmosquitto.so.1','libprotobuf.so','libfdtokenclient.so','libfnvthread.so','libanalyticsidl.so','libipclite.so','libRCN_DiagnosticsLib.so.1','libRCN_AnalyticsLib.so.1','libanalytics.so','libipclite.so','libRCN_DiagnosticsLib.so.1','libRCN_AnalyticsLib.so.1','libanalytics.so','libmq.so.1','libscreen.so.1','libQt5Qml.so.5.12.2','libQt5Network.so.5.12.2','libQt5Widgets.so.5.12.2','libQt5Gui.so.5.12.2','libQt5Core.so.5.12.2','libc++.so.1','libm.so.3','ldqnx-64.so.2','liblgmon.so.1','libsocket.so.3','libGLESv2.so.1','libEGL.so.1','libz.so.2','libQt5QuickControls2.so.5.12.2','libQt5Sql.so.5.12.2','libpps.so.1','libasound.so.2','libgestures.so.1','libgestures.so.1','libslog2.so.1','libssl.so.2','libcrypto.so.2','libcares.so.1','libpng16.so.0','libicui18n.so.60.2','libicuuc.so.60.2','libicudata.so.60.2','libQt5QuickTemplates2.so.5.12.2','libc.so.4','libfontconfig.so.1','libfreetype.so.1','libxml2.so.2','libtiff.so.5'] 
curPath = os.getcwd() + '/'+ sys.argv[1]
for i in list:
	finddir(lisdir, i)
	finddir(lisdir1, i)
	finddir(lisdir2, i)
	finddir(lisdir3, i)

for i in listpathfind :
	shutil.copy(i,curPath)	
