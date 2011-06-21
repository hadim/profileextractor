#!/usr/bin/env sh

VERSION="$1"

git add ..
git ci -am "Release $1"

git co release

sed -i "s/.*/$1/" ../VERSION
sed -i "s/self.version = .*/self.version = \'$1\'/" ../src/ui/mainwindow.py

git ci -am "put version number"

git merge master
git ci -am "Release $1"
git tag -a $1 -m "$1"

#git pull origin release
git push origin release --tag



