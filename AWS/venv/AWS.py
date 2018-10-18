import boto.ec2

#A security group is already created using the protocols provided, its name is "csc326lab2"
#a key pair is also created called "ourKeyPair"
#an instance has been run with amiID "ami-9aaa1cf2"

#set up the region we will use
conn = boto.ec2.connect_to_region("us-east-1")
group=conn.get_all_security_groups()
resp=conn.get_all_instances()
print "hello"

