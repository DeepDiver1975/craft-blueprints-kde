# -*- coding: utf-8 -*-
import info
from Package.AutoToolsPackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.buildDependencies["dev-utils/msys"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["dev-utils/m4"] = None
        self.buildDependencies["dev-utils/sed"] = None
        self.buildDependencies["dev-utils/help2man"] = None
        self.buildDependencies["libs/gettext"] = None

    def setTargets(self):
        self.description = "Bison is a general-purpose parser generator that converts an annotated context-free grammar into a deterministic LR or generalized LR (GLR) parser employing LALR(1) parser tables"
        self.svnTargets['master'] = 'git://git.savannah.gnu.org/bison.git'
        for ver in ["3.0.4", "3.3.2"]:
            self.targets[ver] = f"http://ftp.gnu.org/gnu/bison/bison-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"bison-{ver}"
        self.patchToApply["3.0.4"] = [("vasnprintf-macos.diff", 1), ("bison-3.0.4-20180904.diff", 1)]
        self.patchToApply["3.3.2"] = [("bison-3.0.4-20180904.diff", 1)]
        self.targetDigests["3.0.4"] = (['a72428c7917bdf9fa93cb8181c971b6e22834125848cf1d03ce10b1bb0716fe1'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["3.3.2"] = (['039ee45b61d95e5003e7e8376f9080001b4066ff357bde271b7faace53b9d804'], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "3.3.2"

class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        # TODO: why is autoreconf broken
        self.subinfo.options.configure.autoreconf = False
        self.subinfo.options.configure.args += " --disable-static --enable-shared"

    def postInstall(self):
        hardCoded = [os.path.join(self.imageDir(), x) for x in ["bin/yacc"]]
        return self.patchInstallPrefix(hardCoded, self.subinfo.buildPrefix, CraftCore.standardDirs.craftRoot())

