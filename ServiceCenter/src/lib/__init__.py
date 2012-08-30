from DB import DB
from Config import srvCenterConf
from Package import Package
from Listen import Listen

Packager = Package.instance( DB, srvCenterConf )
Listener = Listen.instance( srvCenterConf )