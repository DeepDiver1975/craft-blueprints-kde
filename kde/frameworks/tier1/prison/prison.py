import info
from Blueprints.CraftPackageObject import CraftPackageObject


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "Qt 5 addon providing a barcode api to produce QRCode barcodes and DataMatrix barcodes."

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtmultimedia"] = None
        self.runtimeDependencies["libs/qrencode"] = None
        self.runtimeDependencies["libs/libdmtx"] = None
        self.runtimeDependencies["libs/zxing-cpp"] = None


class Package(CraftPackageObject.get("kde/frameworks").pattern):
    def __init__(self):
        super().__init__()
