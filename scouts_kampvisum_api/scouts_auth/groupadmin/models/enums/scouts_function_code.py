class AbstractScoutsFunctionCode:

    GROUP_LEADER = "GRL"
    ADJUNCT_GROUP_LEADER = "AGRL"
    GROUP_LEADER_TEAM = "GRLP"
    TEAM_RESPONSIBLE_GROUP_LEADER_TEAM = "PGRL"

    DISTRICT_COMMISSIONER = "DC"
    ADJUNCT_DISCTRICT_COMMISSIONER = "ADC"

    SHIRE_PRESIDENT = "GV"
    ADJUNCT_SHIRE_PRESIDENT = "AGV"
    SHIRE_COMMISSIONER = "GC"
    ADJUNCT_SHIRE_COMMISSIONER = "AGC"
    ADJUNCT_SHIRE_COMMISSIONER_DIVERSITY = "AGCD"
    ADJUNCT_SHIRE_COMMISSIONER_OPEN_CAMP = "AGCO"
    ADJUNCT_SHIRE_COMMISSIONER_AKABE = "AGCA"
    ADJUNCT_SHIRE_COMMISSIONER_EDUCATION = "AGCV"
    ADJUNCT_SHIRE_COMMISSIONER_ECOLOGY = "AGCE"
    ADJUNCT_SHIRE_COMMISSIONER_SPIRITUALITY = "AGCZ"
    SHIRE_MANAGER = "GB"
    ADJUNCT_SHIRE_MANAGER = "AGB"

    UNKNOWN = ""

    code: str

    def __init__(self, code: str = None):
        if not code or len(code) == 0:
            code = self.UNKNOWN
        self.code = code

    def is_group_leader(self):
        return self.code in (
            self.GROUP_LEADER,
            self.ADJUNCT_GROUP_LEADER,
            self.GROUP_LEADER_TEAM,
            self.TEAM_RESPONSIBLE_GROUP_LEADER_TEAM,
        )

    def is_district_commissioner(self):
        return self.code in (
            self.DISTRICT_COMMISSIONER,
            self.ADJUNCT_DISCTRICT_COMMISSIONER,
        )
    
    def is_shire_president(self):
        return self.code in (
            self.SHIRE_PRESIDENT,
            self.ADJUNCT_SHIRE_PRESIDENT,
            self.SHIRE_COMMISSIONER,
            self.ADJUNCT_SHIRE_COMMISSIONER,
            self.ADJUNCT_SHIRE_COMMISSIONER_DIVERSITY,
            self.ADJUNCT_SHIRE_COMMISSIONER_OPEN_CAMP,
            self.ADJUNCT_SHIRE_COMMISSIONER_AKABE,
            self.ADJUNCT_SHIRE_COMMISSIONER_EDUCATION,
            self.ADJUNCT_SHIRE_COMMISSIONER_ECOLOGY,
            self.ADJUNCT_SHIRE_COMMISSIONER_SPIRITUALITY,
            self.SHIRE_MANAGER,
            self.ADJUNCT_SHIRE_MANAGER,
        )
