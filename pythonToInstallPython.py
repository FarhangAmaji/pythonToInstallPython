import http.client
import time
import subprocess
from bs4 import BeautifulSoup
import os
import sys
import re
pythonDefaultVersion= '3.11.2'
notToInstalPythonDefaultVersionIfExists = input(f"first try to Install Python Default Version({pythonDefaultVersion}) If its file Exists:(!!!enter sth if u dont want to)")
print("InstalPythonDefaultVersionIfExists",not notToInstalPythonDefaultVersionIfExists)
def createIfTheDirectoryDoesntExist(dir_):
    if not os.path.exists(dir_):
        os.makedirs(dir_)
basePath= r'c:\pythonToInstallPython\\'
createIfTheDirectoryDoesntExist(basePath)
logFile=basePath+'pythonToInstallPythonLog.txt'
print("pythonToInstallPython",file=open(logFile, "w"))
print("basePath:",basePath,file=open(logFile, "a"))
def isPythonInstalled():
    try:
        subprocess.check_call(['python', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Python is installed on Windows.",file=open(logFile, "a"))
        return True
    except:
        print("Python is not installed on Windows.",file=open(logFile, "a"))
        return False
def waitForAFileToBeInstalled(filename,options):
    try:
        cmdArgs=[filename, *options]
        print("cmdArgs:",cmdArgs,file=open(logFile, "a"))
        install_process = subprocess.run(cmdArgs, shell=True, check=True)
        while install_process.poll() is None:
            time.sleep(1)
        # Check the exit code of the installation process
        if install_process.returncode == 0:
            print(f"{filename} installation completed successfully.",file=open(logFile, "a"))
        else:
            print(f"{filename} installation failed.",file=open(logFile, "a"))
    except Exception as e:
        currentFuncName=inspect.stack()[0][3]
        print(f'error in {currentFuncName}',time.time(),file=open(logFile, "a"))
        print(e,time.time(),file=open(logFile, "a"))
def extract_version(text):
    match = re.search(r"\d+\.\d+(\.\d+)?", text)
    if match:
        return match.group()
    else:
        return False
def getLatestPythonVersion():
    try:
        conn = http.client.HTTPSConnection("www.python.org")
        conn.request("GET", "/downloads/")
        res = conn.getresponse()
        html = res.read().decode()
        soup = BeautifulSoup(html, "html.parser")
        version = soup.select_one("#touchnav-wrapper > header > div > div.header-banner > div > div.download-os-windows > p > a").text
        if extract_version(version):
            return extract_version(version)
        else:
            return pythonDefaultVersion
    except Exception as e:
        currentFuncName=inspect.stack()[0][3]
        print(f'error in {currentFuncName}',time.time(),file=open(logFile, "a"))
        print(e,time.time(),file=open(logFile, "a"))
        return pythonDefaultVersion
def doesTheFileExistsWithSizeMoreThan10Mb(filename):
    print('fileExist:',filename,os.path.exists(filename),file=open(logFile, "a"))
    if os.path.exists(filename):
        print('filesize:',filename,os.path.getsize(filename),file=open(logFile, "a"))
        if os.path.getsize(filename)>10_000_000:
            return True
    return False
def pythonToInstallPythonHttpDownloader(filename,latestPythonVersion):
    dlPython=not doesTheFileExistsWithSizeMoreThan10Mb(filename)
    if dlPython:
        print('prepythonDownload',time.time(),file=open(logFile, "a"))
        try:
            conn = http.client.HTTPSConnection("www.python.org")
            conn.request("GET", f"/ftp/python/{latestPythonVersion}/python-{latestPythonVersion}-amd64.exe")
            res = conn.getresponse()
            with open(filename, "wb") as file:
                file.write(res.read())
            conn.close()
        except Exception as e:
            currentFuncName=inspect.stack()[0][3]
            print(f'error in {currentFuncName}',time.time(),file=open(logFile, "a"))
            print(e,time.time(),file=open(logFile, "a"))
        print('postpythonDownload',time.time(),file=open(logFile, "a"))
def addPythonToEnvironmentalVariablesIfItsNot():
    # Get the location of the Python executable
    python_exe = sys.executable
    # Get the current value of the PATH environment variable
    path = os.environ["PATH"]
    print('path:',path,time.time(),file=open(logFile, "a"))
    # Check if the Python executable is in the PATH environment variable
    print('python_exe not in path:',python_exe not in path,file=open(logFile, "a"))
    if python_exe not in path:
        # Add the Python executable to the PATH environment variable
        os.environ["PATH"] = f"{python_exe};{path}"
    # Check if the Python executable is now in the PATH environment variable
    if python_exe in os.environ["PATH"]:
        print("Python executable added to PATH environment variable.",file=open(logFile, "a"))
    else:
        print("Python executable not added to PATH environment variable.",file=open(logFile, "a"))
def installRequirements():
    currentPath=os.getcwd()
    os.chdir(basePath)
    os.system(r"pip install -r requirements.txt")
    os.chdir(currentPath)
def downloadAndInstallLatestPython():
    latestPythonVersion=getLatestPythonVersion()
    filename=f'python-{latestPythonVersion}-amd64.exe'
    print('before downloader',file=open(logFile, "a"))
    pythonToInstallPythonHttpDownloader(filename,latestPythonVersion)
    print('before installer',file=open(logFile, "a"))
    waitForAFileToBeInstalled(filename,["/quiet", "/passive", "/norestart","InstallAllUsers=1", "PrependPath=1"])
def installPythonIfNotInstalled():
    try:
        if not isPythonInstalled():
            installedTheDefaultVersion=False
            if not notToInstalPythonDefaultVersionIfExists:
                filename=f'python-{pythonDefaultVersion}-amd64.exe'
                if doesTheFileExistsWithSizeMoreThan10Mb(filename):
                    print('before installer',file=open(logFile, "a"))
                    waitForAFileToBeInstalled(filename,["/quiet", "/passive", "/norestart","InstallAllUsers=1", "PrependPath=1"])
                    installedTheDefaultVersion=True
            if not installedTheDefaultVersion:
                downloadAndInstallLatestPython()
        print('before adding path',file=open(logFile, "a"))
        addPythonToEnvironmentalVariablesIfItsNot()
        print('before installRequirements',file=open(logFile, "a"))
        installRequirements()
    except Exception as e:
        currentFuncName=inspect.stack()[0][3]
        print(f'error in {currentFuncName}',time.time(),file=open(logFile, "a"))
        print(e,time.time(),file=open(logFile, "a"))
installPythonIfNotInstalled()