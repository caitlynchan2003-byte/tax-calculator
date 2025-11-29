import pandas as pd

def verify_user(ic_number, password):
    """
    Verify user credentials
    
    Args:
        ic_number (str): 12-digit IC number
        password (str): Last 4 digits of IC
    
    Returns:
        bool: True if valid, False otherwise
    """
    # Check if IC is exactly 12 digits and numeric
    if len(ic_number) != 12 or not ic_number.isdigit():
        return False
    
    # Check if password matches last 4 digits
    if len(password) != 4 or password != ic_number[-4:]:
        return False
    
    return True

def calculate_tax(income, tax_relief):
    """
    Calculate Malaysian tax based on income and reliefs
    
    Args:
        income (float): Annual income
        tax_relief (float): Total tax relief amount
    
    Returns:
        float: Tax payable amount
    """
    # Calculate chargeable income
    chargeable_income = income - tax_relief
    
    if chargeable_income <= 0:
        return 0
    
    # Malaysian tax rates for 2024
    tax_brackets = [
        (5000, 0.00),      # 0% on first 5,000
        (20000, 0.01),     # 1% on next 15,000
        (35000, 0.03),     # 3% on next 15,000
        (50000, 0.06),     # 6% on next 15,000
        (70000, 0.11),     # 11% on next 20,000
        (100000, 0.19),    # 19% on next 30,000
        (400000, 0.25),    # 25% on next 300,000
        (600000, 0.26),    # 26% on next 200,000
        (2000000, 0.28),   # 28% on next 1,400,000
        (float('inf'), 0.30)  # 30% on remainder
    ]
    
    tax_payable = 0
    previous_limit = 0
    
    for limit, rate in tax_brackets:
        if chargeable_income > previous_limit:
            taxable_amount = min(chargeable_income, limit) - previous_limit
            tax_payable += taxable_amount * rate
            previous_limit = limit
        else:
            break
    
    return round(tax_payable, 2)

def save_to_csv(data, filename="tax_records.csv"):
    """
    Save user data to CSV file
    
    Args:
        data (dict): User data to save
        filename (str): CSV filename
    """
    try:
        # Try to read existing file
        df = pd.read_csv(filename)
        # Append new data
        new_df = pd.DataFrame([data])
        df = pd.concat([df, new_df], ignore_index=True)
    except FileNotFoundError:
        # Create new file with header
        df = pd.DataFrame([data])
    
    # Save to CSV
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

def read_from_csv(filename="tax_records.csv"):
    """
    Read data from CSV file
    
    Args:
        filename (str): CSV filename
    
    Returns:
        DataFrame or None: Pandas DataFrame if file exists
    """
    try:
        df = pd.read_csv(filename)
        return df
    except FileNotFoundError:
        return None

# Test function for development
def test_functions():
    """Test all functions with sample data"""
    print("Testing verification function:")
    print(f"Valid credentials: {verify_user('123456789012', '9012')}")
    print(f"Invalid IC: {verify_user('12345', '9012')}")
    print(f"Wrong password: {verify_user('123456789012', '1234')}")
    
    print("\nTesting tax calculation:")
    test_cases = [
        (30000, 9000),   # Low income
        (50000, 12000),  # Medium income
        (100000, 20000), # High income
        (10000, 15000)   # Negative chargeable income
    ]
    
    for income, relief in test_cases:
        tax = calculate_tax(income, relief)
        print(f"Income: RM{income:,}, Relief: RM{relief:,}, Tax: RM{tax:,.2f}")

if __name__ == "__main__":
    test_functions()