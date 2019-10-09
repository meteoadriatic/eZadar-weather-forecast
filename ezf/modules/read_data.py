def read_csv(csvfile):
    import pandas as pd

    df = pd.read_csv(csvfile)
    # df = pd.read_csv(os.path.join(root, 'data/Grossglockner.csv'))

    df.drop(columns=['wind', 'wdir', 'h0', 'tstorm', 'fog', 'weather',
                     'mlcape', 'd2m', 't850', 'vt'], inplace=True)
    df.rename(columns={'altt2m': 't2m', 'precpctdisp': 'ppr', 'precave': 'prec', 'h2mdisp': 'h2m',
                       'snowpctdisp': 'spr', 'cldave': 'cld', 'tstormpctdisp': 'tpr'}, inplace=True)

    df['ppr'] = df['ppr'].str.replace('<1%', '0')
    df['ppr'] = df['ppr'].str.replace('>90%', '100')
    df['ppr'] = df['ppr'].map(lambda x: x.rstrip('%'))
    df['spr'] = df['spr'].str.replace('<1%', '0')
    df['spr'] = df['spr'].str.replace('>90%', '100')
    df['spr'] = df['spr'].map(lambda x: x.rstrip('%'))
    df['tpr'] = df['tpr'].str.replace('<1%', '0')
    df['tpr'] = df['tpr'].str.replace('>90%', '100')
    df['tpr'] = df['tpr'].map(lambda x: x.rstrip('%'))

    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df.set_index(pd.DatetimeIndex(df['datetime']))
    df.drop(columns=['datetime'], inplace=True)

    return df