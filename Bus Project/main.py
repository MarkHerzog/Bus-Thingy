from direction import done
from group import main
from turning import convert

starting_stop = '16 Washington Valley Rd'

groups = main()
print(groups)
for group in groups:
    print(group)
    addresses = convert(group)
    print(addresses)
    addresses.insert(0, starting_stop)
    done(addresses, len(addresses))