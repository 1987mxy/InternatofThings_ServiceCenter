Create TABLE [DataPackage](
	[PackageID] integer PRIMARY KEY UNIQUE NOT NULL COLLATE NOCASE
	,[Name] varchar(64) UNIQUE NOT NULL COLLATE RTRIM
	,[Code] binary(16) UNIQUE NOT NULL COLLATE BINARY
	,[Struct] varchar(32) COLLATE RTRIM
	,[StructLabel] text COLLATE RTRIM
	,[ExistReply] bit(1) NOT NULL DEFAULT 1 COLLATE BINARY
	,[Encrypt] varchar(8) NOT NULL DEFAULT none COLLATE RTRIM
	,[Auth] integer NOT NULL DEFAULT 0 COLLATE NOCASE
	,[Memo] text COLLATE NOCASE
);
INSERT INTO datapackage ( Name, Code, Struct, StructLabel, ExistReply, Encrypt, Auth, Memo ) VALUES ( 'PubKey', 1, 's', 'pubkey', 1, 'none', 0, '公钥' );
INSERT INTO datapackage ( Name, Code, Struct, StructLabel, ExistReply, Encrypt, Auth, Memo ) VALUES ( 'Key', 2, 'Ls', 'password,deskey', 1, 'rsa_public', 0, '口令' );
INSERT INTO datapackage ( Name, Code, Struct, StructLabel, ExistReply, Encrypt, Auth, Memo ) VALUES ( 'Response', 3, '', '', 0, 'none', 0, '响应' );
INSERT INTO datapackage ( Name, Code, Struct, StructLabel, ExistReply, Encrypt, Auth, Memo ) VALUES ( 'ShutDown', 4, '', '', 0, 'none', 0, '断开' );
INSERT INTO datapackage ( Name, Code, Struct, StructLabel, ExistReply, Encrypt, Auth, Memo ) VALUES ( 'WOL', 5, 'B', 'terminalID', 1, 'des', 10,'远程唤醒' );
INSERT INTO datapackage ( Name, Code, Struct, StructLabel, ExistReply, Encrypt, Auth, Memo ) VALUES ( 'TerminalInfo', 6, 's', 'terminalInfo', 1, 'des', 10, '终端信息' );
INSERT INTO datapackage ( Name, Code, Struct, StructLabel, ExistReply, Encrypt, Auth, Memo ) VALUES ( 'TerminalStatus', 7, 'B', 'terminalStatus', 1, 'des', 10, '终端状态' );
INSERT INTO datapackage ( Name, Code, Struct, StructLabel, ExistReply, Encrypt, Auth, Memo ) VALUES ( 'QueryTerminals', 8, '', '', 1, 'none', 10, '询问终端信息' );
INSERT INTO datapackage ( Name, Code, Struct, StructLabel, ExistReply, Encrypt, Auth, Memo ) VALUES ( 'QueryStatus', 9, '', '', 1, 'none', 10, '询问终端状态' );

Create TABLE [Terminal](
	[TerminalID] integer PRIMARY KEY UNIQUE NOT NULL COLLATE NOCASE
	,[Name] varchar(32) COLLATE RTRIM
	,[IPv6] varchar(39) UNIQUE COLLATE RTRIM
	,[IPv4] varchar(15) UNIQUE COLLATE RTRIM
	,[Mac] varchar(17) UNIQUE COLLATE RTRIM
	,[Type] varchar(16) NOT NULL COLLATE RTRIM
	,[LastActive] integer COLLATE NOCASE
);