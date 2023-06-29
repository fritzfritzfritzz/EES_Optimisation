def read_csv_files_in_directory(directory):
    '''
    reads all .csv files within given directory into pandas dataframe
    objects and returns a list of these dataframes
    param:
    directory: directory path (str)
    '''
    file_list = [file for file in os.listdir(directory) if file.endswith('.csv')]
    dataframes = []

    for file in file_list:
        file_path = os.path.join(directory, file)
        df = pd.read_csv(file_path)
        dataframes.append(df)

    #concatenated_df = pd.concat(dataframes, ignore_index=True)
    return dataframes

def time_cleanup(df):
    ''' 
    1st: add the starting time to the date column 
    2nd: transform the date column into datetime format
    '''
    df.Date = df.Date + ' ' + df.Start 
    df.Date = pd.to_datetime(df.Date, format=('%b %d, %Y %I:%M %p')) 
    return df

def add_one(number):
    return number + 1

def divide(x, y):
    """ Devision function """
    if y == 0:
        return "Can not divide by zero"
    return x // y
