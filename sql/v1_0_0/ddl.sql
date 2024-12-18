DROP TABLE IF EXISTS `account`;
DROP TABLE IF EXISTS `sub_account`;
DROP TABLE IF EXISTS `inner_journal_entry`;
DROP TABLE IF EXISTS `journal_entry`;

create table IF not exists `account` (
    `id` VARCHAR(40) NOT NULL,
    `name` VARCHAR(100) NOT NULL, -- 勘定科目名
    `description` VARCHAR(500) NOT NULL, -- 説明
    `dept` INTEGER(4) NOT NULL, -- 分類(当座資産など)
    `bs_pl` INTEGER(4) NOT NULL, -- 分類(BSかPL)
    `credit_debit` INTEGER(4) NULL, -- 分類(借方か貸方)
    `createDate` DATETIME NOT NULL,
    `createObjectId` VARCHAR(40) NOT NULL,
    `updateDate` DATETIME NOT NULL,
    `updateObjectId` VARCHAR(40) NOT NULL,
    PRIMARY KEY(`id`)
) DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;

create table IF not exists `sub_account` (
    `id` VARCHAR(40) NOT NULL,
    `name` VARCHAR(100) NOT NULL,-- 名前
    `account_id` VARCHAR(40) NOT NULL, -- 勘定科目id
    `description` VARCHAR(100) NOT NULL, -- 説明
    `createDate` DATETIME NOT NULL,
    `createObjectId` VARCHAR(40) NOT NULL,
    `updateDate` DATETIME NOT NULL,
    `updateObjectId` VARCHAR(40) NOT NULL,
    PRIMARY KEY(`id`)
) DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;

create table IF not exists `inner_journal_entry` (
    `id` VARCHAR(40) NOT NULL,
    `journal_entry_id` VARCHAR(40) NOT NULL, -- 仕訳id
    `account_id` VARCHAR(40) NOT NULL, -- 勘定科目id
    `sub_account_id` VARCHAR(40) NOT NULL, -- 補助科目id
    `amount` INTEGER(10) NOT NULL, -- 金額
    `credit_debit` INTEGER(4) NULL, -- 貸方借方
    `index` INTEGER(10) NULL, -- 仕訳中の位置(借方貸方ごと)
    `createDate` DATETIME NOT NULL,
    `createObjectId` VARCHAR(40) NOT NULL,
    `updateDate` DATETIME NOT NULL,
    `updateObjectId` VARCHAR(40) NOT NULL,
    PRIMARY KEY(`id`)
) DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;

create table IF not exists `journal_entry` (
    `id` VARCHAR(40) NOT NULL,
    `date` DATE NOT NULL, -- 日時
    `status` INTEGER(4) NOT NULL, -- 状態
    `createDate` DATETIME NOT NULL,
    `createObjectId` VARCHAR(40) NOT NULL,
    `updateDate` DATETIME NOT NULL,
    `updateObjectId` VARCHAR(40) NOT NULL,
    PRIMARY KEY(`id`)
) DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;
