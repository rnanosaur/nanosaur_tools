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
import argparse
import subprocess
from packaging.version import parse

from colors import bcolors

def check_nanosaur_script(version, path):
    # Nanosaur script version
    path_nanosaur_script=os.path.join(path, "nanosaur_core", "src", "nanosaur", "nanosaur", "scripts", "nanosaur")
    print(f"Check nanosaur script: {os.path.abspath(path_nanosaur_script)}")
    nanosaur_version = subprocess.run([path_nanosaur_script, "-v"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    nanosaur_version.stdout.decode("utf-8")
    script_version=parse(nanosaur_version.stdout.decode("utf-8"))
    print(script_version)
    
    if version == script_version:
        print(bcolors.ok(f"[ OK ] nanosaur {script_version}"))
        return True
    else:
        print(bcolors.fail(f"[ERROR] nanosaur {script_version} != {version}"))
        return False  

def main():
    parser = argparse.ArgumentParser(description='version build check for all packages')
    parser.add_argument("version")
    args = parser.parse_args()

    new_version = parse(args.version)
    # Get all folders in repo
    path = "..7"
    # Check nanosaur script
    check = check_nanosaur_script(new_version, path)
    # Exit status
    exit(0 if check else 1)

if __name__ == '__main__':
    main()
# EOF

