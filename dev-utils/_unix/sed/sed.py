# -*- coding: utf-8 -*-
import info
from Package.AutoToolsPackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.buildDependencies["dev-utils/msys"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["dev-utils/m4"] = None
        self.buildDependencies["libs/gettext"] = None

    def setTargets(self):
        self.description = "sed (stream editor) is a non-interactive command-line text editor."
        for ver in ["4.7"]:
            self.targets[ver] = f"http://ftp.gnu.org/gnu/sed/sed-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"sed-{ver}"
        self.targetDigests["4.7"] = (['2885768cd0a29ff8d58a6280a270ff161f6a3deb5690b2be6c49f46d4c67bd6a'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "4.7"

class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args += " --disable-static --enable-shared"
