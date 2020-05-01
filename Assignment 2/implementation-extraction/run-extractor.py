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

    # regex_extractor.extract_contents_rtvslo(
    #     "../input-extraction/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html")

    # regex_extractor.extract_contents_gsc("../input-extraction/globalscaleco.com/gsc04.html")

    # XPATH
    # xpath_extractor.extract_content_overstock("../input-extraction/overstock.com/jewelry01.html")
    # xpath_extractor.extract_content_gsc("../input-extraction/globalscaleco.com/gsc03.html")
    # xpath_extractor.extract_content_rtvslo(
    #     "../input-extraction/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html")
    # xpath_extractor.extract_content_rtvslo(
    #     "../input-extraction/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html")

    # ROAD-RUNNER
    sys.setrecursionlimit(3000)
    # roadrunner.run("../input-extraction/overstock.com/jewelry01.html",
    #                "../input-extraction/overstock.com/jewelry02.html")
    roadrunner.run("../input-extraction/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html",
                   "../input-extraction/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html",
                   encoding='utf-8')
