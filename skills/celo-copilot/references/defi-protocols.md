# DeFi Protocol Reference for Celo

> Sources: docs.celo.org, protocol documentation
> **For live TVL data**, always query DefiLlama API — see `live-data-sources.md`
> Do NOT rely on hardcoded TVL numbers in this file — they go stale quickly.

---

## Uniswap (V3 + V4)

The primary DEX on Celo. Both V3 and V4 are deployed.

### V4 Contracts (Mainnet)

| Contract | Address |
|----------|---------|
| PoolManager | `0x288dc841A52FCA2707c6947B3A777c5E56cd87BC` |
| PositionManager | `0xf7965f3981e4d5bc383bfbcb61501763e9068ca9` |
| UniversalRouter | `0xcb695bc5d3aa22cad1e6df07801b061a05a0233a` |
| V4Quoter | `0x28566da1093609182dff2cb2a91cfd72e61d66cd` |
| StateView | `0xbc21f8720babf4b20d195ee5c6e99c52b76f2bfb` |
| Permit2 | `0x000000000022D473030F116dDEE9F6B43aC78BA3` |

### V3 Contracts (Mainnet)

| Contract | Address |
|----------|---------|
| UniswapV3Factory | `0xAfE208a311B21f13EF87E33A90049fC17A7acDEc` |
| SwapRouter02 | `0x5615CDAb10dc425a742d643d949a7F474C01abc4` |
| NonfungiblePositionManager | `0x3d79EdAaBC0EaB6F08ED885C05Fc0B014290D95A` |
| QuoterV2 | `0x82825d0554fA07f7FC52Ab63c961F330fdEFa8E8` |
| UniversalRouter | `0x643770E279d5D0733F21d6DC03A8efbABf3255B4` |

### Swap Example (Viem + UniversalRouter)

```typescript
import { createPublicClient, http, encodeFunctionData, parseUnits } from "viem";
import { celo } from "viem/chains";

// Quote a swap: CELO → USDm
const quoterAddress = "0x82825d0554fA07f7FC52Ab63c961F330fdEFa8E8";
const CELO = "0x471EcE3750Da237f93B8E339c536989b8978a438";
const USDM = "0x765DE816845861e75A25fCA122bb6898B8B1282a";

// Use QuoterV2 to get expected output
const quote = await publicClient.readContract({
  address: quoterAddress,
  abi: quoterV2Abi,
  functionName: "quoteExactInputSingle",
  args: [{
    tokenIn: CELO,
    tokenOut: USDM,
    fee: 3000, // 0.3% fee tier
    amountIn: parseUnits("1", 18),
    sqrtPriceLimitX96: 0n,
  }],
});
```

### Key Pools

Explore pools at: https://app.uniswap.org/explore/pools/celo

Common fee tiers: `100` (0.01%), `500` (0.05%), `3000` (0.3%), `10000` (1%)

### Merkl Rewards

Some Uniswap pools on Celo have Merkl incentives: https://merkl.angle.money/?chain=42220

---

## Aave V3

Multi-asset lending/borrowing protocol. Deployed on Celo March 2025.

### Contracts (Mainnet)

| Contract | Address |
|----------|---------|
| Pool | `0x3E59A31363E2ad014dcbc521c4a0d5757d9f3402` |
| PoolAddressesProvider | `0x9F7Cf9417D5251C59fE94fB9147feEe1aAd9Cea5` |
| PoolConfigurator | `0x7567E3434CC1BEf724AB595e6072367Ef4914691` |
| AaveOracle | `0x1e693D088ceFD1E95ba4c4a5F7EeA41a1Ec37e8b` |
| ACLManager | `0x7a12dCfd73C1B4cddf294da4cFce75FcaBBa314C` |
| ProtocolDataProvider | `0x2e0f8D3B1631296cC7c56538D6Eb6032601E15ED` |
| UIPoolDataProvider | `0xe48424542b30b0b8D1Dc09099aceE407f40b4491` |
| WalletBalanceProvider | `0xB91DA65093d54a1a7cb0fe684860F568A5E57123` |

### Supported Assets

USDC, USDT, EURm (cEUR), USDm (cUSD), CELO, WETH

### Supply/Borrow Pattern

```typescript
import { parseUnits } from "viem";

const AAVE_POOL = "0x3E59A31363E2ad014dcbc521c4a0d5757d9f3402";
const USDC = "0xcebA9300f2b948710d2653dD7B07f33A8B32118C";
// NOTE: the USDC constant above is the token address — correct for balances/approvals/transfers.
// If you pay gas in USDC via `feeCurrency`, use the adapter `0x2F25deB3848C207fc8E0c34035B3Ba7fC157602B`
// instead. See builder-guide.md → Allowed Fee Currencies.

// 1. Approve USDC to Pool
await walletClient.writeContract({
  address: USDC,
  abi: erc20Abi,
  functionName: "approve",
  args: [AAVE_POOL, parseUnits("100", 6)],
});

// 2. Supply USDC
await walletClient.writeContract({
  address: AAVE_POOL,
  abi: aavePoolAbi,
  functionName: "supply",
  args: [
    USDC,                    // asset
    parseUnits("100", 6),    // amount
    userAddress,             // onBehalfOf
    0,                       // referralCode
  ],
});

// 3. Borrow USDm against USDC collateral
await walletClient.writeContract({
  address: AAVE_POOL,
  abi: aavePoolAbi,
  functionName: "borrow",
  args: [
    "0x765DE816845861e75A25fCA122bb6898B8B1282a", // USDm
    parseUnits("50", 18),                          // amount
    2,                                             // interestRateMode (2=variable)
    0,                                             // referralCode
    userAddress,                                   // onBehalfOf
  ],
});
```

### Read Pool Data

```typescript
// Get user account data
const userData = await publicClient.readContract({
  address: AAVE_POOL,
  abi: aavePoolAbi,
  functionName: "getUserAccountData",
  args: [userAddress],
});
// Returns: totalCollateralBase, totalDebtBase, availableBorrowsBase,
//          currentLiquidationThreshold, ltv, healthFactor
```

### Fetching Live APY (Supply & Borrow Rates)

Two options:

**Option A — On-chain via UIPoolDataProvider (read-only, no indexer):**

```typescript
import { createPublicClient, http, formatUnits } from "viem";
import { celo } from "viem/chains";

const UI_POOL_DATA_PROVIDER = "0xe48424542b30b0b8D1Dc09099aceE407f40b4491";
const POOL_ADDRESSES_PROVIDER = "0x9F7Cf9417D5251C59fE94fB9147feEe1aAd9Cea5";

const client = createPublicClient({ chain: celo, transport: http() });

const [reservesData] = await client.readContract({
  address: UI_POOL_DATA_PROVIDER,
  abi: uiPoolDataProviderAbi, // from @aave/contract-helpers, or declare manually
  functionName: "getReservesData",
  args: [POOL_ADDRESSES_PROVIDER],
});

// Each reserve has liquidityRate (supply APR) and variableBorrowRate (borrow APR) in RAY (1e27),
// both expressed as a per-second rate.
for (const r of reservesData) {
  const supplyAPR = Number(formatUnits(r.liquidityRate, 27)) * 100;
  const borrowAPR = Number(formatUnits(r.variableBorrowRate, 27)) * 100;
  console.log(r.symbol, { supplyAPR, borrowAPR });
}
```

> Rates from `UIPoolDataProvider` are **per-second in RAY (1e27)** — the snippet above converts to a simple annualized percentage. For the exact compounding formula Aave UI uses: `(1 + ratePerSecond)^SECONDS_PER_YEAR - 1`. See Aave V3 docs.

**Option B — Off-chain via Aave V3 Subgraph (if available for Celo):**

Check `https://thegraph.com/explorer` for the current Celo-Aave-V3 subgraph slug. Query shape:

```graphql
{
  reserves {
    symbol
    liquidityRate
    variableBorrowRate
    totalLiquidity
    totalCurrentVariableDebt
  }
  _meta { block { number } }
}
```

> ⚠️ Subgraph availability on Celo has historically lagged other chains. Always verify the subgraph is live and fresh (check `_meta.block.number` vs current block) before relying on it. Default to on-chain reads for critical paths.

**Which to use:** on-chain read is authoritative and latency-sensitive apps should prefer it. Subgraph is cheaper for UIs displaying many reserves with historical context.

---

## Morpho Blue

Permissionless lending with isolated markets. No governance needed to create markets.

### Contracts (Mainnet)

| Contract | Address |
|----------|---------|
| Morpho Blue | `0xd24ECdD8C1e0E57a4E26B1a7bbeAa3e95466A569` |

### Market Structure

Each Morpho market is defined by:
- **Loan token** — what you borrow
- **Collateral token** — what you deposit
- **Oracle** — price feed for liquidation
- **IRM** — interest rate model
- **LLTV** — liquidation loan-to-value ratio

### Market Interaction

```typescript
const MORPHO = "0xd24ECdD8C1e0E57a4E26B1a7bbeAa3e95466A569";

// Supply collateral
await walletClient.writeContract({
  address: MORPHO,
  abi: morphoAbi,
  functionName: "supplyCollateral",
  args: [marketParams, amount, userAddress, "0x"],
});

// Borrow
await walletClient.writeContract({
  address: MORPHO,
  abi: morphoAbi,
  functionName: "borrow",
  args: [marketParams, amount, 0n, userAddress, userAddress],
});
```

**UI**: https://app.morpho.org (filter by Celo)

---

## Mento (Stablecoin Protocol)

Celo-native stablecoin protocol powering 15+ local currency stablecoins.

### How It Works

- Mento uses a Reserve of crypto assets to back stablecoins
- Users can mint/burn stablecoins through the Broker contract
- Exchange rates come from SortedOracles (multiple oracle reporters)
- Each stablecoin has its own Exchange contract

### Mento V2 Contracts (BiPool System — Mainnet)

| Contract | Address |
|----------|---------|
| Broker | `0x777A8255cA72412f0d706dc03C9D1987306B4CaD` |
| BiPoolManager | `0x22d9db95E6Ae61c104A7B6F6C78D7993B94ec901` |
| Reserve | `0x9380fA34Fd9e4Fd14c06305fd7B6199089eD4eb9` |
| SortedOracles | `0xefB84935239dAcdecF7c5bA76d8dE40b077B7b33` |
| BreakerBox | `0x303ED1df62Fa067659B586EbEe8De0EcE824Ab39` |

### Mento V3 Contracts (FPMM — Mainnet)

| Contract | Address |
|----------|---------|
| FPMMFactory | `0xa849b475FE5a4B5C9C3280152c7a1945b907613b` |
| Router | `0x4861840C2EfB2b98312B0aE34d86fD73E8f9B6f6` |
| OracleAdapter | `0xa472fBBF4b890A54381977ac392BdF82EeC4383a` |
| ReserveV2 | `0x4255Cf38e51516766180b33122029A88Cb853806` |
| MENTO Token | `0x7FF62f59e3e89EA34163EA1458EEBCc81177Cfb6` |
| veMENTO | `0x001Bb66636dCd149A1A2bA8C50E408BdDd80279C` |
| Governor | `0x47036d78bB3169b4F5560dD77BF93f4412A59852` |
| Timelock | `0x890DB8A597940165901372Dd7DB61C9f246e2147` |

### Key FPMM Pools (Mainnet)

| Pool | Address |
|------|---------|
| USDC/USDm | `0x462fe04b4FD719Cbd04C0310365D421D02AaA19E` |
| USDT/USDm | `0x0FEBa760d93423D127DE1B6ABECdB60E5253228D` |
| GBPm/USDm | `0x8C0014afe032E4574481D8934504100bF23fCB56` |

### Mento SDK v3

```typescript
import { Mento, ChainId } from "@mento-protocol/mento-sdk";
const mento = await Mento.create(ChainId.CELO);
// Services: mento.tokens, mento.pools, mento.routes, mento.quotes, mento.swap
```

### Mento App

Swap between Mento stablecoins at: https://app.mento.org

### Building with Local Stablecoins

6 USD-pegged + 20 regional currency stablecoins available on Celo.

- Docs: https://docs.celo.org/build-on-celo/build-with-local-stablecoin
- All Mento token addresses: see `contracts.md`

---

## stCELO (Liquid Staking)

Liquid staking derivative for CELO. Deposit CELO → receive stCELO (accrues value over time).

### Key Info

| Property | Value |
|----------|-------|
| stCELO Proxy | `0xC668583dcbDc9ae6FA3CE46462758188adfdfC24` |
| stCELO Manager | `0x0239b96D10a434a56CC9E09383077A0490cF9398` |
| Exchange Rate | NOT 1:1 — stCELO accrues value (~0.9 stCELO per CELO) |
| Website | https://stcelo.xyz |

### Staking Flow

```solidity
// Deposit CELO → receive stCELO
IStCeloManager(manager).deposit{value: celoAmount}();

// Withdraw stCELO → receive CELO (may be delayed)
IStCeloManager(manager).withdraw(stCeloAmount);
```

**Gotcha**: `deposit()` sends native CELO via `msg.value`. On Foundry forks, pre-fund the contract with `vm.deal()` because the `0xfd` precompile doesn't work.

---

## Ubeswap

Leading Celo-native DEX (mobile-optimized). Both V2 and V3 deployed.

### Contracts (Mainnet)

| Contract | Address |
|----------|---------|
| V3 Factory | `0x67FEa58D5a5a4162cED847E13c2c81c73bf8aeC4` |
| V3 Universal Router | `0x3C255DED9B25f0BFB4EF1D14234BD2514d7A7A0d` |
| V3 NFT Position Manager | `0x897387c7B996485c3AAa85c94272Cd6C506f8c8F` |
| V2 Factory | `0x62d5b84bE28a183aBB507E125B384122D2C25fAE` |
| V2 Router | `0xE3D8bd6Aed4F159bc8000a9cD47CffDb95F96121` |
| UBE Token | `0x71e26d0E519D14591b9dE9a0fE9513A398101490` |
| V3 Farm Protocol | `0xA6E9069CB055a425Eb41D185b740B22Ec8f51853` |

Website: https://ubeswap.org

---

## Velodrome V3

Concentrated liquidity DEX with ve-tokenomics, deployed on Celo.

Website: https://velodrome.finance (filter to Celo)

---

## Curve

Efficient stablecoin swaps on Celo.

Website: https://curve.finance (filter to Celo)

---

## Common DeFi Patterns on Celo

### 1. Stablecoin Swap
Use Uniswap V3 or Mento for swapping between stablecoins (USDm ↔ USDC ↔ USDT).

### 2. Yield Farming
- Supply to Aave V3 → earn interest
- Provide liquidity on Uniswap → earn fees + Merkl rewards
- Use Beefy for autocompounding

### 3. Leveraged Staking
- Deposit stCELO as collateral on Morpho Blue
- Borrow CELO
- Stake borrowed CELO for more stCELO
- Repeat (loop)

### 4. Flash Loans
Aave V3 supports flash loans on Celo. Useful for liquidations, arbitrage, and collateral swaps.

### 5. Oracle Integration
- **Chainlink**: Standard price feeds
- **RedStone**: Pull-based oracle with wide asset coverage
- **Band Protocol**: Live on Celo L2 from day one

Oracle docs: https://docs.celo.org/tooling/oracles/index
