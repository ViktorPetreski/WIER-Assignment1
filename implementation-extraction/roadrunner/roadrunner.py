from lxml import html
from utils.utils import *


def run(wrapper, sample, encoding="iso-8859-1"):
    wrapper = prettify(wrapper, encoding=encoding)
    sample = prettify(sample, encoding=encoding)
    res_final = roadrunner(wrapper, sample, 0, 0, [])
    res = "".join(res_final)
    document_root = html.fromstring(res)
    pretty_html = html.tostring(document_root, encoding='unicode', pretty_print=True, method="html")
    print(pretty_html)
    # with open("globalscaleco_wrapper.html", "w", encoding = encoding) as file:
    #     file.write(pretty_html)


def roadrunner(wrapper, sample, i, j, result):
    """
       The main algorithm.
       :param wrapper: the wrapper page
       :param sample: the sample page
       :param i: current position in the wrapper page
       :param j: current position in the sample page
       :param result: The current partial generated wrapper (Not the same as the wrapper param)
       :return: The finished wrapper
       """
    if i == len(wrapper) or j == len(sample):  # finish the recursion
        return result
    # get the current html element from the wrapper and sample
    line_wrapper = wrapper[i]
    line_sample = sample[j]
    if line_sample == line_wrapper:  # check if the elements are the same and add them
        result.append(line_wrapper)
        return roadrunner(wrapper, sample, i + 1, j + 1, result)  # onto the next
    # the elements are not the same but they are strings
    elif not check_tag(line_wrapper) and not check_tag(line_sample):
        result.append("#text")
        return roadrunner(wrapper, sample, i + 1, j + 1, result)  # onto the next
    # none of the above worked so.. potential loops :'(
    else:
        # previous tags
        prev_wrapper_tag = wrapper[i - 1]
        prev_sample_tag = sample[j - 1]
        is_optional = False  # whether it is optional element or not

        # First check if there are loops:

        # loop detected in the wrapper
        # the previous tag is closing, current is opening and they are of the same nature ex.(<li> </li>)
        if ending_tag(prev_wrapper_tag) and starting_tag(line_wrapper) and compare_base_of_tags(prev_wrapper_tag,
                                                                                                line_wrapper):
            # find the squares
            internal_wrapper, internal_sample, next_i = match_square(wrapper, line_wrapper, i)

            if internal_sample is not None:
                # call the algorithm with the smaller squares found. Here it is called with wrapper and sample from
                # the same list (in this case, the wrapper)
                internal_result = roadrunner(internal_wrapper, internal_sample, 0, 0, [])
                if internal_result is not None:
                    # if something is found, create a loop badge?? from that
                    res_string = "({})+".format("".join(internal_result))
                    if res_string != result[-1]:  # append only if it is not the same as the previous element/loop
                        result.append(res_string)
                    return roadrunner(wrapper, sample, next_i, j, result)
                else:
                    is_optional = True  # nothing found, should be optional
            else:
                is_optional = True  # nothing found, should be optional
        # loop detected in the sample (everything else is the same as in the wrapper part
        elif ending_tag(prev_sample_tag) and starting_tag(line_sample) and compare_base_of_tags(prev_sample_tag,
                                                                                                line_sample):
            internal_sample, internal_wrapper, next_j = match_square(sample, line_sample, j)
            if internal_sample is not None:
                internal_result = roadrunner(internal_wrapper, internal_sample, 0, 0, [])
                if internal_result is not None:
                    res_string = "({})+".format("".join(internal_result))
                    if res_string != result[-1]:
                        result.append(res_string)
                    return roadrunner(wrapper, sample, i, next_j, result)
                else:
                    is_optional = True  # nothing found, should be optional
            else:
                is_optional = True  # nothing found, should be optional
        else:
            is_optional = True  # nothing found, should be optional

        # it detected optional
        if is_optional:

            if check_tag(line_wrapper) and check_tag(line_sample):
                # Two tags on the same line, find which one is optional
                found_wrap, counter_wrap, res_wrap = assess_next_lines(line_wrapper, sample, j)
                found_samp, counter_samp, res_samp = assess_next_lines(line_sample, wrapper, i)

                if counter_wrap <= counter_samp:
                    if result[-1][-1] == "?":
                        latest_item = result.pop(-1)
                        res_wrap = "{}{}".format(latest_item[:-2], res_wrap)

                        if found_wrap:
                            result.append(res_wrap)
                    return roadrunner(wrapper, sample, i, j + counter_wrap, result)
                else:
                    if result[-1][-1] == "?":
                        latest_item = result.pop(-1)
                        res_samp = "{}{}".format(latest_item[:-2], res_samp)
                    if found_samp:
                        result.append(res_samp)
                    return roadrunner(wrapper, sample, i + counter_samp, j, result)

            elif check_tag(line_wrapper):
                found_wrap, counter_wrap, res_wrap = assess_next_lines(line_wrapper, sample, j)
                # this is to avoid multiple )? after each optional
                if result[-1][-1] == "?":
                    latest_item = result.pop(-1)
                    res_wrap = "{}{}".format(latest_item[:-2], res_wrap)
                if found_wrap:
                    result.append(res_wrap)
                return roadrunner(wrapper, sample, i, j + counter_wrap, result)

            elif check_tag(line_sample):
                found_samp, counter_samp, res_samp = assess_next_lines(line_sample, wrapper, i)
                if result[-1][-1] == "?":
                    latest_item = result.pop(-1)
                    res_samp = "{}{}".format(latest_item[:-2], res_samp)
                if found_samp:
                    result.append(res_samp)
                return roadrunner(wrapper, sample, i + counter_samp, j, result)
            else:  # nothing is found, have to move on
                return roadrunner(wrapper, sample, i + 1, j + 1, result)
