from extractors import regex_extractor, xpath_extractor
# from roadrunner.roadrunner import roadrunner
from roadrunner import roadrunner
import argparse
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # parser.add_argument("algorithm", help='type of algorithm: regex, xpath, roadrunner')
    # args = parser.parse_args()

    # REGEX
    # xpath_extractor.extract_content_overstock("../input-extraction/overstock.com/jewelry01.html")
    # regex_extractor.extract_contents_rtvslo(
    #     "../input-extraction/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html")
    # regex_extractor.extract_contents_gsc("../input-extraction/globalscaleco.com/gsc04.html")


    # XPATH

    # xpath_extractor.extract_content_gsc("../input-extraction/globalscaleco.com/gsc03.html")


    # ROAD-RUNNER
    sys.setrecursionlimit(1500)
    roadrunner.run("../input-extraction/overstock.com/jewelry01.html",
                   "../input-extraction/overstock.com/jewelry02.html")
