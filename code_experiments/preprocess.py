from pathlib import Path
import sys
import pandas as pd

from bcause.util.datautils import filter_data


# Specify the root path of this project if needed
prjpath = Path(".")
sys.path.append(str(prjpath.resolve()))


# Load the utilities
from code_experiments.util import build_model


import logging
logging.getLogger("bcause").setLevel(logging.CRITICAL)


# Needed folders relative to the project path
modelsfolder = Path(prjpath, "models")
datafolder = Path(prjpath, "data")
resfolder = Path(prjpath, "results")


# The domain of the variables are defined as a dictionary where the keys are the variable names and the values are the posible states.
domains = dict(
    age35=["no", "yes"],
    cardiotoxicity=["no", "yes"],
    chemo_adiu=["no", "yes"],
    chemo_neo=["no", "yes"],
    cohort=["h", "pb"],
    cvds=["no", "yes"],
    death_in_5y=["no", "yes"],
    dyslipidemia=["no", "post", "pre"],
    grade=["i", "ii", "iii"],
    histology=[
        "adenomas_and_adenocarcinomas",
        "complex_epithelial_neoplasms",
        "ductal_and_lobular_neoplasms",
        "epithelial_neoplasms_nos",
        "mucinous_adenocarcinoma",
        "neoplasms_nos",
        "papillary_cystadenocarcinoma",
        "squamous_cell_neoplasms"
    ],
    hormons_adiu=["no", "yes"],
    hormons_neo=["no", "yes"],
    hypertension=["no", "post", "pre"],
    ischemic_heart_disease=["no", "yes"],
    ki67=["no", "yes"],
    pn=["pn+", "pn0"],
    pt=["pt1", "pt2", "pt3", "pt4"],
    radio_adiu=["no", "yes"],
    radio_neo=["no", "yes"],
    receptors=[
        "her_2_arricchiti",
        "luminal",
        "luminal_a",
        "luminal_b",
        "luminal_her2",
        "triple_negative"
    ],
    surgery=["conservative", "radical"],
    t2db=["no", "post", "pre"],
    target_adiu=["no", "yes"],
    target_neo=["no", "yes"],
    vascular=["no", "yes"]
)


# Set the relevant nodes
relevant = [
    "hormons_neo",
    "ischemic_heart_disease", "hypertension", "dyslipidemia",
    "t2db"]

# Set the nodes that are fixed
fixed = {"cohort": "pb", "receptors": "yes", "hormons_adiu": "yes"}

# Irrelevant nodes
irrelevant = ["cardiotoxicity", "cvds"]


# Function that modifies the domain of some variables
def process_data(datafile):

    logging.info(f"Reading data from {datafile}")
    data = pd.read_csv(datafile)

    data["receptors"] =data["receptors"].apply(lambda  x : "yes" if x in ["luminal_a","luminal_b","luminal"] else "no")
    domains["receptors"] = ["no", "yes"]

    new_data = filter_data(data, fixed).reset_index(drop=True)
    new_data = new_data[relevant]

    # binarize domains

    to_bin = ['hypertension', 'dyslipidemia', 't2db']
    for v in to_bin:
        domains[v] = ["no","yes"]
        new_data[v] = new_data[v].apply(lambda x: 'yes' if x != 'no' else 'no')

    logging.info(f"Variables in preprocessed data: {list(data.columns)}")

    new_path = str(datafile).replace("_data.csv","_procdata.csv")
    new_data.to_csv(new_path)
    logging.info(f"Preprocessed data saved at: {new_path}")


if __name__ == "__main__":

    # Fake data that can be shared
    datafile = Path(datafolder, "fake_cancer_data.csv")

    # Real data
    #datafile = Path(datafolder, "cancer_data.csv")

    
    # File with
    edgesfile = Path(modelsfolder, "cancer_edges.csv")

    # Run the preprocessing
    process_data(datafile)
    build_model(edgesfile, domains, relevant, irrelevant, fixed)





