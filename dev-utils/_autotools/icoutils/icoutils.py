import info


class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ["0.32.3"]:
            self.targets[ ver ] = f"http://savannah.nongnu.org/download/icoutils/icoutils-{ver}.tar.bz2"
            self.targetInstSrc[ ver ] = f"icoutils-{ver}"

        self.targetDigests["0.32.3"] =  (['17abe02d043a253b68b47e3af69c9fc755b895db68fdc8811786125df564c6e0'], CraftHash.HashAlgorithm.SHA256)
        self.description = "The icoutils are a set of command-line programs for extracting and converting images in Microsoft Windows(R) icon and cursor files."
        self.webpage = "http://www.nongnu.org/icoutils/"
        self.defaultTarget = "0.32.3"

    def setDependencies( self ):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/msys"] = None
        self.runtimeDependencies["libs/libpng"] = None

from Package.AutoToolsPackageBase import *

class Package(AutoToolsPackageBase):
    def __init__( self, **args ):
        AutoToolsPackageBase.__init__( self )
        self.subinfo.options.configure.autoreconf = False

