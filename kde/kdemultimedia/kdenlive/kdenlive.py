import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "Libre Video Editor, by KDE community"

    def setDependencies(self):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtmultimedia"] = None
        self.runtimeDependencies["libs/qt5/qtspeech"] = None
        self.runtimeDependencies["libs/qt5/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt5/qtquickcontrols"] = None
        self.runtimeDependencies["libs/qt5/qtquickcontrols2"] = None
        self.runtimeDependencies["libs/qt5/qtnetworkauth"] = None
        self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kguiaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kitemviews"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kplotting"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwidgetsaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcompletion"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kjobwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kdeclarative"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kbookmarks"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kconfigwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        if not CraftCore.compiler.isWindows:
            self.runtimeDependencies["kde/kdenetwork/kio-extras"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knewstuff"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifications"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifyconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kservice"] = None
        self.runtimeDependencies["kde/frameworks/tier3/ktextwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kinit"] = None
        self.runtimeDependencies["kde/frameworks/tier3/purpose"] = None
        self.runtimeDependencies["libs/ffmpeg"] = None
        self.runtimeDependencies["libs/mlt"] = "master"
        self.runtimeDependencies["kde/plasma/breeze"] = None
        if not CraftCore.compiler.isMacOS:
            self.runtimeDependencies["libs/frei0r-bigsh0t"] = None
        # if CraftCore.compiler.isWindows:
        #     self.runtimeDependencies["libs/drmingw"] = None
        if CraftCore.compiler.isLinux:
            self.runtimeDependencies["kde/plasma/drkonqi"] = None


from Package.CMakePackageBase import *
from Utils import GetFiles

class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args += " -DCMAKE_DISABLE_FIND_PACKAGE_KF5FileMetaData=ON"
        if self.buildTarget == "master" or self.buildTarget >= CraftVersion("21.11.70"):
            self.subinfo.options.configure.args += " -DNODBUS=ON"
        if self.buildTarget == "master":
            self.subinfo.options.configure.args += " -DRELEASE_BUILD=OFF"

    def setDefaults(self, defines: {str:str}) -> {str:str}:
        defines = super().setDefaults(defines)
        if isinstance(self, AppImagePackager):
            defines["runenv"] += [
                'TEST=hello',
                'PACKAGE_TYPE=appimage',
                'KDE_FORK_SLAVES=1',
                'FONTCONFIG_PATH=/etc/fonts',
                'LD_LIBRARY_PATH=$this_dir/usr/lib/:$LD_LIBRARY_PATH',
                'MLT_REPOSITORY=$this_dir/usr/lib/mlt-7/',
                'MLT_DATA=$this_dir/usr/share/mlt-7/',
                'MLT_ROOT_DIR=$this_dir/usr/',
                'LADSPA_PATH=$this_dir/usr/lib/ladspa',
                'FREI0R_PATH=$this_dir/usr/lib/frei0r-1',
                'MLT_PROFILES_PATH=$this_dir/usr/share/mlt-7/profiles/',
                'MLT_PRESETS_PATH=$this_dir/usr/share/mlt-7/presets/',
                'SDL_AUDIODRIVER=pulseaudio']
        return defines

    def createPackage(self):
        if not CraftCore.compiler.isMacOS:
            self.blacklist_file.append(os.path.join(self.packageDir(), 'exclude.list'))
        if self.buildTarget == "master" or self.buildTarget >= CraftVersion("21.11.70"):
            self.addExecutableFilter(r"bin/(?!(ff|kdenlive|kioslave|melt|update-mime-database|data/kdenlive)).*")
        else:
            self.addExecutableFilter(r"bin/(?!(dbus-daemon|ff|kdenlive|kioslave|melt|update-mime-database|data/kdenlive)).*")
        self.ignoredPackages.append("libs/llvm-meta")
        self.ignoredPackages.append("data/hunspell-dictionaries")
        self.ignoredPackages.append("binary/mysql")

        self.defines["appname"] = "kdenlive"
        self.defines["icon"] = os.path.join(self.sourceDir(), "data", "icons", "kdenlive.ico")
        self.defines["icon_png"] = os.path.join(self.sourceDir(), "data", "icons", "128-apps-kdenlive.png")
        self.defines["shortcuts"] = [{"name" : "Kdenlive", "target":"bin/kdenlive.exe", "description" : self.subinfo.description}]
        self.defines["mimetypes"] = ["application/x-kdenlive"]
        self.defines["file_types"] = [".kdenlive"]
        return super().createPackage()

    def postInstall(self):
        if CraftCore.compiler.isWindows:
            self.schemeDir = os.path.join(self.installDir(), 'bin', 'data', 'color-schemes')
        else:
            self.schemeDir = os.path.join(self.installDir(), 'share', 'color-schemes')
        for scheme in ['BreezeClassic', 'BreezeDark', 'BreezeLight']:
            GetFiles.getFile('https://invent.kde.org/plasma/breeze/-/raw/master/colors/'+scheme+'.colors', self.schemeDir)
        for scheme in ['RustedBronze']:
            GetFiles.getFile('https://raw.githubusercontent.com/Bartoloni/RustedBronze/master/'+scheme+'.colors', self.schemeDir)
        return True

