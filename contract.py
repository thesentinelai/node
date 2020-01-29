
contractABI= [
	{
		"constant": False,
		"inputs": [
			{
				"name": "_modelHash",
				"type": "string"
			},
			{
				"name": "_rounds",
				"type": "uint256"
			}
		],
		"name": "createTask",
		"outputs": [],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": False,
		"inputs": [
			{
				"name": "_taskID",
				"type": "uint256"
			},
			{
				"name": "_modelHash",
				"type": "string"
			}
		],
		"name": "updateModelForTask",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"name": "taskID",
				"type": "uint256"
			},
			{
				"indexed": True,
				"name": "_user",
				"type": "address"
			},
			{
				"indexed": False,
				"name": "_amt",
				"type": "uint256"
			},
			{
				"indexed": False,
				"name": "_time",
				"type": "uint256"
			}
		],
		"name": "newTaskCreated",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"name": "taskID",
				"type": "uint256"
			},
			{
				"indexed": False,
				"name": "_modelHash",
				"type": "string"
			},
			{
				"indexed": False,
				"name": "_time",
				"type": "uint256"
			}
		],
		"name": "modelUpdated",
		"type": "event"
	},
	{
		"constant": True,
		"inputs": [],
		"name": "getTaskCount",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"name": "_taskID",
				"type": "uint256"
			}
		],
		"name": "getTaskHashes",
		"outputs": [
			{
				"name": "",
				"type": "string[]"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [],
		"name": "getTasksOfUser",
		"outputs": [
			{
				"name": "",
				"type": "uint256[]"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"name": "SentinelTasks",
		"outputs": [
			{
				"name": "taskID",
				"type": "uint256"
			},
			{
				"name": "currentRound",
				"type": "uint256"
			},
			{
				"name": "totalRounds",
				"type": "uint256"
			},
			{
				"name": "cost",
				"type": "uint256"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"name": "",
				"type": "address"
			},
			{
				"name": "",
				"type": "uint256"
			}
		],
		"name": "UserTaskIDs",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	}
];
contractAddress = "0xdFF74cBcD63811C050A6a2545E62bF7960C55671";
