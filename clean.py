import numpy as np
import pandas as pd


def int_to_char(index: int):
    letter = ''
    while index > 25:
        letter += chr(65 + int((index)/26) - 1)
        index = index - (int((index)/26))*26
    letter += chr(65 + (int(index)))
    return letter

# Vineyard processing


def vineyard_size(size):
    if size < 10:
        return 1
    elif size < 25:
        return 2
    elif size < 50:
        return 3
    elif size < 100:
        return 4
    else:
        return 5


def proc_vineyard(df):
    df.rename(columns={
        'Red grapes': 'Red grapes (ha)',
        'White grapes': 'White grapes (ha)'
    }, inplace=True)

    df['Total Vineyard Area  (ha)'] = \
        df['Red grapes (ha)'] + \
        df['White grapes (ha)']

    df['Vineyard Size'] = df['Total Vineyard Area  (ha)'].map(
        vineyard_size)

    df['t/ha'] = df['Grapes harvested (t)'] / \
        df['Total Vineyard Area  (ha)']

    df['Total Vineyard not harvested (ha)'] = (
        df['New development / redevelopment (ha)'] +
        df['Frost (ha)'] +
        df['Pest/disease (ha)'] +
        df['Non-sale (ha)'])

    df['t/ha harvested from'] = df['Grapes harvested (t)'] / \
        (df['Total Vineyard Area  (ha)'] -
         df['Total Vineyard not harvested (ha)'])

    df['% not harvested compared to total vineyard area'] = \
        df['Total Vineyard not harvested (ha)'] / \
        df['Total Vineyard Area  (ha)']

    df['Total water used (ML)'] = \
        (df['River water (ML)'] +
         df['Groundwater (ML)'] +
         df['Surface water dam (ML)'] +
         df['Recycled water from winery (ML)'] +
         df['Recycled water from other source (ML)'] +
         df['Mains water (ML)'] +
         df['Other water (ML)'] +
         df['Water applied for frost control (ML)'])

    df['Water Use (ML/ha)'] = df['Total water used (ML)'] / \
        df['Total Vineyard Area  (ha)']

    df['Electricity CO2e'] = df['Electricity from the grid (kWh)'] * \
        0.51
    df['Electricity in tonnes of CO2e'] = df['Electricity CO2e'] / \
        1000
    df['Electricity CO2e/ha'] = df['Electricity CO2e'] / \
        df['Total Vineyard Area  (ha)']
    df['Electricity CO2e/t'] = df['Electricity CO2e'] / \
        df['Grapes harvested (t)']

    df['Renewable energy sourced from the grid (kWh)'] = \
        df['Renewable energy sourced from the grid (kWh)'] + \
        df['Solar (kWh)'] + \
        df['Wind (kWh)'] + \
        df['Renewable electricity generated and ' \
           'exported to the grid (kWh)']

    df['Petrol kg CO2e'] = df['Petrol (L)'] * 2.289
    df['Petrol kg CO2e/ha'] = df['Petrol kg CO2e'] / \
        df['Total Vineyard Area  (ha)']
    df['Petrol kg CO2e/t'] = df['Petrol kg CO2e'] / \
        df['Grapes harvested (t)']

    df['LPG kg CO2e'] = df['LPG (L)'] * 1.578
    df['LPG kg CO2e/ha'] = df['LPG kg CO2e'] / \
        df['Total Vineyard Area  (ha)']
    df['LPG kg CO2e/t'] = df['LPG kg CO2e'] / \
        df['Grapes harvested (t)']

    df['Diesel CO2e'] = df['Diesel (L)'] * 2.694
    df['Diesel CO2e/ha'] = df['Diesel CO2e'] / \
        df['Total Vineyard Area  (ha)']
    df['Diesel CO2e/t'] = df['Diesel CO2e'] / \
        df['Grapes harvested (t)']

    df['Biodiesel CO2e'] = df['Biodiesel (L)'] * 0.123
    df['Biodiesel CO2e/ha'] = df['Biodiesel CO2e'] / \
        df['Total Vineyard Area  (ha)']
    df['Biodiesel CO2e/t'] = df['Biodiesel CO2e'] / \
        df['Grapes harvested (t)']

    df['Total fuel CO2e'] = df['Petrol kg CO2e'] + df['LPG kg CO2e'] \
        + df['Diesel CO2e'] + df['Biodiesel CO2e']

    df['Total fuel CO2e/ha'] = df['Petrol kg CO2e/ha'] + \
        df['LPG kg CO2e/ha'] + df['Diesel CO2e/ha'] + \
        df['Biodiesel CO2e/ha']

    df['Total fuel CO2e/t'] = df['Petrol kg CO2e/t'] + \
        df['LPG kg CO2e/t'] + df['Diesel CO2e/t'] + \
        df['Biodiesel CO2e/t']

    df['Total elect + fuel CO2e / ha'] = df['Total fuel CO2e/ha'] + \
        df['Electricity CO2e/ha']

    df['Total elect + fuel CO2e / t'] = df['Total fuel CO2e/t'] + \
        df['Electricity in tonnes of CO2e']

    df['recycle vs landfill'] = \
        df['How many timber trellis posts have been re-used or '
           'recycled in the past 12 months?'] / \
        df['How many posts have been disposed (e.g. '
           'landfill/combustion) in the past 12 months?']

    df['Total Tractor Passes per season'] = \
        df['Slashing Number of times/passes per year'] + \
        df['Fungicide spraying Number of times/passes per year'] + \
        df['Herbicide spraying Number of times/passes per year'] + \
        df['Herbicide spraying Number of times/passes per year']

    df['Synthetic nitrogen kg CO2'] = df['Synthetic nitrogen'] * 3.98
    df['Synthetic nitrogen kg CO2/ha'] = df['Synthetic nitrogen kg '
                                            'CO2'] / \
        df['Grapes harvested (t)']

    df['Organic nitrogen kg CO2'] = df['Organic nitrogen'] * 3.98
    df['Organic nitrogen kg CO2/ha'] = df['Organic nitrogen kg '
                                          'CO2'] / \
        df['Grapes harvested (t)']

    df['Urea kg CO2'] = df['Urea'] * 0.733

    #TODO
    # Is it intended that total nitrogen per CO2 includes Urea?
    df['Total Nitrogen kg CO2'] = df['Synthetic nitrogen kg CO2'] + \
        df['Organic nitrogen kg CO2'] + df['Urea kg CO2']

    df['Total Nitrogen kg CO2/ha'] = df['Total Nitrogen kg CO2'] / \
        df['Total Vineyard Area  (ha)']

    df['Total Nitrogen kg CO2/t'] = df['Total Nitrogen kg CO2'] / \
        df['Grapes harvested (t)']

    #TODO
    # There was no formula for the below column
    df['Total Nitrogen fertiliser use (kg N applied/ha)'] = np.nan

    df['Total Emissions kg CO2/ha'] = df['Total Nitrogen fertiliser'
                                         ' use (kg N applied/ha)'] \
        + df['Total elect + fuel CO2e / ha']
    #TODO
    # The below field column is listed as t/kg but is actually t/kg/ha
    df['Productivity (t/kg CO2e)'] = df['Total Emissions kg CO2/ha'] \
        / df['Grapes harvested (t)']

    df['Gross margin'] = df['Total vineyard revenue (from grape '
                            'sales)'] - df['Total vineyard operating '
                                           'costs']
    df['Average operating cost per hectare'] = df['Total vineyard '
                                                  'operating costs'] \
        / df['Total Vineyard Area  (ha)']
    df['Average operating cost per tonne'] = df['Total vineyard '
                                                'operating costs'] / \
        df['Grapes harvested (t)']

    df['Other Spray Diary Used total'] = \
        ((df['GrowData'] == np.nan) +
         (df['Accolade'] == np.nan) +
         (df['Yalumba'] == np.nan) +
         (df['SAW'] == np.nan) +
         (df['Other'] == np.nan))*1

    df['Total no. of Spray Diaries used'] = \
        df['Other Spray Diary Used total'] + \
        (((df['GrapeWeb'] == np.nan) +
         (df['GrapeLink'] == np.nan)) * 1)

    df['More than 1 spray diary used'] = \
        (df['Total no. of Spray Diaries used'] > 1) * 1

    """
        df['Nitrogen Factor %'] = "=VLOOKUP(" + \
            int_to_char(df.columns.get_loc('GrapeWeb')) + \
            (df.reset_index().index + 2).astype(str) + \
            ",'file:///sites/Proj/4-" \
            "2-1-sustainability/Shared Documents/" \
            "Database/Carbon calculator/National " \
            "Greenhouse Accounts Factors.xlsx'#$'" \
            "Fertiliser Factors'.$A$1:$D$1048576," \
            "4,FALSE())"
    
        df['Nitrogen kg'] = df['Applied'] * df['Nitrogen Factor %']
    """

    return df


if __name__ == '__main__':
    """
    Start of reading and writing
    """

    path = 'Copy of SWA Data 2021-07-01 - 2022-06-30 raw with extra ' \
           'columns for cleanup start 16 Sep 2022.xlsx'

    sheets = pd.ExcelFile(path).sheet_names

    df = {}

    for sheet in sheets:
        df[sheet] = pd.read_excel(path, sheet_name=sheet)
        df[sheet] = df.get(sheet).loc[
                    :, ~df[sheet].columns.duplicated()].copy()
        if sheet == 'Vineyard':
            df[sheet] = proc_vineyard(df[sheet])
