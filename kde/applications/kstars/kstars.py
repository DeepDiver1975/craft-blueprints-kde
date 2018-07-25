import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = 'a desktop planetarium'
        for ver in ['2.9.7']:
            self.targets[ver] = 'http://download.kde.org/stable/kstars/kstars-%s.tar.xz' % ver
            self.targetInstSrc[ver] = 'kstars-%s' % ver
        self.defaultTarget = '2.9.7'
        self.displayName = "KStars Desktop Planetarium"

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["libs/qt5/qtdeclarative"] = "default"
        self.runtimeDependencies["libs/qt5/qtquickcontrols"] = "default"
        self.runtimeDependencies["libs/qt5/qtquickcontrols2"] = "default"
        self.runtimeDependencies["libs/qt5/qtsvg"] = "default"
        self.runtimeDependencies["libs/qt5/qtdatavis3d"] = "default"
        self.runtimeDependencies["libs/qt5/qtwebsockets"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = "default"
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kwidgetsaddons"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/knewstuff"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kdbusaddons"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kinit"] = "default"
        self.runtimeDependencies["kde/frameworks/tier2/kjobwidgets"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kplotting"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/knotifications"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/knotifyconfig"] = "default"
        self.runtimeDependencies["libs/eigen3"] = "default"
        self.runtimeDependencies["libs/cfitsio"] = "default"
        self.runtimeDependencies["libs/wcslib"] = "default"
        self.runtimeDependencies["libs/indiclient"] = "default"
        self.runtimeDependencies["libs/libraw"] = "default"
        self.runtimeDependencies["libs/gsl"] = "default"
        self.runtimeDependencies["qt-libs/phonon-vlc"] = "default"
        self.runtimeDependencies["qt-libs/qtkeychain"] = "default"

        # Install proper theme
        self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.ignoredPackages.append("binary/mysql")
        self.blacklist_file = ["blacklist.txt"]

    def createPackage(self):
        self.defines["executable"] = "bin\\kstars.exe"
        #self.defines["setupname"] = "kstars-latest-win64.exe"
        self.defines["icon"] = os.path.join(self.packageDir(), "kstars.ico")

        return TypePackager.createPackage(self)
