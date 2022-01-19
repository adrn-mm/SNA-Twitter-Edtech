# Import Libraries
from functools import reduce

import community
import networkx as nx
import pandas as pd

# Import Datasets
edglst_zenius = pd.read_csv(
    r"c:\\Users\\LENOVO\\OneDrive\\Desktop\\Tugas Akhir\\Programming\\data\\post-preprocessing/zenius-edglst.csv"
)
edglst_ruangguru = pd.read_csv(
    r"c:\\Users\\LENOVO\\OneDrive\\Desktop\\Tugas Akhir\\Programming\\data\\post-preprocessing/ruangguru-edglst.csv"
)

# Convert to Networkx Graph
g_ruangguru, g_zenius = [
    nx.from_pandas_edgelist(x, source="Source", target="Target", edge_attr="Weight")
    for x in [edglst_ruangguru, edglst_zenius]
]
# convert undirected graph
g_ruangguru = g_ruangguru.to_undirected()
g_zenius = g_zenius.to_undirected()

# Size & Order
size_ruangguru, order_ruangguru = [g_ruangguru.size(), g_ruangguru.order()]
size_zenius, order_zenius = [g_zenius.size(), g_zenius.order()]
print(
    "Size dan Order dari Graf Ruangguru: "
    + str(size_ruangguru)
    + " dan "
    + str(order_ruangguru)
)
print(
    "Size dan Order dari Graf Zenius: " + str(size_zenius) + " dan " + str(order_zenius)
)

# Density
density_ruangguru = nx.classes.function.density(g_ruangguru)
density_zenius = nx.classes.function.density(g_zenius)
print("Density dari Graf Ruangguru: " + str(density_ruangguru))
print("Density dari Graf Zenius: " + str(density_zenius))

# Connected Components
conn_ruangguru = nx.number_connected_components(g_ruangguru)
conn_zenius = nx.number_connected_components(g_zenius)
print("Connected Components dari Graf Ruangguru: " + str(conn_ruangguru))
print("Connected Components dari Graf Zenius: " + str(conn_zenius))

"""
Define All Functions
"""

# modularity funcion
def modularity(g):
    mod = community.modularity(community.best_partition(g, resolution=1), g)
    return mod


# diamater function
def diameter(g):
    return max([max(j.values()) for (i, j) in nx.all_pairs_shortest_path_length(g)])


# average path length function
def avg_path(g):
    return sum([sum(j.values()) for (i, j) in nx.all_pairs_shortest_path_length(g)]) / (
        g.order() * (g.order() - 1)
    )


# average degree function
def avg_deg(g):
    return sum([val for (node, val) in g.degree()]) / g.order()


# degree centrality function
def degree_c(g):
    res = nx.algorithms.centrality.degree_centrality(g)
    return (
        pd.DataFrame(
            list(zip(list(res.keys()), list(res.values()))),
            columns=["Node", "Degree Centrality"],
        )
        .sort_values("Degree Centrality", ascending=False)
        .reset_index(drop=True)
    )


# betweenness centrality function
def betweenness_c(g):
    res = nx.algorithms.centrality.betweenness_centrality(g, normalized=False)
    return (
        pd.DataFrame(
            list(zip(list(res.keys()), list(res.values()))),
            columns=["Node", "Betweenness Centrality"],
        )
        .sort_values("Betweenness Centrality", ascending=False)
        .reset_index(drop=True)
    )


# closeness centrality function
def closeness_c(g):
    res = nx.algorithms.centrality.closeness_centrality(g, wf_improved=True)
    return (
        pd.DataFrame(
            list(zip(list(res.keys()), list(res.values()))),
            columns=["Node", "Closeness Centrality"],
        )
        .sort_values("Closeness Centrality", ascending=False)
        .reset_index(drop=True)
    )


# eigenvector centrality function
def eigen_c(g):
    res = nx.algorithms.centrality.eigenvector_centrality(g, weight=None)
    return (
        pd.DataFrame(
            list(zip(list(res.keys()), list(res.values()))),
            columns=["Node", "Eigenvector Centrality"],
        )
        .sort_values("Eigenvector Centrality", ascending=False)
        .reset_index(drop=True)
    )


# all centrality function
def all_centrality(deg, bet, clos, eig):
    return reduce(
        lambda left, right: pd.merge(left, right, on=["Node"]), [deg, bet, clos, eig]
    ).sort_values(
        [
            "Degree Centrality",
            "Betweenness Centrality",
            "Closeness Centrality",
            "Eigenvector Centrality",
        ],
        ascending=[False, False, False, False],
    )


# adding attributes to graph function
def data_to_gephi(g):
    nx.set_node_attributes(
        g, community.best_partition(g, resolution=1), "Modularity Class"
    )
    nx.set_node_attributes(g, nx.betweenness_centrality(g), "Betweenness Centrality")
    return g


"""
Implement The Function
"""
# apply the modularity function
mod_ruangguru, mod_zenius = [modularity(g) for g in [g_ruangguru, g_zenius]]
print("Modularity dari Graf Ruangguru: " + str(mod_ruangguru))
print("Modularity dari Graf Zenius: " + str(mod_zenius))
# implement the diameter function
d_ruangguru, d_zenius = [diameter(x) for x in [g_ruangguru, g_zenius]]
print("Diameter dari Graf Ruangguru: " + str(d_ruangguru))
print("Diameter dari Graf Zenius: " + str(d_zenius))
# implement the average path length function
avgpath_ruangguru, avgpath_zenius = [avg_path(x) for x in [g_ruangguru, g_zenius]]
print("Average Path Length dari Graf Ruangguru: " + str(avgpath_ruangguru))
print("Average Path Length dari Graf Zenius: " + str(avgpath_zenius))
# implement the average degree function
avgdeg_ruangguru, avgdeg_zenius = [avg_deg(g) for g in [g_ruangguru, g_zenius]]
print("Average Degree dari Graf Ruangguru: " + str(avgdeg_ruangguru))
print("Average Degree dari Graf Zenius: " + str(avgdeg_zenius))
# implement the degree centrality function
df_degreecent_ruangguru, df_degreecent_zenius = [
    degree_c(x) for x in [g_ruangguru, g_zenius]
]
# implement the betweenness centrality function
df_betwenncent_ruangguru, df_betwenncent_zenius = [
    betweenness_c(x) for x in [g_ruangguru, g_zenius]
]
# implement the close centrality function
df_closecent_ruangguru, df_closecent_zenius = [
    closeness_c(x) for x in [g_ruangguru, g_zenius]
]
# implement the eigenvector centrality function
df_eigencent_ruangguru, df_eigencent_zenius = [
    eigen_c(x) for x in [g_ruangguru, g_zenius]
]
# implement all centrality function
df_centrality_ruangguru = all_centrality(
    df_degreecent_ruangguru,
    df_betwenncent_ruangguru,
    df_closecent_ruangguru,
    df_eigencent_ruangguru,
)

df_centrality_zenius = all_centrality(
    df_degreecent_zenius,
    df_betwenncent_zenius,
    df_closecent_zenius,
    df_eigencent_zenius,
)
# implement the adding attributes to graph
g_ruangguru, g_zenius = [data_to_gephi(x) for x in [g_ruangguru, g_zenius]]
# write to gexf
nx.write_gexf(
    g_ruangguru,
    r"c:\Users\LENOVO\OneDrive\Desktop\Tugas Akhir\Programming\data\to-gephi\ruangguru.gexf",
)
nx.write_gexf(
    g_zenius,
    r"c:\Users\LENOVO\OneDrive\Desktop\Tugas Akhir\Programming\data\to-gephi\zenius.gexf",
)

"""
Transform to CSV Format
"""
# network properties
lst_column = ["Metrics", "Ruangguru", "Zenius"]
data = [
    ["Size", size_ruangguru, size_zenius],
    ["Order", order_ruangguru, order_zenius],
    ["Density", density_ruangguru, density_zenius],
    ["Modularity", mod_ruangguru, mod_zenius],
    ["Diameter", d_ruangguru, d_zenius],
    ["Average Path Length", avgpath_ruangguru, avgpath_zenius],
    ["Average Degree", avgdeg_ruangguru, avgdeg_zenius],
    ["Connected Component", conn_ruangguru, conn_zenius],
]
df_prop = pd.DataFrame(data, columns=lst_column)
df_prop.to_csv(
    r"c:\Users\LENOVO\OneDrive\Desktop\Tugas Akhir\Programming\data\post-SNA\network-properties\network_properties.csv",
    index=False,
    header=True,
)
# degree centrality
df_degreecent_ruangguru.to_csv(
    r"c:\Users\LENOVO\OneDrive\Desktop\Tugas Akhir\Programming\data\post-SNA\centrality\degree-centrality\ruangguru-degree.csv",
    index=False,
    header=True,
)
df_degreecent_zenius.to_csv(
    r"c:\Users\LENOVO\OneDrive\Desktop\Tugas Akhir\Programming\data\post-SNA\centrality\degree-centrality\zenius-degree.csv",
    index=False,
    header=True,
)
# closeness centrality
df_closecent_ruangguru.to_csv(
    r"c:\Users\LENOVO\OneDrive\Desktop\Tugas Akhir\Programming\data\post-SNA\centrality\closeness-centrality\ruangguru-closeness.csv",
    index=False,
    header=True,
)
df_closecent_zenius.to_csv(
    r"c:\Users\LENOVO\OneDrive\Desktop\Tugas Akhir\Programming\data\post-SNA\centrality\closeness-centrality\zenius-closeness.csv",
    index=False,
    header=True,
)
# betweenness centrality
df_betwenncent_ruangguru.to_csv(
    r"c:\Users\LENOVO\OneDrive\Desktop\Tugas Akhir\Programming\data\post-SNA\centrality\betweenness-centrality\ruangguru-betweenness.csv",
    index=False,
    header=True,
)
df_betwenncent_zenius.to_csv(
    r"c:\Users\LENOVO\OneDrive\Desktop\Tugas Akhir\Programming\data\post-SNA\centrality\betweenness-centrality\zenius-betweenness.csv",
    index=False,
    header=True,
)
# eigen centrality
df_eigencent_ruangguru.to_csv(
    r"c:\Users\LENOVO\OneDrive\Desktop\Tugas Akhir\Programming\data\post-SNA\centrality\eigenvector-centrality\ruangguru-eigenvector.csv",
    index=False,
    header=True,
)
df_eigencent_zenius.to_csv(
    r"c:\Users\LENOVO\OneDrive\Desktop\Tugas Akhir\Programming\data\post-SNA\centrality\eigenvector-centrality\zenius-eigenvector.csv",
    index=False,
    header=True,
)
# all centrality
df_centrality_ruangguru.to_csv(
    r"c:\Users\LENOVO\OneDrive\Desktop\Tugas Akhir\Programming\data\post-SNA\centrality\all-centrality-ruangguru.csv",
    index=True,
    header=True,
)
df_centrality_zenius.to_csv(
    r"c:\Users\LENOVO\OneDrive\Desktop\Tugas Akhir\Programming\data\post-SNA\centrality\all-centrality-zenius.csv",
    index=True,
    header=True,
)
