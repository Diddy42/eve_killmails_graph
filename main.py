from utils import get_list_of_past_dates
from EveRefUtils import update_data
from GraphUtils import build_graph_from_dates, get_pagerank, get_connected_components, show_graph

data_dir = 'data/'
numDays = 1

update_data(numDays, data_dir)

dates = get_list_of_past_dates(numDays)
g = build_graph_from_dates(dates, data_dir)

'''res = get_connected_components(g)
i = 0
for el in res:
    if i == 266:
        cc = el
    print(i, list(el))
    i = i + 1

subgraph = g.subgraph(cc)
show_graph(subgraph)'''





