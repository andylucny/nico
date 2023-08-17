from .hand import AbstractHand


class RH6DHand(AbstractHand):
    """This class represents the Seed Robotics RH4D Hand."""

    current_limit = 225

    sensitive_motors = ("thumb_z", "thumb_x", "indexfinger_x", "middlefingers_x")

    current_ports = {
        "wrist_z": 0,
        "wrist_x": 1,
        "thumb_z": 2,
        "thumb_x": 3,
        "indexfinger_x": 4,
        "middlefingers_x": 5,
    }

    poses = {
        "pointAt": {
            "indexfinger_x": (-170.0, 1.0),
            "middlefingers_x": (150.0, 1.0),
            "thumb_x": (60.0, 0.6),
            "thumb_z": (150.0, 1.0),
        },
        "openHand": {
            "indexfinger_x": (-150.0, 1.0),
            "middlefingers_x": (-150.0, 1.0),
            "thumb_x": (-150.0, 1.0),
            "thumb_z": (-150.0, 1.0),
        },
        "closeHand": {
            "indexfinger_x": (120.0, 1.0),
            "middlefingers_x": (120.0, 1.0),
            "thumb_x": (60.0, 0.6),
            "thumb_z": (150.0, 1.0),
        },
        "thumbsUp": {
            "indexfinger_x": (150.0, 1.0),
            "middlefingers_x": (150.0, 1.0),
            "thumb_x": (-150.0, 1.0),
            "thumb_z": (-150.0, 1.0),
        },
        "okSign": {
            "indexfinger_x": (-25.0, 1.0),
            "middlefingers_x": (-170.0, 1.0),
            "thumb_x": (-25.0, 1.0),
            "thumb_z": (45.0, 1.0),
        },
        "pinchToIndex": {
            "indexfinger_x": (-25.0, 1.0),
            "middlefingers_x": (150.0, 1.0),
            "thumb_x": (-25.0, 1.0),
            "thumb_z": (45.0, 1.0),
        },
        "keyGrip": {
            "indexfinger_x": (30.0, 1.0),
            "middlefingers_x": (150.0, 1.0),
            "thumb_x": (30.0, 1.0),
            "thumb_z": (-170.0, 1.0),
        },
        "pencilGrip": {
            "indexfinger_x": (90.0, 0.5),
            "middlefingers_x": (150.0, 1.0),
            "thumb_x": (60.0, 0.6),
            "thumb_z": (150.0, 1.0),
        },
        "prepareGrab": {
            "indexfinger_x": (-150.0, 1.0),
            "middlefingers_x": (-150.0, 1.0),
            "thumb_x": (-150.0, 1.0),
            "thumb_z": (150.0, 1.0),
        },
    }

    conversion_angles = {}

    def __init__(self, robot, isLeft, monitorCurrents=True, vrep=False):
        super(RH6DHand, self).__init__(robot, isLeft, monitorCurrents, vrep=vrep)
