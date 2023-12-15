import xml.etree.ElementTree as ET

def extract_steps_from_xml(xml_content):

    root = ET.fromstring(xml_content)

    results_pod = root.find(".//pod[@title='Results']")

    if results_pod is not None:
        # Find the subpod with the title 'Possible intermediate steps' under the 'Results' pod
        subpod = results_pod.find(".//subpod[@title='Possible intermediate steps']")

        if subpod is not None:
            # Find the plaintext tag under the subpod
            plaintext_tag = subpod.find('.//plaintext')

            if plaintext_tag is not None:
                # Extract the text from the plaintext tag
                steps_text = plaintext_tag.text
                return steps_text

    return None