import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['10.37']:
            self.targets[ver] = f"https://github.com/PhilipHazel/pcre2/releases/download/pcre2-{ver}/pcre2-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"pcre2-{ver}"

        self.patchToApply["10.37"] = [("pcre2-10.37-20211120.diff", 1)]
        self.targetDigests["10.37"] = (['04e214c0c40a97b8a5c2b4ae88a3aa8a93e6f2e45c6b3534ddac351f26548577'], CraftHash.HashAlgorithm.SHA256)
        self.patchLevel["10.37"] = 2

        self.description = "Perl-Compatible Regular Expressions (version2)"
        self.defaultTarget = '10.37'

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libbzip2"] = None
        self.runtimeDependencies["libs/zlib"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args += " -DBUILD_SHARED_LIBS=ON -DPCRE2_BUILD_PCRE2_16=ON -DPCRE2_BUILD_PCRE2_32=ON"
