# GnuPG - Windows development package
#
# This Package contains the headers and libraries for the gnupg software:
#
# libgpg-error-1.8
# libgcrypt-1.4.5
# libassuan-2.0.0
# libksba-1.0.7
# gpgme-1.3.0
#
# The intention is that they should keep up with the recent versions of gpg4win
# (www.gpg4win.de) which packages gnupg seperatly so KDE software can interact
# with gpg4win.

import glob

import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        version = "20130507"
        self.targets[version] = \
            "http://files.kolab.org/local/gpg4win/gpg4win-dev-" + version + ".tar.bz2"
        self.defaultTarget = version
        self.targetDigests[version] = '0e0c6ae454e85d682a7c88b95f95d37bd9f3b03d'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.package.packSources = False

    def compile(self):
        return True

    def install(self):
        if (not self.cleanImage()):
            return False
            # This package is built with MinGW gcc, since the msvc expects a different
            # Name it shall get it.
        if CraftCore.compiler.isMSVC():
            gcc_names = glob.glob(self.sourceDir() + '/lib/*.dll.a')
            for gcc_name in gcc_names:
                msvc_name = gcc_name.replace(".dll.a", ".lib")
                shutil.move(gcc_name, msvc_name)
        shutil.copytree(self.sourceDir(), self.installDir())
        return True
