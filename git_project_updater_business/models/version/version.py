from enum import Enum, auto


class ChildVersion:

    def __init__(self, value: str, version_type: "ChildVersionType"):
        self.value = value
        self.version_type = version_type

    def __str__(self):
        return self.value

class MavenChildVersion(ChildVersion):

    def __init__(self, value, version_type, property_tag_value):
        super().__init__(value, version_type)
        self.property_tag_value = property_tag_value

       
class ChildVersionType(Enum):

    PARENT_PROJECT_VERSION = auto()

    PROJECT_VERSION = auto()

    PROJECT_PROPERTY_VERSION = auto()

    PARENT_PROJECT_PROPERTY_VERSION = auto()

    ARTIFACT_VERSION = auto()

    DEPENDENCY_MANAGEMENT_ARTIFACT_VERSION = auto()

    PARENT_DEPENDECY_MANAGEMENT_ARTIFACT_VERSION = auto()
 
