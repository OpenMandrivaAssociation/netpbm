%define major 11
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	Tools for manipulating graphics files in netpbm supported formats
Name:		netpbm
Version:	10.57.01
Release:	2
License:	GPL Artistic MIT
Group:		Graphics
URL:		http://netpbm.sourceforge.net/
# Source0 is prepared by
# svn checkout https://netpbm.svn.sourceforge.net/svnroot/netpbm/stable netpbm-%{version}
# svn checkout https://netpbm.svn.sourceforge.net/svnroot/netpbm/userguide netpbm-%{version}/userguide
# and removing the .svn directories ( find -name "\.svn" -type d -print0 | xargs -0 rm -rf )
# and removing the ppmtompeg code, due to patents ( rm -rf netpbm-%{version}/converter/ppm/ppmtompeg/ )
Source0:	netpbm-%{version}.tar.xz
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
Patch14:	netpbm-svgtopam.patch
Patch15:	netpbm-docfix.patch
Patch16:	netpbm-ppmfadeusage.patch
Patch17:	netpbm-fiasco-overflow.patch
Patch18:	netpbm-lz.patch
Patch20:	netpbm-noppmtompeg.patch
Patch21:	netpbm-cmuwtopbm.patch
Patch22:	netpbm-pamtojpeg2k.patch
Patch23:	netpbm-manfix.patch
Patch24:	netpbm-10.56.03-linkage_fix.diff
Patch100:	netpbm-10.35.57-format_not_a_string_literal_and_no_format_arguments.diff
Requires:	%{libname} >= %{version}
BuildRequires:	flex
BuildRequires:	pkgconfig(jasper)
BuildRequires:	jbig-devel
BuildRequires:	jpeg-devel
BuildRequires:	tiff-devel
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	python
BuildRequires:	python-devel
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

%package -n	%{develname}
Summary:	Development tools for programs which will use the netpbm libraries
Group:		Development/C
Requires:	%{libname} >= %{version}
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
%patch14 -p0 -b .svgtopam
%patch15 -p1 -b .docfix
%patch16 -p1 -b .ppmfadeusage
%patch17 -p1 -b .fiasco-overflow
%patch18 -p0 -b .lz
%patch20 -p1 -b .noppmtompeg
%patch21 -p1 -b .cmuwtopbmfix
%patch22 -p1 -b .pamtojpeg2kfix
%patch23 -p1 -b .manfix
%patch24 -p0 -b .linkage_fix

%patch100 -p1 -b .format_not_a_string_literal_and_no_format_arguments

sed -i 's/STRIPFLAG = -s/STRIPFLAG =/g' config.mk.in

##mv shhopt/shhopt.h shhopt/pbmshhopt.h
##perl -pi -e 's|shhopt.h|pbmshhopt.h|g' `find -name "*.c" -o -name "*.h"` ./GNUmakefile

rm -rf converter/other/jpeg2000/libjasper/
sed -i -e 's/^SUBDIRS = libjasper/SUBDIRS =/' converter/other/jpeg2000/Makefile

%build
%serverbuild
export CFLAGS="$CFLAGS -fPIC -flax-vector-conversions -fno-strict-aliasing"

./configure <<EOF



















EOF

TOP=`pwd`
make \
    CC="%{__cc}" \
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
    ../buildtools/makeman ${i}
done
for i in 1 3 5 ; do
    mkdir -p man/man${i}
    mv *.${i} man/man${i}
done

%install
rm -rf %{buildroot}

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
rm -f %{buildroot}%{_mandir}/man1/ppmtompeg.1*

install -d %{buildroot}%{_datadir}/printconf/mf_rules
cp %{SOURCE1} %{buildroot}%{_datadir}/printconf/mf_rules/

install -d %{buildroot}%{_datadir}/printconf/tests
cp test-images/* %{buildroot}%{_datadir}/printconf/tests/

%multiarch_includes %{buildroot}%{_includedir}/netpbm/pm_config.h

%files
%attr(0755,root,root) %{_bindir}/*
%{_datadir}/%{name}-%{version}
%dir %{_datadir}/printconf
%dir %{_datadir}/printconf/mf_rules
%dir %{_datadir}/printconf/tests
%{_datadir}/printconf/mf_rules/*
%{_datadir}/printconf/tests/*
%{_mandir}/man[15]/*

%files -n %{libname}
%doc doc/*
%attr(0755,root,root) %{_libdir}/lib*.so.%{major}*

%files -n %{develname}
%dir %{_includedir}/netpbm
%{_includedir}/netpbm/*.h
%{multiarch_includedir}/netpbm/pm_config.h
%attr(0755,root,root) %{_libdir}/lib*.so
%{_mandir}/man3/*


%changelog
* Sat Jan 28 2012 Oden Eriksson <oeriksson@mandriva.com> 10.57.01-1
+ Revision: 769496
- 10.57.01

* Thu Dec 22 2011 Oden Eriksson <oeriksson@mandriva.com> 10.56.05-2
+ Revision: 744411
- rebuilt against libtiff.so.5

* Mon Dec 19 2011 Oden Eriksson <oeriksson@mandriva.com> 10.56.05-1
+ Revision: 743712
- 10.56.05
- drop the static devel sub package

* Fri Dec 02 2011 Oden Eriksson <oeriksson@mandriva.com> 10.56.04-1
+ Revision: 737194
- sync with fedora
- various fixes

* Sat Nov 19 2011 Oden Eriksson <oeriksson@mandriva.com> 10.56.03-1
+ Revision: 731903
- slight cleanup
- another go at it...
- added some futile attempts to make it build, but seems this is a gcc issue
- 10.56.03 (sync with netpbm-10.56.03-1.fc17.src.rpm)
- rediffed some patches and dropped some
- new major 11 for the library, relinking has to be done
- attempt to relink against libpng15.so.15
- 10.47.30

  + Paulo Andrade <pcpa@mandriva.com.br>
    - Import netpbm changes to work with newer libpng.

* Wed Jul 27 2011 Oden Eriksson <oeriksson@mandriva.com> 10.47.29-1
+ Revision: 691938
- 10.47.29

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 10.47.27-1
+ Revision: 678124
- sync with netpbm-10.47.27-1.fc16.src.rpm

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 10.47.21-2
+ Revision: 661707
- multiarch fixes

* Tue Dec 21 2010 Oden Eriksson <oeriksson@mandriva.com> 10.47.21-1mdv2011.0
+ Revision: 623736
- 10.47.21 (sync slightly with fedora)
- remove the ppmtompeg man page too. ppmtompeg was removed due to licensing issues

* Tue Oct 12 2010 Oden Eriksson <oeriksson@mandriva.com> 10.47.20-1mdv2011.0
+ Revision: 585187
- more format string fixes
- rediffed one patch
- sync with fedora

* Mon Aug 09 2010 Oden Eriksson <oeriksson@mandriva.com> 10.47.17-1mdv2011.0
+ Revision: 568120
- sync with netpbm-10.47.17-1.fc14.src.rpm

* Sun Jan 31 2010 Oden Eriksson <oeriksson@mandriva.com> 10.47.09-1mdv2010.1
+ Revision: 498807
- really sync it
- sync with netpbm-10.47.09-2.fc13.src.rpm

* Mon Jan 11 2010 Funda Wang <fwang@mandriva.org> 10.47.07-2mdv2010.1
+ Revision: 489538
- rebuild for libjpeg v8

  + Oden Eriksson <oeriksson@mandriva.com>
    - 10.47.07

* Sat Dec 19 2009 Oden Eriksson <oeriksson@mandriva.com> 10.47.06-1mdv2010.1
+ Revision: 480135
- sync with netpbm-10.47.06-1.fc13.src.rpm

* Mon Nov 09 2009 Oden Eriksson <oeriksson@mandriva.com> 10.47.04-1mdv2010.1
+ Revision: 463436
- sync with netpbm-10.47.04-1.fc12.src.rpm
- rediffed the format string patch
- dropped the jpeg-7 patch, it was implemented upstream

* Sun Sep 27 2009 Olivier Blin <blino@mandriva.org> 10.35.64-4mdv2010.0
+ Revision: 450162
- buildrequire libx11-devel instead of full X11-devel
  (from Arnaud Patard)

* Sat Aug 15 2009 Oden Eriksson <oeriksson@mandriva.com> 10.35.64-3mdv2010.0
+ Revision: 416591
- fix build
- rebuilt against libjpeg v7

* Sat Jun 27 2009 Oden Eriksson <oeriksson@mandriva.com> 10.35.64-1mdv2010.0
+ Revision: 389813
- sync with netpbm-10.35.64-1.fc12.src.rpm
- rediffed one patch

* Wed May 06 2009 Oden Eriksson <oeriksson@mandriva.com> 10.35.62-1mdv2010.0
+ Revision: 372602
- sync with netpbm-10.35.62-1.fc11.src.rpm

* Sun Feb 01 2009 Oden Eriksson <oeriksson@mandriva.com> 10.35.59-1mdv2009.1
+ Revision: 336021
- sync with netpbm-10.35.59-1.fc11.src.rpm

* Sat Jan 31 2009 Oden Eriksson <oeriksson@mandriva.com> 10.35.57-2mdv2009.1
+ Revision: 335844
- rebuilt against new jbigkit major

* Sat Dec 20 2008 Oden Eriksson <oeriksson@mandriva.com> 10.35.57-1mdv2009.1
+ Revision: 316456
- sync with netpbm-10.35.57-1.fc11.src.rpm
- fix build with -Werror=format-security (P21)
- use %%ldflags

* Mon Oct 27 2008 Oden Eriksson <oeriksson@mandriva.com> 10.35.53-1mdv2009.1
+ Revision: 297571
- sync with netpbm-10.35.53-1.fc10.src.rpm

* Sat Jul 12 2008 Oden Eriksson <oeriksson@mandriva.com> 10.35.46-1mdv2009.0
+ Revision: 234002
- sync (slightly) with netpbm-10.35.46-1.fc10.src.rpm
- fix deps
- fix a typo in P8

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Wed Nov 07 2007 Oden Eriksson <oeriksson@mandriva.com> 10.34-10mdv2008.1
+ Revision: 106741
- P16: security fix for CVE-2007-2721 (embedded libjasper)
- added P8 to link against system libs such as jbigkit and libjasper,
  that should render P16 obsolete, but keep it for reference.

* Mon Oct 15 2007 Funda Wang <fwang@mandriva.org> 10.34-9mdv2008.1
+ Revision: 98351
- fix requires of develname

* Mon Oct 01 2007 Oden Eriksson <oeriksson@mandriva.com> 10.34-8mdv2008.0
+ Revision: 94149
- rebuilt due to missing packages

* Wed Sep 19 2007 Guillaume Rousse <guillomovitch@mandriva.org> 10.34-7mdv2008.0
+ Revision: 90006
- rebuild

* Tue Sep 18 2007 Anssi Hannula <anssi@mandriva.org> 10.34-6mdv2008.0
+ Revision: 89729
- rebuild due to package loss

* Sun Sep 09 2007 Oden Eriksson <oeriksson@mandriva.com> 10.34-5mdv2008.0
+ Revision: 83516
- new devel naming


* Sun Oct 15 2006 Oden Eriksson <oeriksson@mandriva.com> 10.34-4mdv2007.0
+ Revision: 64864
- bzip2 cleanup
- rebuild
- bunzip patches
- Import netpbm

* Sun Jul 16 2006 Christiaan Welvaart <cjw@daneel.dyndns.org> 10.34-2
- add BuildRequires: libx11-devel libxml2-devel

* Fri Jul 14 2006 Stew Benedict <sbenedict@mandriva.com> 10.34-1mdv2007.0
- New release 10.34
- update P7(Red Hat security patch, name it 10.34 though)
- rediff P13(bmptopnm)
- drop P16(ppmtogif), P17(nstring), P18(pnmtofits overflow)
- add 3 more CR to the empty configure input

* Sat May 27 2006 Stew Benedict <sbenedict@mandriva.com> 10.33-2mdv2007.0
- P18: fix for #21444 (buffer overflow in pnmtofits)

* Tue May 09 2006 Stew Benedict <sbenedict@mandriva.com> 10.33-1mdk
- 10.33 
- drop commented P8,12; drop P2,9,15; update P13
- update P3,6,7; add P15,16,17 (from Fedora)

* Fri Nov 04 2005 Frederic Crozat <fcrozat@mandriva.com> 10.29-4mdk
- package now owns its share directories

* Wed Nov 02 2005 Olivier Blin <oblin@mandriva.com> 10.29-3mdk
- from Stew Benedict: security update for CAN-2005-2978 (P15, #19447)
  (diff against pnmtopng.c from 0.30)

* Wed Nov 02 2005 Abel Cheung <deaddog@mandriva.org> 10.29-2mdk
- Rebuild

* Sun Aug 21 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 10.29-1mdk
- 10.29
- sync with fedora:
	o fix segfault in bmptopnm caused by freeing an uninitialized pointer (P13)
	o update .CAN-2005-2471 patch (P14)
	o update P4, P6 & P7
- drop P8
- fix buildconflicts
- %%mkrel

* Sun Aug 14 2005 Stew Benedict <sbenedict@mandriva.com> 10.26-5mdk
- buildconflicts

* Sun Aug 14 2005 Stew Benedict <sbenedict@mandriva.com> 10.26-4mdk
- rebuild in a clean(er) environment without libsvgalib

* Sat Aug 13 2005 Olivier Blin <oblin@mandriva.com> 10.26-3mdk
- from Vincent Danen: security fix for pstopnm (Patch12)
- fix Patch7 for gcc4
- remove Requires on release

* Wed Feb 16 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 10.26-2mdk
- multiarch
- netpbm is very likely to depend on libm (pow, log), aka fix build of
  e.g. gocr with netpbm support on x86_64 and others without such builtins

* Thu Jan 13 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 10.26-1mdk
- 10.26
- update security patch (P7 from fedora)
- drop P9 (merged with P7) & P10 (merged upstream)

* Sat Dec 18 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 10.25-2mdk
- remove fix of path to perl in scripts (not needed anymore)

* Fri Dec 17 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 10.25-1mdk
- sync with fedora (about friggin' time!)
- cosmetics

