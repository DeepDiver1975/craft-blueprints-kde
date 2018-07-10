# -*- coding: utf-8 -*-

import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'https://github.com/KDAB/Charm.git'
        for ver in ["1.12.0"]:
            self.targets[ver] = f"https://github.com/KDAB/Charm/archive/{ver}.tar.gz"
            self.archiveNames[ver] = f"charm-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"Charm-{ver}"
        self.defaultTarget = "1.12.0"

        self.description = "The Cross-Platform Time Tracker"
        self.displayName = "Charm"

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["libs/qt5/qtwinextras"] = "default"
        self.runtimeDependencies["libs/qt5/qtmacextras"] = "default"
        self.runtimeDependencies["qt-libs/qtkeychain"] = "default"


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        if self.subinfo.buildTarget != "master":
           self.subinfo.options.configure.args = f"-DCharm_VERSION={self.subinfo.buildTarget}"

    def createPackage(self):
        self.blacklist_file.append(os.path.join(self.packageDir(), 'blacklist.txt'))
        self.defines["company"] = "Klarälvdalens Datakonsult AB"
        self.defines["executable"] = "bin\\Charm.exe"
        self.defines["license"] = os.path.join(self.sourceDir(), "License.txt")
        self.defines["icon"] = os.path.join(self.sourceDir(), "Charm", "Icons", "Charm.ico")
        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("libs/dbus")
        return TypePackager.createPackage(self)

