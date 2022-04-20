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
from sys import exit
import argparse
from packaging.version import parse
from CI import check_packages
from CI import check_script


def main():
    parser = argparse.ArgumentParser(description='version build check for all packages')
    parser.add_argument("version")
    args = parser.parse_args()

    version=parse(args.version)
    path = "../"
    folders = []
    # Get all ros workspaces
    for folder in os.listdir(path):
        if folder.startswith('nanosaur'):
            # Check if has a src folder
            new_path = os.path.join(path, folder, "src")
            if os.path.isdir(new_path):
                # Check all nanosaur repositories
                for name in os.listdir(new_path):
                    if name.startswith('nanosaur'):
                        folders +=[os.path.join(path, folder, "src", name)]
    
    for folder in folders:
        print(f"Folder: {os.path.abspath(folder)}")
        check_packages(version, folder)
    
    # Nanosaur script version
    check_script(version, os.path.join(path, "nanosaur_core", "src", "nanosaur"))

if __name__ == '__main__':
    main()
# EOF
