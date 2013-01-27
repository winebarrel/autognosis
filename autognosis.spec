Name:		autognosis
Version:	0.1.3
Release:	1%{?dist}
Summary:	autognosis is a tool which processes when a spot instance is terminated compulsorily.

Group:		Development/Tools
License:	BSD
URL:		https://bitbucket.org/winebarrel/autognosis
# wget https://bitbucket.org/winebarrel/autognosis/get/01ab6b766745.tar.gz -O $RPM_SOURCE_DIR/autognosis.tar.gz
Source0:	autognosis.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:	noarch

Requires:  ruby, cronexec, jq, describe-spot-price-history, wget

%description
autognosis is a tool which processes when a spot instance is terminated compulsorily.

%prep
%setup -q -n winebarrel-autognosis-01ab6b766745

%install
rm -rf %{buildroot}
install -d -m 0755 %{buildroot}%{_sbindir}
install -d -m 0755 %{buildroot}/etc/init
install -m 0755 usr/sbin/autognosis %{buildroot}%{_sbindir}
install -m 0755 etc/init/autognosis.conf %{buildroot}/etc/init
#install -d -m 0755 %{buildroot}%{_initddir}
#install -m 0755 etc/init.d/autognosis %{buildroot}%{_initddir}

%clean
rm -rf %{buildroot}

%post
/sbin/initctl reload-configuration
#chkconfig --add autognosis

if [ ! -e /etc/sysconfig/autognosis ]; then
  touch /etc/sysconfig/autognosis
  chmod 0600 /etc/sysconfig/autognosis

  cat > /etc/sysconfig/autognosis <<'EOF'
# AWS Credential
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=

# expected json: {"maxPrice":0.3}
#MAX_PRICE=`curl -s 169.254.169.254/latest/user-data | jq '.maxPrice'`

#CHECK_INTERVAL=5

ON_TERMINATE='echo processing when terminating'
EOF
fi

%postun
/sbin/initctl reload-configuration
#chkconfig --del autognosis

%files
%defattr(-,root,root,-)
%{_sbindir}/autognosis
/etc/init/autognosis.conf
#%{_initddir}/autognosis
