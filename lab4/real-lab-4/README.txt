We are team 27, this is our lab4 for csc326
Our final report is in the pdf in this folder.
Our DNS: c2-100-24-87-175.compute-1.amazonaws.com
Our IP: 100.24.87.175


To run our website locally, please first crawl the web by:
	1. Install redis by running "apt-get install redis-server"(we can't install them on school machine, because permission denied)
	2. Install redis python library by "pip install redis" 
	3. go to folder "backend"
	4. run setup.py
Then run the website by:
	5. go to frontend folder
	6. run front_end_server.py
	7. your website will be at address "localhost:8090"
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!Note: it is on port "8090" not "8080"!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!Note: it is on port "8090" not "8080"!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!Note: it is on port "8090" not "8080"!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

To one-click deploy the website, you need to:
	1. go to folder one_click_deployment
	2. put your keypair .pem file in that folder (one_click_deployment)
	3. run backenddeployment.py and give it the name of the keypair file as argument (please include .pem in your argument)
	4. example: python backenddeployment.py <your_keypair_name>.pem
	5. It will create a new instance on the account based on your configuration of aws
	6. It will make you wait 5 or more minutes to wait until the new instance is stable before it deploys the website on the instance
	7. Please be patient and wait
	8. Please be patient and wait a little longer
	9. Please be patient and wait just a tiny longer
		If this failed, the instance id it created should be printed on terminal, please run the backenddeployment script again with the instance id as the second argument
		 "python backenddeployment.py <your_keypair_name>.pem <instance_id>"
		It will skip creating a new instance if it sees the second argument
	10. It will finally finish setup and print the ID, DNS, and instance id on the terminal
	11. We noticed some behaviours of setting up:
		Sometimes the library installation on the new instance is not successful
		The script will not quit at the end, because the nohup command does not word very well with our approach with boto library for sending ssh commands
		However, the website will run persistently even if you close the terminal

To one-click terminate an instance, you need to:
	1. go to folder one_click_deployment
	2. run shutdowninstance.py on command line and give it the instance id as argument
	3. example: python shutdowninstance.py <your_instance_id>
	4. It will terminate the instance, but not the security group as it is not required by lab document

FINALLY: Thank you for all your help and all your work, you guys are the best TAs!!!!!!!!!!!!!!!!!!!!!!!!!!