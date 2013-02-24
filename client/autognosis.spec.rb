#!/usr/bin/env ruby
require 'erb'

mercurial_hash = 'f4385c4f378c'
spec_path = File.join(File.expand_path(File.dirname(__FILE__)), 'autognosis.spec')
conf_path = File.join(File.expand_path(File.dirname(__FILE__)), 'etc/sysconfig/autognosis')

open(spec_path, 'wb') do |spec|
  spec.puts(ERB.new(DATA.read).result(binding))
end

__END__
Name:		autognosis
Version:	0.3.0
Release:	1
Summary:	autognosis is a tool which processes when a spot instance is terminated compulsorily.

Group:		Development/Tools
License:	BSD
URL:		https://bitbucket.org/winebarrel/autognosis
# wget https://bitbucket.org/winebarrel/autognosis/get/<%= mercurial_hash %>.tar.gz -O $RPM_SOURCE_DIR/
Source0:	<%= mercurial_hash %>.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:	noarch

#Requires:	cronexec, jq, curl, bc, libmemcached, describe-spot-price-history
Requires:	cronexec, jq, curl, bc, libmemcached

%description
autognosis is a tool which processes when a spot instance is terminated compulsorily.

%prep
%setup -q -n winebarrel-autognosis-<%= mercurial_hash %>

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
<%= open(conf_path) {|f| f.read }.strip %>
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
