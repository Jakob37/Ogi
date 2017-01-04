#/usr/bin/env python3

import argparse
import re
import datetime
import configparser
import os


from modules.time_entry import TimeEntry

def main(args, conf):

    output_path = conf.get("file_paths", "data")
    test_output_path = conf.get("file_paths", "test_data")

    time_entry = TimeEntry(args.log_type, 
                           args.message,
                           args.focus,
                           args.date,
                           args.time,
                           args.project,
                           args.duration)

    if not args.testrun:
        with open(output_path, 'a') as append_fh:
            print(time_entry, file=append_fh)
    else:
        print("Test entry written")
        print(time_entry)
        with open(test_output_path, 'a') as append_fh:
            print(time_entry, file=append_fh)

