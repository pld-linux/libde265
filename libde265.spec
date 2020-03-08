#
# Conditional build:
%bcond_without	qt		# Qt based visual inspection GUI (sherlock265)
%bcond_without	static_libs	# don't build static libraries
#
Summary:	H.265/HEVC video decoder
Summary(pl.UTF-8):	Dekoder obrazu H.265/HEVC
Name:		libde265
Version:	1.0.5
Release:	1
License:	LGPL v3+ (library), GPL v3+ (programs)
Group:		Libraries
#Source0Download: https://github.com/strukturag/libde265/releases/
Source0:	https://github.com/strukturag/libde265/releases/download/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	385c88166cb255a068a8c936d0ab23ef
URL:		http://www.libde265.org/
BuildRequires:	SDL-devel
BuildRequires:	autoconf >= 2.68
BuildRequires:	ffmpeg-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	libvideogfx-devel
BuildRequires:	pkgconfig
%if %{with qt}
BuildRequires:	Qt5Core-devel >= 5
BuildRequires:	Qt5Gui-devel >= 5
BuildRequires:	Qt5Widgets-devel >= 5
BuildRequires:	qt5-build >= 5
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libde265 is an open source implementation of the H.265 video codec. It
is written from scratch and has a plain C API to enable a simple
integration into other software.

%description -l pl.UTF-8
libde265 to mająca otwarte źródła implementacja kodeka obrazu H.265.
Została napisana od zera i ma API w czystym C, pozwalające na prostą
integrację w innym oprogramowaniu.

%package tools
Summary:	Encoding and decoding tools for libde265 library
Summary(pl.UTF-8):	Narzędzia kodujące i dekodujące dla biblioteki libde265
License:	LGPL v3+ (library), GPL v3+ (programs)
Group:		Applications/Graphics
Requires:	%{name} = %{version}-%{release}

%description tools
Encoding and decoding tools for libde265 library.

%description tools -l pl.UTF-8
Narzędzia kodujące i dekodujące dla biblioteki libde265.

%package gui
Summary:	Visual inspection tool (sherlock265) for libde265 library
Summary(pl.UTF-8):	Narzędzie do wizualnego badania (sherlock265) dla biblioteki libde265
Group:		X11/Applications/Graphics
Requires:	%{name} = %{version}-%{release}

%description gui
Visual inspection tool (sherlock265) for libde265 library.

%description gui -l pl.UTF-8
Narzędzie do wizualnego badania (sherlock265) dla biblioteki libde265.

%package devel
Summary:	Header files for libde265 library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libde265
License:	LGPL v3+
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
Header files for libde265 library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libde265.

%package static
Summary:	Static libde265 library
Summary(pl.UTF-8):	Statyczna biblioteka libde265
License:	LGPL v3+
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libde265 library.

%description static -l pl.UTF-8
Statyczna biblioteka libde265.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_qt:--disable-sherlock265} \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# examples
%{__rm} $RPM_BUILD_ROOT%{_bindir}/{bjoentegaard,block-rate-estim,gen-enc-table,hdrcopy,rd-curves,tests,yuv-distortion}

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README.md
%attr(755,root,root) %{_libdir}/libde265.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libde265.so.0

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/acceleration_speed
# R: SDL libvideogfx
%attr(755,root,root) %{_bindir}/dec265
# R: (only base)
%attr(755,root,root) %{_bindir}/enc265

%if %{with qt}
%files gui
%defattr(644,root,root,755)
%doc sherlock265/README
# R: Qt5 (Core Gui Widgets) ffmpeg/libswscale
%attr(755,root,root) %{_bindir}/sherlock265
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libde265.so
%{_includedir}/libde265
%{_pkgconfigdir}/libde265.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libde265.a
%endif
