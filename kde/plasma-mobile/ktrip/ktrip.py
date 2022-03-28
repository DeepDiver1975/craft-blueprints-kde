import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues(gitUrl = "https://invent.kde.org/utilities/ktrip.git")
        self.description = "Public transport assistant"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt5/qtquickcontrols2"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kitemmodels"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/libs/kpublictransport"] = None
        self.runtimeDependencies["kde/unreleased/kirigami-addons"] = None
        if not CraftCore.compiler.isAndroid:
            self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None
            self.runtimeDependencies["kde/frameworks/tier3/qqc2-desktop-style"] = None
            self.runtimeDependencies["kde/plasma/breeze"] = None
        else:
            self.runtimeDependencies["libs/qt5/qtandroidextras"] = None
            self.runtimeDependencies["kde/plasma/qqc2-breeze-style"] = None

from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.defines["executable"] = r"bin\ktrip.exe"
        self.addExecutableFilter(r"(bin|libexec)/(?!(ktrip|update-mime-database)).*")
        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("libs/dbus")
