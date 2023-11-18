import xml.etree.ElementTree as ET

class testxmledit:

    def editevents(self):

        # Parse the XML data
        tree = ET.parse('Content/xmlfiles/events.xml')
        root = tree.getroot()

        # Find and update events with "Vehicle" in the name
        for event in root.findall("./event"):
            name = event.get('name')
            if 'Vehicle' in name:
                # Find the <active> tag and set its text to '0'
                active_tag = event.find('active')
                if active_tag is not None:
                    active_tag.text = '1'

        # Save the modified XML
        tree.write('Content/xmlfiles/events.xml')

inst = testxmledit()
inst.editevents()