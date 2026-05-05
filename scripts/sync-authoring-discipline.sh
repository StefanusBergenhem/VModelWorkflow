#!/usr/bin/env bash
#
# sync-authoring-discipline.sh
#
# Propagate the canonical authoring-discipline.md to every affected skill bundle
# (framework path + vmodel-core mirror) and verify md5 parity across all copies.
#
# The canonical lives at docs/authoring-discipline.md and is the source of truth.
# Each affected skill ships a verbatim copy at references/authoring-discipline.md
# so the skill bundles are self-contained.
#
# Idempotent: running twice produces the same state.
# Failure modes: missing skill directories, missing references/ subdirectories,
# or md5 drift after copy → script exits non-zero with a loud diagnostic.
#
set -euo pipefail

# --- Config ---------------------------------------------------------------

CANONICAL="/home/stefanus/repos/VModelWorkflow/docs/authoring-discipline.md"
FRAMEWORK_ROOT="/home/stefanus/repos/VModelWorkflow/.claude/skills"
MIRROR_ROOT="/home/stefanus/repos/vmodel-core/.claude/skills"

# All ten affected skills (the architecture pair + the four other artifact pairs).
SKILLS=(
  "vmodel-skill-author-architecture"
  "vmodel-skill-author-requirements"
  "vmodel-skill-author-detailed-design"
  "vmodel-skill-author-testspec"
  "vmodel-skill-author-adr"
  "vmodel-skill-review-architecture"
  "vmodel-skill-review-requirements"
  "vmodel-skill-review-detailed-design"
  "vmodel-skill-review-testspec"
  "vmodel-skill-review-adr"
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

  cp "$CANONICAL" "$fw_refs/authoring-discipline.md"
  cp "$CANONICAL" "$mr_refs/authoring-discipline.md"
done

# --- Verify md5 parity across all 21 paths --------------------------------

ALL_PATHS=("$CANONICAL")
for skill in "${SKILLS[@]}"; do
  ALL_PATHS+=("$FRAMEWORK_ROOT/$skill/references/authoring-discipline.md")
  ALL_PATHS+=("$MIRROR_ROOT/$skill/references/authoring-discipline.md")
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
