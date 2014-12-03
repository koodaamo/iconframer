#!/bin/bash

HELP="\nUsage:\n\n topdf svgdir pdfdir \n topdf -h\n"

if [ "$1" == -h ]
  then
    echo -e $HELP
    exit
fi

if [ "$2" == "" ]
  then
    echo -e $HELP; exit
  else
    echo -e "\nStarting conversion\n"
fi

echo " - reading SVG files from $1"
echo -e " - writing PDF files to $2\n"

shopt -s nullglob
for fullfile in $1/*.svg
do
  filename=$(basename "$fullfile")
  extension="${filename##*.}"
  filename="${filename%.*}"
  outfullfile=$1/"$filename".pdf
  rsvg-convert $fullfile -f pdf > $outfullfile #echo $outfullname #pdftk "$f" output "output.$f" user_pw "YOURPASSWORD-HERE"
  echo " ... converted '$filename'."
done
echo
shopt -u nullglob
