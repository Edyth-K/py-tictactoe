from client import run_client
from server import run_server

import argparse
import sys

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description='Tic-Tac-Toe Multiplayer Game')
    
    # Add mutually exclusive group for server/client modes
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-s', '--server', action='store_true', 
                      help='Run as server')
    group.add_argument('-c', '--client', action='store_true',
                      help='Run as client')
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Run appropriate mode based on arguments
    if args.server:
        print(f"Starting server on port...")
        run_server()
    elif args.client:
        print(f"Connecting...")
        run_client()


if __name__ == "__main__":
    main()