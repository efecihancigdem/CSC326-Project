import boto.ec2

#A security group is already created using the protocols provided, its name is "csc326lab2"
#a key pair is also created called "ourKeyPair"
#an instance has been run with amiID "ami-9aaa1cf2"

#set up the region we will use
conn = boto.ec2.connect_to_region("us-east-1")
key_pair = conn.create_key_pair("ourKeyPair")
group =  conn.create_security_group("csc326-group27")
group.authorize("icmp", -1, -1, "0.0.0.0/0")
group.autorize("tcp", 22, 22, "0.0.0.0/0")
group.autorize("tcp", 80, 80, "0.0.0.0/0")

