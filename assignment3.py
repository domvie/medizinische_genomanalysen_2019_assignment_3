#! /usr/bin/env python3

import vcf
import myvariant
import httplib2

__author__ = 'Dominic Viehböck'


##
##
## Aim of this assignment is to annotate the variants with various attributes
## We will use the API provided by "myvariant.info" - more information here: https://docs.myvariant.info
## NOTE NOTE! - check here for hg38 - https://myvariant.info/faq
## 1) Annotate the first 900 variants in the VCF file
## 2) Store the result in a data structure (not in a database)
## 3) Use the data structure to answer the questions
##
## 4) View the VCF in a browser
##

class Assignment3:
    
    def __init__(self):
        ## Check if pyvcf is installed
        print("PyVCF version: %s" % vcf.VERSION)
        
        ## Call annotate_vcf_file here
        self.vcf_path = "chr16.vcf"
        self.hits = self.annotate_vcf_file()
        self.genelist = []


    def annotate_vcf_file(self):
        '''
        - Annotate the VCF file using the following example code (for 1 variant)
        - Iterate of the variants (use first 900)
        - Store the result in a data structure
        :return:
        '''    
        print("TODO")
                
        ##
        ## Example loop
        ##
        
        ## Build the connection
        h = httplib2.Http()
        headers = {'content-type': 'application/x-www-form-urlencoded'}
                
        params_pos = []  # List of variant positions
        with open(self.vcf_path) as my_vcf_fh:
            vcf_reader = vcf.Reader(my_vcf_fh)
            for counter, record in enumerate(vcf_reader):
                params_pos.append(record.CHROM + ":g." + str(record.POS) + record.REF + ">" + str(record.ALT[0]))
                
                if counter >= 899:
                    break
        
        ## Build the parameters using the list we just built
        params = 'ids=' + ",".join(params_pos) + '&hg38=true'
        
        ## Perform annotation
        res, con = h.request('http://myvariant.info/v1/variant', 'POST', params, headers=headers)
        annotation_result = con.decode('utf-8')

        # Alternative way with myvariant package (normal http request returns string not list/dict!
        mv = myvariant.MyVariantInfo()

        annotation_result = mv.getvariants(params)

        ## TODO now do something with the 'annotation_result'
        reslist = []
        for result in annotation_result:
            try:
                if result['notfound']:
                    pass
                else:
                    reslist.append(result)
            except:
                reslist.append(result)
        ##
        ## End example code
        ##
        
        return reslist  ## return the data structure here
    
    
    def get_list_of_genes(self):
        '''
        Print the name of genes in the annotation data set
        :return:
        '''
        print("List of genes: ")
        for hit in self.hits:
            try:
                if hit['cadd']['gene']:
                    #print(hit['cadd']['gene']['genename'])
                    self.genelist.append(hit['cadd']['gene']['genename'])
            except:
                pass
        print(self.genelist)
    
    def get_num_variants_modifier(self):
        '''
        Print the number of variants with putative_impact "MODIFIER"
        :return:
        '''
        cnt = 0
        for hit in self.hits:
            if 'snpeff' in hit:
                key, value = "putative_impact", "MODIFIER"
                if key in hit['snpeff']['ann'] and value == hit['snpeff']['ann']['putative_impact']:
                    cnt += 1

        print("Num. of variants modifiers: ", cnt)
    
    def get_num_variants_with_mutationtaster_annotation(self):
        '''
        Print the number of variants with a 'mutationtaster' annotation
        :return:
        '''
        cnt = 0
        for hit in self.hits:
            try:
                if hit['dbnsfp']['mutationtaster']:
                    cnt += 1
            except:
                pass
        print("Num. variants with mutationtaster annotation: ", cnt)
    
    def get_num_variants_non_synonymous(self):
        '''
        Print the number of variants with 'consequence' 'NON_SYNONYMOUS'
        :return:
        '''
        cnt = 0
        for hit in self.hits:
            try:
                if 'cadd' in hit:
                    key, value = "consequence", "NON_SYNONYMOUS"
                    if key in hit['cadd'] and value == hit['cadd']['consequence']:
                        cnt += 1
            except:
                pass

        print("Num. of non synonymous variants: ", cnt)
    
    def view_vcf_in_browser(self):
        '''
        - Open a browser and go to https://vcf.iobio.io/
        - Upload the VCF file and investigate the details
        :return:
        '''
   
        ## Document the final URL here
        print("The .vcf file was compressed with bgzip and a tabix index created with tabix -p vcf ch16.vcf")
        print("The resulting files were uploaded to https://vcf.iobio.io/")
        print("The final URL: https://vcf.iobio.io/?species=Human&build=GRCh38")
            
    
    def print_summary(self):
        self.get_list_of_genes()
        self.get_num_variants_modifier()
        self.get_num_variants_with_mutationtaster_annotation()
        self.get_num_variants_non_synonymous()
        self.view_vcf_in_browser()


def main():
    print("Assignment 3")
    assignment3 = Assignment3()
    assignment3.print_summary()
    print("Done with assignment 3")


if __name__ == '__main__':
    print(__author__)
    main()

    



