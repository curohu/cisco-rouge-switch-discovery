# Cisco Rouge Switch Discovery

This script will discover any interfaces that have more than 2 MAC addresses and then write them to an Excel document. This is a wrapper for some older code that I wrote a year ago, so it may not work on all switch versions. It has been tested on the latest 3850 and 9300 code. There is no risk to run this as all it does is send to the switch "show mac-address table" and then get the output.


Instructions:
1.	Download and install Python 3 (Python 2.7 will not work)
2.	Download and extract the Repository [HERE](https://git.emea.zf-world.com/cullen.humphries/cisco-rouge-switch-discovery/-/archive/master/cisco-rouge-switch-discovery-master.zip) 
3.	Add hostnames or IP addresses that you want to check to the "hostnames.txt" file
4.	Run the script by browsing to the directory with CMD and running "run.py" with "python.exe .\run.py"
5.	Enter all required information, the Usernames and Password are not recorded
6.	Open the Analysis file that it creates and review


The analysis file will list all ports with more than 2 MAC addresses and the vendors for those MAC addresses based on OUI prefixes. It is up to the user to review the table. Suspicious ports will have more than 2 MAC addresses and have weird MAC address vendors. Chinese names or consumer grade equipment vendors, like Netgear or Asus, are usually giveaways.


In the next version I may add an automated review function and move the script from SSH to Netconf or equivalent. I will also look into reformatting the script for Junos devices


If you have any questions about the script please email me at: Cullen.Humphries@zf.com










