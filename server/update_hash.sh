#!/bin/bash

# Updates the resource pack hash so that it matches the zip file in server.properties
url=$(grep '^resource-pack=' server.properties | sed 's/resource-pack=//' | sed 's/\\:/:/') &&
wget $url -O pack.zip &&

hash=$(sha1sum < "pack.zip" | awk '{print $1}') &&
echo $hash &&
sed -i '/^resource-pack-sha1/ d' server.properties &&
echo "resource-pack-sha1=$hash" >> server.properties