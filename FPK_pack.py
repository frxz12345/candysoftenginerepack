import struct, os

game = 'ねえちゃん、もう出ちゃうよ！～淫姉は俺の愛玩具～'
oldarc = 'data.fpk'
nowarc = 'data.cn_'
cn = './CN\\'
en = False
def from_bytes(a: bytes):
    return int.from_bytes(a, byteorder='little')
def name():
    f = open(oldarc, 'rb')
    b = f.read()
    f.close()
    f = open('1', 'wb')
    key = b[-8:-4]
    indexpos = from_bytes(b[-4:])
    x = 0x80000000
    filecount = from_bytes(b[0:4])-x
    print(filecount)
    print(key)
    b =b[indexpos:indexpos+filecount*36]
    for i in range(len(b)):
        x = b[i]
        x = x ^ (key[i % 4])
        f.write(struct.pack('B', x))
    f.close()
files = os.listdir(cn)
filecount = len(files)
print(hex(filecount))
f = open('data.cn_', 'wb')
c = 0X80000000
print(hex((c+filecount)))
f.write(struct.pack('I', filecount + c))
pos = 4 + filecount * 36
print(hex(pos))
data = b''
f1 = open('1','rb')
fs = len(files) *[b'\x00']
key = bytes.fromhex('FF FF FF FF')
for i in range(len(files)):
    f1.read(8)
    files[i] = f1.read(24).decode('CP932')
    files[i] = files[i].replace('\x00','')
    fs[i] = f1.read(4)
f1.close()
i=0
for file in files:
    size = os.stat(cn + file).st_size
    nl = len(file.encode('cp932'))
    null = (24 - nl) * b'\x00'
    data = data + struct.pack('i', pos)
    data = data + struct.pack('i', size)
    data = data + file.encode('CP932')
    data = data + null
    data = data + fs[i]
    i = i + 1
    pos = pos + size
pos = 0
if en:
    for i in range(len(data)):
        d = data[i]^key[i%len(key)]
        d = struct.pack('B',d)
        f.write(d)
else:
    f.write(data)
for file in files:
    f1 = open(cn + file, 'rb')
    b = f1.read()
    f1.close()
    f.write(b)
if en:
    f.write(key)#加密文件名
else:
    f.write(b'\x00'*4)  #不加密文件名
f.write(struct.pack('i', 4))#索引位置
f.close()
