import info


# deprecated class
class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['svnHEAD'] = 'https://libface.svn.sourceforge.net/svnroot/libface/trunk'
        self.defaultTarget = 'svnHEAD'
        self.patchToApply['svnHEAD'] = ('libface-20120122.patch', 1)

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/opencv"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
