__author__ = 'wangxiunian'

import os


def getFile(files):
    for inputPath in files:
        f = open(inputPath)
        dic = {}
        p = 0
        while 1:
            p += 1
            line = f.readline()
            if not line:
                break
            pass
            if line.startswith("interface.log."):
                flag = ' [default'
                position = line.find(flag)
                if dic.has_key(line[position - 23:position]):
                    dic[line[position - 23:position] + '_0' + str(p)] = line
                else:
                    dic[line[position - 23:position]] = line
            else:
                print(line)
        f.close()
        sortedDic = sorted(dic.items(), key=lambda dic: dic[0])
        outputPath = inputPath[0: len(inputPath) - len(inputPath.split(".")[-1]) - 1] + "_out.txt"
        out_f = open(outputPath, 'a')
        for (d, x) in sortedDic:
            out_f.writelines(x)
        out_f.close()


def scan_files(directory, prefix=None, postfix=None):
    files_list = []
    root = os.listdir(directory)
    for i in root:
        if os.path.isfile(os.path.join(directory, i)):
            if i.endswith(postfix):
                files_list.append(os.path.join(directory, i))
    return files_list


getFile(scan_files("../", None, ".txt"))