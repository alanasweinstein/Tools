#!/usr/bin/env python2.7
"""
Takes a regulon (.adj format) and a list of gene IDs (i.e. the first column of
an expression matrix) and removes from the regulon any genes not also appearing
in the list of genes. 

The entire line of the .adj file (regulator + regulated genes) is removed if:
1) the regulator does not appear in the list of genes; or
2) fewer than "cutoff number" genes remain as regulated genes after removal
of those not appearing in the list
 
Otherwise, only individual genes are removed.

For each line removed, prints the regulator to stderr.

example use:
filter_adj_regulon_genes.py --adj regulon.adj --expr_genes gene_ids.lst --cutoff_number 15
"""
# Author: Alana Weinstein
# April 2016

from __future__ import print_function, division
import argparse
import sys


def parse_arguments():
    """
    Defines, parses, checks, and returns command line arguments 
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--adj', help=""".adj file regulon""", 
                        type=argparse.FileType(mode='r'), required=True)
    parser.add_argument('--expr_genes', help="""list of gene IDs in expression 
                        matrix (first column of expr matrix)""", 
                        type=argparse.FileType(mode='r'), required=True)
    # parser.add_argument('--cutoff_percent', help="""remove entire row (regulator plus genes)
    # if percent (out of 100) of genes remaining is below this value AND # genes remaining is below
    # the cutoff_number argument""", type=int, required=False, default=30)
    
    parser.add_argument('--cutoff_number', help=""""remove entire row (regulator plus regulon genes)
    if number of genes remaining is below this value, defaults to 25""", type=int, required=False, default=25)
    args = parser.parse_args()

    return args


def main():
    """

    """
    # get commmand line args
    args = parse_arguments()
    
    adj_file = args.adj # open("UCSC_VIPER/pathways/extended_pathways_transcriptional.adj", "r")
   
    # this set isn't actually used in the script, but I was curious...
    adj_gene_set = set()    
    
    cutoff_number = args.cutoff_number
    #cutoff_percent = args.cutoff_percent
    
    expr_gene_file = args.expr_genes #open("stanford_batchK1-12.HUGO_only_genes.lst", 'r')
    expr_genes = [line.strip() for line in expr_gene_file]    
    
    # for each line, check that the regulator and other genes are in the
    # expression matrix gene set. if not, remove them, or remove the whole
    # line if the regulator isn't in the set or if too few genes remain
    for line in adj_file:
        
        line_list = line.strip().split()
        regulator_plus_gene_list = [x for x in line_list if x !="1.0"]
        regulator = regulator_plus_gene_list[0]
        
        if regulator not in expr_genes:
            # remove the whole regulator + regulon
            print("Skipped a line (regulator not in expr genes): ", 
                  line_list[0], file=sys.stderr)        
            continue
        
        gene_list = regulator_plus_gene_list[1:]
        list_size = len(gene_list)
        adj_gene_set.update(gene_list)
       
        how_many_to_remove= 0
        good_genes = []
        
        for gene in gene_list:
            if gene not in expr_genes:
                how_many_to_remove += 1
            else:
                good_genes.append(gene)
                
        #print("\n")
        #pdb.set_trace()
        #if (100-how_many_to_remove/list_size*100 < cutoff_percent) and (list_size-how_many_to_remove < cutoff_number):
        if (list_size-how_many_to_remove < cutoff_number):
            print("Skipped a line (too many removed): ", line_list[0], file=sys.stderr)
   
        else:
            # re-generate the new line of the .adj file with kept genes
            #genes_to_print = good_genes.insert(0, regulator)
            regulated_genes = "\t1.0\t".join(good_genes)
            print(regulator+"\t"+regulated_genes+"\t1.0")
    
            



if __name__ == "__main__":
    main()  