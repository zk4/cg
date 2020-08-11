#coding: utf-8
from .logx import setup_logging
import logging
import argparse
import sys
import os
# don`t remove this line
setup_logging()
logger = logging.getLogger(__name__)
from os.path import join, isfile,basename
from pathlib import Path


def copying(src,dest):
    pass

def fullReplace(root,oldKey,newKey):
    if oldKey == newKey or len(newKey)==0:
        return
    for dname, dirs, files in os.walk(root,topdown=False):
        for filename in files:
            oldfile = join(dname,filename)
            if isfile(oldfile):
                if oldKey in filename:
                    newfile = join(dname,filename.replace(oldKey,newKey))
                    print(oldfile,newfile)
                    os.rename(oldfile,newfile)

        # rename folder 
        if oldKey in basename(dname):
            destfolder = join(Path(dname).parent,basename(dname).replace(oldKey,newKey))
            os.rename(dname,destfolder)

def main(root,args):
    keypais={}
    prefix = args.arg_prefix or "CG_ARG__"
    print(args.magic)
    idx = 0
    for m in args.magic:
        if ":" not in m:
            root = join(root,m)
        else:
            ms = m.split(":")
            key = ms[0]
            val = ms[1]
            if key == val:
                print(f"keypair: {key}:{val} must not be the same!")
                return 
            if len(key.strip()) == 0:
                key = prefix +str(idx)
                idx+=1
            keypais[key] = val
        
    print(root,keypais)
    return
    fullReplace(tmpls_folder,oldKey,newKey)

def list(root,depth):
    stuff = os.path.abspath(os.path.expanduser(os.path.expandvars(root)))

    for root,dirs,files in os.walk(stuff):
        if root[len(stuff):].count(os.sep) < depth:
            # for f in files:
            print(os.path.join(root))

def entry_point():
    parser = createParse()
    mainArgs=parser.parse_args()
    root  = os.environ.get("CG_TMPLS")
    if root is None:
        print("env CG_TMPLS is not definded!")
        return

    if mainArgs.list:
        list(root,mainArgs.depth)
    else:
        main(root,mainArgs)

def createParse():
    parser = argparse.ArgumentParser( formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="")
    # subparsers = parser.add_subparsers()
    # eat_parser = subparsers.add_parser('eat',formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="",  help='sub command demo')
    parser.add_argument('magic', metavar="o", type=str, nargs='*',
            help='folder or  newkey:oldkey')

    parser.add_argument('-a', '--arg_prefix',type=str,required=False, help='ex: CG_ARG__', default="CG_ARG__")  
    # parser.add_argument('-o', '--oldKey',type=str,required=False, help='oldKey', default="")  
    # parser.add_argument('-n', '--newKey',type=str,required=False, help='newKey', default="")  
    parser.add_argument('-l', '--list', help='list folders', default=False, action='store_true') 
    parser.add_argument('-d', '--depth',type=int,required=False, help='list depth', default=3)  
    return parser
