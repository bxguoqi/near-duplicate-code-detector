import argparse
import json
import os
import os.path
import gzip
import time

dups = 0
labeb_set = set()
dup_mark = {}

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
def load_data(filename):
    global dups
    global labeb_set
    global dup_mark
    if not os.path.exists(filename):
        dups = 0
        labeb_set = set()
        dup_mark = {}
    else:
        with open(filename) as f:
            dups = json.loads(f.readline())
            label_list = json.loads(f.readline())
            labeb_set = set(label_list)
            dup_mark = json.loads(f.readline())


def comp2dicts(refers,filename,t_set,t_dict,kj,j):
    # refer 里的id较小，使用归并集，把大的类别归并到小的
    dups_local = 0
    for filename_ref,(t_set_ref,t_dict_ref) in refers.items():
        if filename in dup_mark.keys() and filename_ref in dup_mark.keys():
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
        label = dup_mark.get(filename_ref,filename_ref)
        labeb_set.add(label)
        dup_mark[filename_ref] = label
        dup_mark[filename] = label
        dups_local+=1
        print("compare {0} with {1} similarity is  {2},{3}".format(filename_ref,filename,keyJaccardSimilarity,jaccardSimilarity))
    return dups_local
def main():
    '''
    Usage:
        python myDup.py \
         --dir=<path> \
         --key-jaccard-threshold=<val> \
         --jaccard-threshold=<val>
         myDup.py --dir tokens --result result.json --begin 0 --end 0.1
        Options:
          --dir=<path>                   Directory where .jsonl.gz files live.
          --key-jaccard-threshold=<val>  The Jaccard similarity threshold for token-sets [default: 0.8].
          --jaccard-threshold=<val>      The Jaccard similarity threshold for token multisets [default: 0.7].
    '''
    global dups
    global labeb_set
    global dup_mark
    # region get parameters
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", default=None, type=str, required=True,
                        help="Directory where .jsonl.gz files live.")
    parser.add_argument("--result", default=None, type=str, required=True,
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

    load_data(args.result)
    print("duplicate files:{}, in {} clusters".format(dups, len(labeb_set)))

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
    print("duplicate files:{}, in {} clusters".format(dups,len(labeb_set)))
    #save dups,label_set and dup_mark
    with open(args.result, 'w') as f:
        json.dump(dups,f)
        f.write('\n')
        json.dump(list(labeb_set),f)
        f.write('\n')
        json.dump(dup_mark,f)




#duplicate files:1974, in 681 clusters
if __name__ == "__main__":
    time_start = time.time()
    main()
    time_end = time.time()
    print('totally cost',time_end-time_start)
