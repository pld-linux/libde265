#
# Conditional build:
%bcond_without	qt		# Qt based visual inspection GUI (sherlock265)
%bcond_without	static_libs	# static library
#
Summary:	H.265/HEVC video decoder
Summary(pl.UTF-8):	Dekoder obrazu H.265/HEVC
Name:		libde265
Version:	1.0.18
Release:	1
License:	LGPL v3+ (library), MIT (programs)
Group:		Libraries
#Source0Download: https://github.com/strukturag/libde265/releases/
Source0:	https://github.com/strukturag/libde265/releases/download/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	1c14b8da1ce75ed87ede01274d4eb15d
URL:		https://www.libde265.org/
BuildRequires:	SDL2-devel >= 2
BuildRequires:	cmake >= 3.16.3
# libswscale
BuildRequires:	ffmpeg-devel
BuildRequires:	libstdc++-devel >= 6:7
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
Summary:	Decoding tool for libde265 library
Summary(pl.UTF-8):	Narzędzie dekodujące dla biblioteki libde265
License:	LGPL v3+ (library), GPL v3+ (programs)
Group:		Applications/Graphics
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description tools
Decoding tool for libde265 library.

%description tools -l pl.UTF-8
Narzędzie dekodujące dla biblioteki libde265.

%package gui
Summary:	Visual inspection tool (sherlock265) for libde265 library
Summary(pl.UTF-8):	Narzędzie do wizualnego badania (sherlock265) dla biblioteki libde265
Group:		X11/Applications/Graphics
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description gui
Visual inspection tool (sherlock265) for libde265 library.

%description gui -l pl.UTF-8
Narzędzie do wizualnego badania (sherlock265) dla biblioteki libde265.

%package devel
Summary:	Header files for libde265 library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libde265
License:	LGPL v3+
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	libstdc++-devel%{?_isa}

%description devel
Header files for libde265 library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libde265.

%package static
Summary:	Static libde265 library
Summary(pl.UTF-8):	Statyczna biblioteka libde265
License:	LGPL v3+
Group:		Development/Libraries
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description static
Static libde265 library.

%description static -l pl.UTF-8
Statyczna biblioteka libde265.

%prep
%setup -q

%build
%if %{with static_libs}
%cmake -B build-static \
	-DBUILD_SHARED_LIBS=OFF

%{__make} -C build-static
%endif

%cmake -B build \
	%{?with_qt:-DENABLE_SHERLOCK265=ON} \

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} -C build-static install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README.md
%{_libdir}/libde265.so.*.*.*
%ghost %{_libdir}/libde265.so.0

%files tools
%defattr(644,root,root,755)
%doc dec265/COPYING
# R: SDL libvideogfx
%attr(755,root,root) %{_bindir}/dec265

%if %{with qt}
%files gui
%defattr(644,root,root,755)
%doc sherlock265/{COPYING,README}
# R: Qt5 (Core Gui Widgets) ffmpeg/libswscale
%attr(755,root,root) %{_bindir}/sherlock265
%endif

%files devel
%defattr(644,root,root,755)
%{_libdir}/libde265.so
%{_includedir}/libde265
%{_pkgconfigdir}/libde265.pc
%{_libdir}/cmake/libde265

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libde265.a
%endif
