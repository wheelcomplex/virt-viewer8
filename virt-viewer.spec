# -*- rpm-spec -*-

# Default to skipping autoreconf.  Distros can change just this one line
# (or provide a command-line override) if they backport any patches that
# touch configure.ac or Makefile.am.
%{!?enable_autotools:%global enable_autotools 0}

%define with_spice 0
%if 0%{?fedora} >= 17 || 0%{?rhel} >= 6
%define with_spice 1
%endif

%define with_govirt 0
%if 0%{?fedora} > 19 || 0%{?rhel} >= 7
%define with_govirt 1
%endif

Name: virt-viewer
Version: 8.0
Release: 1%{?dist}
Summary: Virtual Machine Viewer
Group: Applications/System
License: GPLv2+
URL: http://virt-manager.org/
Source0: http://virt-manager.org/download/sources/%{name}/%{name}-%{version}.tar.gz
Requires: openssh-clients
Requires(post):   %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

%if 0%{?enable_autotools}
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gettext-devel
BuildRequires: libtool
%endif

BuildRequires: gcc
BuildRequires: pkgconfig(glib-2.0) >= 2.40
BuildRequires: pkgconfig(gtk+-3.0) >= 3.12
BuildRequires: pkgconfig(libvirt) >= 0.10.0
BuildRequires: pkgconfig(libvirt-glib-1.0) >= 0.1.8
BuildRequires: pkgconfig(libxml-2.0) >= 2.6.0
BuildRequires: pkgconfig(gtk-vnc-2.0) >= 0.4.0
%if %{with_spice}
BuildRequires: pkgconfig(spice-client-gtk-3.0) >= 0.35
BuildRequires: pkgconfig(spice-protocol) >= 0.12.7
%endif
BuildRequires: /usr/bin/pod2man
BuildRequires: intltool
%if %{with_govirt}
BuildRequires: pkgconfig(govirt-1.0) >= 0.3.3
%endif

%if 0%{?fedora} >= 20
Obsoletes: spice-client < 0.12.3-2
%endif


%description
Virtual Machine Viewer provides a graphical console client for connecting
to virtual machines. It uses the GTK-VNC or SPICE-GTK widgets to provide
the display, and libvirt for looking up VNC/SPICE server details.

%prep
%setup -q

%build

%if 0%{?enable_autotools}
autoreconf -if
%endif

%if %{with_spice}
%define spice_arg --with-spice-gtk
%else
%define spice_arg --without-spice-gtk
%endif

%if %{with_govirt}
%define govirt_arg --with-ovirt
%endif

%configure %{spice_arg} %{govirt_arg} --with-buildid=%{release} --disable-update-mimedb
%__make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%__make install  DESTDIR=$RPM_BUILD_ROOT
%find_lang %{name}


%files -f %{name}.lang
%doc README.md COPYING AUTHORS ChangeLog NEWS
%{_bindir}/%{name}
%{_bindir}/remote-viewer
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/icons/hicolor/*/devices/*
%{_datadir}/applications/remote-viewer.desktop
%{_datadir}/appdata/remote-viewer.appdata.xml
%{_datadir}/mime/packages/virt-viewer-mime.xml
%{_mandir}/man1/virt-viewer.1*
%{_mandir}/man1/remote-viewer.1*

%changelog
