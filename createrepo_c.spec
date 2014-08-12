%global gitrev 1e32fcd
# gitrev is output of: git rev-parse --short HEAD

Summary:        Creates a common metadata repository
Name:           createrepo_c
Version:        0.6.1
Release:        1%{?dist}
License:        GPLv2
Group:          System Environment/Base
# Use the following commands to generate the tarball:
#  git clone https://github.com/Tojaj/createrepo_c.git
#  cd createrepo_c
#  utils/make_tarball.sh %{gitrev}
Source0:        createrepo_c-%{gitrev}.tar.xz
URL:            https://github.com/Tojaj/createrepo_c

BuildRequires:  bzip2-devel
BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  expat-devel
BuildRequires:  file-devel
BuildRequires:  glib2-devel >= 2.22.0
BuildRequires:  libcurl-devel
BuildRequires:  libxml2-devel
BuildRequires:  openssl-devel
BuildRequires:  python2-devel
BuildRequires:  python-nose
BuildRequires:  python-sphinx
BuildRequires:  rpm-devel >= 4.8.0-28
BuildRequires:  sqlite-devel
BuildRequires:  xz-devel
BuildRequires:  zlib-devel
Requires:       %{name}-libs =  %{version}-%{release}
%if 0%{?rhel} == 6
Requires: rpm >= 4.8.0-28
%else
Requires: rpm >= 4.9.0
%endif

%description
C implementation of Createrepo.
A set of utilities (createrepo_c, mergerepo_c, modifyrepo_c)
for generating a common metadata repository from a directory of
rpm packages and maintaining it.

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

%package -n python-createrepo_c
Summary:    Python bindings for the createrepo_c library
Group:      Development/Languages
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description -n python-createrepo_c
Python bindings for the createrepo_c library.

%prep
%setup -q -n createrepo_c

%build
%cmake .
make %{?_smp_mflags} RPM_OPT_FLAGS="$RPM_OPT_FLAGS"
make doc-c

%check
make tests
make ARGS="-V" test

%install
make install DESTDIR=$RPM_BUILD_ROOT/

%post -n %{name}-libs -p /sbin/ldconfig

%postun -n %{name}-libs -p /sbin/ldconfig

%files
%doc README.md
%doc COPYING
%_mandir/man8/createrepo_c.8.*
%_mandir/man8/mergerepo_c.8.*
%_mandir/man8/modifyrepo_c.8.*
%config%{_sysconfdir}/bash_completion.d/createrepo_c.bash
%{_bindir}/createrepo_c
%{_bindir}/mergerepo_c
%{_bindir}/modifyrepo_c

%files libs
%doc COPYING
%{_libdir}/libcreaterepo_c.so.*

%files devel
%{_libdir}/libcreaterepo_c.so
%{_libdir}/pkgconfig/createrepo_c.pc
%{_includedir}/createrepo_c/*
%doc COPYING
%doc doc/html

%files -n python-createrepo_c
%{python_sitearch}/createrepo_c/

%changelog
* Tue Aug  12 2014 Tomas Mlcoch <tmlcoch at redhat.com> - 0.6.1-1
- updateinfo: Use Python datetime objects in python bindings

* Tue Aug   5 2014 Tomas Mlcoch <tmlcoch at redhat.com> - 0.6.0-1
- Support for updateinfo.xml manipulation (including Python bindings)

* Fri Jul  18 2014 Tomas Mlcoch <tmlcoch at redhat.com> - 0.5.0-1
- Experimental delta rpm (DRPM) support (Disabled in Fedora build).

* Thu Jun  26 2014 Tomas Mlcoch <tmlcoch at redhat.com> - 0.4.1-1
- Initialize threads correctly on old versions of GLib2 (RhBug: 1108787)
- Do not print log domain (get rid off C_CREATEREPOLIB prefix in log messages)
- Implements support for --cachedir
- New option --retain-old-md-by-age
- Few small API changes

* Tue May   6 2014 Tomas Mlcoch <tmlcoch at redhat.com> - 0.4.0-1
- Change default behavior of repodata files handling. (RhBug: 1094539)
  See: https://github.com/Tojaj/createrepo_c/wiki/New-File-Handling
  By default, createrepo leaves old groupfiles (comps files)
  in the repodata/ directory during update.
  Createrepo_c did the same thing but the version 0.4.0 changes this behaviour.

* Thu Apr  10 2014 Tomas Mlcoch <tmlcoch at redhat.com> - 0.3.1-2
- Support for weak and rich dependecies

* Mon Mar  10 2014 Tomas Mlcoch <tmlcoch at redhat.com> - 0.3.0-1
- Relevant only for developers using createrepo_c library: New approach for
  metadata loading in case of internal high-level parser functions (see commit
  messages for more information: d6ed327595, 0b0e75203e, ad1e8450f5)
- Support for changelog limit value == -1 (include all changelogs)
- Update debug compilation flags
- Update man pages (Add synompsis with usage)
- Update usage examples in help

* Thu Feb  20 2014 Tomas Mlcoch <tmlcoch at redhat.com> - 0.2.2-1
- Temporary remove deltarepo subpackages
- cmake: Do not install deltarepo stuff yet
- helper: Removed cr_remove_metadata() and cr_get_list_of_md_locations()
- Add module helpers
- Sanitize strings before writting them to XML or sqlitedb (ISSUE #3)

* Mon Jan  27 2014 Tomas Mlcoch <tmlcoch at redhat.com> - 0.2.1-3
- New expert option: --ignore-lock

* Mon Jan  20 2014 Tomas Mlcoch <tmlcoch at redhat.com> - 0.2.1-2
- More effort to avoid residual .repodata/ directory on error
- Add deltarepo and python-deltarepo subpackages
- Add modifyrepo_c
- Add documentation for python bindings
- Refactored code & a lot of little bug fixes

* Wed Aug  14 2013 Tomas Mlcoch <tmlcoch at redhat.com> - 0.2.1-1
- checksum: Set SHA to be the same as SHA1 (For compatibility with original
  Createrepo)

* Mon Aug   5 2013 Tomas Mlcoch <tmlcoch at redhat.com> - 0.2.0-1
- Speedup (More parallelization)
- Changed C API
- Add python bindings
- A lot of bugfixes
- Add new make targets: tests (make tests - builds c tests) and test
  (make test - runs c and python test suits).
- Changed interface of most of C modules - Better error reporting
  (Add GError ** param).
- Experimental Python bindings (Beware: The interface is not final yet!).
- package: Add cr_package_copy method.
- sqlite: Do not recreate tables and triggers while opening existing db.
- mergerepo_c: Implicitly use --all with --koji.
- Man page update.

* Thu Apr  11 2013 Tomas Mlcoch <tmlcoch at redhat.com> - 0.1.17-3
- mergerepo_c: Add --simple-md-filenames and --unique-md-filenames
options. (RhBug: 950994)
- mergerepo_c: Always include noarch while mimic koji
mergerepos. (RhBug: 950991)
- Rename cr_package_parser_shutdown to cr_package_parser_cleanup()
- cr_db_info_update is now safe from sqlinjection.

* Mon Mar  25 2013 Tomas Mlcoch <tmlcoch at redhat.com> - 0.1.17-1
- Fix double free() when old metadata parsing failed. (related to RhBug: 920795)
- Convert all strings to UTF-8 while dumping XML. (related RhBug: 920795)

* Mon Mar  11 2013 Tomas Mlcoch <tmlcoch at redhat.com> - 0.1.16-2
- Remove creation of own empty rpm keyring for a transaction set.
This is not necessary since rpm-4.8.0-28 (rpm commit
cad147070e5513312d851f44998012e8f0cdf1e3). Moreover, own rpm keyring
causes a race condition in threads (causing double free()) which use
rpmReadPackageFile() called from cr_package_from_rpm().

* Thu Mar  07 2013 Tomas Mlcoch <tmlcoch at redhat.com> - 0.1.16-1
- Fix usage of rpm keyring (RhBug:918645)
- More generic interface of repomd module
- Code refactoring
- Add some usage examples into the doxygen documentation and .h files
- Rename version constants in version.h
- New function cr_package_nevra (returns package nevra string)

* Mon Feb  11 2013 Tomas Mlcoch <tmlcoch at redhat.com> - 0.1.15-1
- Fix bug in final move from .repodata/ -> repodata/
- Fix warnings from RPM library. RPM library is thread-unsafe. This
includes also reading headers. Use of empty keyring for rpm transaction
should work around the problem.

* Tue Nov  27 2012 Tomas Mlcoch <tmlcoch at redhat.com> - 0.1.14-1
- Fix filelists database generation (use '.' instead of '' for current dir)

* Tue Nov  20 2012 Tomas Mlcoch <tmlcoch at redhat.com> - 0.1.13-1
- Fix race-condition during task buffering in createrepo_c

* Tue Nov  20 2012 Tomas Mlcoch <tmlcoch at redhat.com> - 0.1.12-2
- Fix removing old repomd.xml while --update

* Thu Nov  15 2012 Tomas Mlcoch <tmlcoch at redhat.com> - 0.1.12-1
- Fix bug in sqlite filelists database
- Fix memory leak

* Fri Nov  09 2012 Tomas Mlcoch <tmlcoch at redhat.com> - 0.1.11-1
- Deterministic output! Packages in output repodata are now sorted
by ASCII value
- Support for Koji mergerepos behaviour in mergerepo_c
(new --koji, --groupfile and --blocked params)
- Better atomicity while finall move .repodata/ -> repodata/
- Repomd module supports pkgorigins record
- Some new functions in misc module
- Small changes in library interface

* Wed Oct  03 2012 Tomas Mlcoch <tmlcoch at redhat.com> - 0.1.10-1
- Another memory usage optimalization

* Mon Sep  03 2012 Tomas Mlcoch <tmlcoch at redhat.com> - 0.1.9-1
- Some changes in library interface
- Memory usage optimalization
- Fix a segfault and a race condition
- New cmd options: --read-pkgs-list and --retain-old-md param
- Few other bugfixes

* Wed Aug  15 2012 Tomas Mlcoch <tmlcoch at redhat.com> - 0.1.8-1
- New interface of repomd module
- New cmd options: --repo --revision --distro --content --basedir
- New createrepo_c specific cmd option --keep-all-metadata
- Few bugfixes

* Thu Jul  26 2012 Tomas Mlcoch <tmlcoch at redhat.com> - 0.1.7-1
- SQLite support
- Bash completion
- createrepo_c support for --compress-type param
- Improved logging
- Subpackages -devel and -libsi
- Relicensed to GPLv2
- Doxygen documentation in devel package
- README update

* Mon Jun  11 2012 Tomas Mlcoch <tmlcoch at redhat.com> - 0.1.5-1
- Support for .xz compression
- Unversioned .so excluded from installation

* Mon Jun   4 2012 Tomas Mlcoch <tmlcoch at redhat.com> - 0.1.4-1
- New mergerepo params: --all, --noarch-repo and --method
- Fix segfault when more than one --excludes param used

* Mon May  28 2012 Tomas Mlcoch <tmlcoch at redhat.com> - 0.1.3-1
- Set RelWithDebInfo as default cmake build type

* Wed May  23 2012 Tomas Mlcoch <tmlcoch at redhat.com> - 0.1.2-1
- Add version.h header file

* Wed May  23 2012 Tomas Mlcoch <tmlcoch at redhat.com> - 0.1.1-1
- Add license

* Wed May  9 2012 Tomas Mlcoch <tmlcoch at redhat.com> - 0.1.0-1
- First public release
