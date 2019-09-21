class MavenPom:
    def __init__(self, **kwargs):
        self.artifact = kwargs.get("artifact", None)
        self.parent_artifact = kwargs.get("parent_artifact", None)
        self.modules = kwargs.get("modules", None)
        self.dependencies = kwargs.get("dependencies", None)
        self.dependencies_management = kwargs.get("dependencies_management", None)
        self.properties = kwargs.get("properties", None)
        self.__validate()

    def is_parent(self):
        return self.artifact.packaging == "pom"

    def __validate(self):
        if self.__valid_nullable_maven_artifact(self.artifact) is False or self.__valid_nullable_maven_artifact(self.parent_artifact) is False:
            raise ValueError("Expected a MavenArtifact")

        if self.__valid_nullable_list_type(self.modules, str) is False:
            raise ValueError("Expected list of strings for modules")

        if self.__valid_nullable_dict_type(self.properties, str) is False:
            raise ValueError(
                "Expected dict of string values for properties")

        if self.__valid_nullable_dict_type(self.dependencies, MavenArtifact) is False:
            raise ValueError(
                "Expected dict with MavenArtifact values for dependencies")

        if self.__valid_nullable_dict_type(self.dependencies_management, MavenArtifact) is False:
            raise ValueError(
                "Expected dict with MavenArtifact values for dependencies management")

    def __valid_nullable_maven_artifact(self, v):
        return not v or isinstance(v, MavenArtifact)

    def __valid_nullable_list_type(self, l, list_type):
        if not l:
            return True

        if not isinstance(l, list):
            return False

        for m in l:
            if not isinstance(m, list_type):
                return False

    def __valid_nullable_dict_type(self, d, dict_value_type):
        if not d:
            return True

        if not isinstance(d, dict):
            return False

        for key, value in d.items():
            if not isinstance(value, dict_value_type):
                return False


class MavenArtifact:
    def __init__(self, **kwargs):
        self.artifact_id = kwargs.get("artifact_id", None)
        self.group_id = kwargs.get("group_id", None)
        self.version = kwargs.get("version", None)
        self.scope = kwargs.get("scope", None)
        self.packaging = kwargs.get("packaging", None)

    def __str__(self):
        return "artifact id: " + self.artifact_id + "\n" + "group id: " + self.group_id + "\n" + "version: " + self.version + "\n" + "scope: " + self.scope
