#! /usr/bin/python
class EVENT:
    TRAINING_STARTED = "_______________Started__________________"
    TRAINING_FINISHED = "\n„„„„„„„„„„„„„„„„Done„„„„„„„„„„„„„„„„„„„„\n\n\n"
    TRAINING_STOPPED = "# STOPPED #"
    TRAINING_STEP_XML = "XML to CSV : Done"
    TRAINING_STEP_TFR = "TF records generated : Done"
    TRAINING_STEP_LABEL_MAP = "Label map generated : Done"
    TRAINING_STEP_TRAIN = "Train process : Done"
    TRAINING_STEP_INFERENCE = "Inference graphs generated : Done"


class Target:
    TRAIN = "Api_Trainings"
    QUERY = "Api_Queries"
    FEED = "Api_Feeds"
    DOWNLOAD = "Api_Downloads"
    OTHER = "Api_Home_404"

