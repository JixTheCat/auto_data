# import warnings
# warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import numpy as np

#############
# variables

threshold = 2.5
minimum_count = 5


def zscore(df: np.array):
    """Returns the z score for np.array within a pandas dataframe.

    Args:
        df: an np.array

    Returns:
        An array of z-scores
    """
    return (df - df.mean())/df.std()


def cond_problem(col1: np.array, col2: np.array, two_way=False):
    """Returns an array indicating the presence of Nans.

    Args:
        col1: An array of values that require corresponding values in
            to be present in col2.
        col2: An array of values that pertain to col1, values that are
            required to be present in a row if a value is present
            in col1
        two_way: If two_way is True then the returned column will be
            'Yes' if either column was missing a value. But not if
            both were.

    Returns:
        An array of 'Yes's for each row when a value is in col 1 but
            not in col2.
    """
    df = pd.DataFrame(
        {'col1': col1, 'col2': col2})

    # remove when both are Nan
    df = df.dropna(axis=0, how='all')
    if not two_way:
        df = df[df['col1'].notna()]

    # change values to binaries
    df.loc[df['col1'].notna(), 'col1'] = 1.0
    df.loc[df['col2'].notna(), 'col2'] = 1.0

    # select when there is only one value
    df = df['col1'] * df['col2']

    return df[df != 1].fillna('Yes')


def climate(region: str):
    if region in ['Macedon Ranges',
                  'Mornington Peninsula',
                  'Orange', 'Canberra District', 'Yarra Valley',
                  'Beechworth',  'Upper Goulburn',
                  'Strathbogie Ranges',
                  'Southern Fleurieu', 'Adelaide Hills']:
        return 'Cool Damp'
    if region in ['Mount Gambier', 'Henty', 'Grampians',
                  'Kangaroo Island', 'Sunbury', 'Wrattonbully',
                  'Coonawarra', 'Robe', 'Mount Benson']:
        return 'Cool Dry'
    if region in ['Geelong', 'Pyrenees']:
        return 'Cool Very Dry'
    if region in ['Alpine Valleys', 'Pemberton', 'Tumbarumba']:
        return 'Mild Damp'
    if region in ['Blackwood Valley',
                  'Eden Valley',
                  'Manjimup',
                  'Granite Belt',
                  'Currency Creek',
                  'Padthaway',
                  'Heathcote']:
        return 'Mild Dry'
    if region in ['Great Southern', 'McLaren Vale', 'Bendigo']:
        return 'Mild Very Dry'
    if region in ['Geographe', 'New England Australia',
                  'Shoalhaven Coast', 'Southern Highlands',
                  'Margaret River']:
        return 'Warm Damp'
    if region in ['Peel', 'Gundagai', 'Glenrowan',
                  'Pericoota','Clare Valley', 'Mudgee']:
        return 'Warm Dry'
    if region in ['Rutherglen', 'Goulburn Valley', 'Langhorne Creek',
                  'Barossa Valley']:
        return 'Warm Very Dry'
    if region in ['Hunter Valley', 'Hastings River']:
        return 'Hot Damp'
    if region in ['Perth Hills', 'Swan District' 'Southern Flinders Ranges']:
        return 'Hot Dry'
    if region in ['South Burnett',
                  'Cowra',
                  'Riverina',
                  'Adelaide Plains',
                  'Riverland',
                  'Swan Hill',
                  'Murray Darling']:
        return 'Hot Very Dry'
    return 'Unknown Climate'


def size(tonnes: float):
    if tonnes < 500:
        return 'Small'
    if tonnes < 10000:
        return 'Medium'
    return 'Large'
    # Sizes:
    # Vlarge > 20k
    # large < 20k
    # med < 10k
    # small < 500
    # micro < 100

##########
# Data in:

def data_in():
    return pd.read_excel(
        'data.xlsx',
        sheet_name='Vineyard',
        index_col='Membership Number')

###################
# Data transformations

def data_transform(df):
    #df = df[~df['Paid At'].isnull()]
    df = df.fillna(0)
    df['Total Vineyard Area'] = df['Red grapes'] + df['White grapes']
    df['t/ha'] = df['Grapes harvested'] / df['Total Vineyard Area']
    df['Total water used'] = df['River water'] + df['Groundwater'] + \
        df['Surface water dam'] + df['Recycled water from winery'] + \
        df['Recycled water from other source'] + df['Mains water'] + \
        df['Other water'] + df['Water applied for frost control']
    df['ml/ha'] = df['Total water used'] / df['Total Vineyard Area']
    df['ml/t'] = df['Total water used'] / df['Grapes harvested']
    df['total irrigation'] = df['Irrigation type - Dripper'] + \
        df['Irrigation type - Undervine Sprinkler'] + \
        df['Irrigation type - Overhead Sprinkler'] + \
        df['Irrigation type - Flood'] + \
        df['Irrigation type - Non-irrigated']
    df['total fuel'] = df['Petrol (L)'] + \
        df['LPG (L)'] +\
        df['Diesel (L)'] + \
        df['Biodiesel (L)']
    df['fuel / t'] = df['total fuel'] / df['Grapes harvested']
    df['#No. Passes'] = df['Slashing Number of times/passes per year'] + \
        df['Fungicide spraying Number of times/passes per year'] + \
        df['Insecticide spraying Number of times/passes per year'] + \
        df['Herbicide spraying Number of times/passes per year']
    df['Applied Fertiliser'] = df['Applied']
    for i in range(1, 6):
        df['Applied Fertiliser'] += df['Applied.{}'.format(i)]

    df['fertiliser/ha'] = df['Applied Fertiliser'] / \
                         df['Total Vineyard Area']
    df['fertiliser/tonnes'] = df['Applied Fertiliser'] / \
        df['Grapes harvested']
    df['total cover'] = df['Annual cover crop'] + \
        df['Permanent cover crop non native'] + \
        df['Permanent cover crop volunteer sward'] + \
        df['Permanent cover crop - native'] + \
        df['Bare soil']
    df['irrigation count'] = \
        (df['Irrigation type - Dripper'] > 0)*1 +\
        (df['Irrigation type - Undervine Sprinkler'] > 0)*1 +\
        (df['Irrigation type - Overhead Sprinkler'] > 0)*1 +\
        (df['Irrigation type - Flood'] > 0)*1 +\
        (df['Irrigation type - Non-irrigated'] > 0)*1
    df['irrigation%'] = \
        df['total irrigation'] / \
        df['Total Vineyard Area']
    df['area not harvested'] =\
        df['Frost'] +\
        df['Non-sale'] +\
        df['New development / redevelopment'] +\
        df['Pest/disease']

    df['Climate'] = df['GI Region'].apply(climate)

    return df.replace({0: np.nan})

df = data_in()
df = data_transform(df)
problems = pd.DataFrame(index=df.index)

###################
# Finding problems using radicals
for col in ['t/ha', 'ml/ha', 'ml/t', 'fuel / t', '#No. Passes',
            'fertiliser/ha', 'fertiliser/tonnes', 'irrigation%']:

    #TODO
    # check by zone as well as region
    gp = df.groupby('GI Region')
    regions = []
    counts = gp[col].count()
    for region in counts.index:
        if counts.loc[region] > minimum_count:
            regions.append(region)
    gp = df[df['GI Region'].isin(regions)].groupby('GI Region')
    #
    df_temp = gp[col].transform(zscore)
    df_temp = pd.concat(
        (df_temp[df_temp > threshold], df_temp[df_temp < -threshold]),
        axis=0)
    cl = df.groupby('Climate')
    cl_temp = cl[col].transform(zscore)
    cl_temp = pd.concat(
        (cl_temp[cl_temp > threshold], cl_temp[cl_temp < -threshold]),
        axis=0)

    problems['Unusual ' + col] = np.nan
    problems['Unusual ' + col].fillna(cl_temp, inplace=True)
    problems['Unusual ' + col].fillna(df_temp, inplace=True)
    #problems['Unusual ' + col + ' (by region)'] = np.nan
    #problems['Unusual ' + col + ' (by region)'].fillna(df_temp, inplace=True)
    #problems['Unusual ' + col + ' (by climate)'] = np.nan
    #problems['Unusual ' + col + ' (by climate)'].fillna(cl_temp, inplace=True)


    #problems.drop(columns='temp')

    df_temp = None
    cl_temp = None

#################################
# Finding problems conditionally

# If using water they need a source of irrigation
problems['Using water without irrigation'] = cond_problem(
    df['total irrigation'], df['Total water used'])

# look for people entering 100 as a percentage instead of the actual
# amount of ha
problems['Using percentages instead of ha/ml'] = np.nan
df_conc = pd.concat(
    [df[df['Total Vineyard Area']!=100][df['total irrigation']==100]
    , df[df['Total Vineyard Area']!=1][df['total irrigation']==1]]
)
problems['Using percentages instead of ha/ml'] = cond_problem(
    df_conc[
        ~df_conc.index.duplicated(
            keep='first')]['Data Reporting Year']
    , problems['Using percentages instead of ha/ml']
)

# Look for people who have listed there developed hectares as separate
# from their total. i.e 5ha crop with 1 ha developed and 6 ha
# irrigated
problems['Not included developed hectares'] = np.nan
df_conc = pd.concat([df[
            df['Total Vineyard Area'] +
            df['New development / redevelopment']
            == df['total irrigation']],
        df[df['Total Vineyard Area'] +
            df['New development / redevelopment']
            == df['total cover']]],
        axis=0)
problems['Not included developed hectares'] = cond_problem(
    df_conc[
        ~df_conc.index.duplicated(
            keep='first')]['Data Reporting Year']
    , problems['Not included developed hectares']
)

# ML water entered as irrigated ha as well (ignore this if it is 1 ML
# per 1 ha, as the ratio will make the ML = ha irrigated)
problems['Area irrigated entered as ML used'] = np.nan
problems['Area irrigated entered as ML used'] = cond_problem(
    df[
        df['Total Vineyard Area'] / df['Total water used'] != 1][
        df['Total water used'] == df['total irrigation']
        ]['Total water used'],
    problems['Area irrigated entered as ML used'])

# - Irrigated land needs to add up to ha of crop - it can go over 100%
problems['Irrigated land does not add up to ha of crop'] = np.nan
problems['Irrigated land does not add up to ha of crop'] = \
    cond_problem(
        df[df['total irrigation'] < df['Total Vineyard Area']]
        ['Data Reporting Year']
        , problems['Irrigated land does not add up to ha of crop']
    )

# - If they have only one source it needs to add up to 100%
problems['Irrigated area below 100% when using single system'] = \
    np.nan
problems['Irrigated area below 100% when using single system'] = \
    cond_problem(
        df[df['irrigation count'] == 1]
        [df['total irrigation'] != round(
            df['Total Vineyard Area'], 3)]
        ['Data Reporting Year']
        , problems['Irrigated area below '
                   '100% when using single system']
    )

# total vineyard not harvested was more than vineyard total area
problems['area not harvested was more than total area'] = np.nan
problems['area not harvested was more than total area'] = \
    cond_problem(
        df[df['area not harvested'] > df['Total Vineyard Area']]
        ['Data Reporting Year']
        , problems['area not harvested was more than total area']
    )

"""
problems['Total area harvested greater than vineyard size'] = np.nan
problems['Total area harvested greater than vineyard size'] = \
    cond_problem(
        df[df['total irrigation'] > df['Total Vineyard Area']]
        ['Data Reporting Year']
        , problems['Total area harvested greater than vineyard size']
    )"""


# Undervine
# Total undervine vs total ha. Has to add up to 100%
# total ha vs inter row is 100% ha
# exclude livestock and include livestock
problems['total undervine does not add up to vineyard area'] = np.nan
problems['total undervine does not add up to vineyard area'] = \
cond_problem(
    df[df['total cover'] < df['Total Vineyard Area']]
    [df['total cover'] + df['Livestock grazing'] !=
        df['Total Vineyard Area']]
    ['Data Reporting Year']
    , problems['total undervine does not add up to vineyard area']
)

# Other was not filled out for undervine
problems['Undervine Other is not filled out'] = cond_problem(
    df['Other'],
    df['If you selected other, please tell us what you are using'
       ' undervine'])

# contractors
df['Mechanical harvesting'] = df['Mechanical harvesting'].fillna(0)
df.loc[df['Mechanical harvesting'] != 'We perform',
       'Mechanical harvesting'] = 0
df.loc[df['Mechanical harvesting'] == 'We perform',
       'Mechanical harvesting'] = 1

df['Mechanical pruning'] = df['Mechanical pruning'].fillna(0)
df.loc[df['Mechanical pruning'] != 'We perform',
       'Mechanical pruning'] = 0
df.loc[df['Mechanical pruning'] == 'We perform',
       'Mechanical pruning'] = 1

df['Slashing'] = df['Slashing'].fillna(0)
df.loc[df['Slashing'] != 'We perform',
       'Slashing'] = 0
df.loc[df['Slashing'] == 'We perform',
       'Slashing'] = 1

df['Fungicide spraying'] = df['Fungicide spraying'].fillna(0)
df.loc[df['Fungicide spraying'] != 'We perform',
       'Fungicide spraying'] = 0
df.loc[df['Fungicide spraying'] == 'We perform',
       'Fungicide spraying'] = 1

df['Insecticide spraying'] = df['Insecticide spraying'].fillna(0)
df.loc[df['Insecticide spraying'] != 'We perform',
       'Insecticide spraying'] = 0
df.loc[df['Insecticide spraying'] == 'We perform',
       'Insecticide spraying'] = 1

df['Herbicide spraying'] = df['Herbicide spraying'].fillna(0)
df.loc[df['Herbicide spraying'] != 'We perform',
       'Herbicide spraying'] = 0
df.loc[df['Herbicide spraying'] == 'We perform',
       'Herbicide spraying'] = 1

col1 = df['Mechanical harvesting'] + \
       df['Mechanical pruning'] + df['Slashing'] + \
       df['Fungicide spraying'] + df['Insecticide spraying'] + \
       df['Herbicide spraying']

col1 = col1.astype(float).replace({0: np.nan})

col2 = df['total fuel'].replace({0: np.nan})
problems['No fuel and No contractors'] = cond_problem(col1, col2)

col2 = df['Diesel (L)'].replace({0: np.nan})
problems['No Diesel and No contractors'] = cond_problem(col1, col2)

problems['No irrigation'] = df[df['total irrigation'].isnull()][
    'total irrigation'].replace({np.nan: 'Yes'})

# TODO
# If some was not harvested then how much was not harvested
problems['Labelled harvested without yield'] = cond_problem(
    df[df['Was any of your vineyard NOT harvested last season?']
       == 'No'][
        'Was any of your vineyard NOT harvested last season?'],
    df['Grapes harvested']
)

col1 = df[df['Electricity from the grid'].isnull()][
    'Electricity from the grid']
col1 = col1.replace({np.nan: 0})

problems['No electricity from the grid and no Solar'] = cond_problem(
    col1,
    df['Solar.1'])

problems['Diesel irrigation and no diesel use'] = cond_problem(
    df['Diesel'], df['Diesel (L)'])

problems['Electric irrigation and no elctricity from grid used'] = \
    cond_problem(df['Electricity'], df['Electricity from the grid'])

problems['Solar irrigation and no solar electricity used'] = \
    cond_problem(df['Solar'], df['Solar.1'])

#TODO
# - If there is no electricity from the grid they have to use solar
# I am not sure if the above is done correctly.

###############################
# Create the output Excel sheet
problems = problems.dropna(axis=0, how='all')
problems.index = problems.index.astype(str).str.zfill(5)
problems.to_excel('problems_vineyard.xlsx')

######################################################################
#                                                                   #
######################################################################

##################
# Winery issues

df = pd.read_excel(
    'data.xlsx', sheet_name='Winery', index_col='Membership Number')

###################
# Data transformations
#df = df[~df['Paid At'].isnull()]
df = df.fillna(0)

df['% Extraction'] = df['Full winemaking'] / df['Tonnes crushed']

df['water / crushed'] = df['Water used'] / df['Tonnes crushed']

df['litre of wine'] = df['Full winemaking'] + \
    df['First stage winemaking'] + df['Final stage winemaking']
df['water / litre of wine'] = df['Water used'] / \
    df['litre of wine']

df['electricity'] = df['Other'] + df['Wind'] + df['Solar'] + \
    df['Renewable energy from the grid'] + \
    df['Electricity from the grid']
df['electricity / tonne'] = df['electricity'] / df['Tonnes crushed']

df['electicity / litre of wine'] = df['electricity'] / \
    df['litre of wine']

df['fuel / co2'] = (df['Petrol (L)'] * 2.289) + \
                   (df['Diesel (L)'] * 2.694) + \
                   (df['Natural gas'] * 51.348) + \
                   (df['LPG'] * 1.578)
df['total fuel / CO2 / Tonne crush'] = df['fuel / co2'] / \
    df['Tonnes crushed']

df['used / waste'] = df['Wastewater generated'] / df['Water used']

df['Size'] = df['Tonnes crushed'].apply(size)

df = df.replace({0: np.nan})
problems = pd.DataFrame(index=df.index)

########################
# Finding errors using radicals
for col in [
    '% Extraction',
    'water / crushed',
    'water / litre of wine',
    'electricity / tonne',
    'electicity / litre of wine',
    'total fuel / CO2 / Tonne crush',
    'used / waste']:
    gp = df.groupby('Size')
    df_temp = gp[col].transform(zscore)
    df_temp = pd.concat(
        (df_temp[df_temp > threshold], df_temp[df_temp < -threshold]),
        axis=0)

    sz_temp = df[col].transform(zscore)
    sz_temp = pd.concat(
        (sz_temp[sz_temp > threshold], sz_temp[sz_temp < -threshold]),
        axis=0)

    problems['Unusual ' + col + ' (both)'] = np.nan
    problems['Unusual ' + col + ' (both)'].fillna(sz_temp, inplace=True)
    problems['Unusual ' + col + ' (both)'].fillna(df_temp, inplace=True)

    df_temp = None
    sz_temp = None

#################################
# Finding problems conditionally

col1 = df[df['Electricity from the grid'].isnull()][
    'Electricity from the grid']
col1 = col1.replace({np.nan: 0})

problems['No electricity from the grid and no Solar'] = cond_problem(
    col1,
    df['Solar'])

col = df.loc[df['Size'] != 'Small', 'Refrigerant'].copy()
col = col.fillna(0)
for i in range(1, 5):
    col += df['Refrigerant.{}'.format(i)].fillna(0)
problems['No Refridgerants (Medium+ size)'] = col[col == 0]
problems['No Refridgerants (Medium+ size)'] = \
    problems['No Refridgerants (Medium+ size)'].replace(
    {0: 'Yes'}
)

problems['No fuel'] = df[df['fuel / co2'].isnull()][
    'fuel / co2'].replace({np.nan: 'Yes'})

###############################
# Create the output Excel sheet
problems = problems.dropna(axis=0, how='all')
problems.index = problems.index.astype(str).str.zfill(5)
problems.to_excel('problems_winery.xlsx')
