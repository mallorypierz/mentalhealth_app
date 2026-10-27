"""Host-only testing-session administration. Does not enable live providers."""
import argparse
from uuid import UUID
from .db import initialize, DATABASE_PATH
from .repositories.voice_budget import create_test_session, close_test_session

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    commands=parser.add_subparsers(dest='command',required=True)
    create=commands.add_parser('create')
    create.add_argument('--id',type=UUID,required=True)
    create.add_argument('--label',required=True)
    create.add_argument('--calls',type=int,required=True)
    create.add_argument('--reservation-cents',type=int,required=True)
    close=commands.add_parser('close'); close.add_argument('--id',type=UUID,required=True)
    args=parser.parse_args(); initialize(DATABASE_PATH,True)
    if args.command=='create':
        ident=create_test_session(DATABASE_PATH,args.id,args.label,args.calls,args.reservation_cents*10000)
        print('Testing session recorded:',ident,'— live providers remain separately configured.')
    else:
        close_test_session(DATABASE_PATH,args.id);print('Testing session closed.')
if __name__=='__main__': main()
