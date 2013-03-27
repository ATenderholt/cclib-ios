#!/bin/bash

set -x

. $(dirname $0)/environment.sh

# credit to:
# http://randomsplat.com/id5-cross-compiling-python-for-embedded-linux.html
# http://latenitesoft.blogspot.com/2008/10/iphone-programming-tips-building-unix.html

# download python and patch if they aren't there
if [ ! -f $CACHEROOT/Python-$IOS_PYTHON_VERSION.tar.bz2 ]; then
    curl http://www.python.org/ftp/python/$IOS_PYTHON_VERSION/Python-$IOS_PYTHON_VERSION.tar.bz2 > $CACHEROOT/Python-$IOS_PYTHON_VERSION.tar.bz2
fi

# download python and patch if they aren't there
if [ ! -f $CACHEROOT/Numeric-24.2.tar.gz ]; then
    curl http://sourceforge.net/projects/numpy/files/Old%20Numeric/24.2/Numeric-24.2.tar.gz/download > $CACHEROOT/Numeric-24.2.tar.gz
fi

# get rid of old build
rm -rf $TMPROOT/Python-$IOS_PYTHON_VERSION
try tar -xjf $CACHEROOT/Python-$IOS_PYTHON_VERSION.tar.bz2
try tar -xzf $CACHEROOT/Numeric-24.2.tar.gz
try mv Python-$IOS_PYTHON_VERSION $TMPROOT
try mv Numeric-24.2 $TMPROOT
try pushd $TMPROOT/Python-$IOS_PYTHON_VERSION

# Patch Python for temporary reduce PY_SSIZE_T_MAX otherzise, splitting string doesnet work
try patch -p1 < $KIVYIOSROOT/src/python_files/Python-$IOS_PYTHON_VERSION-ssize-t-max.patch
try patch -p1 < $KIVYIOSROOT/src/python_files/Python-$IOS_PYTHON_VERSION-dynload.patch
try patch -p1 < $KIVYIOSROOT/src/python_files/Python-$IOS_PYTHON_VERSION-static-_sqlite3.patch

# Copy our setup for modules
try cp $KIVYIOSROOT/src/python_files/ModulesSetup Modules/Setup.local
try cp $KIVYIOSROOT/src/python_files/_scproxy.py Lib/_scproxy.py

# Copy Numeric modules
try cp $TMPROOT/Numeric-24.2/Src/_numpymodule.c Modules/
try cp $TMPROOT/Numeric-24.2/Src/ufuncobject.c Modules/
try cp $TMPROOT/Numeric-24.2/Src/multiarraymodule.c Modules/
try cp $TMPROOT/Numeric-24.2/Src/arrayobject.c Modules/
try cp $TMPROOT/Numeric-24.2/Src/arraytypes.c Modules/
try mkdir Modules/Numeric
try cp $TMPROOT/Numeric-24.2/Include/Numeric/arrayobject.h Modules/Numeric
try cp $TMPROOT/Numeric-24.2/Include/Numeric/ufuncobject.h Modules/Numeric

# Copy cclib-lite
try mkdir Lib/cclib
try cp -R $KIVYIOSROOT/src/cclib-lite/ Lib/cclib/

echo "Building for native machine ============================================"

if [ ! -e hostpython ]; then
	try ./configure CC="$CCACHE clang -Qunused-arguments -fcolor-diagnostics" LDFLAGS="-lsqlite3"
	try make python.exe Parser/pgen
	try mv python.exe hostpython
	try mv Parser/pgen Parser/hostpgen
	try make distclean
fi

echo "Building for Simulator ================================================="

if [ ! -e $BUILDROOT/lib/libpython2.7-i386 ]; then

	# set up environment variables for simulator compilation
	export MACOSX_DEPLOYMENT_TARGET=10.8
	export SIM_VERSION=`xcodebuild -showsdks | fgrep "iphonesimulator" | tail -n 1 | awk '{print $4}'`
	export SIMDEVROOT=`xcode-select -print-path`/Platforms/iPhoneSimulator.platform/Developer
	export SIMSDKROOT="$SIMDEVROOT/SDKs/iPhoneSimulator${SIM_VERSION}.sdk"
	export I386_CPPFLAGS="-I$SIMSDKROOT/usr/lib/gcc/arm-apple-darwin10/4.2.1/include/ -I$SIMSDKROOT/usr/include/"
	export I386_CFLAGS="$I386_CPPFLAGS -pipe -no-cpp-precomp -isysroot $SIMSDKROOT"
	export I386_LDFLAGS="-isysroot $SIMSDKROOT"
	export I386_CPP="/usr/bin/cpp $I386_CPPFLAGS"

	if [ ! -d "$SIMSDKROOT" ]; then
	    echo "SIMSDKROOT doesn't exist. SIMSDKROOT=$SIMSDKROOT"
	    exit 1
	fi

	# Compile some stuff statically; Modules/Setup taken from pgs4a-kivy
	try cp $KIVYIOSROOT/src/python_files/ModulesSetup Modules/Setup.local

	mkdir $BUILDROOT/python-i386
	try ./configure CC="$SIMDEVROOT/usr/bin/i686-apple-darwin11-llvm-gcc-4.2 -m32" \
		    LD="$SIMDEVROOT/usr/bin/ld" \
			CFLAGS="$I386_CFLAGS" \
			LDFLAGS="$I386_LDFLAGS -lsqlite3" \
			--disable-toolbox-glue \
			--host=i386-apple-darwin \
			--prefix=$BUILDROOT/python-i386

	make HOSTPYTHON=./hostpython HOSTPGEN=./Parser/hostpgen \
	     CROSS_COMPILE_TARGET=yes

	deduplicate $(pwd)/libpython2.7.a

	try mv libpython2.7.a $BUILDROOT/lib/libpython2.7-i386.a

	try make distclean
fi


echo "Building for iOS ======================================================="

if [ ! -e $BUILDROOT/lib/libpython2.7-armv7.a ]; then

	# set up environment variables for cross compilation
	export CPPFLAGS="-I$IOSSDKROOT/usr/lib/gcc/arm-apple-darwin11/4.2.1/include/ -I$IOSSDKROOT/usr/include/"
	export CPP="$CCACHE /usr/bin/cpp $CPPFLAGS"
	export MACOSX_DEPLOYMENT_TARGET=

	# patch python to cross-compile
	try patch -p1 < $KIVYIOSROOT/src/python_files/Python-$IOS_PYTHON_VERSION-xcompile.patch

	# make a link to a differently named library for who knows what reason
	mkdir extralibs||echo "foo"
	ln -s "$IOSSDKROOT/usr/lib/libgcc_s.1.dylib" extralibs/libgcc_s.10.4.dylib || echo "sdf"

	# Copy our setup for modules
	try cp $KIVYIOSROOT/src/python_files/ModulesSetup Modules/Setup.local
	try cp $KIVYIOSROOT/src/python_files/_scproxy.py Lib/_scproxy.py

	try ./configure CC="$ARM_CC" LD="$ARM_LD" \
		CFLAGS="$ARM_CFLAGS" \
		LDFLAGS="$ARM_LDFLAGS -Lextralibs/ -Lextralibs -lsqlite3" \
		--without-pymalloc \
		--disable-toolbox-glue \
		--host=armv7-apple-darwin \
		--prefix=/python \
		--without-doc-strings

	try make HOSTPYTHON=./hostpython HOSTPGEN=./Parser/hostpgen \
		CROSS_COMPILE_TARGET=yes

	try make install HOSTPYTHON=./hostpython CROSS_COMPILE_TARGET=yes \
		prefix="$BUILDROOT/python"

	try mv -f $BUILDROOT/python/lib/libpython2.7.a $BUILDROOT/lib/

	deduplicate $BUILDROOT/lib/libpython2.7.a

	mv $BUILDROOT/lib/libpython2.7{,-armv7}.a
fi

lipo -create -output $BUILDROOT/lib/libpython2.7.a \
	$BUILDROOT/lib/libpython2.7-i386.a $BUILDROOT/lib/libpython2.7-armv7.a

