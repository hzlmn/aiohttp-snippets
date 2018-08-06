from functools import partial

import trafaret as t

NotEmptyList = partial(t.List, min_length=1)

stringify = lambda value: "".join(value)

UserTrafaret = t.Dict(
    {
        t.Key("email"): NotEmptyList(t.String) >> stringify,
        t.Key("name"): NotEmptyList(t.String) >> stringify,
    }
).allow_extra("*")

UsersOutputTrafaret = NotEmptyList(UserTrafaret)
