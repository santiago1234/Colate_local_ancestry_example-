"""
This script extracts the samples in the polabels file.
The output is the same as the Gnomix input.
"""
import pandas as pd


def load_pop_codes(msp_file):
    """
    Reads the population codes from
    the msp_file. The population codes are included
    in the first line of the msp file.
    """
    mf = open(msp_file, 'r')
    header_codes = mf.readline()
    mf.close()
    pop_codes = (
        header_codes
        .replace('#Subpopulation order/codes: ', '')
        .strip()
        .split('\t')
    )
    return {str(b): a for (a, b) in [x.split('=') for x in pop_codes]}


def load_msp_file(msp_file):
    """
    Loads the msp_file as a pandas.DataFrame
    NOTE: The msp file is the Gnomix output with the predicted local ancestry
    """
    msp = pd.read_table(msp_file, skiprows=1)
    p_codes = load_pop_codes(msp_file)
    return msp, p_codes


gnomix = '/data/users/smedina/genome-america/experiments/23-04-25-LAI-MaskNonIndigenousAncestries/results/query_results-chrn22.msp'
msp, pcodes = load_msp_file(gnomix)
samples = pd.read_csv('example.poplabels', sep=' ')
samples = samples['sample'].tolist()

_main_cols = ['#chm', 'spos', 'epos', 'sgpos', 'egpos', 'n snps']

sample_to_hap_cols = lambda sam: [f'{sam}.0', f'{sam}.1']

sample_cols = []

for sample in samples:
    a_sam = f'{sample}.0'
    if a_sam in msp.columns:
        sample_cols.extend(sample_to_hap_cols(sample))


msp = msp[_main_cols + sample_cols]

out_file = 'example.msp'


# Step 1: Read the existing file and store its content
with open(gnomix, 'r') as file:
    content = file.readlines()
    
# Extract the first row (header) from the content
first_row = content[0]

# Step 2: Create a new file and write the first row to it
with open(out_file, 'w') as new_file:
        new_file.write(first_row)

msp.to_csv(out_file, sep='\t', mode='a', index=False)
