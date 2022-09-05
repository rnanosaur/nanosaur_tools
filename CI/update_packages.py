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
import sys
import lxml.etree as ET
from packaging.version import parse

from .colors import bcolors

def update_packages(new_version, path):
    # Get all folders in repo
    folders = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name)) if not name.startswith('.')]
    # Check if is a ROS package
    parser = ET.XMLParser(remove_comments=False)
    for folder in folders:
        package_manifest = os.path.join(path, folder, 'package.xml')
        if os.path.exists(package_manifest):
            try:
                tree = ET.parse(package_manifest, parser=parser)
                version_tag = tree.find('version')
                version_old = version_tag.text
                # Update version
                version_tag.text = str(new_version)
                # Check new version
                version = tree.find('version').text
            except Exception as e:
                print(e)
                pass
            
            # Version update check
            print(f"{folder} - {version_old} > {version}")
            # Write the file with the new version
            with open(package_manifest, 'wb') as doc:
                doc.write(ET.tostring(tree, pretty_print=True, xml_declaration=True, encoding=None))
# EOF
