Name:       connectionagent-qt5

# >> macros
# << macros

Summary:    User Agent daemon
Version:    0.11.11.1
Release:    0
Group:      Communications/Connectivity Adaptation
License:    LGPLv2
URL:        http://github.com/lpotter/connectionagent
Source0:    %{name}-%{version}.tar.bz2
Source1:    connectionagent.tracing
Requires:   connman-qt5-declarative
Requires:   systemd
Requires:   systemd-user-session-targets
Requires: connman >= 1.21
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5DBus)
BuildRequires:  pkgconfig(connman-qt5)
BuildRequires:  pkgconfig(qofono-qt5)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5Test)
BuildRequires:  pkgconfig(Qt5Qml)
Provides:   connectionagent > 0.10.1
Obsoletes:   connectionagent <= 0.7.6

%description
Connection Agent provides multi user access to connman's User Agent.
It also provides autoconnecting features.


%package declarative
Summary:    Declarative plugin for connection agent.
Group:      Development/Tools
Requires:   %{name} = %{version}-%{release}
Requires:   %{name} = %{version}

%description declarative
This package contains the declarative plugin for connection agent.

%package test
Summary:    auto test for connection agent.
Group:      Development/Tools
Requires:   %{name} = %{version}-%{release}
Requires:   %{name} = %{version}

%description test
This package contains the auto tests for connection agent.

%package tracing
Summary:    Configuration for Connectionagent to enable tracing
Group:      Development/Tools
Requires:   %{name} = %{version}-%{release}

%description tracing
Will enable tracing for Connectionagent


%prep
%setup -q -n %{name}-%{version}

# >> setup
# << setup

%build
# >> build pre
# << build pre

%{!?qtc_qmake5:%define qtc_qmake5 %qmake5}
%{!?qtc_make:%define qtc_make make}

%qtc_qmake5
%qtc_make %{?_smp_mflags}

# >> build post
# << build post

%install
rm -rf %{buildroot}
# >> install pre
# << install pre
%qmake5_install

%make_install
mkdir -p %{buildroot}%{_sysconfdir}/tracing/connectionagent/
cp -a %{SOURCE1} %{buildroot}%{_sysconfdir}/tracing/connectionagent/

# >> install post
mkdir -p %{buildroot}%{_libdir}/systemd/user/user-session.target.wants
ln -s ../connectionagent.service %{buildroot}%{_libdir}/systemd/user/user-session.target.wants/
# << install post

%post
# >> post
if [ "$1" -ge 1 ]; then
systemctl-user daemon-reload || :
systemctl-user restart connectionagent.service || :
fi
# << post

%postun
# >> postun
if [ "$1" -eq 0 ]; then
systemctl-user stop connectionagent.service || :
systemctl-user daemon-reload || :
fi
# << postun

%files
%defattr(-,root,root,-)
%{_bindir}/connectionagent
%{_datadir}/dbus-1/services/com.jolla.Connectiond.service
%{_libdir}/systemd/user/connectionagent.service
%{_sysconfdir}/dbus-1/session.d/connectionagent.conf
# >> files
%{_libdir}/systemd/user/user-session.target.wants/connectionagent.service
# << files

%files declarative
%defattr(-,root,root,-)
%{_libdir}/qt5/qml/com/jolla/connection/*
# >> files declarative
# << files declarative

%files test
%defattr(-,root,root,-)
%{_prefix}/opt/tests/libqofono/*
# >> files test
# << files test

%files tracing
%defattr(-,root,root,-)
%config %{_sysconfdir}/tracing/connectionagent
# >> files tracing
# << files tracing

