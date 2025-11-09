#!/usr/bin/python3

# INET4031
# Your Name
# Data Created
# Date Last Modified

# Imports:
import os # run system commands
import re # validate and parse each input line with regular expressions
import sys # read lines from stdin and control process exit/status

def main():
    for line in sys.stdin:

        # Verifies the line contains the field delimiter (':'). 
        match = re.match("^#",line)

        # Splits the input line into 5 expected fields
        fields = line.strip().split(':')

        # This IF statement skips lines that are either comments or improperly formatted 
        # It depends on the previous regex (match) and split (fields) to detect these conditions
        # If true, 'continue' moves to the next line instead of processing invalid or commented input
        if match or len(fields) != 5:
            continue

        # These three lines extract key user information from the colon-delimited input.
        # username: the account name, password: user's login password, and gecos: combined full name info.
        # This mirrors the fields stored in /etc/passwd, where username and GECOS data are written for each use
        username = fields[0]
        password = fields[1]
        gecos = "%s %s,,," % (fields[3],fields[2])

        # This splits the list of groups (field[4]) by commas so each group can be processed separately later
        groups = fields[4].split(',')

        # Provies feedback to the user so they can see which account is being created
        print("==> Creating account for %s..." % (username))
        # Builds the Linux command to create a new user with the given GECOS info but no present password
        # CMD will contain something like "/usr/sbin/adduser
        cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos,username)

        # Print first for verification
        # If uncommented - what will the os.system(cmd) statemetn attempt to do?
        #print cmd
        #os.system(cmd)

        # Tells the user that the script is about to set a password
        print("==> Setting the password for %s..." % (username))
        # Builds a command to set the password using echo and passwd. 
        #"cmd" will contain: echo -ne 'password\npassword' | sudo passwd username
        cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password,password,username)

        # What  will the os.system(cmd) statemetn attempt to do?
        #print cmd
        #os.system(cmd)

        for group in groups:
            # Checks whether the group field contains a real group name.
            # If group != '-', the script adds the user to that group using adduser.
            if group != '-':
                print("==> Assigning %s to the %s group..." % (username,group))
                cmd = "/usr/sbin/adduser %s %s" % (username,group)
                #print cmd
                #os.system(cmd)

if __name__ == '__main__':
    main()
