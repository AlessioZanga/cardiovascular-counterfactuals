from datetime import datetime

import pandas as pd

from bcause.inference.causal.multi import EMCC
from bcause.models.cmodel import StructuralCausalModel
from bcause.util.watch import Watch
from pathlib import Path

import logging
logging.getLogger("bcause").setLevel(logging.CRITICAL)

# Specify the root path of this project if needed
prjpath = Path(".")

# Needed folders relative to the project path
modelsfolder = Path(prjpath, "models")
datafolder = Path(prjpath, "data")
resfolder = Path(prjpath, "results")

# Set the number iterations per EM run and the number of EM runs
max_iter = 500
num_runs = 100



# Real preprocessed data
#datapath = Path(datafolder, "cancer_procdata.csv")

# Fake preprocessed data
datapath = Path(datafolder, "fake_cancer_procdata.csv")

modelpath = Path(modelsfolder, "cancer.bif")

logging.info(f"Reading data from {datapath}")
logging.info(f"Reading model from {modelpath}")


data = pd.read_csv(datapath, index_col=0)
model = StructuralCausalModel.read(modelpath)



# Set the results
resfilepath = Path(resfolder,datapath.name.replace(".csv",f"_results{datetime.now().strftime('%Y%m%d-%H%M%S')}.csv"))
logging.info(f"Results will be stored at: {resfilepath}")

results = pd.DataFrame()

# Start the loop of the experimentation. Each iteration of the loop generates a single point estimate of the queries
logging.info("Starting causal learning loop")

t0 = 0
Watch.start()

i = 1
for i in range(num_runs):

    inf = EMCC(model, data, num_runs=1, max_iter=max_iter, min_rating=0.0)

    t0 = Watch.get_time()
    inf.compile()


    pn = inf.prob_necessity("hormons_neo", "ischemic_heart_disease", true_false_cause=["yes", "no"],
                            true_false_effect=["yes", "no"])
    ps = inf.prob_sufficiency("hormons_neo", "ischemic_heart_disease", true_false_cause=["yes", "no"],
                              true_false_effect=["yes", "no"])

    pns = inf.prob_necessity_sufficiency("hormons_neo", "ischemic_heart_disease", true_false_cause=["yes", "no"],
                                         true_false_effect=["yes", "no"])

    t1 = Watch.get_time()



    msg = f"pn = {[min(pn), max(pn)]} ps = {[min(ps), max(ps)]} pns = {[min(pns), max(pns)]}\t {i+1} iter. {t1-t0} ms."
    logging.info(msg)
    llk_ratio = inf.models[-1].rating


    # Save the results
    r = pd.DataFrame(dict(iter=i+1, pn=pn[-1], ps=ps[-1], pns=pns[-1],
                          llk_ratio=llk_ratio, max_iter=max_iter), index=[0])
    results = pd.concat([results, r], ignore_index=True)
    results.to_csv(resfilepath)

