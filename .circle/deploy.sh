#!/bin/bash

set -e

git clone git@github.com:webplates/docker-symfony-php-dev.git -b images repo

rm -rf repo/images/
cp -r images/ repo/

if [[ $(git -C repo status --porcelain | wc -l) -lt 1 ]]; then
    echo "No changes to the output on this push, exiting."
    rm -rf repo/
    exit 0
fi

git -C repo config user.name "Circle CI"
git -C repo config user.email "circleci@webplates.xyz"

git -C repo add .
git -C repo commit -m "Uploading Dockerfiles built for ${CIRCLE_SHA1}"
git -C repo push origin images

rm -rf repo/
