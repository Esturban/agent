#!/usr/bin/env python3
import os
import argparse
from qdrant_client import QdrantClient
from dotenv import load_dotenv

load_dotenv()


def list_collections(client):
    cols = client.get_collections()
    return [c.name for c in cols.collections]


def delete_collection(client, name):
    client.delete_collection(collection_name=name)


def main():
    parser = argparse.ArgumentParser(description="List or delete Qdrant collections safely.")
    parser.add_argument("--url", default=os.getenv("QDRANT_URL"), help="Qdrant URL")
    parser.add_argument("--key", default=os.getenv("QDRANT_KEY"), help="Qdrant API key")
    parser.add_argument("--list", action="store_true", help="List collections")
    parser.add_argument("--delete", help="Delete collection by name")
    parser.add_argument("--all", action="store_true", help="Delete all collections (requires --yes)")
    parser.add_argument("--yes", action="store_true", help="Confirm destructive actions")
    args = parser.parse_args()

    if not args.url:
        print("QDRANT_URL not provided; set env or pass --url")
        return

    client = QdrantClient(url=args.url, api_key=args.key)

    if args.list:
        print("Collections:")
        for c in list_collections(client):
            print(" -", c)
        return

    if args.delete:
        if not args.yes:
            confirm = input(f"Delete collection '{args.delete}'? Type YES to confirm: ")
            if confirm != "YES":
                print("Aborting")
                return
        delete_collection(client, args.delete)
        print(f"Deleted collection {args.delete}")
        return

    if args.all:
        if not args.yes:
            confirm = input("Delete ALL collections? Type YES to confirm: ")
            if confirm != "YES":
                print("Aborting")
                return
        for name in list_collections(client):
            print("Deleting:", name)
            delete_collection(client, name)
        print("All collections deleted")
        return

    parser.print_help()


if __name__ == "__main__":
    main()


