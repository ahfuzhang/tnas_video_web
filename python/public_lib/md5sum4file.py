# fast md5sum
import sys, os, os.path
import hashlib
import mmap

def md5sum(file_path, size):
    if size<0:
        raise Exception('size error [%d]'%size)
    if not os.path.exists(file_path):
        return None
    f = open(file_path, 'rb')
    if f is None:
        return None
    m = mmap.mmap(f.fileno(), size, mmap.MAP_SHARED, mmap.PROT_READ)
    md5 = hashlib.md5()
    if size==0:
        size = m.size()
    md5.update(m[:size])
    m.close()
    f.close()
    return md5.digest()

if __name__=='__main__':
    if len(sys.argv)<2:
        print('usage:%s <file> [size=0]')
        sys.exit(-1)
    size = 0
    if len(sys.argv)>=3:
        size = long(sys.argv[2])
    print(md5sum(sys.argv[1], size).hex() )
