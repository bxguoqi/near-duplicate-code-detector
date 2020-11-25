import argparse
import json
import os
import os.path
import gzip
from pprint import pprint

def get_read_gz_file_line_count(path):
    if os.path.exists(path):
        with gzip.open(path, 'rb') as f:
            for i, l in enumerate(f):
                pass
        print("File {1} contain {0} lines".format(i, path))
        return i
    else:
        print('the path [{}] is not exist!'.format(path))
        return 0
def read_gz_file(path):
    if os.path.exists(path):
        with gzip.open(path, 'r') as pf:
            for line in pf:
                yield line
    else:
        print('the path [{}] is not exist!'.format(path))
def comp2dicts():
    ''''''
    pass
def main():
    '''
    Usage:
        python myDup.py \
         --dir=<path> \
         --key-jaccard-threshold=<val> \
         --jaccard-threshold=<val>
         eg:python myDup.py --dir tokens --begin 0.1 --end 0.3
        Options:
          --dir=<path>                   Directory where .jsonl.gz files live.
          --key-jaccard-threshold=<val>  The Jaccard similarity threshold for token-sets [default: 0.8].
          --jaccard-threshold=<val>      The Jaccard similarity threshold for token multisets [default: 0.7].
    '''

    # region parameters
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", default=None, type=str, required=True,
                        help="Directory where .jsonl.gz files live.")
    parser.add_argument("--begin", default=0.0, type=float,
                        help="deal with the part of the data")
    parser.add_argument("--end", default=1.0, type=float,
                        help="deal with the part of the data")
    parser.add_argument("--key-jaccard-threshold", default=0.8,
                        help="The Jaccard similarity threshold for token-sets [default: 0.8].")
    parser.add_argument("--jaccard-threshold", default=0.7,
                        help="The Jaccard similarity threshold for token multisets [default: 0.7].")
    args = parser.parse_args()
    # endregion

    file_path=''
    for root, dirs, files in os.walk(args.dir):
        for file in files:
            #只要第一个file
            file_path = os.path.join(root, file)
            break
    # count the size and the begin,end
    size = get_read_gz_file_line_count(file_path)
    begin = int(size*args.begin)
    begin = begin+1 if begin>0 else begin
    end = int(size*args.end)
    print(size,begin,end)

    # compare the (begin,end] part to (begin,size] part
    dicts = []
    con = read_gz_file(file_path)
    if getattr(con, '__iter__', None):
        for idx,line in enumerate(con):
            if idx < begin:
                continue
            data = json.loads(line)
            filename = data.get('filename')
            tokens = data.get('tokens')
            comp2dicts(filename,tokens)
            if idx <=end:
                print(idx)
                continue
            else:
                continue
            t_dict = {}
            for token in tokens:
                t_dict[token] = t_dict.get(token, 0)+1
            t_set = set(t_dict.keys())
            print(t_set)
            print(t_dict)


if __name__ == "__main__":
    # di = {}
    # di.get(1)

    main()