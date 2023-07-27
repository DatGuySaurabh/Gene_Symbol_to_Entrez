import argparse
import gzip
import csv

def create_ste(input):
    ste = {}
    with gzip.open(input, 'rt') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            gene_id = row[1]
            symbols = row[2]
            synonyms = row[4]
            all_symbols = set(symbols.split('|'))
            all_symbols.update(synonyms.split('|'))
            for symbol in all_symbols:
                ste[symbol] = gene_id
    return ste

def replace_symbols_with_entrez(gmt_input, ste):
    new_gmt_lines = []
    with open(gmt_input, 'r') as f:
        for line in f:
            pathway_info, *symbols = line.strip().split('\t')
            entrez_ids = [ste.get(symbol, symbol) for symbol in symbols]
            new_line = '\t'.join([pathway_info] + entrez_ids)
            new_gmt_lines.append(new_line)
    return new_gmt_lines

def write_new_gmt_file(gmt_output, new_gmt_lines):
    with open(gmt_output, 'w') as f:
        f.write('\n'.join(new_gmt_lines))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("gene_info_file")
    parser.add_argument("gmt_file")
    parser.add_argument("output_file")
    args = parser.parse_args()

    ste = create_ste(args.gene_info_file)
    new_gmt_lines = replace_symbols_with_entrez(args.gmt_file, ste)
    write_new_gmt_file(args.output_file, new_gmt_lines)

if __name__ == '__main__':
    main()
