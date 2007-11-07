%define major 10
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d
%define staticdevelname %mklibname %{name} -d -s

Summary:	Tools for manipulating graphics files in netpbm supported formats
Name:		netpbm
Version:	10.34
Release:	%mkrel 10
License:	GPL Artistic MIT
Group:		Graphics
URL:		http://netpbm.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/netpbm/%{name}-%{version}.tar.bz2
Source1:	mf50-netpbm_filters
Source2:	test-images.tar.bz2
Source3:	http://prdownloads.sourceforge.net/netpbm/%{name}doc-%{version}.tar.bz2
Patch0:		netpbm-10.17-time.patch
Patch1:		netpbm-9.24-strip.patch
Patch3:		netpbm-10.32-message.patch
Patch4:		netpbm-10.22-security2.patch
Patch5:		netpbm-10.22-cmapsize.patch
Patch6:		netpbm-10.30-gcc4.patch
Patch7:		netpbm-10.34-security.patch
Patch8:		netpbm-systemlibs.diff
Patch11:	netpbm-10.24-nodoc.patch
Patch13:	netpbm-10.34-bmptopnm.patch
Patch14:	netpbm-10.28-CAN-2005-2471.patch
Patch15: 	netpbm-10.33-ppmtompeg.patch
Patch16:	libjasper-1.701.0-CVE-2007-2721.patch
BuildRequires:	flex
BuildRequires:	jasper-devel
BuildRequires:	jbig-devel
BuildRequires:	jpeg-devel
BuildRequires:	libx11-devel
BuildRequires:	libxml2-devel
BuildRequires:	png-devel
BuildRequires:	tiff-devel
Requires:	%{libname} = %{version}
Obsoletes:	libgr-progs libgr1-progs
Provides:	libgr-progs libgr1-progs
BuildConflicts:	svgalib-devel
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The netpbm package contains a library of functions which support
programs for handling various graphics file formats, including .pbm
(portable bitmaps), .pgm (portable graymaps), .pnm (portable anymaps),
.ppm (portable pixmaps) and others.

%package -n	%{libname}
Summary:        A library for handling different graphics file formats
Group:          System/Libraries
Provides:	lib%{name}
Provides:	libgr libgr1 libnetpbm1
Obsoletes:      libgr libgr1 libnetpbm1

%description -n	%{libname}
The netpbm package contains a library of functions which support
programs for handling various graphics file formats, including .pbm
(portable bitmaps), .pgm (portable graymaps), .pnm (portable anymaps),
.ppm (portable pixmaps) and others.

%package -n	%{develname}
Summary:	Development tools for programs which will use the netpbm libraries
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	lib%{name}-devel
Obsoletes:	libgr-devel libgr1-devel libnetpbm1-devel
Provides:	libgr-devel libgr1-devel libnetpbm1-devel netpbm-devel
Obsoletes:	%{mklibname %{name} 10 -d}

%description -n	%{develname}
The netpbm-devel package contains the header files and programmer's
documentation for developing programs which can handle the various
graphics file formats supported by the netpbm libraries.

Install netpbm-devel if you want to develop programs for handling the
graphics file formats supported by the netpbm libraries. You'll also
need to have the netpbm package installed.

%package -n	%{staticdevelname}
Summary:	Static libraries for the netpbm libraries
Group:		Development/C
Requires:	%{develname} = %{version}
Provides:	lib%{name}-static-devel
Obsoletes:	libgr-static-devel libgr1-static-devel libnetpbm1-static-devel
Provides:	libgr-static-devel libgr1-static-devel libnetpbm1-static-devel netpbm-static-devel
Obsoletes:	%{mklibname %{name} 10 -d -s}

%description -n	%{staticdevelname}
The netpbm-devel package contains the static libraries (.a)
for developing programs which can handle the various
graphics file formats supported by the netpbm libraries.

Install netpbm-devel if you want to develop programs for handling the
graphics file formats supported by the netpbm libraries. You'll also
need to have the netpbm package installed.

%prep

%setup -q -a 2
%patch0 -p1 -b .time
%patch1 -p1 -b .strip
%patch3 -p1 -b .message
%patch4 -p1 -b .security2
%patch5 -p1 -b .cmapsize
%patch7 -p1 -b .security
%patch8 -p0 -b .systemlibs
%patch6 -p1 -b .gcc4
%patch11 -p1 -b .nodoc
%patch13 -p1 -b .bmptopnm
%patch14 -p1 -b .CAN-2005-2471
%patch15 -p1 -b .ppmtompeg
pushd converter/other/jpeg2000
%patch16 -p1 -b .cve-2007-2721
popd

tar xjf %{SOURCE2}
chmod 0644 doc/*

%build
%serverbuild

./configure <<EOF



















EOF

TOP=`pwd`
make \
    CC=%{__cc} \
    CFLAGS="$CFLAGS -fPIC" \
    LDFLAGS="-L$TOP/pbm -L$TOP/pgm -L$TOP/pnm -L$TOP/ppm" \
    TIFFLIB=-ltiff \
    TIFFHDR_DIR=%{_includedir} \
    JPEGLIB=-ljpeg \
    JPEGHDR_DIR=%{_includedir} \
    PNGLIB=-lpng \
    PNGHDR_DIR=%{_includedir} \
    ZLIB=-lz \
    ZHDR_DIR=%{_includedir} \
    JBIGLIB=-ljbig \
    JBIGHDR_DIR=%{_includedir} \
    JASPERLIB=-ljasper \
    JASPERHDR_DIR=%{_includedir} \
    JASPERDEPLIBS=-ljpeg \
    X11LIB=-lX11 \
    X11HDR_DIR=%{_includedir} \
    LINUXSVGALIB="NONE"

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}
make package pkgdir=%{buildroot}%{_prefix} LINUXSVGALIB="NONE"

# Ugly hack to have libs in correct dir on 64bit archs.
mkdir -p %{buildroot}%{_libdir}
if [ "%{_libdir}" != "/usr/lib" ]; then
  mv %{buildroot}/usr/lib/lib* %{buildroot}%{_libdir}
fi

cp -af lib/libnetpbm.a %{buildroot}%{_libdir}/libnetpbm.a
ln -sf libnetpbm.so.%{major} %{buildroot}%{_libdir}/libnetpbm.so

mkdir -p %{buildroot}%{_mandir}
tar jxf %{SOURCE3} -C %{buildroot}%{_mandir}

mkdir -p %{buildroot}%{_datadir}/%{name}-%{version}
mv %{buildroot}/usr/misc/*.map %{buildroot}%{_datadir}/%{name}-%{version}
rm -rf %{buildroot}/usr/README
rm -rf %{buildroot}/usr/VERSION
rm -rf %{buildroot}/usr/link
rm -rf %{buildroot}/usr/misc
rm -rf %{buildroot}/usr/man
rm -rf %{buildroot}/usr/pkginfo
rm -rf %{buildroot}/usr/config_template


mkdir -p %{buildroot}/usr/share/printconf/mf_rules
cp %{SOURCE1} %{buildroot}/usr/share/printconf/mf_rules/

mkdir -p %{buildroot}/usr/share/printconf/tests
cp test-images/* %{buildroot}/usr/share/printconf/tests/

# multiarch policy
%multiarch_includes %{buildroot}%{_includedir}/pm_config.h


%clean
rm -rf %{buildroot}

%post   -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%files 	-n %{libname}
%defattr(-,root,root)
%attr(755,root,root) %{_libdir}/lib*.so.*
%doc doc/*

%files 	-n %{develname}
%defattr(-,root,root)
%doc doc/COPYRIGHT.PATENT doc/Netpbm.programming
%{_includedir}/*.h
%multiarch %{multiarch_includedir}/pm_config.h
%attr(0755,root,root) %{_libdir}/lib*.so
%{_mandir}/man3/*

%files 	-n %{staticdevelname}
%defattr(-,root,root)
%doc doc/COPYRIGHT.PATENT
%{_libdir}/*.a

%files
%defattr(-,root,root)
%doc doc/COPYRIGHT.PATENT
%attr(0755,root,root) %{_bindir}/*
%{_mandir}/man[15]/*
%{_datadir}/%{name}-%{version}
%dir %{_datadir}/printconf
%dir %{_datadir}/printconf/mf_rules
%dir %{_datadir}/printconf/tests
%{_datadir}/printconf/mf_rules/*
%{_datadir}/printconf/tests/*
