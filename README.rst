autognosis
==========

Description
-----------

autognosis is a tool which processes when EC2 Spot Instance is terminated compulsorily.

Server Installation
-------------------
::

  shell> sudo rpm -ihv cronexec.rpm describe-spot-price-history.rpm
  shell> sudo yum install memcached libmemcached
  shell> sudo rpm -ihv autognosis-server-X.X.X-X.rpm
  
  shell> sudo vi /etc/sysconfig/autognosis-server
  # (define environments...)
  #AWS_ACCESS_KEY_ID=...
  #AWS_SECRET_ACCESS_KEY=...
  
  shell> sudo initctl start autognosis-server
  shell> memdump -s 127.0.0.1 # check of starting of a server

Client Installation
-------------------
::

  local> # launch a spot instance with user-data
  local> ec2-request-spot-instances -d '{"maxPrice":0.3}' -p 0.3 -t c1.xlarge ami-4e6cd34f -k ...
  ...
  shell> sudo rpm -ihv cronexec.rpm
  shell> sudo yum install curl memcached libmemcached
  shell> sudo rpm -ihv autognosis-X.X.X-X.rpm
  
  shell> sudo vi /etc/sysconfig/autognosis
  # (define environments...)
  #MAX_PRICE=...
  #ON_TERMINATE=...
  #PRODUCT_DESCRIPTION=...
  
  shell> sudo initctl start autognosis
  ...
  # If the current price exceeds the max price...
  # shell> sudo tail /var/log/messages
  # Jan 26 14:55:15 ip-10-148-74-46 autognosis: processing when terminating

*It seems that there is a margin for about 1 minute after a price goes up before terminating...probably...*

Dependence Tools
----------------

* cronexec

  - http://www.netfort.gr.jp/~tosihisa/cronexec/
  - CentOS / Amazon Linux RPM: https://bitbucket.org/winebarrel/cronexec.spec/downloads

* jq

  - http://stedolan.github.com/jq
  - CentOS / Amazon Linux RPM: https://bitbucket.org/winebarrel/jq.spec/downloads

* describe-spot-price-history

  - https://bitbucket.org/winebarrel/describe-spot-price-history
  - CentOS / Amazon Linux RPM: https://bitbucket.org/winebarrel/describe-spot-price-history/downloads
