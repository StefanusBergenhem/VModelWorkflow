#!/usr/bin/env bash
#
# sync-requirements-shape-checklist.sh
#
# Propagate the canonical requirements-shape-checklist.md to every affected
# skill bundle (framework path + vmodel-core mirror) and verify md5 parity
# across all copies.
#
# The canonical lives at docs/requirements-shape-checklist.md and is the
# source of truth. Each affected skill ships a verbatim copy at
# references/requirements-shape-checklist.md so the skill bundles are
# self-contained.
#
# Idempotent: running twice produces the same state.
# Failure modes: missing canonical, missing skill directories, missing
# references/ subdirectories, or md5 drift after copy → script exits
# non-zero with a loud diagnostic.
#
set -euo pipefail

# --- Config ---------------------------------------------------------------

CANONICAL="/home/stefanus/repos/VModelWorkflow/docs/requirements-shape-checklist.md"
FRAMEWORK_ROOT="/home/stefanus/repos/VModelWorkflow/.claude/skills"
MIRROR_ROOT="/home/stefanus/repos/vmodel-core/.claude/skills"

# Affected skills: the two skills that consume the requirements-shape
# checklist as a peer-spec sanity check at authoring time.
SKILLS=(
  "vmodel-skill-author-adr"
  "vmodel-skill-author-architecture"
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

  cp "$CANONICAL" "$fw_refs/requirements-shape-checklist.md"
  cp "$CANONICAL" "$mr_refs/requirements-shape-checklist.md"
done

# --- Verify md5 parity across all 5 paths ---------------------------------

ALL_PATHS=("$CANONICAL")
for skill in "${SKILLS[@]}"; do
  ALL_PATHS+=("$FRAMEWORK_ROOT/$skill/references/requirements-shape-checklist.md")
  ALL_PATHS+=("$MIRROR_ROOT/$skill/references/requirements-shape-checklist.md")
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
