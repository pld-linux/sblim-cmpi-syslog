# TODO: syslog-ng support; runtime syslog daemon selection?
# PLDify syslog-service.sh
#
# Conditional build:
%bcond_with	rsyslog	# support rsyslog instead of plain syslog
#
Summary:	SBLIM CMPI Syslog providers
Summary(pl.UTF-8):	Dostawcy danych Syslog dla SBLIM CMPI
Name:		sblim-cmpi-syslog
Version:	0.9.0
Release:	0.1
License:	Eclipse Public License v1.0
Group:		Libraries
Source0:	http://downloads.sourceforge.net/sblim/%{name}-%{version}.tar.bz2
# Source0-md5:	e5edc37a3fd55946f2a43305886d8027
Patch0:		%{name}-link.patch
URL:		http://sblim.sourceforge.net/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	sblim-cmpi-base-devel >= 1.5.4
BuildRequires:	sblim-cmpi-devel
BuildRequires:	sblim-indication_helper-devel
Requires:	sblim-cmpi-base >= 1.5.4
Requires:	sblim-sfcb
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# circular dependencies
%define		skip_post_check_so	libsyslogconfutil.so.* libsyslogsettingparse.so.*

%description
SBLIM CMPI Syslog providers.

%description -l pl.UTF-8
Dostawcy danych Syslog dla SBLIM CMPI.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	CIMSERVER=sfcb \
	PROVIDERDIR=%{_libdir}/cmpi \
	%{?with_rsyslog:SYSLOG=rsyslog} \
	--disable-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

# modules
%{__rm} $RPM_BUILD_ROOT%{_libdir}/cmpi/lib*.la
# API not exported
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.{la,so}
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%{_datadir}/%{name}/provider-register.sh \
	-r %{_datadir}/%{name}/{Syslog_Configuration,Syslog_Log,Syslog_Service}.registration \
	-m %{_datadir}/%{name}/{Syslog_Configuration,Syslog_Log,Syslog_Service}.mof >/dev/null

%preun
if [ "$1" = "0" ]; then
	%{_datadir}/%{name}/provider-register.sh -d \
		-r %{_datadir}/%{name}/{Syslog_Configuration,Syslog_Log,Syslog_Service}.registration \
		-m %{_datadir}/%{name}/{Syslog_Configuration,Syslog_Log,Syslog_Service}.mof >/dev/null
fi

%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/syslog-service.sh
%attr(755,root,root) %{_libdir}/libSyslog_ConfUtils.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libSyslog_ConfUtils.so.0
%attr(755,root,root) %{_libdir}/libSyslog_LogUtils.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libSyslog_LogUtils.so.0
%attr(755,root,root) %{_libdir}/libSyslog_ServiceUtils.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libSyslog_ServiceUtils.so.0
%attr(755,root,root) %{_libdir}/libsyslogconfutil.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsyslogconfutil.so.0
%attr(755,root,root) %{_libdir}/libsysloglogutil.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsysloglogutil.so.0
%attr(755,root,root) %{_libdir}/libsyslogserviceutil.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsyslogserviceutil.so.0
%attr(755,root,root) %{_libdir}/libsyslogsettingparse.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsyslogsettingparse.so.0
%attr(755,root,root) %{_libdir}/libsyslogtimeparse.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsyslogtimeparse.so.0
%attr(755,root,root) %{_libdir}/cmpi/libSyslog_Configuration.so
%attr(755,root,root) %{_libdir}/cmpi/libSyslog_LogRecord.so
%attr(755,root,root) %{_libdir}/cmpi/libSyslog_MessageLog.so
%attr(755,root,root) %{_libdir}/cmpi/libSyslog_RecordInLog.so
%attr(755,root,root) %{_libdir}/cmpi/libSyslog_Service.so
%attr(755,root,root) %{_libdir}/cmpi/libSyslog_ServiceProcess.so
%attr(755,root,root) %{_libdir}/cmpi/libSyslog_Setting.so
%attr(755,root,root) %{_libdir}/cmpi/libSyslog_SettingContext.so
%dir %{_datadir}/sblim-cmpi-syslog
%{_datadir}/sblim-cmpi-syslog/Syslog_Configuration.mof
%{_datadir}/sblim-cmpi-syslog/Syslog_Configuration.registration
%{_datadir}/sblim-cmpi-syslog/Syslog_Log.mof
%{_datadir}/sblim-cmpi-syslog/Syslog_Log.registration
%{_datadir}/sblim-cmpi-syslog/Syslog_Service.mof
%{_datadir}/sblim-cmpi-syslog/Syslog_Service.registration
%attr(755,root,root) %{_datadir}/sblim-cmpi-syslog/provider-register.sh
