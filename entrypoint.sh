#!/bin/sh -e

isMounted    () { findmnt -rno SOURCE,TARGET "$1" >/dev/null;} # path or device
isDevMounted () { findmnt -rno SOURCE        "$1" >/dev/null;} # device only
isPathMounted() { findmnt -rno        TARGET "$1" >/dev/null;} # path only

# Ensure that the data directory is a docker volume
if ! isPathMounted "$DATA_LOCATION"; then
  echo "The $DATA_LOCATION directory is required to be a mounted docker volume."
  echo "Please add the following to your docker command."
  echo "--volume='calllogger-data:$DATA_LOCATION'"
  exit 0
fi

# Ensure that the docker container is in network host mode
if [ ! -d "/sys/class/net/docker0" ]; then
  echo "Looks like the docker network mode was not set to host."
  echo "Please add the following to your docker command."
  echo "--network host"
  exit 0
fi

case $1 in
  mock)
    exec calllogger-mock
  ;;
  getid)
    exec calllogger-getid
  ;;
  calllogger)
    # Set the plugin to use if one
    # is given using cli parameters
    if [ -n "$2" ]; then
      export PLUGIN="$2"
    fi
    exec calllogger
  ;;
  *)
    exec "$@"
  ;;
esac

exit 0
