import json
from pathlib import Path

# Directory containing individual text files
text_dir = Path("data/processed/text")
# Output combined file in knowledge_base directory
combined_file = Path(__file__).resolve().parents[2] / "src" / "knowledge_base" / "combined_restaurants.txt"

# Read and concatenate all .txt files
all_lines = []
for txt in sorted(text_dir.glob("*.txt")):
    # Add separator header
    all_lines.append(f"# {txt.name}")
    # Read content
    content = txt.read_text(encoding="utf-8").splitlines()
    all_lines.extend(content)
    all_lines.append("")  # blank line between files

# Ensure output directory exists
combined_file.parent.mkdir(parents=True, exist_ok=True)
# Write combined content
combined_file.write_text("\n".join(all_lines), encoding="utf-8")
print(f"Wrote {len(all_lines)} lines to {combined_file}")
