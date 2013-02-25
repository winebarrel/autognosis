Name:		autognosis-server
Version:	0.3.0
Release:	1
Summary:	autognosis-server is a server for autognosis which records the price of spot instances on memcached. 

Group:		Development/Tools
License:	BSD
URL:		https://bitbucket.org/winebarrel/autognosis
# wget https://bitbucket.org/winebarrel/autognosis/get/21957088a6de.tar.gz -O $RPM_SOURCE_DIR/
Source0:	21957088a6de.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:	noarch

Requires:	cronexec, memcached, libmemcached

%description
autognosis-server is a server for autognosis which records the price of spot instances on memcached.

%prep
%setup -q -n winebarrel-autognosis-21957088a6de

%install
rm -rf %{buildroot}
install -d -m 0755 %{buildroot}%{_sbindir}
install -d -m 0755 %{buildroot}/etc/init
install -m 0755 server/usr/sbin/autognosis-server %{buildroot}%{_sbindir}
install -m 0755 server/etc/init/autognosis-server.conf %{buildroot}/etc/init

%clean
rm -rf %{buildroot}

%post
if [ ! -e /etc/sysconfig/autognosis-server ]; then
  touch /etc/sysconfig/autognosis-server
  chmod 0600 /etc/sysconfig/autognosis-server

  cat > /etc/sysconfig/autognosis-server <<'EOF'
# AWS Credential
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=

REGION=`curl -s 169.254.169.254/latest/dynamic/instance-identity/document | awk -F'[ :"]+' '/region/{print $3}'`
START_TIME=`date -u -d "3 hours ago" +%Y-%m-%dT%H:%M:%SZ`

#CHECK_INTERVAL=5
#MEMCACHED_SERVERS=127.0.0.1
EOF
fi

if ! service memcached status > /dev/null 2> /dev/null; then
  service memcached start
fi

initctl reload-configuration
echo "Please execute 'sudo initctl start autognosis-server'"

%postun
initctl stop autognosis-server 2> /dev/null
initctl reload-configuration

%files
%defattr(-,root,root,-)
%{_sbindir}/autognosis-server
/etc/init/autognosis-server.conf
#%{_initddir}/autognosis-server
