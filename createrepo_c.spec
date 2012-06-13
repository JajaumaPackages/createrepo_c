Summary:        Creates a common metadata repository
Name:           createrepo_c
Version:        0.1.5
Release:        1%{?dist}
License:        LGPLv2
Group:          System Environment/Base
Source0:        https://fedorahosted.org/releases/c/r/createrepo_c/%{name}-%{version}.tar.xz
URL:            https://fedorahosted.org/createrepo_c/

BuildRequires:  cmake
BuildRequires:  glib2-devel >= 2.26.0
BuildRequires:  file-devel
BuildRequires:  zlib-devel
BuildRequires:  bzip2-devel
BuildRequires:  rpm-devel >= 4.8.1
BuildRequires:  libxml2-devel
BuildRequires:  libcurl-devel
BuildRequires:  expat-devel
BuildRequires:  xz-devel

%description
C implementation of Createrepo. This utility will generate a common
metadata repository from a directory of rpm packages

%prep
%setup -q

%build
%cmake .
make %{?_smp_mflags} RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
make install DESTDIR=$RPM_BUILD_ROOT/

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc AUTHORS
%doc README
%doc COPYING
%_mandir/man8/createrepo_c.8.*
%_mandir/man8/mergerepo_c.8.*
%{_libdir}/libcreaterepo_c.so.*
%{_bindir}/createrepo_c
%{_bindir}/mergerepo_c

%changelog
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
