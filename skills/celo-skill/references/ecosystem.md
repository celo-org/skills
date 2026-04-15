# Celo Ecosystem Directory

> Sources: docs.celo.org, DefiLlama, celo.org/ecosystem
> For live TVL data, always refer to https://defillama.com/chain/Celo
> Last updated: 2026-04-15

---

## DeFi Protocols

### DEXes

| Protocol | Description | Website |
|----------|-------------|---------|
| Uniswap V3 | Concentrated liquidity AMM | https://app.uniswap.org |
| Uniswap V4 | Next-gen AMM with hooks (deployed Oct 2025) | https://app.uniswap.org |
| Velodrome V3 | Concentrated liquidity, ve-tokenomics | https://velodrome.finance |
| Curve | Efficient stablecoin trading | https://curve.finance |
| Ubeswap | Celo-native DEX (V2 + V3) | https://ubeswap.org |
| Carbon DeFi | Automated on-chain trading strategies (Bancor) | https://app.carbondefi.xyz |
| Mento V3 | Multi-currency FX infrastructure | https://app.mento.org |

### Lending & Borrowing

| Protocol | Description | Website |
|----------|-------------|---------|
| Aave V3 | Multi-asset lending, largest on Celo | https://aave.com |
| Morpho V1 | Permissionless isolated lending markets | https://app.morpho.org |
| Feather | Risk-adjusted permissionless lending | https://app.feather.zone |

> **For live TVL data**, query DefiLlama: `curl -s https://api.llama.fi/protocols | jq '[.[] | select(.chains[]? == "Celo")] | sort_by(-.tvl)'`
> See `live-data-sources.md` for more API examples.

### Yield & Liquidity Management

| Protocol | Description | Website |
|----------|-------------|---------|
| Beefy | Autocompounding yield farming | https://beefy.com |
| Steer Protocol | Automated liquidity management | https://app.steer.finance |
| ICHI | Algorithmic liquidity strategies | https://www.ichi.org |
| TheDeep | Cross-chain DeFi liquidity automation | https://app.thedeep.ink |
| Gamma | Active liquidity management | https://www.gamma.xyz |

### Stablecoins

| Protocol | Description | Website |
|----------|-------------|---------|
| Mento V2 | Celo-native stablecoin protocol (15+ currencies) | https://app.mento.org |
| Angle | Over-collateralized stablecoin protocol | https://app.angle.money |

### Liquid Staking

| Protocol | Description | Website |
|----------|-------------|---------|
| stCELO | Liquid staking for CELO | https://stcelo.xyz |

### Derivatives

| Protocol | Description | Website |
|----------|-------------|---------|
| Lynx | Perpetuals DEX with high leverage | https://app.lynx.finance |

### RWA (Real-World Assets)

| Protocol | Description | Website |
|----------|-------------|---------|
| Toucan Protocol | Carbon credit tokenization | https://toucan.earth |
| EthicHub | ReFi protocol for unbanked farmers | https://ethichub.com |
| Anemoy Capital | Institutional RWA | https://www.anemoy.io |
| Midas RWA | Tokenized real-world assets | https://midas.app |
| VNX | Tokenized commodities/forex | https://vnx.li |
| Untangled Vault | Capital allocation | https://untangled.finance |

### Payments & Streaming

| Protocol | Description | Website |
|----------|-------------|---------|
| Superfluid | Programmable cashflows, subscriptions, salaries | https://superfluid.org |

### Governance

| Protocol | Description | Website |
|----------|-------------|---------|
| Gardens | Community governance platform | https://app.gardens.fund |

### Other

| Protocol | Description | Website |
|----------|-------------|---------|
| PoolTogether V3 | No-loss prize games | https://pooltogether.com |

---

## Stablecoin Ecosystem

Celo is known as the "Home of Stablecoins" with 15+ Mento local-currency stablecoins.

### Mento Stablecoins (see contracts.md for addresses)

| Currency | Symbol | Region |
|----------|--------|--------|
| US Dollar | USDm (cUSD) | Global |
| Euro | EURm (cEUR) | Europe |
| Brazilian Real | BRLm (cREAL) | Brazil |
| West African CFA Franc | XOFm (eXOF) | West Africa |
| Kenyan Shilling | KESm | Kenya |
| Nigerian Naira | NGNm | Nigeria |
| Colombian Peso | COPm | Colombia |
| British Pound | GBPm | UK |
| Swiss Franc | CHFm | Switzerland |
| Japanese Yen | JPYm | Japan |
| Australian Dollar | AUDm | Australia |
| Canadian Dollar | CADm | Canada |
| Ghanaian Cedi | GHSm | Ghana |
| Philippine Peso | PHPm | Philippines |
| South African Rand | ZARm | South Africa |

### External Stablecoins

| Token | Symbol |
|-------|--------|
| USDC (Circle) | USDC |
| Tether USD | USDT |

---

## Infrastructure

### Oracles

| Provider | Docs |
|----------|------|
| Chainlink | https://docs.celo.org/tooling/oracles/chainlink-oracles |
| Band Protocol | https://docs.celo.org/tooling/oracles/band-protocol |
| RedStone | https://docs.celo.org/tooling/oracles/redstone |
| Supra | https://docs.celo.org/tooling/oracles/supra |
| Quex | https://docs.celo.org/tooling/oracles/quex-oracles |

### Data Indexers

| Provider | Docs |
|----------|------|
| The Graph | https://docs.celo.org/tooling/indexers/the-graph |
| Envio | https://docs.celo.org/tooling/indexers/envio |
| SubQuery | https://docs.celo.org/tooling/indexers/subquery |
| GoldRush (Covalent) | https://docs.celo.org/tooling/indexers/goldrush |
| Indexing Co | https://docs.celo.org/tooling/indexers/indexing-co |

### Bridges

| Bridge | URL | Type |
|--------|-----|------|
| Superbridge | https://superbridge.app/celo | Native L2 bridge |
| Wormhole (Portal) | https://portalbridge.com | Cross-chain |
| Axelar (Satellite) | https://satellite.money | Cross-chain |
| Chainlink CCIP (Transporter) | https://www.transporter.io | Cross-chain messaging |
| Squid Router | https://v2.app.squidrouter.com | Liquidity routing |
| Jumper Exchange | https://jumper.exchange | Cross-chain DEX |
| Hyperlane Nexus | https://www.usenexus.org | Cross-chain messaging |
| AllBridge | https://app.allbridge.io | Multi-chain |
| Layerswap | https://layerswap.io | EVM/non-EVM transfers |
| SmolRefuel | https://smolrefuel.com | Gas top-up |

Cross-chain messaging docs: https://docs.celo.org/tooling/bridges/cross-chain-messaging

### Wallets

| Wallet | Type | Platforms | URL |
|--------|------|-----------|-----|
| MiniPay | Non-custodial stablecoin | Android, iOS | https://www.opera.com/products/minipay |
| Valora | Non-custodial multichain | iOS, Android | https://valora.xyz |
| Celo Terminal | Desktop wallet + dApp hub | Mac, Linux, Windows | https://celoterminal.com |
| Safe Wallet | Multisig | Web | https://app.safe.global |
| MetaMask | Browser extension + mobile | All platforms | https://metamask.io |

Wallet infrastructure (WaaS): Privy, Alchemy Smart Wallets, Thirdweb, Reown, Portal, JAW, Dynamic

Wallet docs: https://docs.celo.org/tooling/wallets/index

### Block Explorers

| Explorer | URL |
|----------|-----|
| Celoscan | https://celoscan.io |
| Blockscout | https://celo.blockscout.com |

### Developer SDKs & Libraries

| Library | Docs |
|---------|------|
| Viem | https://docs.celo.org/tooling/libraries-sdks/viem/index |
| Ethers.js | https://docs.celo.org/tooling/libraries-sdks/ethers/index |
| Web3.js | https://docs.celo.org/tooling/libraries-sdks/web3/index |
| ContractKit | https://docs.celo.org/tooling/libraries-sdks/contractkit/index |
| Thirdweb SDK | https://docs.celo.org/tooling/libraries-sdks/thirdweb-sdk/index |
| Reown (WalletConnect) | https://docs.celo.org/tooling/libraries-sdks/reown/index |
| Composer Kit UI | https://docs.celo.org/tooling/libraries-sdks/composer-kit |
| Celo CLI | https://docs.celo.org/tooling/libraries-sdks/cli/index |

### Development Environments

| Tool | Docs |
|------|------|
| Foundry | https://docs.celo.org/tooling/dev-environments/foundry |
| Hardhat | https://docs.celo.org/tooling/dev-environments/hardhat |
| Remix | https://docs.celo.org/tooling/dev-environments/remix |
| Thirdweb | https://docs.celo.org/tooling/dev-environments/thirdweb/overview |

---

## MiniPay Ecosystem

MiniPay is Celo's flagship stablecoin wallet, built into Opera Mini and also available as a standalone app.

**Stats**: 14M+ wallets, 300M+ stablecoin transactions, 15M+ monthly Mini App opens, 60+ countries

### Known Mini Apps

| App | Category | Description |
|-----|----------|-------------|
| BitGifty | Bill Payments | Stablecoin-powered bill payments (450K+ active users, 10+ countries) |
| Bando | Vouchers & Bills | Local voucher and bill payment service |
| Topcasters | Prediction Gaming | USDT-powered prediction market game (2.2M+ predictions, 138K+ users) |
| Mdundo | Music Streaming | Africa's top music platform, subscriptions from $0.50 |
| Gamifly | Gamified Rewards | Trivia and challenge app with stablecoin rewards |
| Kiln Earn | DeFi Yield | Earn on USDT via Aave on Celo |
| Tether Gold (XAUt) | Gold Investment | Buy/hold tokenized gold |

### Building for MiniPay

- Quickstart: https://docs.celo.org/build-on-celo/build-on-minipay/quickstart
- Code Library: https://docs.celo.org/build-on-celo/build-on-minipay/code-library
- Deeplinks: https://docs.celo.org/build-on-celo/build-on-minipay/deeplinks
- Detection: Check `window.ethereum.isMiniPay` in browser

---

## AI & Agent Infrastructure

Celo is positioning itself for AI agent use cases:

- **ERC-8004 (Agent Trust Protocol)**: Identity, Reputation, and Validation registries for AI agents
  - Docs: https://docs.celo.org/build-on-celo/build-with-ai/8004
- **x402 Protocol**: HTTP-native micropayments using stablecoins
  - Docs: https://docs.celo.org/build-on-celo/build-with-ai/x402
- **Agent Skills**: Modular capabilities for AI coding agents
  - Docs: https://docs.celo.org/build-on-celo/build-with-ai/agent-skills
- **Celo MCP Server**: Model Context Protocol for blockchain data
  - Docs: https://docs.celo.org/build-on-celo/build-with-ai/mcp/celo-mcp
- **Vibe Coding**: AI-assisted development on Celo
  - Docs: https://docs.celo.org/build-on-celo/build-with-ai/vibe-coding

---

## Notable Ecosystem Projects (2025)

| Project | Category | Launch |
|---------|----------|--------|
| Aave V3 | Lending | March 2025 |
| Uniswap V4 | DEX | October 2025 |
| Self Protocol | ZK Identity (Aadhaar support) | 2025 |
| Nightfall L3 (EY) | Privacy/ZK Layer | 2025 |
| Prosperity Pass | Savings (2.5K accounts, $150K locked) | May 2025 |
