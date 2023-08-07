## ======================================================================================= ##
## Dependencies

## Basic Packages
from basic_packages import *

## For accessing files created in python in joblib or pickle file
import joblib

### Steamlit Packages

import streamlit as st
## For importing option menu in streamlit
from streamlit_option_menu import option_menu


## ======================================================================================= ##
## Importing Functions
from machinelearning_functions import *

## ======================================================================================= ##
## SITE TITLE

## Setting Page Title
st.set_page_config(
                ## Meaning that the sidebar is not opened when visiting the site
                initial_sidebar_state="expanded", ## Other option "expanded"
                ## Page title in the tab
                page_title='Automated Data Analysis',
                layout="wide",
                page_icon = "static//coding.png"
                )

## ======================================================================================= ##




## ======================================================================================= ##
## Sidebar Settings

# from streamlit_option_menu import option_menu

# with st.sidebar:
#     selected = option_menu(
#                 menu_title='Menu',
#                 options = ['Home','Section 1'],
#                 icons = ['house','book'],
#                 menu_icon='cast',
#                 default_index = 0,
#         )


## ======================================================================================= ##
## SITE CONFIGURATION

# Note: All the contents that is about the modification of the site settings, must also be copied to every pages.

## Remove the contents in the sidebar itself, this pertains to the pages in the sidebar

# no_sidebar_style = """
#     <style>
#         div[data-testid="stSidebarNav"] {display: none;}
#     </style>
# """
# st.markdown(no_sidebar_style, unsafe_allow_html=True)


## Hide the expander itself. (sidebar)
## Note: Don't use when you are planning to use the sidebar
# st.markdown(
#     """
# <style>
#     [data-testid="collapsedControl"] {
#         display: none
#     }
# </style>
# """,
#     unsafe_allow_html=True,
# )


## Hide the github icon on the right side in the deployed app
# hide_github_icon = """
#     <style>
#     .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob, .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137, .viewerBadge_text__1JaDK{ display: none; } #MainMenu{ visibility: hidden; } footer { visibility: hidden; } header { visibility: hidden; }
#     </style>
# """
# st.markdown(hide_github_icon, unsafe_allow_html=True)


## To remove the hamburger menu (this is in the right part of the site)
# hide_streamlit_style = """
# <style>
# #MainMenu {visibility: hidden;}
# footer {visibility: hidden;}
# </style>"""
# st.markdown(hide_streamlit_style, unsafe_allow_html=True)

## ======================================================================================= ##
## Sidebar

## Sample Form
# with st.form(key ='Form1'):
#     with st.sidebar:
#         user_word = st.text_input("Enter a keyword", "habs")    
#         select_language = st.radio('Tweet language', ('All', 'English', 'French'))
#         include_retweets = st.checkbox('Include retweets in data')
#         num_of_tweets = st.number_input('Maximum number of tweets', 100)
#         submitted1 = st.form_submit_button(label = 'Search Twitter 🔎')


with st.sidebar:
    df = None
    next_step = 0
    analysis_step = 0

    with st.form(key ='Dataset Form'):

        st.header('Dataset 📄')
        st.write('Upload your dataset in CSV format here:')
        uploaded_file = st.file_uploader(label = 'hi',label_visibility='collapsed',type='csv')

        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)

        preloaded = st.selectbox('Or, use a preloaded dataset',(None,'iris',
                                                                        'tips',
                                                                        'penguins',))

        if preloaded is None:
            pass
        else:
            df = sns.load_dataset(preloaded)
            

        load_button = st.form_submit_button(label = 'Load Data')    

    if load_button:
        if df is None:
        # Can be used wherever a "file-like" object is accepted:
            st.error('No File Loaded')
        else:
            next_step = 1
            st.success(f'Dataset has been loaded!')
    
        
## ======================================================================================= ##
## SITE CONTENTS
sitedetails = st.container()
with sitedetails:
    ## Writing text in the website
    st.title('Automated Data Analysis')

    ## Writing the purpose of this web application

    ## Justify

    # st.markdown('<div style="text-align: justify;">  </div>', unsafe_allow_html=True)
    # st.write("")

    st.markdown('<div style="text-align: justify;"> The Automated EDA Analysis project revolves around a web application designed to streamline the process of Exploratory Data Analysis (EDA) for datasets. By integrating the power of data visualization libraries like Seaborn and Matplotlib along with data manipulation using Pandas, this web application offers an efficient and intuitive platform for users to input datasets or choose from pre-loaded ones. The application provides comprehensive insights, including dataset components, univariate and bivariate analyses, and correlation plots, all in a user-friendly interface and automated manner.  </div>', unsafe_allow_html=True)
    st.write("")


    st.info('You can start using this web application by uploading a dataset in csv format or by using pre-loaded dataset',
            icon = 'ℹ'
    
    )
    st.markdown("""<hr style="height:5px;border:none;color:#ffc107;background-color:#1a1e3b;" /> """, unsafe_allow_html=True)



if df is not None:
    @st.cache(allow_output_mutation=True)
    def load_data():
        return df
    
    df = load_data()
    columns,\
    missing_val,\
    data_type,\
    categorical,\
    numerical =\
    dataframe_describe_2(df)

    with st.form(key ='Target Form'):
        target = st.selectbox('What is the target/dependent variable in the dataset?',df.columns)

        target_val = st.form_submit_button(label = 'Start the Analysis')    

    # if target is not None:
    if target_val:

        tab_1,tab_2 = st.tabs(["Dataset Description", "Exploratory Data Analysis (EDA)"])

        with tab_1:
            st.header('Dataset Description')

            col1, col2 = st.columns([6,4])

            with col1:
                st.subheader('Viewing the Dataset')
                st.dataframe(df, height = 300, width = 600)
            
            with col2:
                
                st.subheader('Understanding the Dataset')

                st.info(f'This dataset has:  \n {df.shape[1]} columns and  \n {df.shape[0]} rows.', icon="ℹ")

                st.write(f'There are {len(categorical)} Categorical variable/s, They are:')
                st.markdown(categorical)

                st.write(f'There are {len(numerical)} Numerical variable/s, They are:')
                st.markdown(numerical)

            st.subheader('Missing Values')
            st.write('These are the number of missing values per column:')

            missing_val = pd.DataFrame(missing_val).T
            st.dataframe(missing_val)
        
        with tab_2:
            ## Disabling the warning in plotting
            st.set_option('deprecation.showPyplotGlobalUse', False)

            ## Data Visualization
            st.header('Exploratory Data Analysis (EDA)')

            eda_1,eda_2,eda_3 = st.tabs(["Univariate Analysis", "Bivariate Analysis", 'Correlation Plot'])

            with eda_1:
                st.subheader('Univariate Analysis')

                st.markdown('<div style="text-align: justify;"> Univariate analysis is the easiest method of quantitative data analysis. As the name suggests, “Uni,” meaning “one,” in univariate analysis, there is only one dependable variable. It is used to test the hypothesis and draw inferences. The objective is to derive data, describe and summarize it, and analyze the pattern in it. </div>', unsafe_allow_html=True)
                st.write('')
                st.write('Univariate data will be shown through count plots / bar graphs:')

                num_columns = len(df.columns)

                if num_columns == 1:
                    figsize = (6,6)
                elif num_columns <= 4:
                    figsize = (14,12)
                elif num_columns <= 9:
                    figsize = (22,20)
                elif num_columns <= 16:
                    figsize = (26,22)
                else:
                    figsize = (32,28)

                st.pyplot(
                univariate_overallplot( df = df,
                columns = df.columns, # use df.columns = all
                categorical = categorical,
                numerical = numerical,
                color = 'Set1',
                # others: 'tab10','Set1','Dark2'
                figsize = (14,12), # 26,22 for 4xn grid, 22,20 for 3xn grid, 14,12, 2xn grid, 7,6 for 1x1
                sort_categorical = 'ValueCounts', # Can be ValueCounts or Alphabetical
                bins_numerical = 'auto' # can be 'auto' or can be number
                ))
            
            with eda_2:
                st.subheader('Bivariate Analysis')

                st.write('In Bivariate Analysis, there are two variables wherein the analysis is related to cause and the relationship between the two variables.')
                st.write('Bivariate Analysis will be shown through Count Plots, Box Plots, and Histograms')


                st.markdown(f'### {target} (Target) with Categorical Variables')

                
                if target in categorical:

                        if len(categorical) == 1:
                            st.info("Plotting is not possible since the only categorical variable is the target variable itself")
                        else:
                            st.pyplot(bivariate_categorical_all(  df = df,
                                    columns = categorical,
                                    target = target,
                                    figsize = figsize,
                                    color = 'Set1',
                                    sort_categorical = 'ValueCounts', # Can be ValueCounts or Alphabetical
                    ))
                
                elif target in numerical:
                    for i in categorical:
                        if i == target:
                            continue

                        if i in df.columns:
                            st.write(f'{target} vs. {i}')
                            st.pyplot(
                            eda_bivariate_numerical(
                                    data = df,
                                    column = target,
                                    target = i,
                                    color = 'Set1',
                                    figsize=(12,6),
                                    val=0,
                                    target_type='categorical'))



                st.markdown(f'### {target} (Target) with Numerical Variables')

                if target in categorical:
                    for i in numerical:
                            if i == target:
                                continue
                            if i in df.columns:
                                st.write(f'{i} vs. {target}')
                                st.pyplot(
                                eda_bivariate_numerical(
                                        data = df,
                                        column = i,
                                        target = target,
                                        color = 'Set1',
                                        figsize=(12,6),
                                        val=0))
                
                elif target in numerical:
                    if len(numerical) == 1:
                        st.info("Plotting is not possible since the only numerical variable is the target variable itself")
                    else:
                        for i in numerical:
                            if i == target:
                                continue

                            if i in df.columns:
                                st.write(f'{i} vs. {target}')
                                st.pyplot(eda_bivariate_numeric_numeric(df = df,
                                                column = i,
                                                target = target))


            with eda_3:
                st.subheader('Correlation Plot')
                st.markdown('<div style="text-align: justify;"> A correlation matrix is a table showing correlation coefficients between variables. Each cell in the table shows the correlation between two variables. A correlation matrix is used to summarize data, as an input into a more advanced analysis, and as a diagnostic for advanced analyses.</div>', unsafe_allow_html=True)
                st.write('')

                ## Plotting the correlation matrix
                correlation_matrix = df[numerical].corr()
                cor_fig = plt.figure(figsize=(9,8))

                ## use mask to cover the upper diagonal in the matrix
                mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))

                sns.heatmap(correlation_matrix,
                            cmap='RdBu_r',
                            # cmap='RdYlGn',
                            annot=True,
                            # Masking the diagonal
                            # mask=mask,
                            fmt='.2f',
                            vmin=-1, vmax=1)
                plt.xticks(rotation = 45)
                plt.yticks(rotation = 45)

                st.pyplot(cor_fig)






