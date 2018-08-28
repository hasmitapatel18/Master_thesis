count = 0
old_loci_file_path = "/Users/hasmitapatel/Desktop/chimp/hg19liftover.bed"
chimp_loci_file_path = "/Users/hasmitapatel/Desktop/chimp/gor3hg19.bed"
old_loci_new_seq_output_path = "/Users/hasmitapatel/Desktop/chimp/old_loci_new_seq.fa"

replacement_loci_lines = {}
chimp_sequences = {}
current_sequence = ""
current_chimp = None

with open("/Users/hasmitapatel/Desktop/chimp/gorseq.fa") as f:
        for line in f:
            if ">" in line:
                if current_chimp != None:
                    current_chimp['sequence'] = current_sequence
                    chimp_sequences[current_line] = current_chimp

                # Start of sequence
                line = line.replace(">","")
                line = line.strip()
                line_split = line.split(":")
                chromosome = line_split[0]
                ranges = line_split[1]
                start_range = ranges.split("-")[0]
                end_range = ranges.split("-")[1]
                temp_dictionary = { 'chromosome': chromosome, 'start_range': start_range, 'end_range': end_range, 'sequence': ""}
                current_sequence = ""
                current_chimp = temp_dictionary
                current_line = line
            else:
                # End of sequence
                current_sequence = current_sequence + line

# print len(chimp_sequences)
# print chimp_sequences.keys()
with open("/Users/hasmitapatel/Desktop/chimp/gorseq.fa") as f:
        for line in f:
            if ">" not in line:
                continue
            #print line
            count = count + 1

            line = line.replace(">","")
            line = line.strip()
            line_split = line.split(":")
            chromosome = line_split[0]
            ranges = line_split[1]
            start_range = ranges.split("-")[0]
            end_range = ranges.split("-")[1]

            hat_value = None
            # open file and find chimp loci and h^ value
            chimp_loci_file = open(chimp_loci_file_path, "r")
            for chimp_loci_line in chimp_loci_file:
                split_chimp_loci_line = chimp_loci_line.strip().strip('\n').split()
                chimp_chromosome = split_chimp_loci_line[0].replace("chr","")
                chimp_start_range = split_chimp_loci_line[1]
                chimp_end_range = split_chimp_loci_line[2]
                chimp_hat_value = split_chimp_loci_line[3]

                if (start_range == chimp_start_range and end_range == chimp_end_range and chromosome == chimp_chromosome ):
                    hat_value = chimp_hat_value
                    break




            # open file and find old loci
            old_loci_file = open(old_loci_file_path, "r")
            for old_loci_line in old_loci_file:
                old_loci_line_split = old_loci_line.strip().strip('\n').split()
                old_loci_hat_choromosome = old_loci_line_split[0].replace("chr","")
                old_loci_start_range = old_loci_line_split[1]
                old_loci_end_range = old_loci_line_split[2]
                old_loci_hat_value = old_loci_line_split[3]

                if hat_value != old_loci_hat_value:
                    continue

                #print "old loci"
                #print old_loci_line
                replace_loci_line = ">" + old_loci_hat_choromosome + ":" + old_loci_start_range + "-" + old_loci_end_range
                replacement_loci_lines[line] = replace_loci_line
                # print replace_loci_line

            old_loci_file.close()


print len(replacement_loci_lines)

output_file = open(old_loci_new_seq_output_path,"w")
for key in replacement_loci_lines.keys():
    header = replacement_loci_lines[key]
    chimp_sequence = chimp_sequences[key]
    output_file.write(header)
    output_file.write("\n")
    output_file.write(chimp_sequence['sequence'])

output_file.close()
