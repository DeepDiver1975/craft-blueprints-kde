# -*- coding: utf-8 -*-
# Copyright 2018 Łukasz Wojniłowicz <lukasz.wojnilowicz@gmail.com>
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

from Package.AutoToolsPackageBase import *
from Package.PackageBase import *
from Package.VirtualPackageBase import VirtualPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["3.4"]:
            self.targets[ver] = "http://www.lysator.liu.se/~nisse/archive/nettle-%s.tar.gz" % ver
            self.targetInstSrc[ver] = "nettle-%s" % ver

        self.targetDigests['3.4'] = (['ae7a42df026550b85daca8389b6a60ba6313b0567f374392e54918588a411e94'], CraftHash.HashAlgorithm.SHA256)

        self.description = "A low-level cryptographic library"
        self.defaultTarget = "3.4"

    def setDependencies(self):
        self.runtimeDependencies["libs/libgmp"] = "default"
        self.runtimeDependencies["libs/openssl"] = "default"
        if CraftCore.compiler.isMinGW():
            self.buildDependencies["dev-utils/msys"] = "default"
        if not CraftCore.compiler.isMacOS:
            self.buildDependencies["dev-utils/m4"] = "default"


class PackageAutoTools(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args = " --enable-shared  --enable-public-key --disable-documentation"
        if CraftCore.compiler.isMacOS:
            # for some reason the version of m4 built by craft will segfault
            # /bin/sh: line 1: 39726 Abort trap: 6
            #           /Users/alex/kde/dev-utils/bin/m4 /Users/alex/kde/build/libs/nettle/work/nettle-3.4/asm.m4 machine.m4 config.m4 aes-decrypt-internal.asm > aes-decrypt-internal.s
            self.subinfo.options.configure.args += " M4=/usr/bin/m4"


if not CraftCore.compiler.isMSVC():
    class Package(PackageAutoTools):
        def __init__(self):
            PackageAutoTools.__init__(self)
else:
    class Package(VirtualPackageBase):
        def __init__(self):
            VirtualPackageBase.__init__(self)
