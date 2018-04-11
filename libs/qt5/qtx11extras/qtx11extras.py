# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.Linux

    def setTargets(self):
        self.versionInfo.setDefaultValues()

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["libs/qt5/qtdeclarative"] = "default"


from Package.Qt5CorePackageBase import *


class QtPackage(Qt5CorePackageBase):
    def __init__(self, **args):
        Qt5CorePackageBase.__init__(self)


class Package(Qt5CoreSdkPackageBase):
    def __init__(self):
        Qt5CoreSdkPackageBase.__init__(self, classA=QtPackage)
