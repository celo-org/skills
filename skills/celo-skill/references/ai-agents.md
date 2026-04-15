# AI Agent Infrastructure on Celo

> Sources: docs.celo.org/build-on-celo/build-with-ai/*, celo-org/agent-skills

Celo is positioning itself as the payments and trust layer for AI agents — sub-cent fees, 1-second finality, native stablecoins, and purpose-built protocols for agent identity, reputation, and payments.

---

## ERC-8004: Agent Trust Protocol

A trust framework for AI agents with three on-chain registries: Identity, Reputation, and Validation.

**Reference**: https://eips.ethereum.org/EIPS/eip-8004 | https://www.8004.org

### Contract Deployments

| Registry | Celo Mainnet | Celo Sepolia |
|----------|-------------|--------------|
| Identity | `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` | `0x8004A818BFB912233c491871b3d84c89A494BD9e` |
| Reputation | `0x8004BAa17C55a88189AE136b182e5fdA19dE9b63` | `0x8004B663056A597Dffe9eCcC1965A193B7388713` |

**SDK**: `npm install @chaoschain/sdk` / `pip install chaoschain-sdk`

### Protocol Stack

```
Application Layer (your agent)
    ↓
Trust Layer (ERC-8004: identity + reputation + validation)
    ↓
Payment Layer (x402: HTTP-native micropayments)
    ↓
Communication Layer (A2A protocol, MCP)
```

### Identity Registry

Agents register as ERC-721 NFTs with metadata URI. Each agent gets a unique `agentId` (token ID).

**Key functions:**

| Function | Description |
|----------|-------------|
| `register()` | Register agent, returns agentId |
| `register(string agentURI)` | Register with metadata URI |
| `register(string agentURI, MetadataTuple[])` | Register with URI + metadata |
| `setAgentURI(uint256 agentId, string uri)` | Update metadata URI |
| `setMetadata(uint256 agentId, MetadataTuple[])` | Set key-value metadata |
| `getMetadata(uint256 agentId, string key)` | Read metadata value |
| `getAgentWallet(uint256 agentId)` | Get agent's payment wallet |
| `setAgentWallet(uint256 agentId, address wallet, uint256 deadline, bytes sig)` | Set payment wallet (requires signature) |
| `isAuthorizedOrOwner(uint256 agentId, address addr)` | Check authorization |
| `tokenURI(uint256 agentId)` | Get full metadata URI |
| `ownerOf(uint256 agentId)` | Get agent owner |

**Agent metadata format:**

```json
{
  "type": "Agent",
  "name": "MyAgent",
  "description": "An AI agent that...",
  "image": "ipfs://...",
  "endpoints": [
    { "type": "a2a", "url": "https://example.com/.well-known/agent.json" },
    { "type": "mcp", "url": "https://example.com/mcp" },
    { "type": "wallet", "address": "0x...", "chainId": 42220 }
  ],
  "supportedTrust": ["reputation", "validation", "tee"]
}
```

### Reputation Registry

On-chain feedback system. Any address can give feedback to any registered agent (self-feedback blocked).

**Key functions:**

| Function | Description |
|----------|-------------|
| `giveFeedback(uint256 agentId, int128 value, uint8 valueDecimals, bytes32 tag1, bytes32 tag2, string endpoint, string feedbackURI, bytes32 feedbackHash)` | Submit feedback |
| `revokeFeedback(uint256 agentId, uint256 feedbackIndex)` | Revoke previous feedback |
| `readFeedback(uint256 agentId, address client, uint256 index)` | Read specific feedback |
| `readAllFeedback(uint256 agentId, address[] clients)` | Read all feedback from clients |
| `getSummary(uint256 agentId, address[] clientAddresses)` | Get aggregated summary (count, sum, decimals) |
| `appendResponse(uint256 agentId, address client, uint256 feedbackIndex, string responseURI)` | Agent responds to feedback |
| `getClients(uint256 agentId)` | Get all clients who gave feedback |

**Standard feedback tags:** `starred` (0-100), `uptime` (%), `successRate` (%), `responseTime` (ms), `reachable` (boolean).

### Registration Example

```typescript
import { createWalletClient, custom } from "viem";
import { celo } from "viem/chains";

const IDENTITY_REGISTRY = "0x8004A169FB4a3325136EB29fA0ceB6D2e539a432";

const client = createWalletClient({
  chain: celo,
  transport: custom(window.ethereum),
});

// Register agent with metadata URI
const txHash = await client.writeContract({
  address: IDENTITY_REGISTRY,
  abi: identityRegistryABI,
  functionName: "register",
  args: ["ipfs://QmYourAgentMetadata"],
});
```

---

## x402: HTTP-Native Micropayments

Protocol enabling pay-per-request APIs using HTTP 402 status code and stablecoin payments.

**Reference**: https://www.x402.org | https://github.com/coinbase/x402

### How It Works

1. Client sends request to protected endpoint
2. Server returns `402 Payment Required` with payment requirements
3. Client signs a stablecoin payment
4. Client retries with `X-PAYMENT` header containing signed payment
5. Server verifies payment via facilitator
6. Server settles on-chain and delivers response

### Supported Tokens on Celo

| Token | Address | Decimals |
|-------|---------|----------|
| USDC | `0xcebA9300f2b948710d2653dD7B07f33A8B32118C` | 6 |
| USDT | `0x48065fbBE25f71C9282ddf5e1cD6D6A887483D5e` | 6 |
| USDm | `0x765DE816845861e75A25fCA122bb6898B8B1282a` | 18 |

### Server Implementation (Next.js)

```typescript
import { settlePayment, facilitator } from "thirdweb/x402";

export async function POST(req: Request) {
  const paymentHeader =
    req.headers.get("payment-signature") || req.headers.get("x-payment");

  if (!paymentHeader) {
    return new Response(JSON.stringify({
      error: "Payment Required",
      scheme: "fixed",
      price: "100000",        // 0.10 USDC (6 decimals)
      // x402 `currency` = the ERC-20 being charged (USDC token address). NOT the `feeCurrency`
      // adapter. Gas for the on-chain settlement is separate — if the settler pays gas in USDC,
      // it must use the USDC adapter (0x2F25deB3848C207fc8E0c34035B3Ba7fC157602B) in `feeCurrency`.
      currency: "0xcebA9300f2b948710d2653dD7B07f33A8B32118C",
      chainId: 42220,
    }), { status: 402 });
  }

  const result = await settlePayment({
    paymentHeader,
    facilitator,
    secretKey: process.env.THIRDWEB_SECRET_KEY!,
  });

  if (!result.success) {
    return new Response("Payment failed", { status: 402 });
  }

  // Deliver the resource
  return new Response(JSON.stringify({ data: "your content here" }));
}
```

### Client Implementation (React)

```typescript
import { useFetchWithPayment } from "thirdweb/react";

function MyComponent() {
  const fetchWithPayment = useFetchWithPayment();

  async function callPaidAPI() {
    const response = await fetchWithPayment("/api/paid-endpoint", {
      method: "POST",
      body: JSON.stringify({ query: "hello" }),
    });
    const data = await response.json();
  }
}
```

### Client Implementation (TypeScript)

```typescript
import { wrapFetchWithPayment } from "thirdweb/x402";
import { privateKeyToAccount } from "thirdweb/wallets";

const account = privateKeyToAccount(process.env.PRIVATE_KEY!);
const fetchWithPayment = wrapFetchWithPayment(fetch, account);

const response = await fetchWithPayment("https://api.example.com/data");
```

### Why Celo for x402

| Metric | Traditional | x402 on Celo |
|--------|-------------|-------------|
| Setup | Days | Minutes |
| Settlement | 2-7 days | ~1 second |
| Fees | 2-3% + $0.30 | ~$0.001 |
| Minimum | $0.50+ | $0.001 |

---

## Celo MCP Server

Model Context Protocol server for querying Celo blockchain data from AI coding assistants.

**Repo**: https://github.com/celo-org/celo-mcp

### Install

```bash
pip install celo-mcp
# or
pipx install celo-mcp
```

### IDE Configuration

**Claude Desktop / Cursor / VS Code:**

```json
{
  "mcpServers": {
    "celo-mcp": {
      "command": "uvx",
      "args": ["--refresh", "celo-mcp"]
    }
  }
}
```

**Environment variables:**
- `CELO_RPC_URL` — default: `https://forno.celo.org`
- `CELO_TESTNET_RPC_URL` — default: `https://forno.celo-sepolia.celo-testnet.org/`

### Available Tools

| Tool | Description |
|------|-------------|
| `get_network_status` | Current block, gas price, chain info |
| `get_block` | Block details by number |
| `get_latest_blocks` | Recent blocks |
| `get_account` | Account balance and nonce |
| `get_transaction` | Transaction details by hash |
| `get_token_info` | ERC-20 token metadata |
| `get_token_balance` | ERC-20 balance for address |
| `get_celo_balances` | CELO + stablecoin balances |
| `get_nft_info` | ERC-721/1155 metadata |
| `get_nft_balance` | NFT balance for address |
| `call_contract_function` | Read contract state |
| `estimate_contract_gas` | Estimate gas for contract call |
| `estimate_transaction` | Estimate gas for transaction |
| `get_gas_fee_data` | Current gas fee data |
| `get_governance_proposals` | List governance proposals |
| `get_proposal_details` | Proposal details by ID |

Supports: ERC-20, ERC-721, ERC-1155, Mento stablecoins, governance proposals.

---

## Agent Skills Specification

Celo's modular skill system for AI coding assistants.

### Install

```bash
# All skills
npx skills add celo-org/agent-skills -g

# Specific skill
npx skills add celo-org/agent-skills --skill evm-hardhat -g
```

### Skill Structure

```
skill-name/
├── SKILL.md           # Main instructions (required, <5000 tokens)
├── references/        # Detailed documentation (loaded on-demand)
├── rules/             # Best practices and standards
└── scripts/           # Executable scripts
```

### Progressive Disclosure

1. **Level 1 — Metadata** (~100 tokens): Name + description for activation detection
2. **Level 2 — SKILL.md** (<5000 tokens): Loaded when skill triggers
3. **Level 3 — References**: Loaded on-demand as needed

Skills activate automatically based on project context (e.g., `hardhat.config.ts` triggers `evm-hardhat`).

---

## AI Agent Use Cases on Celo

Key opportunities for AI agents on Celo:

- **Onchain FX Trading**: Arbitrage bots across Mento stablecoin pairs, LP management on Uniswap, Merkl rewards optimization
- **Prediction Markets**: Automated market making and trading
- **Automated Savings/DCA**: Dollar-cost averaging into CELO or stablecoins
- **Data Collection Payments**: x402 micropayments for data (82.7% data gap outside NA/Europe)
- **Retroactive Funding Optimization**: Track Proof-of-Ship metrics via Karma dashboard
- **Payment Agents**: Autonomous bill payment, remittance, payroll

**Resources:**
- Agent ideas: https://github.com/celo-org/ai-agent-ideas
- Uniswap pools: https://app.uniswap.org/explore/pools/celo
- Merkl rewards: https://merkl.angle.money/?chain=42220
