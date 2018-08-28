import glob, os
import subprocess

os.chdir("/Users/hasmitapatel/Desktop/yoruba_NA18505/hg19_bamfiles")
for files in glob.glob("*.bam"):
    print files
    subprocess.call(["/usr/local/bin/bcftools mpileup -Ou -f /Users/hasmitapatel/Desktop/human_g1k_v37.fasta " + files + " > /Users/hasmitapatel/Desktop/yoruba_NA18505/yoruba.bcf"],shell=True)
