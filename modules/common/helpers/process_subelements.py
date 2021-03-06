def add_to_processed_string(processed_string, structured_element, ignore_linebreaks):
    """wenn Element Absätze oder andere Strukturelemente enthält, diese verarbeiten, analog zum Template process_html"""
    for sub_element in structured_element:
        if sub_element.text is not None:
            if not (processed_string.endswith("<br />")) and len(
                    processed_string) > 0 and sub_element.tag not in ignore_linebreaks:
                processed_string += "<br />"
            if sub_element.tag in tuple(["{urn:isbn:1-931666-22-9}span", "{urn:isbn:1-931666-22-9}em"]) and not processed_string.endswith(" "):
                processed_string += " {}".format(sub_element.text)
            else:
                processed_string += sub_element.text
        if sub_element.tail is not None:
            if len(processed_string) > 0 and sub_element.tag not in ignore_linebreaks:
                processed_string += "<br />"
            elif len(processed_string) > 0 and not processed_string.endswith(tuple([" ", "<br />"])) and not sub_element.tail.startswith(tuple([" ", ",", ".", ";", ":", "?", "!", "/"])):
                processed_string += " "
            processed_string += sub_element.tail
        if sub_element.tail is None and sub_element.tag == "{urn:isbn:1-931666-22-9}lb" and sub_element.tag not in ignore_linebreaks:
            sub_element_sibling = sub_element.getnext()
            if sub_element_sibling is not None:
                if sub_element_sibling.tag == "{urn:isbn:1-931666-22-9}lb":
                    processed_string += "<br />"
        if len(sub_element) > 0:  # Abprüfen auf weitere Sub-Elemente (innerhalb des gerade behandelten Elements)
            processed_string = add_to_processed_string(processed_string, sub_element, ignore_linebreaks)


    return processed_string


def parse_xml_content(structured_element, prefix, input_file, attributes = None, ignore_linebreaks = None):
    # Umsetzung des Templates process_html in Python --> process_subelements (process_html) sowie replace_subelements (delete_html)
    # Werden im Parameter attributes Elementnamen übergeben, so werden auch die entsprechenden Attributwerte verarbeitet.
    # Werden im Parameter ignore_linebreaks Elementnamen übergeben, so wird der Elementinhalt nicht durch Zeilenumbrüche vom übrigen String separiert.

    if ignore_linebreaks is None:
        ignore_linebreaks = []

    processed_string = ""
    processed_string_prefix = ""

    if structured_element is not None:
        if structured_element.text is not None:  # or len(structured_element) > 0
            processed_string += structured_element.text

        if prefix is not None:
            if prefix != "":
                if not processed_string.startswith(prefix):
                    if not prefix.endswith(":"):
                        processed_string_prefix += "{}: ".format(prefix)
                    else:
                        processed_string_prefix += "{} ".format(prefix)

        processed_string = processed_string_prefix + processed_string

        processed_string = add_to_processed_string(processed_string, structured_element, ignore_linebreaks)

    if attributes is not None:
        if not processed_string.endswith("<br />") and len(processed_string) > 0:
            processed_string += "<br />"
        for attribute_i, attribute in enumerate(attributes):
            processed_string += structured_element.attrib[attribute]
            if attribute_i < len(attributes)-1:
                processed_string += " - "


    return processed_string