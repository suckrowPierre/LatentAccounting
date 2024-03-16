import pandas as pd


def identify_and_filter_transactions(combined_df):
    # Assuming booking_date and value_date are already in datetime format; if not, convert them
    combined_df['booking_date'] = pd.to_datetime(combined_df['booking_date'])
    combined_df['value_date'] = pd.to_datetime(combined_df['value_date'])

    # Sort DataFrame to optimize search
    combined_df = combined_df.sort_values(by=['booking_date', 'value_date', 'amount'], ascending=[False, False, True])

    # Add temporary columns for matching
    combined_df['inverse_amount'] = combined_df['amount'] * -1
    combined_df['matched'] = False

    # Iterate over the DataFrame to find matches
    for index, row in combined_df.iterrows():
        if not row['matched']:  # Skip already matched transactions
            # Potential matches are opposite amounts on the same date(s)
            potential_matches = combined_df[(combined_df['booking_date'] == row['booking_date']) &
                                            (combined_df['value_date'] == row['value_date']) &
                                            (combined_df['inverse_amount'] == row['amount']) &
                                            (~combined_df['matched'])]

            # If a match is found, mark both transactions
            if not potential_matches.empty:
                first_match_index = potential_matches.index[0]
                combined_df.at[index, 'matched'] = True
                combined_df.at[first_match_index, 'matched'] = True


    # Filter out matched transactions
    filtered_df = combined_df[~combined_df['matched']].drop(columns=['inverse_amount', 'matched'])

    return filtered_df

def combine_and_filter_bank_accounts(accounts):
    combined_df = pd.concat(accounts, ignore_index=True)
    filtered_df = identify_and_filter_transactions(combined_df)
    return filtered_df

