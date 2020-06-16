#!/usr/bin/expect -f
set timeout -1
#spawn ssh -i ~/.ssh/LightsailDefaultKey-ap-southeast-2.pem ubuntu@13.211.238.88
#spawn ssh -i ~/.ssh/aws-test-ec2.pem ubuntu@3.106.115.205
#spawn ssh -i ~/.ssh/aws-flexdapps-dev-default.pem ubuntu@13.211.159.53
spawn ./waitforssh.sh "-i ~/.ssh/aws-flexdapps-dev-default.pem ubuntu@54.206.66.139"

expect "ubuntu@*:"

send "ls | grep pollock\r"
expect "pollock\r"

send "sudo python3 -m pollock --ensure-swap --expected-release 4.15.0-1051-aws --expected-nodename ip-172-31-9-1\r"
expect "SWAP OKAY.\r"

send "sudo python3 -m pollock --ensure-deps --expected-release 4.15.0-1051-aws --expected-nodename ip-172-31-9-1\r"
expect "DEPS OKAY.\r"

send "python3 -m pollock --install --expected-release 4.15.0-1051-aws --expected-nodename ip-172-31-9-1\r"
expect "BUILD OKAY.\r"

# start alice node (validator)
# ./substrate-node-template/target/release/node-template --base-path /tmp/alice --chain local --alice --port 30333 --ws-port 9944 --rpc-port 9933 --telemetry-url ws://telemetry.polkadot.io:1024 --validator

send "echo worked\r"
expect "worked\r"

expect "$ "
send "exit\r"
expect eof
