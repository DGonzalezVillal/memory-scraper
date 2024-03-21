This script can be used to find secrets contained in Virtual Machine memory.

# Usage
The program has to be used with root privileges.

3 parametrs have to be passed to run the program:

- The PID of the running VM

You can find the PID by running the command:
```
sudo ps axo pid,command | grep qemu
```
It will be the number that leads the command use to launch the VM. 

- The size of the VM memory in MB.

This can be found on the command used to launch the VM as well. 
If no memory parameter was passed on QEMU, the default size is 128 MB.

- The secret to be looked for.

The secret has to be provided in quotation marks since it is string being searched.
The secret is case-unsensitive, so it will mach the string regardless of it being upper-case or lower-case.

Example:
```
sudo python3 ./memory_scraper.py 10288 128 "THIS IS MY SECRET"
```