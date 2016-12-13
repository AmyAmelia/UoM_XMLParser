# Foxy Parser an LRG file parser
A .xml file parser developed to extract exonic information from a Locus Reference Genomic file (LRG file), outputting a .tsv file for each transcript.   
Further information regarding LRG files and options to download LRG files may be found at http://www.lrg-sequence.org/

## Authors
FoxyParser was written by Amy Slater and Matthew Wherlock (2016)

## Usage
### Requirements
To run FoxyParser you will need:
* Python version 3.5 
  
With the following python packages installed:
* xml.etree.ElementTree
* pandas
*	warnings
*	os
* glob

### Instructions
TO DO: Add in instructions  

## Output
Output is as .tsv format.  
Outputted fields are parsed to a subdirectory generated by the parser within the current work directory. Subdirectories are named as input LRG ID plus ‘output’ as a suffix e.g. LRG_62_output   
A separate .tsv file is generated for each transcript identified in the input LRG file. Transcript number is added as a suffix to the .tsv file name to permit identification. e.g. LRG_62.xml_t1.tsv  
FoxyParser extracts the LRG ID, gene symbol, chromosome, strand direction, transcript number, the exome co-ordinates for genome builds GRC37 and GRCh38, exome length and the exonic sequence for each transcript of the gene.   
In the output .tsv file LRG ID, gene symbol, chromosome, strand direction and transcript number are displayed as a header. The exome co-ordinates for genome builds GRC37 and GRCh38, exome length and exonic sequence are displayed in tab separated format below the header.  

## Testing
TO DO: Add in testing criteria/ conditions.   
  
The outputted exonic locations and sequence for genome builds GRC37 and GRCh38 were confirmed by comparison to UCSC (https://genome.ucsc.edu/) for each genome build for LRG_62 (_FOXP3_) and LRG_517 (_RB1_).

## Limitations
Identified limitations of FoxyParser include:

*	Not currently accounting for sequence differences between genome builds. This limitation should be addressed in future iterations of FoxyParser. 
*	Output file currently does not include:
  *	HGNC accession number
  *	Information regarding intronic length or sequence
  *	Information regarding transcripts RefSeq ID, length or sequence
  *	Information regarding the protein. Including ID number, length or sequence
*	Glob module cannot identify and list files located within the ‘Downloads’ file. Workaround: ensure FoxyParser and downloaded LRG files are not located within the ‘Downloads’ folder prior to running the tool. 


## Further Development
This code does not currently account for sequence variations between genome builds GRC37 and GRCh38. This information is present within the LRG.xml file and therefore could be extracted and included within the tsv output in future iterations of the parser.  
Further development should also focus upon extracting and displaying the omitted genetic information listed in point two of the limitations sections.   
Further functionality could also be added by permitting users to input a value of flanking intronic bases to be included in the sequence output. Including flanking intronic regions of exons could permit investigation of splice sites. Currently the exonic sequence is split on the intron:exon boundary using the exome start and stop position within the function def add_sequence().   

## Licencing 
See separate licencing documentation. 

## Parser naming
FoxyParser was named following original testing on gene _FOXP3_
