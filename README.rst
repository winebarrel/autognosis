autognosis
==========

Description
-----------

**autognosis** is a tool which processes when EC2 Spot Instance is terminated compulsorily.

Installation
------------
::

  local> # launch a spot instance with user-data
  local> ec2-request-spot-instances -d '{"maxPrice":0.3}' -p 0.3 -t c1.xlarge ami-4e6cd34f -k ...
  ...
  shell> sudo rpm -ihv cronexec.rpm jq.rpm describe-spot-price-history.rpm
  shell> sudo rpm autognosis

Usage
-----
::

  shell> sudo vi /etc/sysconfig/autognosis
  shell> sudo cat /etc/sysconfig/autognosis
  # AWS Credential
  AWS_ACCESS_KEY_ID=...
  AWS_SECRET_ACCESS_KEY=...
  
  # expected json: {"maxPrice":0.3}
  MAX_PRICE=`curl -s 169.254.169.254/latest/user-data | jq '.maxPrice'`
  
  #CHECK_INTERVAL=5
  
  ON_TERMINATE='echo processing when terminating'
  
  #EXECUTE_ONCE=1
  #EXEC_FLAG_FILE=/var/tmp/autognosis.executed
  shell> sudo initctl start autognosis
  ...
  # If the current price exceeds the max price...
  # shell> sudo tail /var/log/messages
  # Jan 26 14:55:15 ip-10-148-74-46 autognosis: processing when terminating

*It seems that there is a margin for about 1 minute after a price goes up before terminating...probably...*

Dependence Tools
================

* cronexec

  - http://www.netfort.gr.jp/~tosihisa/cronexec/
  - CentOS / Amazon Linux RPM: https://bitbucket.org/winebarrel/cronexec.spec/downloads

* jq

  - http://stedolan.github.com/jq
  - CentOS / Amazon Linux RPM: https://bitbucket.org/winebarrel/jq.spec/downloads

* describe-spot-price-history

  - https://bitbucket.org/winebarrel/describe-spot-price-history
  - CentOS / Amazon Linux RPM: https://bitbucket.org/winebarrel/describe-spot-price-history/downloads
