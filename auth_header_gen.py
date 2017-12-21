import getopt, sys
from base64 import b64encode

def usage():
    print(
        """
        Generate an HTTP Basic Authentication header from a username and a
        password.

        Usage: python auth_header_gen.py --user test@test.com --password xxxxxx
        """)

def main():
    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hu:p:",
            ["help", "user=", "password="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    user = None
    password = None

    for option, arg in opts:
        if option in ("-h", "--help"):
            usage()
            sys.exit()
        elif option in ("-u", "--user"):
            user = arg
        elif option in ("-p", "--password"):
            password = arg
        else:
            assert False, "unhandled option"

    if not user: assert False, "missing user"
    if not password: assert False, "missing password"

    auth_string = f"{user}:{password}"
    encoded_auth = b64encode(str.encode(auth_string)).decode("ascii")
    auth_header = f"'Authorization' : Basic {encoded_auth}"

    print(f"user: {user}, password: {password}")
    print(auth_header)


if __name__ == "__main__":
    main()
