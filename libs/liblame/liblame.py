# -*- coding: utf-8 -*-
import info
from Package.MakeFilePackageBase import MakeFilePackageBase
from CraftCompiler import CraftCompiler

class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['3.100']:
            self.targets[ver] = f'https://sourceforge.net/projects/lame/files/lame/{ver}/lame-{ver}.tar.gz'

            self.targetInstSrc[ver] = 'lame-'+ver
        self.patchToApply['3.100'] = [("lame_init_old-missing-symfile.patch", 1),
                                      ("liblame-3.100-20190112.diff", 1)]
        self.targetDigests['3.100'] = (['ddfe36cab873794038ae2c1210557ad34857a4b6bdc515785d1da9e175b1da1e'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = '3.100'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/msys"] = None
        self.buildDependencies["dev-utils/nasm"] = None


from Package.AutoToolsPackageBase import *


if CraftCore.compiler.isGCCLike():
    class Package(AutoToolsPackageBase):
        def __init__(self, **args):
            AutoToolsPackageBase.__init__(self)
            self.subinfo.options.configure.args = " --disable-static --disable-gtktest --disable-frontend --enable-nasm "
else:
    class Package(MakeFilePackageBase):
        def __init__(self):
            MakeFilePackageBase.__init__(self)
            self.subinfo.options.useShadowBuild = False
            self.subinfo.options.make.supportsMultijob = False
            self.subinfo.options.make.args += f"-f Makefile.MSVC dll comp=msvc GTK=NO CRAFT_ARCH=x{CraftCore.compiler.bits}"
            if CraftCore.compiler.architecture == CraftCompiler.Architecture.x86_64:
                self.subinfo.options.make.args += " MSVCVER=Win64 ASM=NO"
            else:
                self.subinfo.options.make.args += " ASM=YES"

        def configure(self, dummyDefines=""):
            return utils.copyFile(os.path.join(self.sourceDir(), "configMS.h"), os.path.join(self.sourceDir(), "config.h"), linkOnly=False)

        def install(self):
            return (
                    utils.copyFile(os.path.join(self.sourceDir(), "include/lame.h"), os.path.join(self.installDir(), "include/lame/lame.h"), linkOnly=False) and
                    utils.copyFile(os.path.join(self.sourceDir(), "output/lame_enc.dll"), os.path.join(self.installDir(), "bin/lame_enc.dll"), linkOnly=False) and
                    utils.copyFile(os.path.join(self.sourceDir(), "output/lame_enc.lib"), os.path.join(self.installDir(), "lib/lame_enc.lib"), linkOnly=False) and
                    utils.copyFile(os.path.join(self.sourceDir(), "output/libmp3lame.dll"), os.path.join(self.installDir(), "bin/libmp3lame.dll"), linkOnly=False) and
                    utils.copyFile(os.path.join(self.sourceDir(), "output/libmp3lame.lib"), os.path.join(self.installDir(), "lib/libmp3lame.lib"), linkOnly=False)

            )

