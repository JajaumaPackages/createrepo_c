Summary:        Creates a common metadata repository
Name:           createrepo_c
Version:        0.1.8
Release:        1%{?dist}
License:        GPLv2
Group:          System Environment/Base
Source0:        https://fedorahosted.org/releases/c/r/createrepo_c/%{name}-%{version}.tar.xz
URL:            https://fedorahosted.org/createrepo_c/

BuildRequires:  cmake
BuildRequires:  glib2-devel >= 2.22.0
BuildRequires:  file-devel
BuildRequires:  zlib-devel
BuildRequires:  bzip2-devel
BuildRequires:  rpm-devel >= 4.8.0
BuildRequires:  libxml2-devel
BuildRequires:  libcurl-devel
BuildRequires:  expat-devel
BuildRequires:  xz-devel
BuildRequires:  sqlite-devel
BuildRequires:  doxygen
Requires:       %{name}-libs =  %{version}-%{release}

%description
C implementation of Createrepo. This utility will generate a common
metadata repository from a directory of rpm packages


%package libs
Summary:    Library for repodata manipulation
Group:      Development/Libraries

%description libs
Libraries for applications using the createrepo_c library
for easy manipulation with a repodata.


%package devel
Summary:    Library for repodata manipulation
Group:      Development/Libraries
Requires:   pkgconfig >= 1:0.14
Requires:   %{name}-libs =  %{version}-%{release}

%description devel
This package contains the createrepo_c C library and header files.
These development files are for easy manipulation with a repodata.


%prep
%setup -q

%build
%cmake .
make %{?_smp_mflags} RPM_OPT_FLAGS="$RPM_OPT_FLAGS"
make doc

%install
make install DESTDIR=$RPM_BUILD_ROOT/

%post -n %{name}-libs -p /sbin/ldconfig

%postun -n %{name}-libs -p /sbin/ldconfig

%files
%doc README
%doc COPYING
%_mandir/man8/createrepo_c.8.*
%_mandir/man8/mergerepo_c.8.*
%config%{_sysconfdir}/bash_completion.d/createrepo_c.bash
%{_bindir}/createrepo_c
%{_bindir}/mergerepo_c

%files libs
%doc COPYING
%{_libdir}/libcreaterepo_c.so.*

%files devel
%{_libdir}/libcreaterepo_c.so
%{_libdir}/pkgconfig/createrepo_c.pc
%{_includedir}/createrepo_c/*
%doc COPYING
%doc doc/html

%changelog
* Wed Aug  15 2012 Tomas Mlcoch <tmlcoch at redhat.com> - 0.1.8-1
- New interface of repomd module
- New cmd options: --repo --revision --distro --content --basedir
- New createrepo_c specific cmd option --keep-all-metadata
- Few bugfixes

* Tue Jul  26 2012 Tomas Mlcoch <tmlcoch at redhat.com> - 0.1.7-1
- SQLite support
- Bash completion
- createrepo_c support for --compress-type param
- Improved logging
- Subpackages -devel and -libsi
- Relicensed to GPLv2
- Doxygen documentation in devel package
- README update

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun  11 2012 Tomas Mlcoch <tmlcoch at redhat.com> - 0.1.5-1
- Support for .xz compression
- Unversioned .so excluded from installation

* Tue Jun   4 2012 Tomas Mlcoch <tmlcoch at redhat.com> - 0.1.4-1
- New mergerepo params: --all, --noarch-repo and --method
- Fix segfault when more than one --excludes param used

* Tue May  28 2012 Tomas Mlcoch <tmlcoch at redhat.com> - 0.1.3-1
- Set RelWithDebInfo as default cmake build type

* Tue May  23 2012 Tomas Mlcoch <tmlcoch at redhat.com> - 0.1.2-1
- Add version.h header file

* Tue May  23 2012 Tomas Mlcoch <tmlcoch at redhat.com> - 0.1.1-1
- Add license

* Tue May  9 2012 Tomas Mlcoch <tmlcoch at redhat.com> - 0.1.0-1
- First public release
