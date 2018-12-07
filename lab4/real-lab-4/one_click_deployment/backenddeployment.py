import sys
import boto.ec2
import os
from boto.manage.cmdshell import sshclient_from_instance
import time

sys.argv.append('ourKeyPair.pem')

if len(sys.argv) is 1:
    print "You did not provide a keypair file, terminating."
    sys.exit()


conn = boto.ec2.connect_to_region("us-east-1")
print "Creating new security group named \'csc326-group27-deployment\'"
try:
    group =  conn.create_security_group(name="csc326-group27-deployment", description="security group for deployment")
except:
    print "Did not create security group, it already exists."
try:
    conn.authorize_security_group('csc326-group27-deployment', ip_protocol="icmp", from_port=-1, to_port=-1,cidr_ip='0.0.0.0/0')
except:
    print "Did not authorize icmp, it has already been authorized"
try:
    conn.authorize_security_group('csc326-group27-deployment', ip_protocol="tcp", from_port=22, to_port=22,cidr_ip='0.0.0.0/0')
    conn.authorize_security_group('csc326-group27-deployment', ip_protocol="tcp", from_port=80, to_port=80,cidr_ip='0.0.0.0/0')
except:
    print "Did not authorize tcp, it has already been authorized"
print "Port forwarding set complete"
if len(sys.argv) is 3:
    inst = conn.get_only_instances(instance_ids=[sys.argv[2]])[0]
else:
    print "running the new instance with type t2.micro"
    # we used sys.argv[1][0:-4] because we want to get rid of the .pem in the string
    resp = conn.run_instances("ami-9aaa1cf2", instance_type="t2.micro", key_name=sys.argv[1][0:-4], security_groups=["csc326-group27-deployment"])
    print "Instance created"
    print "Please wait for 5 minutes before the instance is stable, after 5 minutes, our script will continue"
    time.sleep(300)
    inst = resp.instances[0]
    print "The new instance's id is: "+ inst.id
    #ssh to the instance we created
    try:
        inst = resp.instances[0]
        inst.update()
        our_inst_id = inst.id
        os.system("ssh-keyscan -H " + our_ip_address + " >> ~/.ssh/known_hosts")
        ssh_client=sshclient_from_instance(inst, sys.argv[1], user_name='ubuntu')
    except:
        print "still not stable, wait another 1 minute please"
        time.sleep(60)
        try:
            inst = resp.instances[0]
            inst.update()
            our_inst_id = inst.id
            os.system("ssh-keyscan -H " + our_ip_address + " >> ~/.ssh/known_hosts")
            ssh_client = sshclient_from_instance(inst, sys.argv[1], user_name='ubuntu')
        except:
            print "still not stable, wait another 5 minutes please, this is the last time we ask you to wait."
            time.sleep(300)
            try:
                inst = resp.instances[0]
                inst.update()
                our_inst_id = inst.id
                os.system("ssh-keyscan -H " + our_ip_address + " >> ~/.ssh/known_hosts")
                ssh_client = sshclient_from_instance(inst, sys.argv[1], user_name='ubuntu')
            except:
                print "failed to connect to the new instance, please run the script again with the instance id as second argument."
                print "Your instance id is: " + inst.id

# update the instance information
inst.update()
our_inst_id=inst.id
our_ip_address=inst.ip_address
our_ip_with_port=our_ip_address+":80"
our_dns=inst.public_dns_name

# ssh-keyscan -H 192.168.1.162 >> ~/.ssh/known_hosts
#make a connection in background, therefore creating a know_host file automatically
os.system("ssh-keyscan -H "+our_ip_address+" >> ~/.ssh/known_hosts")
ssh_client = sshclient_from_instance(inst, sys.argv[1], user_name='ubuntu')
#copy the compressed package to the new instance
os.system("scp -o StrictHostKeyChecking=no -i "+ sys.argv[1] + " package.tar.gz ubuntu@" + our_dns + ":")
os.system("scp -o StrictHostKeyChecking=no -i "+ sys.argv[1] + " script_nohup.py ubuntu@" + our_dns + ":")
print "finished copying files to new instance"

print "The new instance's IP address: ", our_ip_address
print "The new instance's public DNS name: ", our_dns

#this Run the command in ssh bash. Returns a tuple consisting of:
#    The integer status of the command
#    A string containing the output of the command
#    A string containing the stderr output of the command
# install redis server
# status, stdout, stderr = ssh_client.run("sudo apt-get install -y redis-server")
# print stdout
# print stderr
#run the website

print "Installing necessary files used to run the website"
print ""
print "sudo apt-get update"
status, stdout, stderr = ssh_client.run("sudo apt-get update")
print stdout
print stderr
print "sudo apt-get install -y python-pip"
status, stdout, stderr = ssh_client.run("sudo apt-get install -y python-pip")
print stdout
print stderr
print "sudo apt-get install -y python-setuptools"
status, stdout, stderr = ssh_client.run("sudo apt-get install -y python-setuptools")
print stdout
print stderr
print "sudo pip install --upgrade pip"
status, stdout, stderr = ssh_client.run("sudo pip install --upgrade pip")
print stdout
print stderr
status, stdout, stderr = ssh_client.run("sudo easy_install BeautifulSoup")
print stdout
print stderr
status, stdout, stderr = ssh_client.run("sudo apt-get install redis-server -y")
print stdout
print stderr

print "sudo pip install --upgrade numpy"
status, stdout, stderr = ssh_client.run("sudo pip install --upgrade numpy")
print stdout
print stderr

print "sudo pip install --upgrade redis"
status, stdout, stderr = ssh_client.run("sudo pip install redis")
print stdout
print stderr

print "sudo easy_install oauth2client"
status, stdout, stderr = ssh_client.run("sudo easy_install oauth2client")
print stdout
print stderr

print "sudo pip install oauth2client"
status, stdout, stderr = ssh_client.run("sudo pip install oauth2client")
print stdout
print stderr

print "sudo pip install --upgrade google-api-python-client"
status, stdout, stderr = ssh_client.run("sudo pip install --upgrade google-api-python-client")
print stdout
print stderr

status, stdout, stderr = ssh_client.run("sudo pip install beaker")
print stdout
print stderr

status, stdout, stderr = ssh_client.run("sudo pip install httplib2")
print stdout
print stderr


# unzip the package file
status, stdout, stderr = ssh_client.run("tar -xvzf package.tar.gz")
print stdout
# crawl the web
status, stdout, stderr = ssh_client.run("sudo python package/Backend/setup.py "+our_ip_with_port)
print stdout
print stderr

print "The new instance's id is: ", our_inst_id
print "The new instance's IP address: ", our_ip_address
print "The new instance's public DNS name: ", our_dns
print "The website should be running on address: ", our_ip_address

status, stdout, stderr = ssh_client.run("nohup sudo python package/frontend/front_end_server.py "+our_ip_with_port+"> foo.out 2> foo.err < /dev/null")
print stdout
print stderr

# status, stdout, stderr = ssh_client.run("nohup sudo python package/frontend/front_end_server.py "+our_ip_with_port+"> foo.out 2> foo.err < /dev/null")
# ssh_client.run("sudo python script_nohup.py")


# status, stdout, stderr = ssh_client.run("sudo pip install --upgrade pip")
# print stdout
# status, stdout, stderr = ssh_client.run("sudo pip install --upgrade paramiko")
# print stdout
# status, stdout, stderr = ssh_client.run("sudo pip uninstall paramiko -y")
# print stdout
print "The new instance's id is: ", our_inst_id
print "The new instance's IP address: ", our_ip_address
print "The new instance's public DNS name: ", our_dns

#use this to transfer files to aws
#scp -o StrictHostKeyChecking=no -i ourKeyPair.pem package.tar.gz ubuntu@ec2-100-24-87-175.compute-1.amazonaws.com:
#ssh -o StrictHostKeyChecking=no -i ourKeyPair.pem ubuntu@ec2-100-24-87-175.compute-1.amazonaws.com