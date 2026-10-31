"""Generate three fictional PaisaPath sample advertisements."""

from app.config import OUTPUT_DIR
from app.content_generator import prepare_copy
from app.template_renderer import render_creative

SAMPLES = (
    {
        "creative_id": "sample-english",
        "product": "Money planning tools",
        "audience": "Everyday planners",
        "offer": "Example offer for demonstration only",
        "language": "English",
    },
    {
        "creative_id": "sample-hindi",
        "product": "पैसों की योजना",
        "audience": "रोज़मर्रा के योजनाकार",
        "offer": "यह केवल प्रदर्शन के लिए एक उदाहरण है।",
        "language": "Hindi",
    },
    {
        "creative_id": "sample-marathi",
        "product": "पैशांचे नियोजन",
        "audience": "दररोज नियोजन करणारे",
        "offer": "हे केवळ प्रात्यक्षिकासाठी एक उदाहरण आहे.",
        "language": "Marathi",
    },
)


def main() -> None:
    """Generate each sample and report its result."""
    output_dir = OUTPUT_DIR / "samples"
    print("Generating PaisaPath sample creatives...")

    for sample in SAMPLES:
        try:
            copy_data = prepare_copy(sample)
            output_path = render_creative(copy_data, output_dir)
        except (OSError, ValueError) as error:
            print(f"ERROR {sample['creative_id']}: {error}")
        else:
            print(f"SAVED {output_path}")


if __name__ == "__main__":
    main()