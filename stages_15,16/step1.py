import glob, os
import subprocess
import tempfile
from classes.region import Region
from classes.region import ChromosomeSet
from classes.region import Population
from classes.region import MafftFormatter

headers_set = set()
header_dictionary = {}

def read_all_headers(lines):
    sequences = {}

    current_header = ""
    current_sequence = ""

    # clean unwanted characters
    characters = ["<INS:ME:ALU>","<INS:ME:LINE1>","<DEL>","LINE1>","<CN0>","<INS:ME:","<INS:ME:>", "<INS:M", "E:"]

    for line in lines:
        for character in characters:
            line = line.replace(character,"")

        line = line.replace("\n","")

        # Header
        if ">" in line:

            # Base case
            if current_sequence != "":
                # current_sequence += "\n"
                sequences[current_header] = current_sequence

            current_header = line
            headers_set.add(current_header)
            current_sequence = ""
            # current_sequence += line + " "
        else:
        # Sequence
            current_sequence += line

    # Add last sequence
    sequences[current_header] = current_sequence

    # Clean all data again before returning
    for key in sequences.keys():
        sequence = sequences[key]
        for character in characters:
            sequence = sequence.replace(character,"")
        sequences[key] = sequence

    # Returns array of headers with sequenes
    return sequences

def read_all_region_less_headers(lines):
    sequences = []

    current_header = ""
    current_sequence = ""

    for line in lines:
        line = line.replace("\n","")
        line = line.replace(" ","")

        # Header
        if ">" in line:

            # Base case
            if current_sequence != "":
                # current_sequence += "\n"
                sequences.append(current_sequence)

            current_header = line
            current_sequence = ""
            # current_sequence += line + " "
        else:
        # Sequence
            current_sequence += line

    # Add last sequence
    sequences.append(current_sequence)

    return sequences

# Start main code
input_directory = "/Users/hasmitapatel/Desktop/block_creation/input/variant/"
output_directory = "/Users/hasmitapatel/Desktop/block_creation/output/"
reference_directory = "/Users/hasmitapatel/Desktop/block_creation/input/reference/"
reference_chimp_directory = "/Users/hasmitapatel/Desktop/block_creation/input/reference_chimps/"

os.chdir(input_directory)

for folder in glob.glob("*"):
    os.chdir(input_directory + folder)

    # Make new header dictionary
    header_dictionary[folder] = {}
    species_dictionary = header_dictionary[folder]

    line_count = 0
    header_count = 0

    for file in glob.glob("*"):
        f  = open(file, "r")
        # print file
        lines = f.readlines()
        sequences = read_all_headers(lines)
        # print len(lines)
        # print len(headers)

        for header in sequences.keys():
            species_dictionary[header] = sequences[header]
            #print header
            #print sequences[header]

        line_count += len(lines)
        header_count += len(sequences)

    #print folder
    #print "total lines : ", line_count
    #print "total headers : ", header_count
    #print "total headers in dictionary: ", len(species_dictionary.keys())

population_dictionary = {}

# Variant files
for population_key in header_dictionary.keys():
    population = Population(population_key)
    for header_key in header_dictionary[population_key]:
        sequence = header_dictionary[population_key][header_key]
        temp_key = header_key
        temp_key = temp_key.replace(">","")
        chromosome = temp_key.split(":")[0]
        region_range = temp_key.split(":")[1].split("-")
        start_range = region_range[0]
        end_range = region_range[1]
        region = Region(chromosome, start_range, end_range, sequence)
        chromosome_int = int(chromosome)
        chromosome_set =  population.get_chromosome_set_by_chromoesome(chromosome_int)
        chromosome_set.add_region(region)

    population.sort_all_chromosome_sets()

    population_dictionary[population_key] = population

# Reference files
reference_population_dictionary = {}
os.chdir(reference_directory)

for file in glob.glob("*"):
    f = open(file,"r")
    population_name = file.replace(".fa","")
    lines = f.readlines()
    sequences = read_all_headers(lines)
    population = Population("reference_"+population_name)
    for key in sequences:
        sequence = sequences[key]
        temp_key = key
        temp_key = temp_key.replace(">","")
        chromosome = temp_key.split(":")[0]
        region_range = temp_key.split(":")[1].split("-")
        start_range = region_range[0]
        end_range = region_range[1]
        region = Region(chromosome, start_range, end_range, sequence)
        chromosome_int = int(chromosome)
        chromosome_set =  population.get_chromosome_set_by_chromoesome(chromosome_int)
        chromosome_set.add_region(region)

    population.sort_all_chromosome_sets()

    reference_population_dictionary[population_name] = population

# for population in reference_population_dictionary.keys():
#     print len(reference_population_dictionary[population].get_all_sorted_regions())


for key in population_dictionary.keys():
    missing_a, missing_b = Population.compare_populations(population_dictionary[key], reference_population_dictionary[key] )
    for missing in missing_a:
        for region in reference_population_dictionary[key].get_all_sorted_regions():
            if region.joint_header_match(missing) == True:
                chromosome_set = population_dictionary[key].get_chromosome_set_by_chromoesome(int(region.chromosome))
                chromosome_set.add_region(region)

    if len(missing_b) != 0:
        print "Sequences missing in reference population"

    population_dictionary[key].sort_all_chromosome_sets()
    # print len(population_dictionary[key].get_all_sorted_regions())

# population_dictionary now has populations that contain variant and reference regions where missing

# Reference chimp files
reference_population_dictionary = {}
os.chdir(reference_chimp_directory)
for file in glob.glob("*"):
    f = open(file,"r")
    population_name = file.replace(".fa","")
    lines = f.readlines()
    sequences = read_all_headers(lines)
    population = Population(population_name)
    for key in sequences:
        sequence = sequences[key]
        temp_key = key
        temp_key = temp_key.replace(">","")
        chromosome = temp_key.split(":")[0]
        region_range = temp_key.split(":")[1].split("-")
        start_range = region_range[0]
        end_range = region_range[1]
        region = Region(chromosome, start_range, end_range, sequence)
        chromosome_int = int(chromosome)
        chromosome_set =  population.get_chromosome_set_by_chromoesome(chromosome_int)
        chromosome_set.add_region(region)

    population.sort_all_chromosome_sets()
    population_dictionary[population_name] = population

#print len(population_dictionary["chimp"].get_all_sorted_regions())
#for region in population_dictionary["chimp"].get_all_sorted_regions():
#    print region.sequence

#for key in population_dictionary.keys():
#    print key
#    print population_dictionary[key].get_all_sorted_regions()[3959].sequence

# Crafting final .fa file
os.chdir(output_directory)
f = open("output.txt","w+")

populations_for_mafft = []
key_ordering = ["yoruba", "spain", "han_chinese", "peru", "chimp", "gorilla", "orangutan"]
mafft_key_dictionary = { "yoruba": ">YRI_AFR_NA18505", "spain":">IBS_EUR_HG01504", "han_chinese":">EAS_NA18531", "peru":">AMR_HG01566", "chimp":">ch", "gorilla":">gor", "orangutan":">orang" }
for key in key_ordering:
    populations_for_mafft.append(population_dictionary[key]);

# Assuming first population region count is the same as all others
region_count = len(populations_for_mafft[0].get_all_sorted_regions())
for i in range(0,region_count):
    print i
    prefixed_regions = []
    sorted_regions = populations_for_mafft[0].get_all_sorted_regions()
    region = sorted_regions[i]

    population_count = 0
    population_regions = []
    for population in populations_for_mafft:
        found_region = population.get_region_by_set_and_range(region.chromosome, region.start_range, region.end_range)
        if found_region is None:
            print "none for " + population.population_name
            continue
        print found_region.joint_header_information()
        population_count = population_count + 1
        found_region_hash = { 'population_name': population.population_name, 'sequence': found_region.sequence + "\n" }
        population_regions.append(found_region_hash)

    # Do dynamic prefix
    for found_region_hash in population_regions:
        sequence = found_region_hash['sequence']
        population_name = found_region_hash['population_name']
        population = population_dictionary[population_name]
        prefix = mafft_key_dictionary[population_name] + "^" + str(populations_for_mafft.index(population) + 1) + "\n"
        #print [prefix, sequence]
        prefixed_regions.append([prefix, sequence])

    mafft_formatter = MafftFormatter(prefixed_regions)
    output_file,output_file_path = mafft_formatter.run_mafft_on_prefixed_regions()
    lines = output_file.readlines()
    sequences = read_all_region_less_headers(lines)
    headers = []
    for line in lines:
        if "^" in line:
            line = line.replace("\n","")
            line = line.replace(">","")
            headers.append(line)

    #print headers
    #print sequences

    # Assuming first sequence length matches all
    try:
        sequences_count = len(sequences)
        sequence_length = len(sequences[1].replace("\n",""))
        populations_count = len(populations_for_mafft)
        header = str(population_count) + " " + str(sequence_length) + "\n"
        f.write(header)

        for i in range(0,sequences_count):
            f.write(headers[i] + "  ")
            f.write(sequences[i] + "\n")
        f.write("\n")
    except:
        print "sequences error"
        print sequences
