Name:		autognosis
Version:	0.3.0
Release:	2
Summary:	autognosis is a tool which processes when a spot instance is terminated compulsorily.

Group:		Development/Tools
License:	BSD
URL:		https://bitbucket.org/winebarrel/autognosis
# wget https://bitbucket.org/winebarrel/autognosis/get/bc0b8c24ad67.tar.gz -O $RPM_SOURCE_DIR/
Source0:	bc0b8c24ad67.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:	noarch

#Requires:	cronexec, jq, curl, bc, libmemcached, describe-spot-price-history
Requires:	cronexec, jq, curl, bc, libmemcached

%description
autognosis is a tool which processes when a spot instance is terminated compulsorily.

%prep
%setup -q -n winebarrel-autognosis-bc0b8c24ad67

%install
rm -rf %{buildroot}
install -d -m 0755 %{buildroot}%{_sbindir}
install -d -m 0755 %{buildroot}/etc/init
install -m 0755 client/usr/sbin/autognosis %{buildroot}%{_sbindir}
install -m 0755 client/etc/init/autognosis.conf %{buildroot}/etc/init

%clean
rm -rf %{buildroot}

%post
if [ ! -e /etc/sysconfig/autognosis ]; then
  touch /etc/sysconfig/autognosis
  chmod 0600 /etc/sysconfig/autognosis

  cat > /etc/sysconfig/autognosis <<'EOF'
MAX_PRICE=`curl -s 169.254.169.254/latest/user-data | jq -r .maxPrice`
# expected json: {"maxPrice":0.3}

ON_TERMINATE='echo processing when terminating'

#EXECUTE_ONCE=1
#EXEC_FLAG_FILE=/var/tmp/autognosis.executed

INSTANCE_TYPE=`curl -s 169.254.169.254/latest/dynamic/instance-identity/document | jq -r .instanceType`
AVAILABILITY_ZONE=`curl -s 169.254.169.254/latest/dynamic/instance-identity/document | jq -r .availabilityZone`

PRODUCT_DESCRIPTION=
# (ProductDescription)
# Linux/UNIX
# Linux/UNIX (Amazon VPC)
# SUSE Linux
# SUSE Linux (Amazon VPC)
# Windows
# Windows (Amazon VPC)

#CHECK_INTERVAL=5
#MEMCACHED_SERVERS=127.0.0.1
EOF
fi

initctl reload-configuration
echo "Please execute 'sudo initctl start autognosis'"

%postun
initctl stop autognosis 2> /dev/null
rm -f /var/tmp/autognosis.executed
initctl reload-configuration

%files
%defattr(-,root,root,-)
%{_sbindir}/autognosis
/etc/init/autognosis.conf
