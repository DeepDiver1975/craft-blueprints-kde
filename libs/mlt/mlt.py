import info

class subinfo(info.infoclass):

    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Compiler.NoCompiler if CraftCore.compiler.isMSVC() else CraftCore.compiler.Platforms.All

    def setTargets( self ):
        self.description = "Open source multimedia framework"
        self.webpage = "https://www.mltframework.org"
        for ver in ['7.6.0']:
            self.targets[ ver ] = f"https://github.com/mltframework/mlt/archive/v{ver}.tar.gz"
            self.targetInstSrc[ ver ] = "mlt-" + ver

        self.svnTargets['master'] = "https://github.com/mltframework/mlt.git"
        self.patchLevel['master'] = 20220704
        self.svnTargets['8734714'] = "https://github.com/mltframework/mlt.git||87347147eac8adf5ecfac0c3c4ec2d4aaf041f9d"
        self.defaultTarget = '8734714'
        if CraftCore.compiler.isMacOS:
            self.patchToApply["8734714"] = [("001-fix-avformat-mac.diff", 1)]
        if CraftCore.compiler.isWindows:
            self.patchToApply["8734714"] = [("pi_patch.diff", 1)]

    def setDependencies( self ):
        self.buildDependencies["dev-utils/pkg-config"] = None
        self.buildDependencies["libs/ladspa-sdk"] = None
        self.runtimeDependencies["libs/libxml2"] = None
        self.runtimeDependencies["libs/ffmpeg"] = None
        self.runtimeDependencies["libs/qt5/qtsvg"] = None
        self.runtimeDependencies["libs/libfftw"] = None
        self.runtimeDependencies["libs/libsamplerate"] = None

        if CraftCore.compiler.isLinux:
            self.runtimeDependencies["libs/libasound2"] = None
            self.runtimeDependencies["libs/libexif"] = None
            self.runtimeDependencies["libs/movit"] = None
        if OsUtils.isWin():
            self.runtimeDependencies["libs/dlfcn-win32"] = None
        # ladspa-swh currently breaks MLT, making render impossible. So disable for now
        #else:
        #    self.runtimeDependencies["libs/ladspa-swh"] = None
        if not CraftCore.compiler.isMacOS:
            # self.runtimeDependencies["libs/jack2"] = None
            self.runtimeDependencies["libs/rubberband"] = None
            self.runtimeDependencies["libs/sox"] = None
        self.runtimeDependencies["libs/frei0r-plugins"] = None
        self.runtimeDependencies["libs/libsdl2"] = None
        self.runtimeDependencies["libs/vidstab"] = None
        self.runtimeDependencies["libs/ladspa-cmt"] = None
        self.runtimeDependencies["libs/ladspa-rnnoise"] = None
        self.runtimeDependencies["libs/ladspa-tap"] = None
        self.runtimeDependencies["libs/opencv/opencv_contrib"] = None
        self.runtimeDependencies["libs/opencv/opencv"] = None
        self.runtimeDependencies["libs/libarchive"] = None

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)
        CMakePackageBase.buildTests = False
        # enable submodule checkout to get glaximate
        self.subinfo.options.fetch.checkoutSubmodules = True
        self.subinfo.options.configure.args += [
            "-DMOD_DECKLINK=OFF",
            "-DWINDOWS_DEPLOY=OFF",
            "-DMOD_OPENCV=ON",
            "-DMOD_GLAXNIMATE=ON",
            "-DRELOCATABLE=ON",
            "-DMOD_GDK=OFF" # don't pull in gtk
        ]
        self.subinfo.options.configure.cxxflags += f" -D_XOPEN_SOURCE=700 "

    def install(self):
        if not super().install():
            return False
        if CraftCore.compiler.isMacOS:
            return utils.mergeTree(self.installDir()/"lib/mlt", self.installDir()/"plugins/mlt")
        return True

