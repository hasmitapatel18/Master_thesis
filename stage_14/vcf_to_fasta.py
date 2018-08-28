import subprocess

with open("~/Desktop/mres/hg19_best.bed")as f:
    for line in f:
        L = line.strip().split()
        r= L[0].replace("chr","")
        m= r + ":" + L[1] + "-" + L[2]
        print L[3]
        print m
        subprocess.call(["/usr/local/bin/samtools faidx /Users/hasmitapatel/Desktop/human_g1k_v37.fasta " + m + "| /usr/local/bin/bcftools consensus /Users/hasmitapatel/Desktop/yoruba_NA18505/consensus_fa/yoruba.vcf.gz >> /Users/hasmitapatel/Desktop/yoruba_NA18505/consensus_fa/yoruba.fa"],shell=True)
