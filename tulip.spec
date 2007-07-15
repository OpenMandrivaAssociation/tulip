%define name	tulip
%define version	3.0.0
%define betaver B6
%define release %mkrel -c %betaver
%define major	0
%define libname	%mklibname %name %major

Summary:	A program that allows visualization of huge graphs
Name:		%{name}
Version:	%{version}
Release:	%{release}
URL:		http://www.tulip-software.org
Source:		%{name}-%{version}%{betaver}.tar.bz2
Source10:	%name-16.png
Source11:	%name-32.png
Source12:	%name-48.png
Patch0:     tulip-2.0.5-fix.patch
License:	GPL
Group:		Graphics
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildRequires:	qt3-devel
BuildRequires:	libmesaglut-devel
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

%package -n     %{libname}-devel
Summary:        A library for handling large graphs
Group:          Development/Other
Requires:       %libname = %version-%release
Requires:       %{libname}-qt = %version-%release
Requires:       %{libname}-ogl = %version-%release

%description -n %{libname}-devel
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

%description -n %{libname}-qt
A set of Qt Widgets for Tulip/Tulip-qt

%prep
%setup -q -n %{name}-%{version}%{betaver}
#%patch -p0 -b .fix

%build
CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS"\
    ./configure \
    --prefix=%{_prefix} \
    --libdir=%_libdir \
    --with-qt-dir=%qt3dir \
    --with-qt-includes=%qt3include \
    --with-qt-libraries=%qt3lib \
    --with-gl-libraries=%_libdir

make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
%makeinstall_std

mkdir -p %buildroot{%{_menudir},%{_miconsdir},%{_iconsdir},%{_liconsdir}}

cp %SOURCE10 %{buildroot}%{_miconsdir}/%name.png
cp %SOURCE11 %{buildroot}%{_iconsdir}/%name.png
cp %SOURCE12 %{buildroot}%{_liconsdir}/%name.png

cat > %{buildroot}%{_menudir}/%{name} <<EOF
?package(%{name}):\
    command="%{_bindir}/tulip"\
    title="Tulip"\
    longtitle="A 3D graph program"\
    needs="x11"\
    section="Office/Graphs"\
    icon="%{name}.png"\
    xdg="true"
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
%dir %_libdir/tlp
%_libdir/tlp/bitmaps/logo32x32.bmp
%_menudir/%name
%{_miconsdir}/%name.png
%{_iconsdir}/%name.png
%{_liconsdir}/%name.png

%files -n %{libname}
%defattr(-,root,root)
%_libdir/libtulip-2.0.so.*
%dir %_libdir/tlp
%dir %_libdir/tlp/plugins
%_libdir/tlp/plugins/clustering
%_libdir/tlp/plugins/colors
%_libdir/tlp/plugins/export
%_libdir/tlp/plugins/import
%_libdir/tlp/plugins/layout
%_libdir/tlp/plugins/metric
%_libdir/tlp/plugins/selection
%_libdir/tlp/plugins/sizes
%_libdir/tlp/plugins/string
%{_datadir}/aclocal/tulip.m4

%files -n %{libname}-devel
%defattr(-,root,root)
%_bindir/tulip-config
%_libdir/libtulip.la
%_libdir/libtulip.a
%_libdir/libtulip.so
%_libdir/libtulip-ogl.la
%_libdir/libtulip-ogl.a
%_libdir/libtulip-ogl.so
%_libdir/libtulip-qt3.la
%_libdir/libtulip-qt3.a
%_libdir/libtulip-qt3.so
%_includedir/%name

%files -n %{libname}-ogl
%defattr(-,root,root)
%_libdir/libtulip-ogl-2.0.so.*
%_libdir/tlp/plugins/glyph
%dir %_libdir/tlp/bitmaps
%_libdir/tlp/bitmaps/*

%files -n %{libname}-qt
%defattr(-,root,root)
%_libdir/libtulip-qt3-2.0.so.*
%_libdir/tlp/plugins/designer

