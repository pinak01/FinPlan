import matplotlib.pyplot as plt

def get_80C_deductions():
    # Ask the user if they have invested in each 80C instrument
    deductions = 0
    summary = {
        "Life Insurance Premium": "Life insurance provides both coverage and tax benefits under 80C. It ensures financial protection for your family.",
        "Public Provident Fund (PPF)": "PPF offers a long-term savings option with a government-guaranteed return and tax savings.",
        "Employees Provident Fund (EPF)": "EPF is a retirement savings scheme for salaried employees with employer contributions.",
        "Equity Linked Savings Scheme (ELSS)": "ELSS offers tax savings and potential market-linked returns with a lock-in period of 3 years.",
        "Unit Linked Insurance Plan (ULIP)": "ULIP combines insurance and investment, offering tax benefits and the chance for market-linked returns.",
        "Tax Saver Fixed Deposits": "These are 5-year fixed deposits in banks that offer tax savings under 80C.",
        "National Pension Scheme (NPS)": "NPS offers retirement savings with additional tax savings under 80CCD.",
        "Home Loan Principal Repayment": "Repaying the principal on a home loan qualifies for tax deduction under 80C.",
        "Sukanya Samriddhi Yojana": "This scheme promotes savings for the girl child with tax benefits and high returns.",
        "Senior Citizens Savings Scheme": "A government-backed savings option with regular interest payouts for senior citizens.",
        "National Savings Certificate": "A fixed-income investment with guaranteed returns and tax benefits under 80C."
    }

    # Iterate over each option and prompt the user
    for investment, desc in summary.items():
        print(f"\n{investment}: {desc}")
        response = input(f"Have you invested in {investment}? (yes/no): ").strip().lower()
        if response == 'yes':
            amount = float(input(f"Enter the amount invested in {investment}: "))
            deductions += amount

    # Ensure 80C deductions are capped at Rs. 1.5 lakh
    deductions = min(deductions, 150000)

    # Ask if the user has invested in NPS for an additional Rs. 50,000 deduction under 80CCD
    nps_investment = input("\nHave you invested in NPS (for additional Rs. 50,000 deduction under 80CCD)? (yes/no): ").strip().lower()
    if nps_investment == 'yes':
        nps_amount = float(input("Enter the amount invested in NPS: "))
        # Deduction under 80CCD for NPS is capped at Rs. 50,000
        deductions += min(nps_amount, 50000)

    return deductions


def get_80D_deductions():
    health_insurance_deduction = 0
    summary = {
        "Health Insurance Premium": "Section 80D allows you to claim deductions on premiums paid for health insurance for yourself, your spouse, children, and parents. The maximum deduction is ₹25,000 (or ₹50,000 for senior citizens) for premiums paid for self and family, and an additional deduction of ₹25,000 (or ₹50,000 for senior citizens) for premiums paid for parents."
    }

    # Show summary
    print(f"\n{summary['Health Insurance Premium']}")

    # Input for self and family health insurance
    response = input("Have you paid any health insurance premiums for yourself and your family? (yes/no): ").strip().lower()
    if response == 'yes':
        amount = float(input("Enter the amount paid for health insurance premiums (self & family): "))
        if amount <= 25000:
            health_insurance_deduction += amount
        else:
            health_insurance_deduction += 25000  # Cap at 25,000

    # Input for parents' health insurance
    response = input("Have you paid any health insurance premiums for your parents? (yes/no): ").strip().lower()
    if response == 'yes':
        amount = float(input("Enter the amount paid for health insurance premiums (parents): "))
        if amount <= 25000:
            health_insurance_deduction += amount
        else:
            health_insurance_deduction += 25000  # Cap at 25,000

    return health_insurance_deduction


def get_section_24_deductions():
    housing_loan_deduction = 0

    # Explain Section 24
    print("\nSection 24 of the Income Tax Act allows you to claim deductions on interest paid on housing loans.")
    print("You can claim a deduction of up to ₹2 lakh per financial year on the interest paid on home loans for a self-occupied property.")
    print("If the property is let out (rented), you can claim the entire interest paid, with no upper limit.")

    # Input for housing loan interest
    response = input("Have you paid any interest on a housing loan? (yes/no): ").strip().lower()
    if response == 'yes':
        amount = float(input("Enter the amount of interest paid on the housing loan: "))
        is_self_occupied = input("Is the property self-occupied? (yes/no): ").strip().lower()
        if is_self_occupied == 'yes':
            housing_loan_deduction += min(amount, 200000)  # Cap for self-occupied property
        else:
            housing_loan_deduction += amount  # No cap for rented property

    return housing_loan_deduction

def get_80E_deductions():
    print("\nEducation Loan Deduction under Section 80E:")
    print("The interest paid on education loans for higher studies is eligible for deduction under Section 80E.")
    print("Key points regarding Section 80E:")
    print("1. Only the interest component of the EMI is eligible for deduction.")
    print("2. This deduction is available for a maximum of eight years, starting from the year you begin repayment.")
    print("3. There is no limit on the maximum amount you can claim as a deduction.")
    print("4. Only individuals can claim this deduction; HUFs and companies are not eligible.")
    print("5. The loan must be taken from recognized financial institutions or approved charitable organizations.")
    if input("Do you have any ongoing education loan:  (yes/no): ").strip().lower() == 'yes':
        interest_paid = float(input("Enter the total interest paid on the education loan: "))
        return interest_paid  # No limit on the deduction
    return 0

def calculate_hra_deduction():
    print("\nHRA Deduction:")
    print("This section allows deductions for House Rent Allowance (HRA) under Section 10(13A).")
    if input("Do you live in a rented house? (yes/no): ").strip().lower() == 'yes':
        basic_salary = float(input("Enter your Basic Salary(check  your salary slip): ₹"))
        hra_received = float(input("Enter HRA received: ₹"))
        rent_paid = float(input("Enter total rent paid per month: ₹"))
        
        rent_paid_annually = rent_paid * 12
    
    # HRA Exemption Calculation
        if input("Do you live in a metro city? (yes/no): ").strip().lower() == 'yes':
            exempt_hra = min(
                hra_received,
                0.5 * basic_salary * 12,
                rent_paid_annually - (0.1 * basic_salary * 12)
            )
        else:
            exempt_hra = min(
                hra_received,
                0.4 * basic_salary * 12,
                rent_paid_annually - (0.1 * basic_salary * 12)
            )
    
        return exempt_hra
    return 0

def calculate_80ccd2_deduction(n=0):
    print("\nSection 80CCD(2) Deduction:")
    print("This section allows salaried individuals to claim deductions on their employer's contribution to the National Pension Scheme (NPS).")
    if input("Does your employer contribute to your nps?(yes/no) ").strip().lower() =='yes':
        basic_salary = float(input("Enter your Basic Salary: ₹"))
        da = float(input("Enter your Dearness Allowance (DA): ₹"))
        employer_contribution = float(input("Enter employer's contribution to NPS: ₹"))
        
        total_salary = basic_salary + da
        
        # Determine the maximum allowable deduction based on the employer type
        if input("Is your employer a Central or State Government? (yes/no): ").strip().lower() == 'yes':
            max_deduction = 0.14 * total_salary  # 14% for government employers
        else:
            if n==0:
                max_deduction = 0.10 * total_salary  # 10% for other employers (old regime)
            else:
                max_deduction = 0.14 * total_salary  # 10% for other
        eligible_deduction = min(employer_contribution, max_deduction)
    
        return eligible_deduction
    print("You can ask your employer if they are willing to contribute to NPS")
    return 0

def calculate_lta_deduction():
    lta = input("yes/no: ".strip().lower())
    if lta=="yes":
        print("\nLeave Travel Allowance (LTA) Exemption:")
        print("This exemption is available for travel costs incurred for domestic travel.")
        print("Key points to note:")
        print("- Only individuals can claim LTA for themselves and their family.")
        print("- Exemption is available only for domestic travel within India.")
        print("- Valid proof of travel is required to claim the exemption.")
        print("- Only actual travel costs (air, rail, bus fare) are eligible for exemption.")
        print("- No expenses like local conveyance, sightseeing, or accommodation are eligible.")
        print("- Can only be claimed twice in a block of four years (Current block 2022-2025).")
        lta_granted = float(input("Enter LTA amount granted by the employer(check your salary dlip): ₹"))
        travel_cost = float(input("Enter actual travel costs incurred (air, rail, bus fare): ₹"))
        print("whichever of the above two costs is less will be taken into consideration for tax deduction")
        lta_exemption = min(lta_granted, travel_cost)
        print(f"Total LTA Exemption: ₹{lta_exemption}")
        return lta_exemption

def calculate_section_80ee_deduction():
    print("Section 80EE Deduction for Home Loan Interest")

    # Get user inputs for eligibility
    owns_property = input("Do you own any residential house property on the date of loan sanction? (yes/no): ").strip().lower()
    if owns_property == 'yes':
        print("You are not eligible for Section 80EE deduction since you own residential property.")
        return 0

    property_value = float(input("What is the value of the property acquired? (INR): "))
    loan_amount = float(input("What is the amount of the home loan taken? (INR): "))
    loan_sanction_date = input("Was the home loan sanctioned between 01.04.2016 and 31.03.2022? (yes/no): ").strip().lower()

    # Check conditions for deduction eligibility
    if property_value > 5000000:
        print("You are not eligible for Section 80EE deduction as the property value exceeds INR 50 Lakhs.")
        return 0
    if loan_amount > 3500000:
        print("You are not eligible for Section 80EE deduction as the loan amount exceeds INR 35 Lakhs.")
        return 0
    if loan_sanction_date != 'yes':
        print("You are not eligible for Section 80EE deduction since the loan was not sanctioned in the specified period.")
        return 0

    # If all conditions are met, calculate deduction
    deduction = 50000  # Maximum deduction under Section 80EE
    print(f"You are eligible for a Section 80EE deduction of INR {deduction}.")
    return deduction

def calculate_section_80G_deduction():
    print("=== Section 80G Deduction Calculation ===")
    print("This section allows taxpayers to claim deductions for donations made to specified charitable institutions and funds.")
    print("The deduction can be up to 100% or 50% of the donated amount, depending on the institution or fund.")
    print("Donations exceeding Rs. 2,000 in cash are not eligible for deduction.")
    
    # Lists of eligible institutions
    full_deduction_institutions = [
        "National Defence Fund by the Central Government",
        "National Illness Assistance Fund",
        "Prime Minister’s National Relief Fund",
        "Fund by State Government for medical relief to poor",
        "National Foundation for Communal Harmony",
        "Zila Saksharta Samiti",
        "Approved university or National institution of national importance",
        "National/State Blood Transfusion Council",
        "National sports and cultural funds",
        "National Trust for Welfare of People with Autism, Cerebral Palsy, Mental Retardation and Multiple Disabilities",
        "Fund for Technology Development and Application",
        "Chief Minister’s Relief Fund",
        "National Children’s Fund",
        "Army Central Welfare Fund",
        "Chief Minister’s Earthquake Relief Fund",
        "Prime Minister’s Armenia Earthquake Relief Fund",
        "Africa Fund",
        "Clean Ganga Fund",
        "National Fund for Control of Drug Abuse",
        "Swacch Bharat Kosh"
    ]
    
    half_deduction_institutions = [
        "Prime Minister's Drought Relief Fund"
    ]
    
    qualifying_limit_institutions = [
        "Government or local authorities for family planning initiatives",
        "Indian Olympic Association or similar recognized organizations in India"
    ]
    
    print("\n=== Eligible Institutions for 100% Deduction ===")
    for institution in full_deduction_institutions:
        print(f"- {institution}")
        
    print("\n=== Eligible Institutions for 50% Deduction ===")
    for institution in half_deduction_institutions:
        print(f"- {institution}")
        
    print("\n=== Institutions Eligible for 50% Deduction with Qualifying Limit ===")
    for institution in qualifying_limit_institutions:
        print(f"- {institution}")
    
    # Ask for the donation amount
    donation_amount = float(input("\nEnter the total donation amount: "))

    # Ask for the mode of donation
    cash_donation = input("Is this donation made in cash? (yes/no): ").strip().lower() == 'yes'
    if cash_donation and donation_amount > 2000:
        print("Cash donations above Rs. 2,000 are not eligible for deduction under Section 80G.")
        return 0.0

    # Ask for eligibility category
    eligible_for_full_deduction = input("Is the donation made to an institution eligible for 100% deduction? (yes/no): ").strip().lower() == 'yes'
    
    if eligible_for_full_deduction:
        print("You can claim 100% of the donated amount as a deduction.")
        return donation_amount
    
    eligible_for_half_deduction = input("Is the donation made to an institution eligible for 50% deduction? (yes/no): ").strip().lower() == 'yes'
    
    if eligible_for_half_deduction:
        # Calculate qualifying limit
        gross_total_income = float(input("Enter your adjusted gross total income: "))
        qualifying_limit = 0.1 * gross_total_income
        half_deduction_amount = donation_amount * 0.5
        
        # Apply maximum limit condition
        amount_deductible = min(half_deduction_amount, qualifying_limit)
        print(f"You can claim {amount_deductible} as a deduction under Section 80G.")
        return amount_deductible
    
    print("The donation does not qualify for deductions under Section 80G.")
    return 0.0


def calculate_80ggc_deduction():
    # Brief summary of Section 80GGC
    summary = (
        "Section 80GGC allows individuals to claim a deduction for donations made to registered political parties. "
        "The entire contribution is eligible for tax deduction, provided it is not made in cash and does not exceed "
        "the individual's total taxable income. It's important to note that this deduction can only be claimed under "
        "the old tax regime."
    )
    print(summary)
    
    # Initialize variables
    donation_amount = 0
    total_taxable_income = 0

    # Ask the user for their taxable income
    total_taxable_income = float(input("Please enter your total taxable income: "))

    # Check if the user has made a donation
    donation_made = input("Have you made a donation to a registered political party? (yes/no): ").strip().lower()
    
    if donation_made == 'yes':
        # Ask for the amount donated
        donation_amount = float(input("Enter the amount donated to the political party: "))
        
        # Check if the donation is cashless
        cashless_donation = input("Was the donation made in cash? (yes/no): ").strip().lower()
        
        if cashless_donation == 'no':
            # Check if the donation amount is within limits
            if donation_amount <= total_taxable_income:
                deduction = donation_amount
                return deduction
            else:
                print("The deduction cannot exceed your total taxable income.")
        else:
            print("Donations made in cash are not eligible for deduction under Section 80GGC.")
    else:
        print("No donation was made. You are not eligible for the deduction under Section 80GGC.")
    return 0

# Call the function to calculate deductions under Section 80GGC


def calculate_tax_old_regime(income, deductions):
    taxable_income = income - deductions
    # Apply rebate for income up to Rs. 550,000
    if taxable_income <= 500000:
        return 0  # Tax is zero after rebate
    tax = 0
    if taxable_income <= 300000:
        tax = 0
    elif taxable_income <= 500000:
        tax = (taxable_income - 300000) * 0.05
    elif taxable_income <= 1000000:
        tax = (200000 * 0.05) + (taxable_income - 500000) * 0.1
    elif taxable_income <= 1500000:
        tax = (200000 * 0.05) + (500000 * 0.1) + (taxable_income - 1000000) * 0.15
    else:
        tax = (200000 * 0.05) + (500000 * 0.1) + (500000 * 0.15) + (taxable_income - 1500000) * 0.2
    return tax


def calculate_tax_new_regime(income,deductions):
    taxable_income = income-deductions
    # Apply rebate for income up to Rs. 750,000
    if taxable_income <= 700000:
        return 0  # Tax is zero after rebate
    tax = 0
    if taxable_income <= 300000:
        tax = 0
    elif taxable_income <= 700000:
        tax = (taxable_income - 300000) * 0.05
    elif taxable_income <= 1000000:
        tax = (400000 * 0.05) + (taxable_income - 700000) * 0.1
    elif taxable_income <= 1200000:
        tax = (400000 * 0.05) + (300000 * 0.1) + (taxable_income - 1000000) * 0.15
    elif taxable_income <= 1500000:
        tax = (400000 * 0.05) + (300000 * 0.1) + (200000 * 0.15) + (taxable_income - 1200000) * 0.2
    else:
        tax = (400000 * 0.05) + (300000 * 0.1) + (200000 * 0.15) + (300000 * 0.2) + (taxable_income - 1500000) * 0.3
    return tax


def compare_tax_regimes(income, deductions,deductions1):
    # Calculate tax under both regimes
    old_taxable_income = calculate_tax_old_regime(income, deductions)
    new_taxable_income = calculate_tax_new_regime(income,deductions1)
    
    regimes = ['Old Tax Regime', 'New Tax Regime']
    values = [old_taxable_income, new_taxable_income]

    # Create a bar chart
    plt.figure(figsize=(8, 6))
    plt.bar(regimes, values, color=['blue', 'green'])
    
    # Adding labels and title
    plt.xlabel('Tax Regime')
    plt.ylabel('Taxable Income (₹)')
    plt.title('Comparison of Old vs New Tax Regime')
    plt.text(0, old_taxable_income + 0.01 * old_taxable_income, f"₹{old_taxable_income:.2f}", ha='center')
    plt.text(1, new_taxable_income + 0.01 * new_taxable_income, f"₹{new_taxable_income:.2f}", ha='center')

    # Show the graph
    plt.show()
    # Output the comparison
    print(f"\nTax under Old Regime: ₹{old_taxable_income}")
    print(f"Tax under New Regime: ₹{new_taxable_income}")
    
    # Compare and suggest which regime is better
    if old_taxable_income < new_taxable_income:
        print("Old Regime is better for you.")
    else:
        print("New Regime is better for you.")


# Example usage

def suggest_tax_savings(taxable_income_old, taxable_income_new, current_deductions,ded,ded1):
    """
    This function suggests tax-saving options and calculates the tax after each deduction.
    The function stops when the user opts out or when tax reaches zero.
    """
    
    # Define maximum deduction limits
    deductions = {
        '80C': {'limit': 150000, 'message': 'Invest in 80C options like PPF, ELSS, etc.'},
        '80D': {'limit': 50000, 'message': 'Purchase health insurance (80D) for yourself or dependents.'},
        'Section 24': {'limit': 200000, 'message': 'Pay interest on your housing loan (Section 24).'},
        '80E': {'limit': 50000, 'message': 'Pay interest on your education loan (80E).'},
        '80GGC': {'limit': taxable_income_old, 'message': 'Donate to political parties (80GGC).'},
        # Add more options if needed
    }

    while True:
        # Display current taxable income and tax amounts under old and new regimes
        print(f"\nCurrent taxable income (Old Regime): {taxable_income_old}")
        print(f"Current taxable income (New Regime): {taxable_income_new}")
        
        # Calculate tax (this should be done using your existing tax calculation function)
        tax_old = calculate_tax_old_regime(taxable_income_old,ded)
        tax_new = calculate_tax_new_regime(taxable_income_new,ded1)
        
        print(f"Tax (Old Regime): {tax_old}")
        print(f"Tax (New Regime): {tax_new}")

        if tax_old == 0 or tax_new == 0:
            print("Congratulations! Your tax liability has been reduced to zero.")
            break

        # Suggest additional deductions
        print("\nYou can further reduce your tax by applying the following deductions:")
        for key, value in deductions.items():
            if current_deductions.get(key, 0) < value['limit']:
                print(f"{key}: {value['message']} (Remaining: {value['limit'] - current_deductions.get(key, 0)})")
        
        # Ask user for input
        deduction_choice = input("Choose a deduction to apply (or type 'exit' to stop): ").strip().upper()
        
        if deduction_choice == 'EXIT':
            print("You chose to stop. Final tax calculations will be displayed.")
            break

        # Validate user input 
        if deduction_choice not in deductions:
            print("Invalid choice. Please try again.")
            continue
        
        # Ask user how much they want to invest or claim under the selected deduction
        amount_to_invest = int(input(f"How much would you like to invest/claim under {deduction_choice}? "))
        
        if amount_to_invest > (deductions[deduction_choice]['limit'] - current_deductions.get(deduction_choice, 0)):
            print(f"You can only invest up to {deductions[deduction_choice]['limit'] - current_deductions.get(deduction_choice, 0)} in {deduction_choice}.")
            continue

        # Apply the deduction to taxable income
        current_deductions[deduction_choice] = current_deductions.get(deduction_choice, 0) + amount_to_invest
        taxable_income_old -= amount_to_invest

        print(f"Deduction of {amount_to_invest} applied under {deduction_choice}. Recalculating tax...")
        
    # Final tax after all deductions
    print("\nFinal Tax Calculation:")
    final_tax_old = calculate_tax_old_regime(taxable_income_old,ded)
    final_tax_new = calculate_tax_new_regime(taxable_income_new,ded1)
    print(f"Final Tax (Old Regime): {final_tax_old}")
    print(f"Final Tax (New Regime): {final_tax_new}")

# Example usage of the function
gross_income = float(input("Enter your gross income: "))
deductions = 0

# Calculate deductions
deductions_80c = get_80C_deductions()
deductions_80d = get_80D_deductions()
deductions_24 = get_section_24_deductions()
deductions_80e = get_80E_deductions()
deductions_hra = calculate_hra_deduction()
deductions_ccd2 = calculate_80ccd2_deduction()
deductions_lta = calculate_lta_deduction()
deductions_80ee = calculate_section_80ee_deduction()
deductions_80g = calculate_section_80G_deduction()
deductions_80gcc = calculate_80ggc_deduction()

deductions = deductions_80c +  deductions_80d + deductions_24 + deductions_80e + deductions_hra + deductions_ccd2+  deductions_lta + deductions_80ee + deductions_80g + deductions_80gcc
deductions1= calculate_80ccd2_deduction(1)

current_deductions = {
    '80C': deductions_80c,  # Deduction claimed so far under Section 80C
    '80D': deductions_80d,  # Deduction claimed so far under Section 80D
    'Section 24': deductions_24,  # Deduction claimed under Section 24 (Housing Loan Interest)
    '80E': deductions_80e,  # Deduction claimed under Section 80E (Education Loan Interest)
    '80GGC': deductions_80gcc,  # Deduction claimed under Section 80GGC (Political Donations)
}
# Compare tax regimes
compare_tax_regimes(gross_income, deductions,deductions1)
taxable_income_old=calculate_tax_old_regime(gross_income,deductions)
taxable_income_new=calculate_tax_new_regime(gross_income,deductions1)
suggest_tax_savings(taxable_income_old, taxable_income_new ,current_deductions,deductions,deductions1)

