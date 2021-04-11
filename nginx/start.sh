#!/usr/bin/env bash

COMMAND="nginx -p . -c nginx/nginx.conf"

if [[ "$(whoami)" == "ec2-user" ]]; then
  sudo $COMMAND
fi
  $COMMAND

