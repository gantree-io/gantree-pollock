# Steps needed

Install curl

```bash
sudo apt install curl -y
```

Install rust prerequisites (WARNING: ISN'T WORKING ON DEBIAN WHEN TRIED. UBUNTU WORKS OKAY.)

```bash
curl https://getsubstrate.io -sSf | bash -s -- --fast
```

Download the Substrate node template

```bash
git clone https://github.com/substrate-developer-hub/substrate-node-template.git
```

Re-open terminal or reboot (reboot used)

Ensure your Rust toolchain is up to date

```bash
cd substrate-node-template
./scripts/init.sh
```

Compile the node-template (takes ages)

```bash
cargo build --release
```

Start first node (arguments will very likely need to change)

```bash
./target/release/node-template \
  --base-path /tmp/alice \
  --chain local \
  --alice \
  --port 30333 \
  --ws-port 9944 \
  --rpc-port 9933 \
  --telemetry-url ws://telemetry.polkadot.io:1024 \
  --validator
```

Install subkey

```bash
cargo install --force subkey --git https://github.com/paritytech/substrate
```

-------------------------
<!-- 
install ansible

```bash
sudo apt-add-repository -y ppa:ansible/ansible
sudo apt update
sudo apt install -y ansible
```

install ssh

```bash
sudo apt update
sudo apt install openssh-server -y
```

- (check it's running with `sudo systemctl status ssh`)

- allow port though firewall (Ubuntu related)

```bash
sudo ufw allow ssh
```

- add fingerprint to known hosts -->
