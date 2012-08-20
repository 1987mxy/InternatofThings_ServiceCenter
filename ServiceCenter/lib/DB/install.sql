Create TABLE MAIN.[DataPackage](
	[PackageID] integer PRIMARY KEY UNIQUE NOT NULL COLLATE RTRIM
	,[Protocol] varchar(16) NOT NULL COLLATE NOCASE
	,[Name] varchar(64) UNIQUE NOT NULL COLLATE RTRIM
	,[Direction] byte NOT NULL COLLATE BINARY
	,[Code] binary(16) UNIQUE NOT NULL COLLATE BINARY
	,[Struct] varchar(32) NOT NULL COLLATE RTRIM
	,[Memo] text COLLATE NOCASE
);
INSERT INTO datapackage ( Protocol, Name, Direction, Code, Struct, Memo ) VALUES ( 'TCP', 'PubKey', 2, 1, '<16s', '公钥' );
INSERT INTO datapackage ( Protocol, Name, Direction, Code, Struct, Memo ) VALUES ( 'TCP', 'Key', 1, 2, '<L', '口令' );
INSERT INTO datapackage ( Protocol, Name, Direction, Code, Struct, Memo ) VALUES ( 'TCP', 'Response', 0, 3, '', '响应' );
INSERT INTO datapackage ( Protocol, Name, Direction, Code, Struct, Memo ) VALUES ( 'TCP', 'ShutDown', 0, 4, '', '断开' );
INSERT INTO datapackage ( Protocol, Name, Direction, Code, Struct, Memo ) VALUES ( 'TCP', 'WOL', 1, 5, '<4B', '远程唤醒' );
INSERT INTO datapackage ( Protocol, Name, Direction, Code, Struct, Memo ) VALUES ( 'TCP', 'TerminalStatusDetail', 2, 6, '<', '终端状态(详细)' );
INSERT INTO datapackage ( Protocol, Name, Direction, Code, Struct, Memo ) VALUES ( 'TCP', 'TerminalStatus', 2, 7, '<', '终端状态' );

Create TABLE MAIN.[Terminal](
	[TerminalID] integer PRIMARY KEY UNIQUE NOT NULL COLLATE NOCASE
	,[IPv6] varchar(39) UNIQUE COLLATE RTRIM
	,[IPv4] varchar(15) UNIQUE COLLATE RTRIM
	,[Mac] varchar(17) UNIQUE NOT NULL COLLATE RTRIM
	,[Type] byte(1) NOT NULL COLLATE BINARY
	,[IsActive] bit(1) NOT NULL COLLATE BINARY
);