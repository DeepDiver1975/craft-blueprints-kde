import info
from CraftOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets(self):
        versions = ['3.1', 'master']
        for ver in versions:
            self.svnTargets[ver] = f"git://anongit.kde.org/kexi|{ver}"
        self.defaultTarget = versions[0]
        self.description = "A visual database applications builder"
        self.displayName = "KEXI"
        self.options.configure.args = " -DBUILD_EXAMPLES=ON"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/glib"] = None # mdb
        self.runtimeDependencies["libs/sqlite"] = None # migration
        self.runtimeDependencies["binary/mysql"] = None # migration
        #TODO self.runtimeDependencies["binary/postgresql"] = None # migration
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtwebkit"] = None
        self.runtimeDependencies["kdesupport/kdewin"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcodecs"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kguiaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwidgetsaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kconfigwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier3/ktextwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["extragear/kdb"] = None
        self.runtimeDependencies["extragear/kproperty"] = None
        self.runtimeDependencies["extragear/kreport"] = None
        # Desktop only:
        self.runtimeDependencies["kde/frameworks/tier2/kcompletion"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier3/ktexteditor"] = None
        self.runtimeDependencies["kde/frameworks/tier3/ktextwidgets"] = None
        if OsUtils.isLinux():
            self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

    def createPackage(self):
        # TODO
        #self.blacklist_file.append(os.path.join(self.packageDir(), 'blacklist.txt'))
        self.defines["executable"] = "bin\\kexi.exe"
        #self.defines["icon"] = os.path.join(self.packageDir(), "kexi.ico")
        # TODO:  find a way to extend the default script
        #self.scriptname = os.path.join(self.packageDir(), "NullsoftInstaller.nsi")
        #self.ignoredPackages.append("binary/mysql")

        return TypePackager.createPackage(self)
