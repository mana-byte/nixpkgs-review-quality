class ReporterService:
    """Write a human readable report for reviews in a .md file"""

    def __init__(self):
        self.report: str = ""

    def add_to_report(self, content: str) -> None:
        self.report += content + "\n\n"

    def __generate_report_str_for_review(self, review: dict[str, str]) -> str:
        content = f"### File: {review['path']}\n"
        content += f"**Line {review['line']}**: \n\n"
        content += f"{review['body']}\n"
        return content

    def produce_report_from_formatted_reviews(
        self, formatted_reviews: list[dict[str, str]]
    ) -> None:
        for review in formatted_reviews:
            self.add_to_report(self.__generate_report_str_for_review(review))

    def print_report(self) -> None:
        print(self.report)

    def save_report(self, file_path: str) -> bool:
        print(f"Saving report to {file_path}...")
        try:
            with open(file_path, "w") as f:
                _ = f.write(self.report)
            return True
        except Exception as e:
            print(f"Error saving report to {file_path}: {e}")
            return False
