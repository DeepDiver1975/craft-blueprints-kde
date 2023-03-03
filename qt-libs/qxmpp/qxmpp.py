# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        if self.options.isActive("libs/qt5/qtbase"):
            self.runtimeDependencies["libs/qt5/qtbase"] = None
            self.buildDependencies["libs/qt5/qttools"] = None
        else:
            self.runtimeDependencies["libs/qt6/qtbase"] = None
            self.buildDependencies["libs/qt6/qttools"] = None
            self.buildDependencies["libs/qt6/qt5compat"] = None

    def setTargets(self):
        self.svnTargets['master'] = 'https://github.com/qxmpp-project/qxmpp.git'
        for ver in ["1.5.2"]:
            self.targets[ver] = f"https://github.com/qxmpp-project/qxmpp/archive/v{ver}.tar.gz"
            self.archiveNames[ver] = f"qxmpp-v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"qxmpp-{ver}"
            self.patchToApply[ver] = [("0001-Install-dll-to-bindir-on-windows.patch", 1)]
        self.targetDigests['1.5.2'] = (
            ['cc26345428d816bb33e63f92290c52b9a417d9a836bf9fabf295e3477f71e66c'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = '1.5.2'


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

        self.subinfo.options.configure.args = "-DBUILD_EXAMPLES=OFF -DBUILD_TESTS=OFF"
