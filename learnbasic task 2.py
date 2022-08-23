import pandas as pd

#change the file name/path according to need
file_path = "Input_1 - Python Developer Intern - Task 2 - Datasets.xlsx"

def uniqcolumns(column): #split the column names
    split_indx = column.find('-')
    test_name = column[:split_indx].strip()
    column_name = column[split_indx+1:].strip()
    return test_name,column_name

df = pd.read_excel(file_path) #read the excel file

test_names = []
column_names = []

for i in range(len(df.columns)): #make lists of test names and test parameters
    column = str(df.columns[i])
    if '-' in column:
        test_name,column_name = uniqcolumns(column)
        if test_name not in test_names:
            test_names.append(test_name)
        if column_name not in column_names:
            column_names.append(column_name)
   
input_columns = df.columns.tolist()
output_columns = df.columns[:3].tolist() + ['Test_Name'] + column_names
output_df = pd.DataFrame(columns=output_columns)
name_list = df.Name.tolist()
final_output_list = []

#Reconstructing the DataFrame
for i,name in enumerate(name_list):
    output_row = []
    initial_values = []
    test_name_done = []
    row_value = df.iloc[i].tolist()
    initial_values = row_value[:3]
    
    for indx in range(3,len(row_value)): 
        column = input_columns[indx]
        test_name = column.split('-')[0].strip()
        if test_name not in test_name_done:                          
            output_row.append(test_name)
            test_name_done.append(test_name)
        output_row.append(row_value[indx])
        
        if len(output_row) == len(column_names)+1:
            flag = 0
            for num in range(len(output_row)):
                if output_row[num] == '-':
                    flag = 1
                    break
                    
            if flag == 0:      
                final_output_list.append(initial_values + output_row)
            output_row = []
    
for item in final_output_list:
    output_df.loc[len(output_df)] = item

output_df = output_df.sort_values(by=['Name','Test_Name'],ascending=True)

output_df.to_excel('programoutput.xlsx',index = False) #final output excel file