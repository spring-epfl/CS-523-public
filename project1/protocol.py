from expression import Expression


class ProtocolSpec:
    """Specification of the SMC protocol.

    Attributes:
        participant_ids: List of IDs of the participating clients
        expr: Expression to be computed
    """

    def __init__(self, participant_ids: list, expr: Expression):
        self.participant_ids = participant_ids
        self.expr = expr
