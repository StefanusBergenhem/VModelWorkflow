#!/usr/bin/env bash
#
# sync-partial-parent-protocol.sh
#
# Propagate the canonical partial-parent-protocol.md to every author skill
# bundle (framework path + vmodel-core mirror) and verify md5 parity across
# all copies.
#
# The canonical lives at docs/partial-parent-protocol.md and is the source of
# truth. Each author skill ships a verbatim copy at
# references/partial-parent-protocol.md so the skill bundles are self-contained
# at runtime (skills do not read TARGET_ARCHITECTURE or this canonical
# directly).
#
# Idempotent: running twice produces the same state.
# Failure modes: missing skill directories, missing references/ subdirectories,
# or md5 drift after copy → script exits non-zero with a loud diagnostic.
#
set -euo pipefail

# --- Config ---------------------------------------------------------------

CANONICAL="/home/stefanus/repos/VModelWorkflow/docs/partial-parent-protocol.md"
FRAMEWORK_ROOT="/home/stefanus/repos/VModelWorkflow/.claude/skills"
MIRROR_ROOT="/home/stefanus/repos/vmodel-core/.claude/skills"

# Five author skills only — the protocol is consumed by author skills; review
# skills accept documented deviations via existing finding shapes and do not
# need their own copy.
SKILLS=(
  "vmodel-skill-author-requirements"
  "vmodel-skill-author-architecture"
  "vmodel-skill-author-detailed-design"
  "vmodel-skill-author-testspec"
  "vmodel-skill-author-adr"
)

# --- Pre-flight -----------------------------------------------------------

if [[ ! -f "$CANONICAL" ]]; then
  echo "ERROR: canonical source not found: $CANONICAL" >&2
  exit 1
fi

CANONICAL_MD5=$(md5sum "$CANONICAL" | awk '{print $1}')

# --- Sync -----------------------------------------------------------------

for skill in "${SKILLS[@]}"; do
  fw_refs="$FRAMEWORK_ROOT/$skill/references"
  mr_refs="$MIRROR_ROOT/$skill/references"

  if [[ ! -d "$fw_refs" ]]; then
    echo "ERROR: framework references/ missing for $skill: $fw_refs" >&2
    exit 1
  fi
  if [[ ! -d "$mr_refs" ]]; then
    echo "ERROR: mirror references/ missing for $skill: $mr_refs" >&2
    exit 1
  fi

  cp "$CANONICAL" "$fw_refs/partial-parent-protocol.md"
  cp "$CANONICAL" "$mr_refs/partial-parent-protocol.md"
done

# --- Verify md5 parity across all 11 paths --------------------------------

ALL_PATHS=("$CANONICAL")
for skill in "${SKILLS[@]}"; do
  ALL_PATHS+=("$FRAMEWORK_ROOT/$skill/references/partial-parent-protocol.md")
  ALL_PATHS+=("$MIRROR_ROOT/$skill/references/partial-parent-protocol.md")
done

drift=0
for p in "${ALL_PATHS[@]}"; do
  m=$(md5sum "$p" | awk '{print $1}')
  if [[ "$m" != "$CANONICAL_MD5" ]]; then
    echo "DRIFT: $p has md5 $m, expected $CANONICAL_MD5" >&2
    drift=1
  fi
done

if [[ $drift -ne 0 ]]; then
  echo "ERROR: md5 drift detected; sync incomplete." >&2
  exit 1
fi

echo "synced ${#SKILLS[@]} skills (framework + mirror); all md5s match canonical"
