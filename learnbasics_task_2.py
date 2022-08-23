#importing packages
import pandas as pd

#split the column names
def uniqcolumns(column): 
    split_indx = column.find('-')
    test_name = column[:split_indx].strip()
    column_name = column[split_indx+1:].strip()
    return test_name,column_name

def conversion_func(file_path):
    #read the xlsx file
    df = pd.read_excel(file_path) 
    #initialising lists to store the values for test names column and test parameters
    test_names = []
    column_names = []

    #make lists of test names and test parameters
    for i in range(len(df.columns)): 
        column = str(df.columns[i])
        if '-' in column:
            test_name,column_name = uniqcolumns(column)
            #only adding unique values to the list
            if test_name not in test_names:
                test_names.append(test_name)
            if column_name not in column_names:
                column_names.append(column_name)
   
    input_columns = df.columns.tolist()
    output_columns = df.columns[:3].tolist() + ['Test_Name'] + column_names
    output_df = pd.DataFrame(columns=output_columns)
    name_list = df.Name.tolist()

    #final list to store the list of rows that will be appended to the output dataframe
    final_output_list = []

    #Reconstructing the DataFrame
    for i,name in enumerate(name_list):
        output_row = []
        initial_values = []
        test_name_done = []
        row_value = df.iloc[i].tolist()

        #holds the column values that will not be changed
        initial_values = row_value[:3]
    
        for indx in range(3,len(row_value)): 
            column = input_columns[indx]
            test_name = column.split('-')[0].strip()
            #if test name already exists, ignore
            if test_name not in test_name_done:                          
                output_row.append(test_name)
                test_name_done.append(test_name)
            output_row.append(row_value[indx])
        
            if len(output_row) == len(column_names)+1:
                if_empty = 0
                #loop to check for NULL values, in this case '-'
                for num in range(len(output_row)):
                    if output_row[num] == '-':
                        if_empty = 1
                        break
                #if no NULL values, append to the final list  
                if if_empty == 0:      
                    final_output_list.append(initial_values + output_row)
                output_row = []
    #adding the items in the final list to the output dataframe
    for item in final_output_list:
        output_df.loc[len(output_df)] = item

    output_df = output_df.sort_values(by=['Name','Test_Name'],ascending=True)
    return output_df

if __name__ == "__main__":
    #file path variable
    file_path = "Input_1 - Python Developer Intern - Task 2 - Datasets.xlsx"
    output_df = conversion_func(file_path)
    output_df.to_excel('programoutput.xlsx',index = False) #final output excel file