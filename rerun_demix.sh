for file in vars/*;
do
	fn="${file##*/}"
	sample="${fn%.tsv}"
	echo "${sample}"
	freyja demix "vars/${sample}.tsv" "depths/${sample}.depth" --output "outputs/${sample}.demixed" --barcodes usher_barcodes_with_gisaid.csv --eps 0.00001
done