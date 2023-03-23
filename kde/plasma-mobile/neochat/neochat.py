import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues(gitUrl = "https://invent.kde.org/network/neochat.git")

        self.displayName = "NeoChat"
        self.description = "A client for matrix, the decentralized communication protocol."

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt5/qtquickcontrols2"] = None
        self.runtimeDependencies["libs/qt5/qtmultimedia"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kitemmodels"] = None
        self.runtimeDependencies["kde/frameworks/tier1/syntax-highlighting"] = None
        self.runtimeDependencies["kde/frameworks/tier1/sonnet"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kquickcharts"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifications"] = None
        self.runtimeDependencies["qt-libs/libquotient"] = None
        self.runtimeDependencies["libs/cmark"] = None
        self.runtimeDependencies["kde/libs/kquickimageeditor"] = None
        self.runtimeDependencies["qt-libs/qcoro"] = None
        self.runtimeDependencies["kde/unreleased/kirigami-addons"] = None
        if not CraftCore.compiler.isAndroid:
            self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None
            self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
            self.runtimeDependencies["kde/frameworks/tier3/qqc2-desktop-style"] = None
            self.runtimeDependencies["kde/plasma/breeze"] = None
        else:
            self.runtimeDependencies["kde/plasma/qqc2-breeze-style"] = None


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = "-DBUILD_TESTING=OFF"

    def createPackage(self):
        self.blacklist_file.append(os.path.join(self.packageDir(), 'blacklist.txt'))
        self.defines["shortcuts"] = [{"name" : "NeoChat", "target":"bin/neochat.exe", "appId": "neochat", "icon": self.buildDir() / "src/NEOCHAT_ICON.ico"}]
        self.defines["icon"] = self.buildDir() / "src/NEOCHAT_ICON.ico"
        # set the icons for the appx bundle
        if os.path.exists(os.path.join(self.sourceDir(), "icons", "150-apps-neochat.png")):
            self.defines["icon_png"] = os.path.join(self.sourceDir(), "icons", "150-apps-neochat.png")
            self.defines["icon_png_44"] = os.path.join(self.sourceDir(), "icons", "44-apps-neochat.png")
        else:
            self.defines["icon_png"] = os.path.join(self.packageDir(), "150-apps-neochat.png")
            self.defines["icon_png_44"] = os.path.join(self.packageDir(), "44-apps-neochat.png")
        self.addExecutableFilter(r"(bin|libexec)/(?!(neochat|update-mime-database|snoretoast)).*")
        self.ignoredPackages.append("binary/mysql")
        if not CraftCore.compiler.isLinux:
            self.ignoredPackages.append("libs/dbus")
        return super().createPackage()
