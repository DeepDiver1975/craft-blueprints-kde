# -*- coding: utf-8 -*-
# Copyright Hannah von Reth <vonreth@kde.org>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

import info
import glob

class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotAndroid

    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "Documentation generation from docbook "

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/perl"] = None
        self.buildDependencies["perl-modules/xml-parser"] = None
        self.buildDependencies["perl-modules/uri-url"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["libs/libxslt"] = None
        self.runtimeDependencies["data/docbook-dtd"] = None
        self.runtimeDependencies["data/docbook-xsl"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

    def postInstall(self):
        dataDir = os.path.relpath(CraftCore.standardDirs.locations.data, CraftCore.standardDirs.craftRoot())
        brokenFiles = [os.path.join(self.installDir(), dataDir, x) for x in ["kf5/kdoctools/customization/xsl/all-l10n.xml",
                                                                             "kf5/kdoctools/customization/dtd/kdedbx45.dtd",
                                                                             "kf5/kdoctools/customization/kde-include-common.xsl",
                                                                             "kf5/kdoctools/customization/kde-include-man.xsl"]]
        return self.patchInstallPrefix(brokenFiles, OsUtils.toUnixPath(self.subinfo.buildPrefix), OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot()))

