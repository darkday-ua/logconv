import re
import sys
import os
import subprocess

fname = None
dir_out = "."
fname_out = None
arguments = list()
verbose = False
filter = None
sorting = None
columns = [
    ("ip", "ip address"),
    ("dt", "datetime"),
    ("bs", "bytes sent"),
    ("status", "status code"),
    ("<digit>", "by field number [0..17]"),
]
col_index = {
    "ip": 0,
    "dt": 1,
    "method": 2,
    "req": 3,
    "proto": 4,
    "bs": 5,
    "status": 6,
    "ref": 7,
    "ua": 8,
    "f0": 9,
    "f1": 10,
    "f2": 11,
    "f3": 12,
    "fromip": 13,
    "f4": 14,
    "f5": 15,
    "f6": 16,
    "hash": 17,
}


def show_help(wrong=""):
    if wrong != "":
        print(f"wrong argument at: {wrong}!", file=sys.stderr)
    print(f"Usage:\n", file=sys.stderr)
    print(f"cat <logfilename> | python logconv.py [OPTIONS]\nor", file=sys.stderr)
    print(f"python logconv.py <logfilename> [OPTIONS]\nor", file=sys.stderr)
    print(f"cat <logfilename> | docker run -i logfilename [OPTIONS]\n", file=sys.stderr)
    print(f"OPTIONS:", file=sys.stderr)
    print(f"-v\t\t\tverbose", file=sys.stderr)
    print(f"-h\t\t\tshow this help", file=sys.stderr)
    print(
        f"-o <fname>\t\tset <fname> as output file. If no -o <fname> is set, the default stdout will be used",
        file=sys.stderr,
    )
    print(
        "-d <dirname>\t\tset <dirname> as output directory (must be present)",
        file=sys.stderr,
    )
    print("-f <filter_string>\tusing filter <filter_string>", file=sys.stderr)
    print("-s <column>\t\tsort by <column>", file=sys.stderr)
    for el in columns:
        print(f"\t{el[0]}\t{el[1]}", file=sys.stderr)
    sys.exit(1)


# print(f"args {sys.argv}", file=sys.stderr)
start_arg = 1
if not sys.stdin.isatty():
    input_stream = sys.stdin
else:
    if len(sys.argv) < 2:
        show_help()
    elif sys.argv[1] == "-h":
        show_help()
    elif len(sys.argv) == 2 and sys.argv[1][0] == "-":
        show_help("filename must preceede options")
    try:
        fname = sys.argv[1]
        start_arg = 2
    except IndexError:
        message = "need filename as a first argument or piped stdin!"
        raise IndexError(message)
    else:
        input_stream = open(fname, "r")
        fname_out = fname + ".csv"

for i in range(start_arg, len(sys.argv)):

    if sys.argv[i][0] == "-":
        arguments.append({"flag": sys.argv[i], "val": None})
        if sys.argv[i] == "-v":
            verbose = True
    else:
        try:

            if not arguments[len(arguments) - 1]["val"]:
                arguments[len(arguments) - 1]["val"] = sys.argv[i]
        except IndexError:
            show_help(sys.argv[i])

# print(arguments, file=sys.stderr)
for arg in arguments:
    flag, val = arg["flag"], arg["val"]
    # print(f"{flag} {val}", file=sys.stderr)
    if flag == "-d":
        dir_out = val
        if not os.path.isdir(dir_out):
            print(f"directory {dir_out} does not exist!", file=sys.stderr)
            sys.exit(1)
    elif flag == "-o":
        fname_out = val

    elif flag == "-f":
        filter = val

    elif flag == "-s":
        sorting = val
    elif flag == "-v":
        pass
    elif flag == "-h":
        show_help()
    else:
        show_help(f"while parsing flag {flag}")


if verbose:
    print(f"start converting with output to {dir_out}/{fname}", file=sys.stderr)
    if filter:
        print(f'using filter string "{filter}"', file=sys.stderr)
    if sorting:
        print(f'using sort by "{sorting}"', file=sys.stderr)

logformat = re.compile(
    r"(?P<ipaddress>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - "
    r"\[(?P<dateandtime>\d{2}\/[a-z]{3}\/\d{4}:\d{2}:\d{2}:\d{2} (\+|\-)\d{4})\]"
    r" ((\"(?P<method>(GET|POST|PUT|DELETE|HEAD|PATCH|TRACE|OPTIONS|CONNECT))"
    r" (?P<reqst>.+) (?P<proto>.*)\")) (?P<statuscode>\d{3}) (?P<bytessent>\d+)"
    r" \"(?P<refferer>(\-)|(.+))\" \"(?P<useragent>.+)\" (?P<field0>\d+) "
    r"(?P<field1>.*) \[(?P<field2>.*)\] \[(?P<field3>.*)\] "
    r"(?P<from>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}\s)"
    r"(?P<field4>\d+) (?P<field5>.+) (?P<field6>\d+) "
    r"(?P<hash>.*$)",
    re.IGNORECASE,
)

if filter:
    sp = re.compile(r"^.*" + filter + ".*$")
else:
    sp = re.compile(r".*")

if verbose:
    print(f"script started", file=sys.stderr)


csv_data = []
for line in input_stream:
    if filter:
        fd = re.search(sp, line)
        if not fd:
            continue
    csv_data.append({})
    res = csv_data[-1]
    data = re.search(logformat, line)
    if data:
        try:
            datadict = data.groupdict()
            res["ip"] = datadict["ipaddress"]
            res["dt"] = datadict["dateandtime"]
            res["method"] = datadict["method"]
            res["req"] = datadict["reqst"]
            res["proto"] = datadict["proto"]
            res["status"] = datadict["statuscode"]
            res["bs"] = int(datadict["bytessent"])
            res["ref"] = datadict["refferer"]
            res["ua"] = datadict["useragent"]
            res["f0"] = int(datadict["field0"])
            res["f1"] = float(datadict["field1"])
            res["f2"] = datadict["field2"]
            res["f3"] = datadict["field3"]
            res["fromip"] = datadict["from"]
            res["f4"] = int(datadict["field4"])
            res["f5"] = float(datadict["field5"])
            res["f6"] = int(datadict["field6"])
            res["hash"] = datadict["hash"]
        except Exception as ex:
            if verbose:
                print(f"error {ex} in parsing line", file=sys.stderr)
fn = None

if sorting:
    if sorting.isdigit():
        try:
            fn = int(sorting)
        except Exception as ex:
            show_help(f"wrong sorting column number {sorting}")
        if fn < 0 or fn > 17:
            show_help(f"wrong sorting column number {fn}")
        for k, v in col_index.items():
            if v == fn:
                fn = k
                break
    else:
        if sorting not in col_index:
            show_help(f"wrong sorting column {sorting}")
    if fn:
        csv_sorted = sorted(csv_data, key=lambda el: el[fn])
    else:
        csv_sorted = sorted(csv_data, key=lambda el: el[sorting])
else:
    csv_sorted = csv_data
if fname_out:
    os.chdir(dir_out + "/")
    subprocess.run(
        ["git", "config", "--global", "user.name", "logconv"], stdout=subprocess.DEVNULL
    )
    subprocess.run(
        ["git", "config", "--global", "user.email", "logconv@log.cc"],
        stdout=subprocess.DEVNULL,
    )
    if not os.path.isdir(".git"):
        print(f"no git initialized in target dir", file=sys.stderr)

        subprocess.run(["git", "init"], stdout=subprocess.DEVNULL)
    else:
        if verbose:
            print("commiting old data", file=sys.stderr)
            subprocess.run(["git", "add", "."], stdout=subprocess.DEVNULL)
            subprocess.run(
                ["git", "commit", "-m", '"previous state"'], stdout=subprocess.DEVNULL
            )

if fname_out:
    csv_file = open(fname_out, "w")

csv = ""

for res in csv_sorted:
    for key, val in res.items():
        csv = csv + str(val) + ";"
    csv = csv + "\n"
    if fname_out:
        csv_file.write(csv)
    else:
        if "DOCKER" in os.environ or not fname_out:
            sys.stdout.write(csv)
    csv = ""

if fname_out:
    csv_file.close()


if verbose:
    print(f"csv file {fname_out} has been updated!", file=sys.stderr)
if fname_out:
    subprocess.run(["git", "add", "."], stdout=subprocess.DEVNULL)
    subprocess.run(["git", "commit", "-m", '"new export"'], stdout=subprocess.DEVNULL)
    if verbose:
        print("new data commited", file=sys.stderr)
