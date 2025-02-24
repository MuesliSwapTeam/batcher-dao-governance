from opshin.prelude import *
from batcher_dao_governance.onchain.utils.ext_interval import *
from opshin.std.builtins import *
from opshin.std.fractions import *

ProposalId = int

EMTPY_TOKENNAME_DICT: Dict[bytes, int] = {}
EMPTY_VALUE_DICT: Value = {}


def proposal_id_later_than(id: ProposalId, other_id: ProposalId) -> bool:
    return id > other_id


def get_minting_purpose(context: ScriptContext) -> Minting:
    purpose = context.purpose
    assert isinstance(purpose, Minting)
    return purpose


def get_spending_purpose(context: ScriptContext) -> Spending:
    purpose = context.purpose
    assert isinstance(purpose, Spending)
    return purpose


@dataclass
class ProposalParams(PlutusData):
    """
    Non-updatable parameters of a proposal
    """

    CONSTR_ID = 0
    # the required quorum for the proposal to be valid
    quorum: int
    # the required threshold for the winning proposal to win
    winning_threshold: Fraction
    # the proposals that can be voted on
    proposals: List[Anything]
    # the end time of the vote
    end_time: ExtendedPOSIXTime
    proposal_id: ProposalId
    tally_auth_nft: Token
    staking_vote_nft_policy: PolicyId
    staking_address: Address
    governance_token: Token
    vault_ft_policy: PolicyId


@dataclass
class TallyState(PlutusData):
    """
    Tracks the tally of a proposal
    """

    CONSTR_ID = 0
    votes: List[int]
    params: ProposalParams


def list_index(listy: List[int], key: int) -> int:
    """
    Get the index of the first occurence of key in listy
    """
    index = 0
    for el in listy:
        if el == key:
            return index
        index += 1
    assert False, f"Key {key} not in list {listy}"
    return -1


@dataclass
class TallyResult(PlutusData):
    CONSTR_ID = 4
    winning_proposal: Anything
    proposal_id: ProposalId


def winning_tally_result(
    tally_input_index: int,
    auth_nft: Token,
    tx_info: TxInfo,
    last_applied_proposal_id: ProposalId,
    enforce_vote_ended: bool,
) -> TallyResult:
    """
    This ensures that the index points to a winning proposal
    """
    tally_input = tx_info.reference_inputs[tally_input_index].resolved
    tally_state: TallyState = resolve_datum_unsafe(tally_input, tx_info)
    assert proposal_id_later_than(
        tally_state.params.proposal_id, last_applied_proposal_id
    ), "Proposal ID not after last proposal ID"
    assert token_present_in_output(auth_nft, tally_input), "AuthNFT missing from input"
    assert not enforce_vote_ended or after_ext(
        tx_info.valid_range, tally_state.params.end_time
    ), "Tally has not ended yet"
    total_votes = sum(tally_state.votes)
    assert total_votes >= tally_state.params.quorum, "Quorum not reached"
    winning_proposal_votes = max(tally_state.votes)
    assert ge_fraction(
        Fraction(winning_proposal_votes, total_votes),
        tally_state.params.winning_threshold,
    ), "Winning threshold not reached"
    winning_proposal_index = list_index(tally_state.votes, winning_proposal_votes)
    return TallyResult(
        tally_state.params.proposals[winning_proposal_index],
        tally_state.params.proposal_id,
    )
