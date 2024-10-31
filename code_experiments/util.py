from pathlib import Path

import networkx as nx
import pandas as pd
from bcause.factors.mulitnomial import canonical_for_model, uniform_multinomial
from bcause.models.cmodel import StructuralCausalModel
import logging

logging.getLogger("bcause").setLevel(logging.CRITICAL)

def add_exogenous_variables(dag: nx.DiGraph):
    # Copy the original DAG
    updated_dag = dag.copy()

    for node in dag.nodes():
        # Create a new exogenous variable name, e.g., "U_node"
        exogenous_var = f"U_{node}"

        # Add the exogenous variable as a new node in the DAG
        updated_dag.add_node(exogenous_var)

        # Add an edge from the exogenous variable to the original node
        updated_dag.add_edge(exogenous_var, node)

    return updated_dag


def create_SCM(dag: nx.DiGraph, dom):
    # Step 1: Add exogenous variables
    # The function `add_exogenous_variables(dag)` adds an exogenous variable for each endogenous variable
    # in the DAG. The updated DAG will have additional nodes representing these exogenous variables.
    updated_dag = add_exogenous_variables(dag)

    # Step 2: Create an empty Structural Causal Model (SCM)
    # A new SCM is initialized with the updated DAG (containing both endogenous and exogenous variables).
    model = StructuralCausalModel(updated_dag)

    # Step 3: Initialize an empty dictionary to store structural equations
    eqs = dict()

    # Step 4: Iterate over each node in the original DAG (endogenous variables)
    # For each node (endogenous variable), a canonical equation is created using the `canonical_for_model` function.
    # This function defines the structural equation for the node based on its endogenous and exogenous parents.
    for node in dag.nodes():

        eqs = {node: canonical_for_model(model, dom, node)}

        # Step 5: Set the structural equation (factor) for the node in the SCM
        # The `set_factor` method of the SCM is used to associate the structural equation with the node.
        model.set_factor(node, eqs[node])

    for u in model.exogenous:
        domu = {u:model.factors[model.get_edogenous_children(u)[0]].domain[u]}
        pu = uniform_multinomial(domu)
        model.set_factor(u, pu)



    # Step 6: Return the updated DAG and the SCM
    # The function returns the the fully defined SCM.
    return model


def build_model(edgesfile, domains, relevant, irrelevant, fixed):
    # First I need a DAG
    # Read edges
    edges_df = pd.read_csv(edgesfile)
    edges = list(zip(edges_df['from'], edges_df['to']))
    logging.info(f"Building SCM with edges from: {edgesfile}")


    # Create a first DAG
    dag_endo = nx.DiGraph(edges)

    to_remove = irrelevant + list(fixed.keys())

    for v in to_remove:
        if v in dag_endo.nodes: dag_endo.remove_node(v)

    for v in list(dag_endo.nodes):
        if v not in relevant: dag_endo.remove_node(v)

    modelpath = Path(str(edgesfile).replace("_edges.csv", ".bif"))

    new_model = create_SCM(dag_endo, {v: domains[v] for v in relevant})
    logging.info(f"SCM built with nodes: {new_model.variables}")

    logging.info(f"Saving SCM to {modelpath}")
    new_model.save(modelpath)


