import os
import argparse

import torch


def calculateAdv(dataset:torch.Tensor)->float:
    positive_label = dataset[dataset[:, -1] == 1][:, -2]
    negative_label = dataset[dataset[:, -1] == 0][:, -2]
    prob_TP = (positive_label == 1).float().mean().item()
    prob_FP = (negative_label == 1).float().mean().item()
    # print(f'Probability of False Positives: {prob_FP}')
    # print(f'Probability of True Positives: {prob_TP}')
    return (prob_TP - prob_FP)
    
if __name__ =='__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', default='geolife', choices=['geolife', 'porto'], help='Name of the tataset to be used in the attack.')
    parser.add_argument('-m', '--model', default='movesim', type=str, choices=['movesim', 'trajgan'])

    opt = parser.parse_args()

    epsilons = ['baseline', 'epsilon2', 'epsilon3', 'epsilon5', 'epsilon10', 'epsilon20', 'epsilon30', 'epsilon40', 'epsilon50', 'infinite']
    privacy_gain = []
    max_adv = 0
    max_baseline = 'Empty'

    for e in epsilons:
        hist_pg = []
        print(f'Iterating for {e}...')
        data_path = f'data/{opt.dataset}'
        predictions_path = f'{data_path}/{opt.model}/{e}/predictions'
        for file in os.listdir(path=predictions_path):            
            results = torch.load(os.path.join(predictions_path, file))
            if e == 'baseline':
                base_adv = calculateAdv(results)
                if max_adv < base_adv:
                    max_adv = base_adv
                    max_baseline = file
                    print(f'Found a better baseline result with advantadge {max_adv:.2f} and name {max_baseline}')
            else:
                e_adv = calculateAdv(results)
                PG = max_adv - e_adv
                hist_pg.append(PG)
                print(f'Found privacy gain {PG:.2f} for attacker {file}')
        if e != 'baseline':
            max_pg = max(hist_pg)
            min_pg = min(hist_pg)
            mean_pg = sum(hist_pg)/len(hist_pg)
            print(f'Mean privacy gain: {mean_pg}, maximum: {max_pg}, minimum: {min_pg}')