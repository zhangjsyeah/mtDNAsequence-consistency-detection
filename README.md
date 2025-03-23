# mtDNAsequence-consistency-detection
To avoid potential biases introduced by matrilineal kinship, this script was used for testing the kinship.
Step 1：安装 MAFFT
sudo apt-get install mafft  # Linux
brew install mafft          # macOS

Step 2：运行比对脚本
chmod +x run_mafft.sh
./run_mafft.sh
所有比对结果将存储在 mafft_results/ 目录。

Step 3：运行 Python 代码计算相似性
python calculate_similarity.py
输出 CSV 格式如下：

Sequence_1	Sequence_2	Similarity (%)
sample1	sample2	99.2
sample1	sample3	98.7
sample2	sample3	97.9
