import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "Interactive Physical Simulator"
        self.webpage = "https://edu.kde.org/step"
        # 22.04.3 not working for MSVC
        if CraftCore.compiler.isMSVC():
            self.defaultTarget = 'master'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kplotting"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knewstuff"] = None
        self.runtimeDependencies["kde/frameworks/tier3/ktextwidgets"] = None
        
        #self.runtimeDependencies["libs/gsl"] = None

from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

    def createPackage(self):
        self.blacklist_file.append(os.path.join(self.packageDir(), 'blacklist.txt'))

        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("libs/dbus")

        self.defines["appname"] = "step"
        self.defines["website"] = "https://apps.kde.org/step"
        self.defines["executable"] = "bin\\step.exe"
        self.defines["shortcuts"] = [{"name" : "Step", "target" : "bin/step.exe", "description" : self.subinfo.description, "icon" : "$INSTDIR\\step.ico" }]
        self.defines["icon"] = os.path.join(self.packageDir(), "step.ico")

        return TypePackager.createPackage(self)
