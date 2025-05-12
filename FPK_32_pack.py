import os
import struct

en = False
cn = './CN\\'
newarc = 'data.cn_'
if not os.path.exists(cn):
    os.mkdir(cn)
files = os.listdir(cn)
filecont = len(files)
print(hex(filecont))
f = open(newarc, 'wb')
c = 0
f.write(struct.pack('I', filecont + c))
pos = 4 + filecont * 32
data = b''
for file in files:
    size = os.stat(cn + file).st_size
    nl = len(file.encode('cp932'))
    null = (24 - nl) * b'\x00'
    data = data + struct.pack('i', pos)
    data = data + struct.pack('i', size)
    data = data + file.encode('CP932')
    data = data + null
    pos = pos + size
f.write(data)
for file in files:
    f1 = open(cn + file, 'rb')
    b = f1.read()
    f1.close()
    f.write(b)
f.close()
