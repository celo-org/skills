# Celo Copilot

The comprehensive skill for building on Celo. Ecosystem intelligence, developer tools, DeFi protocols, MiniPay integration, AI agent infrastructure, governance, grants, and verified contract addresses — all in one install.

## Install

```bash
npx skills add celo-org/copilot
```

Works with Claude Code, Codex, and OpenClaw.

## What it does

### Ecosystem Intelligence
Search 6,300+ crypto products via The Grid, find competitors, analyze vertical saturation, and discover what's deployed on Celo vs other EVM chains.

### Builder Assistant
Foundry/Hardhat configs for Celo, fee abstraction implementation, SDK selection guide (Viem, Wagmi, ContractKit, Thirdweb), deployment and verification workflows.

### DeFi Copilot
Deep protocol reference for Uniswap V3/V4, Aave V3, Morpho Blue, Mento stablecoins, stCELO, Velodrome, and Curve on Celo. Includes contract addresses, interaction patterns, and yield strategies.

### MiniPay App Builder
Build Mini Apps for MiniPay (11M+ wallets). Wallet detection, auto-connect patterns, stablecoin payments, phone number resolution, testing with ngrok, and ready-to-use code templates.

### AI Agent Builder
ERC-8004 (Agent Trust Protocol), x402 (HTTP micropayments), Celo MCP Server, and the Agent Skills specification. Build AI agents that transact autonomously on Celo.

### Governance
On-chain governance reference: proposal lifecycle, voting with Mondo/CeloCLI, Security Council, epoch rewards, and carbon offset fund.

### Contract Addresses
150+ verified addresses from docs.celo.org — core protocol, 15+ Mento stablecoins, L1 bridge contracts, Uniswap V3/V4, Aave V3, Morpho Blue, and testnet deployments.

### Grant Matchmaking
20+ grant programs tracked (3 live, 17 past) with a matchmaking guide. Find the right grant based on what you're building.

## Usage

Once installed, the skill activates automatically. Just describe what you need:

- *"What lending protocols exist on Celo?"*
- *"Set up a Foundry project for Celo with fee abstraction"*
- *"Give me the Uniswap V4 contract addresses on Celo mainnet"*
- *"I want to build a payments Mini App — show me how"*
- *"How do I integrate Aave V3 on Celo?"*
- *"What grants can I apply to for a DeFi project?"*
- *"How saturated is the DEX vertical on EVM chains?"*
- *"Build an AI agent that makes micropayments with x402"*

## Data Sources

| Source | What | Auth |
|--------|------|------|
| [The Grid](https://beta.node.thegrid.id/graphql) | 6,300+ crypto products, live ecosystem data | None (public) |
| [docs.celo.org](https://docs.celo.org) | Contract addresses, network info, documentation | None |
| [DefiLlama](https://defillama.com/chain/Celo) | TVL data (linked, not embedded) | None |
| [celo-org/agent-skills](https://github.com/celo-org/agent-skills) | SDK patterns, code examples | None |

## Structure

```
skills/celo-copilot/
  SKILL.md                          # Main skill definition (v1.0.0)
  references/
    # Phase 1: Ecosystem Intelligence
    network-info.md                 # Chain IDs, RPCs, explorers, fee currencies
    contracts.md                    # 150+ verified contract addresses
    ecosystem.md                    # 30+ DeFi protocols, infra, MiniPay apps
    the-grid-skill.md               # 9 GraphQL query templates for The Grid
    grants-funding.md               # 20+ grant programs (3 live, 17 past)
    docs-map.md                     # Full docs.celo.org sitemap (~150 pages)
    live-data-sources.md            # DefiLlama, celopg.eco, RPC, Blockscout APIs
    # Phase 2: Builder Assistant
    builder-guide.md                # Celo-specific dev patterns and gotchas
    dev-templates.md                # Foundry, Hardhat, Viem, Wagmi configs
    sdk-reference.md                # SDK quick reference and selection guide
    # Phase 3: DeFi Copilot
    defi-protocols.md               # Deep protocol reference (Uniswap, Aave, Morpho, Mento)
    # Phase 4: MiniPay App Builder
    minipay-guide.md                # Complete MiniPay development guide
    minipay-templates.md            # Ready-to-use Mini App code templates
    # Phase 5: Platform Features
    governance.md                   # On-chain governance reference
    ai-agents.md                    # ERC-8004, x402, MCP, Agent Skills
```

## Contributing

Data is sourced from official Celo documentation. If you find outdated information:

1. Check [docs.celo.org](https://docs.celo.org) for the current value
2. Update the relevant reference file
3. Bump the version in `SKILL.md`
4. Open a PR

## License

Apache-2.0
