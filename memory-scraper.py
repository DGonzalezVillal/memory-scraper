import sys
import argparse
import memory_reader


parser = argparse.ArgumentParser(
    description="Pass PID and Secret for scraping")
parser.add_argument("pid", help="pid of vm", type=str)
parser.add_argument("secret", help="secret to look for in the vm", type=str)

def get_vm_address(pid):
    # Find the size of the memory (Eg QEMU -m 2048 M)
    mem_size = memory_reader.convert_mb_to_bytes(2048)
    # With the memory size found, find the top and bottom adresses corresponding to the VMs memory
    top_addr, bot_addr = memory_reader.find_ram_specific_memory(
        pid, mem_size)
    return top_addr, bot_addr

def print_memory_pages(pid,top_addr,bot_addr):
    # Grab one page of memory for printing
    memory = memory_reader.read_one_memory_page_for_printing(pid, top_addr, bot_addr)
    #For each line in the memory page, print its contents
    print(memory.stdout.decode('utf-8'))

def print_secret(pid,top_addr,bot_addr,secret):
    # Grab one page of memory for printing
    secret = memory_reader.find_secret(pid, top_addr, bot_addr,secret)
    #For each line in the memory page, print its contents
    # if secret and hasattr(secret, "stdout") and not hasattr(secret, "stderr"):
    if secret.returncode == 0:
        print(secret.stdout.decode('utf-8'))
        # print(secret.stdout)
    else:
        print("NO SECRET FOUND!")

def main():
    args = parser.parse_args()
    top_addr, bot_addr = get_vm_address(args.pid)
    # print_memory_pages(args.pid, top_addr, bot_addr)
    print_secret(args.pid, top_addr, bot_addr, args.secret)
    

if __name__ == "__main__":
    sys.exit(main())