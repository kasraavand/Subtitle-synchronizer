from datetime import datetime, timedelta
from tempfile import NamedTemporaryFile
from operator import attrgetter, add, sub
import shutil
import argparse
import re


def synchronizer(file_name, mode, second):
    regex = re.compile(r'(\d+:\d+:\d+),(\d+) --> (\d+:\d+:\d+),(\d+)')
    tempfile = NamedTemporaryFile(delete=False)
    d = {'trail': add, 'lead': sub}
    with open(file_name) as f, open('new.srt', 'w') as tempfile:
        for line in f:
            m = regex.search(line)
            if m:
                start, v1, end, v2 = m.groups()
                start = d[mode](datetime.strptime(start, '%H:%M:%S'), timedelta(seconds=second))
                start = start.strftime('%H:%M:%S')
                end = d[mode](datetime.strptime(end, '%H:%M:%S'), timedelta(seconds=second))
                end = end.strftime('%H:%M:%S')
                tempfile.write("{},{} --> {},{}\n".format(start, v1, end, v2))
            else:
                tempfile.write(line)
    shutil.move(tempfile.name, file_name)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Subtitle synchronizer ;)")
    # Adding arguments
    parser.add_argument("-F", "-file_name", help="Name of subtitle", default='')
    parser.add_argument("-M", "-mode", help="lead (subtracting time) or trail (adding time)", default='lead')
    parser.add_argument("-T", "-time", help="trailing or leading Time in second", default='')
    args = parser.parse_args()
    synchronizer(*attrgetter('F', 'M')(args), int(args.T)
