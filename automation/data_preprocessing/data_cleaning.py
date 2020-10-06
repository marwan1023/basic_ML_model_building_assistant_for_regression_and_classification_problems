'''
    This module is used to perform some basic but also neccessary tasks upto null value counts.
    Some of these are:-
        " Finding the **datatypes** for each feature "
        " Getting the **columns' name** and keeping track on them "
        " Finding the **null** values in the feature and giving the appropriate strategy 
        to deal with them "
'''
import pandas as pd
import numpy as np
import scipy.stats as stats


class Basic:
    '''This is the base class of ml-automator that serves various impartant basic task 
    required in the automation for any ml use-case.
    
    Functionalities
    =======
    1. concating the dataframe/ series; same as concat of pandas.
    2. display head of the dataset/ dataframe.
    3. display shape of the dataset/ dataframe.
    4. getting the unique values of any particular column of the dataset passed as
    a parameter.
    5. getting isnull values of the dataset/ dataframe.
    6. getting sum of isnull values of the dataset/dataframe.
    '''
    def __init__(self):
        raise NotImplementedError("Not accessible directly")

    def concat(self, *args, **kwargs):
        ''' arg is used to take dataframes/ series type objects(one or more then one)
        and kwargs is used to take parameters required to concate two dataframes/ series object. '''
        self.data = pd.concat(objs=args, **kwargs)
        return self.data

    def head(self, value=5):
        return self.data.head(value)

    @property
    def shape(self):
        return self.data.shape

    def unique(self, column):
        return self.get_col(column).unique()

    def unique_prcntg(self, column):
        return round((len(self.unique(column)) / self.data_len)*100, 2)

    def isnull(self):
        return self.data.isnull()

    def isnull_sum(self, column=None):
        ''' return sum of null values present in the dataset. '''
        if column:
            return self.isnull().sum()[column]
        return self.isnull().sum()

    @property
    def data_len(self):
        ''' return the total length of the dataset'''
        return self.shape[0]

    def isnull_sum_prcntg(self, column=None):
        ''' return the percentage of sum of null values present in the dataset. '''
        if column:
            return round((self.isnull_sum(column) / self.data_len)*100, 2)
        return round((self.isnull_sum / self.data_len)*100, 2)

    def drop(self, column, **kwargs):
        if not isinstance(column, list):
            column = [column]
        return self.data.drop(column, **kwargs)

    @staticmethod
    def dataframe(*args, **kwargs):
        return pd.DataFrame(*args, **kwargs)

    def central_tendency_finder(self, column_name, measure):
        ''' return the measure(mean, median, mode) of selected column in the dataset
        according to the parameter(measure) is passed. '''
        measure = measure.lower()
        if measure == "mode":
            return self.data[column_name].mode()[0]
        elif measure == "mean":
            return self.data[column_name].mean()
        elif measure == "median":
            return self.data[column_name].median()
        else:
            raise AttributeError(f"Wrong attribute is passed; {measure} measure is not recognized")

    def inter_quartile_range(self, column_name):
        """
        Returns the inter quartile range for any particular feature.
        The inter quartile range is the difference b/w Q3 and Q1 i.e.
        75% - 25% and basically its the midspread of the data.
        """
        return self.data[column_name].apply(stats.iqr)

    def Q1(self, column_name):
        """
        Returns the first quantile for the column of the dataset.
        """
        return self.data[column_name].quantile(q=.25)

    def Q3(self, column_name):
        """
        Returns the third quantile for the column of the dataset.
        """
        return self.data[column_name].quantile(q=.75)

    def col_minval(self, column_name):
        """
        Returns the min value of the feature
        """
        return self.data[column_name].min()


class Columns(Basic):
    '''Takes in the main data i.e. dataframe object performs certain task to deal
    with features of the dataset.
    
    Example
    ========
    >>> df = Column(dataframe)
    >>> df.column_name
    return "total column names as list type object."
    
    >>> df.cat_col()
    return "All categorical features of the dataset if present; return type list"
    
    >>> df.num_col()
    return "All numerical features of the dataset if present; return type list"
    
    >>> df.is_cat([column])
    return True "if column is of categorical type"
    
    >>> df.is_cat([columns,])
    return True "if all columns are of categorical type"
    if "all columns are not of categorical type":
        return "column name that are of categorical type"
    else:
        return "column is not of categorical type"
    
    >>> df.is_num([column/ columns])     
    # Does the same work as done by is_cat but this time its for numerical feature
    
    >>> df.track_col()    # ------- this method is used by child class to overwrite.
    '''

    def __init__(self, *args):
        if len(args) == 1:
            self.data = args[0]
        else:
            # Data can be already divided into train and test datas.
            self.data = self.concat(*args, **dict(axis=0, ignore_index=True))

    @property
    def column_name(self):
        return list(self.data.columns)

    def get_col(self, column):
        return self.data[column]

    def col_len(self):
        ''' return the total length of columns of the dataset '''
        return self.shape[1]

    def cat_col(self):
        ''' Keeps track of only categorical features of the dataset '''
        _dict = self.data_type()
        categorical_col = _dict.get("categorical_feature", None)
        if categorical_col is None:
            return("There is no categorical feature present in the dataset.")
        return categorical_col

    def num_col(self):
        ''' Keeps tracks of only numerical features of the dataset '''
        _dict = self.data_type()
        numerical_col = _dict.get("numerical_feature", None)
        if numerical_col is None:
            return("There is no numerical feature present in the dataset.")
        return numerical_col

    def is_cat(self, *args):
        '''args takes column names as list type object'''
        _dict = self.data_type(*args)
        categorical_col = _dict.get("categorical_feature", None)
        
        if categorical_col is None:
            return(f"{args[0]} not found.")
        
        if categorical_col == args[0]:
            return True
        return f" Only {tuple(categorical_col)} is of categorical type."

    def is_num(self, *args):
        '''args takes column names as a list type object'''
        _dict = self.data_type(*args)
        numerical_col = _dict.get("numerical_feature", None)
        if numerical_col is None:
            return(f"{args[0]} not found")
        
        if numerical_col == args[0]:
            return True
        
        return f" Only {tuple(numerical_col)} is of numeric type."

    def track_col(self):
        ''' Track all of the columns along with their datatypes;
        implemented in the child class. '''
        pass


class DataType(Columns):
    ''' Finds datatypes of every features and categorize the features accordingly into
    categorical or numerical features. '''
    def __init__(self, *args):
        Columns.__init__(self, *args)

    def track_col(self, *args):
        ''' Args takes column name as list type object.
        
        This method is used to get datatypes of features and return the output as
        dictionary object.
        >>> return {column_name: column_type}
        '''
        column_name = None
        if args:
            column_name = args[0]
        else:
            column_name = self.column_name
        df = self.data
        self._dict = dict((features, df[features].dtype) for features in column_name)
        return self._dict

    def data_type(self, *args):
        ''' Args take column names as list type object.
        >>> data_type([columns])
        
        If column names are passed all of
        the computation is done for the particular columns but if not the default computation
        is done for each feature of the dataset.
        
        Return a dictionary object with names of categorical and numerical features.
        
        >>> return {'categorical_feature': [column_names], 'numerical_feature': [column_names]}
        '''
        features_type = None
        cat_list = []
        num_list = []
        
        if args:
            features_type = self.track_col(*args).items()
        else:
            features_type = self.track_col().items()
        
        for col_name, col_type in features_type:
            if 'int' in str(col_type):
                if self.unique_prcntg(col_name) <= 0.5:
                    # categorial feature; numerical type
                    cat_list.append(col_name)
                else:
                    # Numerical feature; discreate type
                    num_list.append(col_name)
                    
            elif col_type == "object":
                # Categorial feature; non-numeric type
                cat_list.append(col_name)
            elif 'float' in str(col_type):
                # Numerical feature; continous type
                num_list.append(col_name)
            else:
                raise AttributeError(f"Wrong datatype encountered; {col_type} is not recognized.")
            
        return dict(
            categorical_feature = cat_list,
            numerical_feature = num_list,
        )


class DataCleaner(DataType):
    def auto_process(self):
        done = None
        cntrl_tndncy_meas = None
        for column in self.column_name:
            null_percentage = self.isnull_sum_prcntg(column)
            if null_percentage == 0:
                done = 'skipped'
            elif  null_percentage <= 40:
                if self.is_cat([column]):
                    cntrl_tndncy_meas = self.central_tendency_finder(column, 'mode')
                else:
                    cntrl_tndncy_meas = self.central_tendency_finder(column, 'mean')
                done = 'filled'
                self.null_filler(column, cntrl_tndncy_meas)
            else:
                done = 'dropped'
                self.drop(column, axis=1, inplace=True)
            
            if done == "skipped":
                yield(f"The {column} column is {done} as it didn't have any kind of null values")
            elif done == "dropped":
                yield(f"The {column} column is {done} as it has {null_percentage}% of the null values.")
            else:
                yield(f"The {column} column is {done} with the value of {cntrl_tndncy_meas}")

    def manual_process(self, column_name, parameter):
        """
        This takes a parameter from the user and according to that it process the data.
        
        parameter:- input type must be of str. It takes one of the (Drop, mean, median, mode)
        value.
        """
        if "drop" in parameter:
            self.drop(column_name, axis=1, inplace=True)
        else:
            value = self.central_tendency_finder(column_name, parameter)
            self.null_filler(column_name, value)

    def id_remover(self):
        for column in self.num_col():
            is_id = False
            
            if "id" in column.lower():
                is_id = True
            
            if is_id:
                prcntage = self.unique_prcntg(column)
                if prcntage >= 80:
                    self.id_col = self.dataframe(self.get_col(column), columns=[column])
                    self.drop(column=column, axis=1, inplace=True)
                    return self.id_col
                return f"Is the {column} column is the ID for the dataset."
        return "There is no Id column present in the dataset."

    def null_filler(self, column_name, value):
        ''' Fill the null values of the feature with the attribute(value) passed '''
        self.data[column_name] = self.data[column_name].fillna(value)


# -------------------------------------
#               Testing
# -------------------------------------


# ---------- only one data ------------
print('-'*50)
print('\t \t Testing no. 1')
print('-'*50)
df = pd.read_csv(r'../../example_datasets/titanic.csv')

# ------- defining the object ---------
df_obj = DataCleaner(df)
print()

# ---------- column names -------------
print('---------- column names -------------')
print(df_obj.column_name)
print()

# --------- tracking column -----------
print('-------- tracking column -----------')
print(df_obj.track_col())
print()

# ----- only categorical column -------
print('----- only categorical column -------')
print(df_obj.cat_col())
print()

# ------ only numerical column --------
print('------ only numerical column --------')
print(df_obj.num_col())
print()

# --------- is cat column? ------------
print('--------- is cat column? ------------')
print(df_obj.is_cat(["Name", "Age"]))
print()

# --------- is num column? ------------
print('--------- is num column? ------------')
print(df_obj.is_num(["Name", "Age"]))
print()

# ------- head of the dataset ---------
print('------- head of the dataset ---------')
print(df_obj.head())
print()

# ------- shape of the dataset --------
print('------- shape of the dataset --------')
print(df_obj.shape)
print()

# --------- checking isnull -----------
print('--------- checking isnull -----------')
print(df_obj.isnull())
print()

# ----------- isnull sum --------------
print('----------- isnull sum --------------')
print(df_obj.isnull_sum())
print()

# -------- manual data cleaner --------
print('-------- manual data cleaner --------')
print(df_obj.manual_process('Cabin', 'drop'))
print()

# --------- auto data cleaner ---------
print('--------- auto data cleaner ---------')
for _ in df_obj.auto_process():
    print(_)
print()

# ----------- isnull sum --------------
print('----------- isnull sum --------------')
print(df_obj.isnull_sum())
print()

# ----------- id remover --------------
print('----------- id remover --------------')
print(df_obj.id_remover())
print()

# ----------- id remover --------------
print('----------- id remover --------------')
print(df_obj.id_remover())
print()

# ------- head of the dataset ---------
print('------- head of the dataset ---------')
print(df_obj.head())
print()


# -------------------------------------
#            Testing no.2
# -------------------------------------


# ----------- two datas ---------------

print('-'*50)
print('\t \t Testing no. 2')
print('-'*50)
data = {'Name': ['Tom', 'nick', 'krish', 'jack'], 'Age': [20, 21, 19, 18]}
data2 = {'Name':['galla', 'uba', 'lilu', 'lala'], 'Age':[34, 24, 1, 69]}

# ------- defining the object ---------
df_obj2 = DataCleaner(*[pd.DataFrame(data), pd.DataFrame(data2)])
print()

# ---------- column names -------------
print('---------- column names -------------')
print(df_obj2.column_name)
print()

# --------- tracking column -----------
print('-------- tracking column -----------')
print(df_obj2.track_col())
print()

# ----- only categorical column -------
print('----- only categorical column -------')
print(df_obj2.cat_col())
print()

# ------ only numerical column --------
print('------ only numerical column --------')
print(df_obj2.num_col())
print()

# --------- is cat column? ------------
print('--------- is cat column? ------------')
print(df_obj2.is_cat(["Name", "Age"]))
print()

# --------- is num column? ------------
print('--------- is num column? ------------')
print(df_obj2.is_num(["Name", "Age"]))
print()

# ------- head of the dataset ---------
print('------- head of the dataset ---------')
print(df_obj2.head())
print()

# ------- shape of the dataset --------
print('------- shape of the dataset --------')
print(df_obj2.shape)
print()

# --------- checking isnull -----------
print('--------- checking isnull -----------')
print(df_obj2.isnull())
print()

# ----------- isnull sum --------------
print('----------- isnull sum --------------')
print(df_obj2.isnull_sum())
print()



# Basic()

# must save the original data
# concat option---> done..
# column_name option ---> done..
# datatype_tracker ---> done..

# class new(pandas):
#     def __init__(self, df):
#         pass

# class Base(pd.DataFrame):
#     def __init__(self , *args):
#         pd.DataFrame.__init__(self, *args)


# df = Base(df)
# print(df.head())

# class New(Base):
#     def new(self):
#         self.head()

# df = New(df)
# print(df.new())
