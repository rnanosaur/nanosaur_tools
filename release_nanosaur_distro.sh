#!/bin/bash
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


bold=`tput bold`
red=`tput setaf 1`
green=`tput setaf 2`
yellow=`tput setaf 3`
blue=`tput setaf 4`
reset=`tput sgr0`


git_push_updates()
{
    local FOLDER=$1
    local VERSION=$2
    local MESSAGE=$3
    local cfolder=$(pwd)
    echo "${blue}[$FOLDER]${reset}"
    # Jump to repo
    cd $FOLDER
    # Commit version update
    git commit -am $MESSAGE
    # tag version
    git tag -a $VERSION -m $MESSAGE
    # git push new version
    git push
    git push --tags
    # Return main folder
    cd $cfolder
}


check_repo()
{
    local FOLDER=$1
    local VERSION=$2
    local cfolder=$(pwd)
    local output_check=0
    echo "${blue}[$FOLDER]${reset}"

    # Load nanosaur configuration file
    if [ ! -d $FOLDER ] ; then
        echo "${red}[ERROR] repository $(basename ${FOLDER}) doesn't exist!${reset}"
        return 1
    fi
    # Jump to repo
    cd $FOLDER
    git pull --quiet
    # Check if there are uncommit
    if git diff-index --quiet HEAD --; then
        # No changes
        echo "${green}[ OK ] git no changes${reset}"
        output_check=$(($output_check | 0))
    else
        # Changes
        echo "${red}[ERROR] git changes${reset}"
        output_check=$(($output_check | 1))
    fi
    # Check if tag version exists
    if [ $(git tag -l "$VERSION") ]; then
        echo "${red}[ERROR] git $VERSION already exist ${reset}"
        output_check=$(($output_check | 1))
    else
        echo "${green}[ OK ] git $VERSION doesn't exist ${reset}"
        output_check=$(($output_check | 0))
    fi
    # Check branch
    branch=$(git branch | sed -n -e 's/^\* \(.*\)/\1/p')
    if [ $branch = "master" ] || [ $branch = "main" ] ; then
        echo "${green}[ OK ] git right branch:$branch ${reset}"
        output_check=$(($output_check | 0))
    else
        echo "${red}[ERROR] git wrong branch:$branch ${reset}"
        output_check=$(($output_check | 1))
    fi
    # Return main folder
    cd $cfolder

    # echo "output $output_check"
    return $output_check
}


main()
{
    local SILENT=false

    local name=$(basename ${0})
    if [ $# -lt 2 ] ; then
        echo "${red}[ERROR] Please write version and message tag${reset}"
        echo "${red}$name [VERSION] [MESSAGE]${reset}"
        exit 1
    fi

    local VERSION=$1
    local MESSAGE=${@:2}

    echo "${bold}Version:${reset} $VERSION"
    echo "${bold}Message:${reset} $MESSAGE"
    echo "----------------------"

    ####################################

    local output_check=0
    # Nanosaur Core repositories
    MAIN_PATH="$HOME/nanosaur_core/src"
    # nanosaur_robot
    check_repo $MAIN_PATH/nanosaur_robot $VERSION
    output_check=$(($output_check | $?))
    # nanosaur
    check_repo $MAIN_PATH/nanosaur $VERSION
    output_check=$(($output_check | $?))
    # nanosaur_perception
    MAIN_PATH="$HOME/nanosaur_perception/src"
    check_repo $MAIN_PATH/nanosaur_perception $VERSION
    output_check=$(($output_check | $?))

    echo "----------------------"
    if [ $output_check -gt 0 ]; then
        echo "${red}[ERROR] I cannot upgrade the nanosaur distro${reset}"
        echo "${red}        Merge to master/main and push all uncommitted changes${reset}"
        exit 1
    fi

    echo "${bold}Version:${reset} $VERSION"
    echo "${bold}Message:${reset} $MESSAGE"
    echo "----------------------"

    while ! $SILENT; do
        read -p "Do you wish to release nanosaur to version ${bold}$VERSION${reset}? [Y/n] " yn
            case $yn in
                [Yy]* ) # Break and install jetson_stats 
                        break;;
                [Nn]* ) exit;;
            * ) echo "Please answer yes or no.";;
        esac
    done

    # Load virtual enviroment
    source .venv/bin/activate

    # Upgrade all repos
    MAIN_PATH="$HOME/nanosaur_core/src"
    # nanosaur_robot
    python upgrade_release.py $VERSION -p $MAIN_PATH/nanosaur_robot
    # nanosaur repo
    python upgrade_nanosaur_script.py $VERSION -p $MAIN_PATH/nanosaur
    python upgrade_release.py $VERSION -p $MAIN_PATH/nanosaur
    # nanoasur_perception
    MAIN_PATH="$HOME/nanosaur_perception/src"
    python upgrade_release.py $VERSION -p $MAIN_PATH/nanosaur_perception

    # Push changes and release tag
    MAIN_PATH="$HOME/nanosaur_core/src"
    git_push_updates $MAIN_PATH/nanosaur_robot $VERSION $MESSAGE
    git_push_updates $MAIN_PATH/nanosaur $VERSION $MESSAGE
    MAIN_PATH="$HOME/nanosaur_perception/src"
    git_push_updates $MAIN_PATH/nanosaur_perception $VERSION $MESSAGE

    # Check version
    output_check=0
    MAIN_PATH="$HOME/nanosaur_core/src"
    # nanosaur_robot
    python check_tag_version.py $VERSION -p $MAIN_PATH/nanosaur_robot
    output_check=$(($output_check | $?))
    # nanosaur repo
    python check_nanosaur_script.py $VERSION -p $MAIN_PATH/nanosaur
    output_check=$(($output_check | $?))
    python check_tag_version.py $VERSION -p $MAIN_PATH/nanosaur
    output_check=$(($output_check | $?))
    # nanosaur_perception
    MAIN_PATH="$HOME/nanosaur_perception/src"
    python check_tag_version.py $VERSION -p $MAIN_PATH/nanosaur_perception
    output_check=$(($output_check | $?))
}


main $@
exit 0
# EOF
