init:
	echo "hello there."

upload_test:
	# rsync pollock/ ubuntu@13.211.238.88:/home/ubuntu/pollock/ -r -e "ssh -i ~/.ssh/LightsailDefaultKey-ap-southeast-2.pem"
	# rsync pollock/ ubuntu@3.106.115.205:/home/ubuntu/pollock/ -r -e "ssh -i ~/.ssh/aws-test-ec2.pem"
	ssh-keygen -R 54.206.66.139
	ssh-keyscan -H 54.206.66.139 >> ~/.ssh/known_hosts
	rsync pollock/ ubuntu@54.206.66.139:/home/ubuntu/pollock/ -r -e "ssh -i ~/.ssh/aws-flexdapps-dev-default.pem"
	./expscript_prepare.sh
	ssh -i ~/.ssh/aws-flexdapps-dev-default.pem ubuntu@54.206.66.139 '{ sleep 1; sudo reboot; } >/dev/null &'
	echo "begin waiting for ssh..."
	./expscript_install.sh

clean:
	rm -rf dist build *.egg-info .eggs

build:
	make clean
	python3 setup.py bdist_wheel sdist

install:
	pip install -r requirements.txt
	pip install dist/pollock-*-*.whl

uninstall:
	pip uninstall pollock -y

dev:
	make uninstall
	make clean
	make build
	make install
