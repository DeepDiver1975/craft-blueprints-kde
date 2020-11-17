import info


class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ["3.4.1", "4.1", "4.2"]:
            self.targets[ ver ] = f"https://ffmpeg.org/releases/ffmpeg-{ver}.tar.bz2"
            self.targetInstSrc[ ver ] = f"ffmpeg-{ver}"
        self.svnTargets['master'] = "https://git.ffmpeg.org/ffmpeg.git"
        self.targetDigests["3.4.1"] = (['f3443e20154a590ab8a9eef7bc951e8731425efc75b44ff4bee31d8a7a574a2c'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["4.1"] = (['b684fb43244a5c4caae652af9022ed5d85ce15210835bce054a33fb26033a1a5'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["4.2"] = (['306bde5f411e9ee04352d1d3de41bd3de986e42e2af2a4c44052dce1ada26fb8'], CraftHash.HashAlgorithm.SHA256)

        if CraftCore.compiler.isMSVC():
            self.patchToApply["4.1"] = [("ffmpeg-4.1-20190507.diff", 1)]
            self.patchToApply["4.2"] = [("ffmpeg-4.1-20190507.diff", 1)]

        self.description = "A complete, cross-platform solution to record, convert and stream audio and video."
        self.webpage = "https://ffmpeg.org/"
        self.defaultTarget = "4.2"

    def setDependencies( self ):
        self.buildDependencies["dev-utils/msys"] = None
        self.buildDependencies["dev-utils/nasm"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/liblame"] = None
        self.runtimeDependencies["libs/libopus"] = None
        if CraftCore.compiler.isGCCLike():
            self.runtimeDependencies["libs/libsdl2"] = None
            self.runtimeDependencies["libs/libvorbis"] = None
            self.runtimeDependencies["libs/libvpx"] = None
            self.runtimeDependencies["libs/x264"] = None
            self.runtimeDependencies["libs/x265"] = None
            self.runtimeDependencies["libs/libass"] = None

from Package.AutoToolsPackageBase import *

class Package(AutoToolsPackageBase):
    def __init__( self, **args ):
        AutoToolsPackageBase.__init__( self )
        self.platform = ""
        self.subinfo.options.configure.noDataRootDir = True
        self.subinfo.options.configure.autoreconf = False
        # with msvc it does not support shadowbuilds
        self.subinfo.options.useShadowBuild = not CraftCore.compiler.isMSVC()

        self.subinfo.options.configure.args = "--enable-shared --disable-debug --disable-doc --enable-gpl " \
                                              "--enable-version3 --enable-avresample --enable-libmp3lame "
        if CraftCore.compiler.isMSVC():
            self.subinfo.options.configure.cflags += " -FS"
            self.subinfo.options.configure.cxxflags += " -FS"
            self.subinfo.options.configure.args += " --toolchain=msvc "
        else:
            # vorbis.pc & ogg.pc currently not generated by patch to use CMake
            self.subinfo.options.configure.args += " --enable-libopus --enable-libvorbis " \
                                                   "--enable-libvpx --enable-libx264 --enable-libx265 --enable-libass "

    def configure(self):
        with utils.ScopedEnv(self._ffmpegEnv()):
            return super().configure()

    def make(self, dummyBuildType=None):
        with utils.ScopedEnv(self._ffmpegEnv()):
            return super().make()

    def install(self):
        if not super().install():
            return False

        if OsUtils.isWin():
            for file in ['avcodec', 'avdevice', 'avfilter', 'avformat', 'avresample', 'avutil', 'postproc', 'swresample', 'swscale']:
                file += ".lib"
                src = os.path.join(self.installDir(), 'bin', file)
                if os.path.isfile(src):
                    os.rename(src, os.path.join(self.installDir(), 'lib', file))

        return True

    def _ffmpegEnv(self):
        if not CraftCore.compiler.isMSVC():
            return {}
        return { "LIB" : f"{os.environ['LIB']};{os.path.join(CraftStandardDirs.craftRoot() , 'lib')}",
                 "INCLUDE" : f"{os.environ['INCLUDE']};{os.path.join(CraftStandardDirs.craftRoot() , 'include')}"}

