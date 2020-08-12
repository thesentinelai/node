
contractABI= [
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "_coordinatorAddress",
          "type": "address"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "constructor"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "address",
          "name": "_user",
          "type": "address"
        },
        {
          "indexed": False,
          "internalType": "string",
          "name": "_fileHash",
          "type": "string"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "_time",
          "type": "uint256"
        }
      ],
      "name": "fileAdded",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "uint256",
          "name": "taskID",
          "type": "uint256"
        },
        {
          "indexed": False,
          "internalType": "string",
          "name": "_modelHash",
          "type": "string"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "_time",
          "type": "uint256"
        }
      ],
      "name": "modelUpdated",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "uint256",
          "name": "taskID",
          "type": "uint256"
        },
        {
          "indexed": True,
          "internalType": "address",
          "name": "_user",
          "type": "address"
        },
        {
          "indexed": False,
          "internalType": "string",
          "name": "_modelHash",
          "type": "string"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "_amt",
          "type": "uint256"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "_time",
          "type": "uint256"
        }
      ],
      "name": "newTaskCreated",
      "type": "event"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "name": "SentinelTasks",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "taskID",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "currentRound",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "totalRounds",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "cost",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "name": "UserFiles",
      "outputs": [
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "name": "UserTaskIDs",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "_coordinatorAddress",
          "type": "address"
        }
      ],
      "name": "updateCoordinator",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "_modelHash",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "_rounds",
          "type": "uint256"
        }
      ],
      "name": "createTask",
      "outputs": [],
      "stateMutability": "payable",
      "type": "function",
      "payable": True
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "_taskID",
          "type": "uint256"
        },
        {
          "internalType": "string",
          "name": "_modelHash",
          "type": "string"
        },
        {
          "internalType": "address payable",
          "name": "computer",
          "type": "address"
        }
      ],
      "name": "updateModelForTask",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "_taskID",
          "type": "uint256"
        }
      ],
      "name": "getTaskHashes",
      "outputs": [
        {
          "internalType": "string[]",
          "name": "",
          "type": "string[]"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    },
    {
      "inputs": [],
      "name": "getTaskCount",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    },
    {
      "inputs": [],
      "name": "getTasksOfUser",
      "outputs": [
        {
          "internalType": "uint256[]",
          "name": "",
          "type": "uint256[]"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "_fileHash",
          "type": "string"
        }
      ],
      "name": "storeFile",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "getFiles",
      "outputs": [
        {
          "internalType": "string[]",
          "name": "",
          "type": "string[]"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    }
  ]
contractAddress = "0x76e0bb0F8618c2c5Bc8F86C394D259fE53E38Eb9"
