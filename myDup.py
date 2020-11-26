import argparse
import json
import os
import os.path
import gzip
import time
from pprint import pprint

dup_mark = set()
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
def comp2dicts(refers,filename,t_set,t_dict,kj,j):
    dups = 0
    for filename_ref,(t_set_ref,t_dict_ref) in refers.items():
        if filename in dup_mark and filename_ref in dup_mark:
            continue
        # region keyJaccardSimilarity
        t_set_u = t_set_ref.union(t_set)
        numDistinct = len(t_set_u)
        sameKeys = len(t_set_ref)+len(t_set)-numDistinct
        keyJaccardSimilarity = 0 if numDistinct == 0 else float(sameKeys) / numDistinct
        # endregion
        if keyJaccardSimilarity<kj:
            continue
        numerator = 0
        denominator = 0
        for k in t_set_u:
            count_ref = t_dict_ref.get(k,0)
            count = t_dict.get(k,0)
            numerator += min(count,count_ref)
            denominator += max(count,count_ref)
        jaccardSimilarity = 0 if denominator==0 else float(numerator)/denominator
        if jaccardSimilarity<j:
            continue
        dup_mark.add(filename_ref)
        dup_mark.add(filename)
        dups+=1
            # print("compare {0} with {1} similarity is  {2},{3}".format(filename1,filename,keyJaccardSimilarity,jaccardSimilarity))
    return dups
def main():
    '''
    1974 2594
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
    parser.add_argument("--keyJaccardThreshold", default=0.8,
                        help="The Jaccard similarity threshold for token-sets [default: 0.8].")
    parser.add_argument("--jaccardThreshold", default=0.7,
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
    refers = {}
    con = read_gz_file(file_path)
    dups =0
    if getattr(con, '__iter__', None):
        for idx,line in enumerate(con):
            if idx < begin:
                continue
            data = json.loads(line)
            filename = data.get('filename')
            tokens = data.get('tokens')
            t_dict = {}
            for token in tokens:
                t_dict[token] = t_dict.get(token, 0)+1
            t_set = set(t_dict.keys())
            dups += comp2dicts(refers,filename,t_set,t_dict,args.keyJaccardThreshold,args.jaccardThreshold)
            if idx <=end:
                refers[filename] = (t_set,t_dict)
    print(dups,len(dup_mark))

if __name__ == "__main__":
    time_start = time.time()
    main()
    time_end = time.time()
    print('totally cost',time_end-time_start)
