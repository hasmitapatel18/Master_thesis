class Region:

   def __init__(self, chromosome, start_range, end_range, sequence):
      self.chromosome = chromosome
      self.start_range = start_range
      self.end_range = end_range
      self.sequence = sequence

   def print_info(self):
      print self.chromosome,self.start_range,self.end_range

   def joint_header_information(self):
       header_information = str(self.chromosome) + ":" + str(self.start_range) + "-" + str(self.end_range)
       return header_information

   def joint_header_match(self,header):
       header_information = str(self.chromosome) + ":" + str(self.start_range) + "-" + str(self.end_range)
       if header == header_information:
           return True
       else:
           return False

class ChromosomeSet:

   def __init__(self,chromosome_number):
       self.chromosome_number = chromosome_number
       self.regions = []
       self.sorted_regions = []

   def add_region(self,region):
       self.regions.append(region)

   def sort_regions(self):
       self.sorted_regions = sorted(self.regions, key=lambda region: int(region.start_range))

   def region_count(self):
       return len(self.regions)

class Population:

    def __init__(self,population_name):
        self.population_name = population_name
        self.chromosome_sets = []
        for i in range(1,23):
            chromosome_set = ChromosomeSet(i)
            self.chromosome_sets.append(chromosome_set)

    @staticmethod
    def compare_populations(population_a, population_b):
        #print "Start comparison : "
        #print "Comparison of ",population_a.population_name," against ",population_b.population_name

        population_a_sorted_regions = population_a.get_all_sorted_regions()
        population_a_dictionary = {}
        population_b_sorted_regions = population_b.get_all_sorted_regions()
        population_b_dictionary = {}

        for region in population_a_sorted_regions:
            header = region.joint_header_information()
            population_a_dictionary[header] = region

        for region in population_b_sorted_regions:
            header = region.joint_header_information()
            population_b_dictionary[header] = region

        missing_a = []
        missing_b = []

        # population a as lookup
        for key in population_b_dictionary.keys():
            try:
                region = population_a_dictionary[key]
            except :
                #print "Missing from ",population_a.population_name," : ", key
                missing_a.append(key)
                # print other_dictionary[key]

        for key in population_a_dictionary.keys():
            try:
                region = population_b_dictionary[key]
            except :
                #print "Missing from ",population_b.population_name," : ", key
                missing_b.append(key)
                # print other_dictionary[key]

        return missing_a, missing_b

    def get_chromosome_set_by_chromoesome(self,chromosome_number):
        for chromosome_set in self.chromosome_sets:
            if chromosome_set.chromosome_number == chromosome_number:
                return chromosome_set
        return None

    def get_all_sorted_regions(self):
        sorted_regions = []
        for chromosome_set in self.chromosome_sets:
            for region in chromosome_set.sorted_regions:
                sorted_regions.append(region)

        return sorted_regions

    def sort_all_chromosome_sets(self):
        for cs in self.chromosome_sets:
            cs.sort_regions()

    def get_region_by_set_and_range(self,chromosome_number,start_range,end_range):
        chromosome_number_str = int(chromosome_number)
        cs = self.get_chromosome_set_by_chromoesome(chromosome_number_str)
        for region in cs.regions:
            if(region.start_range == start_range and region.end_range == end_range):
                return region
        return None

class MafftFormatter:
   os = __import__('os')
   tf = __import__('tempfile')
   sp = __import__('subprocess')
   def __init__(self, prefixed_regions):
      self.prefixed_regions = prefixed_regions

   def run_mafft_on_prefixed_regions(self):
       file,path = self.write_to_temp_file()
       file.close()

       output_path = "/tmp/mafft_output"
       output_file = open(output_path,"w+")
       output_file.close()

       command = "/usr/local/bin/mafft " + format(path) + " > " + output_path

       FNULL = open(self.os.devnull, 'w')
       self.sp.call([command],shell=True,stdout=FNULL,stderr=FNULL)

       output_file = open(output_path,"r")

       return output_file,output_path

   def write_to_temp_file(self):
      path = "/tmp/mafft_input"
      file = open(path,"w+")
      for prefixed_region in self.prefixed_regions:
         file.write(prefixed_region[0])
         file.write(prefixed_region[1])
      return file,path
