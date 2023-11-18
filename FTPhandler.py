import logging as log
import datetime as dt
import os
import xml.etree.ElementTree as ET
import ApiHandler
import time



class FTPhandler:

    def __init__(self):
        log_time = dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')  # Time to be set as file name
        current_dir = os.path.dirname(__file__)
        log_file_path = os.path.join(current_dir, 'Content', 'Logs', f'Log_{log_time}.txt')
        log.basicConfig(
            filename=log_file_path,
            level=log.DEBUG,
            format=f'[%(asctime)s] -- %(message)s',
            filemode='a'
        )

    def FtpVehicleReset(self, selectedService):
        path = "dayzstandalone%2Fmpmissions%2FdayzOffline.chernarusplus%2Fcustom%2Fevents.xml"

        def editVehiclesReset0():
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
                        active_tag.text = '0'
            # Save the modified XML
            tree.write('Content/xmlfiles/events.xml')

        def editVehiclesReset1():
            # Parse the XML data
            tree = ET.parse('Content/xmlfiles/events.xml')
            root = tree.getroot()
            # Find and update events with "Vehicle" in the name
            for event in root.findall("./event"):
                name = event.get('name')
                if 'Vehicle' in name:
                    # Find the <active> tag and set its text to '1'
                    active_tag = event.find('active')
                    if active_tag is not None:
                        active_tag.text = '1'
            # Save the modified XML
            tree.write('Content/xmlfiles/events.xml')

        for Service in selectedService:
            editVehiclesReset0()
            if instAPI.apiRemoveFile(Service, "dayzstandalone\mpmissions\dayzstandaloneTestServer\mpmissions\dayzOffline.chernarusplus\custom\events.xml"):
                instAPI.apiRestartService(Service)

            while not instAPI.apiGetServiceStatus(Service):
                log.info("Checking service status")
                time.sleep(5)

            editVehiclesReset1()
            if instAPI.apiAddFile(Service, "dayzstandalone\mpmissions\dayzstandaloneTestServer\mpmissions\dayzOffline.chernarusplus\custom", "Content/xmlfiles/events.xml"):
                instAPI.apiRestartService(Service)




instAPI = ApiHandler.ApiHandler()
