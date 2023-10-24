"""
Convert Gnomix local ancestry files to Colate format.

This script is used to convert local ancestry data from Gnomix format to Colate format.
    In addition to the standard input files, an assignment file, typically named
    "assignments.txt," is required.
    This file stores the local ancestry information for all samples in the Relate tree.

The assignment file's format is as follows:

- The first row lists all possible group labels.
- Each subsequent row represents a chromosome and includes chromosome name,
    base pair position (BP), and the group index of samples.
    Each row has a length of N+2, where N is the number of haploid sequences.
- The first row for each chromosome must start with BP = 0.

Example assignment file:

group1 group2 group3
1   0 0 0 0 0 0 1 2 1 1
1   150000000 0 0 1 1 1 2 0 0
1   300000000 1 1 1 1 0 2 0 0

Note: The first column in the assignment file must exactly match the chromosome
    name indicated in the filename of the Relate trees.
    For example, it should be '1' and not 'chr1'.
"""
import pandas as pd


def load_pop_codes(msp_file):
    """
    Reads population codes from the msp_file, which are included in the file's first line.
    Returns a dictionary mapping codes to names.
    """
    with open(msp_file, 'r') as mf:
        header_codes = mf.readline().strip()
    
    pop_codes = header_codes.replace('#Subpopulation order/codes: ', '').split('\t')
    return {code: name for name, code in (x.split('=') for x in pop_codes)}


def load_msp_file(msp_file):
    """
    Loads the msp_file as a pandas DataFrame. The msp file is the Gnomix output with predicted local ancestry.
    Returns the DataFrame and a dictionary of population codes.
    """
    msp = pd.read_table(msp_file, skiprows=1)
    pop_codes = load_pop_codes(msp_file)
    return msp, pop_codes


def convert_gnomix_to_colate(gnomix, poplabels):
    # Sort the gnomix DataFrame by 'spos' column
    gnomix = gnomix.sort_values(by='spos', ascending=True)

    # Rename 'CHR' and 'BP' columns
    gnomix['CHR'] = gnomix['#chm'].str.replace('chr', '')
    gnomix['BP'] = gnomix['spos']

    # Set the first BP for each chromosome to 0
    gnomix.iloc[0, gnomix.columns.get_loc('BP')] = 0

    # Define sample and haplotype order
    sample_order = poplabels['sample'].tolist()
    haplotypes_order = [f"{sample}_0" for sample in sample_order] + [f"{sample}_1" for sample in sample_order]

    # Convert haplotype columns from Gnomix format to Colate format
    for haplotype in haplotypes_order:
        hap_gnomix = haplotype.replace('_', '.')
        gnomix[haplotype] = gnomix[hap_gnomix].copy() if hap_gnomix in gnomix.columns else ANCESTRY_OF_INTEREST

    # Define the final column order
    column_order = ['CHR', 'BP'] + haplotypes_order
    gnomix = gnomix[column_order]

    return gnomix


def write_assignments(pop_codes, colate_file, assignment):
    group_labels = ' '.join([f'{pop_codes[str(x)]}' for x in range(len(pop_codes))])

    with open(colate_file, 'w') as a_file:
        a_file.write(group_labels + '\n')

    assignment.to_csv(colate_file, sep=' ', mode='a', index=False, header=False)


if __name__ == "__main":
    # Specify the paths to poplabels and gnomix files
    poplabels_file = 'data/example.poplabels'
    gnomix_file = 'data/example.msp'
    out_colate = 'data/assignment.txt'
    # Define a constant for the ancestry of interest
    ANCESTRY_OF_INTEREST = 0

    # Load poplabels and gnomix data
    poplabels = pd.read_csv(poplabels_file, sep=' ')
    gnomix, _ = load_msp_file(gnomix_file)

    # Convert Gnomix data to Colate format
    assignment = convert_gnomix_to_colate(gnomix, poplabels)

    # save
    write_assignments(pop_codes, out_colate, assignment)
