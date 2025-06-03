import os
import pandas as pd

def preprocess_data(pr_root='data/PR', ghi_root='data/GHI', output_csv='processed_data.csv'):
    combined_data = []

    for root, _, files in os.walk(pr_root):
        for file in files:
            if file.endswith('.csv'):
                pr_path = os.path.join(root, file)                
                ghi_path = pr_path.replace(pr_root, ghi_root)
                if not os.path.exists(ghi_path):
                    print(f"Missing GHI file for {pr_path}")
                    continue

                pr_df = pd.read_csv(pr_path)
                ghi_df = pd.read_csv(ghi_path)

                if 'Date' in pr_df.columns and 'PR' in pr_df.columns and \
                    'Date' in ghi_df.columns and 'GHI' in ghi_df.columns:

                    merged_df = pd.merge(pr_df[['Date', 'PR']], ghi_df[['Date', 'GHI']], on='Date')
                    combined_data.append(merged_df)

                else:
                    print(f"Incorrect column headers in: {file}")



    final_df = pd.concat(combined_data, ignore_index=True)
    final_df['Date'] = pd.to_datetime(final_df['Date'])
    final_df = final_df.sort_values('Date')    
    final_df.to_csv(output_csv, index=False)
    print(f"Final CSV saved as {output_csv} with {len(final_df)} rows")
    return final_df


preprocess_data()