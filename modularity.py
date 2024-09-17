"""Functions and stuff for computing modularity"""
# import numpy as np
# import pandas as pd
from pandas import DataFrame

def Q_g(nodes: DataFrame, edges: DataFrame, col, chi=0.0, weight_col="total_weight",
        u_col="node1", v_col="node2",
        suffixes=["_1","_2"]):
    """Compute the generalized modularity score of a partition.
    
    Parameters:
        nodes: a DataFrame whose index is node IDs, and `nodes[partition_col]` contains the cluster IDs
        edges: a DataFrame where `edges[u_col]`, `edges[v_col]`, `edges[weight_col]` specifies a weighted, undirected edge
        
        suffixes: If `None`, merge `nodes` into `edges` twice so each edge has its endpoint clusters identified.
                  Otherwise, the cluster identities are in `edges[partition_col+suffixes[0]]` and
                  `edges[partition_col + suffixes[1]]`"""
    
    if suffixes is None:
        # need to merge in node data first
        suffixes = ["_u", "_v"]
        edges = edges.merge(nodes[col], left_on=u_col, right_index=True)
        edges = edges.merge(nodes[col], left_on=v_col, right_index=True, suffixes=suffixes)
    
    m = edges[weight_col].sum()

    # tmp = edges[edges[col + suffixes[0]] == edges[col + suffixes[1]]].groupby([col+suffixes[0], col+suffixes[1]]).agg({weight_col: "sum"}).rename(columns={weight_col: "mC"})
    # tmp.index = tmp.index.get_level_values(0)
    # tmp["nC"] = nodes.value_counts(col)
    # tmp["KC"] = edges.groupby(col+suffixes[0]).agg({weight_col: "sum"}) + edges.groupby(col+suffixes[1]).agg({weight_col: "sum"})
    # tmp["q"] = (2 * tmp["mC"] - (tmp["KC"] ** 2) / (2 * m)) / (2 * m)
    # tmp["rho"] = tmp["nC"].where(tmp["nC"] == 0, 2 * tmp["mC"] / (tmp["nC"] * (tmp["nC"] - 1)))
    # tmp["rhochi"] = tmp["rho"].where(tmp["rho"] == 0, tmp["rho"] ** chi)
    tmp = Q_table(nodes, edges, col, chi, weight_col=weight_col, suffixes=suffixes)
    return (tmp["q"] * tmp["rhochi"]).sum()


def DeltaQ_g(nodes: DataFrame, edges: DataFrame, col, chi,
             v, D,
             weight_col="total_weight", u_col="node1", v_col="node2", suffixes=["_1","_2"],
             Q_tbl=None, m_tbl=None, K_tbl=None):
    """Compute the change in Q_g when the label of vertex `v` is changed to `D`
    
    This computation can be sped up by passing in precomputed tables for the Q_g terms (`Q_tbl`),
    the node-cluster degrees (`m_tbl`), and the node degrees (`K_tbl`)."""
    if Q_tbl is None:
        Q_tbl = Q_table(nodes, edges, col, chi, weight_col=weight_col, suffixes=suffixes)
    if m_tbl is None:
        m_tbl = m_table(edges, col, u_col=u_col, v_col=v_col, weight_col=weight_col, suffixes=suffixes)
    if K_tbl is None:
        K_tbl = K_table(edges, u_col=u_col, v_col=v_col, weight_col=weight_col)

    m = edges[weight_col].sum()
    C = nodes.loc[v, col]

    mC = Q_tbl.loc[C, "mC"]
    mCprime = mC - m_tbl.loc[C, v]
    mD = Q_tbl.loc[D, "mC"]
    mDprime = mD + m_tbl.loc[D, v]

    KC = Q_tbl.loc[C, "KC"]
    KD = Q_tbl.loc[D, "KC"]
    Kv = K_tbl.loc[v, weight_col]
    KCprime = KC - Kv
    KDprime = KD + Kv

    nCprime = Q_tbl.loc[C, "nC"] - 1
    nDprime = Q_tbl.loc[D, "nC"] + 1
    
    qC = Q_tbl.loc[C, "q"]
    qCprime = (mCprime / m) - (KCprime / (2 * m)) ** 2
    qD = Q_tbl.loc[D, "q"]
    qDprime = (mDprime / m) - (KDprime / (2 * m)) ** 2

    rhoCchi = Q_tbl.loc[C, "rhochi"]
    if mCprime > 0 and nCprime > 1:
        rhoCprime = 2 * mCprime / (nCprime * (nCprime - 1))
    else:
        rhoCprime = 0.0
    if rhoCprime > 0:
        rhoCprimechi = rhoCprime ** chi
    else:
        rhoCprimechi = 0.0
    
    rhoDchi = Q_tbl.loc[D, "rhochi"]
    if mDprime > 0 and nDprime > 1:
        rhoDprime = 2 * mDprime / (nDprime * (nDprime - 1))
    else:
        rhoDprime = 0.0
    if rhoDprime > 0:
        rhoDprimechi = rhoDprime ** chi
    else:
        rhoDprimechi = 0.0
    
    return qCprime * rhoCprimechi - qC * rhoCchi + qDprime * rhoDprimechi - qD * rhoDchi



def Q_table(nodes: DataFrame, edges: DataFrame, col, chi,
            weight_col="total_weight", suffixes=["_1","_2"]):
    """Compute all the individual terms in the summation to compute Q_g.
    
    Parameters:
        nodes: The node dataframe. Nodes are stored as the index, and `nodes[col]`
               contains the cluster label
        edges: The edge dataframe, which includes the following columns:
               edges[weight_col]: the weight of the edge
               edges[col+suffixes[0]]: the cluster ID of the first node in the edge
               edges[col+suffixes[1]]: the cluster ID of the second node in the edge
               
    Returns:
        A dataframe `df` with columns 'nC', 'mC', and 'rho' which correspond to the terms in Q_g,
        as well as 'q' and 'rhochi', where `Q_g = sum(df['q'] * df['rhochi'])`"""
    m = edges[weight_col].sum()

    # tmp = edges[edges[col + suffixes[0]] == edges[col + suffixes[1]]].groupby([col+suffixes[0], col+suffixes[1]]).agg({weight_col: "sum"}).rename(columns={weight_col: "mC"})
    # tmp.index = tmp.index.get_level_values(0)
    # tmp["nC"] = nodes.value_counts(col)
    # tmp["KC"] = edges.groupby(col+suffixes[0]).agg({weight_col: "sum"}) + edges.groupby(col+suffixes[1]).agg({weight_col: "sum"})
    # tmp["q"] = (2 * tmp["mC"] - (tmp["KC"] ** 2) / (2 * m)) / (2 * m)
    # tmp["rho"] = tmp["nC"].where(tmp["nC"] == 0, 2 * tmp["mC"] / (tmp["nC"] * (tmp["nC"] - 1)))
    # tmp["rhochi"] = tmp["rho"].where(tmp["rho"] == 0, tmp["rho"] ** chi)
    # return tmp
    Q_t = DataFrame(nodes.value_counts(col)).rename(columns={0: "nC"})
    mC = edges[edges[col + suffixes[0]] == edges[col + suffixes[1]]].groupby([col+suffixes[0], col+suffixes[1]]).agg({weight_col: "sum"}).rename(columns={weight_col: "mC"})
    mC.index = mC.index.get_level_values(0)
    mC.index.name = Q_t.index.name
    Q_t = Q_t.merge(mC, left_index=True, right_index=True, how="outer").fillna(0)
    KC = edges.groupby(col + suffixes[0]).agg({weight_col: sum}).add(edges.groupby(col + suffixes[1]).agg({weight_col: sum}), fill_value=0).rename(columns={weight_col: "KC"})
    Q_t = Q_t.merge(KC, left_index=True, right_index=True)
    Q_t["q"] = (2 * Q_t["mC"] - (Q_t["KC"] ** 2) / (2 * m)) / (2 * m)
    Q_t["rho"] = Q_t["mC"].where(Q_t["nC"] < 2, 2 * Q_t["mC"] / (Q_t["nC"] * (Q_t["nC"] - 1)))
    Q_t["rhochi"] = Q_t["rho"].where(Q_t["rho"] == 0.0, Q_t["rho"] ** chi)
    return Q_t


def m_table(edges: DataFrame, col,
            u_col="node1", v_col="node2",
            weight_col="total_weight", agg="sum",
            suffixes=["_1","_2"]):
    """Compute the sum of weights of edges from nodes to clusters.
    Returns a dataframe `mv` where the clusters are the index, the nodes are the columns.
    
    The value at `mv.loc[c, v]` is the sum of edge weights of all edges connecting node `v`
    to a node in cluster `c` (in either direction).
    
    Using `agg='sum'` will compute the weighted degree sum. Using `agg='count'` will """
    u_table = edges.groupby([u_col, col + suffixes[1]]).agg({weight_col: agg})
    u_table.index.names = ["node", "cluster"]
    v_table = edges.groupby([v_col, col + suffixes[0]]).agg({weight_col: agg})
    v_table.index.names = ["node", "cluster"]
    # mv = u_table.merge(v_table, how="outer", left_index=True, right_index=True, suffixes=suffixes).fillna(0)
    # mv["weight"] = mv[weight_col+suffixes[0]] + mv[weight_col+suffixes[1]]
    # return mv.pivot_table(index="cluster", columns="node", values="weight", fill_value=0)
    mv = u_table.add(v_table, fill_value=0)
    return mv.pivot_table(index="cluster", columns="node", values=weight_col, fill_value=0)


def K_table(edges: DataFrame,
            u_col="node1", v_col="node2",
            weight_col="total_weight"):
    """Compute each node's weight-degree sum, which is its contribution to the K_C term"""
    Ku = edges.groupby(u_col).agg({weight_col: "sum"})
    Kv = edges.groupby(v_col).agg({weight_col: "sum"})
    # Ktable = Ku.merge(Kv, how="outer", left_index=True, right_index=True, suffixes=suffixes).fillna(0)
    # Ktable["Kv"] = Ktable[weight_col+suffixes[0]] + Ktable[weight_col+suffixes[1]]
    return Ku.add(Kv, fill_value=0)


def kappa_table(edges: DataFrame, col,
                u_col="node1", v_col="node2",
                weight_col="total_weight",
                suffixes=["_1","_2"],
                agg="sum", node_name="bodyId"):
    r"""Compute the within-module degree. This is equivalent to a subset of `m_table`
    that has been stacked.
    
    To compute the terms $\bar{kappa}_{s_i}$ and $\sigma_{\kappa_{s_i}}$
    in Guimera & Amaral (2005), https://doi.org/10.1038/nature03288,
    use the following:
    ```
    kappa_tbl = kappa_table(...)
    kappa_tbl.groupby(col).agg({weight_col: ["mean", "std"]})
    ```
    """
    col1 = col + suffixes[0]
    col2 = col + suffixes[1]
    within = edges[edges[col1] == edges[col2]]
    uC_table = within.groupby([u_col, col2]).agg({weight_col: agg})
    uC_table.index.names = [node_name, col]
    vC_table = within.groupby([v_col, col1]).agg({weight_col: agg})
    vC_table.index.names = [node_name, col]
    return uC_table.add(vC_table, fill_value=0)


def participation_score(nodes: DataFrame, edges: DataFrame, col, v,
                        weight_col="total_weight", u_col="node1", v_col="node2", suffixes=["_1","_2"],
                        m_tbl=None, K_tbl=None):
    """Compute the partitcipation score of a node `v` relative to a given partition of a network.
    
    See Guimera & Amaral (2005), https://doi.org/10.1038/nature03288"""
    if m_tbl is None:
        m_tbl = m_table(edges, col, u_col=u_col, v_col=v_col, weight_col=weight_col, suffixes=suffixes)
    if K_tbl is None:
        K_tbl = K_table(edges, u_col=u_col, v_col=v_col, weight_col=weight_col)
    
    return 1 - ((m_tbl[v] / K_tbl.loc[v]) ** 2).sum()


def participation_scores(edges: DataFrame, col,
                         weight_col="total_weight", u_col="node1", v_col="node2", suffixes=["_1","_2"],
                         m_tbl=None, K_tbl=None):
    """Compute participation score for all nodes simulatenously.
    
    See Guimera & Amaral (2005), https://doi.org/10.1038/nature03288"""
    if m_tbl is None:
        m_tbl = m_table(edges, col, u_col=u_col, v_col=v_col, weight_col=weight_col, suffixes=suffixes)
    if K_tbl is None:
        K_tbl = K_table(edges, u_col=u_col, v_col=v_col, weight_col=weight_col)
    
    return 1 - ((m_tbl.T / K_tbl.values) ** 2).sum(axis=1)


def directed_participation_score(edges: DataFrame, col, v,
                                 weight_col="total_weight", u_col="node1", v_col="node2", suffixes=["_1", "_2"],
                                 m_tbl=None, K_tbl=None):
    """Compute the directed participation score of a node `v` relative to a given partition of a network.
    Simple extension of participation score from Guimera & Amaral (2005), https://doi.org/10.1038/nature03288"""
    

def z_score(nodes: DataFrame, edges: DataFrame, col, v,
            weight_col="total_weight", u_col="node1", v_col="node2", suffixes=["_1","_2"],
            agg="sum",
            m_tbl=None, K_tbl=None, kappa_tbl=None):
    """Compute the degree z-score for node `v` relative to a given partition of a network.
    
    See Guimera & Amaral (2005), https://doi.org/10.1038/nature03288"""
    if m_tbl is None:
        m_tbl = m_table(edges, col, u_col=u_col, v_col=v_col, weight_col=weight_col, suffixes=suffixes)
    if K_tbl is None:
        K_tbl = K_table(edges, u_col=u_col, v_col=v_col, weight_col=weight_col)
    if kappa_tbl is None:
        kapp_tbl = kappa_table(edges, col, u_col, v_col, weight_col, suffixes, agg)
    
    C = nodes.loc[v, col]  # get the node's current cluster
    C_nodes = nodes[nodes[col] == C].index
    m_vC = m_tbl.loc[C, v]  # edges from v to other nodes in its cluster
    mbar_vC = m_tbl.loc[C, C_nodes].mean()  # average over nodes in cluster
    sigma_vC = m_tbl.loc[C, C_nodes].std()  # std over nodes in cluster

    return (m_vC - mbar_vC) / sigma_vC


def z_scores(nodes: DataFrame, edges: DataFrame, col,
             weight_col="total_weight", u_col="node1", v_col="node2", suffixes=["_1","_2"],
             agg="sum", node_name="bodyId",
             kappa_tbl=None):
    """Compute the within-module degree z-score for all nodes simultaneously"""
    if kappa_tbl is None:
        kappa_tbl = kappa_table(edges, col, u_col, v_col, weight_col, suffixes, agg, node_name)
    
    mean_std = kappa_tbl.groupby(col).agg({weight_col: ["mean", "std"]})
    mean_std.columns = ["mean", "std"]
    tbl = kappa_tbl.reset_index(col).merge(mean_std, left_on=col, right_index=True)
    # tbl["z"] = (tbl[weight_col] - tbl[(weight_col, "mean")]) / tbl[(weight_col, "std")]
    return tbl["std"].where(tbl["std"] == 0.0, (tbl[weight_col] - tbl["mean"]) / tbl["std"])

    