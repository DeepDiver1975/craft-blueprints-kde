import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'https://github.com/quotient-im/libQuotient.git'

        for ver in ['0.6.7']:
            self.targets[ver] = 'https://github.com/quotient-im/libQuotient/archive/%s.tar.gz' % ver
            self.archiveNames[ver] = 'libQuotient-%s.tar.gz' % ver
            self.targetInstSrc[ver] = 'libQuotient-%s' % ver

        self.targetDigests['0.6.7'] = (['7f7c56ef5f775d38a0bd9f112f2fb7473d42d1e886d17e84d4be1afda146999658eea8691c38071fd87aec7ece52b97bc837cc98452cc698cf152003474193f2'], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = '0.6.7'
        self.description = "A Qt5 library to write cross-platform clients for Matrix"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None

class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        if CraftCore.compiler.isMSVC():
            # LINK : fatal error LNK1104: cannot open file 'Quotient.lib
            self.subinfo.options.dynamic.buildStatic = True
