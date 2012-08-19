Create TABLE MAIN.[DataPackage](
	[PackageID] integer PRIMARY KEY UNIQUE NOT NULL COLLATE RTRIM
	,[Protocol] varchar(16) NOT NULL COLLATE NOCASE
	,[Name] varchar(64) UNIQUE NOT NULL COLLATE RTRIM
	,[Code] binary(16) UNIQUE NOT NULL COLLATE BINARY
	,[Struct] varchar(32) NOT NULL COLLATE RTRIM
	,[StructLabel] text NOT NULL COLLATE RTRIM
	,[Memo] text COLLATE NOCASE
);
INSERT INTO datapackage ( Protocol, Name, Code, Struct, StructLabel, Memo ) VALUES ( 'UDP', 'WOL', hex( 1 ), '104s', 'content', '远程唤醒' );
Create TABLE MAIN.[Terminal](
	[TerminalID] integer PRIMARY KEY UNIQUE NOT NULL COLLATE NOCASE
	,[IPv6] varchar(39) UNIQUE COLLATE RTRIM
	,[IPv4] varchar(15) UNIQUE COLLATE RTRIM
	,[Mac] varchar(17) UNIQUE NOT NULL COLLATE RTRIM
	,[Type] byte(1) NOT NULL COLLATE BINARY
	,[IsActive] bit(1) NOT NULL COLLATE BINARY
);