
#This is used by the generic holon system gui monitor
GuiPluginPath = ["paintshop", "agv/system"]

#This is only used by the gui to filter which holons are visible
#it should be the other way around and only define which holons we do not wnt to see
KnownHolonTypes = [
    "::hms.Agent",
    "::hms::Holon",
    "::hms::agv::AGVCentralHolon",
    "::hms::agv::AGVHolon",
    "::hms::agv::AGVOrderHolon",
    "::hms::agv::AGVOrderHolonFactory",
    '::hms::agv::Localizer',
    '::hms::agv::VelocityController',
    '::hms::agv::MotorController',
    '::hms::agv::AGVGMEInfo',
    '::hms::agv::PathPlanner',
    "::hms::agv::"
    ]




