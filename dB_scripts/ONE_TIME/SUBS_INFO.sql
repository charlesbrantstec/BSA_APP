CREATE TABLE [IF NOT EXISTS] SUBS_INFO
(
    SUB_ID
    SERIAL
    PRIMARY
    KEY
    NOT
    NULL,
    SUB_NAME
    VARCHAR
(
    100
) NOT NULL,
    ADDR VARCHAR
(
    200
),
    EIN VARCHAR
(
    30
),
    ITIN VARCHAR
(
    30
),
    SS VARCHAR
(
    30
)
    );