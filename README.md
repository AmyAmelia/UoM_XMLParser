# Foxy Parser an LRG file parser
A .xml file parser developed to extract exonic information from a Locus Reference Genomic file (LRG file), outputting a .tsv file for each transcript.   
Further information regarding LRG files and options to download LRG files may be found at http://www.lrg-sequence.org/

## Authors
FoxyParser was written by Amy Slater and Matthew Wherlock (2016)

## Usage
### Requirements
To run FoxyParser you will need:
* Python version 3.5 (preferred) or Python 2.7

With the following python packages installed:
* future
* xml.etree.ElementTree
* pandas
* warnings
* os
* glob
* sys

### Instructions
TO DO: Add in instructions  and assumptions

## Output
Output is as .tsv format.  
Outputted fields are parsed to a subdirectory generated by the parser within the current work directory. Subdirectories are named as input LRG ID plus ‘output’ as a suffix e.g. `LRG_62_output/`     
A separate .tsv file is generated for each transcript identified in the input LRG file. Transcript number is added as a suffix to the .tsv file name to permit identification. e.g. `LRG_62.xml_t1.tsv`  
FoxyParser extracts the LRG ID, gene symbol, chromosome, strand direction, transcript number, the exome co-ordinates for genome builds GRC37 and GRCh38, exome length and the exonic sequence for each transcript of the gene.   
In the output .tsv file LRG ID, gene symbol, chromosome, strand direction and transcript number are displayed as a header. The exome co-ordinates for genome builds GRC37 and GRCh38, exome length and exonic sequence are displayed in tab separated format below the header.     
Examples of output are located in `Example_outputs/` directory for genes _FOXP3, NF1, BRCA1_ and _RB1_

## Testing

For future development, a series of unit tests are included in the `test/` folder.  Running the testing suite requires the pytest module to be installed.

For installation:
>`pip install -U pytest`

To run the unit tests, simply type `pytest` from the root directory of this package.

Non .xml file and non LRG files where used in testing to assertain correct file selection, copies of these files are located in  `test_files/` directory.  

LRG files tested on the Parser are located in `LRG_files/` directory, including sigle and multiple transcript genes.  
  
The outputted exonic locations and sequence for genome builds GRC37 and GRCh38 were confirmed by comparison to UCSC (https://genome.ucsc.edu/) for each genome build for LRG 62 _(FOXP3)_ and LRG 517 _(RB1)_.

## Limitations
Identified limitations of FoxyParser include:
*	Not currently accounting for sequence differences between genome builds. This limitation should be addressed in future iterations of FoxyParser.  
*	Output file currently does not include:
  *	HGNC accession number
  *	Information regarding intronic length or sequence
  *	Information regarding transcripts RefSeq ID, length or sequence
  *	Information regarding the protein. Including ID number, length or sequence
*	Glob module cannot identify and list files located within the ‘Downloads’ file. Workaround: ensure FoxyParser and downloaded LRG files are not located within the ‘Downloads’ folder prior to running the tool. 
* Does not display to the user the LRG_ID and gene symbol of the .xml files identified in a directory. 

## Assumptions
* LRG files are down loaded locally.
* LRG files are not located within the 'download' directory
* User is aware of correct HGNC nomenclature or LRG ID for gene of intrest. 

## Further Development
This code does not currently account for sequence variations between genome builds GRC37 and GRCh38. This information is present within the LRG.xml file and therefore could be extracted and included within the tsv output in future iterations of the parser.  
Further development should also focus upon extracting and displaying the omitted genetic information listed in point two of the limitations sections.   
Further functionality could also be added by permitting users to input a value of flanking intronic bases to be included in the sequence output. Including flanking intronic regions of exons could permit investigation of splice sites. Currently the exonic sequence is split on the intron:exon boundary using the exome start and stop position within the function def add_sequence().   

## Licencing 
See separate licencing documentation. 

## Parser naming
FoxyParser was named following original development and testing on gene _FOXP3_
