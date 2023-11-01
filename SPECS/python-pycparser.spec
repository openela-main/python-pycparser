%if 0%{?fedora} || 0%{?rhel} >= 8
%global with_python3 1
%endif

%if 0%{?rhel} > 7
# Disable python2 build by default
%bcond_with python2
%else
%bcond_without python2
%endif

Name:           python-pycparser
Summary:        C parser and AST generator written in Python
Version:        2.14
Release:        14%{?dist}
License:        BSD
Group:          System Environment/Libraries
URL:            http://github.com/eliben/pycparser
Source0:        http://github.com/eliben/pycparser/archive/release_v%{version}.tar.gz
Source1:        pycparser-0.91.1-remove-relative-sys-path.py

Patch100:       pycparser-2.10-ply.patch
# This is Fedora-specific; I don't think we should request upstream to
# remove embedded libraries from their distribuution, when we can remove
# them during packaging.

BuildArch:      noarch

%if %{with python2}
BuildRequires:  python2-devel python2-setuptools

# for unit tests
BuildRequires:  python2-ply >= 3.6
%endif # with python2

BuildRequires:  dos2unix

%if 0%{?with_python3}
BuildRequires:  python3-devel python3-setuptools
# for unit tests
BuildRequires:  python3-ply       
%endif # if with_python3

%description
pycparser is a complete parser for the C language, written in pure Python.
It is a module designed to be easily integrated into applications that
need to parse C source code.

%if %{with python2}
%package -n python2-pycparser
Summary:        C parser and AST generator written in Python
Group:          System Environment/Libraries
Requires:       python2-ply >= 3.6
%{?python_provide:%python_provide python2-pycparser}

%description -n python2-pycparser
pycparser is a complete parser for the C language, written in pure Python.
It is a module designed to be easily integrated into applications that
need to parse C source code.
%endif # with python2

%if 0%{?with_python3}
%package -n python3-pycparser
Summary:        C parser and AST generator written in Python
Group:          System Environment/Libraries
Requires:       python3-ply
%{?python_provide:%python_provide python3-pycparser}

%description -n python3-pycparser
pycparser is a complete parser for the C language, written in pure Python.
It is a module designed to be easily integrated into applications that
need to parse C source code.
%endif # if with_python3

%prep
%setup -q -n pycparser-release_v%{version}
%patch100 -p1 -F5 -b .ply

# remove embedded copy of ply
rm -rf pycparser/ply

# examples
%if 0%{?with_python3}
%{__python3} %{SOURCE1} examples
%else
%{__python2} %{SOURCE1} examples
%endif
dos2unix LICENSE

%build
%if %{with python2}
%py2_build
pushd build/lib/pycparser
%{__python2} _build_tables.py
popd
%endif # with python2

%if 0%{?with_python3}
%py3_build
pushd build/lib/pycparser
%{__python3} _build_tables.py
popd
%endif # with_python3

%install
%if %{with python2}
%py2_install
%endif # with python2

%if 0%{?with_python3}
%py3_install
%endif # with_python3

%check
%if %{with python2}
%{__python2} tests/all_tests.py
%endif # with python2

%if 0%{?with_python3}
%{__python3} tests/all_tests.py
%endif # with_python3
 
 %if %{with python2}
%files -n python2-pycparser
%license LICENSE
%doc examples
%{python2_sitelib}/pycparser/
%{python2_sitelib}/pycparser-*.egg-info
%endif # with python2

%if 0%{?with_python3}
%files -n python3-pycparser
%license LICENSE
%doc examples
%{python3_sitelib}/pycparser/
%{python3_sitelib}/pycparser-*.egg-info
%endif # with_python3

%changelog
* Sun Jun 10 2018 Charalampos Stratakis <cstratak@redhat.com> - 2.14-14
- Conditionalize the python2 subpackage

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.14-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Sep 27 2017 Troy Dawson <tdawson@redhat.com> - 2.14-12
- Cleanup spec file conditionals

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.14-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.14-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 6 2017 Orion Poplawski <orion@cora.nwra.com> - 2.14-9
- Ship python2-pycparser
- Modernize spec

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 2.14-8
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14-7
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Jul  8 2016 Tom Callaway <spot@fedoraproject.org> - 2.14-6
- rebuild to update yacctab.py

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Oct 13 2015 Robert Kuska <rkuska@redhat.com> - 2.14-4
- Rebuilt for Python3.5 rebuild

* Tue Jul 14 2015 Stephen Gallagher <sgallagh@redhat.com> - 2.14-3
- Rebuild alongside python-ply 3.6

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 09 2015 Nathaniel McCallum <npmccallum@redhat.com> - 2.14-1
- Update to 2.14

* Wed Aug 20 2014 Eric Smith <brouhaha@fedoraproject.org> 2.10-1
- Update to latest upstream.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.09.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 12 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 2.09.1-8
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.09.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Eric Smith <brouhaha@fedoraproject.org> 2.09.1-6
- Added Python 3 support.

* Mon Jul 22 2013 Eric Smith <brouhaha@fedoraproject.org> 2.09.1-5
- Renumbered Fedora-specific Patch1 to Patch100
- Added new Patch1 to fix table generation when the build system
  already has a python-pycparser package installed.
- Submitted Patch0 and Patch1 as upstream issues.
- Added comments about patches.

* Sun Jul 21 2013 Eric Smith <brouhaha@fedoraproject.org> 2.09.1-4
- Upstream repository is now on github.
- Fix rpmlint strange-permission complaint.
- Rename patches, Source1 to all start with pycparser-{version}, to
  simplify updating patches for future upstream releases.

* Sun Jul 21 2013 Eric Smith <brouhaha@fedoraproject.org> 2.09.1-3
- Run _build_tables.py to build the lextab.py and yacctab.py; otherwise
  they have to be regenerated at runtime for no benefit.

* Tue Mar 19 2013 Jos de Kloe <josdekloe@gmail.com> 2.09.1-2
- remove the embedded ply code

* Fri Jan 18 2013 Scott Tsai <scottt.tw@gmail.com> 2.09.1-1
- upstream 2.09.1
