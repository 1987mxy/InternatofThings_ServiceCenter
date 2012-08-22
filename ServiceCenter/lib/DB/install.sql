Create TABLE MAIN.[DataPackage](
	[PackageID] integer PRIMARY KEY UNIQUE NOT NULL COLLATE NOCASE
	,[Name] varchar(64) UNIQUE NOT NULL COLLATE RTRIM
	,[Code] binary(16) UNIQUE NOT NULL COLLATE BINARY
	,[Struct] varchar(32) NOT NULL COLLATE RTRIM
	,[StructLabel] text NOT NULL COLLATE RTRIM
	,[Memo] text COLLATE NOCASE
);
INSERT INTO datapackage ( Name, Code, Struct, StructLabel, Memo ) VALUES ( 'PubKey', 1, '56s', 'pubkey', '公钥' );
INSERT INTO datapackage ( Name, Code, Struct, StructLabel, Memo ) VALUES ( 'Key', 2, '47s', 'password', '口令' );
INSERT INTO datapackage ( Name, Code, Struct, StructLabel, Memo ) VALUES ( 'Response', 3, '', '', '响应' );
INSERT INTO datapackage ( Name, Code, Struct, StructLabel, Memo ) VALUES ( 'ShutDown', 4, '', '', '断开' );
INSERT INTO datapackage ( Name, Code, Struct, StructLabel, Memo ) VALUES ( 'WOL', 5, 'B', 'terminalID','远程唤醒' );
INSERT INTO datapackage ( Name, Code, Struct, StructLabel, Memo ) VALUES ( 'TerminalInfo', 6, 's', 'terminalInfo', '终端信息' );
INSERT INTO datapackage ( Name, Code, Struct, StructLabel, Memo ) VALUES ( 'TerminalStatus', 7, 'B', 'terminalStatus', '终端状态' );

Create TABLE MAIN.[Terminal](
	[TerminalID] integer PRIMARY KEY UNIQUE NOT NULL COLLATE NOCASE
	,[Name] varchar(32) COLLATE RTRIM
	,[IPv6] varchar(39) UNIQUE COLLATE RTRIM
	,[IPv4] varchar(15) UNIQUE COLLATE RTRIM
	,[Mac] varchar(17) UNIQUE NOT NULL COLLATE RTRIM
	,[Type] varchar(16) NOT NULL COLLATE RTRIM
	,[LastActive] integer NOT NULL COLLATE NOCASE
);