import subprocess

count = 0
output_file_path = "/Users/hasmitapatel/Desktop/chimp/pongoseq.fa"
output_file  = open(output_file_path, "w")

with open("/Users/hasmitapatel/Desktop/chimp/ponhg19.bed")as f:
    for line in f:
        L = line.strip().split()
        r = L[0].replace('_random', '')


        m = r + ":" + L[1] + "-" + L[2] + '\n'
        # subprocess.check_output(["/usr/local/bin/samtools faidx /Users/hasmitapatel/Desktop/chimp/panTro5.fa " + m + " >> /Users/hasmitapatel/Desktop/chimp/chimpseq.fa"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        command = "/usr/local/bin/samtools faidx /Users/hasmitapatel/Desktop/chimp/ponref.fa " + m + " >> /Users/hasmitapatel/Desktop/chimp/gorseq.fa"
        out = subprocess.check_output([command], shell=True)
        output_file.write(out)
