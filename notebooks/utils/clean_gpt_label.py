def clean_gpt_label(row):
    try:
        row = row.strip('[]()')
        # row = row.strip()
        li = row.split(',')
        y = []
        if li[0] == 'No_Enough_Information':
            y.append(26)
        else:
            try:
                for x in li:
                    y.append(int(x))
            except:
                return ['Fail to convert']
        # Print the row ID and the row
        # print("Row ID:", row.name, "Row:", row)
        return y
    except:
        # print("Row ID:", row.name, "Row:", row)
        return ['Fail to convert']
    
    
def filter_26_label(row):
    while((26 in row) and (len(row)>1)):
        row.remove(26)
    return row


def filter_abnormal_and_short(df):
    df = df[[i[0]!='Fail to convert' for i in df['label']]]
    df = df[[len(i.split())>10 for i in df['paragraph']]]
    return df


