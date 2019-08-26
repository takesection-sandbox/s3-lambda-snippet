#!/bin/sh

mkdir target
rm -f target/*
(cd trigger; zip -r ../target/trigger.zip .)
(cd src; zip -r ../target/consumer.zip .)