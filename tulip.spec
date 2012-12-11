%define name	tulip
%define version	3.7.0
%define release 3
%define major	0
%define api 3.7
%define libname	%mklibname %name %major
%define develname %mklibname -d %name

Summary:	A program that allows visualization of huge graphs
Name:		%{name}
Version:	%{version}
Release:	%{release}
URL:		http://www.tulip-software.org
Source0:	http://downloads.sourceforge.net/project/auber/%{name}/%{name}-%{version}/%{name}-%{version}-src.tar.gz
#Source10:	%name-16.png
#Source11:	%name-32.png
#Source12:	%name-48.png
#Source13:	mandriva-%{name}.desktop
#Patch0:		tulip-3.3.0-fix-link.patch
#Patch1:		tulip-3.4.1-fix-cmake-install.patch
Patch0:		0001-fix-Missing-include-stdlib.h.patch
Patch1:		0001-fix-Force-link-of-libOGDF.so-against-pthread.patch
Patch2:		0001-fix-Tulip-lib-install-dir.patch
Patch3:		0001-fix-Path-for-python-packages-installation.patch
Patch4:		0001-fix-Use-local-XSL-references.patch
Patch5:		0001-fix-Install-python-modules-in-site-packages.patch
License:	GPLv2+
Group:		Graphics
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildRequires:	qt4-devel qt-assistant-adp-devel qt4-assistant
BuildRequires:	cmake
BuildRequires:	pkgconfig(glew)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	jpeg-devel
BuildRequires:	xmltex doxygen graphviz libxml2-utils
BuildRequires:	gomp-devel
BuildRequires:	python-devel
BuildRequires:	python-sphinx
BuildRequires:	python-sip
BuildRequires:	doxygen
BuildRequires:	docbook-style-xsl
BuildRequires:	ftgl-devel
BuildRequires:	java
Obsoletes: tulip-render < %{version}

%description
Tulip software is a system dedicated to the visualization of huge graphs.
It manages graphs with a number of elements (node and edges) up to 500.000 
on a personal computer (PIII 600, with 256mo). Its SuperGraph technology 
architecture enables to do the following things :

  * 3D visualizations
  * 3D modifications
  * Plug-in support for easy evolution
  * Building of clusters and navigation into it
  * Automatic drawing of graphs
  * Automatic clustering of graphs
  * Automatic selection of elements
  * Automatic Metric coloration of graphs

%package -n     %{libname}
Summary:        A development library for handling large graphs
Group:		    System/Libraries
Provides:       lib%{name} = %version-%release

%description -n %{libname}
A library for handling large graphs

%package -n     %{develname}
Summary:        A library for handling large graphs
Group:          Development/Other
Provides:	%{name}-devel = %version-%release
Provides:	lib%{name}-devel = %version-%release
Requires:       %libname = %version-%release
Requires:       %{libname}-qt = %version-%release
Requires:       %{libname}-ogl = %version-%release
Requires:       %{libname}-ogdf = %version-%release
Obsoletes:	%{libname}-devel

%description -n %{develname}
A library for handling large graphs.
You need this package if you plan to build apps using
tulip libraries.

%package -n     %{libname}-ogl
Summary:        A library for displaying graph in a GL context
Group:		Graphics
Requires:       %{libname} = %version-%release
Requires:	%{name}-ogl-data = %{version}-%{release}
Provides:       %name-qt = %version-%release
Provides:       lib%name-ogl = %version-%release

%description -n %{libname}-ogl
A library for displaying graph in a GL context

%package -n     %{name}-ogl-data
Summary:        Data files for Tulip's library for displaying graph in a GL context
Group:		Graphics
BuildArch:	noarch

%description -n %{name}-ogl-data
Data files for Tulip's library for displaying graph in a GL context

%package -n     %{libname}-ogdf
Summary:        A library for playing with graph
Group:		Development/C++
Requires:       %{libname} = %version-%release
Provides:       lib%name-ogdf = %version-%release

%description -n %{libname}-ogdf
A Library for playing with graph

%package -n     %{libname}-qt
Summary:        A set of Qt Widgets for Tulip/Tulip-qt
Group:          Graphics
Requires:       %libname = %version-%release
Provides:       %name-qt = %version-%release
Provides:       lib%name-qt = %version-%release
Conflicts:	%{develname} < 3.0.1

%description -n %{libname}-qt
A set of Qt Widgets for Tulip/Tulip-qt

%package -n python-%{name}
Summary:	A Python binding for Tulip's library
Group:		Development/Python
Requires:       %libname = %version-%release

%description -n python-%{name}
A Python binding for Tulip's library

%package -n python-%{name}-doc
Summary:	Documentation of Python binding for Tulip's library
License:	LGPLv2
BuildArch:	noarch

%description -n python-%{name}-doc
Documentation of Python binding for Tulip's library

%package doc
Summary:	Tulip user documentation
License:	LGPLv2
BuildArch:	noarch

%description doc
This package contains Tulip user documentation in HTML

%package -n %{name}-devel-doc
Summary:	Tulip developer Handbook
License:	LGPLv2
BuildArch:	noarch
Requires:	%{name}-doc = %{version}-%{release}

%description -n %{name}-devel-doc
This package contains the Tulip developer Handbook in HTML

%prep
%setup -q -n %{name}-%{version}-src
#patch0 -p0
#patch1 -p0
%apply_patches

# defining at cmake level works but gets overwritten at make install step
sed -ri 's/UBUNTU_PPA_BUILD OFF/UBUNTU_PPA_BUILD ON/g' CMakeLists.txt

%build
# use -fpermissive to avoid:
# [ 46%] Building CXX object library/tulip-python/tulip/CMakeFiles/tulippython.dir/siptuliptlpGraph.cpp.o
# /home/alex/BuildSystem/tulip/BUILD/tulip-3.7.0-src/build/library/tulip-python/tulip/siptuliptlpGraph.cpp: In function 'PyObject* meth_tlp_Graph_setName(PyObject*, PyObject*)':
# /home/alex/BuildSystem/tulip/BUILD/tulip-3.7.0-src/build/library/tulip-python/tulip/siptuliptlpGraph.cpp:5494:32: error: passing 'const tlp::Graph' as 'this' argument of 'virtual void tlp::Graph::setName(const string&)' discards qualifiers [-fpermissive]
%cmake_qt4 -DBUILD_DOC=on -DCMAKE_CXX_FLAGS="-fpermissive"
%make

%install
%makeinstall_std -C build

%{__mv} %{buildroot}%{_datadir}/cmake-2.8 %{buildroot}%{_datadir}/cmake

%files
%defattr(-,root,root)
%{_bindir}/tulip
%{_bindir}/tulip_app
%{_bindir}/tulip_need_restart
%{_datadir}/applications/
%{_datadir}/pixmaps/
%{_datadir}/%{name}/apiFiles/
%{_datadir}/%{name}/%{name}*.qch
%{_datadir}/%{name}/%{name}*.qhc
#{_datadir}/doc/%{name}/AUTHORS
#{_datadir}/doc/%{name}/ChangeLog
#{_datadir}/doc/%{name}/INSTALL
#{_datadir}/doc/%{name}/NEWS
#{_datadir}/doc/%{name}/README

%files -n %{libname}
%{_libdir}/libgzstream-tulip*.so
%{_libdir}/libOGDF-tulip*.so
%{_libdir}/libtulip-%{api}.so
%{_libdir}/tulip/view/*.so
%{_libdir}/tulip/interactors/*.so

%files -n %{develname}
%{_includedir}/%name
%{_datadir}/cmake/Modules/
%{_datadir}/tulip/*.cmake
%{_bindir}/tulip-config
%{_bindir}/tulip_check_pl

%files -n %{libname}-ogl
%_libdir/libtulip-ogl-%{api}.so
%_libdir/tulip/glyphs

%files -n %{name}-ogl-data
%dir %_datadir/tulip/bitmaps
%_datadir/tulip/bitmaps/*

%files -n %{libname}-ogdf
%{_libdir}/libtulip-ogdf-%{api}.so
%{_libdir}/tulip/libogdf*.so

%files -n %{libname}-qt
%defattr(-,root,root)
%_libdir/libtulip-qt4-%{api}.so
%_libdir/tulip/*.so
%exclude %{_libdir}/tulip/libogdf*.so

%files -n python-%{name}
%{py_platsitedir}/

%files -n python-%{name}-doc
%{_datadir}/doc/tulip-python/

%files doc
%{_datadir}/doc/tulip/userHandbook/

%files -n %{name}-devel-doc
%{_datadir}/doc/tulip/common/
%{_datadir}/doc/tulip/doxygen/
%{_datadir}/doc/tulip/developerHandbook/


%changelog
* Mon Apr 02 2012 Alexandre Lissy <alissy@mandriva.com> 3.7.0-3
+ Revision: 788761
- Fixing installation path of python modules
- pushing release
- Putting platform-independant bitmaps in separate and platform-independant package
- Using %%{name} for python package name and not %%{libname} -> python-lib64tulip0 becomes python-tulip
- fix: rpmlint flags useless provide on python-lib64tulip0

* Mon Apr 02 2012 Alexandre Lissy <alissy@mandriva.com> 3.7.0-1
+ Revision: 788719
- Fixing remote references to XSL with local ones.
- Adding java buildrequires for documentation building
- Adding buildrequires against python-sip
- Tulip 3.7.0 building
  Using icons and desktop file provided
  Building as "Ubuntu PPA" (correct install paths)
- Updating to tulip 3.7.0
  Introducing python binding
  Splitting doc in separate package
  Building doc from sources
  Managing .desktop file as source file
  Removing useless patches
  Adding gcc 4.7 specific patch
  Adding new buildrequires to follow those changes (qt4-assistant, python-devel, python-sphinx, doxygen, docbook-style-xsl, texlive-passivetex)

* Thu Oct 28 2010 Funda Wang <fwang@mandriva.org> 3.4.1-2mdv2011.0
+ Revision: 589709
- rebuild

* Thu Sep 30 2010 Funda Wang <fwang@mandriva.org> 3.4.1-1mdv2011.0
+ Revision: 582130
- should be 3.4.1
- new version 3.4.1
- BR qt-assistant-adp

* Sat Mar 13 2010 Funda Wang <fwang@mandriva.org> 3.3.1-1mdv2010.1
+ Revision: 518688
- new version 3.3.1
- add BR

* Sat Feb 27 2010 Funda Wang <fwang@mandriva.org> 3.3.0-1mdv2010.1
+ Revision: 512269
- New version 3.3.0

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Fri Jan 23 2009 Funda Wang <fwang@mandriva.org> 3.1.1-1mdv2009.1
+ Revision: 333094
- New version 3.1.1

* Fri Dec 26 2008 Olivier Thauvin <nanardon@mandriva.org> 3.1.0-1mdv2009.1
+ Revision: 319257
- install the pdf documentation
- 3.1.0

* Fri Aug 08 2008 Thierry Vignaud <tv@mandriva.org> 3.0.1-2mdv2009.0
+ Revision: 269440
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Sat May 31 2008 Funda Wang <fwang@mandriva.org> 3.0.1-1mdv2009.0
+ Revision: 213663
- add conflicts with old packages
- move plugin manager to qt package
- clean file list
- more patches
- New version 3.0.1

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Jul 15 2007 Funda Wang <fwang@mandriva.org> 3.0.0-0.B6.1mdv2008.0
+ Revision: 52198
- fix file list
- use xdg menu
- BR qt4
- New version

