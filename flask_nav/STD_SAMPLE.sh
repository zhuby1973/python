#!/bin/bash
cat /tmp/adpass.txt |sudo -S su - pm2 >/dev/null 2>&1
sudo su - pm2
