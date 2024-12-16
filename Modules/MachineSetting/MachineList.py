import enum

class MachineList(enum.Enum):
    filterCoverScrewMachine = "Filter Cover"
    RUConnectorScrewMachine = "RU Connector"
    FUAssemblyMachine = "FU Assembly"
    rearMissingInspectionMachine = "missing Inspection"
    housing_connector_packing = "Housing connector packing"
    loadFrameMachine = "Load Frame"
    locationDetect = "Location Detect"
    demo_color_detect = "Demo Color Detect"
    demo_location_detect = "Demo location detect"
    demo_classify = "Classify"
    demo_circle_measurement = "Circle measurement"
    demo_line_measurement = "Line measurement"
    demo_counting = "Counting"
    demo_focus_checking = "Focus checking"
    roto_weighing = "Roto Weighing"
    fpc_inspection = "FPC Inspection"
    fpc_verify = "FPC Verify"
    ddk_inspection = "DDK Inspection"
    hik_barcode_demo = "Hik Barcode Demo"
    reading_weighing = "Reading Weighing"
    e_map_checking = "EMAP Checking"
    counting_in_conveyor = "Counting In Conveyor"
    washing_machine_inspection = "Washing Machine Inspection"
    syc_phone_check = "SYC Phone Check" # khai báo chương trình
    all = "all"

    def isFilterCoverScrewMachine(self):
        return self is self.filterCoverScrewMachine

    def isRUConnectorScrewMachine(self):
        return self is self.RUConnectorScrewMachine

    def isFUAssemblyMachine(self):
        return self is self.FUAssemblyMachine

    def isLoadFrameMachine(self):
        return self is self.loadFrameMachine

    def isRearMissingInspectionMachine(self):
        return self is self.rearMissingInspectionMachine

    def is_housing_connector_packing(self):
        return self is self.housing_connector_packing

    def isLocationDetect(self):
        return self is self.locationDetect

    def is_demo_color_detect(self):
        return self is self.demo_color_detect

    def is_demo_classify(self):
        return  self is self.demo_classify

    def is_demo_location_detect(self):
        return self is self.demo_location_detect

    def is_roto_weighing_robot(self):
        return self is self.roto_weighing

    def is_demo_circle_measurement(self):
        return self is self.demo_circle_measurement

    def is_demo_line_measurement(self):
        return self is self.demo_line_measurement

    def is_demo_counting(self):
        return self is self.demo_counting

    def is_focus_checking(self):
        return self is self.demo_focus_checking

    def is_fpc_inspection(self):
        return self is self.fpc_inspection

    def is_fpc_verify(self):
        return self is self.fpc_verify

    def is_ddk_inspection(self):
        return self is self.ddk_inspection

    def is_syc_phone_check(self): # nhận biết đang chạy ctrinh nào
        return self is self.syc_phone_check

    def is_hik_barcode_demo(self):
        return self is self.hik_barcode_demo

    def is_e_map_checking(self):
        return self is self.e_map_checking

    def is_reading_weighing(self):
        return self is self.reading_weighing

    def is_counting_in_conveyor(self):
        return self is self.counting_in_conveyor

    def is_washing_machine_inspection(self):
        return self is self.washing_machine_inspection