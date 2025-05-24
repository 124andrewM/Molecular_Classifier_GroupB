#!/usr/bin/perl

# Example usage:
# perl log_extractor.pl <input_directory> <output_directory>

# Description:
# This script takes in a directory of log files and extracts the spatial coordinates for
# each, saving the data to corresponding CSV files in the specified output directory.
# Modified from a script provided by Professor Amir Karton ("log_script_single.pl").

# A list of atomic symbols, as found in QM9 Gaussian log files, for conversion to atomic number.
@at_symbols = (
	      'X', 'H',                                'He',
	      'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne',
	      'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar',
	      'K', 'Ca',
	      'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn',
	      'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr',
	      'Rb', 'Sr',
	      'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd',
	      'In', 'Sn', 'Sb', 'Te', 'I', 'Xe',
               'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd',
               'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W',
               'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po',
               'At', 'Rn'
	      );

# Verify and store command line arguments
die "Usage: perl $0 <input_directory> <output_directory>\n" if @ARGV != 2;
$input_dir = $ARGV[0];
$output_dir = $ARGV[1];

# Create output directory (won't modify/delete if already exists)
mkdir($output_dir);

# Open the input directory and access the log files within in ascending order
opendir(DIR, $input_dir) || die "Can't open $input_dir: $!\n";
my @files = sort(readdir(DIR));
shift @files;
shift @files;
while (my $file = shift @files) {
    
    # Open log file and iterate over every individual line, skipping irrelevant content.
    open (FILE, "$input_dir/$file") || die ("Can't Open $file: $!\n");
    # Each log file contains repeated outputs. The data extracted here will be overriden by subsequent
    # iterations so that only the final output/repetition is kept.
    while (<FILE>){
    	# Atom coordinates are in a table called either "Standard orientation" or "Input orientation".
        if (/^.*[Standard|Input] orientation:\s*$/)     {
	    $natoms=0;  
	    $line=<FILE>;
	    $line=<FILE>;
	    $line=<FILE>;
	    # The format of the table row contents can vary slightly.
            @check=split(/\s+/,$line);
            if (@check[3] =~ /type/i) {
                $format=1;
            }
            else {
                $format=2;
            }
	    $line=<FILE>;
	    while($line =<FILE>) 	{
	        last if($line =~ /^\s*------------------+\s*$/);
	        $natoms=$natoms+1;
	        $lines[$natoms]=$line;
	    }
        }
    }
    
    # Open/create the output CSV file. Will override existing files with the same name.
    $output_file = "$output_dir/" . $file . ".csv";
    open (OUTFILE, ">", $output_file) || die ("Can't Open $output_file: $!\n");
    
    # Write the position information to the output file. Requires slightly different regex depending on the
    # format of the final coordinate table in the log file, as determined earlier.
    if ($format == 1) {
        for($i=1;$i<=$natoms;$i=$i+1) {
            $lines[$i] =~ /^\s*(\d+)\s*(\d+)\s*\d\s*(-?\d*\.\d+)\s*(-?\d*\.\d+)\s*(-?\d*\.\d+)/;
            printf OUTFILE ("%s,%f,%f,%f\n",$at_symbols[$2],$3,$4,$5);
        }
    }
    elsif ($format == 2) {
        for($i=1;$i<=$natoms;$i=$i+1) {
            $lines[$i] =~ /^\s*(\d+)\s*(\d+)\s*(-?\d*\.\d+)\s*(-?\d*\.\d+)\s*(-?\d*\.\d+)/;
            printf OUTFILE ("%s,%f,%f,%f\n",$at_symbols[$2],$3,$4,$5);
        }
    }

    close(OUTFILE) or "Couldn't close $output_file";
}
closedir(DIR) || "Couldn't close $output_dir";
