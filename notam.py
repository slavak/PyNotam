import parsimonious

grammar = parsimonious.Grammar(r"""
    header = notamn_header / notamr_header / notamc_header
    notamn_header = notam_id _ "NOTAMN"
    notamr_header = notam_id _ "NOTAMR" _ notam_id
    notamc_header = notam_id _ "NOTAMC" _ notam_id
    notam_id = ~r"[A-Z][0-9]{4}/[0-9]{2}"

    q_clause = "Q)" _ fir "/" notam_code "/" traffic_type "/" purpose "/" scope "/" lower_limit "/" upper_limit "/" area_of_effect
    fir = icao_id
    notam_code = ~r"Q[A-Z]{4}"
    traffic_type = ~r"(?=[IVK]+)I?V?K?"
    purpose = ~r"(?=[NBOMK]+)N?B?O?M?K?"
    scope = ~"(?=[AEWK]+)A?E?W?K?"
    lower_limit = int3
    upper_limit = int3
    area_of_effect = ~r"(?P<lat>[0-9]{4}[NS])(?P<long>[0-9]{5}[EW])(?P<radius>[0-9]{3})"

    a_clause = "A)" _ location_icao
    location_icao = icao_id

    b_clause = "B)" _ datetime
    c_clause = "C)" _ ((datetime estimated?) / permanent)
    estimated = "EST"
    permanent = "PERM"

    d_clause = "D)" _ ~r".*?(?=(?:$)|(?: E\)))"m

    _ = " "
    icao_id = ~r"[A-Z]{4}"
    datetime = int2 int2 int2 int2 int2 # year month day hours minutes
    int2 = ~r"[0-9]{2}"
    int3 = ~r"[0-9]{3}"
""")
