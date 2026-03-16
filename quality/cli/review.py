from quality.review.reviewer import Reviewer


def handle_reviewer(args):
    if args.pr_number is None:
        raise ValueError("PR number is required.")

    owner = args.repo.split("/")[0]
    repo = args.repo.split("/")[1]

    reviewer = Reviewer(args.harshness)
    reviewer.checkout_pr(
        prnumber=args.pr_number,
        owner=owner,
        repo=repo,
    )
    reviewer.review_files(agent=args.agent, model=args.model)
