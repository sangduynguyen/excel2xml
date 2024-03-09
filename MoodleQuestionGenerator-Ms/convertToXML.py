import pandas as pd

question_types = [
    {
        "name": "Sheet1",
        #"name": "Multiple Choice",
        "type": "multichoice"
    },
]

from xml.etree.ElementTree import Element, SubElement, Comment

from xml.etree import ElementTree
from xml.dom import minidom


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


# Configure one attribute with set()
def convert_to_xml(file):
    root = Element('quiz')

    for question_type in question_types:
        data = pd.read_excel(file, sheet_name=question_type['name'])
        data = data.fillna('')
        if question_type['type'] == 'matching':
            data = data.groupby('Question Type', as_index=False)
        else:
            data = data.iterrows()
        for _, d in data:
            question = Element('question', {'type': question_type['type']})
            SubElement(question, 'shuffleanswers').text = 'true'
            SubElement(question, 'idnumber').text = ''
            SubElement(question, 'hidden').text = '0'
            if question_type['type'] == 'multichoice':
                SubElement(SubElement(question, 'name'), 'text').text = str(d['Question Text'])
                SubElement(SubElement(question, 'questiontext'), 'text').text = str(d['Question Type'])
                SubElement(question, 'defaultgrade').text = '1.0000000'
	#SubElement(question, 'penalty').text = '0.3333333'
                #SubElement(SubElement(question, 'generalfeedback'), 'text').text = str(d['Feedback'])
                #SubElement(question, 'defaultgrade').text = '{0}.0000000'.format(int(d['Marks']))
	#SubElement(question, 'defaultgrade').text = '1.0000000'
                SubElement(question, 'single').text = 'true'
                SubElement(question, 'answernumbering').text = 'ABC'
                SubElement(question, 'showstandardinstruction').text = '0'
                SubElement(SubElement(question, 'correctfeedback'), 'text').text = 'Your answer is correct.'
                #SubElement(SubElement(question, 'partiallycorrectfeedback'), 'text').text = 'Your answer is partially correct.'
                SubElement(SubElement(question, 'incorrectfeedback'), 'text').text = 'Your answer is incorrect.'
                SubElement(question, 'shownumcorrect').text = ''
                for i in range(1, 5):
                    answer = SubElement(question, 'answer', {'fraction': '100' if '{0}'.format(i) == str(d['Correct Answer']) else '0'})
	    #answer = SubElement(question, 'answer', {'fraction': '100' if 'Option {0}'.format(i) == str(d['Correct Answer']) else '0'})
                    SubElement(answer, 'text').text = str(d['Option {0}'.format(i)])
	    #SubElement(answer, 'text').text = str(d['Option {0}'.format(i)])
	    #SubElement(answer, 'text').text = str(d['{0}'.format(i)])
                    #SubElement(SubElement(answer, 'feedback'), 'text').text = str(d['Option {0} Feedback'.format(i)])
            else:
                continue
            root.append(question)
    return prettify(root)
