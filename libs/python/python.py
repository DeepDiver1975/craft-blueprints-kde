# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Hannah von Reth <vonreth@kde.org>

import glob
from pathlib import Path

import info
import utils
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Package.MSBuildPackageBase import MSBuildPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotAndroid
        if CraftCore.compiler.isMinGW():
            self.parent.package.categoryInfo.compiler = CraftCore.compiler.Compiler.NoCompiler

    def setTargets(self):
        for ver in ["3.11.5"]:
            self.targets[ver] = f"https://www.python.org/ftp/python/{ver}/Python-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"Python-{ver}"
        self.targetDigests["3.11.5"] = (["85cd12e9cf1d6d5a45f17f7afe1cebe7ee628d3282281c492e86adf636defa3f"], CraftHash.HashAlgorithm.SHA256)
        if CraftCore.compiler.isMSVC():
            self.patchToApply["3.11.5"] = [(".msvc/patches", 1)]
        self.description = "Python is a high-level, general-purpose programming language"
        self.defaultTarget = "3.11.5"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        # self.buildDependencies["dev-utils/msys"] = None
        self.buildDependencies["dev-utils/automake"] = None
        self.runtimeDependencies["libs/libbzip2"] = None
        self.runtimeDependencies["libs/expat"] = None
        self.runtimeDependencies["libs/openssl"] = None
        self.runtimeDependencies["libs/gettext"] = None
        self.runtimeDependencies["libs/sqlite"] = None
        self.runtimeDependencies["libs/libffi"] = None
        self.runtimeDependencies["libs/liblzma"] = None


if CraftCore.compiler.isMSVC():

    class Package(MSBuildPackageBase):
        def __init__(self, **args):
            super().__init__()
            # msvc support and patches are based on https://github.com/microsoft/vcpkg/tree/0e47c1985273129e4d0ee52ff73bed9125555de8/ports/python3
            self.subinfo.options.configure.projectFile = self.sourceDir() / "PCbuild/pcbuild.proj"
            self.subinfo.options.configure.args += [
                "/p:IncludeExtensions=true",
                "/p:IncludeExternals=true",
                "/p:IncludeCTypes=true",
                "/p:IncludeSSL=true",
                "/p:IncludeTkinter=false",
                "/p:IncludeTests=false",
                f"/p:ForceImportBeforeCppTargets={self.sourceDir()}/PCbuild/python_vcpkg.props",
            ]

        def configure(self, defines=""):
            vars = {"VCPKG_LIBRARY_LINKAGE": "dynamic", "CURRENT_INSTALLED_DIR": CraftCore.standardDirs.craftRoot(), "VCPKG_TARGET_ARCHITECTURE": "x64"}

            def addLib(key, libName, libNameDebug=None):
                if not libNameDebug:
                    libNameDebug = libName
                vars[f"{key}_RELEASE"] = CraftCore.standardDirs.craftRoot() / f"lib/{libName}.lib"
                vars[f"{key}_DEBUG"] = CraftCore.standardDirs.craftRoot() / f"lib/{libNameDebug}.lib"

            addLib("BZ2", "bzip2", "bzip2d")
            addLib("CRYPTO", "libcrypto")
            addLib("EXPAT", "libexpat")
            addLib("FFI", "libffi")
            addLib("LZMA", "liblzma")
            addLib("SQLITE", "sqlite3")
            addLib("SSL", "libssl")
            addLib("ZLIB", "zlib")
            if not utils.configureFile(self.blueprintDir() / ".msvc/python_vcpkg.props.in", self.sourceDir() / "PCbuild/python_vcpkg.props", vars):
                return False
            if not utils.configureFile(self.blueprintDir() / ".msvc/openssl.props.in", self.sourceDir() / "PCbuild/openssl.props", vars):
                return False

            with (self.sourceDir() / "PCbuild/libffi.props").open("wt", encoding="UTF-8") as out:
                out.write("<?xml version='1.0' encoding='utf-8'?><Project xmlns='http://schemas.microsoft.com/developer/msbuild/2003' />")

            return super().configure()

        def make(self):
            with utils.ScopedEnv({"PythonForBuild": sys.executable}):
                return super().make()

        def install(self):
            self.cleanImage()
            verMinor = self.subinfo.buildTarget.split(".")[1]
            for p in ["python.exe", "pythonw.exe", "venvlauncher.exe", "venvwlauncher.exe"]:
                if not utils.copyFile(self.sourceDir() / f"PCbuild/amd64/{p}", self.imageDir() / f"bin/{p}"):
                    return False
            if not self._globCopy(self.sourceDir() / "PCbuild/amd64/", self.imageDir() / "bin", ["*.dll"]):
                return False
            for p in ["python3.lib", f"python3{verMinor}.lib"]:
                if not utils.copyFile(self.sourceDir() / f"PCbuild/amd64/{p}", self.imageDir() / f"lib/{p}"):
                    return False
            if not self._globCopy(self.sourceDir() / "PCbuild/amd64/", self.imageDir() / f"bin/DLLs", ["*.pyd"]):
                return False
            if not utils.copyDir(self.sourceDir() / "Include/", self.imageDir() / f"include/python3.{verMinor}"):
                return False
            if not utils.copyFile(self.sourceDir() / "PC/pyconfig.h", self.imageDir() / f"include/python3.{verMinor}/pyconfig.h"):
                return False
            if not utils.copyDir(self.sourceDir() / "Lib", self.imageDir() / "bin/Lib"):
                return False
            return True

else:

    class Package(AutoToolsPackageBase):
        def __init__(self, **args):
            super().__init__()
            self.shell.useMSVCCompatEnv = True
            # we call it specially in configure
            self.subinfo.options.configure.autoreconf = False
            self.subinfo.options.configure.args += [
                "--enable-shared",
                "--without-static-libpython",
                "--enable-ipv6",
                "--with-system-expat",
                "--with-pkg-config=yes",
                "--enable-loadable-sqlite-extensions",
                "--with-libc=",
                # if enabled it will somtimes install pip sometimes not,
                # if needed we can still call python3 -m ensurepip
                "--with-ensurepip=no",
            ]
