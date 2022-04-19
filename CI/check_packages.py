#!/usr/bin/python
# Copyright (C) 2022, Raffaello Bonghi <raffaello@rnext.it>
# All rights reserved
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright 
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its 
#    contributors may be used to endorse or promote products derived 
#    from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND 
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, 
# BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS 
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, 
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; 
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE 
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, 
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
from xml.etree.ElementTree import ElementTree
from packaging.version import parse

from .colors import bcolors


def check_packages(new_version, path):
    check = True
    # Get all folders in repo
    folders = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name)) if not name.startswith('.')]
    # Check if is a ROS package
    for folder in folders:
        package_manifest = os.path.join(path, folder, 'package.xml')
        if os.path.exists(package_manifest):
            try:
                root = ElementTree(None, package_manifest)
                version = root.findtext('version')
            except Exception:
                pass
            
            # https://packaging.pypa.io/en/latest/version.html#packaging.version.parse
            pkg_version = parse(version)
            
            if pkg_version.is_prerelease:
                print(bcolors.fail(f"[ERROR] Can't be a dev version {new_version}"))
                check = check and False
                continue
            # Check version
            if new_version.is_prerelease:
                if new_version.base_version == pkg_version.base_version:
                    print(bcolors.warning(f"[ OK ] (Developer version {new_version}) {folder} {pkg_version}"))
                    check = check and True
                else:
                    print(bcolors.fail(f"[ERROR] {folder} {pkg_version} != {new_version}"))
                    check = check and False
            else:
                if new_version == pkg_version:
                    print(bcolors.ok(f"[ OK ] {folder} {pkg_version}"))
                    check = check and True
                else:
                    print(bcolors.fail(f"[ERROR] {folder} {pkg_version} != {new_version}"))
                    check = check and False
    return check
# EOF
