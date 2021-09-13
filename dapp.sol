// version of solidity being used to compile
pragma solidity >=0.4.22 <0.6.0;

contract SecretBallot {
    /// State variables - stored permanently on blockchain
    struct Option {
        string description;
        uint voteCount;
    }
    struct Voter {
        uint weight;
        bool voted;
        uint8 vote;
        uint ballot;
    }
    // ballot contains the minimum number of participants before the vote can be revealed, the number of options, voters and people who have voted, the array of options and array of voters for that ballot
    struct Ballot {
        uint min_participants;
        uint num_options;
        uint num_voters;
        uint num_voted;
        mapping(uint => Option) options;
        mapping(address => Voter) voters;
    }
    
    // associating chairperson with address of contract creator
    address chairperson;
    
    // array of ballot structs
    Ballot[] public ballots;
    uint num_ballots = 0;

    // constructor - run when contract created
    constructor() payable public {
        chairperson = msg.sender;
    }
    

    // function for chairperson to create new ballot
    function createBallot(uint min_participants) public {
        require (msg.sender == chairperson, "Only chairperson can initiate vote");
        // initialising new Ballot and adding to array
        Ballot memory ballot;
        ballot.min_participants = min_participants;
        ballot.num_options = 0;
        ballot.num_voters = 1; //chairperson already registered to vote
        ballot.num_voted = 0;
        // adding new ballot to array
        ballots.push(ballot);
        // setting chairperson weight in ballot voters and incrementing number of ballots
        ballots[num_ballots].voters[chairperson].weight = 1;
        num_ballots +=1;
    }
    
    // function for the chairperson to add an option to a ballot
    function addOption(uint toBallot, string memory name) public {
        require (msg.sender == chairperson, "Only chairperson can add option");
        ballots[toBallot].options[ballots[toBallot].num_options].description = name;
        ballots[toBallot].options[ballots[toBallot].num_options].voteCount = 0;
        ballots[toBallot].num_options +=1;
    }
    
    // function to allow someone who pays to register to vote for their chosen ballot
    function registerToVote(uint toBallot) public payable {
        require(msg.value >= 1000000, "Must pay 1000000 wei to vote");
        Voter storage sender = ballots[toBallot].voters[msg.sender];
        // ensure voter not already registered for ballot
        require(sender.weight == 0, "Already registered for this ballot");
        sender.weight = 1;
        ballots[toBallot].num_voters +=1;
    }

    /// Give your vote for your chosen ballot
    function vote(uint toBallot, uint8 toOption) public returns (string memory description_) {
        Voter storage sender = ballots[toBallot].voters[msg.sender];
        // ensure voter has registered and not already voted on ballot
        require(sender.weight == 1, "Need to register before voting");
        if (sender.voted || toOption >= ballots[toBallot].num_options) return "Already voted";
        sender.voted = true;
        sender.vote = toOption;
        sender.ballot = toBallot;
        ballots[toBallot].options[toOption].voteCount += sender.weight;
        ballots[toBallot].num_voted +=1;
        description_ = ballots[toBallot].options[toOption].description;
    }
    
    // winning option for ballot viewable once min_participants have registered to vote and all voted
    function winningOption(uint toBallot) public view returns (string memory _winningOptionName) {
        require (ballots[toBallot].num_voters >= ballots[toBallot].min_participants, "Not enough participants to reveal winner");
        require (ballots[toBallot].num_voters == ballots[toBallot].num_voted, "Not everyone has voted");
        // circle through ballot options and find the one with the most votes
        uint256 winningVoteCount = 0;
        for (uint8 min_num = 0; min_num < ballots[toBallot].num_options; min_num++)
            if (ballots[toBallot].options[min_num].voteCount > winningVoteCount) {
                winningVoteCount = ballots[toBallot].options[min_num].voteCount;
                _winningOptionName = ballots[toBallot].options[min_num].description;
            }
        return _winningOptionName;
        
    }
    
    // enables voters to see options before voting
    function seeOptions(uint toBallot, uint toOption) public view returns (string memory name) {
        return ballots[toBallot].options[toOption].description;
    }

}