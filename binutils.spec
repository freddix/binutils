# based on PLD Linux spec git://git.pld-linux.org/packages/binutils.git
%bcond_with	pass2

Summary:	GNU Binary Utility Development Utilities
Name:		binutils
Version:	2.25
Release:	2
Epoch:		3
License:	GPL
Group:		Development/Tools
#Source0:	http://www.kernel.org/pub/linux/devel/binutils/%{name}-%{version}.tar.bz2
Source0:	ftp://ftp.gnu.org/gnu/binutils/%{name}-%{version}.tar.bz2
# Source0-md5:	a5dd5dd2d212a282cc1d4a84633e0d88
URL:		http://sources.redhat.com/binutils/
%if %{without pass2}
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gettext
BuildRequires:	perl-tools-pod
BuildRequires:	texinfo
%endif
Requires(post,postun):	/usr/sbin/ldconfig
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if %{with pass2}
%define	    no_install_post_strip   1
%define	    no_install_post_chrpath 1
%define	    _enable_debug_packages  0
%endif

%description
A set of programs to assemble and manipulate binary and object files.

%package libs
Summary:	GNU binutils shared libraries (libbfd, libopcodes).
Group:		Libraries

%description libs
GNU binutils shared libraries (libbfd, libopcodes).

%package devel
Summary:	Development files for GNU binutils libraries
Group:		Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}

%description devel
Development files for GNU binutils libraries.

%package static
Summary:	GNU binutils static libraries
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
GNU binutils static libraries.

%prep
%setup -q

%build
cp -f /usr/share/automake/config.* .

install -d build
cd build

CFLAGS="%{rpmcflags}"	\
LDFLAGS="%{rpmldflags}"	\
../configure %{_target_platform}	\
	--infodir=%{_infodir}		\
	--libdir=%{_libdir}		\
	--mandir=%{_mandir}		\
	--prefix=%{_prefix}		\
	--disable-debug			\
	--disable-werror		\
%if %{without pass2}
	--enable-gold			\
	--enable-ld=default		\
	--enable-plugins		\
	--enable-shared			\
%endif
	--with-lib-path=%{_libdir}	\
	--with-tooldir=%{_prefix}
%{__make} configure-host -j1
%{__make} tooldir=%{_prefix}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	tooldir=%{_prefix} \
	DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_infodir}/dir
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

# remove these man pages unless we cross-build for win*/netware platforms.
# however, this should be done in Makefiles.
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/{dlltool,nlmconv,windres}.1

%find_lang bfd
%find_lang binutils
%find_lang gas
%find_lang gprof
touch ld.lang
%find_lang ld
%find_lang opcodes
cat bfd.lang opcodes.lang > %{name}-libs.lang
cat gas.lang gprof.lang ld.lang >> %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	-p /usr/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%post	devel -p /usr/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	devel -p /usr/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/addr2line
%attr(755,root,root) %{_bindir}/ar
%attr(755,root,root) %{_bindir}/as
%attr(755,root,root) %{_bindir}/c++filt
%attr(755,root,root) %{_bindir}/elfedit
%attr(755,root,root) %{_bindir}/gprof
%attr(755,root,root) %{_bindir}/ld
%attr(755,root,root) %{_bindir}/ld.bfd
%attr(755,root,root) %{_bindir}/nm
%attr(755,root,root) %{_bindir}/objcopy
%attr(755,root,root) %{_bindir}/objdump
%attr(755,root,root) %{_bindir}/ranlib
%attr(755,root,root) %{_bindir}/readelf
%attr(755,root,root) %{_bindir}/size
%attr(755,root,root) %{_bindir}/strings
%attr(755,root,root) %{_bindir}/strip
%if %{without pass2}
%attr(755,root,root) %{_bindir}/dwp
%attr(755,root,root) %{_bindir}/ld.gold
%endif
%{_prefix}/lib/ldscripts

%{_mandir}/man1/*

%{_infodir}/as.info*
%{_infodir}/binutils.info*
%{_infodir}/gprof.info*
%{_infodir}/ld.info*

%files libs -f %{name}-libs.lang
%defattr(644,root,root,755)
%if %{without pass2}
%attr(755,root,root) %{_libdir}/libbfd-*.so
%attr(755,root,root) %{_libdir}/libopcodes-*.so
%endif

%files devel
%defattr(644,root,root,755)
%if %{without pass2}
%attr(755,root,root) %{_libdir}/libbfd.so
%attr(755,root,root) %{_libdir}/libopcodes.so
%endif
%{_includedir}/*.h
%{_infodir}/bfd.info*

%files static
%defattr(644,root,root,755)
%{_libdir}/libbfd.a
%{_libdir}/libopcodes.a

