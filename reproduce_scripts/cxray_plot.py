import os
import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def get_base_dir(test_domain, dataset, metric):
    
    if metric == 'mia':
        res_dir= 'results/'+str(dataset)+'/privacy/' + str(test_domain) + '/'

    elif metric == 'privacy_entropy':
        res_dir= 'results/'+str(dataset)+'/privacy_entropy/' + str(test_domain) + '/'

    elif metric == 'privacy_loss_attack':
        res_dir= 'results/'+str(dataset)+'/privacy_loss/' + str(test_domain) + '/' 

    elif metric == 'attribute_attack':
        res_dir= 'results/'+str(dataset)+'/attribute_attack_' + data_case + '/'  + str(test_domain) + '/'  

    elif metric  == 'acc:train':
        res_dir= 'results/' + str(dataset) + '/acc_' + 'train' + '/' + str(test_domain) + '/'

    elif metric  == 'acc:test':
        res_dir= 'results/' + str(dataset) + '/acc_' + 'test' + '/' + str(test_domain) + '/'
        
    elif metric  == 'match_score:train':
        res_dir= 'results/' + str(dataset) + '/match_score_' + 'train' + '/' + str(test_domain) + '/'    

    elif metric  == 'match_score:test':
        res_dir= 'results/' + str(dataset) + '/match_score_' + 'test' + '/' + str(test_domain) + '/'    
        
    return res_dir

# kaggle, nih, chex
test_domain= sys.argv[1]

x=['ERM', 'Rand', 'MatchDG', 'CSD', 'IRM', 'Hybrid']
methods=['erm', 'rand', 'matchdg_erm', 'csd', 'irm', 'hybrid']
dataset= 'chestxray'

# metrics= ['acc:train', 'acc:test', 'mia', 'privacy_entropy', 'privacy_loss_attack', 'match_score:train', 'match_score:test']

metrics= ['acc:train', 'acc:test', 'privacy_loss_attack', 'match_score:test']

acc_train=[]
acc_train_err=[]

acc_test=[]
acc_test_err=[]

mia=[]
mia_err=[]

entropy=[]
entropy_err=[]

loss=[]
loss_err=[]

rank_train=[]
rank_train_err=[]

rank_test=[]
rank_test_err=[]

for metric in metrics:
    for method in methods:
        
        res_dir= get_base_dir(test_domain, dataset, metric)
        
        f= open(res_dir+method+'.txt')
        data= f.readlines()
#         print(data[-3].replace('\n', '').split(':')[-1].split(' '))
        mean= float(data[-3].replace('\n', '').split(':')[-1].split(' ')[-2])
        sd= float(data[-3].replace('\n', '').split(':')[-1].split(' ')[-1])
        
        if metric == 'acc:train':
            acc_train.append(mean)
            acc_train_err.append(sd)
        elif metric == 'acc:test':
            acc_test.append(mean)
            acc_test_err.append(sd)
        elif metric == 'mia':
            mia.append(mean)
            mia_err.append(sd)
        elif metric == 'privacy_entropy':
            entropy.append(mean)
            entropy_err.append(sd)
        elif metric == 'privacy_loss_attack':
            loss.append(mean)
            loss_err.append(sd)
        elif metric == 'match_score:train':
            rank_train.append(mean)
            rank_train_err.append(sd)
        elif metric == 'match_score:test':
            rank_test.append(mean)
            rank_test_err.append(sd)

for idx in range(4):
    
    matplotlib.rcParams.update({'errorbar.capsize': 2})
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    fontsize=30
    fontsize_lgd= fontsize/1.2
    ax.tick_params(labelsize=fontsize)
    ax.set_xticklabels(x, rotation=25)
    
    if idx == 0:
        ax.errorbar(x, acc_train, yerr=acc_train_err, label='Train Accuracy', fmt='o--')
        ax.errorbar(x, acc_test, yerr=acc_test_err, label='Test Accuracy', fmt='o--')
#         ax.set_xlabel('Models', fontsize=fontsize)
        ax.set_ylabel('OOD Accuracy of ML Model', fontsize=fontsize)
        ax.legend(fontsize=fontsize_lgd)
    
    if idx == 1:
#         ax.errorbar(x, mia, yerr=mia_err, label='Classifier Attack', color='blue', fmt='o--')        
#         ax.errorbar(x, entropy, yerr=entropy_err, label='Entropy Attack', color='red', fmt='o--')
        ax.errorbar(x, loss, yerr=loss_err, label='Loss Attack', color='orange', fmt='o--')
        ax.set_ylabel('MI Attack Accuracy', fontsize=fontsize)
        ax.legend(fontsize=fontsize_lgd)

    if idx == 2:
#         ax.errorbar(x, rank_train, yerr=rank_train_err, label='Train', fmt='o--', color='brown')
        ax.errorbar(x, rank_test, yerr=rank_test_err, label='Test', fmt='o--', color='green')
#         ax.set_xlabel('Models', fontsize=fontsize)
        ax.set_ylabel('Mean Rank of Perfect Match', fontsize=fontsize)
        ax.legend(fontsize=fontsize_lgd)
    
    if idx == 3:
        ax.errorbar(x, np.array(acc_train) - np.array(acc_test), yerr=acc_train_err, label='Train Accuracy', fmt='o--')
#         ax.set_xlabel('Models', fontsize=fontsize)
        ax.set_ylabel('Train-Test Accuracy Gap of ML Model', fontsize=fontsize)
        ax.legend(fontsize=fontsize_lgd)
            
    
    save_dir= 'results/' + dataset+ '/plots/'+ test_domain +'/'    
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)        
    
    plt.tight_layout()
    plt.savefig(save_dir + 'privacy_' + str(dataset)+'_' + str(idx) + '.pdf', dpi=600)