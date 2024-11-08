# Autonomous Blockchain-Agents

This repository contains an autonomous agent system built in Python. The agents are designed to communicate and handle tasks like message processing and token transfers. The project structure supports scalability and includes modules for agent behaviors, message handling, utilities, and background processing for non-blocking operations.

## Prerequisites

1. **Python 3**: Ensure Python 3 is installed.
2. **Poetry**: Poetry is used to manage dependencies. Install it with:

   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. **Redis**: Ensure Redis is installed and running, as it’s required for managing background tasks with Redis Queue (RQ).

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Mohsinsiddi/ai-agent.git
   cd ai-agent
   ```

2. **Install Dependencies**:
   Use Poetry to install all dependencies:

   ```bash
   poetry install
   ```

3. **Activate Virtual Environment**:
   Enter Poetry's virtual environment:

   ```bash
   poetry shell
   ```

4. **Environment Setup**:

   - Copy the `.env.example` file to create a `.env` file:
     ```bash
     cp .env.example .env
     ```
   - Populate the `.env` file with required values for main operations and testing.

     ### Required Environment Variables for Main Operations:

     - `WEB3_PROVIDER_URL`: URL of the Web3 provider (e.g., Infura).
     - `TOKEN_ADDRESS`: ERC20 token address for balance checks and transfers.
     - `WALLET1_ADDRESS`: Source wallet 1 address for token transfers.
     - `WALLET2_ADDRESS`: Source wallet 2 address for token transfers.
     - `TARGET_ADDRESS`: Target wallet address for token transfers.
     - `PRIVATE_KEY1`: Private key of wallet 1 for agent1 (**never commit this to version control**).
     - `PRIVATE_KEY2`: Private key of wallet 2 for agent2 (**never commit this to version control**).
     - `REDIS_URL`: URL for Redis server, used for background task management.

     ### Required Environment Variables for Testing:

     Before running tests, set the following additional environment variables in `.env` to provide necessary values for the test suite:

     - `TEST_TOKEN_ADDRESS`: Token address used for testing purposes.
     - `TEST_WALLET1_ADDRESS`: Wallet 1 address used in test scenarios.
     - `TEST_WALLET2_ADDRESS`: Wallet 2 address used in test scenarios.
     - `TEST_TARGET_ADDRESS`: Target wallet address used in test transfers.
     - `TEST_PRIVATE_KEY`: Private key for testing transactions (**never commit this to version control**).
     - `RPC_URL`: RPC URL for testing on the blockchain network.

   - **Note**: Ensure `.env` is listed in `.gitignore` to keep sensitive information secure.

To update your README with an explanation of why you chose Tenderly’s Virtual Testnet over the general virtual testnet, and include details on using Sepolia Testnet for smoother transactions, you could add a new section under **Network and Deployment Details**. Here's how you could format it:

---

## Network and Deployment Details

This project interacts with the blockchain via the **Sepolia Testnet**, where we deployed a custom token contract and ensured a funded source wallet. While exploring test environments, we initially considered using a **Virtual Testnet** with Tenderly. However, due to a block limit of 50 for trial sessions on the Virtual Testnet, we would need to reset frequently and redeploy our token contract each time, leading to inefficiencies in testing. This constraint prompted us to choose the Sepolia Testnet to avoid repetitive redeployment and to simulate real-time delays during transaction processing.

**Note**: The Tenderly Virtual Testnet remains an option for faster transactions if configured with its RPC URL. When switching to this environment, deploy the token contract on the Virtual Testnet and adjust the values in `.env` accordingly, including the funded wallets and private keys.

> _See the attached image for the block limit trial notice on the Virtual Testnet._

<img width="1492" alt="Screenshot 2024-11-05 at 8 42 52 PM" src="https://github.com/user-attachments/assets/0117e04a-1cf3-4f27-bd43-89c4fdd813b1">

## Running the Project

Two primary commands are needed to run the system:

1. **Transfer Processor**: Start the background task processor that handles crypto transfers asynchronously to avoid blocking agents.

   ```bash
   poetry run transfer-processor
   ```

2. **Agent System**: Start the autonomous agents.
   ```bash
   poetry run agent-system
   ```

**Suggested CLI Workflow**:
To run both commands concurrently, open two separate terminals and execute each command in a separate terminal. Alternatively, you can use a command multiplexer (like `tmux` or `screen`) to run both commands within the same terminal session.

<img width="1175" alt="Screenshot 2024-11-06 at 6 50 55 PM" src="https://github.com/user-attachments/assets/abfab27e-dbf7-4ffa-ad11-20b7857f6a4a">

## Running Tests

Before running the test suite, ensure the test environment variables are set in the `.env` file as described above.

- **Basic Test**: Run all tests with:
  ```bash
  poetry run pytest tests/test_autonomous_agents.py -v
  ```
- **With CLI Logs**: For detailed CLI logs, use:
  ```bash
  poetry run pytest tests/test_autonomous_agents.py -v --log-cli-level=DEBUG
  ```

## Code Overview

### Folder Structure

- **core/**: Core functionality, including agent setup, message handling, and utilities.
- **handlers/**: Message handlers for processing messages such as text and transaction requests.
- **behaviors/**: Agent behaviors, including balance checks and random message generation.
- **utils/**: Utility functions and configurations, such as logging setup.
- **tasks/**: Background tasks for processing crypto transfers, using Redis Queue (RQ) to handle asynchronous transfers.

### Key Components

- **Handlers**:

  - `MessageHandler`: Base class for message handling.
  - `HelloMessageHandler`: Processes “hello” messages and logs the receipt.
  - `CryptoTransferHandler`: Manages token transfers between wallets with error handling.

- **Behaviors**:
  - `RandomMessageBehavior`: Periodically generates random messages for agent interaction.
  - `TokenBalanceCheckBehavior`: Checks token balances at intervals with logging.

### Background Processing with Redis Queue (RQ)

This project uses Redis and RQ to handle token transfer operations in the background, ensuring the agents are non-blocking. Redis tasks are processed separately by running the `transfer-processor` script, which manages background transfers.

### Logging

- Uses **colorlog** for color-coded logs. Logs are structured with levels and timestamps for easy debugging.

### Error Handling

- Robust error handling is integrated into both handlers and behaviors, especially for Web3 transactions and balance checks.
  <img width="1190" alt="Screenshot 2024-11-06 at 6 53 41 PM" src="https://github.com/user-attachments/assets/b2f19d82-091d-436f-a129-15af2e7a38ed">

## Dependencies

This project relies on the following packages:

- **web3**: For Ethereum blockchain interaction.
- **eth-typing** and **eth-account**: For Ethereum-specific type definitions and account handling.
- **colorlog**: For enhanced log visibility.
- **python-dotenv**: Loads environment variables from `.env` files.
- **redis** and **rq**: For Redis Queue-based background task processing.

### Development Dependencies

For testing and development, the following packages are included:

- **pytest**: Framework for running tests.
- **pytest-asyncio**: Adds asyncio support to pytest.
- **pytest-mock**: Provides mock functionality for testing.
