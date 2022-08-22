import argparse
import os
import sys
import zlib

from binary_search_tree import *

argparser = argparse.ArgumentParser(description="Key-value store")
argsubparsers = argparser.add_subparsers(title="Commands", dest="command")
argsubparsers.required = True

def main(argv=sys.argv[1:]):
    print("hello")
    args = argparser.parse_args(argv)
    if args.command == "init": cmd_init(args)
    elif args.command == "connect": cmd_connect(args)

class Database():

    path = None
    root = None

    def __init__(self, path):
        if not os.path.isdir(path):
            raise Exception("Not a database %s" % path)
        self.path = path
        
        data = ""
        data_path = self.get_path("data")
        if os.stat(data_path).st_size > 0:
            f = open(data_path, "rb")
            data = zlib.decompress(f.read()).decode()
            f.close()

        self.root = deserialize(data)

    def get_path(self, *path):
        return os.path.join(self.path, *path)

    # Serialize updated tree and write to data file
    def save(self):
        data_path = self.get_path("data")
        f = open(data_path, "wb")

        s = serialize(self.root)

        f.write(zlib.compress(s.encode()))
        f.close()

def db_init(path):
    print("(INIT)")

    if os.path.exists(path):
        raise Exception("%s already exists" % path)
    os.makedirs(path)

    f = open(os.path.join(path, "meta"), "x")
    f.close()
    f = open(os.path.join(path, "data"), "x")
    f.close()
    f = open(os.path.join(path, "logs"), "x")
    f.close()

def db_connect(path):
    print("(CONNECT)")

    if not os.path.exists(path):
        print("Path does not exist.")

    db = Database(path)

    # Main loop
    while True:
        cmd = input("What would you like to do? (get/put/del/quit): ")

        if cmd == "get":
            key = input("(GET) Key: ")

            result = search(db.root, key)
            
            if result == "NULL":
                print("(GET) Key not found")
            else:
                print(result)
        
        elif cmd == "put":
            key = input("(PUT) Key: ")
            val = input("(PUT) Value: ")
            db.root = insert(db.root, key, val)

        elif cmd == "del":
            key = input("(DEL) Key: ")
            db.root = delete(db.root, key)

        elif cmd == "quit":
            print("(QUIT) Shutting down.")
            
            db.save()

            break

        else:
            print("Not sure what you meant by that.")
        
        cmd = None

argsp = argsubparsers.add_parser("init", help="Initialize a new database.")
argsp.add_argument("path", metavar="directory", nargs="?", default="./db", help="Location of database.")

def cmd_init(args):
    db_init(args.path)

argsp = argsubparsers.add_parser("connect", help="Connect to an existing database.")
argsp.add_argument("path", metavar="directory", nargs="?", default="./db", help="Location of database.")

def cmd_connect(args):
    db_connect(args.path)

if __name__ == "__main__":
    main()