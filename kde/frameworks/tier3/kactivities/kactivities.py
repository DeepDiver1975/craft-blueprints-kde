import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Runtime and library to organize the user work in separate activities"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kservice"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["libs/boost/boost-headers"] = None

        # those are only needed for building the activity manager daemon


# self.runtimeDependencies['libs/boost-range'] = 'default'
#        self.runtimeDependencies['libs/boost-containers'] = 'default'

from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = "-DKACTIVITIES_LIBRARY_ONLY=YES"
