Name:		autognosis
Version:	0.2.0
Release:	1
Summary:	autognosis is a tool which processes when a spot instance is terminated compulsorily.

Group:		Development/Tools
License:	BSD
URL:		https://bitbucket.org/winebarrel/autognosis
# wget https://bitbucket.org/winebarrel/autognosis/get/4e2381c892d0.tar.gz -O $RPM_SOURCE_DIR/autognosis.tar.gz
Source0:	autognosis.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:	noarch

#Requires:	cronexec, jq, describe-spot-price-history, wget, bc, libmemcached
Requires:	cronexec, jq, wget, bc, libmemcached

%description
autognosis is a tool which processes when a spot instance is terminated compulsorily.

%prep
%setup -q -n winebarrel-autognosis-80249df5a7c8

%install
rm -rf %{buildroot}
install -d -m 0755 %{buildroot}%{_sbindir}
install -d -m 0755 %{buildroot}/etc/init
install -m 0755 client/usr/sbin/autognosis %{buildroot}%{_sbindir}
install -m 0755 client/etc/init/autognosis.conf %{buildroot}/etc/init
#install -d -m 0755 %{buildroot}%{_initddir}
#install -m 0755 client/etc/init.d/autognosis %{buildroot}%{_initddir}

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

#EXECUTE_ONCE=1
#EXEC_FLAG_FILE=/var/tmp/autognosis.executed

#    INSTANCE_TYPE=`wget -q -O- http://169.254.169.254/latest/dynamic/instance-identity/document | jq -r .instanceType`
#AVAILABILITY_ZONE=`wget -q -O- http://169.254.169.254/latest/dynamic/instance-identity/document | jq -r .availabilityZone`
#           REGION=`wget -q -O- http://169.254.169.254/latest/dynamic/instance-identity/document | jq -r .region`

#CURRENT_PRICE_SCRIPT='describe-spot-price-history -k "$AWS_ACCESS_KEY_ID" -s "$AWS_SECRET_ACCESS_KEY" -r "$REGION" -t "$INSTANCE_TYPE" -d Linux/UNIX -z "$AVAILABILITY_ZONE" --start-time "$PENDING_TIME" --sort time --attrs price --tail 1 --tsv'

# --- autognosys client configuration ---
#    INSTANCE_TYPE=0
#AVAILABILITY_ZONE=0
#           REGION=0
#CURRENT_PRICE_SCRIPT=`memcat -s <server> current_price`
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
