# Releasing a pack

The initial public release is 1.0.0, sequence 1. Pack versions are independent of desktop versions.

1. Submit and review the data changes; ensure `Validate assets` passes.
2. Increase **both** `version` and monotonically increasing `sequence` in `manifest.json`. Update CHANGELOG. The pending 2.0.0 pack uses `engine: 2`, `schemaVersion: 1` and requires the corresponding desktop engine. Do not publish it as an engine-1 update.
3. Merge into main. Run the manual **Publish signed support pack** workflow on main. It validates fixtures and public content again, checks the version against the current stable channel, signs with the repository secret `SUPPORT_PACK_SIGNING_KEY`, updates `channel/stable.json` and publishes a versioned GitHub release.
4. In the updated app choose Settings → Device support → Check device support. Confirm the staged version, then close/reopen when existing work is complete. Test representative devices and inspect their command coverage.

Ordinary staff clients need no GitHub token or repository membership. They download public signed data only, never upload device/customer evidence here. Changing vendor files alone does not publish an update; only the signed channel is consumed.

## Recovery

In Settings choose Restore previous pack. This stages the last verified local version and pauses automatic updates. The active scan is unchanged. Close/reopen the app to apply it. Resume updates after a fixed higher-sequence release is available. Never reuse a version/sequence or force clients backwards through the online channel.

Keep the signing-key backup outside Git. Restrict repository write/admin access and workflow edits. Losing the key requires a desktop trust-root update; replacing `trust.json` in this repository does **not** change already installed clients' trusted key. A compromised key likewise requires revocation through a reviewed desktop update. This is a pinned-key signed channel with expiry/sequence protection, not a claim of full TUF key-rotation/delegation support.

A pack's download metadata is valid for 180 days. Publish a new sequence before expiry if the channel should remain fresh even when device definitions are unchanged. Existing installed packs remain usable offline. Never rotate the secret casually or paste it into issues/logs.
