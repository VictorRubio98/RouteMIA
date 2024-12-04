import os
import argparse

import numpy as np
import pandas as pd

def parse_csv(df: pd.DataFrame, gps: pd.DataFrame) -> pd.DataFrame:
    grouped = df.groupby('tid')[['lat', 'lon']]

    parsed = pd.DataFrame()
    for tid, group in grouped:
        index_traj = []
        for row in group.values:
            mask = gps.eq(row).lat * gps.eq(row).lon
            index_traj.append(gps.index[mask].values[0])

        parsed=pd.concat([parsed,pd.DataFrame([index_traj])], ignore_index=True)
    return parsed


parser = argparse.ArgumentParser()

parser.add_argument('-f', '--file', type=str, help='Path of the file from the generated data from the model LSTM-TrajGAN.')
parser.add_argument('-e', '--epsilon', type=str, default='baseline')
parser.add_argument('-d', '--dataset', default='geolife', type=str, choices=['geolife', 'porto'])

opt = parser.parse_args()

df = pd.read_csv(opt.file)

df['lat'] = df['lat'].round(3)
df['lon'] = df['lon'].round(3)
        
model_path = f'data/{opt.dataset}/trajgan/'
elements = os.listdir(model_path)

if 'real.data' not in elements or 'test.data' not in elements:
    train_df = pd.read_csv(os.path.join(model_path, 'test_latlon.csv'))
    test_df = pd.read_csv(os.path.join(model_path, 'train_latlon.csv'))
    all_df = pd.concat([train_df, test_df, df], ignore_index=True)
    gps = all_df.drop_duplicates(subset=['lat', 'lon'])[['lat','lon']]
    gps.to_csv(os.path.join(model_path, 'gps'),sep=' ',index=False, header=False)
    real_data = parse_csv(train_df, gps)
    test_data = parse_csv(test_df, gps)
    
    real_data.to_csv(os.path.join(model_path, 'real.data'),sep=' ',index=False, header=False)
    test_data.to_csv(os.path.join(model_path, 'test.data'),sep=' ',index=False, header=False)
    
else:
    gps = pd.read_csv(os.path.join(model_path, 'gps'), sep=' ')
    gps.columns = ['lat', 'lon']
    gps = pd.concat([gps, df[['lat', 'lon']]], axis=0, ignore_index=True)[['lat', 'lon']]
    gps.to_csv(os.path.join(model_path, 'gps'),sep=' ',index=False, header=False)

parsed = parse_csv(df, gps)
parsed.to_csv(os.path.join(model_path, opt.epsilon, 'gene.data'), sep=' ',index=False, header=False)


