import boto.ec2

conn = boto.ec2.connect_to_region("us-east-1")
key_pair=conn.delete_key_pair("ourKeyPair")
key_pair=conn.create_key_pair("ourKeyPair")
key_pair.save("")
