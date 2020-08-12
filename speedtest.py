#Python progam to test and log internet speed

import speedtest
import math

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
