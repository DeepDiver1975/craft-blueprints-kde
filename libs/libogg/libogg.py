import info

from Package.CMakePackageBase import *
from Package.AutoToolsPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['1.2.0', '1.3.0', '1.3.1', '1.3.3']:
            self.targets[ver] = 'http://downloads.xiph.org/releases/ogg/libogg-' + ver + '.tar.gz'
            self.targetInstSrc[ver] = 'libogg-' + ver
            self.patchToApply[ver] = ('libogg-1.2.0-20100707.diff', 1)
        self.targetDigests['1.2.0'] = '135fb812282e08833295c91e005bd0258fff9098'
        self.targetDigests['1.3.0'] = 'a900af21b6d7db1c7aa74eb0c39589ed9db991b8'
        self.targetDigests['1.3.1'] = '270685c2a3d9dc6c98372627af99868aa4b4db53'
        self.targetDigests['1.3.3'] = (['c2e8a485110b97550f453226ec644ebac6cb29d1caef2902c007edab4308d985'], CraftHash.HashAlgorithm.SHA256)

        self.description = "reference implementation for the ogg audio file format"
        self.defaultTarget = '1.3.3'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


if CraftCore.compiler.isGCCLike:
    class Package(AutoToolsPackageBase):
        def __init__(self):
            AutoToolsPackageBase.__init__(self)
else:
    class Package(CMakePackageBase):
        def __init__(self):
            CMakePackageBase.__init__(self)

