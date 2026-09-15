#!/bin/bash

if [ ! -f /Workspace/Configuration/.gitignore ]; then
    touch /Workspace/Configuration/.gitignore
    echo "cache" >> /Workspace/Configuration/.gitignore
    echo "libraries" >> /Workspace/Configuration/.gitignore
    echo "versions" >> /Workspace/Configuration/.gitignore
fi

if [ "$accept_minecraft_eula" = "true" ]; then
    echo "eula=true" > /Workspace/Configuration/eula.txt
fi

if [ -z "$java_xms" ]; then
    java_xms="512m"
fi

if [ -z "$java_xmx" ]; then
    java_xmx="2g"
fi

command="java -Xms$java_xms -Xmx$java_xmx -jar /Workspace/Application/PaperServer.jar --nogui --universe /Workspace/Data"
echo "Run '$command'..."
bash -c "$command"
