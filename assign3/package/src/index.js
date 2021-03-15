import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

function Square(props) {
  return (
    <button className="square" onClick={props.onClick}>
      {props.value}
    </button>
  );
}

class Board extends React.Component {
  renderSquare(i) {
    return (
      <Square
        value={this.props.squares[i]}
        onClick={() => this.props.onClick(i)}
      />
    );
  }

  render() {
    return (
      <div>
        <div className="board-row">
          {this.renderSquare(0)}
          {this.renderSquare(1)}
          {this.renderSquare(2)}
        </div>
        <div className="board-row">
          {this.renderSquare(3)}
          {this.renderSquare(4)}
          {this.renderSquare(5)}
        </div>
        <div className="board-row">
          {this.renderSquare(6)}
          {this.renderSquare(7)}
          {this.renderSquare(8)}
        </div>
      </div>
    );
  }
}

class Game extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      history: [
        {
          squares: Array(9).fill(null)
        }
      ],
      stepNumber: 0,
      xIsNext: true,
      previousSpot: 0,
      mustWin: false
    };
  }

  handleClick(i) {
    const history = this.state.history.slice(0, this.state.stepNumber + 1);
    const current = history[history.length - 1];
    const squares = current.squares.slice();
    const xCount = countArray(squares, 'X'); 
    const oCount = countArray(squares, 'O'); 
    if (calculateWinner(squares) 
    	|| (squares[i] === null && xCount === 3 && oCount === 3)
    	|| (squares[i] === 'X' && xCount === 3 
    		&& oCount === 3 && this.state.xIsNext === false)
    	|| (squares[i] === 'O' && xCount === 3 
    		&& oCount === 3 && this.state.xIsNext === true)
    	|| (squares[i] && oCount < 3)
    	){
      return;
    }

    
    //if all pieces are on the board, chose one to move
    if(xCount === 3 && oCount === 3)
    {
    	var winNextMove = false; 
    	//if peice is in the center, vacate it!
    	if(this.state.xIsNext && squares[4] === 'X' && i !== 4)  
    	{
    		if(winNextStep(squares, i, 'X') === true)
    		{
    			winNextMove = true; 
    		}
    		else
    		{
    			return; 
    		}	
    		
    	}
    	if(!this.state.xIsNext && squares[4] === 'O' && i !== 4)
    	{
 			if(winNextStep(squares, i, 'O') === true)
    		{
    			winNextMove = true; 
    		}
    		else
    		{
    			return; 
    		}
    	}
    	if(noMove(squares, i) === false)
    	{
    		return; 
    	}
    	
    	squares[i] = null;  
    	this.setState({
          history: history.concat([
          {
              squares: squares
          }
      	]),
      	stepNumber: history.length,
      	xIsNext: this.state.xIsNext,
      	previousSpot: i, 
      	mustWin: winNextMove
      	});
    }
    else
    {
    	//check to make sure player is moving to a valid position if there
    	//are 5 pieces on the board and stepNumber > 5 
    	if(squares[i] !== null || (this.state.stepNumber > 6 && (isValid(this.state.previousSpot, i) === false)))
    	{
    		return; 
    	}

    	squares[i] = this.state.xIsNext ? "X" : "O";
    	if(this.state.mustWin === true)
    	{
    		if(win(squares) === false)
    		{
    			squares[i] = null; 
    			return; 
    		}
    		
    	}

        this.setState({
          history: history.concat([
          {
              squares: squares
          }
      ]),
      stepNumber: history.length,
      xIsNext: !this.state.xIsNext,
      previousSpot: i, 
      mustWin: false
      });
  }
}	

  jumpTo(step) {
    this.setState({
      stepNumber: step,
      xIsNext: (step % 2) === 0
    });
  }

  render() {
    const history = this.state.history;
    const current = history[this.state.stepNumber];
    const winner = calculateWinner(current.squares);

    const moves = history.map((step, move) => {
      const desc = move ?
        'Go to move #' + move :
        'Go to game start';
      return (
        <li key={move}>
          <button onClick={() => this.jumpTo(move)}>{desc}</button>
        </li>
      );
    });

    let status;
    if (winner) {
      status = "Winner: " + winner;
    } else {
      status = "Next player: " + (this.state.xIsNext ? "X" : "O");
    }

    return (
      <div className="game">
        <div className="game-board">
          <Board
            squares={current.squares}
            onClick={i => this.handleClick(i)}
          />
        </div>
        <div className="game-info">
          <div>{status}</div>
          <ol>{moves}</ol>
        </div>
      </div>
    );
  }
}

// ========================================

ReactDOM.render(<Game />, document.getElementById("root"));

function calculateWinner(squares) {
  const lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
  ];
  for (let i = 0; i < lines.length; i++) {
    const [a, b, c] = lines[i];
    if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
      return squares[a];
    }
  }
  return null;
}

function winNextStep(squares, index, player)
{
	var board = squares; 
	board[index] = null; 
	
	for(let i = 0; i < 9; i++)
	{
		if (board[i] === null && isValid(index, i))
		{
			var play = board; 
			play[i] = player; 
			if(win(play))
			{
				play[i] = null; 
				return true; 
			}
			play[i] = null; 
		}
	}
	return false; 
}

function win(squares)
{
	const lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
  ];
  for (let i = 0; i < lines.length; i++) {
    const [a, b, c] = lines[i];
    if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
      return true;
    }
  }
  return false;
}

function noMove(squares, index)
{
	const valid_moves = {
		0 : [1, 3, 4, -1, -1, -1, -1, -1], 
		1 : [0, 2, 3, 4, 5, -1, -1, -1], 
		2 : [1, 4, 5, -1, -1, -1, -1, -1], 
		3 : [0, 1, 4, 6, 7, -1, -1, -1], 
		4 : [0, 1, 2, 3, 5, 6, 7, 8], 
		5 : [1, 2, 4, 7, 8, -1, -1, -1], 
		6 : [3, 4, 7, -1, -1, -1, -1, -1], 
		7 : [3, 4, 5, 6, 8, -1, -1, -1], 
		8 : [4, 5, 7, -1, -1, -1, -1, -1]
	}; 

	var val = valid_moves[index]; 
	
	for(var i = 0; i < 8; i++)
	{
		if(val[i] === -1) 
			return false; 
		if(squares[val[i]] === null)
			return true; 
	}
	return false; 
}

function isValid(prevIndex, index)
{
	//0 1 2
	//3 4 5
	//6 7 8
	const valid_moves = {
		0 : [1, 3, 4, -1, -1, -1, -1, -1], 
		1 : [0, 2, 3, 4, 5, -1, -1, -1], 
		2 : [1, 4, 5, -1, -1, -1, -1, -1], 
		3 : [0, 1, 4, 6, 7, -1, -1, -1], 
		4 : [0, 1, 2, 3, 5, 6, 7, 8], 
		5 : [1, 2, 4, 7, 8, -1, -1, -1], 
		6 : [3, 4, 7, -1, -1, -1, -1, -1], 
		7 : [3, 4, 5, 6, 8, -1, -1, -1], 
		8 : [4, 5, 7, -1, -1, -1, -1, -1]
	}; 

	var valid_spots = valid_moves[prevIndex]; 
	for(var i = 0; i < 8; i++)
	{
		if(valid_spots[i] === index)
			return true; 
	}
	return false; 
}

function countArray(squares, what)
{
	var count = 0;
    for (var i = 0; i < 9; i++) {
        if (squares[i] === what) {
            count++;
        }
    }
    return count;
}
