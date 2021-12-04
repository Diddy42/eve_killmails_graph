from utils import TrackProgress
import networkx as nx
import matplotlib.pyplot as plt
from EveRefUtils import from_date_to_filename, tar_to_json_list, extract_ch_ids_from_killmail

def show_graph(graph):
    nx.draw(graph)
    plt.draw()
    plt.show()

def build_graph_from_dates(date_list, data_dir):
    killmails = []

    for d in date_list:
        killmails_filename = from_date_to_filename(d)
        killmails.extend(tar_to_json_list(data_dir + killmails_filename))

    print(len(killmails))
    g = nx.Graph()
    
    tp = TrackProgress()

    i = 0
    for km in killmails:
        ch_ids = extract_ch_ids_from_killmail(km)
        
        for c_outer in ch_ids:
            for c_inner in ch_ids:
                if c_outer != c_inner:
                    g.add_edge(c_outer, c_inner, killmail_id=km['killmail_id'])

        perc = (i/len(killmails))*100
        tp.check(perc)
        i = i + 1

        
    
    print(g.number_of_nodes(), g.size())

    #i need to sort it
    #pr = nx.pagerank(g)
    #print(pr)

    '''connected_components = nx.connected_components(g)
    for cc in connected_components:
        print(cc)'''


    #show_graph(g)
