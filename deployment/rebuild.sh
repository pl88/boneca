#!/bin/bash
set -e

cd $REPOSITORY_PATH
git pull
cd $REPOSITORY_PATH/backend
make run-dev
cd $REPOSITORY_PATH/frontend
npm install
npm run build
rm -rf $WEB_INSTALL_PATH/*
mkdir -p $WEB_INSTALL_PATH
cp -r $REPOSITORY_PATH/frontend/dist/* $WEB_INSTALL_PATH
