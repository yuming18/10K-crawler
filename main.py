"Crawl 10k report from https://www.sec.gov/edgar/searchedgar/companysearch.html"

import argparse
import logging 
import os
from utils import Params, setlogger
from utils import get_cik_list
from crawler import crawl_all

parser = argparse.ArgumentParser()
parser.add_argument("--model_path", default="./", help="Directory contain json file with input parameters")
parser.add_argument("--data_path", default="rawdata/", help="csv file of storing cik index.")
parser.add_argument("--save_dir", default="result/", help="dir of saving output json files")

if __name__ == "__main__":

    args = parser.parse_args()

    if not os.path.exists(os.path.join(os.getcwd(), args.save_dir)):
        os.makedirs(os.path.join(os.getcwd(), args.save_dir))

    json_path = os.path.join(args.model_path, "params.json")
    assert os.path.isfile(json_path), "No json file is found at {}".format(args.model_path)
    params = Params(json_path)

    # why?
#    print(params.file_type)
#    print(params.__dict__)
#    params.file_type = "10-Q"
#    print(params.file_type)
#    print(params.__dict__)
    
    log_path = os.path.join(args.model_path, "info.log")
    setlogger(log_path)

    logging.info("Get cik index")
    cik_list = get_cik_list(os.path.join(args.data_path, "cik_ticker.csv"))

    crawl_all(params, cik_list, args.save_dir)
