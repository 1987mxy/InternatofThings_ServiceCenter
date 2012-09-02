import Global

from Log import Log
Global.Logger = Log.instance()

from DB.Database import Database
Global.DB = Database.instance()

from Package import Package
Global.Packager = Package.instance()

from TerminalManage.TerminalManage import TerminalManage
Global.TerminalManager = TerminalManage.instance()

from Listen import Listen
Global.Listener = Listen.instance()