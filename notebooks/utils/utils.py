import os


def get_lda_table()-> dict:
    lda_table = {
        'Business_Ethics': 0,
        'Data_Security': 1,
        'Access_And_Affordability': 2,
        'Business_Model_Resilience': 3,
        'Competitive_Behavior': 4,
        'Critical_Incident_Risk_Management': 5,
        'Customer_Welfare': 6,
        'Director_Removal': 7,
        'Employee_Engagement_Inclusion_And_Diversity': 8,
        'Employee_Health_And_Safety': 9,
        'Human_Rights_And_Community_Relations': 10,
        'Labor_Practices': 11,
        'Management_Of_Legal_And_Regulatory_Framework': 12,
        'Physical_Impacts_Of_Climate_Change': 13,
        'Product_Quality_And_Safety': 14,
        'Product_Design_And_Lifecycle_Management': 15,
        'Selling_Practices_And_Product_Labeling': 16,
        'Supply_Chain_Management': 17,
        'Systemic_Risk_Management': 18,
        'Waste_And_Hazardous_Materials_Management': 19,
        'Water_And_Wastewater_Management': 20,
        'Air_Quality': 21,
        'Customer_Privacy': 22,
        'Ecological_Impacts': 23,
        'Energy_Management': 24,
        'GHG_Emissions': 25,
        'No_Enough_Information': 26
    }
    return lda_table

def get_lda_list(label: int):
    if label == 26:
        return ['Business_Ethics:0', 'Data_Security:1', 'Access_And_Affordability:2', 'Business_Model_Resilience:3',
                'Competitive_Behavior:4', 'Critical_Incident_Risk_Management:5', 'Customer_Welfare:6',
                'Director_Removal:7', 'Employee_Engagement_Inclusion_And_Diversity:8', 'Employee_Health_And_Safety:9',
                'Human_Rights_And_Community_Relations:10', 'Labor_Practices:11', 'Management_Of_Legal_And_Regulatory_Framework:12',
                'Physical_Impacts_Of_Climate_Change:13', 'Product_Quality_And_Safety:14', 'Product_Design_And_Lifecycle_Management:15',
                'Selling_Practices_And_Product_Labeling:16', 'Supply_Chain_Management:17', 'Systemic_Risk_Management:18',
                'Waste_And_Hazardous_Materials_Management:19', 'Water_And_Wastewater_Management:20', 'Air_Quality:21',
                'Customer_Privacy:22', 'Ecological_Impacts:23', 'Energy_Management:24', 'GHG_Emissions:25'
            ] 
    elif label == 27:
        return ['Business Ethics:0', 'Data Security:1', 'Access And Affordability:2', 'Business Model Resilience:3',
            'Competitive Behavior:4', 'Critical Incident Risk Management:5', 'Customer Welfare:6',
            'Director Removal:7', 'Employee Engagement Inclusion And Diversity:8', 'Employee Health And Safety:9',
            'Human Rights And Community Relations:10', 'Labor Practices:11', 'Management Of Legal And Regulatory Framework:12',
            'Physical Impacts Of Climate Change:13', 'Product Quality And Safety:14', 'Product Design And Lifecycle Management:15',
            'Selling Practices And Product Labeling:16', 'Supply Chain Management:17', 'Systemic Risk Management:18',
            'Waste And Hazardous Materials Management:19', 'Water And Wastewater Management:20', 'Air Quality:21',
            'Customer Privacy:22', 'Ecological Impacts:23', 'Energy Management:24', 'GHG Emissions:25', 'No Enough Information:26'
            ]
    else:
        raise ValueError("Label number can only be 26 or 27")

def get_reversed_dict()->dict:
    lda_table = get_lda_table()
    return {value: key for key, value in lda_table.items()}


def get_all_file_list(nation):
    if nation == 'american':
        return [
            '1_dow_1_85.pdf', 
            '2_agilent_1_106.pdf', '3_amazon_1_79.pdf', '4_apple_1_72.pdf',
            '5_boeing_1_66.pdf', '6_bxp_1_65.pdf', '7_charles_1_50.pdf', '8_cisco_1_56.pdf', '9_citigroup_1_137.pdf', '10_cme_1_34.pdf', 
            '11_colgate_1_84.pdf', '12_corning_1_71.pdf', '13_expeditor_1_37.pdf', '14_eei_1_80.pdf', '15_itt_1_44.pdf', 
            '16_fedex_1_34.pdf', '17_firstscolar_1_57.pdf', '18_google_1_14.pdf', '19_intel_1_86.pdf', '20_jpmorgan_1_61.pdf', 
            '21_microsoft_1_89.pdf', '22_rockwell_1_58.pdf', '23_ibm_1_49.pdf', '24_traveler_1_147.pdf', '25_visa_1_52.pdf', '0710_Tino_clean.pdf']
    elif nation == 'taiwan':
        return [ '1_umc_1_154.pdf',
            '2_agilent_1_106.pdf', '3_amazon_1_79.pdf', '4_apple_1_72.pdf',
            '5_boeing_1_66.pdf', '6_bxp_1_65.pdf', '7_charles_1_50.pdf', '8_cisco_1_56.pdf', '9_citigroup_1_137.pdf', '10_cme_1_34.pdf', 
            '11_colgate_1_84.pdf', '12_corning_1_71.pdf', '13_expeditor_1_37.pdf', '14_eei_1_80.pdf', '15_itt_1_44.pdf', 
            '16_fedex_1_34.pdf', '17_firstscolar_1_57.pdf', '18_google_1_14.pdf', '19_intel_1_86.pdf', '20_jpmorgan_1_61.pdf', 
            '21_microsoft_1_89.pdf', '22_rockwell_1_58.pdf', '23_ibm_1_49.pdf', '24_traveler_1_147.pdf', '25_visa_1_52.pdf']
        
        
def get_distribution(label):
    value_counts = label.value_counts()
    for key, value in value_counts.items():
        print(f"{key}: {value}")
        
        
def get_multi_label_distribution(df):
    import ast
    df['label'] = df['label'].apply(ast.literal_eval)
    labels = []
    counts = []
    for i, row in df.iterrows():
        x = set()
        for label in row['label']:
            x.add(str(label))
            # print(label)
            # Iterate through the rows of the CSV file
        labels.extend(x)
    for i in range(27):
        # count label number in collected column value
        count = labels.count(str(i))
        counts.append(count)
    all_counts = sum(counts)
    weights = []
    probability = []
    for index, x in enumerate(counts):
        result = x / all_counts
        print(f"{index} : {result:.5f}")
        weight = round((1 / result) / 10, 5)
        probability.append(round(result, 5))
        weights.append(weight)
    for index, weight in enumerate(weights):
        print(f'{index} : {weight:.5f}')
    
def _convert_onehot(row):
    y = []
    for i in range(27):
        if i in row:
            y.append(1)
        else:
            y.append(0)
    return y


def multi_to_onehot(label):
    import ast
    label = label.apply(ast.literal_eval)
    label = label.apply(_convert_onehot)
    return label
