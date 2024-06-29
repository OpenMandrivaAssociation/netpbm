#!/bin/sh
rm -rf netpbm
svn checkout https://svn.code.sf.net/p/netpbm/code/advanced netpbm
cp netpbm/version.mk .
cat >>version.mk <<'EOF'

all:
	@echo $(NETPBM_MAJOR_RELEASE).$(NETPBM_MINOR_RELEASE).$(NETPBM_POINT_RELEASE)
EOF
VERSION=$(make -f version.mk)
svn checkout https://svn.code.sf.net/p/netpbm/code/userguide netpbm/userguide
# Using this instead of svn export because of the 2 mixed repositories
# (code and userguide)
find netpbm -name .svn -type d |xargs rm -rf
# remove the ppmtompeg code due to patents
rm -rf netpbm/converter/ppm/ppmtompeg

mv netpbm netpbm-${VERSION}
tar cf netpbm-${VERSION}.tar netpbm-${VERSION}
zstd --ultra --rm -22 netpbm-${VERSION}.tar
