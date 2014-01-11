var yourName = prompt("What is your name?");
var chooseOne = prompt("rock, paper, scissors, lizard, Spock?");
var computerChoice = '';

function whowins (player1, player2,name1, name2) {
    var winner = '';
    if (player1 === player2) {
        console.log("The result is a tie.");
    } else {
        switch(player1){
            case 'rock':
                switch(player2) {
                    case 'paper':
                        console.log("Paper covers rock.");
                        winner = name2;
                        break;
                    case 'scissors':
                        console.log("Rock crushes scissors.");
                        winner = name1;
                        break;
                    case 'lizard':
                        console.log("Rock crushes lizard.");
                        winner = name1;
                        break;
                    case 'Spock':
                        console.log("Spock vaporizes rock.");
                        winner = name2;
                        break;
                }
            break;
            case 'paper':
                switch(player2) {
                    case 'rock':
                        console.log("Paper covers rock.");
                        winner = name1;
                        break;
                    case 'scissors':
                        console.log("Scissors cut paper.");
                        winner = name2;
                        break;
                    case 'lizard':
                        console.log("Lizard eats paper.");
                        winner = name2;
                        break;
                    case 'Spock':
                        console.log("Paper disproves Spock.");
                        winner = name1;
                        break;
                }
            break;
            case 'scissors':
                switch(player2) {
                    case 'rock':
                        console.log("Rock crushes scissors");
                        winner = name2;
                        break;
                    case 'paper':
                        console.log("Scissors cut paper.");
                        winner = name1;
                        break;
                    case 'lizard':
                        console.log("Scissors decapitate lizard.");
                        winner = name1;
                        break;
                    case 'Spock':
                        console.log("Spock smashes scissors.");
                        winner = name2;
                        break;
                }
            break;
            case 'lizard':
                switch(player2) {
                    case 'rock':
                        console.log("Rock crushes lizard.");
                        winner = name2;
                        break;
                    case 'paper':
                        console.log("Lizard eats paper.");
                        winner = name1;
                        break;
                    case 'scissors':
                        console.log("Scissors decapitate lizard.");
                        winner = name2;
                        break;
                    case 'Spock':
                        console.log("Lizard poisons Spock.");
                        winner = name1;
                        break;
                }
            break;
            case 'Spock':
                switch(player2) {
                    case 'rock':
                        console.log("Spock vaporizes rock.");
                        winner = name1;
                        break;
                    case 'paper':
                        console.log("Paper disproves Spock.");
                        winner = name2;
                        break;
                    case 'scissors':
                        console.log("Spock smashes scissors.");
                        winner = name1;
                        break;
                    case 'lizard':
                        console.log("Lizard poisons Spock.");
                        winner = name2;
                        break;
                }
            break;
        }
    }
    if (winner) {
        console.log("The winner is " + winner);
    }
}
                
                       
var validanswer = true;             

function commentonuserchoice(answer) {
    switch(answer) {
      case 'rock':
        console.log("You wish");
        break;
      case 'paper':
          console.log("I see where you are going with this.");
          break;
      case 'scissors':
          console.log("You are obsessed with sharp things.");
          break;
      case 'lizard':
          console.log("Very creative answer.");
          break;
      case 'Spock':
          console.log("I knew you would choose Spock.");
          break;
          default:
          console.log("It's not that difficult of a question.");
          validanswer = false;
    }}

function computerchooses() {
    var randomNum = Math.random();
    if (randomNum <= .20) {
        computerChoice = "rock";
    } else if (randomNum <= .40) {
        computerChoice = "scissors";
    } else if (randomNum <= .60) {
        computerChoice = "paper";
    } else if (randomNum <= .80) {
        computerChoice = "lizard";
    } else {
        computerChoice = "Spock";
    }
    console.log ("Computer chooses "+ computerChoice + ".");
}

commentonuserchoice(chooseOne);
computerchooses();
whowins(chooseOne,computerChoice,yourName,"The computer");
