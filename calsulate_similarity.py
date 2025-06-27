
import os
import subprocess
import csv
import itertools
from Bio import SeqIO


sample_dir = "./sample.path"         
ref_file = "rCRS.fasta"         
output_csv = "pairwise_differences.csv" 


sample_files = [os.path.join(sample_dir, f) for f in os.listdir(sample_dir) if f.endswith(".fasta")]
sample_names = [os.path.splitext(os.path.basename(f))[0] for f in sample_files]


def compare_sequences(seq1, seq2, ref_seq):
    diffs = 0
    for i in range(len(ref_seq)):
        base1 = seq1[i] if i < len(seq1) else '-'
        base2 = seq2[i] if i < len(seq2) else '-'
        if base1 != base2 and base1 not in ['N', '-'] and base2 not in ['N', '-']:
            diffs += 1
    return diffs


def align_and_count(file1, file2, ref_file):
    input_file = "input_tmp.fasta"
    output_file = "aligned_tmp.fasta"

   
    ref_record = next(SeqIO.parse(ref_file, "fasta"))
    ref_id = ref_record.id

   
    with open(input_file, "w") as out:
        for f in [file1, file2, ref_file]:
            for r in SeqIO.parse(f, "fasta"):
                SeqIO.write(r, out, "fasta")

    
    subprocess.run(["mafft", "--auto", input_file], stdout=open(output_file, "w"), stderr=subprocess.DEVNULL, check=True)

    aligned = list(SeqIO.parse(output_file, "fasta"))
    seqs = {rec.id: str(rec.seq).upper() for rec in aligned}

    if ref_id not in seqs:
        raise ValueError(f"参考序列ID {ref_id} 未出现在比对结果中。包含的ID为: {list(seqs.keys())}")

    sample_ids = [i for i in seqs if i != ref_id]
    if len(sample_ids) != 2:
        raise ValueError("应包含2个样本和1个参考序列。")

    return compare_sequences(seqs[sample_ids[0]], seqs[sample_ids[1]], seqs[ref_id])


diff_matrix = {name: {other: 0 for other in sample_names} for name in sample_names}


for file1, file2 in itertools.combinations(sample_files, 2):
    name1 = os.path.splitext(os.path.basename(file1))[0]
    name2 = os.path.splitext(os.path.basename(file2))[0]
    print(f"Comparing: {name1} vs {name2} ...")

    try:
        diff_count = align_and_count(file1, file2, ref_file)
        diff_matrix[name1][name2] = diff_count
        diff_matrix[name2][name1] = diff_count
    except Exception as e:
        print(f"Error comparing {name1} and {name2}: {e}")
        diff_matrix[name1][name2] = diff_matrix[name2][name1] = "ERR"


with open(output_csv, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Sample"] + sample_names)
    for name in sample_names:
        row = [name] + [diff_matrix[name][other] for other in sample_names]
        writer.writerow(row)

print(f"\n✅ finished：{output_csv}")

