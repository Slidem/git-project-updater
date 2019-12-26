import nxpy.command.command
import nxpy.command.option
import nxpy.core.sequence
import logging

_log = logging.getLogger(__name__)

_config = nxpy.command.option.Config(
    prefix="-",
    separator=",",
    iterable_opts=("f"), )


class MvnWrapper(nxpy.command.command.Command):
    def __init__(self, debug=None):
        super(MvnWrapper, self).__init__("mvn", debug)

    def _make_options(self, projects):
        kwargs = {}
        if projects is not None:
            kwargs["f"] = nxpy.core.sequence.make_tuple(projects)
        return kwargs

    def run_maven_commands(self, projects=None, *commands: str):
        if not commands:
            raise ValueError("Cannot run maven instructions with empty list of commands")

        command = " ".join(commands)
        _log.info(f"Running maven command: mvn {command}")                 
        self.__run_with_option(projects, command)

    def clean(self, projects=None):
        self.__run_with_option(projects, "clean")

    def install(self, projects=None):
        self.__run_with_option(projects, "install")

    def deploy(self, projects=None):
        self.__run_with_option(projects, "deploy")

    def package(self, projects=None):
        self.__run_with_option(projects, "package")

    def __run_with_option(self, projects, option):
        op = nxpy.command.option.Parser(_config, None, (option, ), {},
                                        **self._make_options(projects))
        self.run(op)
