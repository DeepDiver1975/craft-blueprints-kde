import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

    def setDependencies(self):
        self.buildDependencies["dev-utils/gperf"] = None
        self.buildDependencies["dev-utils/flexbison"] = None
        self.buildDependencies["dev-utils/nodejs"] = None
        self.buildDependencies["python-modules/html5lib"] = None

        self.runtimeDependencies["libs/qt6/qtbase"] = None
        self.runtimeDependencies["libs/qt6/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt6/qtpositioning"] = None
        self.runtimeDependencies["libs/qt6/qttools"] = None
        self.runtimeDependencies["libs/qt6/qtwebchannel"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

    def _getEnv(self):
        # webengine requires enormous amounts of ram
        jobs = int(CraftCore.settings.get("Compile", "Jobs", multiprocessing.cpu_count()))
        env = {"NINJAFLAGS": f"-j{int(jobs/2)}"}
        if CraftCore.compiler.isWindows:
            # shorten the path to python
            shortDevUtils = CraftShortPath(Path(CraftCore.standardDirs.craftRoot()) / "dev-utils/").shortPath
            env["PATH"] = f"{shortDevUtils}/bin;{os.environ['PATH']}"
        return env

    def configure(self):
        with utils.ScopedEnv(self._getEnv()):
            return super().configure()

    def make(self):
        with utils.ScopedEnv(self._getEnv()):
            return super().make()
