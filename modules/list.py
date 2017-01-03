#!/usr/bin/env python3

def main(args, conf):

    output_path = conf.get("file_paths", "data")

    proj_dict = dict()

    header_line = None

    with open(output_path) as in_fh:
        for line in in_fh:
            line = line.rstrip()
            
            if header_line is None:
                header_line = line
                continue

            fields = line.split('\t')

            date = fields[0]
            time = fields[1]
            log_type = fields[2]
            focus = fields[3]
            duration = int(fields[4])
            message = fields[5]
            project = fields[6]
            
            if proj_dict.get(project) is None:
                proj_dict[project] = duration
            else:
                proj_dict[project] += duration
    
    print("Logged projects")
    print("Projects\tTime")
    for proj in sorted(proj_dict, key=lambda x:proj_dict[x], reverse=True):
        print("{}\t{}".format(proj, proj_dict[proj]))

