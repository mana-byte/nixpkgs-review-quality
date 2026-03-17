# nixpkgs-review-quality

Automate Nixpkgs PR reviews to reduce repetitive manual checks.

## Features

- Automated review assistance using LLMs
- Simple CLI for GitHub interaction
- Review point database for prompt engineering

## Requirements

- GitHub access token (`ACCESS_TOKEN`)
- API key from OpenAI or Mistral AI (`MISTRAL_API_KEY` or `OPEN_AI_API_KEY`)

## Usage

```bash
# Use nix (obviously)
nix develop github:mana-byte/nixpkgs-review-quality

# Help
nixpkgs-review-quality pr -h
    positional arguments:
      pr_number             The number of the pull request to review (required).

    options:
      -h, --help            show this help message and exit
      --post-review         Whether to post the review on GitHub after generating it (default: False). If not set, the review will only be printed to the console.
      --agent, -a {AGENTS.MISTRAL,AGENTS.OPEN_AI}
                            The agent to use for the review. Possible values: ['MISTRAL', 'OPEN_AI'].
      --model, -m MODEL     The model to use for the review (default: devstral-latest).
      --harshness {1,2,3,4,5}
                            Review strictness (1-5, default: 5). Only review points with importance < harshness will be considered.
      --repo, -r REPO       Repository in format owner/repo (default: NixOS/nixpkgs).
      --review-type {REVIEW_TYPE.COMMENT,REVIEW_TYPE.APPROVE,REVIEW_TYPE.REQUEST_CHANGES}
                            Type of review to submit (default: COMMENT).
      --message MESSAGE     Additional message to include in the review body.
      --save-report SAVE_REPORT
                            Save the generated review report to a given file.

# Submit review directly (Only works with write access)
nixpkgs-review-quality pr <PR_NUMBER> --post-review

# Save review to file
nixpkgs-review-quality pr <PR_NUMBER> --save-report report.md
```

**Note**: If you are using OPEN AI models you will need to add

```bash
nixpkgs-review-quality pr <PR_NUMBER> -a OPEN_AI -m "some model"
```

Because by default these are set to `-a MISTRAL -m "devstral-latest"`

## Examples

```bash
# Review PR from personal fork
nixpkgs-review-quality pr 2 -r mana-byte/nixpkgs --post-review
```

Check results at
[mana-byte/nixpkgs#2](https://github.com/mana-byte/nixpkgs/pull/2)

```bash
# Review a random Python PR
nixpkgs-review-quality pr 475398 --save-report .
```

## Roadmap

- Check dependencies and build-system with original repo
- Expand review point database and clear it
- Support local Nix expressions review
- Add Go and Rust builders
- Review commit message format

