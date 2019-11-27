#!/bin/sh
EDX_VERSION="${EDX_VERSION:-ironwood.2}"


echo Downloading latest image
docker pull derex/openedx-ironwood
ddc-local reset-mysql
ddc-local reset-rabbitmq
[ -f "${EDX_VERSION}.tar.gz" ] || wget https://github.com/edx/edx-demo-course/archive/open-release/${EDX_VERSION}.tar.gz
tar xf ${EDX_VERSION}.tar.gz
ddc-local run -v ${PWD}/edx-demo-course-open-release-${EDX_VERSION}:/demo-course --rm cms ./manage.py cms import /openedx/data /demo-course