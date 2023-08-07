## Basic Packages
from basic_packages import *

import streamlit as st
## For importing option menu in streamlit
from streamlit_option_menu import option_menu


def univariate( df,
                columns,
                categorical,
                numerical,
                figsize,
                color,
                sort_categorical = 'ValueCounts', # Can be ValueCounts or Alphabetical
                bins_numerical = 'auto' # or can be number
               ):

    color = color
    palette_color = sns.color_palette(color)

    if type(columns) == str:
        columns = [columns]

    for i in columns:   
        if sort_categorical == 'ValueCounts':
            order = df[i].value_counts().index
        elif sort_categorical == 'Alphabetical':
            order = np.sort(df[i].unique())

        if i in categorical:
            if df[i].nunique() > 15:
                print(f'column {i} has many unique values n = {df[i].nunique()} and will not be plotted')
                print('=======================================================')
                continue
            else:
                print(f'{i}')
                fig,ax = plt.subplots(figsize = figsize)
                ax = sns.countplot(x = i, 
                    data=df,
                    palette=color,
                    order = order,
                    edgecolor = "black"
                    )
                ax.set_ylabel('Count')

                patches = ax.patches

                for j in range(len(patches)):
                    # list_unq_val = list(df[i].unique())

                    # cleaned = [x for x in list_unq_val if str(x) != 'nan']
                    offset = df[i].value_counts().max() * 0.01
                    percentage = list(df[i].value_counts())[j]/df[i].value_counts().sum()
                    x = patches[j].get_x() + patches[j].get_width()/2
                    y = patches[j].get_height()+ offset
                    ax.annotate('{:.1f}%'.format(percentage*100), (x, y), ha='center')

                plt.xticks(rotation = 45)
                    
                plt.show()
                print('=======================================================')
        
        elif i in numerical:
            print(f'{i}')
            fig,ax = plt.subplots(figsize = figsize)

            ax = sns.histplot(x = i, 
                    data=df,
                    bins = bins_numerical,
                    kde = True,
                    color=palette_color[0],
                    )
            ax.set_ylabel('Count')
            plt.show()
            print('=======================================================')


## printing the shape and head
def head(df,shape_only=False):
    print(df.shape)

    if shape_only:
        return
    else:
        return df.head()

## describing the dataframe
def dataframe_describe(df):
    columns = df.columns.tolist()
    print('=======================================================')
    print(f'There are {df.shape[0]} rows and {len(df.columns.tolist())} columns in the dataframe')
    print('=======================================================')
    print(f'These are the column names of the dataframe: \
        {columns}')

    print('=======================================================')

    categorical = df.select_dtypes(exclude=['float64']).columns.tolist()

    print(f'These are the {len(categorical)} categorical columns in the dataframe: \
        {categorical}')
    
    print('=======================================================')

    numerical = df.select_dtypes(include=['float64']).columns.tolist()


    print(f'These are the {len(numerical)} numerical columns in the dataframe: \
        {numerical}')

    print('=======================================================')

    data_type = df.dtypes

    print(f'These are the datatypes of each column in the dataframe: \
        {data_type}')
    
    print('=======================================================')
    
    missing_val = df.isna().sum()

    print(f'These are the missing values per column in the dataframe: \
        {missing_val}')

    print('=======================================================')
    
    print('These are the information of the dataframe')
    print(df.info())

    print('=======================================================')

    return columns,\
           missing_val,\
           data_type,\
           categorical,\
           numerical, 

## Cardinality count of categorical features
def cardinality_cat(df,categorical):
    print("cardinality of categorical features in training datasets is:")
    print(df[categorical].nunique())



## if you want to set the dtype of your columns for later purposes
def column_dtype_manual(df):
    categorical = []
    numerical = []
    ordinal = []

    for i in df.columns:
        dtype = input(f' Is {i} a Categorical,Numerical, or Ordinal Variable? Choose from: c, n, and o. Respectively')

        if dtype == 'c':
            categorical.append(i)
        
        if dtype == 'n':
            numerical.append(i)
        
        if dtype == 'o':
            ordinal.append(i)

    return categorical, numerical, ordinal

## for EDA of categorical values
def eda_bivariate_categorical(  df,
                                column,
                                target,
                                color,
                                sort_categorical,
                                ):

    fig,ax = plt.subplots(figsize = (9,8))

    color = color

    palette_color = sns.color_palette(color)

    if sort_categorical == 'ValueCounts':
        order = df[column].value_counts().index
    elif sort_categorical == 'Alphabetical':
        order = np.sort(df[column].unique())

    ax = sns.countplot(x = column, data=df, hue=target,palette=color,order = order,edgecolor = "black",)
    ax.set_ylabel('Count')

    ax.set_xticklabels(labels=order,rotation = 45)

    offset = df[column].value_counts().max() * 0.005

    list_bars = df.groupby([column,target])[column].agg(['count']).unstack().fillna(0).values

    patches = ax.patches
    bars_pos = 0

    for i in range(df[target].nunique()):
        for j in range(df[column].nunique()):
            list_bars_col = list_bars[j] 
            total_sum = list_bars_col.sum()
            value = list_bars_col[i]

            percentage = value / total_sum

            if percentage == 0:
                bars_pos += 1
                continue
            else:
                x = patches[bars_pos].get_x() + patches[j].get_width()/2
                y = patches[bars_pos].get_height() + offset
                ax.annotate('{:.1f}%'.format(percentage*100), (x, y), ha='center')
                bars_pos += 1
    plt.show()

def bivariate_categorical_all( df,
                            columns,
                            target,
                            figsize,
                            color,
                            sort_categorical = 'ValueCounts', # Can be ValueCounts or Alphabetical
               ):
    color = color
    palette_color = sns.color_palette(color)

    nrows, ncol = get_dimension(columns)

    if len(columns) == 1:
        st.write("Plotting is not possible since the only categorical variable is the target variable itself")
        return

    fig,axes = plt.subplots(nrows, ncol, figsize=figsize)
    val = 0

    ## Check if the target variable is the last in the categorical column
    if target == columns[len(columns)-1]:
        columns.reverse()



    for m in range(nrows):

        for n in range(ncol):

            if nrows == 1 and ncol == 1:
                axes_pos = axes
            elif nrows * ncol <= 2:
                axes_pos = axes[val]
            else:
                axes_pos = axes[m,n]

            if val in range(len(columns)):

                if columns[val] == target:
                    val += 1

                if sort_categorical == 'ValueCounts':
                    order = df[columns[val]].value_counts().index
                elif sort_categorical == 'Alphabetical':
                    order = np.sort(df[columns[val]].unique())
                
                ax = sns.countplot(x = columns[val], data=df, hue=target,palette=color,order = order,edgecolor = "black",ax = axes_pos)

                ax.set_ylabel('Count')

                ax.set_xticklabels(labels=order,rotation = 45)

                offset = df[columns[val]].value_counts().max() * 0.005

                list_bars = df.groupby([columns[val],target])[columns[val]].agg(['count']).unstack().fillna(0).values

                patches = ax.patches
                bars_pos = 0

                for i in range(df[target].nunique()):
                    for j in range(df[columns[val]].nunique()):
                        list_bars_col = list_bars[j] 
                        total_sum = list_bars_col.sum()
                        value = list_bars_col[i]

                        percentage = value / total_sum

                        if percentage == 0:
                            bars_pos += 1
                            continue
                        else:
                            x = patches[bars_pos].get_x() + patches[j].get_width()/2
                            y = patches[bars_pos].get_height() + offset
                            ax.annotate('{:.1f}%'.format(percentage*100), (x, y), ha='center')
                            bars_pos += 1
                
                val += 1
                plt.tight_layout()

                
            else:
                ## This is to remove the extra plots
                fig.delaxes(axes[m,n])

    plt.show()



## Function that plots numerical variables into histogram and violin plot
def eda_bivariate_numerical(data,column,target,color,
                    figsize=(12,6),
                    # save=True,
                    val=0,
                    target_type = 'Numerical'):

    fig, axes = plt.subplots(1, 2, figsize=figsize)
    cmap = sns.color_palette(color)
    val = val

    for i in range(1):
        for j in range(2):
            if j==0:
                    sns.histplot(data = data,x=data[column],hue=target,
                                bins=50,kde=True,palette=color,ax=axes[j])
                    axes[j].set(xlabel=None)
                    axes[j].grid(False)
            elif j==1:
                sns.boxplot(data = data,x=data[column],y = target, ax=axes[j], palette=color,orient='h',
                )
                axes[j].set(xlabel=None)
                axes[j].grid(False)
                val += 1
                plt.tight_layout()
            if target_type == 'Numerical':
                plt.suptitle(column)
            else:
                plt.suptitle(f'{column} vs. {target}')
    plt.show()
    
    # path = 'Figures\\Numerical\\'
    # if save:
    #     plt.savefig(f"{path}{column}.pdf",dpi=1000)

def eda_bivariate_numeric_numeric(df,column,target):

    fig,ax = plt.subplots(figsize = (9,8))

    color = 'Set2'

    palette_color = sns.color_palette(color)

    ax = sns.scatterplot(x = target, data=df, y =column,color = palette_color[0])

    plt.show()


def update_col_type(df,col_type):
    for i in col_type:
        if i not in df.columns:
            col_type.remove(i)




def dataframe_describe_2(df):
    columns = df.columns.tolist()

    categorical = df.select_dtypes(exclude=['float64']).columns.tolist()



    numerical = df.select_dtypes(include=['float64']).columns.tolist()




    data_type = df.dtypes


    

    
    missing_val = df.isna().sum()





    return columns,\
           missing_val,\
           data_type,\
           categorical,\
           numerical,

def get_dimension(column):
    length = len(column)
    if length == 1:
        m = 1
        n = 1
    elif length == 2:
        m = 1
        n = 2
    else:
        initial = 2
        initial_2 = 1
        while length > initial**2:
            initial = initial + 1
        
        n = initial

        while length > initial_2*n:
            initial_2 = initial_2 + 1
        
        m = initial_2
    return m,n

def univariate_overallplot( df,
                columns,
                categorical,
                numerical,
                figsize,
                color,
                sort_categorical = 'ValueCounts', # Can be ValueCounts or Alphabetical
                bins_numerical = 'auto' # or can be number
               ):

    color = color
    palette_color = sns.color_palette(color)

    if type(columns) == str:
        columns = [columns]


    nrows, ncol = get_dimension(columns)

    fig,axes = plt.subplots(nrows, ncol, figsize=figsize)
    val = 0


    for m in range(nrows):

        for n in range(ncol):

            if nrows == 1 and ncol == 1:
                axes_pos = axes
            elif nrows * ncol <= 2:
                axes_pos = axes[val]
            else:
                axes_pos = axes[m,n]

            if val in range(len(columns)):
                
                if sort_categorical == 'ValueCounts':
                    order = df[columns[val]].value_counts().index
                elif sort_categorical == 'Alphabetical':
                    order = np.sort(df[columns[val]].unique())

                if columns[val] in categorical:
                    if df[columns[val]].nunique() > 15:
                        print(f'column {columns[val]} has many unique values n = {df[columns[val]].nunique()} and will not be plotted')
                        val += 1
                        continue
                    else:
                        ax = sns.countplot(x = columns[val], 
                            data=df,
                            palette=color,
                            order = order,
                            edgecolor = "black",
                            ax = axes_pos
                            )
                        ax.set_ylabel('Count')

                        patches = ax.patches

                        for j in range(len(patches)):
                            # list_unq_val = list(df[i].unique())

                            # cleaned = [x for x in list_unq_val if str(x) != 'nan']
                            offset = df[columns[val]].value_counts().max() * 0.01
                            percentage = list(df[columns[val]].value_counts())[j]/df[columns[val]].value_counts().sum()
                            x = patches[j].get_x() + patches[j].get_width()/2
                            y = patches[j].get_height()+ offset
                            ax.annotate('{:.1f}%'.format(percentage*100), (x, y), ha='center')

                        ax.set_xticklabels(labels=order,rotation = 45)

                        val += 1
                        plt.tight_layout()
                
                elif columns[val] in numerical:

                    ax = sns.histplot(x = columns[val], 
                            data=df,
                            bins = bins_numerical,
                            kde = True,
                            color=palette_color[0],
                            ax = axes_pos,
                            )
                    ax.set_ylabel('Count')
                    val += 1
                    plt.tight_layout()

            else:
                ## This is to remove the extra plots
                fig.delaxes(axes[m,n])