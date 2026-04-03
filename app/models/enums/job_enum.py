import enum

class JobSource(enum.Enum):
    djinni = "djinni"
    workua = "workua"
    dou = "dou"

class JobLevel(enum.Enum):
    junior = "junior"
    middle = "middle"
    senior = "senior"
    any = "any"

class JobRemote(enum.Enum):
    full_remote = "full_remote"
    part_time = "part_time"
    office = "office"
    any = "any" 