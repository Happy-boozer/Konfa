import tarfile
def echo(*args):
    print(*args)
    #return args

def ls():
    tar = tarfile.open("nry.tar")
    namelist = tar.getnames()
    for file in namelist:
        print(file)
