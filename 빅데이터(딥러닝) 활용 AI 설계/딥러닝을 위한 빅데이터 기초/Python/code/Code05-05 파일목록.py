import os
for dirName, subDirList, fnames in os.walk("images\\") :
    for fname in fnames :
        if os.path.splitext(fname)[1].upper() == ".GIF" :
            print(os.path.join(dirName, fname))
