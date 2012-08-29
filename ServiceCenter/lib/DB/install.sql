Create TABLE MAIN.[DataPackage](
	[PackageID] integer PRIMARY KEY UNIQUE NOT NULL COLLATE NOCASE
	,[Name] varchar(64) UNIQUE NOT NULL COLLATE RTRIM
	,[Code] binary(16) UNIQUE NOT NULL COLLATE BINARY
	,[Struct] varchar(32) NOT NULL COLLATE RTRIM
	,[StructLabel] text NOT NULL COLLATE RTRIM
	,[ExistReply] bit(1) NOT NULL DEFAULT 1 COLLATE BINARY
	,[Encrypt] varchar(8) NOT NULL DEFAULT none COLLATE RTRIM
	,[Memo] text COLLATE NOCASE
);
INSERT INTO datapackage ( Name, Code, Struct, StructLabel, ExistReply, Encrypt, Memo ) VALUES ( 'PubKey', 1, '32s', 'pubkey', 1, 'none', '公钥' );
INSERT INTO datapackage ( Name, Code, Struct, StructLabel, ExistReply, Encrypt, Memo ) VALUES ( 'Key', 2, '23s', 'password', 1, 'rsa_public', '口令' );
INSERT INTO datapackage ( Name, Code, Struct, StructLabel, ExistReply, Encrypt, Memo ) VALUES ( 'Response', 3, '', '', 0, 'none', '响应' );
INSERT INTO datapackage ( Name, Code, Struct, StructLabel, ExistReply, Encrypt, Memo ) VALUES ( 'ShutDown', 4, '', '', 0, 'none', '断开' );
INSERT INTO datapackage ( Name, Code, Struct, StructLabel, ExistReply, Encrypt, Memo ) VALUES ( 'WOL', 5, 'B', 'terminalID', 1, 'des','远程唤醒' );
INSERT INTO datapackage ( Name, Code, Struct, StructLabel, ExistReply, Encrypt, Memo ) VALUES ( 'TerminalInfo', 6, 's', 'terminalInfo', 1, 'des', '终端信息' );
INSERT INTO datapackage ( Name, Code, Struct, StructLabel, ExistReply, Encrypt, Memo ) VALUES ( 'TerminalStatus', 7, 'B', 'terminalStatus', 1, 'des', '终端状态' );

Create TABLE MAIN.[Terminal](
	[TerminalID] integer PRIMARY KEY UNIQUE NOT NULL COLLATE NOCASE
	,[Name] varchar(32) COLLATE RTRIM
	,[IPv6] varchar(39) UNIQUE COLLATE RTRIM
	,[IPv4] varchar(15) UNIQUE COLLATE RTRIM
	,[Mac] varchar(17) UNIQUE NOT NULL COLLATE RTRIM
	,[Type] varchar(16) NOT NULL COLLATE RTRIM
	,[LastActive] integer COLLATE NOCASE
);