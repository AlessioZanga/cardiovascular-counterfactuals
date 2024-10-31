library(bnlearn)
library(Rgraphviz)
#library(gRain)
#library(splitTools)
#library(caret)
library(grDevices)


#install.packages("yarrr")
library(yarrr)
transp = yarrr::transparent("blue", trans.val = 1)

if (grepl('AIxAI24/figures$', getwd())==FALSE)
  setwd("./dev_ig/AIxAI24/figures")

model <- read.bif("./extended_model.bif")

#DAG After fixing the variables - cohort, receptors, hormons_adiu

g = graphviz.plot(model, render = FALSE, shape = "rectangle", highlight = list(arcs = rbind(outgoing.arcs(model, "cohort"), outgoing.arcs(model, "receptors"), outgoing.arcs(model, "hormons_adiu")), col = transp))
#gr = renderGraph(g, format="png", filename = "dag1")
#dev.off()

pdf("dag-selection.pdf")
#plot(g)
g = graphviz.plot(model, render = TRUE, shape = "rectangle", fontsize=14,
                  highlight = list(arcs = rbind(outgoing.arcs(model, "cohort"),
                                                outgoing.arcs(model, "receptors"), outgoing.arcs(model, "hormons_adiu")),
                                   col = transp))

dev.off()


#DAG After removing all the nodes not ancestors of ischemic_heart_disease

ancestor_nodes <- c("age35", "grade", "histology", "vascular", "pn", "hormons_neo", "t2db", "hypertension", "dyslipidemia", "ischemic_heart_disease")

all_nodes <- nodes(model)

non_ancestor_nodes <- setdiff(all_nodes, ancestor_nodes)

arcs_set = matrix(nrow = 80, ncol = 2)

for (node in non_ancestor_nodes) {
  arcs_set <- rbind(arcs_set, outgoing.arcs(model, node))
  arcs_set <- rbind(arcs_set, incoming.arcs(model, node))
}
arcs_set <- na.omit(arcs_set)



pdf("dag-barren.pdf")
#plot(g)
graphviz.plot(model, fontsize = 14, shape = "rectangle",
              highlight = list(arcs = arcs_set, nodes = non_ancestor_nodes,
                               col = transp, fill = transp, textCol = transp))


dev.off()



#DAG After removing all the nodes D-separated from ischemic_heart_disease
nodes_removed <- rbind(non_ancestor_nodes, c("vascular", "age35", "grade", "histology", "pn"))

for (node in nodes_removed) {
  arcs_set <- rbind(arcs_set, outgoing.arcs(model, node))
  arcs_set <- rbind(arcs_set, incoming.arcs(model, node))
}
arcs_set <- na.omit(arcs_set)



#### Abbreviate names #####
names_map = list(hormonsneo="HN", ischemicheartdisease="D", hypertension="HT", t2db="DB", dyslipidemia="DP")
new_names = c()

for(v in nodes(model)){
  k = gsub('_', '', v)
  if(k %in% names(names_map)){
    new_names = c(new_names, names_map[[k]])
  }else{
    new_names = c(new_names, v)
  }

}
for (i in seq(dim(arcs_set)[1])){
  k = gsub('_', '', arcs_set[i,"from"])
  if(k %in% names(names_map)) arcs_set[i,"from"] = names_map[[k]]

  k = gsub('_', '', arcs_set[i,"to"])
  if(k %in% names(names_map)) arcs_set[i,"to"] = names_map[[k]]
}




model = rename.nodes(model, new_names)
pdf("dag-dsep.pdf")
#plot(g)


#graphviz.plot(model, fontsize=14, shape = "rectangle", highlight = list(arcs = arcs_set, nodes = nodes_removed, col = "white", fill = "white", textCol = "white"))
graphviz.plot(model, fontsize=14, shape = "rectangle",
              highlight = list(arcs = arcs_set,
                               nodes = nodes_removed,
                               col = transp,
                               fill = transp,
                               textCol = transp))

dev.off()


nodes(model)




