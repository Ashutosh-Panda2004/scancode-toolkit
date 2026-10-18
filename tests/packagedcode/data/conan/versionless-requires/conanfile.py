from conans import ConanFile


class MyPkg(ConanFile):
    name = "mypkg"
    version = "1.0"
    requires = "zlib"
