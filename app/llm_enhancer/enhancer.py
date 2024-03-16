def attempt_with_retries(operation, max_retries, *args, **kwargs):
    number_of_fails = 0
    while number_of_fails < max_retries:
        try:
            result = operation(*args, **kwargs)
            return result  # Operation succeeded, return result
        except Exception as e:
            print(f"Error during operation {operation.__name__}: {e}")
            number_of_fails += 1
            if number_of_fails >= max_retries:
                print(f"Max number of fails reached for operation {operation.__name__}")
                raise Exception(f"GPT error")

def extracting_process(gpt_bank, pandas_df, max_number_of_fails):
    #iterate through the rows of the dataframe
    for index, row in pandas_df.iterrows():
        enhanced_description = attempt_with_retries(
            gpt_bank.enhance_description,
            max_number_of_fails,
            description=row["description"],
            amount=row["amount"]
        )
        if enhanced_description is None:
            continue
        else:
            print(f"Enhanced description: {enhanced_description}")
            pandas_df.at[index, "enhanced_description"] = enhanced_description

        categories = attempt_with_retries(
            gpt_bank.extract_categories,
            max_number_of_fails,
            description=pandas_df.at[index, "description"]
        )
        if categories is None:
            continue
        else:
            print(f"Categories: {categories}")
            pandas_df.at[index, "categories"] = categories
    return pandas_df