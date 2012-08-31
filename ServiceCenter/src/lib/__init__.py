import Global

from DB.Database import Database
Global.DB = Database.instance()

from Log import Log
Global.Logger = Log.instance()

from Package import Package
Global.Packager = Package.instance()

from Listen import Listen
Global.Listener = Listen.instance()

from TerminalManage.TerminalManage import TerminalManage
Global.TerminalManager = TerminalManage.instance()