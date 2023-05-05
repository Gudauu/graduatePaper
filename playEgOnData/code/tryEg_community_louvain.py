from include import *
from time import *
import community


if __name__ == '__main__':
    DEBUG = True
    # versions = ['19980101','19980201','19980301','19980401']
    for year in range(2000,2023+1):

        version = f"{year}0101"

        G = getG(version, flag_directed = False, flag_nx = True)

        # run community detection louvain
        # Run Louvain community detection algorithm
        partition = community.best_partition(G)

        # Create a dictionary to store the communities
        communities = {}

        # Loop through each node and its community assignment
        for node, community_id in partition.items():
            # If the community doesn't exist yet, create a new one
            if community_id not in communities:
                communities[community_id] = []

            # Add the node to the community
            communities[community_id].append(str(node))
        ofile = open(f"playEgOnData/results/{version}/community_louvain","w")
        # Print the communities in an easy-to-read format
        for i, nodes in communities.items():
            ofile.write(f"{','.join(sorted(nodes))}\n")
            # print(f"Community {i}: {', '.join(sorted(nodes))}")

        ofile.close()

    

    
    
    
    