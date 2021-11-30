#!/bin/bash
git clone https://gitlab.com/allianceauth/allianceauth.git aa-git
cp -R aa-git/docker ./aa-docker
rm -rf aa-git
