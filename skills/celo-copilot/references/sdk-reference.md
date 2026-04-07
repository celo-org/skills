# Celo SDK Quick Reference

> Sources: docs.celo.org/tooling/libraries-sdks/*, celo-org/agent-skills

---

## Viem (Recommended)

Viem has first-class Celo support with `feeCurrency` for CIP-64 transactions.

**Install**: `npm install viem`

### Celo-Specific Features

| Feature | Usage |
|---------|-------|
| Chain export | `import { celo, celoSepolia } from "viem/chains"` |
| Fee abstraction | `feeCurrency` field on `sendTransaction` |
| Gas estimation | Pass `feeCurrency` to `estimateGas` |
| Gas price in token | `eth_gasPrice` with fee currency param |
| CIP-64 tx type | Automatic when `feeCurrency` is set |

### Key Patterns

```typescript
import { createPublicClient, createWalletClient, http, custom } from "viem";
import { celo } from "viem/chains";

// Public client (read-only)
const publicClient = createPublicClient({
  chain: celo,
  transport: http(),
});

// Wallet client (browser)
const walletClient = createWalletClient({
  chain: celo,
  transport: custom(window.ethereum),
});

// Send with fee abstraction
await walletClient.sendTransaction({
  to: "0x...",
  value: 0n,
  feeCurrency: "0x765DE816845861e75A25fCA122bb6898B8B1282a",
});

// Read contract
await publicClient.readContract({
  address: "0x...",
  abi: myAbi,
  functionName: "myFunction",
  args: [arg1, arg2],
});

// Write contract
await walletClient.writeContract({
  address: "0x...",
  abi: myAbi,
  functionName: "myFunction",
  args: [arg1, arg2],
  feeCurrency: "0x765DE816845861e75A25fCA122bb6898B8B1282a",
});
```

**Docs**: https://docs.celo.org/tooling/libraries-sdks/viem/index

---

## Wagmi (React Hooks)

Wagmi provides React hooks for wallet connection, contract reads/writes, and transaction sending — all with Celo support.

**Install**: `npm install wagmi viem @tanstack/react-query`

### Key Hooks

| Hook | Purpose |
|------|---------|
| `useAccount` | Get connected address and chain |
| `useConnect` | Connect wallet |
| `useDisconnect` | Disconnect wallet |
| `useSendTransaction` | Send transaction (supports `feeCurrency`) |
| `useReadContract` | Read contract state |
| `useWriteContract` | Write to contract |
| `useWaitForTransactionReceipt` | Wait for tx confirmation |
| `useBalance` | Get native balance |

### Fee Abstraction with Wagmi

```tsx
import { useSendTransaction, useWaitForTransactionReceipt } from "wagmi";

function PayWithUSDm() {
  const { data: hash, sendTransaction } = useSendTransaction();
  const { isSuccess } = useWaitForTransactionReceipt({ hash });

  return (
    <button onClick={() => sendTransaction({
      to: "0xRecipient",
      value: 0n,
      feeCurrency: "0x765DE816845861e75A25fCA122bb6898B8B1282a",
    })}>
      {isSuccess ? "Sent!" : "Send (gas in USDm)"}
    </button>
  );
}
```

**Docs**: https://docs.celo.org/tooling/libraries-sdks/wagmi (if available) or https://wagmi.sh

---

## ContractKit (Legacy)

ContractKit is Celo's original SDK. **Use viem instead for new projects.** ContractKit is only needed for:
- Legacy governance contract interactions
- ODIS phone number privacy
- Old Celo-specific contracts not on the OP Stack

**Install**: `npm install @celo/contractkit`

```typescript
import { newKit } from "@celo/contractkit";

const kit = newKit("https://forno.celo.org");
const accounts = await kit.web3.eth.getAccounts();

// Governance interactions
const governance = await kit.contracts.getGovernance();
const proposals = await governance.getDequeue();

// Election voting
const election = await kit.contracts.getElection();
const validators = await election.getValidatorGroupsVotes();
```

**Docs**: https://docs.celo.org/tooling/libraries-sdks/contractkit/index

---

## Composer Kit (UI Components)

Pre-built React components themed for Celo dApps.

**Install**: Check https://docs.celo.org/tooling/libraries-sdks/composer-kit for latest install instructions.

**Docs**: https://docs.celo.org/tooling/libraries-sdks/composer-kit

---

## Thirdweb SDK

Full-stack Web3 SDK with 500+ wallet options, prebuilt UI, and one-click deploy.

**Install**: `npm install thirdweb`

```typescript
import { createThirdwebClient, getContract } from "thirdweb";
import { celo } from "thirdweb/chains";

const client = createThirdwebClient({ clientId: "YOUR_CLIENT_ID" });

const contract = getContract({
  client,
  chain: celo,
  address: "0xContractAddress",
});
```

**Docs**: https://docs.celo.org/tooling/libraries-sdks/thirdweb-sdk/index

---

## Ethers.js

Standard ethers.js works with Celo. No special configuration needed beyond the RPC URL.

**Install**: `npm install ethers`

```typescript
import { ethers } from "ethers";

const provider = new ethers.JsonRpcProvider("https://forno.celo.org");
const balance = await provider.getBalance("0xAddress");
```

Note: ethers.js does NOT have native `feeCurrency` support. Use viem for fee abstraction.

**Docs**: https://docs.celo.org/tooling/libraries-sdks/ethers/index

---

## Web3.js

Standard web3.js works with Celo.

**Install**: `npm install web3`

Note: Like ethers.js, web3.js does NOT have native `feeCurrency` support. Use viem for fee abstraction.

**Docs**: https://docs.celo.org/tooling/libraries-sdks/web3/index

---

## Wallet Integration Libraries

| Library | Use Case | Docs |
|---------|----------|------|
| Reown (WalletConnect) | Multi-wallet connection | https://docs.celo.org/tooling/libraries-sdks/reown/index |
| Dynamic | Embedded wallets + social login | https://docs.celo.org/tooling/libraries-sdks/dynamic/index |
| JAW | Wallet abstraction | https://docs.celo.org/tooling/libraries-sdks/jaw/index |
| Portal | Wallet infrastructure | https://docs.celo.org/tooling/libraries-sdks/portal/index |

---

## When to Use What

```
Need fee abstraction?
  └── Yes → Viem (only SDK with native feeCurrency support)
  └── No → Any SDK works

Building React dApp?
  └── Yes → Wagmi + RainbowKit (+ viem under the hood)
  └── No → Viem directly

Need embedded wallets / social login?
  └── Yes → Thirdweb or Dynamic
  └── No → Standard wallet connection

Interacting with old Celo governance?
  └── Yes → ContractKit
  └── No → Don't use ContractKit

Quick prototype?
  └── Yes → Thirdweb (prebuilt UI + dashboard)
  └── No → Viem + Wagmi for full control
```
