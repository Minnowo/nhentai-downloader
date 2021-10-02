
"""Build a standalone executable using PyInstaller"""

import PyInstaller.__main__
import util
import os

VIEWER_BASE = util.path("nhentai\\viewer\\")

PyInstaller.__main__.run([
    "--onefile",
    "--console",
    "--name", "nhentai." + ("exe" if os.name == "nt" else "bin"),
    "--add-data", VIEWER_BASE+"*;viewer\\",
    "--add-data", VIEWER_BASE+"default\\*;viewer\\default\\",
    "--add-data", VIEWER_BASE+"minimal\\*;viewer\\minimal\\",
    "--additional-hooks-dir", util.path("scripts"),
    "--distpath", util.path("dist"),
    "--workpath", util.path("build"),
    "--specpath", util.path("build"),
    util.path("nhentai", "__main__.py"),
])