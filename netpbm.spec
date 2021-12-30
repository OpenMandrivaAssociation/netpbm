%define _disable_ld_no_undefined 1

%define major	11
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

Summary:	Tools for manipulating graphics files in netpbm supported formats
Name:		netpbm
Version:	10.85.03
Release:	1
License:	GPL Artistic MIT
Group:		Graphics
Url:		http://netpbm.sourceforge.net/
# Source0 is prepared by
# svn checkout https://svn.code.sf.net/p/netpbm/code/advanced netpbm-%{version}
# svn checkout https://svn.code.sf.net/p/netpbm/code/userguide netpbm-%{version}/userguide
# and removing the .svn directories ( find -name "\.svn" -type d -print0 | xargs -0 rm -rf )
# and removing the ppmtompeg code, due to patents ( rm -rf netpbm-%{version}/converter/ppm/ppmtompeg/ )
Source0:	%{name}-%{version}.tar.gz
Source1:	mf50-netpbm_filters
Source2:	test-images.tar.bz2
Patch1:		http://pkgs.fedoraproject.org/cgit/rpms/netpbm.git/plain/netpbm-CVE-2017-2587.patch
Patch2:		http://pkgs.fedoraproject.org/cgit/rpms/netpbm.git/plain/netpbm-noppmtompeg.patch
Patch3:		http://pkgs.fedoraproject.org/cgit/rpms/netpbm.git/plain/netpbm-ppmfadeusage.patch
Patch5:		http://pkgs.fedoraproject.org/cgit/rpms/netpbm.git/plain/netpbm-security-scripts.patch

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
%autopatch -p1

%build
#export CC=gcc
#export CXX=g++

%serverbuild
export CFLAGS="$CFLAGS -fPIC -flax-vector-conversions -fno-strict-aliasing"

find . -name Makefile |xargs sed -i -e 's,\$(AR) -rc,$(AR) rc,g'

./configure <<EOF



















EOF

TOP=`pwd`
%make \
	CC="%{__cc}" \
	CFLAGS="$RPM_OPT_FLAGS -fPIC -flax-vector-conversions -fno-strict-aliasing" \
	CFLAGS_FOR_BUILD="$RPM_OPT_FLAGS -fPIC -flax-vector-conversions -fno-strict-aliasing" \
	LDFLAGS="-flto" \
	LADD="-flto -lm" \
	JASPERLIB=-ljasper \
	JASPERHDR_DIR=%{_includedir} \
	JPEGINC_DIR=%{_includedir} \
	PNGINC_DIR=%{_includedir} \
	TIFFINC_DIR=%{_includedir} \
	JPEGLIB_DIR=%{_libdir} \
	PNGLIB_DIR=%{_libdir} \
	TIFFLIB_DIR=%{_libdir} \
	LINUXSVGALIB="NONE" \
	X11LIB=%{_libdir}/libX11.so \
	XML2LIBS="NONE"

# prepare man files
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

%files
%{_bindir}/*
%{_datadir}/%{name}-%{version}
%dir %{_datadir}/printconf
%dir %{_datadir}/printconf/mf_rules
%dir %{_datadir}/printconf/tests
%{_datadir}/printconf/mf_rules/*
%{_datadir}/printconf/tests/*

%files -n %{libname}
%{_libdir}/lib*.so.%{major}*

%files -n %{devname}
%doc doc/*
%dir %{_includedir}/netpbm
%{_includedir}/netpbm/*.h
%{_libdir}/lib*.so

