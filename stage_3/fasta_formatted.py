f  = open("humansX.txt", "r")
fw = open("outputX.fa", "w")


import re
counter = 1


for line in f:
    ret = ">h^{}".format(counter)
    #print(ret)
    sfrep = line.replace("h^1", ret + "\n")
    sfrep = sfrep + "\n"
    counter += 1
    print sfrep
    fw.write(sfrep)
