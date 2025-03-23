#!/bin/bash

# 设置 FASTA 文件所在目录
FASTA_DIR="/Users/zhangjs/Downloads/testmtDNA"  # 替换为你的目录路径
OUTPUT_DIR="/Users/zhangjs/Downloads/test"  # 存储比对结果的目录

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 获取所有 FASTA 文件
FASTA_FILES=($(ls "$FASTA_DIR"/*.fasta))

# 进行两两比对
for ((i=0; i<${#FASTA_FILES[@]}; i++)); do
    for ((j=i+1; j<${#FASTA_FILES[@]}; j++)); do
        FILE1="${FASTA_FILES[$i]}"
        FILE2="${FASTA_FILES[$j]}"
        MERGED_FILE="$OUTPUT_DIR/$(basename "$FILE1" .fasta)_vs_$(basename "$FILE2" .fasta).merged.fasta"
        OUTPUT_FILE="$OUTPUT_DIR/$(basename "$FILE1" .fasta)_vs_$(basename "$FILE2" .fasta).aln"

        # 合并两个 FASTA 文件
        cat "$FILE1" "$FILE2" > "$MERGED_FILE"

        # 使用 MAFFT 进行比对
        mafft --auto "$MERGED_FILE" > "$OUTPUT_FILE"

        echo "比对完成: $FILE1 vs $FILE2 -> $OUTPUT_FILE"
    done
done

