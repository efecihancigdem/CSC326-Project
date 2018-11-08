import boto.ec2

conn = boto.ec2.connect_to_region("us-east-1")
key_pair = conn.create_key_pair("ourKeyPair")
group =  conn.create_security_group("csc326-group27")
group.authorize("icmp", -1, -1, "0.0.0.0/0")
group.autorize("tcp", 22, 22, "0.0.0.0/0")
group.autorize("tcp", 80, 80, "0.0.0.0/0")
resp = conn.run_instances("ami-9aaa1cf2", instance_type="t2.micro", key_name="ourKeyPair")

