import easygraph as eg 
import networkx as nx
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}
import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)
from icecream import ic

listFileName_1998 = []
for i in range(1,10):
    listFileName_1998.append('dataCAIDA/AS_relationships/raw/19980'+str(i)+ '01.as-rel.txt')
for i in range(10,13):
    listFileName_1998.append('dataCAIDA/AS_relationships/raw/1998'+str(i)+ '01.as-rel.txt')

def readList(fn) -> list:
    listResult = []
    ifile = open(fn,'r')
    for line_ in ifile:
        line = line_[:-1]
        listResult.append(line)

    return listResult


def readDict(fn,separator=':') -> dict:
    dictResult = {}
    ifile = open(fn,'r')
    for line_ in ifile:
        line = line_[:-1]
        line_list = line.split(separator)
        dictResult[line_list[0].strip()] = line_list[1].strip()

    return dictResult

def readRank(fn,separator=':') -> dict:
    dictResult = {}
    ifile = open(fn,'r')
    i = 0
    for line_ in ifile:
        i += 1
        line = line_[:-1]
        line_list = line.split(separator)
        dictResult[line_list[0]] = i

    return dictResult

def getVersionFromName(fn:str) -> str:
    return fn[31:39] 


def readCommunity(version) -> dict:
    dict_community_asList = {}
    ifile_community = open(f"playEgOnData/results/{version}/community_louvain",'r')
    num = 0
    for line in ifile_community:
        list_AS = line[:-1].split(",")
        dict_community_asList[num] = list_AS
        num += 1
    ifile_community.close()
    return dict_community_asList


def buildAsRelGraph(version,flag_directed = True, flag_community = False) -> eg.DiGraph:
    if flag_directed:
        G = eg.DiGraph()
    else:
        G = eg.Graph()
    
    if flag_community:
        dict_asn_community = {}
        ifile_community = open(f"playEgOnData/results/{version}/community_louvain",'r')
        num = 0
        for line in ifile_community:
            list_AS = line[:-1].split(",")
            for asn in list_AS:
                dict_asn_community[int(asn)] = num 
            num += 1
        ifile_community.close()


    ifileName = 'dataCAIDA/AS_relationships/raw/'+version+'.as-rel.txt'
    ifile = open(ifileName,'r')

    for line in ifile:
        if line[0] == '#': # comment
            continue
        listLine = line.split('|')  # ASN|ASN|type
        type_edge = int(listLine[2])
        asn1 = int(listLine[0])
        asn2 = int(listLine[1])

        if flag_community:  
            num_community1 = -1
            num_community2 = -1
            if asn1 in dict_asn_community:
                num_community1 = dict_asn_community[asn1]
            if asn2 in dict_asn_community:
                num_community2 = dict_asn_community[asn2]
            G.add_node(asn1, node_attr={'community':num_community1})
            G.add_node(asn2, node_attr={'community':num_community2})
            G.add_edge(asn1, asn2)  # ,edge_attr={'type':type_edge}
        else:
            G.add_edge(asn1, asn2)  # ,edge_attr={'type':type_edge}
        if type_edge == 0 and flag_directed: # if undirected, no need to add edge: # peer edge
            G.add_edge(asn2, asn1) # ,edge_attr={'type':type_edge}
    return G


def buildAsRelGraph_nx(ifileName, flag_directed = True) -> nx.DiGraph:
    if flag_directed:
        # Create an empty DiGraph
        G = nx.DiGraph()
    else:
        G = nx.Graph()

    # Open the file and read in the edges
    with open(ifileName, 'r') as f:
        for line in f:
            if line[0] == '#': # comment
                continue
            # Split the line into node1, node2, and edge_type
            node1, node2, edge_type = line.strip().split('|')
            
            # Convert edge_type to an integer
            edge_type = int(edge_type)
            
            # Add the appropriate edges to the graph
            G.add_edge(int(node1), int(node2))
            if edge_type == 0 and flag_directed: # if undirected, no need to add edge
                G.add_edge(int(node2), int(node1))

    # Print the graph
    print(G.edges())
    return G


def getG(version,DEBUG = False,flag_directed = True, flag_nx = False, flag_community = False):
    if flag_nx:
        if DEBUG:
            G = nx.DiGraph() if flag_directed else nx.Graph()
            G.add_edges_from([(5,6),(7,8),(6,5),(1,20),(2,1),(2,7),(20,8)])
            
        else:  
            fn = 'dataCAIDA/AS_relationships/raw/'+version+'.as-rel.txt'
            G = buildAsRelGraph_nx(fn,flag_directed)
    else:  # eg
        if DEBUG:
            G = eg.DiGraph() if flag_directed else eg.Graph()
            G.add_edges([(5,6),(7,8),(6,5),(1,20),(2,1)])
        else:  
            G = buildAsRelGraph(version,flag_directed, flag_community)
    return G


