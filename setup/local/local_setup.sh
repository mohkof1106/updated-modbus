echo "Setting up tunnel"


echo "create tunnel file"
echo "#!/bin/bash
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
" > ~/create_ssh_tunnel.sh
chmod u+x ~/create_ssh_tunnel.sh

echo "ssh configuration"
sudo mv ssh_config /etc/ssh/ssh_config
sudo mv sshd_config /etc/ssh/sshd_config

echo "set up crontab"
crontab crontab.txt
