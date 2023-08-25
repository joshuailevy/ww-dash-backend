# data='samples_names.txt'
data='samp_names.txt'
#skip the header row. 
# tail +2 wastewater_ncbi.csv | cut -d, -f1 > $data

while read sample; do

if [ ! -f "vars/${sample}.tsv" ]; then
	echo $sample
	bedfile=$(python -c "from get_ncbi_metadata import *;pull_sample_bed('${sample}')")
	echo $bedfile
	bedfile="bedfiles/${bedfile}.bed"
	fasterq-dump --split-files ${sample}

	minimap2 -ax sr data/NC_045512_Hu-1.fasta ${sample}_1.fastq ${sample}_2.fastq | samtools view -bS - > "bams/${sample}.bam"
	rm ${sample}_1.fastq ${sample}_2.fastq

	samtools sort -o "bams/${sample}.sorted.bam" "bams/${sample}.bam"
	samtools index "bams/${sample}.sorted.bam" 
	ivar trim -x 4 -e -m 80 -i "bams/${sample}.sorted.bam" -b ${bedfile} -p "trimmed/${sample}.trimmed"

	rm bams/*

	samtools sort -o "trimmed/${sample}.trimmed.sorted.bam" "trimmed/${sample}.trimmed.bam"
	samtools index "trimmed/${sample}.trimmed.sorted.bam"
	freyja variants "trimmed/${sample}.trimmed.sorted.bam" --variants "vars/${sample}.tsv" --depths "depths/${sample}.depth" --ref data/NC_045512_Hu-1.fasta --annot data/NC_045512_Hu-1.gff
	freyja demix "vars/${sample}.tsv" "depths/${sample}.depth" --output "outputs/${sample}.demixed" --barcodes usher_barcodes_with_gisaid.csv

	minSite=22556
	maxSite=23156
	freyja covariants trimmed/${sample}.trimmed.sorted.bam $minSite $maxSite --min_count 10 --gff-file data/NC_045512_Hu-1.gff --ref-genome  data/NC_045512_Hu-1.fasta --output covariants/${sample}.covariants.tsv 
	rm trimmed/*
fi

done < $data
