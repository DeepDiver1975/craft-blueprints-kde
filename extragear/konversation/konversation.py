# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['1.7'] = 'git://anongit.kde.org/konversation|1.7'
        self.svnTargets['master'] = 'git://anongit.kde.org/konversation|master'
        for ver in ['1.7.4']:
            self.targets[ver] = 'http://download.kde.org/stable/konversation/%s/src/konversation-%s.tar.xz' % (ver, ver)
            self.targetInstSrc[ver] = 'konversation-%s' % ver
        self.defaultTarget = '1.7.4'

        self.displayName = "Konversation"
        self.description = "a KDE based irc client"

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kbookmarks"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kconfigwidgets"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kemoticons"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kidletime"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/knotifyconfig"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kparts"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/solid"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/sonnet"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kwallet"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kwidgetsaddons"] = "default"
        self.runtimeDependencies["kdesupport/qca"] = "default"
        self.runtimeDependencies["qt-libs/phonon"] = "default"


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.blacklist_file = [
            PackagerLists.runtimeBlacklist,
            os.path.join(os.path.dirname(__file__), 'blacklist.txt')
        ]

    def createPackage(self):
        self.defines["executable"] = "bin\\konversation.exe"
        self.defines["icon"] = os.path.join(os.path.dirname(__file__), "konversation.ico")

        self.ignoredPackages.append("binary/mysql")

        return TypePackager.createPackage(self)
