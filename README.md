# On Counterfactual Explainations of Cardiovascular Risk in Adolescents and Young Adults Breast Cancer Survivors

This bundle contains the code for reproducing the experiments of the manuscript accepted to  _HC@AIxIA 2024 (3rd AIxIA Workshop on Artificial Intelligence For Healthcare)_ and entitled
"On Counterfactual Explainations of Cardiovascular Risk in Adolescents and Young Adults Breast Cancer Survivors".
The organisation  is the following:

- _code_experiments_: code for replicating the examples in the paper.

- _data_: dataset with the format required in the script.
- _figures_: paper figures and code for its generation.
- _models_: structural causal model in bif format of the study case.
- _results_: real results of teh experimentation.





## Setup

Running the code requires Python 9 or higher. All the counterfactual reasoning is done with bcause package, instalable with 
the following terminal command.

```console
pip install git+https://github.com/PGM-Lab/bcause.git@55d1aa6af54029ee40268196f0df5411cd9b022e
```

If needed, at scripts ``preprocess.py``, ``run.py`` and ``util.py`` set the path to the root of this project by modifying the line:

```python
# Specify the root path of this project if needed
prjpath = Path(".")
```

## Data and model

The data preprocessing and model construction for the study case is done with the script `preprocess.py`:

```console
python3 ./code_experiments/preprocess.py
```

```
INFO:root:Reading data from data/fake_cancer_data.csv
INFO:root:Variables in preprocessed data: ['cohort', 'chemo_neo', 'radio_neo', 'hormons_neo', 'target_neo', 'age35', 'histology', 'chemo_adiu', 'radio_adiu', 'hormons_adiu', 'target_adiu', 'surgery', 'cvds', 'ischemic_heart_disease', 'cardiotoxicity', 'dyslipidemia', 'hypertension', 't2db', 'grade', 'vascular', 'ki67', 'receptors', 'pt', 'pn', 'death_in_5y']
INFO:root:Preprocessed data saved at: data/fake_cancer_procdata.csv
INFO:root:Building SCM with edges from: models/cancer_edges.csv
INFO:root:SCM built with nodes: ['ischemic_heart_disease', 'dyslipidemia', 'hormons_neo', 't2db', 'hypertension', 'U_ischemic_heart_disease', 'U_dyslipidemia', 'U_hormons_neo', 'U_t2db', 'U_hypertension']
INFO:root:Saving SCM to models/cancer.bif
```
This script saves the SCM in bif format at `models/cancer.bif` and the preprocessed data is stored at `data/fake_cancer_procdata.csv`.

By default, the previous script does not load the real data which cannot be shared. Instead, a fake dataset defined over the same variables is considered.
If the true data is available, just replace the path in variable `datafile`.


## Counterfactual inference

The counterfactual queries can be run with the following script (by default, the fake data is used).

```
python3 ./code_experiments/run.py       
```

```
INFO:root:Reading data from data/fake_cancer_procdata.csv
INFO:root:Reading model from models/cancer.bif
INFO:root:Results will be stored at: results/fake_cancer_procdata_results20241031-151016.csv
INFO:root:Starting causal learning loop
INFO:root:pn = [0.9210288989327757, 0.9210288989327757] ps = [0.48368304133347045, 0.48368304133347045] pns = [0.4403394047601672, 0.4403394047601672]   1 iter. 3110.6770038604736 ms.
INFO:root:pn = [0.9245667454674343, 0.9245667454674343] ps = [0.4286064404537217, 0.4286064404537217] pns = [0.3951970801233141, 0.3951970801233141]     2 iter. 3199.7361183166504 ms.
INFO:root:pn = [0.9199961311182153, 0.9199961311182153] ps = [0.44680466209016273, 0.44680466209016273] pns = [0.4090857220414997, 0.4090857220414997]   3 iter. 3215.2180671691895 ms.
INFO:root:pn = [0.9227345296437447, 0.9227345296437447] ps = [0.44206278678577, 0.44206278678577] pns = [0.40634893590143306, 0.40634893590143306]       4 iter. 3276.728868484497 ms.
INFO:root:pn = [0.9181009559880492, 0.9181009559880492] ps = [0.4186055289919908, 0.4186055289919908] pns = [0.38565138581207153, 0.38565138581207153]   5 iter. 3156.8870544433594 ms.
INFO:root:pn = [0.9159930382028231, 0.9159930382028231] ps = [0.4569930038378868, 0.4569930038378868] pns = [0.41808841089581583, 0.41808841089581583]   6 iter. 3195.2340602874756 ms.
INFO:root:pn = [0.925544338913141, 0.925544338913141] ps = [0.44564242957189215, 0.44564242957189215] pns = [0.4109177837051773, 0.4109177837051773]     7 iter. 3113.3711338043213 ms.
INFO:root:pn = [0.9249310545549561, 0.9249310545549561] ps = [0.4297721998816296, 0.4297721998816296] pns = [0.3966860371159237, 0.3966860371159237]     8 iter. 3103.7051677703857 ms.
INFO:root:pn = [0.9181976204249158, 0.9181976204249158] ps = [0.42978941396169057, 0.42978941396169057] pns = [0.39443605719500663, 0.39443605719500663]         9 iter. 3117.5618171691895 ms.
INFO:root:pn = [0.9225451703674273, 0.9225451703674273] ps = [0.4331779379743284, 0.4331779379743284] pns = [0.39977105080608366, 0.39977105080608366]   10 iter. 3115.2758598327637 ms.

```