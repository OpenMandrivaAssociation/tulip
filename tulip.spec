%define name	tulip
%define version	3.0.1
%define release %mkrel 1
%define major	0
%define api 3.0
%define libname	%mklibname %name %major
%define develname %mklibname -d %name

Summary:	A program that allows visualization of huge graphs
Name:		%{name}
Version:	%{version}
Release:	%{release}
URL:		http://www.tulip-software.org
Source:		%{name}-%{version}.tar.bz2
Source10:	%name-16.png
Source11:	%name-32.png
Source12:	%name-48.png
Patch0:     tulip-2.0.5-fix.patch
Patch1:		tulip-3.0.1-gcc4.3-includes.patch
License:	GPLv2+
Group:		Graphics
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildRequires:	qt4-devel
BuildRequires:	libmesaglut-devel glew-devel
BuildRequires:	xmltex doxygen graphviz libxml2-utils
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
Obsoletes:	%{libname}-devel

%description -n %{develname}
A library for handling large graphs.
You need this package if you plan to build apps using
tulip libraries.

%package -n     %{libname}-ogl
Summary:        A library for displaying graph in a GL context
Group:		    Graphics
Requires:       %{libname} = %version-%release
Provides:       %name-qt = %version-%release
Provides:       lib%name-ogl = %version-%release

%description -n %{libname}-ogl
A library for displaying graph in a GL context

%package -n     %{libname}-qt
Summary:        A set of Qt Widgets for Tulip/Tulip-qt
Group:          Graphics
Requires:       %libname = %version-%release
Provides:       %name-qt = %version-%release
Provides:       lib%name-qt = %version-%release
Conflicts:	%{develname} < 3.0.1

%description -n %{libname}-qt
A set of Qt Widgets for Tulip/Tulip-qt

%prep
%setup -q -n %{name}-%{version}
#%patch -p0 -b .fix
%patch1 -p1

%build
%configure2_5x \
    --with-qt-dir=%qt4dir \
    --with-qt-includes=%qt4include \
    --with-qt-libraries=%qt4lib \
    --with-gl-libraries=%_libdir
%make

%install
rm -fr %buildroot
%makeinstall_std

mkdir -p %buildroot{%{_miconsdir},%{_iconsdir},%{_liconsdir}}

cp %SOURCE10 %{buildroot}%{_miconsdir}/%name.png
cp %SOURCE11 %{buildroot}%{_iconsdir}/%name.png
cp %SOURCE12 %{buildroot}%{_liconsdir}/%name.png

mkdir -p %buildroot%{_datadir}/applications
cat > %buildroot%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Tulip
Comment=A 3D graph program
Exec=tulip
Icon=tulip
Type=Application
Categories=Qt;Graphics;3DGraphics;
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{update_menus}

%postun
%{clean_menus}

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%post -n %{libname}-ogl -p /sbin/ldconfig
%postun -n %{libname}-ogl -p /sbin/ldconfig

%post -n %{libname}-qt -p /sbin/ldconfig
%postun -n %{libname}-qt -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog INSTALL NEWS README
%_bindir/tulip
%_datadir/tulip
%{_datadir}/applications/mandriva-%{name}.desktop
%{_miconsdir}/%name.png
%{_iconsdir}/%name.png
%{_liconsdir}/%name.png

%files -n %{libname}
%defattr(-,root,root)
%_libdir/libtulip-%{api}.so
%dir %_libdir/tlp
%{_datadir}/aclocal/tulip.m4

%files -n %{develname}
%defattr(-,root,root)
%_includedir/%name
%_bindir/tulip-config
%_bindir/tulip_check_pl
%_libdir/*.la
%_libdir/libtulip.so
%_libdir/libtulip-qt4.so
%_libdir/libtulip-ogl.so
%_libdir/libtulip-pluginsmanager.so
%_libdir/tlp/*.la
%_libdir/tlp/designer/*.la

%files -n %{libname}-ogl
%defattr(-,root,root)
%_libdir/libtulip-ogl-%{api}.so
%_libdir/tlp/glyphs
%dir %_libdir/tlp/bitmaps
%_libdir/tlp/bitmaps/*

%files -n %{libname}-qt
%defattr(-,root,root)
%_libdir/libtulip-qt4-%{api}.so
%_libdir/libtulip-pluginsmanager-%{api}.so
%_libdir/tlp/*.so
%_libdir/tlp/designer/*.so
