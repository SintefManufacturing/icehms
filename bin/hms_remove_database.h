#!/usr/bin/bash
echo "This script will remove the icegrid/icenode database on disk"
echo "Make sure ice registry is not running"
echo "Click Enter to continue"
read ans
rm -rfv db/registry/*
rm -rfv db/node/*
echo "Removing done"
