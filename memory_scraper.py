'''Script that will allow you to scrape a VM's memory 
in order to find a secret inside of the memory.
Can be used to test SEV memory encryption.
A user will have to pass in the pid of the vm,
the size of the VM in MB,
and the desired secret in quotations.
'''

import sys
import argparse
import memory_reader


parser = argparse.ArgumentParser(
    description="Pass PID and Secret for scraping")
parser.add_argument("pid", help="pid of vm", type=str)
parser.add_argument("mem_size", help="memory size of the VM in MB", type=str)
parser.add_argument("secret", help="secret to look for in the vm", type=str)

def get_vm_address(pid, mem_size):
    '''
    Using the VM's pid and memory size, find the addresses of the virtual 
    machine in memory.
    '''
    # Convert size of the VM into bytes (Eg QEMU -m 2048 M)
    mem_size = memory_reader.convert_mb_to_bytes(mem_size)
    # With the memory size, find the top and bottom adresses corresponding to the VMs memory
    top_addr, bot_addr = memory_reader.find_ram_specific_memory(
        pid, mem_size)
    return top_addr, bot_addr

def print_memory_pages(pid,top_addr,bot_addr):
    '''Print a single page of memory to the terminal'''
    # Grab one page of memory for printing
    memory = memory_reader.read_one_memory_page_for_printing(pid, top_addr, bot_addr)
    #For each line in the memory page, print its contents
    print(memory.stdout.decode('utf-8'))

def print_secret(pid,top_addr,bot_addr,secret):
    '''Find the desired secret in memory, if the secret is not found
    print no secret found'''
    # Grab one page of memory for printing
    secret = memory_reader.find_secret(pid, top_addr, bot_addr,secret)
    # If the secret is found print the memory section where the secret is
    # contained
    if secret.returncode == 0:
        print(secret.stdout.decode('utf-8'))
    else:
        print("NO SECRET FOUND!")

def main():
    '''Script that will allow you to scrape a VM's memory 
    in order to find a secret inside of the memory.
    Can be used to test SEV memory encryption.
    A user will have to pass in the pid of the vm,
    the size of the VM in MB,
    and the desired secret in quotations.
    '''
    args = parser.parse_args()
    top_addr, bot_addr = get_vm_address(args.pid, int(args.mem_size))
    print_secret(args.pid, top_addr, bot_addr, args.secret)

if __name__ == "__main__":
    sys.exit(main())
    