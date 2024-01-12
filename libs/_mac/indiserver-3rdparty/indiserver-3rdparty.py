import glob
from xml.etree import ElementTree as et

import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "INDI Library 3rd Party"
        self.svnTargets["master"] = "https://github.com/indilib/indi-3rdparty.git"
        self.targetInstSrc["master"] = ""

        ver = "v2.0.5"
        self.svnTargets["stable"] = "https://github.com/indilib/indi-3rdparty/archive/refs/tags/v%s.tar.gz" % ver
        self.archiveNames["stable"] = "indi-%s.tar.gz" % ver
        self.targetInstSrc["stable"] = ""

        self.defaultTarget = "master"

    def setDependencies(self):
        self.buildDependencies["dev-utils/grep"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/libnova"] = None
        self.runtimeDependencies["libs/cfitsio"] = None
        self.runtimeDependencies["libs/libcurl"] = None
        self.runtimeDependencies["libs/libgphoto2"] = None
        self.runtimeDependencies["libs/libftdi"] = None
        self.runtimeDependencies["libs/libdc1394"] = None
        self.runtimeDependencies["libs/libraw"] = None
        self.runtimeDependencies["libs/tiff"] = None
        self.runtimeDependencies["libs/libfftw"] = None
        self.runtimeDependencies["libs/ffmpeg"] = None
        self.runtimeDependencies["libs/indiserver"] = None
        self.runtimeDependencies["libs/indiserver-3rdparty-libraries"] = None
        self.runtimeDependencies["libs/librtlsdr"] = None
        self.runtimeDependencies["libs/limesuite"] = None
        self.runtimeDependencies["libs/opencv/opencv"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def fixLibraryFolder(self, folder):
        craftLibDir = os.path.join(CraftCore.standardDirs.craftRoot(), "lib")
        for library in utils.filterDirectoryContent(str(folder)):
            for path in utils.getLibraryDeps(str(library)):
                if path.startswith(craftLibDir):
                    utils.system(["install_name_tool", "-change", path, os.path.join("@rpath", os.path.basename(path)), library])
            utils.system(["install_name_tool", "-add_rpath", craftLibDir, library])

    def __init__(self):
        super().__init__()
        self.subinfo.options.package.disableStriping = True
        root = str(CraftCore.standardDirs.craftRoot())
        craftLibDir = os.path.join(root, "lib")
        # Avalon Universal Drivers is off because we do not have recipe yet for libzmq3 library.
        self.subinfo.options.configure.args = (
            "-DCMAKE_INSTALL_PREFIX="
            + root
            + " -DCMAKE_BUILD_TYPE=RelWithDebInfo -DWITH_AVALONUD=Off -DCMAKE_MACOSX_RPATH=1 -DCMAKE_INSTALL_RPATH="
            + craftLibDir
        )

    def install(self):
        ret = CMakePackageBase.install(self)
        if OsUtils.isMac():
            self.fixLibraryFolder(os.path.join(str(self.imageDir()), "bin"))
        return ret
