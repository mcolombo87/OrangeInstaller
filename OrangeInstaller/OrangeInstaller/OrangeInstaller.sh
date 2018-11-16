#!/bin/bash
cd $(dirname $0)
hash svn 2>/dev/null || { echo >&2 "SVN not installed."; echo "run 'apt-get install subversion' and try again"; exit 1; }
if [ -f /lib/x86_64-linux-gnu/libz.so.1 ] && [ ! -f libz.so.1.badfile ]
then
    echo "Making link to images library"
    mv libz.so.1 libz.so.1.badfile
    ln -s /lib/x86_64-linux-gnu/libz.so.1
fi
./OrangeInstaller
