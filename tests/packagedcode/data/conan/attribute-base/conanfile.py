import conan


class MyPkg(conan.ConanFile):
    name = "mypkg"
    version = "1.0"
    requires = "zlib/1.2.13"
