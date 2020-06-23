#============================================================
# determine OS type
{% if grains['os'] == 'CentOS' %}
{% set apache = 'apache' %}
{% set webserver = 'httpd' %}
{% elif grains['os'] == 'Ubuntu' %}
{% set apache = 'www-data' %}
{% set webserver = 'apache2' %}
{% endif %}

include:
  - .webserverpackages
  - .webserverdirs
  - .webservercrontasks

git:
  pkg.installed

# Node Package Manager
npm:
  pkg.installed

# Grunt - JS build system 
grunt-cli:
  npm:
    - installed
    - require:
      - pkg: npm    
#
# Make Directory
#
/opt/graphite/webapp/grafana:
  file.directory:
    - user: {{ apache }}
    - group: {{ apache }}
    - mode: 775
    - makedirs: true
#
# Download to /tmp
#
https://github.com/grafana/grafana.git:
  git.latest:
    - rev: master
    - target: /tmp/grafana
#
# cleanup old code if present
#
rm -rf /opt/graphite/webapp/grafana/*:
  cmd.run
#
# Use grunt to compile the CSS etc
#
cmd.run:
  - name: grunt
  - cwd: /tmp/grafana
  - watch:
     - git: https://github.com/grafana/grafana.git
#
# place it where we want it to run from
#
cp -R /tmp/grafana/src/* /opt/graphite/webapp/grafana/:
  cmd.run
#
# Custom JS file for production use
#
/opt/graphite/webapp/grafana/config.js:
  file.managed:
    - source: salt://cnx_servers/grafana/config.js
#
# Setup perms for the right web server and restart services for the OS type
#
chown -R {{ apache }}:{{ apache }} /opt/graphite/webapp/grafana/:
  cmd.run 

{% if grains['os'] == 'CentOS' %}

/etc/httpd/conf.d/grafana.conf:
  file.managed:
    - source: salt://cnx_servers/grafana/grafana.conf
service httpd restart:
  cmd.run

{% elif grains['os'] == 'Ubuntu' %}

/etc/init.d/apache2 restart:
  cmd.run

{% endif %}
