from loguru import logger
import lxml.html
import os
import json

from modules.common.helpers.normalize_filename import process_filenames

def serialize_xml_result(xml_findbuch_in, input_file, output_path, input_type, mdb_override):
    # Serialisieren des modifizierten XML-Baums; Schreiben des Outputs als XML-Datei in das Dateisystem
    xml_output_path = None
    if input_type == 'findbuch' or input_type == 'bestandsfindbuch':
        xml_output_path = output_path + 'findbuch/' + process_filenames(input_file, restrict_length=False)
    elif input_type == 'tektonik':
        xml_output_path = output_path + 'tektonik/' + process_filenames(input_file, restrict_length=False)
    else:
        xml_output_path = output_path + 'findbuch/' + process_filenames(input_file, restrict_length=False)
        logger.warning("Im Element archdesc/@type angegebener Wert entspricht nicht den erwarteten Werten 'findbuch' oder 'tektonik'. Als Standardwert wird 'findbuch' verwendet.")
    if not mdb_override:
        os.chdir('../..')
    xml_output = open(xml_output_path, 'wb')
    xml_findbuch_in.write(xml_output, encoding='utf-8', xml_declaration=True)  # für PrettyPrint: Parameter pretty_print=True hinzufügen
    xml_output.close()

    logger.info("Prozessierung erfolgreich. Ausgabe: {}".format(xml_output_path))

def serialize_json_result(xml_findbuch_in, input_file, output_path, input_type):
    if input_type == 'findbuch' or input_type == 'bestandsfindbuch':
        output_path_prefix = "findbuch"
    elif input_type == 'tektonik':
        output_path_prefix = "tektonik"
    else:
        output_path_prefix = "findbuch"

    os.chdir('../..')

    if type(xml_findbuch_in) is list:
        # Ausgabe mehrerer JSON-Dateien
        for item in xml_findbuch_in:
            json_output_path = output_path + '{}/{}.json'.format(output_path_prefix, item["object_id"])
            logger.debug("Ausgabepfad: {}".format(os.path.abspath(json_output_path)))
            with open(json_output_path, 'w') as json_output:
                json.dump(item["json_object"], json_output)
                logger.info("Prozessierung erfolgreich. Ausgabe: {}".format(json_output_path))
    else:
        # Ausgabe nur einer JSON-Datei
        json_output_path = output_path + '{}/{}.json'.format(output_path_prefix, process_filenames(input_file))
        with open(json_output_path, 'wb') as json_output:
            json.dump(xml_findbuch_in, json_output)

        logger.info("Prozessierung erfolgreich. Ausgabe: {}".format(json_output_path))

def serialize_html_result(html_template_in, html_type, findbuch_file_in, html_data, html_output_path):
    """Serialisieren der statischen Seiten als HTML und schreiben in das Dateisystem."""

    if html_type == "Gliederungsgruppen":
        if not os.path.exists("../preview/Gliederungsgruppen"):
            os.makedirs("../preview/Gliederungsgruppen")
        output_file = "{} {}.html".format(process_filenames(findbuch_file_in), process_filenames(html_data["Titel"]))

    elif html_type == "Bestaende":
        if not os.path.exists("../preview/Bestaende"):
            os.makedirs("../preview/Bestaende")
        output_file = "{} {}.html".format(process_filenames(html_data["Bestandssignatur"]).replace(html_data["Institution"], ""), process_filenames(html_data["Titel"]))

    elif html_type == "Verzeichnungseinheiten":
        if not os.path.exists("../preview/Verzeichnungseinheiten"):
            os.makedirs("../preview/Verzeichnungseinheiten")
        output_file = "{} {}.html".format(process_filenames(html_data["Archivaliensignatur"]).replace(html_data["Institution"] + ", ", ""), process_filenames(html_data["Titel"]))

    elif html_type == "Technische_Validierung":
        if not os.path.isdir("Technische_Validierung"):
            os.mkdir("Technische_Validierung")
        output_file = "{}.html".format(html_data["Titel"])

    elif html_type == "Validierung":
        if not os.path.exists(html_output_path):
            os.makedirs(html_output_path)
        output_file = "Validierung.html"

    else:
        if not os.path.isdir("Statistik"):
            os.mkdir("Statistik")
        output_file = "{}_{}.html".format(process_filenames(findbuch_file_in), html_data["Titel"])

    output_path = html_output_path + output_file

    try:
        html_output = open(output_path, 'wb')
    except FileNotFoundError:
        logger.warning("Der folgende Dateipfad ist zu lang, Dateiname wird gekürzt: {}".format(output_path))
        full_path = os.path.abspath(output_path)
        html_output = open(full_path[:245] + ".html", 'wb')

    xml_string = lxml.html.tostring(html_template_in, pretty_print=True)
    html_output.write(xml_string)
    html_output.close()
