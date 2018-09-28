import info

from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['0.9.26', '0.9.30']:
            self.targets[ver] = 'http://download.librdf.org/source/rasqal-' + ver + '.tar.gz'
            self.targetInstSrc[ver] = 'rasqal-' + ver
        self.patchToApply['0.9.26'] = ('rasqal-0.9.26-20130523.diff', 1)
        self.targetDigests['0.9.26'] = '5496312158c0569bc047b4cab85604a06f116555'
        self.patchToApply['0.9.30'] = ('rasqal-0.9.30-20130831.diff', 1)
        self.targetDigests['0.9.30'] = '8e104acd68fca9b3b97331746e08d53d07d2e20a'
        self.description = "Rasqal RDF Query Library - for executing RDF queries"
        self.defaultTarget = '0.9.30'

    def setDependencies(self):
        self.runtimeDependencies["libs/yajl"] = None
        self.runtimeDependencies["libs/expat"] = None
        self.runtimeDependencies["libs/libcurl"] = None
        self.runtimeDependencies["libs/pcre"] = None
        self.runtimeDependencies["libs/libxml2"] = None
        self.runtimeDependencies["libs/libxslt"] = None
        self.runtimeDependencies["libs/raptor2"] = None
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
