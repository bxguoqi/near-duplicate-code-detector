import argparse
def main():
    '''
    Usage:
          CloneDetectorCli [options] (--dir=<folder> | --input=<file>) <output-file-prefix>

        Options:
          -h --help                      Show this screen.
          --dir=<path>                   Directory where .jsonl.gz files live.
          --input=<path>                 The path to the input .jsonl.gz file.
          --id-fields=<fields>           A colon (:)-separated list of names of fields that form the identity of each entry [default: filename].
          --tokens-field=<name>          The name of the field containing the tokens of the code [default: tokens].
          --key-jaccard-threshold=<val>  The Jaccard similarity threshold for token-sets [default: 0.8].
          --jaccard-threshold=<val>      The Jaccard similarity threshold for token multisets [default: 0.7].
    '''
    parser = argparse.ArgumentParser()
    ## Required parameters
    parser.add_argument("--dir", default=None, type=str, required=True,
                        help="Directory where .jsonl.gz files live.")
    parser.add_argument("--key-jaccard-threshold", default=0.8,
                        help="The Jaccard similarity threshold for token-sets [default: 0.8].")
    parser.add_argument("--jaccard-threshold", default=0.7,
                        help="The Jaccard similarity threshold for token multisets [default: 0.7].")
