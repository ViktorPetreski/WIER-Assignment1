from extractors import regex_extractor, xpath_extractor
from roadrunner.roadrunner import roadrunner
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # parser.add_argument("algorithm", help='type of algorithm: regex, xpath, roadrunner')
    # args = parser.parse_args()
    # regex_extractor.extract_contents("./input-extraction/overstock.com/jewelry01.html")
    # regex_extractor.extract_contents("./input-extraction/overstock.com/jewelry02.html")
    # xpath_extractor.extract_content("./input-extraction/overstock.com/jewelry01.html")
    # prettify.run("./input-extraction/WebPages/overstock.com/jewelry01.html", "./WebPages/overstock.com/jewelry02.html")
    # regex_extractor.extract_contents_rtvslo(
    #     "../input-extraction/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html")
    # regex_extractor.extract_contents_gsc("../input-extraction/globalscaleco.com/gsc04.html")
    xpath_extractor.extract_content_gsc("../input-extraction/globalscaleco.com/gsc03.html")
