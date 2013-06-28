#! /usr/bin/env python
# Copyright (C) 2013 David Loureiro <david.loureiro1@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, version 3 of the
# License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
from os import mkdir, path, access, R_OK  # W_OK for write permission.
from shutil import copy2, copytree
import codecs
import json
import glob
from os.path import normpath, basename

# version
VERSION = "1.0"

#-- author
AUTHOR = {}
# author name
AUTHOR["name"] = "David Loureiro"
# author e-mail
AUTHOR["e-mail"] = "david.loureiro1@gmail.com"

#-- project
PROJECT = {}
# project url
PROJECT["url"] = ""

# defining operations file default
operationsFile = path.join(os.getcwd(),"operations.json")

class PYSTAGEError(Exception):
    """Exception raised for errors in the pyStage module.

    Attributes:
        msg  -- explanation of the error
    """
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return repr(self.value)

def checkingOperationFile(aFile) :
    """Checking for operations file existence

    Attributes:
        aFile -- file containing the operations to realise during the staging
    """

    if not path.exists(aFile) :
        print "operations.json file does not exist"
        sys.exit(4)

def loadingOperations(aFile) :
    """ Loading operations file content

    Attribute:
        aFile -- operations file
    """

    json_data=codecs.open(aFile, "r", "utf-8")
    data = json.load(json_data)
    json_data.close()
    return data

def checkingOperations(data) :
    """Verifying operations file structure

    Attributes:
        data -- the data contained in the operations file
    """

    ## source root dir
    if "source_root" not in data :
        raise PYSTAGEError("No source_root defined")


    ## destination root dir
    if "destination_root" not in data :
        raise PYSTAGEError("No destination_root defined")

    if "operations" not in data :
        raise PYSTAGEError("No staging operations to perform")

    # retrieving source_root
    source_root = data["source_root"]
    # retrieving destination_root
    destination_root = data["destination_root"]

    # checking if source_root exists
    if not path.exists(source_root) :
        raise PYSTAGEError( source_root + " does not exist!" )

    # cheking if source_root is not a file
    if path.isfile(source_root) :
        raise PYSTAGEError( source_root + " is not a directory!" )

    # checking existence of destination root
    if path.exists(destination_root) :
        # the path exists
        # verifying if it's not a file
        if path.isfile(destination_root) :
            # it's a file
            raise PYSTAGEError( destination_root + " is not a directory!" )
        # it's a directory

def creatingDestinationRootDirectory(destination_root) :
    """Creating destination root directory as defined in the operations file

    Attributes:
        destination_root -- destination root path to create

    """

    print "Creating destination folder : " + destination_root
    os.makedirs(destination_root)

def printingOperationMessage(src, dest, operation):
    """Printing operation message

    Attributes:
        src -- source node to stage
        dest -- destination node where the source node must be copied
        operation -- operation node in the data object with the message in it
    """

    message =  " - Copying " + src + " to " + dest + " "
    if "message" in operation :
        message = " - " + operation["message"]
    print message

def performingOperations(source_root, destination_root, operations) :
    print "Staging from : " + source_root
    print "To : " + destination_root

    for operation in operations :
        src = path.join(source_root, operation['src'])
        final_dir = operation['dest']
        if final_dir.strip() == "." :
            final_dir = ""
        dest = normpath(path.join(destination_root ,final_dir))

        src_dir = glob.glob(src)
        if src_dir is [] :
            print "Nothing to do with " + src
        else :
            for element in src_dir :
                if path.isfile(element) :
                    printingOperationMessage(element,dest, operation)
                    copy2(element, dest)
                if path.isdir(element) :
                    if path.exists(dest) :
                        dest = path.join(dest,basename(normpath(element)))
                    printingOperationMessage(element,dest, operation)
                    copytree(element,dest)
    print "Staging done !"

def printHelp() :
    print ""
    print sys.argv[0] + " is a simple staging program"
    print ""
    print "You can copy/stage/install files automatically"
    print "You must have a 'operations.json' file in the current working directory"
    print ""

def printVersion() :
    print ""
    print sys.argv[0] + " " + VERSION

def printCopyright() :
    print ""
    print "Copyright (C) 2013 " + AUTHOR["name"] + " <" + AUTHOR["e-mail"] + ">"
    print "This program is free software: you can redistribute it and/or modify"
    print "it under the terms of the GNU Affero General Public License as"
    print "published by the Free Software Foundation, version 3 of the"
    print "License."
    print ""
    print "This program is distributed in the hope that it will be useful,"
    print "but WITHOUT ANY WARRANTY; without even the implied warranty of"
    print "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the"
    print "GNU Affero General Public License for more details."
    print ""
    print "You should have received a copy of the GNU Affero General Public License"
    print "along with this program.  If not, see <http://www.gnu.org/licenses/>."
    print ""

def main() :
    checkingOperationFile(operationsFile)
    data = loadingOperations(operationsFile)
    checkingOperations(data)
    creatingDestinationRootDirectory(data["destination_root"])
    performingOperations(data["source_root"], data["destination_root"], data["operations"])

if __name__ == "__main__":

    if len(sys.argv) > 1 :
        if sys.argv[1] == "-h" or sys.argv[1] == "--help" :
            printVersion()
            printHelp()
        if sys.argv[1] == "-V" or sys.argv[1] == "--version" :
            printVersion()
            printCopyright()
        else :
            main()
    else :
        main()