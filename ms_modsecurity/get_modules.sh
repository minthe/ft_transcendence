#!/bin/bash

# Run your command and save its output into a variable
output=$(nginx -V)
./configure --add-dynamic-module=../ModSecurity-nginx $output



#cat << EOF > get_modules.sh
#output=$(nginx -V)
#./configure --add-dynamic-module=../ModSecurity-nginx $output
#EOF



