# MiniPay Development Guide

> Source: docs.celo.org/build-on-celo/build-on-minipay/*

MiniPay is a non-custodial stablecoin wallet integrated into Opera Mini and available as a standalone app on Android and iOS. It's the fastest growing wallet in the Global South with 14M+ activations, 300M+ stablecoin transactions, available in 60+ countries.

> Wallet counts are updated by the MiniPay team via the MiniPay site and Celo blog. If a precise current number is needed, prefer fetching from those sources over the number above.

- Android: https://play.google.com/store/apps/details?id=com.opera.minipay
- iOS: https://apps.apple.com/de/app/minipay-easy-global-wallet/id6504087257

### Live Mini Apps in discovery (for builders)

To see **what is already shipping** in MiniPay (categories, publishers, deep links) and how **country targeting** works, use the skill reference **`minipay-live-apps.md`**. It is a **snapshot** from the discovery export, **not** a live API — and **not every app is available in every country**; the reference documents whitelist/blacklist hints from the export.

---

## Quickstart

### Scaffold a Mini App

```bash
npx @celo/celo-composer@latest create -t minipay
```

> **Prefer a raw Next.js setup without Composer?** See `minipay-scaffold-from-scratch.md` for a minimal `create-next-app` + viem + ngrok path — useful for integrating MiniPay into an existing Next.js project or skipping Composer's monorepo/Hardhat scaffolding.

### Requirements

- TypeScript v5+
- Viem v2+
- Physical Android or iOS device (emulators do NOT work)
- ngrok for local testing

### Install Dependencies

```bash
npm install viem@2 @celo/abis @celo/identity
```

---

## MiniPay Detection

Check if your dApp is running inside MiniPay:

```typescript
function isMiniPay(): boolean {
  return typeof window !== "undefined"
    && window.ethereum !== undefined
    && window.ethereum.isMiniPay === true;
}
```

---

## Wallet Connection

### Without Any Library (simplest)

```typescript
import { createWalletClient, custom } from "viem";
import { celo, celoSepolia } from "viem/chains";

const client = createWalletClient({
  chain: celo,
  transport: custom(window.ethereum),
});

const [address] = await client.getAddresses();
```

### With Wagmi (React)

```typescript
import { useConnect } from "wagmi";
import { injected } from "wagmi/connectors";

// Auto-connect in MiniPay (no connect button needed)
useEffect(() => {
  if (window.ethereum?.isMiniPay) {
    connect({ connector: injected({ target: "metaMask" }) });
  }
}, []);
```

### Conditional Connect Button

```tsx
const [hideConnectBtn, setHideConnectBtn] = useState(false);

useEffect(() => {
  if (window.ethereum?.isMiniPay) {
    setHideConnectBtn(true);
    connect({ connector: injected({ target: "metaMask" }) });
  }
}, []);

// Only show connect button outside MiniPay
{!hideConnectBtn && <ConnectButton />}
```

---

## Supported Stablecoins

| Token | Symbol | Token Address | Decimals | `feeCurrency` (for gas) |
|-------|--------|---------------|----------|-------------------------|
| Mento Dollar | USDm (cUSD) | `0x765DE816845861e75A25fCA122bb6898B8B1282a` | 18 | `0x765DE816845861e75A25fCA122bb6898B8B1282a` (same) |
| USDC | USDC | `0xcebA9300f2b948710d2653dD7B07f33A8B32118C` | 6 | `0x2F25deB3848C207fc8E0c34035B3Ba7fC157602B` (**adapter**) |
| USDT | USDT | `0x48065fbBE25f71C9282ddf5e1cD6D6A887483D5e` | 6 | `0x0e2a3e05bc9a16f5292a6170456a710cb89c6f72` (**adapter**) |

**Important — two separate things**:

1. **Decimals**: USDm has 18 decimals; USDC/USDT have 6. Always check decimals before displaying amounts.
2. **Fee abstraction**: For **balances, transfers, and approvals**, use the **Token Address** column. For the **`feeCurrency` transaction field** (paying gas in stablecoins), use the **`feeCurrency` adapter address** — USDC/USDT transactions will **fail** if you pass the token address instead of the adapter. See `builder-guide.md` → _Allowed Fee Currencies (Mainnet)_ for the canonical table and underlying mechanics (CIP-64, FeeCurrencyDirectory).

> **Bridged-token caveat:** the decimals above are for the **canonical** USDC/USDT on Celo. Bridged variants from other chains may have different decimals or different contract addresses. Always verify against the token's contract on Celoscan before integrating.

---

## Check Token Balance

```typescript
import { createPublicClient, http, formatUnits } from "viem";
import { celo } from "viem/chains";

const USDM_ADDRESS = "0x765DE816845861e75A25fCA122bb6898B8B1282a";

const ERC20_ABI = [
  {
    name: "balanceOf",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "account", type: "address" }],
    outputs: [{ name: "", type: "uint256" }],
  },
] as const;

const publicClient = createPublicClient({
  chain: celo,
  transport: http(),
});

const balance = await publicClient.readContract({
  address: USDM_ADDRESS,
  abi: ERC20_ABI,
  functionName: "balanceOf",
  args: [userAddress],
});

const formatted = formatUnits(balance, 18); // "12.50"
```

---

## Send Stablecoin Payment

```typescript
import { createWalletClient, custom, encodeFunctionData, parseUnits } from "viem";
import { celo } from "viem/chains";

const USDM_ADDRESS = "0x765DE816845861e75A25fCA122bb6898B8B1282a";

const ERC20_ABI = [
  {
    name: "transfer",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "to", type: "address" },
      { name: "value", type: "uint256" },
    ],
    outputs: [{ name: "", type: "bool" }],
  },
] as const;

const walletClient = createWalletClient({
  chain: celo,
  transport: custom(window.ethereum),
});

const [address] = await walletClient.getAddresses();

const data = encodeFunctionData({
  abi: ERC20_ABI,
  functionName: "transfer",
  args: [recipientAddress, parseUnits("1.00", 18)], // Send 1 USDm
});

const txHash = await walletClient.sendTransaction({
  account: address,
  to: USDM_ADDRESS,
  data,
  // Pay gas with USDm (fee abstraction)
  feeCurrency: USDM_ADDRESS,
});
```

---

## Gas Estimation with Fee Currency

MiniPay users pay gas in stablecoins. Estimate gas cost in USDm:

```typescript
// Estimate gas units
const gasEstimate = await publicClient.estimateGas({
  account: address,
  to: USDM_ADDRESS,
  data,
  feeCurrency: USDM_ADDRESS,
});

// Get gas price in USDm
const gasPrice = await publicClient.request({
  method: "eth_gasPrice",
  params: [USDM_ADDRESS], // Pass fee currency address
});

// Calculate total fee
const totalFee = gasEstimate * BigInt(gasPrice);
const feeFormatted = formatUnits(totalFee, 18); // e.g., "0.0001"
```

---

## Phone Number → Address Resolution

Resolve **E.164** numbers (e.g. `+14155552671`) to wallet addresses using **ODIS (PnP)** + **FederatedAttestations**. MiniPay mappings are attested under issuer **`0x7888612486844Bb9BE598668081c59A9f7367FBc`** (pass this as a **trusted issuer**, not as the ODIS quota account).

- **Quota**: Mainnet PnP queries need **non-zero `remainingQuota`**. A **USDm/cUSD balance alone is not enough** — you usually must **`payInCUSD`** on **OdisPayments** after **`increaseAllowance`** on the stable token. See **`odis-socialconnect.md`** for the full quota flow and contract addresses (`contracts.md`).

**Pattern** (ContractKit + `@celo/identity`; typical for **backend** signers — use **DEK / wallet signing** appropriately in Mini Apps):

```typescript
import { newKit } from "@celo/contractkit";
import { OdisUtils } from "@celo/identity";
import type { AuthSigner } from "@celo/identity/lib/odis/query";

const MINIPAY_ISSUER = "0x7888612486844Bb9BE598668081c59A9f7367FBc";

const kit = newKit("https://forno.celo.org");
kit.addAccount(walletPrivateKey); // 0x-prefixed hex
const locals = kit.connection.getLocalAccounts();
kit.defaultAccount = locals[0];
const quotaAccount = locals[0];

const serviceContext = OdisUtils.Query.getServiceContext(
  OdisUtils.Query.OdisContextName.MAINNET,
  OdisUtils.Query.OdisAPI.PNP,
);

const authSigner: AuthSigner = {
  authenticationMethod: OdisUtils.Query.AuthenticationMethod.WALLET_KEY,
  contractKit: kit,
};

const { obfuscatedIdentifier } =
  await OdisUtils.Identifier.getObfuscatedIdentifier(
    phoneE164,
    OdisUtils.Identifier.IdentifierPrefix.PHONE_NUMBER,
    quotaAccount,
    authSigner,
    serviceContext,
  );

const federated = await kit.contracts.getFederatedAttestations();
const { accounts } = await federated.lookupAttestations(obfuscatedIdentifier, [
  MINIPAY_ISSUER,
]);
// accounts[0] is the resolved address when an attestation exists
```

**Install**: `npm install @celo/contractkit @celo/identity`

See **`references/odis-socialconnect.md`** for troubleshooting, **DEK (`ENCRYPTION_KEY`)** auth, viem alternatives, and doc links.

---

## Deeplinks

| Deeplink | URL | Purpose |
|----------|-----|---------|
| Add Cash | `https://minipay.opera.com/add_cash` | Open add cash screen |

---

## Testing with ngrok

MiniPay cannot access localhost. Use ngrok to expose your dev server:

```bash
# Start your dev server
npm run dev  # e.g., port 3000

# In another terminal
ngrok http 3000
```

### Configure dev server for ngrok

**Vite** (`vite.config.ts`):
```typescript
export default defineConfig({
  server: {
    allowedHosts: [".ngrok.io", ".ngrok-free.app"],
  },
});
```

**Next.js** — no special config needed, but add CORS headers if needed.

### Load in MiniPay

1. Open MiniPay on your device
2. Go to Settings > About > tap Version 7+ times to enable Developer Settings
3. Enable Developer Mode + Use Testnet
4. Enter your ngrok HTTPS URL in "Load Test Page"

### Remote Debugging

Connect your Android device via USB and visit `chrome://inspect` in desktop Chrome to debug the MiniPay WebView.

The ngrok dashboard at `http://localhost:4040` shows all requests for debugging.

---

## Important Constraints

1. **No emulators** — MiniPay requires a physical device
2. **Legacy transactions only** — MiniPay ignores EIP-1559 fields. Do not set `maxFeePerGas` / `maxPriorityFeePerGas`
3. **Fee abstraction** — MiniPay pays gas with USDm by default. Use `feeCurrency` parameter
4. **No message signing** — `personal_sign` and `eth_signTypedData` are not supported
5. **Small screens** — Design for mobile-first, low-bandwidth environments
6. **2MB footprint** — Keep Mini App bundle size small

---

## UX Best Practices for Emerging Markets

- Display amounts in local currency when possible (use Mento local stablecoins)
- Minimize data usage — lazy load images, compress assets
- Design for small screens (most users are on budget Android phones)
- Show clear transaction confirmations with USD equivalents
- Handle network errors gracefully (intermittent connectivity is common)
- Keep flows short — minimize steps to complete an action
- Support offline-capable patterns where possible

---

## Funding for MiniPay Builders

- **Celo Builder Fund** (Verda Ventures): $25K investment for MiniPay builders
  - Contact: team@verda.ventures
- **Proof of Ship**: Monthly rewards for consistent building
  - Subscribe: https://celo-devs.beehiiv.com/subscribe
