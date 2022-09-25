#!/bin/sh
TMPDIR=`mktemp -d /tmp/netpbmvcXXXXXX`
mkdir -p "$TMPDIR"
cd "$TMPDIR"
wget "http://svn.code.sf.net/p/netpbm/code/advanced/version.mk" &>/dev/null
cat >>version.mk <<'EOF'

all:
	@echo $(NETPBM_MAJOR_RELEASE).$(NETPBM_MINOR_RELEASE).$(NETPBM_POINT_RELEASE)
EOF
VERSION=$(make -f version.mk)
cd /
rm -rf "$TMPDIR"
echo $VERSION
