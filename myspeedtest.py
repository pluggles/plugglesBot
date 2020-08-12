#Python progam to test and log internet speed

import speedtest
import os
import sys
import math
def AddChatId(myId):
    try:
        file = 'speedtest.txt'
        EnsureFileExists(file)
        with open(file) as f:
            lines = f.read().splitlines()
        if str(myId) in lines:
            return "This chat is already receiving internet speed info"
        else:
            lines.append(str(myId))
            f = open(file, 'w')
            for line in lines:
                f.write("%s\n" % line)
            f.close
            return "Chat will now get notified of internet speed info"
    except:
        print "error", sys.exc_info()[0]
        return "something terrible may have just happened"
def RemoveChatId(myId):
    try:
        file = 'speedtest.txt'
        EnsureFileExists(file)
        with open(file) as f:
            lines = f.read().splitlines()
        if str(myId) in lines:
            lines.remove(str(myId))
            f = open(file, 'w')
            for line in lines:
                f.write("%s\n" % line)
            f.close
            return "Chat will no longer be notified of internet speed info"
        else:
            return "This chat isn't currently getting notified of internet speed info"
            
    except:
        print "error", sys.exc_info()[0]
        return "something terrible may have just happened"
def GetChatIds():
    file = 'speedtest.txt'
    EnsureFileExists(file)
    with open(file) as f:
        lines = f.read().splitlines()
    return lines
def EnsureFileExists(filename):
    if not os.path.exists(filename):
        file(filename, 'w').close()
def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])

def get_internet_speeds():
    st = speedtest.Speedtest()
    st.get_best_server()
    download = st.download()
    upload = st.upload()
    return (convert_size(download) + " Down " + convert_size(upload) + " Up")

def main():
    print (get_internet_speeds())


if __name__ == '__main__':
    main()
