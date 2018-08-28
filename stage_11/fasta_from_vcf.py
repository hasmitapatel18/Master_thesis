with open("/Users/hasmitapatel/Desktop/mres/chromosome_bed/chr1.bed")as f:
    for line in f:
        L = line.strip().split()
        r= L[0].replace("chr","")
        m= r + ":" + L[1] + "-" + L[2]
        #print L[3]
        #print m
        command = "/usr/local/bin/samtools faidx /Users/hasmitapatel/Desktop/human_g1k_v37.fasta " + m + " | /Users/hasmitapatel/bin/vcftools_0.1.13/bin/vcf-consensus /Volumes/Maxtor/vcf_1000_genomes/bgzipped/reg3/test_sorted.vcf.gz >> /Volumes/Maxtor/vcf_1000_genomes/bgzipped/reg3/all_region_yoruba.fa"

        print command
        subprocess.call([command],shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        # print m
