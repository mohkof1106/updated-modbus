#!/bin/bash
createTunnel() {
  /usr/bin/ssh -N -R 12345:localhost:22 pi1@enerwhere.com
  if [[ $? -eq 0 ]]; then
    echo Tunnel to enerwhere.com created successfully
  else
    echo An error occurred creating a tunnel to enerwhere.com. RC was $?
  fi
}
/bin/pidof ssh
if [[ $? -ne 0 ]]; then
  echo Creating new tunnel connection
  createTunnel
fi

# from instructions from:
# http://www.tunnelsup.com/raspberry-pi-phoning-home-using-a-reverse-remote-ssh-tunnel
