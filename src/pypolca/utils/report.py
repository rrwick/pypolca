import math
import sys
from pathlib import Path

from Bio import SeqIO


def create_report(vcf: Path, genome: Path, report_file: Path) -> None:
    with open(vcf, "r") as file:
        lines = file.readlines()

    # subs
    numsub = 0
    for line in lines:
        if not line.startswith("#"):
            fields = line.strip().split("\t")
            if len(fields[3]) == 1 and len(fields[4]) == 1:
                parts = fields[9].split(":")
                if int(parts[3]) == 0 and int(parts[5]) > 1:
                    # parts[3] is the number of reads supporting the ref
                    # parts[5] is the number of reads supporting the alternative
                    numsub += 1

    # index

    # Initialize variables
    nind = 0

    # Iterate through the lines and perform the desired operations
    for line in lines:
        # Skip lines starting with #
        if not line.startswith("#"):
            # Split the line using whitespace
            fields = line.split()
            # Check if the fourth and fifth fields have length greater than 1
            if len(fields[3]) > 1 or len(fields[4]) > 1:
                parts = fields[9].split(":")
                if int(parts[3]) == 0 and int(parts[5]) > 1:
                    nind += abs(len(fields[3]) - len(fields[4]))

    # Print the result

    total_size = 0
    for record in SeqIO.parse(genome, "fasta"):
        total_size += len(record.seq)

    numerr = numsub + nind
    erate = numerr / total_size

    qual = 100 - (erate) * 100

    qv = round(-10 * math.log10(erate + 0.0000000001), 2)

    with open(report_file, "w") as f:
        f.write("Stats BEFORE polishing:\n")
        f.write(f"Substitution Errors Found: {numsub}\n")
        f.write(f"Insertion/Deletion Errors Found: {nind}\n")
        f.write(f"Assembly Size: {total_size}\n")
        f.write(f"Consensus Quality Before Polishing: {qual}\n")
        f.write(f"Consensus QV Before Polishing: {qv}\n")