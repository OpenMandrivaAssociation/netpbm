%define major 10
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d
%define staticdevelname %mklibname %{name} -d -s

Summary:	Tools for manipulating graphics files in netpbm supported formats
Name:		netpbm
Version:	10.35.59
Release:	%mkrel 1
License:	GPL Artistic MIT
Group:		Graphics
URL:		http://netpbm.sourceforge.net/
# Source0 is prepared by
# svn checkout https://netpbm.svn.sourceforge.net/svnroot/netpbm/stable netpbm-%{version}
# svn checkout https://netpbm.svn.sourceforge.net/svnroot/netpbm/userguide netpbm-%{version}/userguide
Source0:	netpbm-%{version}.tar.bz2
Source1:	mf50-netpbm_filters
Source2:	test-images.tar.bz2
Patch1:		netpbm-10.17-time.patch
Patch2:		netpbm-9.24-strip.patch
Patch3:		netpbm-10.19-message.patch
Patch4:		netpbm-10.22-security2.patch
Patch6:		netpbm-10.23-security.patch
Patch7:		netpbm-10.24-nodoc.patch
Patch8:		netpbm-10.28-gcc4.patch
Patch9:		netpbm-10.27-bmptopnm.patch
Patch10:	netpbm-10.28-CAN-2005-2471.patch
Patch11:	netpbm-10.31-xwdfix.patch
Patch12:	netpbm-10.33-ppmtompeg.patch
Patch13:	netpbm-10.33-multilib.patch
Patch14:	netpbm-10.34-pamscale.patch
Patch15:	netpbm-10.35-ppmquantall.patch
Patch16:	netpbm-10.35-pbmtog3segfault.patch
Patch17:	netpbm-10.35-pbmtomacp.patch
Patch18:	netpbm-10.35-glibc.patch
Patch19:	netpbm-10.35-gcc43.patch
Patch20:	netpbm-10.35-rgbtxt.patch
Patch21:	netpbm-10.35-pamtosvgsegfault.patch
Patch22:	netpbm-10.35-pnmmontagefix.patch
Patch23:	netpbm-10.35-pnmtofiasco-stdin.patch
Patch24:	netpbm-10.35-64bitfix.patch
Patch25:	netpbm-10.35-ximtoppmsegfault.patch
Patch100:	netpbm-10.35.57-format_not_a_string_literal_and_no_format_arguments.diff
Requires:	%{libname} = %{version}
BuildRequires:	flex
BuildRequires:	jasper-devel
BuildRequires:	jbig-devel
BuildRequires:	jpeg-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	libxml2-devel
BuildRequires:	png-devel
BuildRequires:	python
BuildRequires:	python-devel
BuildRequires:	tiff-devel
BuildRequires:	X11-devel
BuildConflicts:	svgalib-devel
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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

%package -n	%{develname}
Summary:	Development tools for programs which will use the netpbm libraries
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	netpbm-devel = %{version}-%{release}
Obsoletes:	%{mklibname netpbm 10 -d}

%description -n	%{develname}
The netpbm-devel package contains the header files and programmer's
documentation for developing programs which can handle the various graphics
file formats supported by the netpbm libraries.

Install netpbm-devel if you want to develop programs for handling the graphics
file formats supported by the netpbm libraries. You'll also need to have the
netpbm package installed.

%package -n	%{staticdevelname}
Summary:	Static libraries for the netpbm libraries
Group:		Development/C
Requires:	%{develname} = %{version}
Provides:	lib%{name}-static-devell = %{version}-%{release}
Provides:	netpbm-static-devel = %{version}-%{release}
Obsoletes:	%{mklibname netpbm 10 -d -s}

%description -n	%{staticdevelname}
The netpbm-devel package contains the static libraries (.a) for developing
programs which can handle the various graphics file formats supported by the
netpbm libraries.

Install netpbm-devel if you want to develop programs for handling the graphics
file formats supported by the netpbm libraries. You'll also need to have the
netpbm package installed.

%prep

%setup -q -a2

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;
		
for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

%patch1 -p1 -b .time
%patch2 -p1 -b .strip
%patch3 -p1 -b .message
%patch4 -p1 -b .security2
%patch6 -p1 -b .security
%patch7 -p1 -b .nodoc
%patch8 -p1 -b .gcc4
%patch9 -p1 -b .bmptopnm
%patch10 -p1 -b .CAN-2005-2471
%patch11 -p1 -b .xwdfix
%patch12 -p1 -b .ppmtompeg
%patch13 -p1 -b .multilib
%patch14 -p1 -b .pamscale
%patch15 -p1 -b .pqall
%patch16 -p1 -b .pbmtog3segfault
%patch17 -p1 -b .pbmtomacp
%patch18 -p1 -b .glibc
%patch19 -p1 -b .gcc43
%patch20 -p1 -b .rgbtxt
%patch21 -p1 -b .pamtosvgsegfault
%patch22 -p1 -b .pnmmontagefix
%patch23 -p1 -b .pnmtofiasco-stdin
%patch24 -p1 -b .64bitfix
%patch25 -p1 -b .ximtoppmsegfault
%patch100 -p1 -b .format_not_a_string_literal_and_no_format_arguments

##mv shhopt/shhopt.h shhopt/pbmshhopt.h
##perl -pi -e 's|shhopt.h|pbmshhopt.h|g' `find -name "*.c" -o -name "*.h"` ./GNUmakefile

%build
%serverbuild


./configure <<EOF



















EOF

TOP=`pwd`
make \
    CC="%{__cc}" \
    LDFLAGS="-L$TOP/pbm -L$TOP/pgm -L$TOP/pnm -L$TOP/ppm %ldflags" \
    CFLAGS="$CFLAGS -fPIC" \
    LADD="-lm" \
    TIFFLIB_DIR=%{_libdir} TIFFLIB=-ltiff TIFFINC_DIR=%{_includedir} TIFFHDR_DIR=%{_includedir} \
    JPEGLIB_DIR=%{_libdir} JPEGLIB=-ljpeg JPEGHDR_DIR=%{_includedir} JPEGINC_DIR=%{_includedir} \
    PNGLIB_DIR=%{_libdir} PNGLIB=-lpng PNGINC_DIR=%{_includedir} PNGHDR_DIR=%{_includedir} \
    ZLIB_DIR=%{_libdir} ZLIB=-lz ZHDR_DIR=%{_includedir} \
    X11LIB_DIR=%{_libdir} X11LIB=-lX11 X11INC_DIR=%{_includedir} X11HDR_DIR=%{_includedir} \
    JBIGLIB_DIR=%{_libdir} JBIGLIB=-ljbig JBIGHDR_DIR=%{_includedir} JBIGHDR_DIR=%{_includedir} \
    JASPERLIB_DIR=%{_libdir} JASPERLIB=-ljasper JASPERHDR_DIR=%{_includedir} JASPERDEPLIBS=-ljpeg \
    XML2LIBS="NONE" LINUXSVGALIB="NONE"

# prepare man files
cd userguide
for i in *.html ; do
    ../buildtools/makeman ${i}
done
for i in 1 3 5 ; do
    mkdir -p man/man${i}
    mv *.${i} man/man${i}
done

%install
rm -rf %{buildroot}

install -d %{buildroot}
make package pkgdir=%{buildroot}%{_prefix} XML2LIBS="NONE" LINUXSVGALIB="NONE"

# Ugly hack to have libs in correct dir on 64bit archs.
install -d %{buildroot}%{_libdir}
if [ "%{_libdir}" != "%{_prefix}/lib" ]; then
    mv %{buildroot}%{_prefix}/lib/lib* %{buildroot}%{_libdir}
fi

install -m0644 lib/libnetpbm.a %{buildroot}%{_libdir}/libnetpbm.a
ln -sf libnetpbm.so.%{major} %{buildroot}%{_libdir}/libnetpbm.so

# fix manpages
install -d %{buildroot}%{_mandir}
mv userguide/man/* %{buildroot}%{_mandir}/

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

install -d %{buildroot}%{_datadir}/printconf/mf_rules
cp %{SOURCE1} %{buildroot}%{_datadir}/printconf/mf_rules/

install -d %{buildroot}%{_datadir}/printconf/tests
cp test-images/* %{buildroot}%{_datadir}/printconf/tests/

%multiarch_includes %{buildroot}%{_includedir}/pm_config.h

%if %mdkversion < 200900
%post   -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/*
%{_datadir}/%{name}-%{version}
%dir %{_datadir}/printconf
%dir %{_datadir}/printconf/mf_rules
%dir %{_datadir}/printconf/tests
%{_datadir}/printconf/mf_rules/*
%{_datadir}/printconf/tests/*
%{_mandir}/man[15]/*

%files -n %{libname}
%defattr(-,root,root)
%doc doc/*
%attr(0755,root,root) %{_libdir}/lib*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/*.h
%multiarch %{multiarch_includedir}/pm_config.h
%attr(0755,root,root) %{_libdir}/lib*.so
%{_mandir}/man3/*

%files -n %{staticdevelname}
%defattr(-,root,root)
%attr(0644,root,root) %{_libdir}/*.a
