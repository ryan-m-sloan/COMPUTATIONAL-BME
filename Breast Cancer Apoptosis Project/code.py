import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind

# Load expression and metadata
data = pd.read_csv('GSE62944_subsample_topVar_log2TPM.csv', index_col=0)
metadata_df = pd.read_csv('GSE62944_metadata.csv', index_col=0)

# Subset BRCA samples
cancer_type = 'BRCA'
cancer_samples = metadata_df[metadata_df['cancer_type'] == cancer_type].index
BRCA_data = data[cancer_samples]
BRCA_metadata = metadata_df.loc[cancer_samples]

# Select apoptosis-related genes
genes_of_interest = ['TP53', 'BRCA1', 'BRCA2']
available_genes = [gene for gene in genes_of_interest if gene in BRCA_data.index]
BRCA_gene_data = BRCA_data.loc[available_genes]

# Merge expression with metadata
BRCA_merged = BRCA_gene_data.T.merge(BRCA_metadata, left_index=True, right_index=True)

# Check tumor_status column
if 'tumor_status' not in BRCA_merged.columns:
    raise KeyError("Column 'tumor_status' not found in metadata. Please verify metadata source.")

# Plot expression by tumor status
for gene in available_genes:
    sns.boxplot(data=BRCA_merged, x='tumor_status', y=gene)
    plt.title(f"{gene} Expression by Tumor Status")
    plt.show()

    # T-test
    tumor_group = BRCA_merged[BRCA_merged['tumor_status'] == 'With Tumor'][gene]
    normal_group = BRCA_merged[BRCA_merged['tumor_status'] == 'Tumor Free'][gene]
    t_stat, p_val = ttest_ind(tumor_group, normal_group, nan_policy='omit')
    print(f"T-test {gene} Tumor vs Tumor Free: t={t_stat:.2f}, p={p_val:.4f}")

# Optional: explore by clinical stage
if 'clinical_stage' in BRCA_merged.columns:
    for gene in available_genes:
        sns.boxplot(data=BRCA_merged, x='clinical_stage', y=gene)
        plt.title(f"{gene} Expression by Clinical Stage")
        plt.xticks(rotation=45)
        plt.show()

# Optional: explore by tumor grade
if 'tumor_grade' in BRCA_merged.columns:
    for gene in available_genes:
        sns.boxplot(data=BRCA_merged, x='tumor_grade', y=gene)
        plt.title(f"{gene} Expression by Tumor Grade")
        plt.xticks(rotation=45)
        plt.show()

# Optional: explore by treatment outcome
if 'treatment_outcome_first_course' in BRCA_merged.columns:
    for gene in available_genes:
        sns.boxplot(data=BRCA_merged, x='treatment_outcome_first_course', y=gene)
        plt.title(f"{gene} Expression by Treatment Outcome")
        plt.xticks(rotation=45)
        plt.show()