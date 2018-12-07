import sys
import boto.ec2

if len(sys.argv) is 1:
    print "you did not give an id."
    sys.exit()
conn = boto.ec2.connect_to_region("us-east-1")
conn.terminate_instances(instance_ids=[sys.argv[1]])
print "instance " + sys.argv[1]+ " terminated."