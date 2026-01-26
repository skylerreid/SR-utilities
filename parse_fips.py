import polars as pl
import re

def parse_fips_data(input_file: str, counties_output: str = 'counties.csv', states_output: str = 'states.csv'):
    """
    Parse FIPS code data from a text file and separate into county and state dataframes.
    
    Args:
        input_file: Path to the input text file
        counties_output: Path for the output CSV file with county data
        states_output: Path for the output CSV file with state data
    """
    
    fips_codes = []
    place_names = []
    
    # Read the file
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Skip header lines (first 3 lines based on your example)
    # Adjust this number if your actual file has different header structure
    data_start = 0
    for i, line in enumerate(lines):
        if '------------' in line:
            data_start = i + 1
            break
    
    # Parse each data line
    for line in lines[data_start:]:
        # Skip empty lines
        if not line.strip():
            continue
        
        # Extract FIPS code and place name using regex or fixed positions
        # The FIPS code appears to be around positions 4-9 and name starts around position 21
        match = re.search(r'(\d{5})\s+(.+)', line)
        
        if match:
            fips_code = match.group(1)
            place_name = match.group(2).strip()
            
            fips_codes.append(fips_code)
            place_names.append(place_name)
    
    # Create a polars dataframe
    df = pl.DataFrame({
        'fips_code': fips_codes,
        'place_name': place_names
    })
    
    # Separate states (FIPS codes ending in 000) from counties
    states_df = df.filter(pl.col('fips_code').str.ends_with('000'))
    counties_df = df.filter(~pl.col('fips_code').str.ends_with('000'))
    
    # Write to CSV files
    counties_df.write_csv(counties_output)
    states_df.write_csv(states_output)
    
    print(f"Parsed {len(df)} total records")
    print(f"States: {len(states_df)} records written to {states_output}")
    print(f"Counties: {len(counties_df)} records written to {counties_output}")
    print(f"\nFirst few counties:")
    print(counties_df.head())
    print(f"\nFirst few states:")
    print(states_df.head())
    
    return counties_df, states_df


if __name__ == "__main__":
    input_file = 'fipsfile.txt'
    
    counties_df, states_df = parse_fips_data(
        input_file=input_file,
        counties_output='counties.csv',
        states_output='states.csv'
    )

