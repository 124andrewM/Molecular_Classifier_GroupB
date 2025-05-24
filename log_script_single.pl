#!/usr/bin/perl


$input_file = $ARGV[0];


@at_symbols = (
	      'X', 'H ',                                'He',
	      'Li', 'Be', 'B ', 'C ', 'N ', 'O ', 'F ', 'Ne',
	      'Na', 'Mg', 'Al', 'Si', 'P ', 'S ', 'Cl', 'Ar',
	      'K ', 'Ca',
	      'Sc', 'Ti', 'V ', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn',
	      'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr',
	      'Rb', 'Sr',
	      'Y ', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd',
	      'In', 'Sn', 'Sb', 'Te', 'I ', 'Xe',
               'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd',
               'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W ',
               'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po',
               'At', 'Rn'
	      );
open (INPUT, "<$input_file")||die ("Can't Open $input_file: $!\n");
while (<INPUT>){
    if (/^.*[Standard|Input] orientation:\s*$/)     {
	$natoms=0;  
	$line=<INPUT>;
	$line=<INPUT>;
	$line=<INPUT>;
        @check=split(/\s+/,$line);
        if (@check[3] =~ /type/i) {
            $format=1;
        }
        else {
            $format=2;
        }
	$line=<INPUT>;
	while($line =<INPUT>) 	{
	    last if($line =~ /^\s*------------------+\s*$/);
	    $natoms=$natoms+1;
	    $lines[$natoms]=$line;
	}
    }
}
#print ("------------------------------------------\n");
if ($format == 1) {
    for($i=1;$i<=$natoms;$i=$i+1) {
        $lines[$i] =~ /^\s*(\d+)\s*(\d+)\s*\d\s*(-?\d*\.\d+)\s*(-?\d*\.\d+)\s*(-?\d*\.\d+)/;
        printf ("%-5s %11f %11f %11f \n",$at_symbols[$2],$3,$4,$5);
    }
}
elsif ($format == 2) {
    for($i=1;$i<=$natoms;$i=$i+1) {
        $lines[$i] =~ /^\s*(\d+)\s*(\d+)\s*(-?\d*\.\d+)\s*(-?\d*\.\d+)\s*(-?\d*\.\d+)/;
        printf ("%-5s %11f %11f %11f \n",$at_symbols[$2],$3,$4,$5);
    }
}
#print ("\n")
#print ("------------------------------------------\n")