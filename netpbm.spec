%define debug_package %{nil}
%define _disable_ld_no_undefined 1

%define major	11
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

Summary:	Tools for manipulating graphics files in netpbm supported formats
Name:		netpbm
Version:	10.68.01
Release:	2
License:	GPL Artistic MIT
Group:		Graphics
Url:		http://netpbm.sourceforge.net/
# Source0 is prepared by
# svn checkout https://netpbm.svn.sourceforge.net/svnroot/netpbm/advanced netpbm-%{version}
# svn checkout https://netpbm.svn.sourceforge.net/svnroot/netpbm/userguide netpbm-%{version}/userguide
# svn checkout https://netpbm.svn.sourceforge.net/svnroot/netpbm/trunk/test netpbm-%{version}/test
# and removing the .svn directories ( find -name "\.svn" -type d -print0 | xargs -0 rm -rf )
# and removing the ppmtompeg code, due to patents ( rm -rf netpbm-%{version}/converter/ppm/ppmtompeg/ )
Source0:	%{name}-%{version}.tar.xz
Source1:	mf50-netpbm_filters
Source2:	test-images.tar.bz2
Patch1:		netpbm-time.patch
Patch2:		netpbm-message.patch
Patch3:		netpbm-security-scripts.patch
Patch4:		netpbm-security-code.patch
Patch5:		netpbm-nodoc.patch
Patch6:		netpbm-gcc4.patch
Patch7:		netpbm-bmptopnm.patch
Patch8:		netpbm-CAN-2005-2471.patch
Patch9:		netpbm-xwdfix.patch
Patch11:	netpbm-multilib.patch
Patch13:	netpbm-glibc.patch
Patch15:	netpbm-docfix.patch
Patch16:	netpbm-ppmfadeusage.patch
Patch17:	netpbm-fiasco-overflow.patch
Patch18:	netpbm-lz.patch
Patch20:	netpbm-noppmtompeg.patch
Patch21:	netpbm-cmuwtopbm.patch
Patch22:	netpbm-pamtojpeg2k.patch
Patch100:	netpbm-10.68.01-stdio.patch
Patch101:	netpbm-10.68.01-link.patch
BuildRequires:	flex
BuildRequires:	jbig-devel
BuildRequires:	jpeg-devel
BuildRequires:	tiff-devel
BuildRequires:	pkgconfig(jasper)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(x11)
BuildConflicts:	svgalib-devel

%description
The netpbm package contains a library of functions which support programs for
handling various graphics file formats, including .pbm (portable bitmaps), .pgm
(portable graymaps), .pnm (portable anymaps), .ppm (portable pixmaps) and
others.

%package -n	%{libname}
Summary:        A library for handling different graphics file formats
Group:          System/Libraries

%description -n	%{libname}
The netpbm package contains a library of functions which support programs for
handling various graphics file formats, including .pbm (portable bitmaps), .pgm
(portable graymaps), .pnm (portable anymaps), .ppm (portable pixmaps) and
others.

%package -n	%{devname}
Summary:	Development tools for programs which will use the netpbm libraries
Group:		Development/C
Requires:	%{libname} >= %{version}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
The netpbm-devel package contains the header files and programmer's
documentation for developing programs which can handle the various graphics
file formats supported by the netpbm libraries.

%prep
%setup -q -a2

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

%patch1 -p1 -b .time
%patch2 -p1 -b .message
%patch3 -p1 -b .security-scripts
%patch4 -p1 -b .security-code
%patch5 -p1 -b .nodoc
%patch6 -p1 -b .gcc4
%patch7 -p1 -b .bmptopnm
%patch8 -p1 -b .CAN-2005-2471
%patch9 -p1 -b .xwdfix
%patch11 -p1 -b .multilib
%patch13 -p1 -b .glibc
%patch15 -p1 -b .docfix
%patch16 -p1 -b .ppmfadeusage
%patch17 -p1 -b .fiasco-overflow
%patch18 -p0 -b .lz
%patch20 -p1 -b .noppmtompeg
%patch21 -p1 -b .cmuwtopbmfix
%patch22 -p1 -b .pamtojpeg2kfix

%patch100 -p1 -b .jpeglib
%patch101 -p1 -b .link
sed -i 's/STRIPFLAG = -s/STRIPFLAG =/g' config.mk.in

##mv shhopt/shhopt.h shhopt/pbmshhopt.h
##perl -pi -e 's|shhopt.h|pbmshhopt.h|g' `find -name "*.c" -o -name "*.h"` ./GNUmakefile

rm -rf converter/other/jpeg2000/libjasper/
sed -i -e 's/^SUBDIRS = libjasper/SUBDIRS =/' converter/other/jpeg2000/Makefile

%build
export CC=gcc
export CXX=g++

%serverbuild
export CFLAGS="$CFLAGS -fPIC -flax-vector-conversions -fno-strict-aliasing"

./configure <<EOF



















EOF

TOP=`pwd`
make \
    CC="gcc" \
    LDFLAGS="-L$TOP/pbm -L$TOP/pgm -L$TOP/pnm -L$TOP/ppm %{ldflags}" \
    CFLAGS_SHLIB="-fPIC" \
    MATHLIB="-lm" \
    TIFFLIB_DIR=%{_libdir} TIFFLIB=-ltiff TIFFINC_DIR=%{_includedir} TIFFHDR_DIR=%{_includedir} \
    JPEGLIB_DIR=%{_libdir} JPEGLIB=-ljpeg JPEGHDR_DIR=%{_includedir} JPEGINC_DIR=%{_includedir} \
    PNGLIB_DIR=%{_libdir} PNGLIB="-L%{_libdir} -lpng" PNGINC_DIR=%{_includedir} PNGHDR_DIR=%{_includedir} \
    ZLIB_DIR=%{_libdir} ZLIB="-L%{_libdir} -lz" ZHDR_DIR=%{_includedir} \
    X11LIB_DIR=%{_libdir} X11LIB="-L%{_libdir} -lX11" X11INC_DIR=%{_includedir} X11HDR_DIR=%{_includedir} \
    JBIGLIB_DIR=%{_libdir} JBIGLIB="-L%{_libdir} -ljbig" JBIGHDR_DIR=%{_includedir} JBIGHDR_DIR=%{_includedir} \
    JASPERLIB_DIR=%{_libdir} JASPERLIB="-L%{_libdir} -ljasper" JASPERHDR_DIR=%{_includedir} JASPERDEPLIBS="-L%{_libdir} -ljpeg" \
    XML2LIBS="NONE" LINUXSVGALIB="NONE"

# prepare man files
cd userguide
for i in *.html ; do
    %__python2 ../buildtools/makeman ${i}
done
for i in 1 3 5 ; do
    mkdir -p man/man${i}
    mv *.${i} man/man${i}
done

%install
install -d %{buildroot}
make package PKGDIR=%{buildroot}%{_prefix} XML2LIBS="NONE" LINUXSVGALIB="NONE"

# Ugly hack to have libs in correct dir on 64bit archs.
install -d %{buildroot}%{_libdir}
if [ "%{_libdir}" != "%{_prefix}/lib" ]; then
    mv %{buildroot}%{_prefix}/lib/lib* %{buildroot}%{_libdir}
fi

ln -sf libnetpbm.so.%{major} %{buildroot}%{_libdir}/libnetpbm.so

# fix manpages
install -d %{buildroot}%{_mandir}
cp -rp userguide/man/* %{buildroot}%{_mandir}/

# Get rid of the useless non-ascii character in pgmminkowski.1
sed -i 's/\xa0//' %{buildroot}%{_mandir}/man1/pgmminkowski.1

# Don't ship man pages for non-existent binaries and bogus ones
for i in hpcdtoppm pcdovtoppm pnmtojbig ppmsvgalib vidtoppm picttoppm jbigtopnm \
    directory error extendedopacity pam pbm pgm pnm ppm index libnetpbm_dir liberror \
    pambackground pamfixtrunc pamtogif pamtooctaveimg pamundice ppmtotga; do
    rm -f %{buildroot}%{_mandir}/man1/${i}.1
done
rm -f %{buildroot}%{_mandir}/man5/extendedopacity.5

install -d %{buildroot}%{_datadir}/%{name}-%{version}
mv %{buildroot}%{_prefix}/misc/*.map %{buildroot}%{_datadir}/%{name}-%{version}
rm -rf %{buildroot}%{_prefix}/README
rm -rf %{buildroot}%{_prefix}/VERSION
rm -rf %{buildroot}%{_prefix}/link
rm -rf %{buildroot}%{_prefix}/misc
rm -rf %{buildroot}%{_prefix}/man
rm -rf %{buildroot}%{_prefix}/pkginfo
rm -rf %{buildroot}%{_prefix}/config_template
rm -rf %{buildroot}%{_prefix}/pkgconfig_template
rm -f %{buildroot}%{_mandir}/man1/ppmtompeg.1*

install -d %{buildroot}%{_datadir}/printconf/mf_rules
cp %{SOURCE1} %{buildroot}%{_datadir}/printconf/mf_rules/

install -d %{buildroot}%{_datadir}/printconf/tests
cp test-images/* %{buildroot}%{_datadir}/printconf/tests/

%multiarch_includes %{buildroot}%{_includedir}/netpbm/pm_config.h

%files
%{_bindir}/*
%{_datadir}/%{name}-%{version}
%dir %{_datadir}/printconf
%dir %{_datadir}/printconf/mf_rules
%dir %{_datadir}/printconf/tests
%{_datadir}/printconf/mf_rules/*
%{_datadir}/printconf/tests/*
%{_mandir}/man[15]/*

%files -n %{libname}
%{_libdir}/lib*.so.%{major}*

%files -n %{devname}
%doc doc/*
%dir %{_includedir}/netpbm
%{_includedir}/netpbm/*.h
%{multiarch_includedir}/netpbm/pm_config.h
%{_libdir}/lib*.so
%{_mandir}/man3/*

