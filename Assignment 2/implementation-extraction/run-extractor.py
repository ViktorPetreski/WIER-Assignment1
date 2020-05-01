from extractors import regex_extractor, xpath_extractor
# from roadrunner.roadrunner import roadrunner
from roadrunner import roadrunner
import argparse
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("algorithm", help='type of algorithm: regex, xpath, roadrunner')
    args = parser.parse_args()

    values = vars(args)
    if values['algorithm'] == 'regex':
        regex_extractor.extract_contents("../input-extraction/overstock.com/jewelry01.html")
        regex_extractor.extract_contents("../input-extraction/overstock.com/jewelry02.html")
        regex_extractor.extract_contents_rtvslo(
            "../input-extraction/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html")
        regex_extractor.extract_contents_rtvslo(
            "../input-extraction/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html")
        regex_extractor.extract_contents_gsc("../input-extraction/globalscaleco.com/gsc03.html")
        regex_extractor.extract_contents_gsc("../input-extraction/globalscaleco.com/gsc04.html")

    if values['algorithm'] == 'xpath':
        xpath_extractor.extract_content_overstock("../input-extraction/overstock.com/jewelry01.html")
        xpath_extractor.extract_content_overstock("../input-extraction/overstock.com/jewelry02.html")
        xpath_extractor.extract_content_rtvslo(
            "../input-extraction/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html")
        xpath_extractor.extract_content_rtvslo(
            "../input-extraction/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html")
        xpath_extractor.extract_content_gsc("../input-extraction/globalscaleco.com/gsc03.html")
        xpath_extractor.extract_content_gsc("../input-extraction/globalscaleco.com/gsc04.html")

    if values['algorithm'] == 'roadrunner':
        sys.setrecursionlimit(3000)
        print('OVERSTOCK')
        roadrunner.run("../input-extraction/overstock.com/jewelry01.html",
                       "../input-extraction/overstock.com/jewelry02.html")
        print('RTVSLO')
        roadrunner.run(
            "../input-extraction/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html",
            "../input-extraction/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html",
            encoding='utf-8')
        print('GLOBALSCALECO')
        roadrunner.run(
            "../input-extraction/globalscaleco.com/gsc03.html",
            "../input-extraction/globalscaleco.com/gsc04.html", encoding='utf-8')
