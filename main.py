from utils import get_list_of_past_dates
from EveRefUtils import update_data
from GraphUtils import build_graph_from_dates

data_dir = 'data/'
numDays = 1

update_data(numDays, data_dir)

dates = get_list_of_past_dates(numDays)
build_graph_from_dates(dates, data_dir)




