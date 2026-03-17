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
    if not reviewer.files or reviewer.files == {}:
        return

    reviewer.review_files(agent=args.agent, model=args.model)

    if not reviewer.reviews or reviewer.reviews == {}:
        return

    if args.post_review:
        reviewer.submit_reviews(
            additional_review_message=args.message, review_type=args.review_type
        )
    elif not args.save_report:
        reviewer.print_reviews()

    if args.save_report:
        _ = reviewer.save_reviews(args.save_report)
