from src.review.reviewer import Reviewer


def handle_reviewer(args):
    if args.pr is None:
        raise ValueError("PR number is required.")

    owner = args.repo.split("/")[0]
    repo = args.repo.split("/")[1]

    reviewer = Reviewer(args.harshness)
    reviewer.checkout_pr(
        prnumber=args.pr,
        owner=owner,
        repo=repo,
    )
    reviewer.review_files(agent=args.agent, model=args.model)
