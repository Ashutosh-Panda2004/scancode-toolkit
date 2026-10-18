from conans import ConanFile


class HelperMixin:
    pass


class MyPkg(HelperMixin, ConanFile):
    name = "mypkg"
    version = "1.0"
    requires = "zlib/1.2.13"
