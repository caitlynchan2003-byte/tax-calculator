from functions import verify_user, calculate_tax, save_to_csv, read_from_csv
import getpass

def register_user():
    """Handle new user registration"""
    print("\n=== User Registration ===")
    
    user_id = input("Enter your ID: ")
    ic_number = input("Enter your IC number (12 digits): ")
    
    # Validate IC number
    while len(ic_number) != 12 or not ic_number.isdigit():
        print("Invalid IC number! Must be 12 digits.")
        ic_number = input("Enter your IC number (12 digits): ")
    
    password = ic_number[-4:]  # Last 4 digits as password
    print(f"Your password (last 4 digits of IC): {password}")
    
    return user_id, ic_number, password

def login_user():
    """Handle user login"""
    print("\n=== User Login ===")
    
    user_id = input("Enter your ID: ")
    password = getpass.getpass("Enter your password (last 4 digits of IC): ")
    
    return user_id, password

def get_tax_inputs():
    """Get income and tax relief inputs from user"""
    print("\n=== Tax Calculation Input ===")
    
    try:
        income = float(input("Enter your annual income (RM): "))
        print("\nAvailable Tax Reliefs:")
        print("1. Individual Relief: RM9,000")
        print("2. Spouse Relief: RM4,000")
        print("3. Child Relief: RM8,000 per child")
        print("4. Medical Expenses: Up to RM8,000")
        print("5. Lifestyle Relief: Up to RM2,500")
        print("6. Education Fees: Up to RM7,000")
        print("7. Parental Care: Up to RM5,000")
        
        total_relief = 0
        print("\nEnter your tax relief amounts:")
        
        # Individual relief (mandatory)
        individual_relief = 9000
        total_relief += individual_relief
        print(f"Individual Relief: RM{individual_relief}")
        
        # Additional reliefs
        spouse_relief = float(input("Spouse Relief (RM): ") or 0)
        child_relief = float(input("Child Relief (RM): ") or 0)
        medical_relief = float(input("Medical Expenses Relief (RM): ") or 0)
        lifestyle_relief = float(input("Lifestyle Relief (RM): ") or 0)
        education_relief = float(input("Education Fees Relief (RM): ") or 0)
        parental_relief = float(input("Parental Care Relief (RM): ") or 0)
        
        total_relief += (spouse_relief + child_relief + medical_relief + 
                        lifestyle_relief + education_relief + parental_relief)
        
        return income, total_relief
        
    except ValueError:
        print("Invalid input! Please enter numeric values.")
        return get_tax_inputs()

def display_tax_records():
    """Display all tax records from CSV"""
    df = read_from_csv()
    if df is not None and not df.empty:
        print("\n=== All Tax Records ===")
        print(df.to_string(index=False))
    else:
        print("No tax records found!")

def main():
    """Main program function"""
    print("=== Malaysian Tax Input Program ===")
    
    while True:
        print("\nOptions:")
        print("1. Register New User")
        print("2. Login Existing User")
        print("3. View Tax Records")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            # Registration flow
            user_id, ic_number, password = register_user()
            
            # Verify and proceed to tax calculation
            if verify_user(ic_number, password):
                income, tax_relief = get_tax_inputs()
                tax_payable = calculate_tax(income, tax_relief)
                
                # Display results
                print(f"\n=== Tax Calculation Results ===")
                print(f"Annual Income: RM{income:,.2f}")
                print(f"Total Relief: RM{tax_relief:,.2f}")
                print(f"Tax Payable: RM{tax_payable:,.2f}")
                
                # Save to CSV
                user_data = {
                    'user_id': user_id,
                    'ic_number': ic_number,
                    'income': income,
                    'tax_relief': tax_relief,
                    'tax_payable': tax_payable
                }
                save_to_csv(user_data)
                print("Data saved successfully!")
            else:
                print("Registration failed! Invalid credentials.")
                
        elif choice == '2':
            # Login flow
            user_id, password = login_user()
            print("Please enter your IC number for verification:")
            ic_number = input("IC Number: ")
            
            if verify_user(ic_number, password):
                income, tax_relief = get_tax_inputs()
                tax_payable = calculate_tax(income, tax_relief)
                
                print(f"\n=== Tax Calculation Results ===")
                print(f"Annual Income: RM{income:,.2f}")
                print(f"Total Relief: RM{tax_relief:,.2f}")
                print(f"Tax Payable: RM{tax_payable:,.2f}")
                
                # Save data
                user_data = {
                    'user_id': user_id,
                    'ic_number': ic_number,
                    'income': income,
                    'tax_relief': tax_relief,
                    'tax_payable': tax_payable
                }
                save_to_csv(user_data)
                print("Data saved successfully!")
            else:
                print("Login failed! Invalid credentials.")
                
        elif choice == '3':
            # View records
            display_tax_records()
                
        elif choice == '4':
            print("Thank you for using Malaysian Tax Input Program!")
            break
            
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()