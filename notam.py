import parsimonious
import datetime

grammar = parsimonious.Grammar(r"""
    root = "(" header __ q_clause __ a_clause __ b_clause __ c_clause __ (d_clause __)? e_clause (__ f_clause __ g_clause)? ")"

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

    a_clause = "A)" _ location_icao ("/" location_icao)*
    location_icao = icao_id

    b_clause = "B)" _ datetime
    c_clause = "C)" _ ((datetime estimated?) / permanent)
    estimated = "EST"
    permanent = "PERM"

    d_clause = "D)" _ till_next_clause
    e_clause = "E)" _ till_next_clause
    f_clause = "F)" _ till_next_clause
    g_clause = "G)" _ till_next_clause

    _ = " "
    __ = " " / "\n"
    icao_id = ~r"[A-Z]{4}"
    datetime = int2 int2 int2 int2 int2 # year month day hours minutes
    int2 = ~r"[0-9]{2}"
    int3 = ~r"[0-9]{3}"
    till_next_clause = ~r".*?(?=(?:\)$)|(?:\s[A-Z]\)))"s
""")

class EstimatedDateTime(datetime.datetime):
    """Represents an estimated point in time. Instances are identical to datetime.datetime in every way,
    except that the instance will have an attribute 'is_estimated' which is set to True."""

    def __new__(cls, *args, **kwargs):
        """May be initialized either identically to a regular datetime.datetime or, optionally, by
        providing an existing datetime object to copy."""

        if not kwargs and len(args)==1 and isinstance(args[0], datetime.datetime):
            other = args[0]
            v = super().__new__(cls, other.year, other.month, other.day,
                                     other.hour, other.minute, other.second,
                                     other.microsecond, other.tzinfo)
        else:
            v = super().__new__(cls, *args, **kwargs)
        v.is_estimated = True
        return v

class NotamParseVisitor(parsimonious.NodeVisitor):
    grammar = grammar

    @staticmethod
    def has_descendant(node, desc_name):
        if node.expr_name == desc_name: return True
        else: return any([NotamParseVisitor.has_descendant(c,desc_name) for c in node.children])

    def visit_simple_regex(self, node, _): return node.match.group(0)
    visit_till_next_clause = visit_simple_regex

    def visit_code_node(self, *args, meanings):
        """Maps coded strings, where each character encodes a special meaning, into a corresponding decoded set
        according to the meanings dictionary (see examples of usage further below)"""
        codes = self.visit_simple_regex(*args)
        return set([meanings[code] for code in codes])

    def visit_intX(self, *args):
        v = self.visit_simple_regex(*args)
        return int(v)

    visit_int2 = visit_intX
    visit_int3 = visit_intX

    @staticmethod
    def visit_notamX_header(notam_type):
        def inner(self, _, visited_children):
            self.notam_id = visited_children[0]
            self.notam_type = notam_type
            if self.notam_type in ('REPLACE', 'CANCEL'):
                self.ref_notam_id = visited_children[-1]
        return inner

    visit_notamn_header = visit_notamX_header.__func__('NEW')
    visit_notamr_header = visit_notamX_header.__func__('REPLACE')
    visit_notamc_header = visit_notamX_header.__func__('CANCEL')

    visit_icao_id = visit_simple_regex
    visit_notam_id = visit_simple_regex
    visit_notam_code = visit_simple_regex

    def visit_q_clause(self, node, visited_children):
        self.fir = visited_children[2]
        self.fl_lower = visited_children[12]
        self.fl_upper = visited_children[14]

    def visit_notam_code(self, *args):
        self.notam_code = self.visit_simple_regex(*args) # TODO: Parse this into the code's meaning. One day...

    def visit_traffic_type(self, *args):
        self.traffic_type = self.visit_code_node(*args, meanings={'I' : 'IFR',
                                                                  'V' : 'VFR',
                                                                  'K' : 'CHECKLIST'})

    def visit_purpose(self, *args):
        self.purpose = self.visit_code_node(*args, meanings={'N' : 'IMMEDIATE ATTENTION',
                                                             'B' : 'OPERATIONAL SIGNIFICANCE',
                                                             'O' : 'FLIGHT OPERATIONS',
                                                             'M' : 'MISC',
                                                             'K' : 'CHECKLIST'})

    def visit_scope(self, *args):
        self.scope = self.visit_code_node(*args, meanings={'A' : 'AERODROME',
                                                           'E' : 'EN-ROUTE',
                                                           'W' : 'NAV WARNING',
                                                           'K' : 'CHECKLIST'})

    def visit_area_of_effect(self, node, _):
        self.area = node.match.groupdict() # dictionary containing mappings for 'lat', 'long', and 'radius'
        self.area['radius'] = int(self.area['radius'])

    def visit_a_clause(self, node, _):
        def _dfs_icao_id(n):
            if n.expr_name == "icao_id": return [self.visit_simple_regex(n, [])]
            return sum([_dfs_icao_id(c) for c in n.children], []) # flatten list-of-lists
        self.location = _dfs_icao_id(node)

    def visit_b_clause(self, node, visited_children):
        self.valid_from = visited_children[2]

    def visit_c_clause(self, node, visited_children):
        if self.has_descendant(node, 'permanent'):
            dt = datetime.datetime.max
        else:
            dt = visited_children[2][0][0]
            if self.has_descendant(node, 'estimated'):
                dt = EstimatedDateTime(dt)
        self.valid_till = dt

    def visit_d_clause(self, _, visited_children):
        self.schedule = visited_children[2]

    def visit_e_clause(self, _, visited_children):
        self.body = visited_children[2]

    def visit_f_clause(self, _, visited_children):
        self.limit_lower = visited_children[2]

    def visit_g_clause(self, _, visited_children):
        self.limit_upper = visited_children[2]

    def visit_datetime(self, node, visited_children):
        dparts = visited_children
        dparts[0] = 1900 + dparts[0] if dparts[0] > 80 else 2000 + dparts[0] # interpret 2-digit year
        return datetime.datetime(*dparts, tzinfo=datetime.timezone.utc)

    def generic_visit(self, _, visited_children):
        return visited_children

    def visit_root(self, _, __):
        pass