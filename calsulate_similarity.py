import os
import glob

def calculate_similarity(alignment_file):
    """ 计算 MAFFT 比对结果的序列相似性百分比 """
    with open(alignment_file, "r") as f:
        lines = f.readlines()

    seq1 = []
    seq2 = []
    read_seq = False

    for line in lines:
        if line.startswith(">"):
            read_seq = not read_seq
        elif read_seq:
            seq2.append(line.strip())
        else:
            seq1.append(line.strip())

    seq1 = "".join(seq1)
    seq2 = "".join(seq2)

    if len(seq1) != len(seq2):
        return None  # 确保序列长度一致

    match_count = sum(1 for a, b in zip(seq1, seq2) if a == b)
    similarity = (match_count / len(seq1)) * 100
    return similarity

# 读取所有比对文件
alignment_files = glob.glob("test/*.aln")
results = []

for aln_file in alignment_files:
    similarity = calculate_similarity(aln_file)
    if similarity is not None:
        sample1, sample2 = os.path.basename(aln_file).replace(".aln", "").split("_vs_")
        results.append([sample1, sample2, similarity])

# 保存到 CSV
import pandas as pd

df = pd.DataFrame(results, columns=["Sequence_1", "Sequence_2", "Similarity (%)"])
df.to_csv("mtDNA_similarity_results.csv", index=False)

print("计算完成，结果已保存到 mtDNA_similarity_results.csv")

